import pandas as pd
from lxml import etree

def load_komet(vuamc_xml_path: str, start=0, end=None) -> pd.DataFrame:
    """
    Parse KOMET TEI XML with XInclude and return a DataFrame:
    columns: ['word', 'metaphor', 'upos'] where
      - 'word' is the token text
      - 'metaphor' is bool (True if inside <seg type="metaphor">)
      - 'upos' is the UPOS tag from @msd (if present, else None)
    Includes punctuation and preserves the original token order.
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(vuamc_xml_path, parser)
    tree.xinclude()
    root = tree.getroot()

    tokens, labels, pos_tags = [], [], []

    for s in root.xpath('.//tei:s', namespaces=ns):
        for child in s.iter():  # visit nested tokens too
            tag = etree.QName(child.tag).localname
            token_text = (child.text or '').strip() if child.text else ''
            
            if tag in ('w', 'pc') and token_text:
                # metaphor label
                is_metaphor = bool(child.xpath('ancestor::tei:seg[@type="metaphor"]', namespaces=ns))
                
                # extract UPOS from @msd (pattern: "UposTag=VERB|...")
                msd = child.get("msd", "")
                pos = "UNK"
                for part in msd.split("|"):
                    if part.startswith("UposTag="):
                        pos = part.split("=", 1)[1]
                        break
                
                tokens.append(token_text)
                labels.append(is_metaphor)
                pos_tags.append(pos)

    return pd.DataFrame({
        'words': tokens[start:end],
        'labels': labels[start:end],
        'pos': pos_tags[start:end]
    })


# XML_FILE_PATH = './Czech-Metaphor-Detection/Data/Komet_Slovenian/komet.tei/komet.xml'

# df = load_komet(XML_FILE_PATH, None, None)

# print(df)
# print(df["labels"].sum())

# for w, l in zip(df["words"][:20], df["labels"][:20]):
#     print(w, l)