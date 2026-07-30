import pandas as pd
import random

path = 'Data/VUA/'

with open(path + 'VUA_sentences.json', 'r', encoding='utf-8') as f:
    df = pd.read_json(f)

count = len(df)
test_samples = round(0.20 * count)

test_ids = random.sample(range(count), k=test_samples)

df_test = df.iloc[test_ids]
df_train = df.drop(test_ids)

print(len(df_test))
print(len(df_train))

df_test.to_json(path + 'VUA_test_sentences.json')
df_train.to_json(path + 'VUA_train_sentences.json')


