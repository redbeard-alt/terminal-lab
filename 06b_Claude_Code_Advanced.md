# TERMINAL LAB — CLAUDE CODE ADVANCED v1
## Sub-agents, Skills & Orchestration — M4 / macOS Tahoe
**Hardware:** M4 MacBook Pro, 48 GB RAM | **Shell:** zsh | **Last updated:** April 2026

> Basics (Plan Mode, hooks, sandbox, budget caps) live in `06_Tool_AI_Terminal_v5.md` Part 3.
> This file covers the upgrade path: zero → skills → sub-agents → orchestration.
> Worked examples focus on **codebase tasks** (multi-file edits, refactors) and **file/data workflows** (transcripts, logs, CSVs).

---

## Part 1 — Mental Model

A **sub-agent** in Claude Code is Claude itself, spawned as a child process to do a bounded task in isolation — its own context window, its own tool calls, its own output. The parent agent reads the result and continues.

A **skill** is a markdown file that loads into Claude's context and gives it a specific instruction set for a domain — like a SOPs manual. Skills replace giant system prompts with composable, loadable modules.

The upgrade path:

```
Level 0: claude one-shots — "Edit this file"
Level 1: Plan Mode — Shift+Tab, review plan, approve tool calls
Level 2: Skills — load domain-specific instruction files at session start
Level 3: Sub-agents — Claude spawns child agents for bounded parallel tasks
Level 4: Orchestration — parent agent coordinates sub-agents, validates output, retries on failure
```

You don't need Level 4 for most work. Start at Level 2 (skills) — the ROI is immediate.

---

## Part 2 — Skills System

### What a skill file is

A skill is a `.md` file you load into context at session start. It tells Claude:
- What domain it's operating in
- What standards to apply
- What output format to use
- What to avoid

Skills replace ad-hoc prompting. Once written, they're reusable across sessions and projects.

### Skill file location convention

Store skills in a dedicated directory so you can reference them consistently:

```
~/Claude-Skills/
  code-review.md
  refactor-python.md
  transcript-extract.md
  log-triage.md
  csv-analysis.md
```

### Minimal skill file structure

```markdown
# Skill: [Name]
**Domain:** [codebase / file-data / research / ops]
**Version:** 1
**Last updated:** [date]

## Role
[One sentence: what Claude is doing in this skill context]

## Standards
- [Standard 1]
- [Standard 2]

## Output format
[Describe expected output: file, JSON, markdown, diff, etc.]

## Do not
- [Anti-pattern 1 specific to this domain]
- [Anti-pattern 2]
```

### Loading a skill at session start

🟢 read-only — loads context, no file writes until you approve

```bash
# Load a single skill
claude --append-system-prompt "$(cat ~/Claude-Skills/refactor-python.md)"

# Load multiple skills (combine into one prompt)
cat ~/Claude-Skills/refactor-python.md ~/Claude-Skills/code-review.md | \
  claude --append-system-prompt "$(cat /dev/stdin)"

# Load via CLAUDE.md (auto-loads for any session in that project directory)
# Add to ~/Projects/myproject/CLAUDE.md:
# "Apply the standards in ~/Claude-Skills/refactor-python.md to all edits."
```

### Auto-loading skills via CLAUDE.md

`CLAUDE.md` at the project root is read by Claude Code automatically at session start. Use it to:
- Reference which skills apply to this project
- Set project-specific constraints (no breaking changes to public API, always add tests)
- Define the output format for this codebase

```markdown
# CLAUDE.md — myproject

## Skills active for this project
- ~/Claude-Skills/refactor-python.md
- ~/Claude-Skills/code-review.md

## Project constraints
- Never modify files under src/legacy/ without explicit approval
- All new functions must have a docstring
- Run `pytest tests/` after any edit to src/

## Output format
- Diffs only — do not rewrite whole files unless asked
- Always show before/after for any rename
```

---

## Part 3 — Codebase Tasks (Multi-file Edits, Refactors)

### The standard session flow

