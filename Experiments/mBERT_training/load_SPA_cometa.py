import pandas as pd


def load_cometa_words(cometa_tsv_path: str, start=0, end=None) -> pd.DataFrame:
    """
    Parse CoMeta dataset and return a DataFrame:
    columns: ['words', 'metaphor', 'upos'] where
      - 'word' is the token text
      - 'labels' is bool 
      - 'pos' is the POS tag
    Includes punctuation and preserves the original token order.
    """
    headers = ["words", "labels", "pos"]
    df = pd.read_csv(cometa_tsv_path, sep='\t', header=None, names=headers)
    df["labels"] = df["labels"].apply(lambda l: False if l == 'O' else True)

    return pd.DataFrame({
        'words': df["words"][start:end],
        'labels': df["labels"][start:end],
        'pos': df["pos"][start:end]
    })


# FILE_PATH = 'Data\cometa_dataset_v1\cometa_pos_train.tsv'

# df = load_cometa_words(FILE_PATH, None, None)

# print(df)
# print(df["labels"].sum())

# for w, l in zip(df["words"][:120], df["labels"][:120]):
#     print(w, l)
