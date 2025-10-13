import pandas as pd

PARTITION = 'train'

df_met = df = pd.read_csv(f'Data\cometa_dataset_v1\cometa_{PARTITION}.tsv', sep='\t', header=None, names=['words', 'labels'])

with open(f"{PARTITION}_processed.conllu", "r", encoding="utf-8") as f:
    conllu_text = f.read()

lines = [line for line in conllu_text.split("\n") if line.strip() and not line.startswith("#")]
data = [line.split("\t") for line in lines if len(line.split("\t")) >= 4]

words = []
pos = []

skip_next = 0
for d in data:
    if skip_next > 0:
        skip_next = skip_next - 1
        continue

    if '-' in d[0]:
        skip_next = int(d[0].split('-')[-1])
        words.append(d[1])
        pos.append(d[3])

    elif d[0] == '1':
        words.append(d[1])
        pos.append(d[3])

df_pos = pd.DataFrame({"words": words, "pos": pos})

print(df_met)
print(df_pos)

assert len(df_met) == len(df_pos)

df_met['pos'] = df_pos['pos']


with open(f'cometa_pos_{PARTITION}.tsv', 'w', encoding='utf-8') as f:
    df_met.to_csv(f, sep='\t', header=None, index=False, lineterminator='\n')