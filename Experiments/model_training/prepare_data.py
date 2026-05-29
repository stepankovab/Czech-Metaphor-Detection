import pandas as pd
from datasets import Dataset

def load_dataset(language, count, purpose, source_dir):
    if language == "en":
        with open(source_dir + f"/Data/VUA/VUA_{purpose}_sentences.json", 'r', encoding='utf-8') as f:
            data_df = pd.read_json(f)[:count]
    elif language == "sl":
        with open(source_dir + f"/Data/Komet_Slovenian/komet_{purpose}_sentences.json", 'r', encoding='utf-8') as f:
            data_df = pd.read_json(f)[:count]
    elif language == "cs":
        with open(source_dir + f"/Data/CZECH_Dalibor/czech_metaphors_{purpose}_sentences.json", 'r', encoding='utf-8') as f:
            data_df = pd.read_json(f)[:count]
    elif language == "es":
        with open(source_dir + f"/Data/cometa_dataset_v1/cometa_{purpose}_sentences.json", 'r', encoding='utf-8') as f:
            data_df = pd.read_json(f)[:count]

    print(purpose, language, "requested:", count, "provided:", data_df.shape[0], sum([sum(l) for l in data_df['labels']])/sum([len(l) for l in data_df['labels']]))
    return data_df


def prepare_data(train_languages, train_counts, test_language, test_count, train_only_pos, test_only_pos, source_dir, tokenizer):
    def align_labels_single_word(encodings, labels):
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
    

    def filter_labels_by_pos(df, pos_to_keep):
        new_labels = []

        for sent_label, sent_pos in zip(df['labels'], df['poss']):
            new_sent_labels = []
            for label, pos in zip(sent_label, sent_pos):
                if pos in pos_to_keep:
                    new_sent_labels.append(label)
                else:
                    new_sent_labels.append(0)
            new_labels.append(new_sent_labels)

        df['labels'] = new_labels
        return df


    train_sentences = []
    train_labels = []
    for language, count in zip(train_languages, train_counts):
        temp_train_df = load_dataset(language=language,
                               count=int(count),
                               purpose="train",
                               source_dir=source_dir)
        
        if len(train_only_pos) > 0:
            temp_train_df = filter_labels_by_pos(df=temp_train_df, pos_to_keep=train_only_pos)
            print("Keeping only metaphors in", train_only_pos, language, "requested:", count, "provided:", temp_train_df.shape[0], sum([sum(l) for l in temp_train_df['labels']])/sum([len(l) for l in temp_train_df['labels']]))

        # HERE i append all training data after each other in order of the languages
        train_sentences.extend(temp_train_df["sentences"])
        train_labels.extend(temp_train_df["labels"])

    print("Total train percentage of metaphor", sum([sum(l) for l in train_labels])/sum([len(l) for l in train_labels]))
    
    train_ds = Dataset.from_dict({"sentences": train_sentences,
                                  "labels": train_labels})
    
    temp_test_df = load_dataset(test_language, test_count, "test", source_dir=source_dir)

    if len(test_only_pos) > 0:
        temp_test_df = filter_labels_by_pos(df=temp_test_df, pos_to_keep=test_only_pos)
        print("Keeping only metaphors in", test_only_pos, test_language, test_count, sum([sum(l) for l in temp_test_df['labels']])/sum([len(l) for l in temp_test_df['labels']]))

    test_ds = Dataset.from_pandas(temp_test_df)

    def tokenize_batch(batch):
        enc = tokenizer(
            batch["sentences"],
            truncation=True,
            is_split_into_words=True,
        )

        aligned_labels = align_labels_single_word(encodings=enc, labels=batch["labels"])

        enc["labels"] = aligned_labels
        return enc


    train_tokenized = train_ds.map(tokenize_batch, batched=True, remove_columns=train_ds.column_names)
    test_tokenized  = test_ds.map(tokenize_batch,  batched=True, remove_columns=test_ds.column_names)

    return train_tokenized, test_tokenized, temp_test_df

