import spacy


def extract(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [ent.text for ent in doc.ents]
