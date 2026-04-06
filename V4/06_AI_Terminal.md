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
pip3 install --user mlx-lm
python3 -c "import mlx.core as mx; print(mx.default_device())"
```

Expected output: `Device(gpu, 0)`.

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

alias mlx8b='mlx_lm.generate --model mlx-community/Llama-3.1-8B-Instruct-4bit --max-tokens 512 --prompt'
alias mlx-whisper-test='source ~/.venvs/whisper/bin/activate && mlx_whisper'

alias cc="claude"
alias cc-resume="claude --resume"
alias cc-check="claude --doctor"
alias cc-continue="claude --continue"
```

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

pip3 install --user --upgrade mlx-lm >> "$LOG" 2>&1

source ~/.venvs/whisper/bin/activate
pip install --upgrade mlx-whisper >> "$LOG" 2>&1
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

*Last updated: April 2026 (v3.1) — Cross-reference: README.md, 00_Index_and_Router.md, 05_Store_Database.md*
