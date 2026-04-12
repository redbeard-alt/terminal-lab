# 06_AI_TERMINAL_INTEGRATION
# TERMINAL LAB — AI TERMINAL INTEGRATION v3.1
> Local and cloud AI tools for the M4 Mac terminal. Ollama · MLX · MLX Whisper · Claude Code · zsh-ai-assist.
> Hardware: M4 MacBook Pro, 48 GB RAM · OS: macOS Tahoe (latest) · Shell: zsh
> Last updated: April 2026
> Baseline environment: see README.md → Environment & Version Policy

---

## Overview

| System | What It Is | When to Use |
|---|---|---|
| Ollama | Local LLM server | Offline, private data, file analysis, daily piping |
| MLX | Apple Silicon-native inference | Fastest local inference on M4, Python-integrated workflows |
| MLX Whisper | Local speech-to-text (ASR) | Transcribe meeting/audio files locally on M4 |
| Claude Code | Anthropic terminal agent v2.x | Multi-file tasks, code, synthesis, long-context research |
| zsh-ai-assist | AI-powered zsh plugin | Generate commands, fix errors, inline terminal help |

**Key principle:** Local AI (Ollama/MLX) = private, offline, free after setup. Cloud AI (Claude Code, zsh-ai-assist) = more capable, requires subscription/API, non-sensitive data only.

**Routing:** When you need better prompts or AI workflows (Jeff Su-style TASK/CONTEXT/EXEMPLARS, XML tags, outcome-based prompting), switch to Prompt Lab and build the prompt there; then run the resulting commands or scripts here.

---

## PART 1: OLLAMA — LOCAL MODEL RUNNER

### Installation

```bash
brew install ollama
ollama --version
ollama serve    # Start server (auto-starts on macOS)
```

### Pull Models by RAM Tier

```bash
# 16 GB M4 — baseline
ollama pull llama3.1:8b
ollama pull deepseek-r1:8b

# 24 GB M4 — add
ollama pull qwen2.5:14b
ollama pull mistral-nemo:12b

# 32–48 GB M4 Max/Pro — add
ollama pull llama3.1:70b
ollama pull qwen2.5:32b
```

### Model Management

```bash
ollama list                     # Downloaded models + sizes
ollama ps                       # Running models + RAM usage
ollama show llama3.1:8b         # Details, context size, parameters
ollama stop llama3.1:8b         # Stop model, free RAM
ollama rm llama3.1:8b           # Delete from disk
ollama pull llama3.1:8b         # Update to latest
ollama cp llama3.1:8b my-llama  # Copy/alias locally
```

### File Pipe Patterns

```bash
cat research_notes.md | ollama run llama3.1:8b "Summarize in 5 bullet points"
cat meeting_transcript.txt | ollama run llama3.1:8b "Extract all action items as numbered list"
cat data.csv | ollama run qwen2.5:14b "Identify 3 most significant patterns"
cat file1.md file2.md | ollama run qwen2.5:14b "What are the biggest contradictions?"
tail -100 app.log | ollama run llama3.1:8b "Identify error patterns and suggest root causes"

# Save to file
cat notes.md | ollama run llama3.1:8b "Write an executive summary" > summary.md
```

### Thinking Mode (Reasoning Models)

```bash
ollama run deepseek-r1:8b "Analyze tradeoffs of microservices vs monolith for a 5-person team"
```

Use for complex analysis, multi-step logic, debugging, and math.

### Custom Models with Modelfile

```bash
cat > Modelfile-research << 'EOF'
FROM llama3.1:8b
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
SYSTEM You are a research assistant. Be precise, cite claims, flag uncertainty. Output in Markdown. Never fabricate sources.
EOF

ollama create research-assistant -f Modelfile-research
ollama run research-assistant "Summarize the key claims" < paper.md
```

### Configuration

```bash
# Move model storage to external drive
export OLLAMA_MODELS=/Volumes/ExternalSSD/ollama/models

# LAN Mode — share models across local network
export OLLAMA_HOST=0.0.0.0:11434
```

Add persistent exports to `~/.zshenv`, not `~/.zshrc`.

### Model Selection by Task

| Task | Best Model | Reason |
|---|---|---|
| Quick summaries, Q&A | llama3.1:8b | Speed |
| Long docs (10k+ tokens) | qwen2.5:14b | Context window |
| Reasoning and analysis | deepseek-r1:8b | Chain-of-thought depth |
| Code review | qwen2.5:14b | Code-trained |
| Minimal RAM | llama3.2:3b | 2 GB only |
| Structured JSON output | qwen2.5:14b | Best schema adherence |

### RAM Usage Reference

| Model | 4-bit RAM | M4 Tier |
|---|---|---|
| 3B | ~2 GB | All |
| 7–8B | ~5–6 GB | 16 GB+ |
| 14B | ~9–10 GB | 24 GB+ |
| 32B | ~20–22 GB | 32 GB+ |
| 70B | ~40–44 GB | 48 GB (this machine) |

---

## PART 2: MLX — APPLE SILICON NATIVE INFERENCE

### Installation

```bash
mkdir -p ~/.venvs
/opt/homebrew/bin/python3.12 -m venv ~/.venvs/mlx
source ~/.venvs/mlx/bin/activate
pip install --upgrade pip
pip install mlx-lm
python3 -c "import mlx.core as mx; print(mx.default_device())"  # Expected: Device(gpu, 0)
deactivate
```

**Notes:**
- Pins Python 3.12 — mlx-lm wheels may lag behind Homebrew’s latest Python.
- If `python3.12` is missing: `brew install python@3.12`

### Usage

```bash
mlx_lm.generate \
  --model mlx-community/Llama-3.1-8B-Instruct-4bit \
  --prompt "Summarize key AI trends for researchers in 2026" \
  --max-tokens 512

alias mlx8b='mlx_lm.generate --model mlx-community/Llama-3.1-8B-Instruct-4bit --max-tokens 512 --prompt'
mlx8b "What is the difference between MLX and Ollama?"
```

### MLX Server Mode (OpenAI-Compatible)

```bash
mlx_lm.server --model mlx-community/Llama-3.1-8B-Instruct-4bit --port 8080

curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"Hello"}]}' | jq .
```

### Fine-Tuning on Apple Silicon (LoRA)

```bash
pip3 install --user 'mlx-lm[training]'

mlx_lm.lora \
  --model mlx-community/Llama-3.1-8B-Instruct-4bit \
  --train \
  --data ./training_data \
  --iters 100

mlx_lm.fuse \
  --model mlx-community/Llama-3.1-8B-Instruct-4bit \
  --adapter-path ./adapters \
  --save-path ./my-finetuned-model
```

### Recommended 4-bit Models for M4 (48 GB)

```bash
mlx-community/Llama-3.1-8B-Instruct-4bit
mlx-community/Qwen2.5-14B-Instruct-4bit
mlx-community/DeepSeek-R1-Distill-8B-4bit
mlx-community/Mistral-7B-Instruct-v0.3-4bit
```

### MLX vs Ollama

