# Thread 8 — research-agent: Final Rename + Pinning

## What This Thread Is

Close the last open work on `redbeard-alt/research-agent` to reach
AGENT_SPEC.md §1 + §3 compliance. This is the only remaining blocker
across all three agents.

audio-agent and newsletter-agent are both 🟢 compliant on main as of
end of Thread 7. research-agent is 🟡 — most scaffolding is done; only
the package rename and requirements.txt pinning remain.

---

## State of the Repo (end of Thread 7)

### Already on main — do NOT redo

| Item | Status |
|---|---|
| `CLAUDE.md` | ✅ 5.2KB (references `agent/` — must update on rename) |
| `README.md` | ✅ 2.6KB |
| `cli.py` | ✅ 25.7KB, click subcommands; 12 `from agent import X` sites |
| `docs/workflow.md` | ✅ 10KB |
| `docs/notebooklm-workflow.md` | ✅ 7.4KB |
| `Makefile` | ✅ has `install`, `run`, `test`, `lint`, `clean` (commit `74ec2cf`) |
| `.env.example` | ✅ has all spec vars (commit `74ec2cf`) |
| `run.py` | ✅ deleted (commit `051cae2`) |
| `agent/rag.py` | ✅ already LanceDB + `sentence-transformers/all-MiniLM-L6-v2` |
| `.claude/skills/` | ✅ exists |

### Still open — this thread closes these

| Gap | Spec ref | Method |
|---|---|---|
| `agent/` → `research_agent/` rename | §1 | Copilot PR A |
| `research_agent/_paths.py` | §1 | Copilot PR A |
| All `from agent.` imports rewritten | §1 | Copilot PR A |
| `CLAUDE.md` references updated | §1 | Copilot PR A |
| `requirements.txt` pinned `>=` → `==` | §3 | Copilot PR B |

### Why a fresh Copilot PR (not manual)

Previous attempt was PR #9. Copilot session was cancelled, branch was
deleted, no usable diff was produced. Manual rename was rejected because
it touches 14 package files plus `cli.py`, `ocr_990_pdfs.py`, `CLAUDE.md`,
and `requirements.txt` — without a complete local snapshot of all 13
package modules, manual risks broken imports or partial moves.

---

## Verified Import Map

### `cli.py` — 12 lazy `from agent import X` statements

`archive`, `index`, `pdf`, `scrape`, `youtube` (in `run_pipeline`);
`project` (×2 in `research`, `notebooklm_cmd`); `discover` (in `research`);
`fetch990` (×2 in `fetch990`, `lookup990`); `summarize990` (in `fetch990`);
`osint` (in `research_person`); `rag` (×3 in `_build_rag`, `search`, `stats`);
`interview` (in `project_cmd`); `notebooklm` (in `notebooklm_cmd`).

All use `from agent import X`. No `import agent.X`.

### `ocr_990_pdfs.py` — 1 statement

`from agent import archive as arc, index as idx, rag`

### Inside `agent/*.py`

Not exhaustively verified end-to-end (sandbox bulk fetch timed out).
Copilot must grep the whole package for any remaining `from agent.` or
`import agent.` and rewrite.

---

## Files to Move (all 14)

```
agent/__init__.py → research_agent/__init__.py
agent/archive.py → research_agent/archive.py
agent/discover.py → research_agent/discover.py
agent/fetch990.py → research_agent/fetch990.py
agent/index.py → research_agent/index.py
agent/interview.py → research_agent/interview.py
agent/notebooklm.py → research_agent/notebooklm.py
agent/osint.py → research_agent/osint.py
agent/pdf.py → research_agent/pdf.py
agent/project.py → research_agent/project.py
agent/rag.py → research_agent/rag.py
agent/scrape.py → research_agent/scrape.py
agent/summarize990.py → research_agent/summarize990.py
agent/youtube.py → research_agent/youtube.py
```

Then delete the empty `agent/` directory.

---

## `_paths.py` Template

```python
"""Centralized path constants for research_agent."""
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RUNS_DIR = REPO_ROOT / "runs"
DATA_DIR = REPO_ROOT / "data"
ARCHIVE_DIR = DATA_DIR / "archive"
LANCE_DB_PATH = DATA_DIR / "lancedb"
DB_PATH = ARCHIVE_DIR / "store.db"
```

---

## Strategy: Two PRs, Sequential

| PR | Scope | Why separate |
|---|---|---|
| A | Rename + `_paths.py` + imports + CLAUDE.md | Mechanical, single-rename diff |
| B | `requirements.txt` pinning | Independent; one-file diff |

Do them sequentially, not in parallel — simultaneous PRs cause merge
conflicts on `requirements.txt`.

---

## Copilot Prompt — PR A (rename)

**Title:** `fix: rename agent/ → research_agent/, add _paths.py, update imports (AGENT_SPEC §1)`

