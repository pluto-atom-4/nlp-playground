
# scripts testing and usage

This section contains usage and development notes for scripts in the NLP Playground monorepo.

## Key Scripts
- `compare_extractors.py`: Runs all extractors on a job description and outputs a Markdown table for side-by-side comparison. Supports assertion-driven grading with Expected Entities.
- `agent_shim.py`: Fetches GitHub issue content, extracts job description and expected entities, runs the benchmark, and prints a graded table for automated triage.
- `update_compare_list.py`: Auto-updates the EXTRACTORS list in `compare_extractors.py` when new sub-projects are added.

## Usage
- Run scripts from the root with `uv run python scripts/<script>.py`
- See each script's help or source for details

## Development
- Scripts are designed for cross-project orchestration and automation
- Do not place sub-project-specific code here

## More Info
- See the root README.md for architecture and workflow details
