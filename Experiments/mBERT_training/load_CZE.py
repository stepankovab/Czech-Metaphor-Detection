import pandas as pd

def load_czech(czech_path) -> pd.DataFrame:
    df = pd.read_csv(czech_path, header=None)
    df = df.T
    df.columns = ['word', 'metaphor']
    df['metaphor'] = df['metaphor'].astype(int).astype(bool)

    new_words = []
    new_labels = []

    for word, label in zip(df['word'], df['metaphor']):
        if len(word) <= 1:
            new_words.append(word)
            new_labels.append(label)
            continue

        if word[-1].isalpha():
            new_words.append(word)
            new_labels.append(label)
            continue

        new_words.append(word[:-1])
        new_labels.append(label)
        new_words.append(word[-1])
        new_labels.append(False)

    return pd.DataFrame({'word': new_words, 'metaphor': new_labels})

train = list(load_czech('Data\CZECH_Dalibor\pokus_train_data.csv')['word'])
test = list(load_czech('Data\CZECH_Dalibor\pokus_data.csv')['word'])





print(' '.join(train))

print()
print()
print()
print()

print(' '.join(test))

