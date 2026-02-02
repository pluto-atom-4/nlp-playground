---
name: fix-nlp-issues
description: Specialized GitHub issue fixing for nlp-playground - utilizes uv workspaces, sub-project isolation, and multi-engine benchmark validation.
license: MIT
---

# Fix NLP Issues - Monorepo Workflow

Automates the resolution of GitHub issues within the nlp-playground monorepo. This skill is optimized for **uv** and ensures that any change to an extraction engine (spaCy, langextract, etc.) is validated against the global benchmark.

## Key Features

- **uv Workspace Aware**: Executes commands using `uv run --package` to prevent dependency cross-contamination.
- **Benchmark Validation**: Automatically runs `compare_extractors.py` after a fix to ensure no regression in extraction accuracy.
- **Pre-commit Integration**: Runs local hooks (Ruff, Sync-list) before pushing to ensure Seattle-standard code quality.
- **Sub-project Targeting**: Intelligently identifies which of the 5 extractors requires a fix based on issue content.
- **Automated Triage Logic**: If the issue contains a "Sample JD" block, uses it as the `JOB_DESCRIPTION` variable in `compare_extractors.py`.
- **Regression Testing**: Compares "Before" vs "After" Markdown tables. Only proceeds to PR if the "After" table shows improved entity extraction.
- **Labeling**: Once the PR is created, uses `gh issue edit` to add the label `status: fixed-by-ai`.

## Workflow Steps

1. **Sync**: `git checkout main && git pull origin main`.
2. **Identify**: Determine which sub-project (e.g., `spacy-project`) the issue concerns.
3. **Branch**: Create `fix/[sub-project]-[issue-description]`.
4. **Implement**: Apply minimal, succinct Python fixes.
5. **Validate**: Run `uv run python compare_extractors.py` to check for side effects.
6. **Lint**: Run `uv run pre-commit run --all-files`.
7. **PR**: Create a Pull Request using `gh pr create`.

## Sub-Project Commands

### Run tests for a specific engine:
```bash
uv run --package [package-name] pytest
```

### Run global benchmark:
```bash
uv run python compare_extractors.py
```

## Branch Naming Convention (Monorepo Style)

- **Format**: `fix/[sub-project-name]/[short-description]`
- **Example**: `fix/spacy-project/entity-mapping-fix`
- **Example**: `fix/langextract/api-timeout-handling`

## Pre-commit Handling (uv specific)

If pre-commit fails due to a new sub-project addition, the agent must verify that the `scripts/update_compare_list.py` has executed correctly to sync the workspace.

## Automated Triage Logic
- **Issue Parsing**: If the issue contains a "Sample JD" block, use it as the `JOB_DESCRIPTION` variable in `compare_extractors.py`.
- **Regression Testing**: Compare the "Before" vs "After" Markdown tables. Only proceed to PR if the "After" table shows improved entity extraction (e.g., more skills caught or higher confidence).
- **Labeling**: Once the PR is created, use `gh issue edit` to add the label `status: fixed-by-ai`.

## Success Criteria

- ✅ Fix verified by `compare_extractors.py` (Markdown table looks correct).
- ✅ Code formatted with **Ruff** via pre-commit.
- ✅ No dependency conflicts in the `uv.lock` file.
- ✅ PR link mentions the specific extractor engine updated.

## Troubleshooting

**Dependency Conflict in Workspace**
- Run `uv sync` to resolve. If persistent, check for version overlaps in the root `pyproject.toml`.

**Benchmark Failure**
- If the Markdown table shows a "❌ Failed" status after a fix, the agent must revert and analyze the sub-project's `src/` logic.