| Dimension | Ollama | MLX |
|---|---|---|
| Interface | CLI + REST API | CLI + Python library |
| Speed on M4 | Fast (Metal GPU) | Fastest (native Metal) |
| Server mode | Built-in port 11434 | `mlx_lm.server` |
| Fine-tuning | Not supported | LoRA/full fine-tuning |
| Model format | GGUF | MLX safetensors |
| Best for | Daily CLI piping, background server | Python workflows, max speed |

---

## PART 2b: MLX WHISPER — LOCAL SPEECH-TO-TEXT

### Setup (venv-safe)

```bash
mkdir -p ~/.venvs
python3 --version
python3 -m venv ~/.venvs/whisper

source ~/.venvs/whisper/bin/activate
pip install --upgrade pip
pip install mlx-whisper
deactivate

brew install ffmpeg
```

**Notes:**
- Follows README version policy: latest stable Homebrew/PyPI, with known-good combos documented in workflows.
- First run downloads the model from Hugging Face (~3 GB, network required).
- Model weights are local after download; transcripts never leave your machine.

### One-File Transcription

```bash
source ~/.venvs/whisper/bin/activate

mlx_whisper cleaned/meeting_cleaned.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language en

deactivate
```

**Notes:**
- Use `mlx-community/whisper-large-v3-mlx`.
- CLI writes `.txt` next to input WAV by default.
- Always call the `mlx_whisper` CLI directly; do **not** use `python -m mlx_whisper`.

### Verify Output

```bash
ls cleaned/*_cleaned.txt
wc -w cleaned/meeting_cleaned.txt
head -30 cleaned/meeting_cleaned.txt
```

### Audio Cleanup with ffmpeg

```bash
ffmpeg -i "meeting.mp4" \
  -vn -ac 1 -ar 16000 \
  -af "afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=80" \
  "cleaned/meeting_cleaned.wav"

# Dry-run
ffmpeg -i "meeting.mp4" \
  -vn -ac 1 -ar 16000 \
  -af "afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=80" \
  -f null -
```

If speech sounds underwater or drops out:

```bash
ffmpeg -i "meeting.mp4" \
  -vn -ac 1 -ar 16000 \
  -af "afftdn=nf=-35,loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=80" \
  "cleaned/meeting_cleaned.wav"
```

**Operational notes:**
- Multi-hour ffmpeg cleanup is CPU-heavy.
- Cleaned WAV files are large; long archives can consume tens of GB.
- Run on AC power; one meeting at a time by default.

### Anti-Hallucination Flags — Problem Files Only

**Symptom:** repeated short phrases despite clear speech.

```bash
source ~/.venvs/whisper/bin/activate

mlx_whisper cleaned/meeting_cleaned.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language en \
  --temperature 0 \
  --no_speech_threshold 0.3 \
  --compression_ratio_threshold 1.8 \
  --condition_on_previous_text False \
  --initial_prompt "Regular board or council meeting. Agenda items, budgets, policy and public comments."

deactivate
```

**Rules:**
- This is **hallucination mode**, not default mode.
- Do **not** bake these flags into default or batch scripts.
- Only enable them after confirming the failure mode on a specific file.

### Full Batch Pipeline

See `05_Store_Database.md` → Workflow **Local Board/Meeting Videos → Whisper Transcripts (MLX, macOS)**.

### Troubleshooting (Quick)

| Symptom | Fix |
|---|---|
| HF 401 / repo not found | Use `whisper-large-v3-mlx`; `huggingface-cli login` if gated |
| `.txt` exists but empty | Used `python -m`; switch to `mlx_whisper` CLI |
| Repeated phrase spam | Use hallucination flags and/or segment audio |
| Speech sounds underwater | Lower `afftdn` or remove denoise |
| Laptop very hot | AC power; one meeting at a time |

---

## PART 3: CLAUDE CODE — TERMINAL AI AGENT v2.x

### Installation

```bash
brew install node
npm install -g @anthropic-ai/claude-code
claude --version
claude --doctor
```

### Core Commands

```bash
claude
claude --continue
claude --resume
claude --doctor
```

### Inside a Session

| Command | What It Does |
|---|---|
| `/help` | All available commands |
| `/status` | Model, context usage, cost so far |
| `/context` | Context diagnostics |
| `/compact` | Summarize context to free tokens |
| `/rewind` | Undo code changes + roll back conversation |
| `/cost` | Token usage and estimated cost |
| `/model` | Switch model mid-session |
| `/permissions` | Manage tool permissions |
| `/mcp` | MCP server status |
| `/todos` | Current todo items |
| `/quit` | Exit |

### Mode Switching (Shift+Tab)

Shift+Tab cycles:
- **AUTO MODE**
- **PLAN MODE** ← required before file operations
- **DELEGATE**

### Rewind

```bash
# Double-tap Escape or /rewind
```

### Hooks System

Hooks are deterministic middleware. Treat the examples below as patterns, not drop-in production policy.

| Event | When It Fires | Can Block? |
|---|---|---|
| PreToolUse | Before Claude runs a tool | Yes |
| PostToolUse | After tool succeeds | No |
| SessionStart | New/resumed/cleared session | No |
| SessionEnd | Exit/sigint/error | No |
| PreCompact | Before context compaction | No |

**Minimal safer pattern:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".scripts/security-check.sh"
          }
        ]
      }
    ]
  }
}
```

**Guidance:**
- Keep hook commands small, deterministic, and fully quoted.
- Avoid complex inline `bash -c` JSON parsing inside hooks unless you test them separately.
- `security-check.sh` should explicitly block destructive patterns (`rm -rf`, `dd`, wide `find -delete`, unsafe `sed -i`, unbounded write/delete loops).

### Agent Teams

```bash
claude "Review this large PR. Create one teammate for security, one for code quality, one for test coverage. Coordinate before reporting back."
```

### Skills Auto-Loading

```bash
cat > .claude/skills/research-review.md << 'EOF'
---
name: research-review
description: Use when reviewing research notes, analyzing claims, or cross-referencing sources in Research.
---
1. Check all factual claims against sources
2. Flag unsupported assertions
3. Note contradictions
4. Output structured findings in Markdown
EOF
```

### 1M Context Window

Use for large codebases or research corpora. Watch `/context`; compact before hitting the ceiling.

### Sandbox Mode

```bash
claude --sandbox
```

### Research Workflows

```bash
claude "Read all .md files in ~/Research. Cross-reference claims. Draft synthesis memo. Save to ~/Research/synthesis.md"
claude "Read ~/Research/Notes/raw_notes.md. Organize into Background, Key Findings, Open Questions, Next Steps. Save structured version."