Every codebase session follows the same five-step loop. Never skip Step 1 or Step 5.

```
1. SCOPE — narrow the task before starting
2. PLAN — Shift+Tab, review plan, approve
3. EDIT — Claude makes changes with tool calls
4. VALIDATE — run tests, check diff
5. SAVE or ROLLBACK — commit if clean, revert if not
```

### Step 1 — Scope the task

Before launching Claude, write a one-paragraph task description that answers:
- What files are in scope?
- What is the desired outcome?
- What must not change?

Save it to a temp file and pass it in:

🟢 read-only — writing the task description only

```bash
cat > /tmp/task.md << 'EOF'
Refactor the authentication module in src/auth/.
Goal: replace all uses of the deprecated `get_user_by_token()` function with `get_user(token=...)` from the new auth v2 API.
Scope: src/auth/*.py and any callers in src/api/*.py.
Do not touch: src/legacy/, tests/, or any file outside src/auth/ and src/api/.
EOF
```

### Step 2 — Launch with Plan Mode

🟡 modifies state — Claude will propose edits after plan approval

```bash
cd ~/Projects/myproject
claude --append-system-prompt "$(cat ~/Claude-Skills/refactor-python.md)"
# Inside session: press Shift+Tab to enter Plan Mode
# Paste the task description from /tmp/task.md
# Review the plan carefully before approving
# Approve only the listed files — reject if scope has crept
```

**Plan Mode review checklist:**
- [ ] Files listed match your scope definition — no extra files
- [ ] No deletions you didn't expect
- [ ] No changes to test files unless you asked
- [ ] No changes to config or lock files

### Step 3 — Validate after edits

🟢 read-only — inspection only

```bash
# See exactly what changed
git diff --stat
git diff src/auth/ src/api/

# Run tests
pytest tests/ -x --tb=short

# Check for remaining old API calls (should be zero)
rg 'get_user_by_token' src/
```

### Step 4 — Commit or rollback

Commit only if tests pass and diff looks clean:

🟡 modifies state — commits changes

```bash
git add src/auth/ src/api/
git commit -m "refactor: replace deprecated get_user_by_token with get_user(token=...)"
```

Rollback if anything looks wrong:

🔴 destructive — discards all uncommitted changes

```bash
# DRY RUN first — see what will be discarded
git diff --stat
git stash list

# LIVE — discard all uncommitted changes
git checkout -- src/auth/ src/api/
```

### Multi-file refactor with iterative sessions

For large refactors (>10 files), break into bounded sessions. Each session gets a narrow scope file and its own Plan Mode review. Never try to do a 40-file refactor in a single session — context degrades past ~20k tokens of edits.

```bash
# Session 1: auth module only
cat > /tmp/task.md << 'EOF'
Scope: src/auth/*.py only. Refactor get_user_by_token → get_user(token=...).
Do not touch callers yet.
EOF
claude --append-system-prompt "$(cat ~/Claude-Skills/refactor-python.md)"

# Validate, commit, then:

# Session 2: update callers
cat > /tmp/task.md << 'EOF'
Scope: src/api/*.py only. Update callers of get_user_by_token to use the new
get_user(token=...) signature. The auth module was already updated in the previous commit.
EOF
claude --append-system-prompt "$(cat ~/Claude-Skills/refactor-python.md)"
```

---

## Part 4 — File & Data Workflows (Transcripts, Logs, CSVs)

### Transcript → structured extract

Take a raw Whisper transcript and extract structured data (action items, decisions, open questions) into a JSON file.

🟡 modifies state — writes output JSON

