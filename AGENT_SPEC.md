# AGENT_SPEC.md — AI Agent Repo Contract

Canonical shared contract for all three AI agent repos: `research-agent`, `audio-agent`, `newsletter-agent`.  
Every repo must conform to every rule in this document before being considered production-ready.

---

## 1. Package Layout

The Python package directory **must** be named after the agent.

| Agent | Required package dir |
|---|---|
| research-agent | `research_agent/` |
| audio-agent | `audio_agent/` |
| newsletter-agent | `newsletter_agent/` |

**Do not** use the generic name `agent/` — it collides when two agents are installed in the same environment.

Minimum required contents inside the package directory:

```
<agent_name>/
├── __init__.py
└── _paths.py       # centralized path constants
```

---

## 2. Entrypoint Convention

- CLI entrypoint: `cli.py` at the **repo root** — not `run.py`, `main.py`, or anything else.
- `cli.py` must use `argparse` or `click` with named subcommands.
- A `Makefile` at the repo root must expose all standard targets (see §3).

```
<repo-root>/
├── cli.py          # ← entrypoint, always this name
└── Makefile        # ← required targets below
```

**Makefile required targets:**

| Target | Purpose |
|---|---|
| `install` | Install dependencies (e.g. `pip install -r requirements.txt`) |
| `run` | Run the agent with sensible defaults |
| `test` | Run the test suite |
| `lint` | Run linter (e.g. `ruff`, `flake8`) |
| `clean` | Remove generated files, `__pycache__`, `.lance`, etc. |

---

## 3. Required Top-Level Files

Every agent repo **must** have all of the following at the repo root or specified path:

| File | Purpose |
|---|---|
| `README.md` | Purpose, setup instructions, usage examples, architecture overview |
| `CLAUDE.md` | Claude Code context file: architecture, module map, dev commands, data flow, gotchas |
| `Makefile` | Targets: `install`, `run`, `test`, `lint`, `clean` |
| `.env.example` | All required env vars with placeholder values and inline comments |
| `requirements.txt` | Pinned dependencies (`pip freeze` or manually pinned) |
| `docs/workflow.md` | End-to-end pipeline walkthrough |

Missing any of these = non-compliant.

---

## 4. RAG Backend Standard

All agents use **LanceDB** as the vector store.

**Not FAISS.** Rationale: LanceDB is on-device, supports Apple Silicon (MLX), has native Python, and has a simpler API than FAISS.

### Module layout

| Module | Role |
|---|---|
| `<agent_name>/index.py` | Write embeddings to LanceDB |
| `<agent_name>/search.py` | Query LanceDB |

### Embedding model

- Library: `sentence-transformers`
- Default model: `all-MiniLM-L6-v2`

### LanceDB setup (minimal)

```python
import lancedb
from sentence_transformers import SentenceTransformer

DB_PATH = "_lancedb"
MODEL = "all-MiniLM-L6-v2"

def get_db():
    return lancedb.connect(DB_PATH)

def embed(texts: list[str]) -> list[list[float]]:
    model = SentenceTransformer(MODEL)
    return model.encode(texts).tolist()
```

---

## 5. Claude Skills Path

All Claude skill files live under `.claude/skills/<skill-name>/`.

```
.claude/
└── skills/
    └── <skill-name>/
        ├── SKILL.md           # required — main skill document
        └── references/        # optional — supplemental reference docs
            └── *.md
```

- `SKILL.md` is required in every skill directory.
- The `references/` subdirectory is optional but must follow that name if used.

---

## 6. Module Naming Conventions

Use these standard names across all agents. Apply only the modules relevant to each agent.

| Module | Role |
|---|---|
| `fetch.py` | Data ingestion / download |
| `scrape.py` | Web scraping |
| `pdf.py` | PDF processing |
| `index.py` | Write to vector store |
| `search.py` | Query vector store |
| `archive.py` | SQLite or file-based archival |
| `export.py` | Output formatting (MD, HTML, JSON) |
| `cli.py` | Entrypoint — repo root, not inside package |
| `_paths.py` | Centralized path constants — inside package |