git -C ~/Research diff
git -C ~/Research status
```

---

## PART 4: ZSH-AI-ASSIST — AI AT THE PROMPT

### Installation

```bash
brew install curl jq
git clone https://github.com/MKSG-MugunthKumar/zsh-ai-assist ~/.zsh-ai-assist
echo 'source ~/.zsh-ai-assist/zsh-ai-assist.plugin.zsh' >> ~/.zshrc
source ~/.zshrc
```

### Usage

```bash
ai "find all PDF files in ~/Research modified in the last 7 days"
ai "compress all .log files in ~/logs older than 30 days"
ai "search all markdown files for lines containing TODO"
??
```

### Tool Selection Guide

| Situation | Tool | Risk |
|---|---|---|
| Quick command you can't remember | `ai "description"` | Review before running |
| Command just failed | `??` | Review before running |
| Complex multi-file task | `claude` | Plan Mode first |
| Private/sensitive data | `ollama` / `mlx` | Local only |
| Fastest M4 inference | `mlx_lm.generate` | Local only |
| Structured JSON extraction | Ollama API + `jq` | Local only |

### Security rule

Never pipe credentials, SSH keys, tokens, or `.zshenv` contents to **any** model or AI assistant. Store API keys in `~/.zshenv` with strict permissions (`chmod 600 ~/.zshenv`).

### Troubleshooting

| Problem | Fix |
|---|---|
| `ai` not found | `source ~/.zshrc` or re-clone plugin |
| `??` not working | Source plugin after other plugins |
| Wrong API key | Check env vars in `~/.zshenv` |
| Slow response | API latency or provider issue |

---

## PART 5: RECOMMENDED .zshrc ALIASES

```bash
alias ai8b="ollama run llama3.1:8b"
alias ai14b="ollama run qwen2.5:14b"
alias ai-think="ollama run deepseek-r1:8b"
alias ai-fast="ollama run llama3.2:3b"
alias ai-models="ollama list"
alias ai-status="ollama ps"
alias ai-stop-all="ollama ps | tail -n +2 | awk '{print \$1}' | xargs -I {} ollama stop {}"

alias mlx-whisper-test='source ~/.venvs/whisper/bin/activate && mlx_whisper'

alias cc="claude"
alias cc-resume="claude --resume"
alias cc-check="claude --doctor"
alias cc-continue="claude --continue"
```

### MLX Shim Scripts (use instead of aliases — no venv activation leak)

```bash
mkdir -p ~/.local/bin

cat > ~/.local/bin/mlx8b << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
~/.venvs/mlx/bin/python3 -m mlx_lm.generate \\
  --model mlx-community/Llama-3.1-8B-Instruct-4bit \\
  --max-tokens 512 --prompt "$@"
EOF
chmod +x ~/.local/bin/mlx8b
```

Ensure `~/.local/bin` is on PATH (add to `.zshrc` if missing):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Ollama aliases (`ai8b`, `ai14b`, `ai-think`, etc.) are unchanged — they don't need venvs.
Claude aliases (`cc`, `cc-resume`, etc.) are unchanged.

---

## PART 6: RESOURCE MONITORING BEFORE LOADING MODELS

```bash
mactop
btop
ollama ps
ai-stop-all
vm_stat | head -5
sysctl -n hw.memsize | awk '{printf "%.0f GB total RAM\n", $1/1024/1024/1024}'
```

RAM guide:
- 3B → ~2 GB free
- 8B → ~5–6 GB free
- 14B → ~10 GB free
- 32B → ~22 GB free
- 70B → ~40 GB free

---

## PART 7: AI TERMINAL SAFETY RULES

### Data Privacy Tiers

| Tool | Data Location | Safe for Private Data? |
|---|---|---|
| Ollama | Local machine only | Yes |
| MLX | Local machine only | Yes |
| MLX Whisper | Local machine only after model download | Yes |
| Claude Code | Sent to Anthropic | Non-sensitive only |
| zsh-ai-assist | Sent to provider | Non-sensitive only |

### Rules

```bash
# 1. NEVER pipe credentials or SSH keys to ANY model
cat ~/.ssh/id_rsa | ollama run ...   # NEVER
cat ~/.zshenv | claude ...           # NEVER

# 2. Claude Code: ALWAYS use Plan Mode before file modifications

# 3. After EVERY Claude Code file session:
git -C ~/Research diff
git -C ~/Research status

# 4. Implement PreToolUse security hook

# 5. Verify teammate count before approving Agent Teams work

# 6. Budget long Claude sessions
claude --max-budget-usd 5.00

# 7. Use /rewind if something goes wrong

# 8. Use sandbox mode for untrusted operations
claude --sandbox

# 9. MLX Whisper downloads model weights from Hugging Face on first run
```

---

## PART 8: TROUBLESHOOTING

### Ollama Issues

| Problem | Fix |
|---|---|
| `ollama run` hangs | Free RAM with `ai-stop-all` |
| Model won't load | Use smaller model |
| `connection refused` | `ollama serve` |
| Slow generation | Check `mactop`, stop other apps |
| Wrong model version | `ollama rm model && ollama pull model` |
| Context too long | Increase `num_ctx` |
| Gibberish output | Lower temp, improve prompt |

```bash
ollama --version
ollama list
ollama ps
mactop
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

### MLX Issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: mlx` | `pip3 install --user mlx-lm` |
| CPU instead of GPU | Update macOS, check device |
| Download fails | Check `~/.cache/huggingface` |
| Out of memory | Use 4-bit model |
| Slow first run | Expected; model download/cache |

```bash
python3 -c "import mlx.core as mx; print(mx.default_device())"
python3 -c "import mlx_lm; print(mlx_lm.__version__)"
ls ~/.cache/huggingface/hub | head -10
```

### Claude Code Issues

| Problem | Fix |
|---|---|
| `claude` not found | `npm install -g @anthropic-ai/claude-code` |
| Auth failure | `claude --doctor` |
| Context exceeded | `/compact` |
| Hooks not firing | Check `.claude/settings.json` |
| MCP unreachable | Restart MCP server |
| Rewind not working | Update Claude Code |
| Sandbox blocks needed command | Adjust sandbox or run outside |

```bash
claude --version
claude --doctor
node --version
npm list -g @anthropic-ai/claude-code
```

### MLX Whisper Issues

| Problem | Fix |
|---|---|
| HF 401 / repo not found | Use correct model id |
| `.txt` empty or missing | Use `mlx_whisper` CLI |
| Repeated phrase spam | Hallucination mode + segmentation |
| Speech sounds underwater | Lower `afftdn` |
| Laptop very hot | AC power, one meeting at a time |

---

## PART 9: MODEL UPDATE PLAYBOOK

### Weekly Update Script

