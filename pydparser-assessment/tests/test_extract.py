import pytest
from pathlib import Path
from pydparser_assessment import extract
import nltk


@pytest.fixture(scope="session", autouse=True)
def download_spacy_model():
    """Download required spaCy model before running tests."""
    import subprocess
    import sys

    try:
        import spacy

        spacy.load("en_core_web_sm")
    except OSError:
        # Model not found, download it
        subprocess.check_call(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
        )


@pytest.fixture(scope="session", autouse=True)
def download_nltk_data():
    """Download required NLTK data before running tests."""
    nltk.download("stopwords", quiet=True)


@pytest.fixture(scope="module")
def sample_resume_path():
    # Get absolute path to the sample resume file
    test_dir = Path(__file__).parent
    root_dir = test_dir.parent.parent
    path = root_dir / "tests" / "data" / "sample_resume.txt"
    return str(path)


def test_extract_returns_data(sample_resume_path):
    print(f"Testing extract function with sample resume file: {sample_resume_path}")
    result = extract(sample_resume_path)
    print(f"\n=== Extract Result ===\nType: {type(result)}\nValue: {result}")
    assert result is not None
