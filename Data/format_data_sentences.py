import pandas as pd
import re
import regex


def load_annotated_csv(file_name, context_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    
    df['contexts'] = len(df) * [context_name]

    words = []
    labels = []
    contexts = []

    for index, row in df.iterrows():
        parts = re.findall(r"\w+|[^\w\s]", row['words'])
        if len(parts) > 1:
            words.extend(parts)
            labels.extend([row['labels']] * len(parts))
            contexts.extend([row['contexts']] * len(parts))

        else:
            words.append(row['words'])
            labels.append(row['labels'])
            contexts.append(row['contexts'])

    return pd.DataFrame({'words': words, 'labels': labels, 'contexts': contexts})


def load_raw_text_annotate_zeroes(file_name, context_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    df = pd.DataFrame({'words': raw_text.split()})
    df['labels'] = len(df) * [0]
    df['contexts'] = len(df) * [context_name]

    words = []
    labels = []
    contexts = []

    for index, row in df.iterrows():
        parts = re.findall(r"\w+|[^\w\s]", row['words'])
        if len(parts) > 1:
            words.extend(parts)
            labels.extend([row['labels']] * len(parts))
            contexts.extend([row['contexts']] * len(parts))

        else:
            words.append(row['words'])
            labels.append(row['labels'])
            contexts.append(row['contexts'])

    return pd.DataFrame({'words': words, 'labels': labels, 'contexts': contexts})
    

def export_words_for_udpipe(file_name, df):
    # print to csv for obtaining POS
    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(' '.join(df['words'].to_list()))


def add_pos_to_df(conllu_file_name, df):
    with open(conllu_file_name, "r", encoding="utf-8") as f:
        conllu_text = f.read()

    lines = [line for line in conllu_text.split("\n") if line.strip() and not line.startswith("#")]
    data_raw = [line.split("\t") for line in lines if len(line.split("\t")) >= 4]

    data = []

    for d in data_raw:
        if d[1][-1] == '“' and len(d[1]) > 1:
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
            labels.append(df['labels'][i])

        contexts.append(df['contexts'][i])

        if df['words'][i] != d[1]:
            print(df['words'][i], d[1], i)

        i += 1

    all_sentences.append(sentence.copy())
    all_poss.append(pos_sentence.copy())
    all_labels.append(labels.copy())
    all_contexts.append(contexts.copy())


    df_pos = pd.DataFrame({"sentences": all_sentences,
                        "labels": all_labels,
                        "poss": all_poss,
                        "contexts": all_contexts})

    print(df)
    print(df_pos)

    return df_pos


def create_zero_labeled_df_from_conllu(conllu_file_name, context_name):
    with open(conllu_file_name, "r", encoding="utf-8") as f:
        conllu_text = f.read()

    lines = [line for line in conllu_text.split("\n") if line.strip() and not line.startswith("#")]
    data_raw = [line.split("\t") for line in lines if len(line.split("\t")) >= 4]

    data = []

    for d in data_raw:
        if d[1][-1] == '“' and len(d[1]) > 1:
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

        labels.append(int(0))
        contexts.append(context_name)

        i += 1

    all_sentences.append(sentence.copy())
    all_poss.append(pos_sentence.copy())
    all_labels.append(labels.copy())
    all_contexts.append(contexts.copy())


    df_pos = pd.DataFrame({"sentences": all_sentences,
                        "labels": all_labels,
                        "poss": all_poss,
                        "contexts": all_contexts})

    print(df_pos)

    return df_pos



if __name__ == "__main__":
    working_dir = "/storage/brno2/home/stepanb2/Czech-Metaphor-Detection/Data/CZECH_ENGLISH_translation/"
    
    # # read raw text file, split punctuation, return with all labels 0
    # df_annotated = load_raw_text_annotate_zeroes(working_dir + "plaintext_sentences_en.txt", "cs_to_en")

    # # read csv with gold annotations, split punctuation
    # df_annotated = load_annotated_csv(working_dir + "metafory_gold_all.csv", "poetry")

    # prepare file for udpipe
    # export_words_for_udpipe(working_dir + "words_only.txt", df_annotated)
    
    # # merge conllu with annotated text
    # df_all = add_pos_to_df(working_dir + "cs_to_en.conllu", df_annotated)

    # add 0 labels to conllu text
    df_all = create_zero_labeled_df_from_conllu(working_dir + "cs_to_en.conllu", "cs_to_en")
    
    # save as sentences
    with open(working_dir + "cs_to_en_sentences.json", 'w', encoding='utf-8') as f:
        df_all.to_json(f)
    


