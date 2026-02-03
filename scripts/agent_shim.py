import subprocess
import json
import sys
import re

def get_issue_content(issue_no):
    """Fetch issue body using GitHub CLI."""
    cmd = ["gh", "issue", "view", str(issue_no), "--json", "body"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)["body"]

def run_benchmark_on_issue(issue_no):
    print(f"🚀 Processing Issue #{issue_no}...")
    
    body = get_issue_content(issue_no)
    target_jd = extract_jd_from_body(body)
    
    print(f"📝 Testing with JD: {target_jd[:50]}...")

    # Execute the comparison script with the specific JD as an argument
    # (Update compare_extractors.py to accept sys.argv[1] as input)
    cmd = ["uv", "run", "python", "compare_extractors.py", target_jd]
    subprocess.run(cmd)

    def parse_issue_metadata(body):
        """
        Extracts the JD and Expected Entities using Regex.
        Expects format: 
        Expected Entities: Python, AWS, Docker
        """
        # Extract JD (Text inside triple backticks)
        jd_match = re.search(r"```(?:text)?(.*?)```", body, re.DOTALL)
        jd = jd_match.group(1).strip() if jd_match else body.strip()

        # Extract Expected Entities (Comma-separated list after header)
        exp_match = re.search(r"Expected Entities:\s*(.*)", body, re.IGNORECASE)
        expected = []
        if exp_match:
            expected = [e.strip().lower() for e in exp_match.group(1).split(",")]
    
        return jd, expected

    def run_graded_benchmark(issue_no):
        body = get_issue_content(issue_no)
        jd, expected = parse_issue_metadata(body)
    
        print(f"### 🤖 Graded Triage for Issue #{issue_no}")
        if expected:
            print(f"**Targeting Entities:** {', '.join([f'`{e}`' for e in expected])}\n")

        # Call comparison script and pass expected entities as a JSON string
        cmd = [
            "uv", "run", "python", "compare_extractors.py", 
            jd, 
            json.dumps(expected)
        ]
        subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    run_graded_benchmark(sys.argv[1])
