import os
import pandas as pd
import re


for file in os.listdir("Data/CZECH_Dalibor/final"):
    seen = 0

    df = pd.read_csv("Data/CZECH_Dalibor/final/" + file)
    words = df['word'].to_list()

    new_words = []
    for w in words:
        if re.search(r'\.\d+$', w):
            print(w)
            w = re.sub(r'\.\d+$', '', w)
            seen += 1
            print(w)

        new_words.append(w)

    if seen != 0:
        df['word'] = new_words

        df.to_csv("Data/CZECH_Dalibor/final/new_" + file, index=False)

