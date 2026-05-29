import pandas as pd

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

df_bara = read_annotations('npfl070/hw/our-annotation/metafory_bara.txt')
df_karel = read_annotations('npfl070/hw/our-annotation/metafory_karel.txt')
df_honza = read_annotations('npfl070/hw/our-annotation/metafory_honza.txt')

gold_df = pd.DataFrame({'words': df_bara['words'].to_list(), 
                        'l1': df_bara['labels'].to_list(), 
                        'l2': df_honza['labels'].to_list(),
                        'l3': df_karel['labels'].to_list()})

gold_df['labels'] = gold_df[['l1', 'l2', 'l3']].mode(axis=1)[0]


test_df = gold_df[['words', 'labels']][:275]
train_df = gold_df[['words', 'labels']][275:]

print_stats(test_df)
print_stats(train_df)

test_df.to_csv('metafory_test.csv', index=False)
train_df.to_csv('metafory_train.csv', index=False)

gold_df[['words', 'labels']].to_csv('metafory_gold_all.csv', index=False)