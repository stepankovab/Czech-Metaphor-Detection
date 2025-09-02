# Fine-tune mBERT on word-level metaphor detection
# Train on Czech df (load_czech()), evaluate on VUAMC (VUAMC.xml)

import os
import random
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

# Hugging Face
from transformers import (
    AutoTokenizer,
    AutoConfig,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    set_seed,
)
from datasets import Dataset

# Metrics
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

# ------------- 1) VUAMC loader -> pd.DataFrame(word, metaphor: bool) -------------
import xml.etree.ElementTree as ET
import pandas as pd

def load_vuamc_words(vuamc_xml_path: str, elements=-1) -> pd.DataFrame:
    """
    Parse VU Amsterdam Metaphor Corpus (TEI P5) and return a DataFrame with:
    columns: ['word', 'metaphor'] where 'metaphor' is bool.
    Includes punctuation and preserves the original token order.
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    tree = ET.parse(vuamc_xml_path)
    root = tree.getroot()

    tokens = []
    labels = []

    # Iterate over all sentences
    for s in root.findall('.//tei:s', ns):
        for child in s:
            if child.tag == f"{{{ns['tei']}}}w":  # word element
                token_text = (child.text or '').strip()
                is_met = False
                seg = child.find('tei:seg', ns)
                if seg is not None and (seg.get('type') == 'met' or seg.get('function') == 'mrw'):
                    inner_text = (seg.text or '').strip()
                    if inner_text:
                        token_text = inner_text
                    is_met = True
                if token_text:
                    tokens.append(token_text)
                    labels.append(is_met)
            elif child.tag == f"{{{ns['tei']}}}c":  # punctuation element
                token_text = (child.text or '').strip()
                if token_text:
                    tokens.append(token_text)
                    labels.append(False)

    df = pd.DataFrame({'word': tokens[:elements], 'metaphor': labels[:elements]})
    return df



from lxml import etree

def load_komet_words(vuamc_xml_path: str, elements=-1) -> pd.DataFrame:
    """
    Parse KOMET TEI XML with XInclude and return a DataFrame:
    columns: ['word', 'metaphor'] where 'metaphor' is bool.
    Includes punctuation and preserves the original token order.
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(vuamc_xml_path, parser)
    tree.xinclude()  # resolve <xi:include>
    root = tree.getroot()

    tokens = []
    labels = []

    # Iterate over all sentences
    for s in root.xpath('.//tei:s', namespaces=ns):
        for child in s:
            tag = etree.QName(child.tag).localname
            token_text = (child.text or '').strip() if child.text else ''
            if tag == 'w' and token_text:
                # check if the word is inside a metaphor segment
                is_metaphor = bool(child.xpath('ancestor::tei:seg[@type="metaphor"]', namespaces=ns))
                tokens.append(token_text)
                labels.append(is_metaphor)
            elif tag in ('c', 'pc') and token_text:
                # punctuation or whitespace
                tokens.append(token_text)
                labels.append(False)

    df = pd.DataFrame({'word': tokens[:elements], 'metaphor': labels[:elements]})
    return df

# ------------- 2) Czech loader stub (user-provided) -------------
# You said you already have a function `load_czech()` returning DataFrame with columns: word (str), metaphor (bool).
# Here we only assume it exists.
def load_czech(czech_path) -> pd.DataFrame:
    df = pd.read_csv(czech_path, header=None)
    df = df.T
    df.columns = ['word', 'metaphor']
    df['metaphor'] = df['metaphor'].astype(int).astype(bool)

    new_words = []
    new_labels = []

    for word, label in zip(df['word'], df['metaphor']):
        if len(word) <= 1:
            new_words.append(word)
            new_labels.append(label)
            continue

        if word[-1].isalpha():
            new_words.append(word)
            new_labels.append(label)
            continue

        new_words.append(word[:-1])
        new_labels.append(label)
        new_words.append(word[-1])
        new_labels.append(False)

    return pd.DataFrame({'word': new_words, 'metaphor': new_labels})

# ------------- 3) Prepare datasets (token classification, single-token samples) -------------
def df_to_hf_dataset(df: pd.DataFrame) -> Dataset:
    # Normalize types
    out = df.copy()
    out['word'] = out['word'].astype(str)
    out['label'] = out['metaphor'].astype(int)  # 0/1
    out = out[['word', 'label']]
    return Dataset.from_pandas(out, preserve_index=False)

