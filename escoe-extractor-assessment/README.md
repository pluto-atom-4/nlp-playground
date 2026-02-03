# escoe-extractor-assessment

This sub-project provides ESCoE/ESCO taxonomy extraction, mapping job text to the ESCO framework using a vector-based approach.

## Features
- Extracts ESCO skills and occupations from job descriptions
- Vector-based matching for robust taxonomy mapping
- Isolated dependencies (see pyproject.toml)

## Usage
- Exposes an `extract(text)` function in `src/escoe_extractor_assessment/__init__.py`
- Runnable as a module:
  ```
  uv run --package escoe-extractor-assessment python -m escoe_extractor_assessment < input.txt
  ```
- Reads input from stdin, outputs JSON

## Development
- All code in `src/escoe_extractor_assessment/`
- Technical context: `.claude/skills.md`

## Testing
```
uv run --package escoe-extractor-assessment pytest
```

## Persona & Skills
- See `.claude/skills.md` for extraction logic and goals
