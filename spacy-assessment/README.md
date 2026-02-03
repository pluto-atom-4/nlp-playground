# spacy-assessment

This sub-project provides spaCy-based NLP workflows for skill and entity extraction.

## Features
- Uses spaCy pipelines for NLP tasks
- Supports custom models and entity recognition
- Isolated dependencies (see pyproject.toml)

## Usage
- Exposes an `extract(text)` function in `src/spacy_assessment/__init__.py`
- Runnable as a module:
  ```
  uv run --package spacy-assessment python -m spacy_assessment < input.txt
  ```
- Reads input from stdin, outputs JSON

## Development
- All code in `src/spacy_assessment/`
- Technical context: `.claude/skills.md`

## Testing
```
uv run --package spacy-assessment pytest
```

## Persona & Skills
- See `.claude/skills.md` for extraction logic and goals
