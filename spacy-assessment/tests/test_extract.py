
from spacy_assessment import extract


def test_extract_happy_path():
    text = "Barack Obama was born in Hawaii. He was elected president in 2008."
    result = extract(text)
    print(result)
    # We expect at least 'Barack Obama' and 'Hawaii' to be recognized as entities
    assert any("Barack Obama" in ent for ent in result)
    assert any("Hawaii" in ent for ent in result)

def test_extract_no_entities():
    text = "This is a simple sentence with no named entities."
    result = extract(text)
    assert result == []  # Expecting an empty list when no entities are present