```bash
# Skill file: ~/Claude-Skills/transcript-extract.md
# (Create this — see template in Part 2)

# Single transcript
claude --append-system-prompt "$(cat ~/Claude-Skills/transcript-extract.md)" << 'EOF'
Read the transcript at ~/Research/Transcripts/meeting-2026-04-14.txt.
Extract:
- Action items (owner, task, due date if mentioned)
- Decisions made
- Open questions
Output as JSON to ~/Research/Extracts/meeting-2026-04-14.json.
EOF

# Batch: process all unextracted transcripts
for f in ~/Research/Transcripts/*.txt; do
  stem=$(basename "${f%.txt}")
  out=~/Research/Extracts/${stem}.json
  [ -f "$out" ] && continue   # skip already extracted
  claude --append-system-prompt "$(cat ~/Claude-Skills/transcript-extract.md)" \
    --print "Extract structured data from $f and write JSON to $out."
done
```

### Log triage: surface anomalies

Give Claude a log file and a triage skill. Get back a prioritized list of anomalies.

🟡 modifies state — writes triage report

```bash
# Scope: one log file at a time to keep context bounded
claude --append-system-prompt "$(cat ~/Claude-Skills/log-triage.md)" << 'EOF'
Read ~/Logs/app-2026-04-14.log.
Identify:
- ERROR and CRITICAL entries
- Repeated patterns (>5 occurrences of same error)
- Timing anomalies (gaps >30s between log entries)
Output a triage report to ~/Logs/triage-2026-04-14.md with severity labels.
EOF
```

### CSV analysis and transformation

For structured data, Claude works best when you give it explicit column names and expected output format upfront.

🟡 modifies state — writes transformed CSV

```bash
claude --append-system-prompt "$(cat ~/Claude-Skills/csv-analysis.md)" << 'EOF'
Read ~/Data/budget-2026.csv.
Columns: date, category, amount, vendor, notes.
Task: group by category, sum amounts, flag any single transaction > $5000.
Output: ~/Data/budget-2026-summary.csv with columns: category, total, flagged_count.
EOF
```

### Safety rules for file/data sessions

- Always specify the output path explicitly — never let Claude decide where to write
- For batch operations, always run with `--dry-run` semantics first: ask Claude to list what it would do before doing it
- Never point Claude at raw credential files, `.env`, or `~/.ssh` directories
- After any write session, `ls -lht ~/Research/Extracts/ | head -10` to verify only expected files were created

---

## Part 5 — Orchestration (Sub-agents, Parallel Tasks, Retry)

### When to use sub-agents

Use sub-agents when a task has **independent subtasks** that don't need to share context mid-stream. If subtask B depends on subtask A's output, run them sequentially. If they're independent, parallelize.

Good candidates for sub-agents:
- Analyze 5 different log files simultaneously
- Run code review + security scan + test generation on the same PR in parallel
- Extract structured data from 20 transcripts simultaneously

Bad candidates (run sequentially instead):
- Refactor a module, then update its callers — order matters
- Extract data, then write a report from that data — output dependency

### Launching parallel sub-agents via bash

Claude Code doesn't have a native parallel-dispatch UI yet. Use zsh/bash to launch multiple bounded sessions in parallel.

🟡 modifies state — writes output files per agent

```bash
# Parallel transcript extraction — up to 4 at a time
LOG_DIR=~/Research/Transcripts
OUT_DIR=~/Research/Extracts
mkdir -p "$OUT_DIR"

# DRY RUN first — show what would run
for f in "$LOG_DIR"/*.txt; do
  stem=$(basename "${f%.txt}")
  out="$OUT_DIR/${stem}.json"
  [ -f "$out" ] && continue
  echo "WOULD PROCESS: $f → $out"
done
echo "DRY RUN COMPLETE"

# LIVE — launch up to 4 parallel claude sessions
for f in "$LOG_DIR"/*.txt; do
  stem=$(basename "${f%.txt}")
  out="$OUT_DIR/${stem}.json"
  [ -f "$out" ] && continue
  claude --print \
    --append-system-prompt "$(cat ~/Claude-Skills/transcript-extract.md)" \
    "Extract structured data from $f and write JSON to $out." &
  # Limit parallelism to 4 — M4 48GB can handle this comfortably
  while [ $(jobs -r | wc -l) -ge 4 ]; do sleep 1; done
done
wait
echo "All agents done."

# Verify
ls -lht "$OUT_DIR" | head -20
```

