import subprocess
import json


# Sample Seattle IT Job Description
import sys
JOB_DESCRIPTION = """
Senior Software Engineer - Seattle, WA. 
Required: 5+ years of experience with Python, AWS, and Kubernetes. 
Experience with spaCy or LangChain is a plus. Salary: $160k - $210k.
"""

# Use JD from CLI argument if provided, otherwise use default
test_jd = sys.argv[1] if len(sys.argv) > 1 else JOB_DESCRIPTION

# Define the sub-projects in your uv workspace
EXTRACTORS = [
    "pydparser", 
    "skills-extractor", 
    "escoe-extractor", 
    "spacy-project", 
    "langextract"
]

def run_extractor(package_name, text):
    # This mock command simulates calling the internal __init__.py logic
    # In a real setup, this returns a JSON string of entities
    cmd = [
        "uv", "run", "--package", package_name, 
        "python", "-c", 
        f"import json; print(json.dumps(['Python', 'AWS', 'SDE']))" # Mock output
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout.strip())
    except:
        return ["Error"]


def calculate_score(actual, expected):
    if not expected: return "N/A"
    actual_lower = [a.lower() for a in actual]
    matches = set(actual_lower).intersection(set(expected))
    score = (len(matches) / len(expected)) * 100 if expected else 0
    return f"{int(score)}%"

if __name__ == "__main__":
    # Accept expected entities as JSON string (sys.argv[2])
    expected = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []

    print("| Engine | Extracted | Match Score | Status |")
    print("| :--- | :--- | :--- | :--- |")
    
    for extractor in EXTRACTORS:
        actual = run_extractor(extractor, test_jd)
        score = calculate_score(actual, expected)
        status = "✅" if score == "100%" else ("⚠️" if score != "0%" and score != "N/A" else ("❌" if score == "0%" else "ℹ️"))
        entity_str = ", ".join([f"`{a}`" for a in actual])
        print(f"| **{extractor}** | {entity_str} | {score} | {status} |")
