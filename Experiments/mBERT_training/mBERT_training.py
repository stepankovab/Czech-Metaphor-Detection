import argparse
import torch

from transformers import (
    AutoTokenizer,
    AutoConfig,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    set_seed,
)
from datasets import Dataset

from evaluation_scripts import evaluate_metrics, compute_POS_percentages
from load_VUE import load_vuamc
from load_SLO import load_komet
from load_CZE import load_czech
from load_SPA_cometa import load_cometa_words


parser = argparse.ArgumentParser()
parser.add_argument("--train_languages", nargs="+", default=["es"], help="Languages to train on")
parser.add_argument("--train_counts", nargs="+", default=[1000], help="Number of words for each train language")
parser.add_argument("--test_language", default="es", type=str, help="Test language.")
parser.add_argument("--test_count", default=1000, type=int, help="Number of test words.")
parser.add_argument("--output_dir", default="./Czech-Metaphor-Detection", type=str, help="Output directory path.")
parser.add_argument("--source_dir", default="./Czech-Metaphor-Detection", type=str, help="Source directory path.")

parser.add_argument("--model_name", default="bert-base-multilingual-cased", type=str, help="Model name in Huggingface Transformers.")
parser.add_argument("--seed", default=42, type=int, help="Seed.")
parser.add_argument("--imbalance_weight", default=0.95, type=float, help="Imbalance weight.")

parser.add_argument("--epochs", default=3, type=int, help="Training epochs.")
parser.add_argument("--train_batch_size", default=32, type=int, help="Train batch size.")
parser.add_argument("--test_batch_size", default=32, type=int, help="Test batch size.")
parser.add_argument("--learning_rate", default=3e-5, type=float, help="Learning rate.")
parser.add_argument("--weight_decay", default=0.01, type=float, help="Weight decay.")
parser.add_argument("--warmup_ratio", default=0.06, type=float, help="Warmup ratio.")


class WeightedTokenTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**{k: v for k, v in inputs.items() if k != "labels"})
        logits = outputs.logits

        loss_fct = torch.nn.CrossEntropyLoss(
            weight=self.class_weights.to(logits.device) if self.class_weights is not None else None,
            ignore_index=-100
        )
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


def prepare_data(train_languages, train_counts, test_language, test_count, source_dir, tokenizer):

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
    
    
    def group_into_sentences(dataset):
        sentences = []
        labels = []
        poss = []

        current_sentence = []
        current_labels = []
        current_pos = []

        if "pos" not in dataset.keys():
            dataset["pos"] = [None for _ in range(len(dataset))]

        for word, label, pos in zip(dataset["words"], dataset["labels"], dataset["pos"]):
            current_sentence.append(word)
            current_labels.append(label)
            current_pos.append(pos)

            # Check if word ends with a dot
            if word[-1] == ".":
                sentences.append(current_sentence)
                labels.append(current_labels)
                poss.append(current_pos)
                current_sentence = []
                current_labels = []
                current_pos = []

        # Add any leftover words as last sentence
        if current_sentence:
            sentences.append(current_sentence)
            labels.append(current_labels)
            poss.append(current_pos)

        return {"sentences": sentences, "labels": labels, "pos": poss}
    

    def load_dataset(language, count, purpose):
        if purpose == "train" and language == "en":
            data_df = load_vuamc(source_dir + "/Data/VUA/VUAMC.xml", None, count)   
        elif purpose == "train" and language == "sl":
            data_df = load_komet(source_dir + "/Data/Komet_Slovenian/komet.tei/komet.xml", None, count)
        elif purpose == "train" and language == "cs":
            data_df = load_czech(source_dir + "/Data/CZECH_Dalibor/group_3_merged.csv")
        elif purpose == "train" and language == "es":
            data_df = load_cometa_words(source_dir + "/Data/cometa_dataset_v1/cometa_pos_train.tsv", None, count)

        elif purpose == "test" and language == "en":
            data_df = load_vuamc(source_dir + "/Data/VUA/VUAMC.xml", -count, None)
        elif purpose == "test" and language == "sl":
            data_df = load_komet(source_dir + "/Data/Komet_Slovenian/komet.tei/komet.xml", -count, None)
        elif purpose == "test" and language == "cs":
            data_df = load_czech(source_dir + "/Data/CZECH_Dalibor/pokus_data.csv")
        elif purpose == "test" and language == "es":
            data_df = load_cometa_words(source_dir + "/Data/cometa_dataset_v1/cometa_pos_test.tsv", None, count)

        print(purpose, language, count, data_df['labels'].sum()/len(data_df))

        data_df = data_df[data_df['words'].astype(str).str.strip() != ""].reset_index(drop=True)
        data_df['words'] = data_df['words'].astype(str)
        data_df['labels'] = data_df['labels'].astype(int)

        return group_into_sentences(data_df)


    train_sentences = []
    train_labels = []
    for language, count in zip(train_languages, train_counts):
        temp_df = load_dataset(language=language,
                               count=int(count),
                               purpose="train")

        train_sentences.extend(temp_df["sentences"])
        train_labels.extend(temp_df["labels"])

    print("Total train percentage of metaphor", sum([sum(l) for l in train_labels])/sum([len(l) for l in train_labels]))
    
    train_ds = Dataset.from_dict({"sentences": train_sentences,
                                  "labels": train_labels})
    
    test_ds = Dataset.from_dict(load_dataset(test_language, test_count, "test"))

    def tokenize_batch(batch):
        enc = tokenizer(
            batch["sentences"],
            truncation=True,
            is_split_into_words=True,
            padding = "longest"
            # padding="max_length",
            # max_length=256
        )

        aligned_labels = align_labels_single_word(encodings=enc, labels=batch["labels"])

        enc["labels"] = aligned_labels
        return enc


    train_tokenized = train_ds.map(tokenize_batch, batched=True, remove_columns=train_ds.column_names)
    test_tokenized  = test_ds.map(tokenize_batch,  batched=True, remove_columns=test_ds.column_names)

    return train_tokenized, test_tokenized, load_dataset(test_language, test_count, "test")


def main(args):

    print(args)

    set_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    train_tokenized, test_tokenized, test_raw = prepare_data(args.train_languages, 
                                                    args.train_counts,
                                                    args.test_language,
                                                    args.test_count,
                                                    args.source_dir,
                                                    tokenizer)

    print(train_tokenized, test_tokenized)

    config = AutoConfig.from_pretrained(
        args.model_name,
        num_labels=2,
        id2label={0: "NON-MET", 1: "MET"},
        label2id={"NON-MET": 0, "MET": 1},
    )
    model = AutoModelForTokenClassification.from_pretrained(args.model_name, config=config)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.test_batch_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        logging_steps=50,              
        logging_dir=f"{args.output_dir}/logs",
        report_to="none",              
        save_total_limit=1,            
        fp16=torch.cuda.is_available(),
        seed=args.seed,
        save_strategy="no",
    )

    trainer = WeightedTokenTrainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=test_tokenized,
        tokenizer=tokenizer,
        compute_metrics=evaluate_metrics,
        class_weights=torch.tensor([1 / (2 * args.imbalance_weight), 1 / (2 * (1 - args.imbalance_weight))], dtype=torch.float),
    )

    trainer.train()
    preds, labels, metrics = trainer.predict(test_tokenized)
    print(metrics)

    pos_percentages = compute_POS_percentages(test_raw, preds, labels)
    print(pos_percentages)
    


if __name__ == "__main__":
    main_args = parser.parse_args([] if "__file__" not in globals() else None)
    main(main_args)

