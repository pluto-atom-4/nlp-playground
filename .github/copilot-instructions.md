
# Copilot Instructions for nlp-playground Monorepo


This workspace uses a Modular Persona Architecture for NLP experimentation, with strict isolation between five sub-projects to minimize dependency conflicts:

- **pydparser/**: Custom parsing logic
- **skills-extractor/**: Skill extraction tools
- **spacy-project/**: spaCy-based NLP workflows
- **langextract/**: Language extraction utilities
- **escoe-extractor/**: ESCoE/ESCO taxonomy extraction

## Modular Persona Architecture
- **Global context** is defined in `.claude/` at the root:
   - `persona.md`: Describes the overall AI persona (e.g., Senior NLP Architect, Seattle focus)
   - `rules.md`: Workspace-wide rules (e.g., always use `uv`, Python 3.12+, strict sub-project isolation)
- **Technical skills** are defined in each sub-project's `.claude/skills.md`:
   - Each file documents the extraction logic, constraints, and goals for that sub-project (see sub-project `.claude/skills.md` for details)
   - **escoe-extractor**: ESCoE/ESCO taxonomy extraction, mapping job text to ESCO framework using vector-based approach

## Key Structure
- Each sub-project has its own `pyproject.toml` and `src/` directory
- Dependencies are managed per sub-project using `uv`
- The root is only for coordination, shared scripts, and global persona/rules

## Developer Workflow
1. **Initialize root and sub-projects**
   - `uv init --lib`
   - `uv init --lib pydparser`
   - `uv init --lib skills-extractor`
   - `uv init --lib spacy-project`
   - `uv init --lib langextract`
   - `uv init --lib escoe-extractor`
2. **Add dependencies per sub-project**
   - `uv add --package pydparser pydparser`
   - `uv add --package skills-extractor skills-extractor-library`
   - `uv add --package spacy-project spacy`
   - `uv run --package spacy-project python -m spacy download en_core_web_sm`
   - `uv add --package langextract langextract`
   - `uv add --package escoe-extractor skills-extractor-library spacy`
3. **Sync environment**
   - `uv sync`

## Conventions
- All code for each sub-project goes in its respective `src/` folder
- Avoid cross-imports between sub-projects unless explicitly coordinated
- Use `uv` for all dependency and environment management
- Each sub-project should have its own README.md for documentation
- Use the `.claude/` and `.claude/skills.md` files for context switching and technical skill reference



## Example: Adding a Dependency
To add `requests` to `skills-extractor`:
```
uv add --package skills-extractor requests
```
To add `pandas` to `escoe-extractor`:
```
uv add --package escoe-extractor pandas
```

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
- The project uses GitHub Actions for CI and code review automation:
   - `.github/workflows/ci.yaml` runs on push/PR to `main` and performs:
      - Dependency sync with `uv`
      - Linting and formatting with Ruff
      - Workspace-wide comparison test (`compare_extractors.py`)
      - Posts a sticky pull request comment with the latest extraction benchmark results as a Markdown table for side-by-side comparison
   - `.github/workflows/review.yaml` runs on PR open/sync and performs:
      - Persona/skills file presence check for all sub-projects
      - Type checking with Pyright

See these workflow files for details and update them as project requirements evolve.

## Cross-Extractor Comparison
To compare extraction results across all sub-projects, use the provided script:
```
uv run python compare_extractors.py
```
This will run a sample IT job description through all five extractors and print the results side-by-side.

## Entry Point Convention
- Each sub-project exposes an `extract(text)` function in its main package (see `src/<project>/__init__.py`).
- Each sub-project is runnable as a module (e.g., `python -m spacy_project`) and reads input from stdin, outputting JSON.


## Persona & Skills Context
- AI agents should use `.claude/persona.md` for global persona context and `.claude/rules.md` for workspace rules.
- Each sub-project's `.claude/skills.md` provides technical extraction logic, constraints, and goals for that module.
- The `.claude/skills/fix-nlp-issues/SKILL.md` defines the agent workflow for automated GitHub issue fixing, uv workspace validation, and multi-engine benchmarking.

## Issue-Driven Agentic Triage
- Use `scripts/agent_shim.py` to fetch GitHub issue content and run the benchmark on user-provided job descriptions.
- The agent skill supports auto-triage: if an issue contains a "Sample JD" block, it is used for targeted extraction benchmarking.
- If the issue contains an `Expected Entities:` section, the shim and comparison script will automatically grade each extractor's output and display a match score and status in the Markdown table.
- Recommended: Set up a GitHub Action to trigger the agent workflow when a `fix-it` label is added to an issue, posting the Markdown table as a comment for proof of fix.
- This enables assertion-driven triage and automated regression validation for every issue.

## Testing & Build
- Run tests per sub-project using `uv run --package <sub-project> pytest` (if pytest is used)
- Build and run commands should be executed from the root using `uv run --package <sub-project> <command>`

## Integration Points
- spaCy models are managed in `spacy-project` only
- ESCoE/ESCO taxonomy extraction is managed in `escoe-extractor` only
- Shared data or scripts should be placed in the root or a dedicated shared folder, not inside sub-projects
- Use `.claude/skills.md` in each sub-project for technical context

## References
- See each sub-project's `pyproject.toml` for dependencies
- See each sub-project's `src/` for implementation
- See `.claude/` and sub-project `.claude/skills.md` for persona and skill context
- See `.github/copilot-instructions.md` for agent guidance

---
For questions about workflow, persona, or skills, refer to `.claude/`, sub-project `.claude/skills.md`, or the root README.md.