```bash
#!/bin/bash
set -euo pipefail
LOG="$HOME/logs/ai-model-update.log"
mkdir -p "$HOME/logs"

{
  echo "=== AI Model Update: $(date) ==="
  echo "Before:"
  python3 --version || true
  ollama --version || true
  claude --version || true
  pip show mlx-lm 2>/dev/null | grep -E 'Name|Version' || true
  pip show mlx-whisper 2>/dev/null | grep -E 'Name|Version' || true
} >> "$LOG" 2>&1

for model in llama3.1:8b deepseek-r1:8b qwen2.5:14b; do
  echo "Pulling $model" >> "$LOG"
  ollama pull "$model" >> "$LOG" 2>&1
done

# --- MLX-LM (venv) ---
source ~/.venvs/mlx/bin/activate
pip show mlx-lm 2>/dev/null | grep -E 'Name|Version' >> "$LOG"
pip install --upgrade mlx-lm >> "$LOG" 2>&1
pip show mlx-lm 2>/dev/null | grep -E 'Name|Version' >> "$LOG"
deactivate

# --- MLX Whisper (venv) ---
source ~/.venvs/whisper/bin/activate
pip show mlx-whisper 2>/dev/null | grep -E 'Name|Version' >> "$LOG"
pip install --upgrade mlx-whisper >> "$LOG" 2>&1
pip show mlx-whisper 2>/dev/null | grep -E 'Name|Version' >> "$LOG"
deactivate

npm update -g @anthropic-ai/claude-code >> "$LOG" 2>&1

{
  echo "After:"
  python3 --version || true
  ollama --version || true
  claude --version || true
  pip show mlx-lm 2>/dev/null | grep -E 'Name|Version' || true
  pip show mlx-whisper 2>/dev/null | grep -E 'Name|Version' || true
  echo "Done."
} >> "$LOG" 2>&1
```

**Notes:**
- Before/after version logging preserved for rollback decisions.
- Each venv block is self-contained: activate → log → upgrade → log → deactivate.

**Rollback guidance:**
- Review `$LOG` before and after versions.
- If an update breaks a workflow, pin/reinstall the previous known-good package version in the relevant venv or npm global install.
- Do not auto-run this on production-critical days without checking release notes.

### Check release notes

```bash
open https://github.com/ollama/ollama/releases
open https://github.com/ml-explore/mlx-lm/releases
open https://www.claudelog.com/claude-code-changelog
```

---

## PART 10: OLLAMA API PATTERNS

### Structured JSON output

```bash
curl -s http://localhost:11434/api/chat \
  -d '{
    "model": "qwen2.5:14b",
    "messages": [{"role": "user", "content": "Extract: The meeting is March 25 at 3pm with Alice and Bob about Q1 budget."}],
    "format": {
      "type": "object",
      "properties": {
        "date": {"type": "string"},
        "time": {"type": "string"},
        "attendees": {"type": "array", "items": {"type": "string"}},
        "topic": {"type": "string"}
      },
      "required": ["date", "time", "attendees", "topic"]
    },
    "stream": false
  }' | jq '.message.content | fromjson'
```

### File + structured JSON pipeline

```bash
CONTENT=$(cat ~/Research/Notes/meeting.md)
curl -s http://localhost:11434/api/chat \
  -d "$(jq -n --arg content "$CONTENT" '{
    model: "qwen2.5:14b",
    messages: [{"role": "user", "content": ("Extract all action items as JSON array\n" + $content)}],
    format: {"type": "array", "items": {"type": "object", "properties": {"owner": {"type": "string"}, "task": {"type": "string"}, "deadline": {"type": "string"}}}},
    stream: false
  }')" | jq '.message.content | fromjson'
```

### OpenAI-compatible chat completions

```bash
curl -s http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "system", "content": "You are a concise research assistant."},
      {"role": "user", "content": "What are the 3 key benefits of local LLMs?"}
    ]
  }' | jq '.choices[0].message.content'
```

### Embeddings

```bash
curl -s http://localhost:11434/api/embed \
  -d '{"model": "llama3.1:8b", "input": "Local AI models provide privacy and speed"}' \
  | jq '.embeddings[0][:5]'
```

--- 

TITLE TERMINAL LAB AI TERMINAL INTEGRATION v3.1 - PART X LOCAL RAG PIPELINE (OLLAMA + CHROMADB)

Local retrieval-augmented generation (RAG) turns your `~/Research` vault into a queryable knowledge base using only local tools. Stack: Ollama embeddings → ChromaDB (local vector store) → Ollama generation. No cloud dependency.

System  
Hardware M4 MacBook Pro, 48 GB RAM  
OS macOS Tahoe latest  
Shell zsh  
RAG stack Ollama, ChromaDB, Python venv (`~/.venvs/rag`)

X.1 What this does

- Scans `~/Research` for `.md` and `.txt` files.  
- Chunks each file into ~1000-character segments with overlap.  
- Embeds chunks via Ollama’s `nomic-embed-text` embedding model.  
- Stores vectors and metadata in a local ChromaDB collection.  
- At query time: embeds your question, retrieves top-k chunks, and feeds them plus the question to a local chat model (`qwen2.5:14b`) for the answer.

Everything stays on-device: same privacy tier as other Ollama/MLX workflows.

X.2 One-time setup (venv + models)

```bash
# 1. Create dedicated venv
mkdir -p ~/.venvs
python3 -m venv ~/.venvs/rag
source ~/.venvs/rag/bin/activate
pip install --upgrade pip
pip install chromadb ollama
deactivate

# 2. Pull embedding + answer models
ollama pull nomic-embed-text
ollama pull qwen2.5:14b
ollama pull llama3.1:8b    # optional fast-answer model
```

X.3 Script locations and wiring

```bash
# Script and wrapper
mkdir -p ~/scripts ~/.local/bin

# Main script
#   ~/scripts/rag.py   (full script in README / Script Swipe File)
# Wrapper (auto-activates venv)
cat > ~/.local/bin/rag << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
source ~/.venvs/rag/bin/activate
exec python3 "$HOME/scripts/rag.py" "$@"
EOF
chmod +x ~/.local/bin/rag
```

Core paths:

- Research dir  `~/Research`  
- Chroma DB     `~/.local/share/rag/chroma`  
- Hash manifest `~/.local/share/rag/hashes.json`  
- Collection    `research_vault`  

X.4 Core workflow

Ingest (initial full build):

```bash
rag ingest --full
rag stats
```

Incremental refresh (changed files only):

```bash
rag-refresh --yes        # preview + auto-ingest
# or:
rag ingest               # direct incremental ingest
```

Ask questions:

```bash
rag ask "Summarize the main upgrade ideas for Terminal Lab."
rag ask "What safety rules does Terminal Lab enforce?"
```

Switch answer model:

```bash
RAG_MODEL=llama3.1:8b rag ask "quick summary"
```

Behavior:

- Embeddings: `nomic-embed-text` with different prefixes for queries vs documents.  
- Answer model: `CHAT_MODEL = os.getenv("RAG_MODEL", "qwen2.5:14b")`.  
- Chunking: 1000 characters, 150-character overlap, `TOP_K = 6` chunks per query.

X.5 Safety and constraints

- Data scope: only `.md` and `.txt` under `~/Research` are ingested.  
- Secrets: do not store API keys, SSH keys, or `.zshenv` contents in `~/Research`; they would be embedded and searchable.  
- Resource use: `nomic-embed-text` uses ~500 MB RAM; `qwen2.5:14b` needs ~10 GB. Use `mactop` before long runs and stop unused models with `ai-stop-all`.  
- Incremental updates: `hashes.json` tracks file hashes, so re-running `rag ingest` only re-embeds changed or new files and removes deleted files from ChromaDB.

