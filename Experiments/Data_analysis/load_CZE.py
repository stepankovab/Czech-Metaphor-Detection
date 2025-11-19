import pandas as pd

def load_czech(czech_path):
    df = pd.read_csv(czech_path)
    df['labels'] = df['labels'].astype(bool)
    return(df[['words', 'labels', 'pos']])



