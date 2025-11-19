import pandas as pd

PARTITION = 'test'

df_met = pd.read_csv(f'Data\cometa_dataset_v1\preprocessing\cometa_{PARTITION}.tsv', sep='\t', header=None, names=['words', 'labels'])

with open(f"Data\cometa_dataset_v1\preprocessing\{PARTITION}_processed.conllu", "r", encoding="utf-8") as f:
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



sentence = []
pos_sentence = []
labels = []

all_sentences = []
all_poss = []
all_labels = []

m = 0
for p in range(len(df_pos)):
    if df_met['words'][m] == "<sep>":
        m += 1
        all_sentences.append(sentence.copy())
        all_poss.append(pos_sentence.copy())
        all_labels.append(labels.copy())

        sentence = []
        pos_sentence = []
        labels = []

    sentence.append(df_met['words'][m])
    pos_sentence.append(df_pos['pos'][p])

    if df_met['labels'][m] == 'O':
        labels.append(int(0))
    else:
        labels.append(int(1))
        if 'B-METAPHOR' != df_met['labels'][m]:
            print(df_met['labels'][m])

    m += 1

df_pos_sent = pd.DataFrame({"sentences": all_sentences,
                            "labels": all_labels,
                            "poss": all_poss})

print(df_met)
print(df_pos_sent)

with open(f"Data/cometa_dataset_v1/cometa_{PARTITION}_sentences.json", 'w', encoding='utf-8') as f:
    df_pos_sent.to_json(f)



# assert len(df_met) == len(df_pos)

# df_met['pos'] = df_pos['pos']


# with open(f'cometa_pos_{PARTITION}.tsv', 'w', encoding='utf-8') as f:
#     df_met.to_csv(f, sep='\t', header=None, index=False, lineterminator='\n')