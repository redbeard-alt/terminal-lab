# Terminal Lab

Senior systems engineer and terminal command assistant.
**Workstation:** M4 MacBook Pro, 48 GB RAM, macOS Tahoe 26. **Shell:** zsh.

This Space helps build, test, debug, and catalog terminal commands, shell scripts, and local AI terminal workflows. Covers:

- One-liners and pipelines
- Bash/zsh scripting and automation
- SSH, Docker, tmux
- Local AI tools: Ollama, MLX, MLX Whisper, Claude Code, zsh-ai-assist
- **MCP servers** for Claude Code: server-fetch, server-filesystem, Context7, local-LLM bridge

---

## File Map

| File | Purpose |
|---|---|
| `00_Index_and_Router.md` | Task-based router — jump to the right file for shell basics, advanced workflows, AI tools, MCP servers, or battle-tested commands |
| `01_Core_Shell.md` | Shell fundamentals, safety patterns, `.zshrc` |
| `02_Core_Advanced.md` | Scripting, automation (launchd), SSH, Docker, tmux |
| `03_Tool_Command_Builder_Templates.md` | Request templates and red-team checklists |
| `04_Tool_QuickRef.md` | One-page cheat sheet — file ops, text processing, Git, networking, modern CLI tools |
| `05_Store_Database.md` | Command and workflow database with risk ratings, tested dates, and heavy workflows (scraping, Whisper transcripts, MCP stacks) |
| `06_AI_Terminal.md` | Ollama, MLX, MLX Whisper, Claude Code, zsh-ai-assist, VLMs (Part 11), pipeline chaining (Part 12) |
| `07_MCP.md` | MCP server stack for Claude Code — install, configure, safety, troubleshoot, custom server template |

---

## Environment and Version Policy

This Space is tuned for my primary workstation. Commands assume:

- **Hardware:** M4 MacBook Pro, 48 GB RAM
- **OS:** macOS Tahoe 26
- **Package manager:** Homebrew, latest stable
- **Python:** `python3` from Homebrew, latest stable (PEP 668 — no system pip)
- **AI libs:** `mlx-lm`, `mlx-whisper`, Ollama, Claude Code, zsh-ai-assist — always updated to latest stable release
- **CLI tools:** `rg`, `fd`, `eza`, `bat`, `zoxide`, `btop`, `ffmpeg`, `jq`, `fzf`, `yq` — installed and updated via Homebrew
- **MCP runners:** `npx` (Node ≥ 18), `uvx` (uv) — see `07_MCP.md` Part 4 for version checks

**Version policy:**
- Default to latest stable via Homebrew / PyPI / NPM for all tools.
- Each heavy workflow (scraping, Whisper, model updates, MCP stacks) documents at least one known-good combo (Python/lib versions + date) so regressions are debuggable.
- All heavy workflows assume an M-series Mac with 32 GB+ RAM. Intel Macs and low-RAM machines are out of scope.

When in doubt, run:

```bash
python3 --version
ffmpeg -version | head -1
pip list | grep -E "mlx|whisper"
ollama --version
claude --version
node --version
```

Record versions in workflow notes.

---

## Safety and Workflow Defaults

All commands in this Space follow these defaults:

- **Explain before execute** — every non-trivial command has a short explanation and risk level.
- **DRY-RUN before mutate** — destructive or heavy commands must have a preview form (`-print`, `-n`, or `--dry-run`) before the live version.
- **Shell safety** — assume zsh, with correct quoting and globbing. Avoid unguarded `rm -rf`, `find -delete`, `sed -i` across trees, or loops that write/delete without a dry-run.
- **Python safety** — use `python3 -m venv` + `pip` inside venv; never `pip` into system Python.
- **Claude Code safety** — always use Plan Mode (`Shift+Tab`) before any file write; always `git diff` after a session that modified files.
- **MCP safety** — filesystem server roots constrained to explicit subdirectories (never `~` or `/`); git MCP server excluded (CVE-2025-68143/44/45); `ENABLE_TOOL_SEARCH=auto` with 3+ servers. See `07_MCP.md` Part 8.
- **Batch job defaults** (Whisper, scraping, large model work):
  - Run on AC power, one heavy job at a time.
  - Prefer dry-run scripts before real batch scripts.
  - Monitor with `btop` / `mactop` when running long jobs.

If a command or script in this Space doesn't follow these defaults, it must say why.

---

## Risk Levels

Throughout the docs, commands are marked with:

- 🟢 **read-only** — no mutation, safe to run if the target path is correct.
- 🟡 **modifies state** — writes files, changes permissions, or alters running processes.
- 🔴 **destructive / high-risk** — deletes data, resets Git history, or makes broad recursive changes.

The rule: run previews first, then decide whether the live variant is appropriate.

---

## AI Credential Rules (Never Violate)

1. **NEVER** pipe credentials, SSH keys, or `.zshenv` to any model — local or cloud.
   - `cat ~/.ssh/id_rsa | ollama run ...` → NEVER
   - `cat ~/.zshenv | claude ...` → NEVER
2. **NEVER** put API keys directly in shell history or MCP descriptors — use `${VAR}` in config, store keys in `.zshenv`.
3. **Claude Code** — ALWAYS use Plan Mode (`Shift+Tab`) before file modifications.
4. After EVERY Claude Code file session: `git diff` + `git status`.
5. MCP servers run as local processes with session context access — only add servers you can review or trust the maintainer of.

---

## Scheduling Guidance

- **Local macOS (Tahoe 26): launchd only.** See `02_Core_Advanced.md` Part 5 for plist templates and load/test commands.
- **cron**: Linux/remote hosts only. Not for the Tahoe workstation.

---

## How to Extend This Space

When adding new commands or workflows:

1. Decide category: `file-ops`, `sysadmin`, `network`, `git`, `docker`, `ai-terminal`, `workflow-playbook`, etc.
2. Write DRY-RUN first — preview or `--dry-run`/`-n` form before any mutation.
3. Mark risk — annotate commands with 🟢/🟡/🔴 and a one-line explanation.
4. Add to `05_Store_Database.md` using the standard entry template.
5. Reference from `00_Index_and_Router.md` if it's a substantial new workflow.
6. Note environment — if it relies on specific Python/MLX/Ollama/MCP behavior, capture a known-good combo with date.
7. For MCP stacks specifically — add a `05_Store_Database.md` entry under `ai-terminal` with scope, roots, server versions, and tested date. See `07_MCP.md` Part 10 for the template.

The goal: a growing, trusted library of commands you can paste and run on the M4/Tahoe box with high confidence, knowing every destructive path has a documented, previewed, and deliberate dry-run ahead of it.

---

*Last updated: April 2026 | v5*