If you later expand this to a full benchmarked “RAG tuned baseline,” reference the Script Swipe File entry for `rag.py` and include tested `CHUNK_SIZE`, `CHUNK_OVERLAP`, and `TOP_K` values with dates.

---

PART 11 MLX VISION & MULTIMODAL MODELS (VLMs)
Local vision-language models (VLMs) run on the M4 GPU and understand images, diagrams, and screenshots far better than tesseract-based OCR. Use them for document OCR replacement, screenshot analysis, diagram-to-text, and chart data extraction.

System:

Hardware: M4 MacBook Pro, 48 GB RAM

OS: macOS Tahoe latest

Shell: zsh

VLM stack: mlx-vlm (MLX backend) + Qwen2-VL models + optional Ollama LLaVA

Key principle:

Image, PDF page, and screenshot data processed entirely on-device (same privacy tier as Ollama and MLX text).

11.1 Installation (venv-safe, Python 3.12)
Goal: Create an isolated venv for VLMs using a stable Python version and MLX-optimized wheels.

🟡 modifies state

bash
# 1. Install stable Python for VLMs (side-by-side with 3.14)
brew install python@3.12

# 2. Create dedicated VLM venv
/opt/homebrew/bin/python3.12 -m venv ~/.venvs/vlm312

# 3. Activate and install MLX-VLM + processor deps
source ~/.venvs/vlm312/bin/activate
pip install --upgrade pip

# Core: MLX-VLM + MLX backend + transformers/datasets, etc.
pip install "mlx-vlm==0.4.3"

# Qwen2-VL processors currently require PyTorch + Torchvision.
# These are used for image/video processing; inference still runs on MLX.
pip install "torch==2.5.1" "torchvision==0.20.1"

# Sanity-check
python - << 'EOF'
import torch, torchvision
print("torch", torch.__version__, "torchvision", torchvision.__version__)
EOF

deactivate
Notes:

Keep VLM workloads in ~/.venvs/vlm312 (Python 3.12); avoid 3.14 until upstream support is boring.

Model weights download once from Hugging Face into ~/.cache/huggingface/hub/, then stay cached locally.

11.2 First Run: Qwen2-VL Baseline Test
Goal: Confirm MLX-VLM is wired correctly, GPU is used, and RAM stays within budget.

🟢 read-only

bash
source ~/.venvs/vlm312/bin/activate

mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --max-tokens 64 \
  --temperature 0.0 \
  --prompt "Describe this image in one short paragraph." \
  --image "http://images.cocodataset.org/val2017/000000039769.jpg"

deactivate
Expected:

First call downloads ~1.3 GB of model + processor files, then prints a paragraph describing two cats on a pink blanket with remote controls, along with telemetry:

Prompt: ~420 tokens, ~370 tokens/sec

Generation: ~50 tokens, ~160 tokens/sec

Peak memory: ~2.5 GB on 2B 4-bit model (fits comfortably in 48 GB).

If this succeeds, MLX-VLM + Qwen2-VL are ready for OCR and screenshot workflows.

11.3 RAM Tiers for Vision Models
Reference for this M4 (48 GB). All RAM numbers are approximate 4-bit VRAM usage.

Model family	Params	4-bit RAM	M4 Tier	Use case
Qwen2-VL-2B-Instruct-4bit	2B	~2.5 GB	All	Fast descriptions, screenshots
Qwen2.5-VL-3B-4bit	3B	~3–4 GB	All	Higher quality OCR / diagrams
Qwen2-VL-7B-4bit	7B	~5–6 GB	16 GB+	More detailed reasoning
Qwen2.5-VL-72B-4bit	72B	~42 GB	48 GB (tight)	Max quality, single-task only
LLaVA 7B (Ollama)	7B	~4.5 GB	16 GB+	General multimodal via Ollama
LLaVA 13B (Ollama)	13B	~10 GB	24 GB+	Higher quality via Ollama
For this machine:

2B and 3B models are “always safe”.

7B is fine alongside one 8B text LLM.

72B and 13B should be run alone (stop other models first with ai-stop-all).

11.4 CLI Usage — Images → Text (MLX-VLM)
Goal: Send local images, diagrams, and screenshots to Qwen2-VL and get structured text back.

11.4.1 Describe any local image
🟢 read-only

bash
source ~/.venvs/vlm312/bin/activate

mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --max-tokens 256 \
  --temperature 0.0 \
  --prompt "Describe this image in detail." \
  --image "/path/to/image.png"

deactivate
What it does:

Loads the 2B VLM via MLX, sends the image + prompt, and streams a detailed description to stdout.

11.4.2 Multiple images (before/after, comparisons)
🟢 read-only

bash
source ~/.venvs/vlm312/bin/activate

mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --max-tokens 512 \
  --temperature 0.0 \
  --prompt "Compare these two screenshots. What changed between the first and second?" \
  --image "/path/to/before.png" "/path/to/after.png"

deactivate
Use cases:

UI diff between two terminal screenshots.

“Before/after” plots and dashboards.

11.5 OCR Replacement: VLM Instead of tesseract
Goal: Replace tesseract in the SVVSD pipeline for hard cases: complex layouts, handwritten annotations, charts, and diagrams.

11.5.1 VLM OCR helper script
🟡 modifies state

bash
source ~/.venvs/vlm312/bin/activate

cat > ~/.venvs/vlm312/vlm_ocr.py << 'EOF'
#!/usr/bin/env python3
"""VLM-based OCR: extract text from a document image using MLX-VLM."""

import sys
from mlx_vlm import load, generate
from mlx_vlm.utils import load_config
from mlx_vlm.prompt_utils import apply_chat_template

MODEL_PATH = "mlx-community/Qwen2-VL-2B-Instruct-4bit"

SYSTEM_PROMPT = (
    "Extract ALL visible text from this document image. "
    "Preserve structure where possible (headings, paragraphs, lists, tables). "
    "Output plain text only. Do not describe the image."
)

def ocr_image(image_path: str, model_path: str = MODEL_PATH) -> str:
    model, processor = load(model_path)
    config = load_config(model_path)
    formatted = apply_chat_template(
        processor,
        config,
        SYSTEM_PROMPT,
        num_images=1,
    )
    return generate(
        model,
        processor,
        formatted,
        [image_path],
        max_tokens=2048,
        verbose=False,
    )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: vlm_ocr.py <image_path>", file=sys.stderr)
        sys.exit(1)
    print(ocr_image(sys.argv[1]))
EOF

chmod +x ~/.venvs/vlm312/vlm_ocr.py

# Test on a scanned PDF page rendered to PNG
~/.venvs/vlm312/vlm_ocr.py "/path/to/scanned-page.png"

deactivate
What it does:

Provides a vlm_ocr.py drop-in script that takes an image path and prints VLM-extracted text.

In your consolidate.py OCR fallback, you can swap pytesseract.image_to_string(img) with a subprocess call to vlm_ocr.py for pages that tesseract struggles with.

11.5.2 When to use VLM vs tesseract
Use VLM OCR when:

