from lxml import etree
import pandas as pd

def load_komet(vuamc_xml_path: str, start, end) -> pd.DataFrame:
    """
    Parse KOMET TEI XML with XInclude and return a DataFrame:
    columns: ['word', 'metaphor'] where 'metaphor' is bool.
    Includes punctuation and preserves the original token order.
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(vuamc_xml_path, parser)
    tree.xinclude()  # resolve <xi:include>
    root = tree.getroot()

    tokens = []
    labels = []

    # Iterate over all sentences
    for s in root.xpath('.//tei:s', namespaces=ns):
        for child in s:
            tag = etree.QName(child.tag).localname
            token_text = (child.text or '').strip() if child.text else ''
            if tag == 'w' and token_text:
                # check if the word is inside a metaphor segment
                is_metaphor = bool(child.xpath('ancestor::tei:seg[@type="metaphor"]', namespaces=ns))
                tokens.append(token_text)
                labels.append(is_metaphor)
            elif tag in ('c', 'pc') and token_text:
                # punctuation or whitespace
                tokens.append(token_text)
                labels.append(False)

    df = pd.DataFrame({'words': tokens[start:end], 'labels': labels[start:end]})
    return df


# df = load_komet_words("Data\Komet_Slovenian\komet.tei\komet.xml")

