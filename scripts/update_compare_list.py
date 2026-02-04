import os
import re


def update_extractors():
    # Find all directories with a pyproject.toml (excluding the root)
    subprojects = [
        d
        for d in os.listdir(".")
        if os.path.isdir(d)
        and os.path.exists(os.path.join(d, "pyproject.toml"))
        and d not in [".venv", ".git", "scripts"]
    ]
    subprojects.sort()

    runner_path = "compare_extractors.py"
    if not os.path.exists(runner_path):
        return

    with open(runner_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find and replace the EXTRACTORS list
    pattern = r"EXTRACTORS = \[.*?\]"
    updated_content = re.sub(
        pattern, f"EXTRACTORS = {subprojects}", content, flags=re.DOTALL
    )

    with open(runner_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"Updated {runner_path} with: {subprojects}")


if __name__ == "__main__":
    update_extractors()
