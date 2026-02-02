import sys
import json
from pydparser import extract

if __name__ == "__main__":
    text = sys.stdin.read()
    print(json.dumps(extract(text)))
