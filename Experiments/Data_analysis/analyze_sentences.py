import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def analyze(df, lang):
    ### num sentences ###

    print(len(df))

    ### avg sentence len ###

    sentence_lenghts = [len(sent) for sent in df['sentences']]
    print(min(sentence_lenghts))
    print(max(sentence_lenghts))
    print(np.mean(sentence_lenghts))
    print(np.median(sentence_lenghts))

    ### counter of POS sequences ###

    pos_counter = Counter([tuple(l) for l in df['poss']])
    print(pos_counter.most_common(5))

    ### metaphor per sentence ###

    met_per_sent = [sum(mets) for mets in df['labels']]
    print(min(met_per_sent))
    print(max(met_per_sent))
    print(np.mean(met_per_sent))
    print(np.median(met_per_sent))

    ### flat df ###

    flat_df = pd.DataFrame({'words': [w for sent in df['sentences'] for w in sent],
                            'labels': [l for lab in df['labels'] for l in lab],
                            'poss': [p for pos in df['poss'] for p in pos]})

    ### which words are the most metaphorical ###

    positive_flat_df = flat_df.where(flat_df['labels'].astype(bool)).dropna()

    positive_words = positive_flat_df['words'].to_list()
    pos_words_counter = Counter(positive_words)
    print(pos_words_counter.most_common(10))

    ### which tags are the most metaphorical ###

    positive_poss = positive_flat_df['poss'].to_list()
    pos_pos_counter = Counter(positive_poss)
    print(pos_pos_counter.most_common(10))

    all_poss = flat_df['poss'].to_list()
    all_pos_counter = Counter(all_poss)
    print(all_pos_counter.most_common(10))


    ### print pos percentage graph ###

    all_keys = list(all_pos_counter.keys())
    subset_counts = {k: pos_pos_counter.get(k, 0) for k in all_keys}

    sorted_keys = sorted(all_keys, key=lambda k: subset_counts[k], reverse=True)

    all_counts = [all_pos_counter[k] for k in sorted_keys]
    subset_counts_list = [subset_counts[k] for k in sorted_keys]

    x = np.arange(len(sorted_keys))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, all_counts, width, label='All')
    ax.bar(x + width/2, subset_counts_list, width, label='Metaphor')

    ax.set_ylabel('Count')
    ax.set_title(f'Metaphor vs all counts of POS - {lang}')
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_keys)
    ax.legend()

    plt.tight_layout()

    plt.savefig(f'Experiments/Data_analysis/graphs/POS_{lang}.png')

    ### print percentages of POS ###

    for key in sorted_keys:
        print(key, all_pos_counter[key], subset_counts[key], round(subset_counts[key] / all_pos_counter[key], 3))





    md_string = f"""
## {lang}

`{sum(met_per_sent)/sum(sentence_lenghts)}%` of metaphors

{sum(sentence_lenghts)} words, {sum(met_per_sent)} metaphors

- {len(df)} sentences:
    - shortest sentence: {min(sentence_lenghts)}
    - longest sentence: {max(sentence_lenghts)}
    - mean length: {np.mean(sentence_lenghts)}
    - median length: {np.median(sentence_lenghts)}

- sentences with metaphor: {sum([0 if m == 0 else 1 for m in met_per_sent])}

- most common sentence structure:
    - {pos_counter.most_common(5)}

- {sum(met_per_sent)} metaphors in the dataset:
    - min metaphors in sentence: {min(met_per_sent)}
    - max metaphors in sentence: {max(met_per_sent)}
    - mean metaphors in sentence: {np.mean(met_per_sent)}
    - median metaphors in sentence: {np.median(met_per_sent)}

most common metaphorical words:
- {pos_words_counter.most_common(10)}

most common metaphorical POS:
- {pos_pos_counter.most_common(10)}

most common POS in dataset:
- {all_pos_counter.most_common(10)}

![POS {lang}](graphs/POS_{lang}.png)

"""
    
    print(md_string)







LANG = 'Spanish'

if LANG == 'Slovenian':
    with open('Data/Komet_Slovenian/komet_sentences.json', 'r', encoding='utf-8') as f:
        df = pd.read_json(f)
elif LANG == 'English':
    with open('Data/VUA/VUA_sentences.json', 'r', encoding='utf-8') as f:
        df = pd.read_json(f)
elif LANG == 'Spanish':
    with open('Data\cometa_dataset_v1\cometa_test_sentences.json', 'r', encoding='utf-8') as f:
        df1 = pd.read_json(f)
    with open('Data\cometa_dataset_v1\cometa_train_sentences.json', 'r', encoding='utf-8') as f:
        df2 = pd.read_json(f)
    
    df = pd.concat([df1, df2])

elif LANG == 'Czech':
    with open('Data/CZECH_Dalibor/czech_metaphors_sentences.json', 'r', encoding='utf-8') as f:
        df = pd.read_json(f)

analyze(df, LANG)



