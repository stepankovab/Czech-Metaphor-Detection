import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import fleiss_kappa

def read_annotations(file_name):
    
    with open(file_name, 'r', encoding='utf-8') as f:
        contents = f.read()

    words = contents.split()
    labels = []

    for w in words:
        if w == '<met>':
            labels[-1] = 1
            labels.append(-1)

        else:
            labels.append(0)

    df = pd.DataFrame({'words': words, 'labels': labels})
    df_filtered = df[df['labels'] != -1]

    return df_filtered

def print_stats(df):
    print(df)
    print('all:', len(df))
    print('positive:', len(df[df['labels'] == 1]))


def pairwise_cohens_kappa(list_of_labels):
    for i in range(len(list_of_labels)):
        for j in range(i + 1, len(list_of_labels)):
            print("pairwise cohens kappa:", cohen_kappa_score(list_of_labels[i], list_of_labels[j]))

def compute_fleiss_kappa(list_of_labels):
    annotations = np.array(list_of_labels)
    annotations = annotations.T

    n_items = annotations.shape[0]
    count_matrix = np.zeros((n_items, 2), dtype=int)
    count_matrix[:, 0] = (annotations == 0).sum(axis=1)
    count_matrix[:, 1] = (annotations == 1).sum(axis=1)

    print("fleiss kappa:", fleiss_kappa(count_matrix))
    

df_raw = read_annotations('npfl070/hw/our-annotation/metafory_raw.txt')
df_bara = read_annotations('npfl070/hw/our-annotation/metafory_bara.txt')
df_karel = read_annotations('npfl070/hw/our-annotation/metafory_karel.txt')
df_honza = read_annotations('npfl070/hw/our-annotation/metafory_honza.txt')

print_stats(df_bara)
print_stats(df_karel)
print_stats(df_honza)

assert len(df_bara) == len(df_karel) and len(df_honza) == len(df_karel)

list_of_labels = [df_bara["labels"], df_karel["labels"], df_honza["labels"]]

pairwise_cohens_kappa(list_of_labels)
compute_fleiss_kappa(list_of_labels)

