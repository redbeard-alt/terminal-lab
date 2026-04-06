# Terminal Lab

Senior systems engineer and terminal command assistant. Workstation: **M4 MacBook Pro, 48 GB RAM**, macOS Tahoe (auto-updated). Shell: **zsh**.

This Space helps build, test, debug, and catalog terminal commands, shell scripts, and local AI terminal workflows.

Covers:
- One-liners and pipelines
- Bash/zsh scripting and automation
- SSH, Docker, tmux
- Local AI tools (Ollama, MLX, MLX Whisper, Claude Code, zsh-ai-assist)

Router and reference files:
- `00_Index_and_Router.md` – task-based router for the whole Space
- `01_Core_Shell.md` – shell fundamentals, safety patterns, .zshrc
- `02_Core_Advanced.md` – scripting, automation, SSH, Docker, tmux, launchd
- `03_Tool_Command_Builder_Templates.md` – templates + red-team checklists
- `04_Tool_QuickRef.md` – quick reference / cheat sheet
- `05_Store_Database.md` – command + workflow database (battle-tested)
- `06_AI_Terminal.md` – AI terminal tools (Ollama, MLX, Whisper, Claude, zsh-ai-assist)

---

## Environment & Version Policy

This Space is tuned for **my** primary workstation. Commands assume:

- **Hardware:** M4 MacBook Pro, 48 GB RAM
- **OS:** macOS Tahoe (latest auto-updated build)
- **Package manager:** Homebrew (latest)
- **Python:** `python3` from Homebrew, kept at the latest stable version
- **AI libs:** `mlx-lm`, `mlx-whisper`, Ollama, Claude Code, zsh-ai-assist – always updated to latest stable release
- **CLI tools:** `rg`, `fd`, `eza`, `bat`, `zoxide`, `btop`, `ffmpeg`, `jq`, `fzf`, `fd`, `yq` – installed and updated via Homebrew

**Version policy**

- Default to **latest stable** via Homebrew / PyPI / NPM for all tools.
- Each heavy workflow (scraping, Whisper, model updates) documents at least one **known-good combo** (Python/lib versions + date) so regressions are debuggable later.
- All heavy workflows assume an **M‑series Mac with ≥32 GB RAM**; Intel Macs and low‑RAM machines are out of scope.

When in doubt, run:

```bash
python3 --version
ffmpeg -version | head -1
pip list | grep -E 'mlx|whisper'
ollama --version
```

and record versions in the workflow notes.

---

## Safety & Workflow Defaults

All commands in this Space follow these defaults:

- **Explain before execute** – every non-trivial command has a short explanation and risk level.
- **DRY-RUN before mutate** – destructive or heavy commands must have a preview form (e.g., `-print` or `--dry-run`) before the live version.
- **Shell safety** – assume `zsh`, with correct quoting and globbing. Avoid unguarded `rm -rf`, `find -delete`, `sed -i` across trees, or loops that write/delete without a dry-run.
- **Python safety** – use `python3 -m venv` + `pip` inside venv; never `pip` into system Python.
- **Claude Code safety** – always use **Plan Mode (Shift+Tab)** before any file write; always `git diff` after a session that modified files.
- **Batch job defaults** – for Whisper, scraping, or large model work:
  - Run on **AC power**, one heavy job at a time by default.
  - Prefer **dry-run scripts** before real batch scripts.
  - Monitor with `btop` / `mactop` when running long jobs.

If a command or script in this Space doesn’t follow these defaults, it must say why.

---

## File Map

### 00_Index_and_Router.md

- Top-level router by task.
- Use to decide whether you’re in shell basics, advanced workflows, or AI-terminal territory.

### 01_Core_Shell.md

- Shell fundamentals: command anatomy, quoting, globbing, redirection.
- Safety patterns: avoiding accidental `rm`, dealing with spaces/newlines in paths.
- `.zshrc` structure and organization.

### 02_Core_Advanced.md

- Bash/zsh scripting, functions, argument parsing, `set -euo pipefail`.
- Automation: `launchd` on macOS (no cron), basic tmux patterns.
- SSH and key management.
- Docker basics and safe cleanup patterns.

### 03_Tool_Command_Builder_Templates.md

- Templates for asking the model to:
  - Generate commands and scripts.
  - Debug failing commands.
  - Red-team and harden scripts.
- Encodes the **EXPLAIN · DRY-RUN · RED TEAM · HARDEN · SCRIPT-IT · SAVE · CHAIN** flow.

### 04_Tool_QuickRef.md

- Quick reference / cheat sheet for:
  - File ops, text processing, processes, disk usage.
  - Networking, curl API patterns, Git basics.
  - Modern CLI tools (`rg`, `fd`, `eza`, `bat`, `zoxide`, `btop`).

### 05_Store_Database.md

- Command and workflow database.
- Organized by `Use Case` (file-ops, sysadmin, git, ai-terminal, etc.).
- Each entry has risk level, what it does, tested date, and notes.
- Includes heavy workflows such as:
  - SVVSD board docs scrape + consolidate → NotebookLM.
  - Local meeting videos → MLX Whisper transcripts (with dry-run and live scripts).
  - Research session aliases + Ollama/Claude integration.

### 06_AI_Terminal.md

- AI terminal integration guide for:
  - **Ollama** – local model runner, OpenAI-compatible API.
  - **MLX** – Apple Silicon-native inference, including **MLX Whisper** (ASR) quickstart.
  - **Claude Code** – terminal AI agent (Plan Mode, hooks, Teams, sandbox).
  - **zsh-ai-assist** – inline AI at the prompt.
- Cross-referenced with `05_Store_Database.md` for concrete workflows.

---

## How to Extend This Space

When adding new commands or workflows:

1. **Decide category** – file-ops, sysadmin, ai-terminal, etc.
2. **Write DRY-RUN first** – preview or `--dry-run` form before any mutation.
3. **Add to 05_Store_Database.md** using the standard entry template.
4. **Reference from 00_Index_and_Router.md** if it’s a substantial new workflow.
5. **Note environment** – if it relies on specific Python/MLX/Ollama behavior, capture a known-good combo with date.

The goal: a growing, trusted library of commands you can paste and run on the M4 Tahoe box with high confidence.