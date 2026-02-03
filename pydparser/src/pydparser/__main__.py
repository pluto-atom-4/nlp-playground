
import sys
import json
from pydparser import extract

def main():
    text = sys.stdin.read()
    print(json.dumps(extract(text)))

if __name__ == "__main__":
    main()
