import pandas as pd
import os

all_dfs = []

for file in os.listdir("Data/CZECH_Dalibor/final"):
    df = pd.read_csv("Data/CZECH_Dalibor/final/" + file, sep=',', header=0)

    all_dfs.append(df)
        
        
df_all = pd.concat(all_dfs)

print(df_all)

print(len(df_all))

df_all['label'] = df_all[['ann1', 'ann2', 'ann3']].mode(axis=1)[0].astype(int)

df_all = df_all[['word', 'label']]

print(df_all)

df_all.to_csv("Data/CZECH_Dalibor/czech_metaphors.csv", index=False)
