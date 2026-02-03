# NLP Playground Monorepo

This repository uses a Modular Persona Architecture for NLP experimentation, with five isolated sub-projects and strict context separation:  

- **pydparser-assessment/**: Custom parsing logic using pydparser
- **skills-extractor-assessment/**: Skill extraction tools
- **spacy-assessment/**: spaCy-based NLP workflows
- **langextract-assessment/**: Language extraction utilities
- **escoe-extractor-assessment/**: ESCoE/ESCO taxonomy extraction

## Modular Persona Architecture
- **Global context** is defined in `.claude/` at the root:
   - `persona.md`: Describes the overall AI persona (e.g., Senior NLP Architect, Seattle focus)
   - `rules.md`: Workspace-wide rules (e.g., always use `uv`, Python 3.12+, strict sub-project isolation)
- **Technical skills** are defined in each sub-project's `.claude/skills.md`:
   - Each file documents the extraction logic, constraints, and goals for that sub-project
   - **escoe-extractor**: ESCoE/ESCO taxonomy extraction, mapping job text to ESCO framework using vector-based approach

## Structure
Each sub-project has its own `pyproject.toml` and `src/` directory to avoid dependency conflicts. Use `uv` for all environment and dependency management. Technical context for each sub-project is in its `.claude/skills.md`.

## Quickstart
1. Initialize root and sub-projects:
   ```
   uv init --lib
   uv init --lib pydparser-assessment
   uv init --lib skills-extractor-assessment
   uv init --lib spacy-assessment
   uv init --lib langextract-assessment
   uv init --lib escoe-extractor-assessment
   ```
2. Add dependencies per sub-project:
   ```
   uv add --package pydparser-assessment pydparser
   uv add --package skills-extractor-assessment skills-extractor-library
   uv add --package spacy-assessment spacy
   uv run --package spacy-assessment python -m spacy download en_core_web_sm
   uv add --package langextract-assessment langextract
   uv add --package escoe-extractor-assessment skills-extractor-library spacy
   ```
3. Sync environment:
   ```
   uv sync
   ```

## Development
- All code for each sub-project goes in its respective `src/` folder
- Avoid cross-imports between sub-projects unless explicitly coordinated
- Each sub-project should have its own README.md for documentation
- Use `.claude/` and `.claude/skills.md` for persona, rules, and technical skill context

## Testing
Run tests per sub-project using:
```
uv run --package <sub-project> pytest
```

## Cross-Extractor Comparison
To compare extraction results across all sub-projects, run:
```
uv run python compare_extractors.py
```
This script runs a sample IT job description through all five extractors and prints the results side-by-side.

## Entry Point Convention
- Each sub-project exposes an `extract(text)` function in its main package (see `src/<project>/__init__.py`).
- Each sub-project is runnable as a module (e.g., `python -m spacy_project`) and reads input from stdin, outputting JSON.


## Persona & Skills Context
- See `.claude/persona.md` for global persona context
- See `.claude/rules.md` for workspace rules
- Each sub-project's `.claude/skills.md` provides technical extraction logic, constraints, and goals
- The `.claude/skills/fix-nlp-issues/SKILL.md` defines the agent workflow for automated GitHub issue fixing, uv workspace validation, and multi-engine benchmarking.

## Issue-Driven Agentic Triage
- Use `scripts/agent_shim.py` to fetch GitHub issue content and run the benchmark on user-provided job descriptions.
- The agent skill supports auto-triage: if an issue contains a "Sample JD" block, it is used for targeted extraction benchmarking.
- If the issue contains an `Expected Entities:` section, the shim and comparison script will automatically grade each extractor's output and display a match score and status in the Markdown table.
- Recommended: Set up a GitHub Action to trigger the agent workflow when a `fix-it` label is added to an issue, posting the Markdown table as a comment for proof of fix.
- This enables assertion-driven triage and automated regression validation for every issue.

## Pre-Commit Automation
- A single root `.pre-commit-config.yaml` manages all sub-projects:
   - Standard hooks: trailing whitespace, end-of-file, YAML, large files
   - Formatting: Ruff and Ruff-format
   - Persona file check: Ensures each sub-project has `.claude/skills.md`
-   - Targeted hooks: e.g., spaCy model validation only runs for `spacy-project` changes
   - Auto-sync: Whenever a new sub-project is added (pyproject.toml changes), the `compare_extractors.py` script is automatically updated to include it in benchmarks
- All hooks use `uv run` for correct environment isolation
- Run all hooks locally with:
   ```
   uv run pre-commit run --all-files
   ```

Zero-Touch Maintenance: Adding a new extractor (e.g., `uv init gliner-extractor`) will auto-update the benchmark script on commit.

## CI & Review Workflows
- Automated CI and review are managed via GitHub Actions:
   - `.github/workflows/ci.yaml` runs on push/PR to `main` and performs:
      - Dependency sync with `uv`
      - Linting and formatting with Ruff
      - Workspace-wide comparison test (`compare_extractors.py`)
      - Posts a sticky pull request comment with the latest extraction benchmark results as a Markdown table for side-by-side comparison
   - `.github/workflows/review.yaml` runs on PR open/sync and performs:
      - Persona/skills file presence check for all sub-projects
      - Type checking with Pyright

See these workflow files for details and update them as project requirements evolve.

## More Info
- See `.claude/` for persona and workspace rules
- See each sub-project's `.claude/skills.md` for technical context
- See `.github/copilot-instructions.md` for agent guidance
- See sub-project READMEs for details