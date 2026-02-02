import sys
import json
from spacy_project import extract

if __name__ == "__main__":
    text = sys.stdin.read()
    print(json.dumps(extract(text)))