### Retry loop on failure

For production batch jobs, wrap each agent call in a retry loop with backoff.

🟡 modifies state — writes output files, retries on failure

```bash
set -euo pipefail

run_with_retry() {
  local cmd="$1"
  local out="$2"
  local max_attempts=3
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    if eval "$cmd"; then
      [ -f "$out" ] && [ $(wc -c < "$out") -gt 10 ] && return 0
    fi
    echo "Attempt $attempt failed for $out — retrying in ${attempt}s"
    sleep $attempt
    attempt=$((attempt + 1))
  done
  echo "FAILED after $max_attempts attempts: $out" >> /tmp/batch-errors.log
  return 1
}

for f in ~/Research/Transcripts/*.txt; do
  stem=$(basename "${f%.txt}")
  out=~/Research/Extracts/${stem}.json
  [ -f "$out" ] && [ $(wc -c < "$out") -gt 10 ] && continue

  cmd="claude --print \
    --append-system-prompt \"\$(cat ~/Claude-Skills/transcript-extract.md)\" \
    \"Extract structured data from $f and write JSON to $out.\""

  run_with_retry "$cmd" "$out"
done

echo "Batch complete. Errors (if any): /tmp/batch-errors.log"
```

### Validation gate pattern

After any multi-agent batch, run a validation pass before treating output as complete.

🟢 read-only — inspection only

```bash
# Validate all JSON outputs are well-formed and non-empty
ERRORS=0
for f in ~/Research/Extracts/*.json; do
  if ! jq empty "$f" 2>/dev/null; then
    echo "INVALID JSON: $f"
    ERRORS=$((ERRORS + 1))
  fi
  if [ $(wc -c < "$f") -lt 50 ]; then
    echo "SUSPICIOUSLY SMALL: $f ($(wc -c < $f) bytes)"
    ERRORS=$((ERRORS + 1))
  fi
done
echo "Validation complete. Errors: $ERRORS"
```

---

## Part 6 — Safety Rails for Agentic Runs

The more autonomous Claude is, the more important the guardrails.

### Non-negotiable rules for any sub-agent or batch session

- **Always dry-run first.** For any batch that writes files, show what would happen before doing it. This is non-negotiable.
- **Explicit output paths only.** Never let Claude or a script choose where to write without you specifying the directory.
- **Narrow filesystem scope.** If using `server-filesystem` MCP, verify allowed roots are narrow before the session. See `07_Meta_MCP_v5.md` Part 8.
- **Budget cap for long sessions.** `claude --max-budget-usd 10.00` for any session expected to run >15 minutes.
- **Sandbox for external content.** `claude --sandbox` when processing scraped docs, unknown repos, or external transcripts. Prompt injection is real.
- **`git diff` after every session.** Even read-only sessions can trigger unexpected tool calls. Always inspect what changed.
- **No credentials in task descriptions.** Never paste API keys, tokens, or passwords into the task file or session prompt.

### Session close checklist

After every agentic session:

```bash
git diff --stat                          # What changed?
git status                               # Anything untracked?
ls -lht ~/Research/Extracts/ | head -10  # Files written where expected?
jq empty ~/Research/Extracts/*.json      # Outputs valid?
cat /tmp/batch-errors.log 2>/dev/null    # Any retry failures?
```

---

## Part 7 — Routing Reference

| Query | Go to |
|---|---|
| Plan Mode, hooks, sandbox, budget basics | `06_Tool_AI_Terminal_v5.md` Part 3 |
| MCP server setup and tool-using sessions | `07_Meta_MCP_v5.md` |
| Sub-agents, skills, orchestration (this file) | `06b_Claude_Code_Advanced.md` |
| Battle-tested commands | `05_Store_Database_v5.md` → `ai-terminal` |
| Shell scripting, set -euo pipefail, traps | `02_Core_Advanced_v5.md` |

---

*Last updated: April 2026 | v1*
