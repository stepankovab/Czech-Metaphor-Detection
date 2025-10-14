import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

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


def compute_POS_percentages(test_data, logits, labels):
    sentences = test_data["sentences"]
    pos_sentences = test_data["pos"]
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


    # print percentage of different categhories

    # print examples of correct and incorrect

    df = pd.DataFrame({"pos": pos, "preds": true_preds, "labels": true_labels})

    # Count true and predicted metaphors per POS
    counts = (
        df.groupby("pos")[["preds", "labels"]]
        .sum()  # count how many are 1 per pos
        .astype(int)
        .reset_index()
    )

    # Optional: also count total per POS if you want percentages later
    counts["total"] = df.groupby("pos").size().values

    # Plot side-by-side bars
    x = range(len(counts))
    bar_width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - bar_width/2 for i in x], counts["labels"], width=bar_width, label="True Metaphors", color="orange")
    plt.bar([i + bar_width/2 for i in x], counts["preds"], width=bar_width, label="Predicted Metaphors", color="blue")

    plt.xticks(x, counts["pos"], rotation=45)
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.show()


    print(3)




