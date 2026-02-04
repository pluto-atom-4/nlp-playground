
# scripts

This folder contains shared scripts for orchestration, benchmarking, and automation across the NLP Playground monorepo.

## Script Index

- [compare_extractors.py](#compare_extractorspy)
- [agent_shim.py](#agent_shimpy)
- [update_compare_list.py](#update_compare_listpy)
- [clean-remote-branches.sh](#clean-remote-branchessh)

---

## clean-remote-branches.sh

Interactive script to clean up remote branches on `origin` using `fzf` and GitHub CLI.

### Features
- Fetches latest remote refs from origin
- Shows ahead/behind status for each branch vs. origin/main
- Uses `fzf` for multi-selection of branches to delete
- Skips protected branches (main, develop, master, staging, production)
- Prompts for confirmation before deleting each branch
- Deletes only remote branches (not local)
- Prints a summary of deleted, skipped, and protected branches


### Usage
1. Ensure you have `fzf`, `git`, and `gh` (GitHub CLI) installed and available in your PATH.
2. Run the script from the root or scripts folder:
	```bash
	./scripts/clean-remote-branches.sh
	```
3. Follow the interactive prompts:
	- Use TAB/SPACE to select branches in the fzf menu
	- Press ENTER to confirm selection
	- Confirm deletion for each branch individually

#### How to install and use fzf in Git Bash on Windows 11

To use `fzf` in Git Bash on Windows 11, follow these steps:

1. **Download fzf Windows binary**
	- Go to the [fzf releases page](https://github.com/junegunn/fzf/releases).
	- Download the latest `fzf-<version>-windows_amd64.zip`.
	- Extract `fzf.exe` to a folder (e.g., `C:\tools\fzf`).

2. **Add fzf to your PATH**
	- Open Windows Search, type `environment variables`, and select **Edit the system environment variables**.
	- Click **Environment Variables**.
	- Under **User variables** or **System variables**, find and edit the `Path` variable.
	- Add the path to the folder where you placed `fzf.exe` (e.g., `C:\tools\fzf`).
	- Click OK to save.

3. **Restart Git Bash**
	- Close all Git Bash windows and open a new one.
	- Type `fzf` and press Enter. You should see the fzf interactive prompt.

4. **(Optional) Install fzf key bindings**
	- Key bindings and fuzzy completion are not natively available in Git Bash, but you can use fzf as a standalone tool in scripts and pipelines.

Now you can use scripts that call `fzf` in Git Bash on Windows 11.

### Notes
- Only remote branches on `origin` are affected
- Protected branches are automatically skipped with a warning
- The script does not delete local branches

---

## Script Documentation Template

### <script_name>

**Description:**

**Features:**

**Usage:**

**Notes:**

---

## Adding Documentation for New Scripts
To add documentation for a new script, copy the template above and fill in the details under a new section.
