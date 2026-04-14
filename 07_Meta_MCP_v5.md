# TERMINAL LAB — MCP SERVER STACK v1
## Claude Code Tool Extension on M4 / macOS Tahoe
**Hardware:** M4 MacBook Pro, 48 GB RAM | **Shell:** zsh | **Last updated:** April 2026

---

## Part 1 — What MCP Adds to Terminal Lab

MCP (Model Context Protocol) turns Claude Code from a file-editing chat agent into a **tool-using agent**. Instead of you manually piping `cat file | ollama run`, Claude calls structured tools inside a Plan Mode session.

Core capabilities unlocked:
- **Fetch** — pull live docs, APIs, changelogs into context without copy-paste
- **Filesystem** — structured read/list/search over constrained root paths
- **Context7** — real-time, version-specific library docs injected at prompt time (prevents hallucinated APIs)
- **Local LLM** — expose vLLM-MLX or Ollama as a callable tool (advanced, see Part 6)

Claude Code already has native git, bash, and file-editing tools. MCP adds **reach**, not duplication.

### Skip the Official Git MCP Server

`mcp-server-git` (Anthropic's reference impl) carries three unpatched-class CVEs:
- CVE-2025-68143 — unrestricted `git_init`, arbitrary path traversal
- CVE-2025-68144 — argument injection in `git_diff` / `git_checkout`
- CVE-2025-68145 — path validation bypass on `--repository` flag

The "toxic combination" is `mcp-server-git` + `mcp-server-filesystem` together: chained, they enable RCE via prompt injection from a malicious README or poisoned commit message. Claude Code's built-in git tools (read-only diffs, status) are safer for daily use. Only add an external git MCP server if you have a concrete need and are pinned to `≥ 2025.12.18`.

Route for git work: use Claude Code's native git tools + your `02_Core_Advanced_v5.md` git section.

---

## Part 2 — Scope Model

Three scopes, one precedence rule: **local > project > user**

| Scope | Flag | Config file | Use for |
|---|---|---|---|
| `local` | (default) | `~/.claude.json` under project path | Experiments, per-session only, not persisted |
| `user` | `--scope user` | `~/.claude.json` globally | Personal tools available in all projects |
| `project` | `--scope project` | `.mcp.json` at repo root (checked into git) | Team-shared servers, project-specific DBs |

**Terminal Lab default:** use `--scope user` for personal utility servers (fetch, context7, filesystem). Use `--scope project` only when the whole team needs a server and it's safe to commit `.mcp.json`.

Never commit API keys to `.mcp.json`. Use `${VAR}` syntax for secrets — they resolve from environment at runtime.

---

## Part 3 — Baseline Stack

Recommended for this machine:

| Server | Package | Transport | Risk | Purpose |
|---|---|---|---|---|
| `server-fetch` | `mcp-server-fetch` (uvx) | stdio | 🟢 read-only | HTTP GET docs, APIs, changelogs |
| `server-filesystem` | `@modelcontextprotocol/server-filesystem` (npx) | stdio | 🟡 read (constrained root) | List, read, search under allowed dirs only |
| `context7` | `@upstash/context7-mcp` (npx) | stdio or HTTP | 🟢 read-only | Live library docs injected at prompt time |

These cover 90% of useful MCP workflows without the git CVE surface. Add more only when you have a concrete workflow need.

---

## Part 4 — Installation

### 4.0 Prerequisites

🟢 read-only — verify before installing

```bash
node --version        # Need ≥ 18; brew install node if missing
npx --version
uvx --version         # brew install uv if missing
claude --version
claude mcp list       # See current servers
```

### 4.1 server-fetch

Fetches URL content (docs, APIs, changelogs) into Claude's context.

🟡 modifies state — writes to `~/.claude.json`

```bash
claude mcp add-json server-fetch --scope user '{
  "command": "uvx",
  "args": ["mcp-server-fetch"]
}'
```

Verify:

```bash
claude mcp get server-fetch
```

### 4.2 server-filesystem

Structured file access constrained to allowed root paths. Set `FS_ROOT` to the directories Claude is allowed to read. Do **not** include `~`, `/`, or your SSH key directory.

🟡 modifies state — writes to `~/.claude.json`

```bash
claude mcp add-json server-filesystem --scope user '{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/Users/YOURNAME/Research",
    "/Users/YOURNAME/Projects"
  ]
}'
```

**RED TEAM note:** Never include `/Users/YOURNAME` (your whole home dir) as an allowed path. List only the specific subdirectories you want Claude to see. Adding `~/.ssh`, `~/.zshenv`, or `~/.claude.json` to the allowed list would be a critical error.

Verify:

```bash
claude mcp get server-filesystem
```

### 4.3 Context7 — Live Library Docs

Context7 injects real-time, version-specific documentation into prompts. Prevents Claude from hallucinating deprecated APIs. Free tier works without an API key; get one at `context7.com/dashboard` for higher rate limits.

**Option A — stdio (local, no API key required):**

🟡 modifies state — writes to `~/.claude.json`

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

**Option B — stdio with API key (higher rate limits):**

🟡 modifies state — writes to `~/.claude.json`

```bash
# Store key in .zshenv first: export CONTEXT7_API_KEY="your-key-here"
# Then register using env var — never paste key directly into shell history
claude mcp add --scope user context7 -- \
  npx -y @upstash/context7-mcp --api-key "${CONTEXT7_API_KEY}"
```

**Option C — HTTP remote (no local process, key in header):**

🟡 modifies state — writes to `~/.claude.json`

```bash
claude mcp add \
  --scope user \
  --transport http \
  --header "CONTEXT7_API_KEY: ${CONTEXT7_API_KEY}" \
  context7 \
  https://mcp.context7.com/mcp
```

Verify connection:

```bash
claude mcp get context7
```

**Auto-invocation (optional):** Add to your `CLAUDE.md` so Claude uses Context7 without being asked:

```
Always use Context7 MCP when I need library/API documentation, code generation, or setup steps without me having to explicitly ask.
```

---

## Part 5 — Verify the Full Stack

After all installs:

🟢 read-only

```bash
claude mcp list
# Should show: server-fetch, server-filesystem, context7

claude --mcp-debug
# Inside session, run: /mcp
# Each server should show "connected", not "failed"
```

Test each server with natural language inside a session:

```bash
claude
# then in session:
# "Fetch the latest changelog from https://docs.example.com"
# "List all .md files under ~/Research/Notes"
# "Use context7 to show me the current LangChain RAG API"
```

---

## Part 6 — Advanced: Local LLM as MCP Tool

Expose vLLM-MLX or Ollama as a callable tool inside Claude Code sessions. Useful for: running eval comparisons, calling a local model for sub-tasks without leaving the session, routing cheaper tasks to local models.

Prerequisite: vLLM-MLX or Ollama already running as a server (see `06_Tool_AI_Terminal_v5.md` Parts 1, 8).

### 6.1 Minimal local-llm MCP server (Python)

🟡 modifies state — creates a new file

```bash
mkdir -p ~/.local/mcp-servers
cat > ~/.local/mcp-servers/local-llm-mcp.py << 'PYEOF'
#!/usr/bin/env python3
"""
local-llm-mcp: Expose Ollama or vLLM-MLX as an MCP tool.
Tool: local_llm_generate(prompt, model) -> string
Reads OLLAMA_HOST from env (default: http://localhost:11434)
"""
import sys, json, os, urllib.request, urllib.error

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("LOCAL_LLM_MODEL", "llama3.1:8b")

def generate(prompt: str, model: str = DEFAULT_MODEL) -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except urllib.error.URLError as e:
        return f"ERROR: Ollama not reachable at {OLLAMA_HOST}: {e}"

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        if req.get("method") == "mcp.toolCall" and req["params"]["name"] == "local_llm_generate":
            args = req["params"]["arguments"]
            result = generate(args.get("prompt", ""), args.get("model", DEFAULT_MODEL))
            resp = {"jsonrpc": "2.0", "id": req["id"], "result": {"content": result}}
            print(json.dumps(resp), flush=True)

if __name__ == "__main__":
    main()
PYEOF
chmod +x ~/.local/mcp-servers/local-llm-mcp.py
```

### 6.2 Register

🟡 modifies state — writes to `~/.claude.json`

```bash
claude mcp add-json local-llm --scope user '{
  "command": "python3",
  "args": ["'"$HOME"'/.local/mcp-servers/local-llm-mcp.py"],
  "env": {
    "OLLAMA_HOST": "http://localhost:11434",
    "LOCAL_LLM_MODEL": "llama3.1:8b"
  },
  "timeout_ms": 120000
}'
```

**Safety note:** Only enable when Ollama is running. This server makes outbound connections to localhost only — no cloud leakage. Data stays on-device.

---

## Part 7 — Tool Search (Mandatory with 3+ Servers)

Without Tool Search, each server loads all its tool definitions upfront. At 3+ servers you can hit 50k–100k tokens of overhead before doing any work. Tool Search defers definitions and loads only what's needed per task.

- **85% context reduction**: ~72,000 tokens → ~8,700 tokens
- **Better accuracy**: Opus 4 tool selection improves from 49% → 74%
- **Requires**: Sonnet 4 or Opus 4 (Haiku doesn't support it)

🟡 modifies state — set in `.zshrc` or `~/.claude.json` env

```bash
# Add to .zshrc (block 7 — AI Terminal Tools)
export ENABLE_TOOL_SEARCH=auto    # activates when MCP tools exceed 10% of context window

# Or run one-off
ENABLE_TOOL_SEARCH=auto claude
```

To set permanently in `~/.claude.json` env field (avoids needing the env var on every launch):

```json
{
  "env": {
    "ENABLE_TOOL_SEARCH": "auto"
  }
}
```

---

## Part 8 — Safety and Hook Defaults

MCP amplifies Claude Code's reach. Apply existing Terminal Lab safety defaults plus MCP-specific additions.

### 8.1 Required session defaults

- **Always use Plan Mode** (`Shift+Tab`) before any session involving filesystem or local-llm MCP servers — same rule as file edits.
- **Always run `git diff` + `git status`** after any session where Claude could have called filesystem write tools.
- **Budget long MCP sessions**: `claude --max-budget-usd 5.00`
- **Sandbox for untrusted inputs**: `claude --sandbox` when processing external content (scraped docs, unknown repos) with MCP active.

### 8.2 Filesystem server hardening checklist

Before adding filesystem server to a scope, verify:

- [ ] Allowed paths are explicit subdirectories, not `~` or `/`
- [ ] No credential directories (`~/.ssh`, `~/.gnupg`, `~/.zshenv`) in allowed list
- [ ] Combined git+filesystem is not active at the same time (CVE chain risk)
- [ ] Plan Mode enforced before session

### 8.3 MCP server trust rules

- **Only add servers you can review or trust the maintainer of.** MCP servers run as local processes with access to your session context.
- **Treat API keys for MCP servers like any other credential**: store in `.zshenv`, inject via `${VAR}` syntax, never paste inline into shell history.
- **Prompt injection surface**: any content Claude reads (READMEs, issue descriptions, fetched URLs) can carry injected instructions. This is especially dangerous with filesystem + git active together.

---

## Part 9 — Troubleshooting

| Problem | Fix |
|---|---|
| `claude mcp list` shows server but `/mcp` shows "failed" | Restart Claude Code — config changes don't take effect until restart |
| `command not found` for `npx` or `uvx` | Claude spawns subprocesses with a different shell env; use absolute paths: `which npx` |
| `nvm` node not found | Add nvm init to `~/.zshrc` (not just `~/.zprofile`) so non-interactive shells find it |
| Server hangs on connect | Switch SSE → HTTP transport; SSE is deprecated |
| JSON config parse error | No trailing commas in JSON; validate with `jq . ~/.claude.json` |
| macOS permission dialog blocks startup | Grant permission, retry — first run only |
| `server-fetch` returns 403 on some URLs | Some APIs block the default User-Agent; normal |
| Context7 rate limited | Get a free API key at context7.com/dashboard |

Quick diagnostic sequence:

🟢 read-only

```bash
claude mcp list                          # Registered servers
claude --mcp-debug                       # Launch with debug output
# Inside session: /mcp                  # Live connection status
jq . ~/.claude.json | head -80           # Validate config JSON
```

---

## Part 10 — 05_Store Entries

For each server you rely on in production, add a `05_Store_Database_v5.md` entry under `ai-terminal`:

```
### Claude MCP — baseline stack (server-fetch + server-filesystem + context7)
- Risk: 🟡 modifies state (filesystem read under constrained root)
- Scope: user (~/.claude.json)
- Roots: ~/Research, ~/Projects
- ENABLE_TOOL_SEARCH: auto
- Tested: [DATE] | Claude Code [VERSION] | Node [VERSION] | uv [VERSION]
- Notes: git MCP server intentionally excluded (CVE-2025-68143/44/45)
```

---

## Part 11 — Routing Reference

| Query | Go to |
|---|---|
| MCP concepts, install, configure, troubleshoot | This file `07_Meta_MCP_v5.md` |
| Claude Code Plan Mode, hooks, sandbox, budget | `06_Tool_AI_Terminal_v5.md` Part 3 |
| Building custom Python/bash scripts | `02_Core_Advanced_v5.md` scripting sections |
| Battle-tested MCP stack commands | `05_Store_Database_v5.md` → `ai-terminal` category |
| vLLM-MLX / Ollama server setup (prerequisite for Part 6) | `06_Tool_AI_Terminal_v5.md` Parts 1, 8 |
| RAG pipeline using Ollama embeddings | `06_Tool_AI_Terminal_v5.md` Part 13 (when added) |

Update `00_Index_Router_v5.md` and `README.md` to reference `07_Meta_MCP_v5.md` as the MCP / Claude tool stack doc.

---

*Last updated: April 2026 | v1*
