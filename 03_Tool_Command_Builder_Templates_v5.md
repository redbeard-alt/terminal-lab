# 03_TOOL_COMMAND_BUILDER_TEMPLATE
# TERMINAL LAB — COMMAND BUILDER TEMPLATES v4
> Fill-in templates for requesting terminal commands.
> Copy → fill in brackets → paste into thread.
> Last updated: April 2026

---

## TEMPLATE A: ONE-LINER / QUICK COMMAND

```
<os>[macOS / Ubuntu / Fedora / WSL]</os>

<task>
I need to [find / delete / move / convert / list / count / monitor]
[files / processes / text / network / packages / permissions]
that [match pattern / older than / larger than / owned by / in directory]
</task>

<constraints>
- [Recursive / current dir only]
- [Dry-run first / execute immediately]
- [Preserve originals / overwrite OK]
- [Human-readable output / machine-parseable]
</constraints>

<context>
[File types, directory paths, expected output format]
</context>
```

**Example:**
```
<os>macOS</os>
<task>Find all .log files larger than 100MB in /var/log not modified in 30 days</task>
<constraints>- Recursive · Dry-run first · Human-readable sizes</constraints>
<context>Review list before deleting anything.</context>
```

---

## TEMPLATE B: SHELL SCRIPT

```
<os>[macOS / Ubuntu / Fedora]</os>
<shell>[bash / zsh / sh]</shell>

<goal>
Write a script that [end-to-end workflow in plain English].
</goal>

<inputs>
- [Arguments or env vars the script takes]
</inputs>

<behavior>
1. [Step 1]
2. [Step 2]
3. [Step 3]
</behavior>

<error_handling>
- On failure: [exit / retry N times / log and continue]
- Logging: [to file / stdout / both]
</error_handling>

<output>
- [What it produces: files, stdout, exit code]
- [Where output goes: path, pipe, variable]
</output>

<constraints>
- [No external deps / specific tools available]
- [Must run as non-root / requires sudo]
- [Idempotent: safe to run multiple times]
</constraints>
```

**Example:**
```
<os>macOS</os><shell>bash</shell>
<goal>Back up a PostgreSQL database, compress it, delete backups older than 7 days.</goal>
<inputs>- DB name as $1 · PG credentials from PGUSER, PGPASSWORD, PGHOST</inputs>
<behavior>1. pg_dump  2. gzip  3. mv to ~/backups/  4. delete .gz older than 7d</behavior>
<error_handling>- Exit on dump failure · Log to ~/backups/backup.log</error_handling>
<output>- Compressed .sql.gz in ~/backups/ · Log entry with timestamp and size</output>
<constraints>- pg_dump + gzip required · Safe to run via cron · Idempotent</constraints>
```

---

## TEMPLATE C: SCHEDULED TASK

```
<os>[macOS / Ubuntu / Windows]</os>
<scheduler>[launchd / cron / systemd timer / schtasks]</scheduler>

<command>
[The command or script path to schedule]
</command>

<schedule>
[Plain English: "Every weekday at 9am" / "Every 15 minutes" / "First of each month"]
</schedule>

<logging>
[File path / syslog / /dev/null]
</logging>

<constraints>
- [User account to run as]
- [Env vars needed]
- [Must not overlap with previous run]
</constraints>
```

> **macOS default:** always use launchd — see `02_Core Part 5` for plist templates and load/test commands.

---

## TEMPLATE D: TROUBLESHOOTING / DEBUG

```
<os>[macOS / Ubuntu / etc.]</os>
<shell>[bash / zsh]</shell>

<command_that_failed>
[Exact command you ran]
</command_that_failed>

<error_output>
[Exact error message]
</error_output>

<expected_behavior>
[What you expected]
</expected_behavior>

<actual_behavior>
[What happened]
</actual_behavior>

<context>
- Installed via: [brew / apt / pip / manual]
- Shell version: [zsh --version]
- Recent changes: [anything updated or modified]
</context>
```

**Self-diagnose before filing:**
```bash
echo $?                    # Exit code (0 = success)
command -v <toolname>      # Installed and in PATH?
ls -la <target_file>       # Permissions
set -x; <your command>     # Trace execution step by step
```

---

## TEMPLATE E: AI-GENERATED COMMAND

Use for generating commands from plain English — in-thread, via `ai "description"` (zsh-ai-assist), or via Claude Code.

```
<goal>
I need a command that [input → transformation → output, be specific].
</goal>

<environment>
- OS: macOS Tahoe 26 / M4
- Shell: zsh
- Working directory: [path]
- Tools available: ripgrep, fd, jq, ollama, glow, eza, bat, zoxide
</environment>

<constraints>
- Format: [single command / pipeline / short script]
- Execution: [dry-run preview first / explain flags only / execute immediately]
- Output: [human-readable / JSON / CSV / saved to file]
- Safety: [read-only / modifications OK / destructive OK with dry-run]
</constraints>

<context>
[File types, directory structure, what you tried, what failed]
</context>
```

**Example:**
```
<goal>Find all .md files in ~/Research modified in last 7 days containing "Ollama",
show filename + matching line.</goal>
<environment>macOS Tahoe 26 · zsh · ~/Research · ripgrep, fd available</environment>
<constraints>Single pipeline · Show command first · filename:line:match · Read-only</constraints>
<context>Updating notes with current Ollama model names.</context>
```

**Quick variant for zsh-ai-assist:**
```bash
ai "find all .md files in ~/Research modified in last 7 days containing 'Ollama'"
ai "using ripgrep, search ~/Research recursively for 'API key' in .md and .txt files"
ai "dry-run only: show what find /tmp -mtime +30 -delete would remove"
some_failing_command
??   # Fix last failed command
```

---

## TEMPLATE F: RED-TEAM & HARDEN A SCRIPT

Use after you already have a draft command or script.

```
<os>[macOS / Ubuntu / etc.]</os>
<shell>[bash / zsh]</shell>

<artifact_type>[one-liner / pipeline / script]</artifact_type>

<artifact>
[Paste the command or script to attack and harden]
</artifact>

<threat_model>
Review this as a [hostile sysadmin / SRE / security engineer].
You have 60 seconds to find reasons to reject this.
</threat_model>

<focus_areas>
- destructive potential and missing safety rails
- bad quoting, globbing, and word-splitting hazards
- spaces/newlines or special chars in paths and input
- missing `set -euo pipefail` where appropriate
- unsafe `xargs`, `find`, `sed -i`, or write/delete loops
- missing dry-run path before mutation
- bad assumptions about OS, shell, PATH, tools, permissions
- cloud/privacy leakage for local AI workflows
- poor rollback or no backup
- non-idempotent behavior for repeated runs
</focus_areas>

<tasks>
1. RED TEAM: List concrete weaknesses and failure modes.
2. HARDEN: Rewrite the weakest parts to survive those attacks.
3. EXPLAIN: Briefly justify each hardening change.
</tasks>
```

**Example:**
```
<os>macOS</os>
<shell>bash</shell>
<artifact_type>script</artifact_type>
<artifact>
#!/usr/bin/env bash
LOG_DIR="$HOME/logs"
find "$LOG_DIR" -type f -mtime +30 -delete
</artifact>
<threat_model>Review as hostile SRE on-call for this box.</threat_model>
<focus_areas>
- destructive find -delete
- missing dry-run and logging
- missing set -euo pipefail
- assumptions about LOG_DIR existence and perms
</focus_areas>
<tasks>
1. RED TEAM: enumerate risks.
2. HARDEN: add safety rails and logging.
3. EXPLAIN: why each change.
</tasks>
```

---

*Last updated: April 2026 (v4)*
