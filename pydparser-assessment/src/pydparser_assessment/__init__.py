import json
import sys
from pydparser import ResumeParser


def extract(file_path: str) -> list[str]:
    """
    Extract entities using pydparser-assessment logic from a file.
    Returns a list: [designation, skill1, skill2, ...] (up to 5 skills)
    """
    try:
        parser = ResumeParser(file_path)
        data = parser.get_extracted_data()
        print(data)  # For debugging purposes
        designation = data.get("designation")
        skills = data.get("skills", [])
        entities = [designation] if designation else []
        entities.extend(skills[:5])
        return entities
    except Exception as e:
        return [f"Error: {e}"]


def main():
    input_text = sys.stdin.read()
    if input_text:
        results = extract(input_text)
        print(json.dumps(results))


if __name__ == "__main__":
    main()