def align_labels_single_word(encodings, labels):
    """
    Align word-level labels to token-level labels for a batch of sentences.
    
    encodings: Hugging Face BatchEncoding from tokenizer(batch, is_split_into_words=True)
    labels: list of lists, each inner list contains word-level labels for one sentence
    """
    aligned_labels = []

    for i in range(len(encodings["input_ids"])):  # iterate over batch
        word_ids = encodings.word_ids(batch_index=i)  # maps each token to its word
        label_ids = []
        previous_word_idx = None

        for word_idx in word_ids:
            if word_idx is None:
                # special tokens like [CLS] or [SEP]
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                # first token of a word → take word label
                label_ids.append(labels[i][word_idx])
            else:
                # subsequent subwords → ignore
                label_ids.append(-100)
            previous_word_idx = word_idx

        aligned_labels.append(label_ids)

    return aligned_labels





# ------------- 4) Weighted loss via custom Trainer -------------
import torch
from torch import nn

class WeightedTokenTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits

        loss_fct = nn.CrossEntropyLoss(
            weight=self.class_weights.to(logits.device) if self.class_weights is not None else None,
            ignore_index=-100
        )
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


# ------------- 5) Metric function -------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)

    # Keep only positions where labels != -100
    true_labels = []
    true_preds = []
    for p_row, l_row in zip(preds, labels):
        mask = l_row != -100
        if mask.any():
            true_labels.extend(l_row[mask])
            true_preds.extend(p_row[mask])

    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, true_preds, average="binary", zero_division=0)
    acc = accuracy_score(true_labels, true_preds)
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

