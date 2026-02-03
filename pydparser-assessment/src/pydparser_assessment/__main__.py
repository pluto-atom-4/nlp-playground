import sys
import json
from pydparser_assessment import extract

if __name__ == "__main__":
    text = sys.stdin.read()
    print(json.dumps(extract(text)))