```
Context:
AGENT_SPEC.md §1 requires the Python package directory to be named after the
agent (research_agent/), not the generic agent/. §1 also requires a _paths.py
module inside the package.

Tasks:
1. Move all 14 files from agent/ to research_agent/. List:
   agent/__init__.py → research_agent/__init__.py
   agent/archive.py → research_agent/archive.py
   agent/discover.py → research_agent/discover.py
   agent/fetch990.py → research_agent/fetch990.py
   agent/index.py → research_agent/index.py
   agent/interview.py → research_agent/interview.py
   agent/notebooklm.py → research_agent/notebooklm.py
   agent/osint.py → research_agent/osint.py
   agent/pdf.py → research_agent/pdf.py
   agent/project.py → research_agent/project.py
   agent/rag.py → research_agent/rag.py
   agent/scrape.py → research_agent/scrape.py
   agent/summarize990.py → research_agent/summarize990.py
   agent/youtube.py → research_agent/youtube.py
   Delete the empty agent/ directory after moving.

2. Update all imports:
   In cli.py: replace every `from agent import X` with `from research_agent import X`
   (12 occurrences across run_pipeline, research, fetch990, lookup990,
   _build_rag, search, stats, project_cmd, notebooklm_cmd).
   In ocr_990_pdfs.py: replace `from agent import archive as arc, index as idx, rag`
   with `from research_agent import archive as arc, index as idx, rag`.
   Inside each module in research_agent/: grep for any cross-module
   `from agent.` or `import agent.` and rewrite to `research_agent.`.

3. Add research_agent/_paths.py with:
   """Centralized path constants for research_agent."""
   from pathlib import Path
   REPO_ROOT = Path(__file__).parent.parent
   RUNS_DIR = REPO_ROOT / "runs"
   DATA_DIR = REPO_ROOT / "data"
   ARCHIVE_DIR = DATA_DIR / "archive"
   LANCE_DB_PATH = DATA_DIR / "lancedb"
   DB_PATH = ARCHIVE_DIR / "store.db"

4. Update CLAUDE.md: replace every `agent/` with `research_agent/` and
   every `from agent.` with `from research_agent.`.

Do NOT touch:
- requirements.txt (separate PR)
- Makefile, .env.example, README.md, docs/* (already compliant)
- .claude/skills/ (already compliant)

Acceptance criteria:
- agent/ directory no longer exists
- research_agent/ exists with all 14 modules + new _paths.py
- `grep -r "from agent" .` returns nothing
- `grep -r "import agent" .` returns nothing
- CLAUDE.md references updated
```

---

## Copilot Prompt — PR B (pinning, queue AFTER PR A merges)

**Title:** `fix: pin requirements.txt to exact versions (AGENT_SPEC §3)`

```
Replace every >= with == exact pinned versions, using current stable
releases as of May 2026. Preserve all comments and section groupings.
Do not add or remove any packages.

Current state:
requests>=2.32
beautifulsoup4>=4.12
lxml>=5.2
trafilatura>=1.9
playwright>=1.44
pdfplumber>=0.11
yt-dlp>=2024.4
faster-whisper>=1.0
lancedb>=0.6
sentence-transformers>=3.0
numpy>=1.26
openai>=1.30
anthropic>=0.40
click>=8.1
python-dotenv>=1.0
tqdm>=4.66
```

---

## After Both PRs Merge — AGENT_SPEC Update

Update `redbeard-alt/terminal-lab/AGENT_SPEC.md`:

**§9 status table** — flip research-agent to 🟢 compliant:
- Package Dir: `research_agent/` ✅
- cli.py: ✅
- CLAUDE.md: ✅
- RAG Backend: LanceDB ✅ (was already true; spec was stale)
- Status: 🟢 compliant

**§10 checklist** — tick all research-agent items. Note inaccuracies
in the original checklist:
- FAISS → LanceDB migration was unnecessary (already done)
- CLAUDE.md was already present end of Thread 7

After this update, **all three agents are 🟢 compliant.**

---

## Quick-Start for Thread 8

1. Verify state: list `redbeard-alt/research-agent` root, confirm `agent/`
   still exists, `cli.py` imports still say `from agent`, `requirements.txt`
   still uses `>=`.
2. Queue Copilot PR A using the prompt above.
3. Review Copilot's commits: 14 files moved, `agent/` deleted, imports
   rewritten in `cli.py` + `ocr_990_pdfs.py`, `_paths.py` created,
   `CLAUDE.md` updated.
4. Merge PR A.
5. Queue Copilot PR B.
6. Merge PR B.
7. Update `terminal-lab/AGENT_SPEC.md` §9 + §10 to flip research-agent 🟢.

Done.

---

*Last updated: May 5, 2026 — end of Thread 7*
