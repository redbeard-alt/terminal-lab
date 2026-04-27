# 00_INDEX_AND_ROUTER.md
# TERMINAL LAB — INDEX & ROUTER v5

> Router and index for Terminal Lab. Use this file to jump to the right doc for shell basics, advanced workflows, AI terminal tools, MCP servers, and battle‑tested commands.

---

## Quick Trigger Commands

| Trigger | Routes To | Behavior |
|---|---|---|
| ROUTE SHELL | 01_Core_Shell_v5.md | Use shell fundamentals, safety patterns, .zshrc guidance |
| ROUTE ADVANCED | 02_Core_Advanced_v5.md | Use scripting, automation, SSH, Docker, tmux, launchd |
| ROUTE STORE | 05_Store_Database_v5.md | Pull battle-tested commands; skip fresh invention |
| ROUTE AI-TERMINAL | 06_Tool_AI_Terminal_v5.md | Use Ollama, MLX, Claude Code, zsh-ai-assist patterns |
| ROUTE MCP | 07_Meta_MCP_v5.md | Use MCP server stack concepts, install, configure, troubleshoot |
| SAFETY FLOW | (no file route) | Re-wrap the last answer into: EXPLAIN → DRY-RUN → RED TEAM → HARDEN → SCRIPT-IT → SAVE → CHAIN |
| SAVE COMMAND slug | 05_Store_Database_v5.md | Extract the last proposed command/script, format it as a ready-to-paste 05_Store entry (category, risk, dry-run/live variants, macOS Tahoe M4 context, notes), and output it |

> For HAND OFF, RED TEAM, and FIX triggers, see 00_Quick_Commands_Universal.md.

---

## Files

- `01_Core_Shell_v5.md` – Shell fundamentals, safety patterns, `.zshrc`.
- `02_Core_Advanced_v5.md` – Scripting, automation, SSH, Docker, tmux, launchd.
- `03_Tool_Command_Builder_Templates_v5.md` – Request templates and red‑team patterns.
- `04_Tool_Quick_Ref_v5.md` – Quick reference card (modern CLI first, risk‑labeled).
- `05_Store_Database_v5.md` – Command + workflow database (battle‑tested).
- `06_Tool_AI_Terminal_v5.md` – Ollama, MLX, MLX Whisper, Claude Code, zsh‑ai‑assist, VLMs, pipeline chaining.
- `07_Meta_MCP_v5.md` – MCP server stack for Claude Code (server‑fetch, server‑filesystem, Context7, local‑LLM bridge).

---

## How to Use This Index

- If the question is about **how to prompt** (Jeff Su formulas, XML tags, verbosity control, Perplexity Computer), route to **Prompt Lab**. If it's about **what to run** (commands, scripts, tooling), stay in Terminal Lab.
- If you already know the **category** (file‑ops, git, AI‑terminal, etc.), go straight to `05_Store_Database_v5.md`.
- If you need to **learn or debug**, start with:
  - `01_Core_Shell_v5.md` for fundamentals and safety patterns.
  - `02_Core_Advanced_v5.md` for scripting, automation, SSH, Docker, tmux.
- For **AI‑assisted workflows** (Ollama, MLX, Claude Code, zsh‑ai‑assist, MLX Whisper), route through `06_Tool_AI_Terminal_v5.md`, then drop to `05_Store_Database_v5.md` for concrete commands.
- For **MCP server setup, tool-using Claude sessions, or Context7**, go to `07_Meta_MCP_v5.md`.
- For **copy‑paste cheats** with risk labels, use `04_Tool_Quick_Ref_v5.md`.

---

## Routing by Task

### Shell and Scripting

- New to the terminal, or want safer patterns for `rm`, `cp`, redirects?
  - Go to `01_Core_Shell_v5.md`.
- Need robust scripts, functions, argument parsing, error handling?
  - Go to `02_Core_Advanced_v5.md` (scripting sections).
- Want templates for asking a model to write or harden scripts?
  - Go to `03_Tool_Command_Builder_Templates_v5.md`.

### System, Network, Git, and Automation

- **System inspection, monitoring, processes, disk usage**
  - `04_Tool_Quick_Ref_v5.md` – system / disk / process sections.
  - `05_Store_Database_v5.md` – `sysadmin` category.
- **Networking (ports, curl APIs, DNS, connectivity)**
  - `04_Tool_Quick_Ref_v5.md` – networking + REST API sections.
  - `05_Store_Database_v5.md` – `network` category.