PDF page has multi-column layouts, sidebars, or heavy formatting.

There are handwritten notes, arrows, or circles.

You need to understand diagrams, charts, or screenshots captured in PDFs.

Keep tesseract for:

Bulk clean text on simple forms and plain text documents.

11.6 Screenshot, Diagram, and Chart Analysis
Goal: Use VLMs for terminal screenshots, error dialogs, diagrams, and chart extraction.

11.6.1 Terminal and error screenshots
🟢 read-only

bash
source ~/.venvs/vlm312/bin/activate

mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --max-tokens 256 \
  --temperature 0.0 \
  --prompt "You are a senior systems engineer. Explain what this error or screenshot shows and suggest next debugging steps." \
  --image "/path/to/terminal-screenshot.png"

deactivate
Use cases:

“What is failing in this panic screen?”

“Explain this stack trace screenshot and next commands to run.”

11.6.2 Chart → data extraction
🟢 read-only

bash
source ~/.venvs/vlm312/bin/activate

mlx_vlm.generate \
  --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --max-tokens 512 \
  --temperature 0.0 \
  --prompt "Read the chart and output key series as CSV with headers and approximate numeric values." \
  --image "/path/to/chart.png"

deactivate
Feeds:

Budget charts from board packets.

Enrollment trends, performance graphs in SVVSD docs.

11.7 Ollama Multimodal (LLaVA) — Optional Path
Goal: Use Ollama’s LLaVA models when you prefer Ollama’s CLI and Modelfiles.

🟡 modifies state

bash
# Pull vision models
ollama pull llava:7b
ollama pull llava:13b

# Simple description
ollama run llava:13b "Describe this image" --images "/path/to/image.png"

# OCR-style extraction
ollama run llava:13b "Extract all visible text from this image as plain text." --images "/path/to/image.png"
Notes:

LLaVA models use the same Ollama privacy guarantees (data stays local, models stored under OLLAMA_MODELS).

Use Ollama vision when you want one unified model list and Modelfiles; use MLX-VLM when you want max speed and Python integration.

11.8 vLLM-MLX Unified Server (Advanced)
Goal: One OpenAI-compatible server that handles text + image (+ video/audio) using MLX models, including Qwen2-VL, with continuous batching.

🟡 modifies state

bash
pip3 install --user vllm-mlx

# Start server with Qwen2-VL for multimodal API
vllm serve mlx-community/Qwen2-VL-2B-Instruct-4bit \
  --host 0.0.0.0 --port 8000
Test — text-only:

bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Qwen2-VL-2B-Instruct-4bit",
    "messages": [{"role": "user", "content": "Hello from MLX on M4."}]
  }' | jq .choices[0].message.content
Test — image via base64:

bash
IMG_B64=$(base64 < "/path/to/image.png")

curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"mlx-community/Qwen2-VL-2B-Instruct-4bit\",
    \"messages\": [{
      \"role\": \"user\",
      \"content\": [
        {\"type\": \"text\", \"text\": \"Extract all visible text from this image.\"},
        {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:image/png;base64,$IMG_B64\"}}
      ]
    }]
  }" | jq .choices[0].message.content
Notes:

vLLM-MLX on M4 Max has been measured at ~460 tokens/sec with continuous batching; your M4 Pro/Max will be in the same ballpark.

API is OpenAI-compatible, so you can point tools like Continue, Open Interpreter, or custom scripts at http://localhost:8000/v1.

11.9 .zshrc Aliases for VLMs
Add to the existing Part 5 alias section.

🟡 modifies state

bash
# MLX-VLM (vision)
alias vlm-activate='source ~/.venvs/vlm312/bin/activate'
alias vlm-describe='vlm-activate && mlx_vlm.generate --model mlx-community/Qwen2-VL-2B-Instruct-4bit --temperature 0.0 --max-tokens 256 --prompt "Describe this image in detail." --image'
alias vlm-ocr='vlm-activate && ~/.venvs/vlm312/vlm_ocr.py'

# Ollama vision
alias ai-vision='ollama run llava:13b'

# Example usage:
# vlm-describe ~/Desktop/screenshot.png
# vlm-ocr ~/Desktop/scanned-page.png
# ai-vision "Explain this error dialog" --images ~/Desktop/error.png
11.10 Troubleshooting (VLM)
Symptoms and fixes to mirror Part 8 layout.

Symptom	Fix
Symptom	Fix
Qwen2VLVideoProcessor requires the PyTorch library	In ~/.venvs/vlm312: pip install torch==2.5.1 torchvision==0.20.1
Model download slow / rate-limited	Set HF_TOKEN in environment, or wait; first pull only.
mlx_vlm not found	source ~/.venvs/vlm312/bin/activate before running commands.
Out of memory when loading 72B VLM	Stop other models (ai-stop-all), or drop to 2B/3B/7B VLM.
Image errors / path issues	Use absolute paths, wrap in quotes, confirm file exists (ls "/path/to/image.png").
vLLM-MLX server port in use	lsof -i :8000, kill conflicting process, restart vllm serve.

---


PART 12 — AI PIPELINE CHAINING AND ORCHESTRATION
Hardware: M4 MacBook Pro, 48 GB RAM | OS: macOS Tahoe | Shell: zsh
Script: scripts/ai-chain.sh (see Script Swipe File Index)

The building blocks are already in place: pipe patterns (Part 1), Ollama API (Part 10), MLX inference (Part 2), Whisper (Part 2b), structured JSON output (Part 10). This part chains them into repeatable, validated multi-step workflows.

12.1 Core Concepts
Every hop in a chain has three properties:

Property	Purpose	Example
Model	Which model to use	llama3.1:8b (fast) vs qwen2.5:14b (deep)
Validator	Quality gate before next step	word count, JSON schema, grep
Retry	What to do on failure	lower temp, fallback to larger model
Use fast models for intermediate steps (summarize, chunk, classify). Use deep models for final synthesis and structured extraction. Reserve reasoning models (deepseek-r1) for multi-step logic only.

12.2 Multi-Hop Pipe Patterns
🟢 Pattern 1: Transcribe → Summarize → Extract actions

text
# Step 1: Transcribe audio (MLX Whisper)
source ~/.venvs/whisper/bin/activate
mlx_whisper meeting.wav \
    --model mlx-community/whisper-large-v3-mlx \
    --language en && deactivate

# Step 2: Summarize transcript (fast model)
cat meeting.txt | ollama run llama3.1:8b \
    "Summarize in 5 bullet points. Focus on decisions and key topics." \
    > summary.md

# Step 3: Extract action items as structured JSON (deep model)
cat summary.md | ollama run qwen2.5:14b \
    'Extract action items. Return ONLY valid JSON array: [{"action":"...","owner":"...","due":"..."}]' \
    > actions.json

# Step 4: Validate JSON before using it downstream
jq '.' actions.json && echo "✓ Valid JSON" || echo "✗ JSON invalid"
🟢 Pattern 2: Research notes → Summarize → Synthesize

