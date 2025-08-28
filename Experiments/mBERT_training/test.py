import xml.etree.ElementTree as ET
import pandas as pd

# def load_vuamc_words(vuamc_xml_path: str, elements=-1) -> pd.DataFrame:
#     """
#     Parse VU Amsterdam Metaphor Corpus (TEI P5) and return a DataFrame with:
#     columns: ['word', 'metaphor'] where 'metaphor' is bool.
#     Includes punctuation and preserves the original token order.
#     """
#     ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
#     tree = ET.parse(vuamc_xml_path)
#     root = tree.getroot()

#     tokens = []
#     labels = []

#     # Iterate over all sentences
#     for s in root.findall('.//tei:s', ns):
#         for child in s:
#             if child.tag == f"{{{ns['tei']}}}w":  # word element
#                 token_text = (child.text or '').strip()
#                 is_met = False
#                 seg = child.find('tei:seg', ns)
#                 if seg is not None and (seg.get('type') == 'met' or seg.get('function') == 'mrw'):
#                     inner_text = (seg.text or '').strip()
#                     if inner_text:
#                         token_text = inner_text
#                     is_met = True
#                 if token_text:
#                     tokens.append(token_text)
#                     labels.append(is_met)
#             elif child.tag == f"{{{ns['tei']}}}c":  # punctuation element
#                 token_text = (child.text or '').strip()
#                 if token_text:
#                     tokens.append(token_text)
#                     labels.append(False)

#     df = pd.DataFrame({'word': tokens[:elements], 'metaphor': labels[:elements]})
#     return df




# df = load_vuamc_words("Data/VUA/VUAMC.xml", 2324567890)



# print(len(df[:1000]))

# print(df[10000:11000])




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


print(load_czech("Data/CZECH_Dalibor/pokus_train_data.csv"))