- **Git hygiene, undo, branching, remote backup**
  - `02_Core_Advanced_v5.md` – git section for explanations.
  - `04_Tool_Quick_Ref_v5.md` – git section (preview‑first, risk‑labeled).
  - `05_Store_Database_v5.md` – `git` and `backup` categories for battle‑tested commands.
- **Scheduling and automation**
  - Local macOS (Tahoe 26): **launchd only** – see `02_Core_Advanced_v5.md` automation/launchd section for plist templates and load/test commands.
  - Linux/remote hosts: `cron` notes live in `02_Core_Advanced_v5.md` for when you're not on the Tahoe workstation.
  - Concrete jobs (Whisper, scrapes, model updates): `05_Store_Database_v5.md` – `automation` category.

### AI Terminal Tools (Local and Cloud)

- **Local LLM via Ollama** (CLI, background server, OpenAI‑compatible API)
  - `06_Tool_AI_Terminal_v5.md` – PART 1 (Ollama).
  - `05_Store_Database_v5.md` – `ai-terminal` category (Ollama pipe patterns).
- **MLX models** for fast single‑shot inference or Python workflows
  - `06_Tool_AI_Terminal_v5.md` – PART 2 (MLX).
  - `05_Store_Database_v5.md` – `ai-terminal` category (MLX examples).
- **Local speech‑to‑text (Whisper on M‑series Mac via MLX)**
  - `06_Tool_AI_Terminal_v5.md` – PART 2b (MLX Whisper quickstart + batch).
  - `05_Store_Database_v5.md` – workflow entries:
    - "Local BoardMeeting Videos → Whisper Transcripts (MLX, macOS)" (DRY‑RUN + live variants).
- **Claude Code as terminal agent** (Plan Mode, hooks, Teams, sandbox, budget)
  - `06_Tool_AI_Terminal_v5.md` – PART 3 (Claude Code).
  - `05_Store_Database_v5.md` – `ai-terminal` category (research workflows, sandbox patterns).
- **MCP servers for Claude Code** (tool‑using agent: fetch, filesystem, Context7, local‑LLM)
  - `07_Meta_MCP_v5.md` – concepts, install, configure, safety, troubleshoot.
  - `05_Store_Database_v5.md` – `ai-terminal` category (MCP baseline stack entries).
- **zsh-ai-assist (AI at the prompt)**
  - `06_Tool_AI_Terminal_v5.md` – PART 4 (zsh‑ai‑assist).
  - `05_Store_Database_v5.md` – `ai-terminal` category (AI command generation).
- **Vision / multimodal (local VLMs)**
  - `06_Tool_AI_Terminal_v5.md` – PART 11 (MLX VLMs).
  - `05_Store_Database_v5.md` – `ai-terminal` (image→text, diagram analysis, OCR replacement).
- **AI pipeline chaining and orchestration** (multi‑hop, validation gates, retry logic)
  - `06_Tool_AI_Terminal_v5.md` – PART 12 (pipeline chaining).
  - `05_Store_Database_v5.md` – `ai-terminal` (chain patterns for research, meeting processing, log triage).

---

### Perplexity Space Management (local scaffolding)

Query: Creating, scaffolding, or managing Perplexity Spaces from the terminal

- **Definition, structure, file naming conventions** → `docs/50_Ops_Perplexity_Space_Scaffolding.md`
- **`newspace` / `space-doc` zsh functions** → `docs/50_Ops_Perplexity_Space_Scaffolding.md`
- **Template seed file** → `/Users/bryanjhein/Perplexity-Spaces/_templates/Space_Template_v2.md`

| Query | Go to |
|---|---|
| Scaffold a new Space folder + files | `newspace <Space-Name>` — see `docs/50_Ops_Perplexity_Space_Scaffolding.md` |
| Add a `docs/` file to an existing Space | `space-doc <Space-Name> <NN_Area_Thing>` — see `docs/50_Ops_Perplexity_Space_Scaffolding.md` |
| Review Space structure or naming conventions | `docs/50_Ops_Perplexity_Space_Scaffolding.md` → Section 3 |
| Audit Space Instructions against canonical template | `docs/50_Ops_Perplexity_Space_Scaffolding.md` → Section 5 |
| Tree view of all Spaces | `eza --tree --level=2 $SPACES_ROOT` |

> Note: This is a local workflow tool — it lives in the `Perplexity-Spaces` tree, not the `terminal-lab` Git repo. It is NOT routed to Prompt Lab.

## MCP Servers Quick Routing

