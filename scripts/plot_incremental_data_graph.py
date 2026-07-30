import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

def plot_f1_curves(md_table, fig_name, figsize=(6, 5)):
    # Parse markdown table
    lines = md_table.strip().splitlines()

    # Remove separator line (|----|----|)
    lines = [lines[0]] + lines[2:]

    # Remove leading/trailing pipes
    lines = ["|".join(part.strip() for part in line.strip().strip("|").split("|"))
             for line in lines]

    csv_data = "\n".join(lines)

    df = pd.read_csv(StringIO(csv_data), sep="|")

    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # Convert numeric columns
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    # Convert F1 values to percentages
    metrics = ["F1", "ADJ F1", "NOUN F1", "VERB F1"]

    plt.figure(figsize=figsize)

    for metric in metrics:
        plt.plot(df["N"], df[metric] * 100,
                 marker="o", linewidth=2, markersize=4,
                 label=metric)

    
    plt.xlabel("Training examples (N)", fontsize=12)
    plt.ylabel("F1 (%)", fontsize=12)
    plt.legend(fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    plt.ylim(0, 100)
    plt.xlim(df["N"].min(), df["N"].max())

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.show()

    plt.xticks(rotation=45)
    plt.savefig(f"{fig_name}.pdf", bbox_inches="tight")



md_table = """|     N |   Precision |   Recall |    F1 |   ADJ F1 |   NOUN F1 |   VERB F1 |
|-------|-------------|----------|-------|----------|-----------|-----------|
|    10 |       0.123 |    0.634 | 0.206 |     0.29 |      0.24 |      0.38 |
|    50 |       0.197 |    0.114 | 0.145 |     0.18 |      0.15 |      0.17 |
|   100 |       0.263 |    0.374 | 0.309 |     0.3  |      0.25 |      0.36 |
|   200 |       0.44  |    0.338 | 0.382 |     0.13 |      0.21 |      0.41 |
|   300 |       0.548 |    0.432 | 0.483 |     0.19 |      0.31 |      0.48 |
|   400 |       0.564 |    0.567 | 0.566 |     0.28 |      0.4  |      0.54 |
|   500 |       0.582 |    0.613 | 0.597 |     0.36 |      0.44 |      0.58 |
|   750 |       0.631 |    0.647 | 0.639 |     0.42 |      0.49 |      0.61 |
|  1000 |       0.662 |    0.625 | 0.643 |     0.45 |      0.5  |      0.62 |
|  1500 |       0.659 |    0.709 | 0.683 |     0.52 |      0.57 |      0.66 |
|  2000 |       0.679 |    0.715 | 0.696 |     0.51 |      0.59 |      0.68 |
|  2500 |       0.672 |    0.749 | 0.708 |     0.56 |      0.61 |      0.68 |
|  3000 |       0.687 |    0.736 | 0.711 |     0.57 |      0.63 |      0.68 |
|  4000 |       0.742 |    0.719 | 0.73  |     0.58 |      0.65 |      0.71 |
|  5000 |       0.756 |    0.728 | 0.742 |     0.59 |      0.66 |      0.72 |
|  6000 |       0.772 |    0.747 | 0.759 |     0.62 |      0.7  |      0.73 |
|  7000 |       0.77  |    0.768 | 0.769 |     0.63 |      0.71 |      0.75 |
|  8000 |       0.787 |    0.772 | 0.779 |     0.66 |      0.72 |      0.76 |
|  9000 |       0.799 |    0.765 | 0.781 |     0.66 |      0.72 |      0.76 |
| 10000 |       0.803 |    0.756 | 0.779 |     0.63 |      0.73 |      0.75 |
| 11000 |       0.813 |    0.762 | 0.787 |     0.65 |      0.73 |      0.76 |
| 12000 |       0.81  |    0.765 | 0.787 |     0.66 |      0.72 |      0.76 |
| 12962 |       0.823 |    0.758 | 0.789 |     0.65 |      0.73 |      0.76 |"""

plot_f1_curves(md_table, "Czech-Metaphor-Detection/results_graphs/incremental_en_en")