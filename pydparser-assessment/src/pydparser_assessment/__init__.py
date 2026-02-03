import json
import sys


class ResumeParser:
    def extract_entities_from_text(self, text):
        # Placeholder logic: replace with actual entity extraction
        # Simulate extraction of designation and skills from text
        # For demo, just extract first word as designation and next 5 as skills
        words = text.strip().split()
        return {
            "designation": words[0] if words else None,
            "skills": words[1:6] if len(words) > 1 else [],
        }


def extract(text):
    """
    Extracts entities using pydparser-assessment logic.
    Returns a list: [designation, skill1, skill2, ...] (up to 5 skills)
    """
    try:
        parser = ResumeParser()
        data = parser.extract_entities_from_text(text)
        entities = []
        if data.get("designation"):
            entities.append(data["designation"])
        if data.get("skills"):
            entities.extend(data["skills"][:5])
        return entities
    except Exception as e:
        return [f"Error: {str(e)}"]


def main():
    input_text = sys.stdin.read()
    if input_text:
        results = extract(input_text)
        print(json.dumps(results))


if __name__ == "__main__":
    main()
