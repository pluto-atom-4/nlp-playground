import sys
import json
from skills_extractor_assessment import extract

if __name__ == "__main__":
    text = sys.stdin.read()
    print(json.dumps(extract(text)))
