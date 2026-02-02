# pydparser

This sub-project provides custom parsing logic for NLP experimentation.

## Features
- Implements custom parsing strategies for job descriptions and related text
- Designed for extensibility and experimentation
- Isolated dependencies (see pyproject.toml)

## Usage
- Exposes an `extract(text)` function in `src/pydparser/__init__.py`
- Runnable as a module:
  ```
  uv run --package pydparser python -m pydparser < input.txt
  ```
- Reads input from stdin, outputs JSON

## Development
- All code in `src/pydparser/`
- Technical context: `.claude/skills.md`

## Testing
```
uv run --package pydparser pytest
```

## Persona & Skills
- See `.claude/skills.md` for extraction logic and goals
