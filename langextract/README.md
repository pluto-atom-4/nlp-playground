# langextract

This sub-project provides language extraction utilities for identifying and processing language entities in text.

## Features
- Detects and extracts language mentions from text
- Designed for modular integration
- Isolated dependencies (see pyproject.toml)

## Usage
- Exposes an `extract(text)` function in `src/langextract/__init__.py`
- Runnable as a module:
  ```
  uv run --package langextract python -m langextract < input.txt
  ```
- Reads input from stdin, outputs JSON

## Development
- All code in `src/langextract/`
- Technical context: `.claude/skills.md`

## Testing
```
uv run --package langextract pytest
```

## Persona & Skills
- See `.claude/skills.md` for extraction logic and goals
