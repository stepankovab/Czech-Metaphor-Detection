import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from collections import Counter



def evaluate_metrics(eval_pred):
    """
    returns: metrics dict, predictions, labels
    """
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


def dump_results_to_json(test_data, logits, labels, out_folder, uuid):
    sentences = test_data["sentences"]
    pos_sentences = test_data["poss"]
    preds = np.argmax(logits, axis=-1)

    words = [word for sentence in sentences for word in sentence]  
    pos = [p for sentence in pos_sentences for p in sentence]

    # Keep only positions where labels != -100
    true_labels = []
    true_preds = []
    for p_row, l_row in zip(preds, labels):
        mask = l_row != -100
        if mask.any():
            true_labels.extend(l_row[mask])
            true_preds.extend(p_row[mask])

    df = pd.DataFrame({"words": words, "poss": pos, "preds": true_preds, "labels": true_labels})
    print('results dupm at:', uuid)
    df.to_json(out_folder + "/" + uuid + '.json')


def compute_POS_percentages(test_data, logits, labels):
    sentences = test_data["sentences"]
    pos_sentences = test_data["poss"]
    preds = np.argmax(logits, axis=-1)

    words = [word for sentence in sentences for word in sentence]  
    pos = [p for sentence in pos_sentences for p in sentence]

    # Keep only positions where labels != -100
    true_labels = []
    true_preds = []
    for p_row, l_row in zip(preds, labels):
        mask = l_row != -100
        if mask.any():
            true_labels.extend(l_row[mask])
            true_preds.extend(p_row[mask])

    df = pd.DataFrame({"words": words, "pos": pos, "preds": true_preds, "labels": true_labels})


    # print percentage of different categhories

    # print examples of correct and incorrect

    # Count true and predicted metaphors per POS
    counts = (
        df.groupby("pos")[["preds", "labels"]]
        .sum()  # count how many are 1 per pos
        .astype(int)
        .reset_index()
    )

    # Optional: also count total per POS if you want percentages later
    counts["total"] = df.groupby("pos").size().values

    return counts



def analyze(df, lang):

    ### metaphor per sentence ###

    met_per_sent = [sum(mets) for mets in df['labels']]
    print(min(met_per_sent))
    print(max(met_per_sent))
    print(np.mean(met_per_sent))
    print(np.median(met_per_sent))

    ### flat df ###

    flat_df = pd.DataFrame({'words': [w for sent in df['sentences'] for w in sent],
                            'labels': [l for lab in df['labels'] for l in lab],
                            'poss': [p for pos in df['poss'] for p in pos]})

    ### which words are the most metaphorical ###

    positive_flat_df = flat_df.where(flat_df['labels'].astype(bool)).dropna()

    positive_words = positive_flat_df['words'].to_list()
    pos_words_counter = Counter(positive_words)
    print(pos_words_counter.most_common(10))

    ### which tags are the most metaphorical ###

    positive_poss = positive_flat_df['poss'].to_list()
    pos_pos_counter = Counter(positive_poss)
    print(pos_pos_counter.most_common(10))

    all_poss = flat_df['poss'].to_list()
    all_pos_counter = Counter(all_poss)
    print(all_pos_counter.most_common(10))


    ### print pos percentage graph ###

    all_keys = list(all_pos_counter.keys())
    subset_counts = {k: pos_pos_counter.get(k, 0) for k in all_keys}

    sorted_keys = sorted(all_keys, key=lambda k: subset_counts[k], reverse=True)

    all_counts = [all_pos_counter[k] for k in sorted_keys]
    subset_counts_list = [subset_counts[k] for k in sorted_keys]

    x = np.arange(len(sorted_keys))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, all_counts, width, label='All')
    ax.bar(x + width/2, subset_counts_list, width, label='Metaphor')

    ax.set_ylabel('Count')
    ax.set_title(f'Metaphor vs all counts of POS - {lang}')
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_keys)
    ax.legend()

    plt.tight_layout()

    plt.savefig(f'Experiments/Data_analysis/graphs/POS_{lang}.png')

    ### print percentages of POS ###

    for key in sorted_keys:
        print(key, all_pos_counter[key], subset_counts[key], round(subset_counts[key] / all_pos_counter[key], 3))