# ------------- 6) Main training/eval routine -------------
def run_training(
    vua_xml_path: str,
    czech_path: str ,
    czech_train_path: str,
    vua_size: int = 2000,
    output_dir: str = "./mb2-metaphor",
    model_name: str = "bert-base-multilingual-cased",
    seed: int = 42,
    num_train_epochs: int = 3,
    per_device_train_batch_size: int = 32,
    per_device_eval_batch_size: int = 32,
    learning_rate: float = 3e-5,
    weight_decay: float = 0.01,
    warmup_ratio: float = 0.06,
):
    set_seed(seed)
    # 1) Load data
    train_df = load_komet_words(vua_xml_path, vua_size)
    train_cz_df = load_czech(czech_train_path)
    
    test_df = load_czech(czech_path)  # <- you provide this

    # Quick sanity filtering: drop empty strings
    train_df = train_df[train_df['word'].astype(str).str.strip() != ""].reset_index(drop=True)
    test_df = test_df[test_df['word'].astype(str).str.strip() != ""].reset_index(drop=True)
    train_cz_df = train_cz_df[train_cz_df['word'].astype(str).str.strip() != ""].reset_index(drop=True)

    # 2) HF datasets
    train_ds = df_to_hf_dataset(train_df)
    test_ds = df_to_hf_dataset(test_df)
    train_cz_df = df_to_hf_dataset(train_cz_df)


    def group_into_sentences(dataset):
        sentences = []
        labels = []

        current_sentence = []
        current_labels = []

        for word, label in zip(dataset["word"], dataset["label"]):
            current_sentence.append(word)
            current_labels.append(label)

            # Check if word ends with a dot
            if word[-1] == ".":
                sentences.append(current_sentence)
                labels.append(current_labels)
                current_sentence = []
                current_labels = []

        # Add any leftover words as last sentence
        if current_sentence:
            sentences.append(current_sentence)
            labels.append(current_labels)

        return {"word": sentences, "metaphor": labels}



    train_sentences = group_into_sentences(train_ds)
    test_sentences  = group_into_sentences(test_ds)
    train_cz_sentences = group_into_sentences(train_cz_df)

    train_sentences_final = {"word": train_sentences["word"] + train_cz_sentences["word"],
                             "metaphor": train_sentences["metaphor"] + train_cz_sentences["metaphor"]}

    train_ds = Dataset.from_dict(train_sentences_final)
    test_ds  = Dataset.from_dict(test_sentences)

    # 3) Tokenizer & tokenization
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_batch(batch):
        enc = tokenizer(
            batch["word"],
            truncation=True,
            padding=True,
            is_split_into_words=True
        )

        aligned_labels = align_labels_single_word(
            encodings=enc,
            labels=batch["metaphor"]
        )

        enc["label"] = aligned_labels
        return enc


    train_tokenized = train_ds.map(tokenize_batch, batched=True, remove_columns=train_ds.column_names)
    test_tokenized  = test_ds.map(tokenize_batch,  batched=True, remove_columns=test_ds.column_names)



    from torch.utils.data import DataLoader

    def inspect_dataset(dataset, tokenizer, batch_size=4, n_samples=2):
        print("🔍 Dataset columns:", dataset.column_names)
        print("🔍 Dataset length:", len(dataset))

        # --- Single sample inspection ---
        print("\n=== First sample ===")
        sample = dataset[0]
        print("Keys:", sample.keys())
        print("Input length:", len(sample["input_ids"]))
        print("Label length:", len(sample["label"]))

        tokens = tokenizer.convert_ids_to_tokens(sample["input_ids"])
        print("\nTokens with labels:")
        for tok, lab in zip(tokens[:50], sample["label"][:50]):  # first 50 tokens
            print(f"{tok:15} {lab}")
        if len(tokens) > 50:
            print("... truncated print ...")

        # --- Label stats ---
        import numpy as np
        labels = np.array(sample["label"])
        valid = (labels != -100).sum()
        ignored = (labels == -100).sum()
        print(f"\nLabel stats for first sample: valid={valid}, ignored={ignored}")

        # --- Inspect a batch ---
        print("\n=== First batch ===")
        dl = DataLoader(dataset, batch_size=batch_size, shuffle=False)
        batch = next(iter(dl))
        print("Batch keys:", batch.keys())
        print("input_ids shape:", len(batch["input_ids"]))
        print("labels shape:", len(batch["label"]))

        for i in range(min(n_samples, batch_size)):
            tokens = tokenizer.convert_ids_to_tokens(batch["input_ids"][i])
            labels = batch["label"][i].tolist()
            print(f"\nSample {i} in batch:")
            for tok, lab in zip(tokens[:30], labels[:30]):  # print first 30
                print(f"{tok:15} {lab}")
            if len(tokens) > 30:
                print("... truncated print ...")

    # Example usage:
    inspect_dataset(train_tokenized, tokenizer, batch_size=4, n_samples=2)
    inspect_dataset(test_tokenized, tokenizer, batch_size=4, n_samples=2)
    inspect_dataset(test_tokenized, tokenizer, batch_size=4, n_samples=2)



    # 4) Model
    id2label = {0: "NON-MET", 1: "MET"}
    label2id = {"NON-MET": 0, "MET": 1}
    config = AutoConfig.from_pretrained(
        model_name,
        num_labels=2,
        id2label=id2label,
        label2id=label2id,
    )
    model = AutoModelForTokenClassification.from_pretrained(model_name, config=config)

    # 5) Class weights (to handle imbalance)
    pos = int(train_df['metaphor'].sum())
    neg = int((~train_df['metaphor']).sum())
    # Avoid division by zero
    if pos == 0 or neg == 0:
        class_weights = torch.tensor([1.0, 1.0], dtype=torch.float)
    else:
        # inverse frequency (scaled)
        total = pos + neg
        w0 = total / (2.0 * neg)
        w1 = total / (2.0 * pos)
        class_weights = torch.tensor([w0, w1], dtype=torch.float)

    # 6) Training args
    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_ratio=warmup_ratio,
        logging_steps=50,              # how often to print progress
        logging_dir=f"{output_dir}/logs",
        report_to="none",              # disable wandb or other integrations
        save_total_limit=1,            # keep only the latest checkpoint
        # fp16=torch.cuda.is_available(), # mixed precision if GPU
        fp16 = False,
        seed=seed,
    )

    # 7) Trainer
    trainer = WeightedTokenTrainer(
        model=model,
        args=args,
        train_dataset=train_tokenized,
        eval_dataset=test_tokenized,  # evaluate on VUA
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        class_weights=class_weights,
    )

    # 8) Train & evaluate
    # trainer.train()
    eval_metrics = trainer.evaluate()
    print("Evaluation on VUAMC:", eval_metrics)

    # 9) Save final artifacts
    # trainer.save_model(output_dir)
    # tokenizer.save_pretrained(output_dir)
    return eval_metrics

# ------------------ Run ------------------
# Example:
metrics = run_training(vua_xml_path="Data\Komet_Slovenian\komet.tei\komet.xml",
                    #    vua_xml_path="Data/VUA/VUAMC.xml",
                       czech_path="Data\CZECH_Dalibor\pokus_data.csv",
                       czech_train_path="Data\CZECH_Dalibor\pokus_train_data.csv",
                       output_dir="./mb2-metaphor",
                       num_train_epochs=5,
                       per_device_train_batch_size=64)
print(metrics)