| Query | Go to |
|---|---|
| MCP concepts, install, configure, troubleshoot | `07_Meta_MCP_v5.md` |
| Claude Code Plan Mode, hooks, sandbox, budget caps | `06_Tool_AI_Terminal_v5.md` Part 3 |
| Claude Code sub-agents, skills, orchestration | `06b_Claude_Code_Advanced.md` |
| Building custom Python MCP servers | `07_Meta_MCP_v5.md` Part 7 + `02_Core_Advanced_v5.md` scripting |
| Battle-tested MCP stack commands | `05_Store_Database_v5.md` → `ai-terminal` |
| vLLM-MLX / Ollama server setup (prereq for local-LLM MCP) | `06_Tool_AI_Terminal_v5.md` Parts 1, 8 |

---

## Modern CLI Tools

On the Tahoe workstation (M4, zsh), **default to modern tools** for interactive work:

- `01_Core_Shell_v5.md` – modern vs classic CLI defaults.
- `04_Tool_Quick_Ref_v5.md` – "Modern CLI Alternatives" table.
- `05_Store_Database_v5.md` – `sysadmin` and `workflow` categories:
  - Brewfile + tool setup.
  - `btop`/`mactop` for long‑running jobs.
  - `rg`, `fd`, `eza`, `bat`, `zoxide`, `fzf`, `jq`, `yq`, `csvlens`, `glow`.

Classic tools (`grep`, `find`, `ls`, `cat`) remain in the docs for **remote hosts, CI, and minimal containers**, not as the default on the local M4 box.

---

## Battle-Tested Commands and Workflows

- Need a command that's already tested and documented?
  - `05_Store_Database_v5.md` is the **source of truth**.
- Categories inside `05_Store_Database_v5.md`:
  - `file-ops`, `text-proc`, `sysadmin`, `network`, `git`, `backup`,
    `dev-tools`, `docker`, `automation`, `security`, `web-scraping`,
    `ai-terminal`, `workflow playbooks`.
- For Whisper/MLX specifically:
  - See `ai-terminal` **workflow playbooks** entries.
  - Each has **DRY‑RUN** and **live** variants, with risk levels and known‑good versions.

---

## Safety and Red-Team Patterns

For safety patterns, red‑team reviews, and hardening checklists:

- `01_Core_Shell_v5.md`
  - Core safety: globbing, quoting, destructive commands.
  - Modern CLI defaults, classic fallbacks, and why.
- `02_Core_Advanced_v5.md`
  - Advanced safety: `xargs`, `find`, SSH, Docker, tmux, launchd.
  - "Dangerous patterns" vs hardened equivalents.
- `03_Tool_Command_Builder_Templates_v5.md`
  - Prompt/templates for:
    - **EXPLAIN** – what the command does and risk level.
    - **DRY-RUN** – preview before mutate.
    - **RED TEAM** – hostile SRE review.
    - **HARDEN** – rewrite with safety rails.
    - **SCRIPT-IT** – full script with `set -euo pipefail` and traps.
    - **SAVE** – add to `05_Store_Database_v5.md` with metadata.
    - **CHAIN** – safe chaining across tools/models.
- `07_Meta_MCP_v5.md`
  - MCP-specific safety: filesystem root constraints, CVE-excluded servers, PreToolUse hooks, sandbox + budget defaults.

Use these when generating new commands via models (Ollama, Claude Code, zsh‑ai‑assist) so everything added to Terminal Lab matches the same safety bar.

---

## When You're Not Sure Where to Start

- Need **one command** from plain English?
  - `03_Tool_Command_Builder_Templates_v5.md` – Template A (one‑liner).
- Need a **script** with arguments, error handling, logging?
  - Template B (shell script) in `03_Tool_Command_Builder_Templates_v5.md`.
- Command **failed** and you want to debug?
  - Template D (troubleshooting) in `03_Tool_Command_Builder_Templates_v5.md`.
  - Then jump to `01_Core_Shell_v5.md` Part 4 (debugging commands).
- Want to **harden** an existing command or script?
  - Template F (red‑team + harden) in `03_Tool_Command_Builder_Templates_v5.md`.
  - Then update `05_Store_Database_v5.md` with the hardened version.
- Want to **chain AI tools** (Whisper → Ollama → JSON extract)?
  - `06_Tool_AI_Terminal_v5.md` PART 12 (pipeline chaining).
- Want Claude to **use tools** (fetch docs, read files, call local LLM)?
  - `07_Meta_MCP_v5.md` for setup, then use Plan Mode in `claude`.

The rule of thumb: if it's new or destructive, route through `03_Tool_Command_Builder_Templates_v5.md` and `05_Store_Database_v5.md` rather than dropping raw commands directly into your notes.

---

> **NOTE:** Syntax standards, post-output protocol, and behavioral directives live in **Space Instructions** — not in this file. This file is for navigation only.

*Last updated: April 2026 | v5*
