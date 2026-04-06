TITLE Terminal Lab Index & Router v4

Overview
- Purpose: Router and index for Terminal Lab. Helps you jump to the right file for shell basics, advanced workflows, AI terminal tools, and battle-tested commands.
- Files:
  - 01_Core_Shell.md – Shell fundamentals, safety patterns, .zshrc.
  - 02_Core_Advanced.md – Scripting, automation, SSH, Docker, tmux, launchd.
  - 03_Tool_Command_Builder_Templates.md – Request templates and red-team patterns.
  - 04_Tool_QuickRef.md – One-page cheat sheet.
  - 05_Store_Database.md – Command & workflow database.
  - 06_AI_Terminal.md – Ollama, MLX, Claude Code, zsh-ai-assist.

How to Use This Index
- If you know what category you’re in (file-ops, git, AI-terminal, etc.), go straight to 05_Store_Database.md.
- If you need to learn or debug, start with 01_Core_Shell.md or 02_Core_Advanced.md, then drop to 05_Store for ready-made commands.
- For AI-assisted workflows (Ollama, MLX, Claude Code, zsh-ai-assist, MLX Whisper), route through 06_AI_Terminal.md.

Routing by Task

Shell and Scripting
- New to the terminal, or want safer patterns for rm, cp, redirects?
  - Go to 01_Core_Shell.md.
- Need robust scripts, functions, argument parsing, error handling?
  - Go to 02_Core_Advanced.md (scripting sections).
- Want templates for asking the model to write or harden scripts?
  - Go to 03_Tool_Command_Builder_Templates.md.

System, Network, Git, and Automation
- System inspection, monitoring, processes, disk usage?
  - 04_Tool_QuickRef.md (sysadmin section).
  - 05_Store_Database.md → sysadmin category.
- Networking (ports, curl APIs, DNS, connectivity)?
  - 04_Tool_QuickRef.md (network section).
  - 05_Store_Database.md → network category.
- Git hygiene, undo, branching, remote backup?
  - 02_Core_Advanced.md (git section) for explanations.
  - 05_Store_Database.md → git and backup categories for commands.
- Scheduling and automation (launchd on macOS, cron on Linux)?
  - 02_Core_Advanced.md → automation/launchd section.
  - 05_Store_Database.md → automation category.

AI Terminal Tools (Local and Cloud)
- Local LLM via Ollama (CLI server, background model, OpenAI-compatible API)?
  - 06_AI_Terminal.md → PART 1 Ollama.
  - 05_Store_Database.md → ai-terminal category, Ollama pipe patterns.
- Local MLX models for fast single-shot inference or Python workflows?
  - 06_AI_Terminal.md → PART 2 MLX.
  - 05_Store_Database.md → ai-terminal category, MLX examples.
- Local speech-to-text (Whisper) on M-series Mac with MLX?
  - 06_AI_Terminal.md → PART 2 “MLX WHISPER (LOCAL SPEECH-TO-TEXT) QUICKSTART”.
  - 05_Store_Database.md → Workflow “Local Board/Meeting Videos → Whisper Transcripts (MLX, macOS)” and DRY-RUN variant.
- Claude Code as terminal agent (Plan Mode, hooks, Teams)?
  - 06_AI_Terminal.md → PART 3 Claude Code.
  - 05_Store_Database.md → ai-terminal category, research workflows.
- zsh-ai-assist / inline AI at the prompt?
  - 06_AI_Terminal.md → PART 4 zsh-ai-assist.
  - 05_Store_Database.md → ai-terminal category, AI command generation.

Modern CLI Tools
- For modern replacements like rg, fd, eza, bat, zoxide, btop:
  - 04_Tool_QuickRef.md → modern tools section.
  - 05_Store_Database.md → sysadmin and workflow categories (Brewfile, tool setup).

Battle-Tested Commands and Workflows
- Need a command that’s already tested and documented?
  - 05_Store_Database.md is the source of truth.
- Categories inside 05_Store_Database.md:
  - file-ops, text-proc, sysadmin, network, git, backup, dev-tools, docker, automation, security, web-scraping, ai-terminal, workflow playbooks.
- For Whisper/MLX specifically:
  - See ai-terminal + workflow playbooks categories.

Safety and Red-Team Patterns
- For safety patterns, red-team reviews, and hardening checklists:
  - 01_Core_Shell.md → core safety (globbing, quoting, destructive commands).
  - 02_Core_Advanced.md → advanced safety (xargs, find, SSH, Docker).
  - 03_Tool_Command_Builder_Templates.md → prompts/templates for EXPLAIN · DRY-RUN · RED TEAM · HARDEN · SCRIPT-IT · SAVE · CHAIN flows.

Last updated: April 2026