text
# Chain uses process substitution for clean multi-file input
cat Research/**/*.md \
    | head -c 40000 \
    | ollama run llama3.1:8b "Summarize the key themes and open questions" \
    | tee summary.md \
    | ollama run qwen2.5:14b "Write a synthesis memo with 3 themes, contradictions, and next steps" \
    > synthesis.md
🟢 Pattern 3: Log triage chain

text
# Extract → Rank → Diagnose
grep -E "ERROR|FATAL|Exception" app.log | head -200 \
    | tee >(sort | uniq -c | sort -rn > ranked_errors.txt) \
    | ollama run llama3.1:8b "Rank these errors by severity and frequency" \
    | ollama run qwen2.5:14b "For each error, suggest root cause and one diagnostic command" \
    > triage.md
12.3 Validation Gates
Never pass model output to the next hop unchecked. Gates prevent garbage from propagating.

🟢 Word count gate — minimum meaningful output:

text
OUTPUT=$(cat notes.md | ollama run llama3.1:8b "Summarize in 5 bullets")
WORDS=$(echo "$OUTPUT" | wc -w | tr -d ' ')
if (( WORDS < 30 )); then
    echo "WARN: output too short ($WORDS words), retrying with deeper model" >&2
    OUTPUT=$(cat notes.md | ollama run qwen2.5:14b "Summarize in 5 bullets")
fi
echo "$OUTPUT" > summary.md
🟢 JSON schema validation — required before any downstream JSON consumer:

text
OUTPUT=$(cat summary.md | ollama run qwen2.5:14b \
    'Extract as JSON: {"name":"...","date":"...","amount":"..."}')

# Validate required keys exist
echo "$OUTPUT" | jq -e 'has("name") and has("date") and has("amount")' > /dev/null \
    && echo "✓ JSON valid" \
    || echo "WARN: missing keys — raw output: $OUTPUT" >&2
🟢 Pattern gate — expect specific content before proceeding:

text
# Ensure the model actually addressed the question
echo "$OUTPUT" | grep -qi "action\|task\|todo\|next step" \
    || echo "WARN: response may not contain action items" >&2
12.4 Retry with Temperature Reduction
🟡 Generic retry function — add to .zshrc or a shared script:

text
# ai_hop <model> <prompt> <input> [validator: words|json|none]
ai_hop() {
    local model="$1" prompt="$2" input="$3" validator="${4:-none}"
    local temp=0.7 attempt=0 output

    while (( attempt <= 2 )); do
        output=$(echo "$input" | ollama run "$model" "$prompt" 2>/dev/null)

        case "$validator" in
            words)
                local w; w=$(echo "$output" | wc -w | tr -d ' ')
                (( w >= 30 )) && { echo "$output"; return 0; } ;;
            json)
                echo "$output" | jq empty 2>/dev/null && { echo "$output"; return 0; } ;;
            *)  echo "$output"; return 0 ;;
        esac

        (( attempt++ ))
        temp=$(echo "$temp - 0.15" | bc)
        [[ "$model" == "llama3.1:8b" ]] && (( attempt == 2 )) && model="qwen2.5:14b"
        echo "RETRY attempt $attempt (temp=$temp, model=$model)" >&2
    done
    echo "$output"  # emit partial output after all retries
}
12.5 Parallel Fan-Out
🟢 Run same prompt on two models simultaneously, diff results:

text
# Fan-out: fast vs deep model in parallel
PROMPT="Summarize the key risks in this document"
FILE="report.md"

diff \
    <(cat "$FILE" | ollama run llama3.1:8b  "$PROMPT" 2>/dev/null) \
    <(cat "$FILE" | ollama run qwen2.5:14b  "$PROMPT" 2>/dev/null) \
    | head -60

# Or save both outputs for manual review
cat "$FILE" | ollama run llama3.1:8b  "$PROMPT" > /tmp/fast_out.txt &
cat "$FILE" | ollama run qwen2.5:14b  "$PROMPT" > /tmp/deep_out.txt &
wait
diff /tmp/fast_out.txt /tmp/deep_out.txt
12.6 ai-chain Script (Full Automation)
The scripts/ai-chain.sh wrapper provides battle-tested versions of the above patterns with validation, retry, logging, and output management built in.

🟡 Install:

text
chmod +x ~/scripts/ai-chain.sh
ln -sf ~/scripts/ai-chain.sh ~/.local/bin/ai-chain
🟡 Usage:

text
# Meeting pipeline: Transcribe → Summarize → Actions JSON
ai-chain meeting recording.wav

# Research vault synthesis
ai-chain research ~/Research/

# Log triage: Rank → Root cause
ai-chain log-triage ~/logs/app.log

# Parallel fan-out with diff
ai-chain fanout "Summarize the key risks" report.md
All output goes to ./chain-output/. Full step log at ./chain-output/chain.log.

ENV overrides:

text
AI_FAST_MODEL=llama3.1:8b ai-chain meeting recording.wav    # default fast
AI_DEEP_MODEL=qwen2.5:14b ai-chain meeting recording.wav    # default deep
OUTDIR=~/Projects/meeting-notes ai-chain meeting call.mp4   # custom output dir
12.7 .zshrc Aliases for Chaining
Add to existing Part 5 alias section:

text
# AI Pipeline Chaining
alias ai-chain='~/.local/bin/ai-chain'
alias ai-meeting='ai-chain meeting'          # ai-meeting recording.wav
alias ai-research='ai-chain research'        # ai-research ~/Research/
alias ai-logtriage='ai-chain log-triage'     # ai-logtriage app.log
alias ai-fanout='ai-chain fanout'            # ai-fanout "prompt" file.md
12.8 Safety Rules for Chains
Dry-run first: for chains that write files, use echo preview or --dry-run flags before committing output

Cap input size: head -c 40000 before any model call — Ollama silently truncates; vLLM-MLX errors. Be explicit.

Never chain to rm or mv without a human review step between the model output and the file operation

Log every hop: write to $OUTDIR/chain.log (built into ai-chain.sh) — when a chain fails mid-run you need to know which step broke

Model privacy tier unchanged: Ollama/MLX chains keep data local; any chain that calls claude or zsh-ai-assist sends data to cloud (see Part 7)

---

PART 13 — BENCHMARKING AND MODEL EVAL FRAMEWORK
Hardware: M4 MacBook Pro, 48 GB RAM | OS: macOS Tahoe | Shell: zsh
Script: scripts/ai-bench.sh (see Script Swipe File Index)
Output: ~/bench/bench_results.csv → append after every ai-model-update.sh run

The model selection table in Part 1 is opinion-based. This part replaces guesswork with measured data: tok/s, TTFT, RAM pressure, and quality scores — and automatically flags regressions after updates.

13.1 What Gets Measured
Metric	Source	How
tok/s	Ollama /api/generate response	eval_count / eval_duration * 1e9
TTFT ms	Ollama /api/generate response	prompt_eval_duration / 1e6
RAM used GB	vm_stat before/after	wired + active pages delta
Quality: summarize	Fixed prompt → scored 0–3	bullet count + word count + no bloat
Quality: JSON	Fixed prompt → scored 0–3	valid JSON + required keys present
Quality: reason	Fixed prompt → scored 0–3	correct answer + steps shown
Quality: code review	Fixed prompt → scored 0–3	specific issues identified + words
13.2 Install and Run
🟡 Install:

text
chmod +x ~/scripts/ai-bench.sh
ln -sf ~/scripts/ai-bench.sh ~/.local/bin/ai-bench
mkdir -p ~/bench
🟢 Benchmark all default models:

text
ai-bench run
Runs llama3.1:8b, qwen2.5:14b, deepseek-r1:8b by default. Each model: 1 bench call + 4 quality prompts. Total runtime: ~5–10 minutes depending on model size.

🟢 View latest results:

text
ai-bench show
# Model                          tok/s   TTFT ms  RAM GB  Q:sum Q:json Q:reason Q:code
# llama3.1:8b                    124.3       892    4.21    3/3    3/3      2/3    2/3
# qwen2.5:14b                     68.1      1240    8.43    3/3    3/3      3/3    3/3
# deepseek-r1:8b                  88.7      1080    5.12    2/3    2/3      3/3    2/3
13.3 Regression Detection Workflow
🟡 Step 1: Set baseline before any model update:

text
ai-bench run          # run benchmarks on current stable versions
ai-bench set-baseline # mark as "known good" baseline
🟡 Step 2: Run your existing update script:

text
~/scripts/ai-model-update.sh  # from Part 9
🟡 Step 3: Re-run bench — regressions auto-flagged:

text
ai-bench run
# ⚠️  REGRESSION DETECTED: qwen2.5:14b
#    Baseline: 68.1 tok/s
#    Current : 52.3 tok/s
#    Drop    : 23.2% (threshold: 10%)
#    → Run: ollama rm qwen2.5:14b && ollama pull qwen2.5:14b
Regression threshold defaults to 10%. Override:

text
REGRESSION_THRESHOLD=15 ai-bench run   # more lenient
REGRESSION_THRESHOLD=5  ai-bench run   # stricter
13.4 Bench Specific Models
🟢 Bench a single model (useful after ollama pull <model>):

text
BENCH_MODELS="qwen2.5:14b" ai-bench run
🟢 Bench all pulled models (after ai-model-update.sh):

text
BENCH_MODELS=$(ollama list | tail -n +2 | awk '{print $1}' | tr '\n' ' ') \
    ai-bench run
13.5 GPU and RAM Live Monitoring During Bench
🟢 Side-by-side: bench + live resource monitor (two terminal panes):

text
# Pane 1: run bench
ai-bench run

# Pane 2: watch GPU/RAM live while bench runs
mactop                   # Apple Silicon GPU/ANE/RAM usage
# or
sudo asitop              # requires sudo, more detail on ANE
# or
while true; do
    vm_stat | grep "Pages wired down" | awk '{print $NF}'
    sleep 2
done
🟢 Powermetrics GPU snapshot (one-shot, non-interactive):

text
# Capture GPU stats during a model run (requires sudo)
sudo powermetrics --samplers gpu_power -n 1 -i 1000 \
    | grep -E "GPU|Active|Idle|Freq"
Note: powermetrics requires sudo and produces significant output. Use mactop (no sudo, always in Terminal Lab) for daily monitoring.

13.6 Cost Tracking — Claude Code
🟢 View Claude Code session cost log:

text
ai-bench cost
# === Claude Code Cost Summary ===
# All-time sessions : 47
# All-time cost     : $8.2341
# Last 7 days       : $1.4200 (12 sessions)
#
# Recent sessions:
#   2026-04-03 01:15  $0.3120  session-abc123.jsonl
#   2026-04-02 22:45  $0.1840  session-def456.jsonl
Manual cost check from ~/.claude/ logs:

text
# Sum all session costs from Claude Code JSONL logs
find ~/.claude/logs -name "*.jsonl" -exec \
    jq -r 'select(.type=="result") | .total_cost // 0' {} \; \
    | awk '{sum+=$1} END {printf "Total: $%.4f\n", sum}'
13.7 CSV Format and Data Analysis
Output CSV at ~/bench/bench_results.csv:

text
date,model,tok_per_sec,ttft_ms,eval_count,eval_duration_ns,ram_used_gb,quality_summarize,quality_json,quality_reason,quality_code
2026-04-03 01:20,llama3.1:8b,124.3,892,256,2060000000,4.21,3,3,2,2
🟢 Quick analysis — best model per task:

text
# Fastest model
sort -t',' -k3 -rn ~/bench/bench_results.csv | head -5

# Best reasoning (col 10)
sort -t',' -k10 -rn ~/bench/bench_results.csv | head -5

# Models with tok/s > 100
awk -F',' '$3 > 100' ~/bench/bench_results.csv
🟢 Trend over time for one model:

text
MODEL="qwen2.5:14b"
grep ",$MODEL," ~/bench/bench_results.csv \
    | awk -F',' '{print $1, "tok/s:", $3, "TTFT:", $4"ms"}'
13.8 .zshrc Aliases for Benchmarking
Add to existing Part 5 alias section:

text
# AI Benchmarking
alias ai-bench='~/.local/bin/ai-bench'
alias ai-bench-run='ai-bench run'              # full benchmark run
alias ai-bench-show='ai-bench show'            # quick table view
alias ai-bench-cost='ai-bench cost'            # Claude Code cost log
alias ai-bench-baseline='ai-bench set-baseline' # mark current as known-good

# Post-update regression check (run after ai-model-update.sh)
alias ai-post-update='ai-bench set-baseline && ai-model-update.sh && ai-bench run'
13.9 Integration with ai-model-update.sh (Part 9)
Add these two lines to the existing ai-model-update.sh from Part 9 (before and after the update block):

🟡 Append to scripts/ai-model-update.sh:

text
# === ADD AT TOP OF UPDATE SCRIPT (after set -euo pipefail) ===
echo "--- Pre-update benchmark baseline ---" | tee -a "$LOG"
ai-bench set-baseline 2>&1 | tee -a "$LOG" || true

# ... (existing update commands: ollama pull, pip upgrade, npm update) ...

# === ADD AT BOTTOM OF UPDATE SCRIPT ===
echo "--- Post-update regression check ---" | tee -a "$LOG"
ai-bench run 2>&1 | tee -a "$LOG" || true
This makes regression detection automatic with zero extra steps.

13.10 Troubleshooting
Problem	Fix
ollama: command not found	ollama serve then retry
All tok/s show 0	Ollama API not responding: curl localhost:11434/api/tags
Model skipped	Model not pulled: ollama pull <model>
Quality all 0	Model loaded but not generating: check ollama ps
RAM delta negative	Normal — OS reclaimed pages between samples
jq: command not found	brew install jq
Baseline not found	Run ai-bench run then ai-bench set-baseline first

---

*Last updated: April 2026 (v3.1) — Cross-reference: README.md, 00_Index_and_Router.md, 05_Store_Database.md*
