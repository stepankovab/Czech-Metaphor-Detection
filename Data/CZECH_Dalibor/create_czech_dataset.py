import pandas as pd
import os
import re
import regex

all_dfs = []

for file in os.listdir("Data/CZECH_Dalibor/final"):
    df = pd.read_csv("Data/CZECH_Dalibor/final/" + file, sep=',', header=0)
    name = '_'.join(file.split('_')[:-1])
    df["context"] = name

    all_dfs.append(df)
        
        
df_all = pd.concat(all_dfs)

print(df_all)

print(len(df_all))

df_all['label'] = df_all[['ann1', 'ann2', 'ann3']].mode(axis=1)[0].astype(int)

df_all = df_all[['word', 'label', 'context']]

print(df_all)

words = []
labels = []
contexts = []

for index, row in df_all.iterrows():
    parts = re.findall(r"\w+|[^\w\s]", row['word'])
    if len(parts) > 1:
        words.extend(parts)
        labels.extend([row['label']] * len(parts))
        contexts.extend([row['context']] * len(parts))

    else:
        words.append(row['word'])
        labels.append(row['label'])
        contexts.append(row['context'])

df_final = pd.DataFrame({'words': words, 'labels': labels, 'contexts': contexts})


## print to csv for obtaining POS
# with open("Data/CZECH_Dalibor/czech_metaphors_words_only.txt", 'w', encoding='utf-8') as f:
#     f.writelines(' '.join(df_all['word'].to_list()))
## add POS


with open("Data/CZECH_Dalibor/czech_processed.conllu", "r", encoding="utf-8") as f:
    conllu_text = f.read()

lines = [line for line in conllu_text.split("\n") if line.strip() and not line.startswith("#")]
data_raw = [line.split("\t") for line in lines if len(line.split("\t")) >= 4]

data = []

for d in data_raw:
    if d[1][-1] == '“':
        first = d.copy()
        first[1] = d[1][:-1]
        second = d.copy()
        second[1] = d[1][-1]
        second[3] = 'PUNCT'
        data.extend([first, second])
    
    else:
        data.append(d)

sentence = []
pos_sentence = []
labels = []
contexts = []

all_sentences = []
all_poss = []
all_labels = []
all_contexts = []

skip_next = 0

i = 0
for d in data:
    if skip_next > 0:
        skip_next = skip_next - 1
        continue

    if '-' in d[0]:
        skip_next = int(d[0].split('-')[-1]) - int(d[0].split('-')[0]) + 1

    if d[0] == '1' and sentence != []:
        if set(pos_sentence) == set(['PUNCT']):
            all_sentences[-1].extend(sentence.copy())
            all_poss[-1].extend(pos_sentence.copy())
            all_labels[-1].extend(labels.copy())
            all_contexts[-1].extend(contexts.copy())
        else:
            all_sentences.append(sentence.copy())
            all_poss.append(pos_sentence.copy())
            all_labels.append(labels.copy())
            all_contexts.append(contexts.copy())

        sentence = []
        pos_sentence = []
        labels = []
        contexts = []

    sentence.append(d[1])

    if regex.match(r'^(?!.*[\p{L}\p{N}]).*$', d[1]):
        pos_sentence.append('PUNCT')
    else:
        pos_sentence.append(d[3])

    if d[3] == 'PUNCT':
        labels.append(int(0))
    else:
        labels.append(df_final['labels'][i])

    contexts.append(df_final['contexts'][i])

    if df_final['words'][i] != d[1]:
        print(df_final['words'][i], d[1], i)

    i += 1

all_sentences.append(sentence.copy())
all_poss.append(pos_sentence.copy())
all_labels.append(labels.copy())
all_contexts.append(contexts.copy())


# df_pos = pd.DataFrame({"words": sentence, "pos": pos_sentence})
df_pos = pd.DataFrame({"sentences": all_sentences,
                       "labels": all_labels,
                       "poss": all_poss,
                       "contexts": all_contexts})

print(df_final)
print(df_pos)

# assert len(df_final) == len(df_pos)

# df_final['pos'] = df_pos['pos']



with open("Data/CZECH_Dalibor/czech_metaphors_sentences.json", 'w', encoding='utf-8') as f:
    df_pos.to_json(f)