Non-standard names (e.g. `ingest.py`, `store.py`, `run.py`) are not allowed for these roles.

---

## 7. Environment Variables

Standard env var names. Use these names exactly — no variations.

| Variable | Purpose | Default |
|---|---|---|
| `PERPLEXITY_API_KEY` | Perplexity search API | — |
| `ANTHROPIC_API_KEY` | Claude API | — |
| `OLLAMA_HOST` | Local Ollama base URL | `http://localhost:11434` |
| `DATA_DIR` | Root data directory | `./data` |
| `DB_PATH` | SQLite database path | — |
| `LANCE_DB_PATH` | LanceDB database path | — |

`.env.example` template:

```dotenv
# Perplexity search API
PERPLEXITY_API_KEY=your-key-here

# Anthropic / Claude API
ANTHROPIC_API_KEY=your-key-here

# Local Ollama base URL
OLLAMA_HOST=http://localhost:11434

# Data directories
DATA_DIR=./data
DB_PATH=./data/archive/store.db
LANCE_DB_PATH=./data/lancedb
```

---

## 8. Data Directory Layout

```
data/
├── raw/            # original downloads, unmodified
├── processed/      # cleaned, chunked, ready for indexing
├── archive/        # sqlite .db files
└── exports/        # final outputs (MD, HTML, JSON)
```

- `data/raw/` — never mutate files here after download.
- `data/processed/` — output of cleaning/chunking pipelines.
- `data/archive/` — all `.db` files; path set by `DB_PATH`.
- `data/exports/` — deliverables consumed outside the pipeline.

---

## 9. Current Agent Status

| Agent | Repo | Package Dir | cli.py | CLAUDE.md | docs/ | RAG Backend | Status |
|---|---|---|---|---|---|---|---|
| research-agent | redbeard-alt/research-agent | `agent/` ❌ rename to `research_agent/` | `run.py` ❌ rename to `cli.py` | ❌ missing | ✅ `docs/workflow.md` | FAISS ❌ migrate to LanceDB | 🔴 needs work |
| audio-agent | redbeard-alt/audio-agent | ❌ no package dir | ❌ missing | ✅ exists | ❌ missing | none ✅ adopt LanceDB | 🔴 scaffold needed |
| newsletter-agent | redbeard-alt/newsletter-agent | `newsletter_agent/` ✅ | `cli.py` ✅ | ❌ missing | ❌ missing | none ✅ N/A | 🟡 minor gaps |

---

## 10. Migration Checklist

### research-agent

- [ ] Rename `agent/` → `research_agent/`
- [ ] Update all imports from `agent.` → `research_agent.`
- [ ] Rename `run.py` → `cli.py`; add `argparse`/`click` subcommands
- [ ] Add `CLAUDE.md`
- [ ] Replace FAISS with LanceDB in `research_agent/index.py` and `research_agent/search.py`
- [ ] Add `LANCE_DB_PATH` to `.env.example`
- [ ] Add `requirements.txt` with pinned deps including `lancedb`, `sentence-transformers`
- [ ] Verify `Makefile` has all five required targets
- [ ] Verify `docs/workflow.md` exists and is current

### audio-agent

- [ ] Create `audio_agent/` package with `__init__.py` and `_paths.py`
- [ ] Create `cli.py` at repo root with subcommands
- [ ] Add `CLAUDE.md`
- [ ] Add `docs/workflow.md`
- [ ] Scaffold `audio_agent/index.py` and `audio_agent/search.py` with LanceDB
- [ ] Add `.env.example` with all standard vars
- [ ] Add `requirements.txt` with pinned deps
- [ ] Add `Makefile` with all five required targets
- [ ] Add `README.md` covering purpose, setup, usage, architecture

### newsletter-agent

- [ ] Add `CLAUDE.md`
- [ ] Add `docs/workflow.md`
- [ ] Verify `Makefile` has all five required targets
- [ ] Verify `.env.example` covers all standard vars
- [ ] Verify `requirements.txt` is pinned

---

*Last updated: May 2026*
