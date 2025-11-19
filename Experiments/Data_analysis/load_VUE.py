import xml.etree.ElementTree as ET
import pandas as pd

# Define approximate CLAWS → UPOS mapping
claws_to_upos = {
    'NN0': 'NOUN', 'NN1': 'NOUN', 'NN2': 'NOUN',
    'NP0': 'PROPN',
    'AJ0': 'ADJ', 'AJC': 'ADJ', 'AJS': 'ADJ',
    'AV0': 'ADV', 'AVP': 'ADV', 'AVQ': 'ADV',
    'VVN': 'VERB', 'VVG': 'VERB', 'VVD': 'VERB', 'VVZ': 'VERB',
    'VVB': 'VERB', 'VVI': 'VERB',
    'VHB': 'AUX', 'VHD': 'AUX', 'VHZ': 'AUX', 'VHG': 'AUX',
    'VBB': 'AUX', 'VBD': 'AUX', 'VBG': 'AUX', 'VBZ': 'AUX',
    'VDB': 'AUX', 'VDD': 'AUX', 'VDG': 'AUX', 'VDI': 'AUX', 'VDZ': 'AUX',
    'DT0': 'DET', 'AT0': 'DET', 'DPS': 'DET', 'DTQ': 'DET',
    'PRP': 'ADP', 'PRF': 'PRON',
    'PNP': 'PRON', 'PNX': 'PRON', 'PNI': 'PRON', 'PNQ': 'PRON',
    'CRD': 'NUM', 'ORD': 'NUM',
    'CJC': 'CCONJ', 'CJS': 'SCONJ', 'CJT': 'SCONJ',
    'ITJ': 'INTJ',
    'POS': 'PART',
    'PUN': 'PUNCT', 'PUL': 'PUNCT', 'PUQ': 'PUNCT', 'PUR': 'PUNCT',
    'TO0': 'PART',
    'EX0': 'PRON',
    'UNC': 'X', 'ZZ0': 'X', 'XX0': 'X'
}

def get_upos(tag):
    base = tag.split('-')[0]  # handle combos like 'NN1-NP0'
    return claws_to_upos.get(base, 'X')

def load_vuamc(vuamc_xml_path: str, start, end) -> pd.DataFrame:
    """
    Parse VU Amsterdam Metaphor Corpus (TEI P5) and return a DataFrame with:
    columns: ['word', 'metaphor'] where 'metaphor' is bool.
    Includes punctuation and preserves the original token order.
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    tree = ET.parse(vuamc_xml_path)
    root = tree.getroot()



    sentence = []
    pos_sentence = []
    labels = []

    all_sentences = []
    all_poss = []
    all_labels = []

    # Iterate over all sentences
    for s in root.findall('.//tei:s', ns):
        for child in s:
            if child.tag == f"{{{ns['tei']}}}w":  # word element
                token_text = (child.text or '').strip()
                is_met = False
                seg = child.find('tei:seg', ns)
                tag = get_upos(child.get("type", ""))

                if seg is not None and (seg.get('type') == 'met' or seg.get('function') == 'mrw'):
                    inner_text = (seg.text or '').strip()
                    if inner_text:
                        token_text = inner_text
                    is_met = True

                if token_text:
                    sentence.append(token_text)
                    labels.append(int(is_met))
                    pos_sentence.append(tag)

                    

            elif child.tag == f"{{{ns['tei']}}}c":  # punctuation element
                token_text = (child.text or '').strip()
                tag = get_upos(child.get("type", ""))

                if token_text:
                    sentence.append(token_text)
                    labels.append(int(0))
                    pos_sentence.append(tag)


        all_sentences.append(sentence.copy())
        all_poss.append(pos_sentence.copy())
        all_labels.append(labels.copy())

        sentence = []
        pos_sentence = []
        labels = []

    # df = pd.DataFrame({'words': sentence[start:end], 'labels': labels[start:end], 'pos': pos_sentence[start:end]})
    # return df

    df_sent = pd.DataFrame({"sentences": all_sentences,
                            "labels": all_labels,
                            "poss": all_poss})

    print(df_sent)

    with open(f"Data/VUA/VUA_sentences.json", 'w', encoding='utf-8') as f:
        df_sent.to_json(f)

VUE_FILE_PATH = './Data/VUA/VUAMC.xml'
df = load_vuamc(VUE_FILE_PATH, None, None)