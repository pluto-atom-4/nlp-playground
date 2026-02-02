# skills-extractor

This sub-project provides skill extraction tools for identifying skills in job descriptions and related text.

## Features
- Extracts skills using rule-based and/or ML approaches
- Designed for modular skill extraction
- Isolated dependencies (see pyproject.toml)

## Usage
- Exposes an `extract(text)` function in `src/skills_extractor/__init__.py`
- Runnable as a module:
  ```
  uv run --package skills-extractor python -m skills_extractor < input.txt
  ```
- Reads input from stdin, outputs JSON

## Development
- All code in `src/skills_extractor/`
- Technical context: `.claude/skills.md`

## Testing
```
uv run --package skills-extractor pytest
```

## Persona & Skills
- See `.claude/skills.md` for extraction logic and goals
