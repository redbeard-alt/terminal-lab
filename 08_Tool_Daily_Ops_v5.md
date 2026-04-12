# 1. Daily Ops Cheat Sheet (Warp + Terminal Space)  
  
Each entry uses a one‑liner description, a risk label, then a paste‑safe block.  
  
## 1.1 Core navigation, search, inspection  
  
Search recursively in current tree for a pattern (e.g., text logs).    
**Risk:** read-only  
  
```bash  
rg "ERROR" .  
```  
  
Find JSON lines with a key/value and pretty‑print.    
**Risk:** read-only  
  
```bash  
rg '"level":"error"' logs/ | jq .  
```  
  
List files with a modern, detailed view.    
**Risk:** read-only  
  
```bash  
eza -lha  
```  
  
Jump to a frequently used directory with zoxide.    
**Risk:** read-only  
  
```bash  
z proj  
```  
  
View a file with syntax highlighting.    
**Risk:** read-only  
  
```bash  
bat logs/app.log  
```  
  
Fuzzy‑find a file and print its path.    
**Risk:** read-only  
  
```bash  
fzf  
```  
  
Monitor CPU, RAM, GPU, and processes.    
**Risk:** read-only  
  
```bash  
btop  
```  
  
## 1.2 Logs + local models  
  
Tail last 200 lines of app log into a temp file for analysis.    
**Risk:** modifies state (creates temp file)  
  
```bash  
tail -200 logs/app.log > /tmp/app_tail.log  
```  
  
Analyze recent log slice with a 14B local model for patterns/causes/actions.    
**Risk:** read-only  
  
```bash  
cat /tmp/app_tail.log | ai-14b \  
  "Identify recurring error patterns, likely root causes, and concrete next actions."  
```  
  
One‑shot log analysis from raw tail (no temp file).    
**Risk:** read-only  
  
```bash  
tail -200 logs/app.log | ai-14b \  
  "Summarize main errors, likely causes, and next steps."  
```  
  
## 1.3 Local LLMs via Ollama  
  
Quick Q&A or summaries on small text with an 8B model.    
**Risk:** read-only  
  
```bash  
ollama run llama3.1:8b \  
  "Summarize the key error patterns in this log snippet."  
```  
  
Deeper reasoning or architecture questions with a reasoning‑tuned model.    
**Risk:** read-only  
  
```bash  
ollama run deepseek-r1:8b \  
  "Explain the tradeoffs between a monolith and microservices for a 5-person team."  
```  
  
Larger‑context analysis with a 14B model for longer logs or docs.    
**Risk:** read-only  
  
```bash  
tail -500 logs/app.log | ollama run qwen2.5:14b  
```  
  
List all local models managed by Ollama.    
**Risk:** read-only  
  
```bash  
ai-models  
```  
  
Show currently running Ollama models.    
**Risk:** read-only  
  
```bash  
ai-status  
```  
  
Preview which models would be stopped before actually stopping them.    
**Risk:** read-only  
  
```bash  
ai-stop-all-preview  
```  
  
Stop all running models after preview.    
**Risk:** modifies state  
  
```bash  
ai-stop-all  
```  
  
## 1.4 MLX / Whisper (meetings)  
  
Verify MLX Whisper virtualenv is usable.    
**Risk:** read-only  
  
```bash  
source ~/.venvs/whisper/bin/activate  
python -c "import mlx_whisper; print('ok')"  
deactivate  
```  
  
Extract 1 hour of mono audio from a meeting recording.    
**Risk:** modifies state (creates wav file)  
  
```bash  
ffmpeg -ss 00:00:00 -t 01:00:00 -i meeting.mp4 \  
  -vn -ac 1 -ar 16000 cleaned_meeting.wav  
```  
  
Transcribe extracted audio with MLX Whisper to a text file.    
**Risk:** modifies state  
  
```bash  
source ~/.venvs/whisper/bin/activate  
mlxwhisper cleaned_meeting.wav \  
  --model mlx-community/whisper-large-v3-mlx \  
  --language en  
deactivate  
```  
  
Summarize a transcript and extract structured action items with a local LLM.    
**Risk:** read-only  
  
```bash  
cat cleaned_meeting.txt | ai-14b \  
  "Summarize this meeting and list all action items with owner, task, due date."  
```  
  
## 1.5 Claude Code (cc) basic flow  
  
Start Claude Code in the current repo (Plan Mode recommended after launch).    
**Risk:** read-only (session attach; edits depend on mode)  
  
```bash  
cd ~/dev/my-project  
cc  
```  
  
Check Claude Code CLI health (auth, network, config).    
**Risk:** read-only  
  
```bash  
claude --doctor  
```  
  
Resume the most recent Claude Code session from this directory.    
**Risk:** read-only  
  
```bash  
cc-resume  
```  
  
Continue the last exchange in the current session.    
**Risk:** read-only  
  
```bash  
cc-continue  
```  
  
## 1.6 zsh‑ai‑assist at the prompt (cloud)  
  
Ask AI (cloud) to explain a command before running it.    
**Risk:** read-only (prompt only)  
  
```bash  
ai "Explain what this command does and label risk: rg \"ERROR\" logs/ | jq ."  
```  
  
Ask AI to propose a safer version with a preview.    
  
**Risk:** read-only (prompt only)  
  
```bash  
ai "Given: COMMAND. Diagnose issues, then propose a preview (read-only) and a corrected command."  
```  
  
## 1.7 RAG (if rag.py is configured)  
  
Create a RAG virtualenv and install dependencies (one‑time).    
**Risk:** modifies state  
  
```bash  
mkdir -p ~/.venvs  
python3 -m venv ~/.venvs/rag  
source ~/.venvs/rag/bin/activate  
pip install --upgrade pip  
pip install chromadb ollama  
deactivate  
```  
  
Ingest `~/Research` into a local Chroma DB.    
**Risk:** modifies state  
  
```bash  
source ~/.venvs/rag/bin/activate  
python ~/scripts/rag.py ingest --root ~/Research --mode full  
deactivate  
```  
  
Ask RAG a question using `qwen2.5:14b`.    
**Risk:** read-only  
  
```bash  
source ~/.venvs/rag/bin/activate  
python ~/scripts/rag.py ask \  
  --model qwen2.5:14b \  
  --question "How do we schedule nightly Whisper jobs?"  
deactivate  
```  
  
---  
  
# 2. Quick‑Start (Fresh Mac: Warp + Terminal Space Stack)  
  
All commands align with the Terminal Lab environment (macOS Tahoe 26, Apple Silicon, zsh, Warp, modern CLI).  
  
## 2.1 Baseline environment  
  
- Confirm macOS Tahoe 26.x+ on Apple Silicon, 32–48 GB+ RAM, and 100 GB free disk.    
- Ensure Warp is the primary terminal.    
- Confirm zsh is the login shell (`echo "$SHELL"` and `chsh -s /bin/zsh` if needed).  
  
## 2.2 Install Homebrew, Warp, and core CLIs  
  
Install Homebrew, Warp, and core modern CLI tools.    
**Risk:** modifies state  
  
```bash  
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  
  
brew install --cask warp  
  
brew install ripgrep fd zoxide eza bat fzf jq btop ffmpeg  
```  
  
## 2.3 Install local AI tools (Ollama, MLX, Whisper)  
  
Install and start Ollama.    
**Risk:** modifies state  
  
```bash  
brew install ollama  
ollama --version  
ollama serve  
```  
  
Install MLX LM base tooling and verify device.    
**Risk:** modifies state  
  
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
  
Create a Whisper virtualenv and install MLX Whisper.    
**Risk:** modifies state  
  
```bash  
mkdir -p ~/.venvs  
python3 -m venv ~/.venvs/whisper  
source ~/.venvs/whisper/bin/activate  
pip install --upgrade pip  
pip install mlx-whisper  
deactivate  
  
brew install ffmpeg  
```  
  
## 2.4 Pull baseline Ollama models  
  
Pull core models and verify they are available and running.    
**Risk:** modifies state  
  
```bash  
ollama pull llama3.1:8b  
ollama pull qwen2.5:14b  
ollama pull deepseek-r1:8b  
  
ollama list  
ollama ps  
```  
  
## 2.5 Install Claude Code CLI  
  
Install Claude Code and dependencies, then run health checks.    
**Risk:** modifies state  
  
```bash  
brew install --cask claude-code || true  
claude --version || true  
claude --doctor || true  
  
brew install node  
npm install -g @anthropic-ai/claude-code  
claude --version  
claude --doctor  
```  
  
## 2.6 Install zsh‑ai‑assist  
  
Clone `zsh-ai-assist` into your home directory.    
**Risk:** modifies state  
  
```bash  
git clone https://github.com/MKSG-MugunthKumar/zsh-ai-assist ~/.zsh-ai-assist  
```  
  
## 2.7 Configure .zshenv for credentials  
  
Add API keys only to `~/.zshenv` (not `.zshrc`), then lock down permissions.    
**Risk:** modifies state  
  
```bash  
cp ~/.zshenv ~/.zshenv.bak 2>/dev/null || true  
cat <<'EOF' >> ~/.zshenv  
# AI API keys (example – fill values in editor)  
export ANTHROPIC_API_KEY="your_key_here"  
export OPENAI_API_KEY="your_key_here"  
EOF  
  
chmod 600 ~/.zshenv  
```  
  
## 2.8 Configure .zshrc for plugins and AI aliases  
  
Configure plugins, aliases, and AI helpers, then reload the shell.    
**Risk:** modifies state  
  
```bash  
cp ~/.zshrc ~/.zshrc.bak 2>/dev/null || true  
cat <<'EOF' >> ~/.zshrc  
# Load zsh-ai-assist only in interactive shells  
if [[ -o interactive ]]; then  
  source ~/.zsh-ai-assist/zsh-ai-assist.plugin.zsh  
fi  
  
# AI aliases - local models (Ollama)  
alias ai-fast='ollama run llama3.1:8b'  
alias ai-think='ollama run deepseek-r1:8b'  
alias ai-14b='ollama run qwen2.5:14b'  
alias ai-models='ollama list'  
alias ai-status='ollama ps'  
  
# List models that would be stopped  
alias ai-stop-all-preview="ollama ps | tail -n +2 | awk '{print \$1}'"  
  
# Stop all running models (run preview first)  
alias ai-stop-all="ai-stop-all-preview | xargs -r ollama stop"  
  
# MLX quick call (ensure mlx-lm is installed)  
alias mlx8b='mlxlm.generate --model mlx-community/Llama-3.1-8B-Instruct-4bit --max-tokens 512 --prompt'  
  
# Claude Code  
alias cc='claude'  
alias cc-resume='claude --resume'  
alias cc-continue='claude --continue'  
alias cc-check='claude --doctor'  
EOF  
  
source ~/.zshrc  
```  
  
## 2.9 Minimal end‑to‑end checks  
  
Run a log + ai‑14b pipeline from a project with `logs/app.log`.    
**Risk:** modifies state (temp file only)  
  
```bash  
tail -200 logs/app.log > /tmp/app_tail.log  
cat /tmp/app_tail.log | ai-14b \  
  "Identify recurring error patterns, likely root causes, and concrete next actions."  
```  
  
Validate the Whisper pipeline (venv + ffmpeg).    
**Risk:** modifies state  
  
```bash  
ffmpeg -ss 00:00:00 -t 01:00:00 -i meeting.mp4 \  
  -vn -ac 1 -ar 16000 cleaned_meeting.wav  
source ~/.venvs/whisper/bin/activate  
mlxwhisper cleaned_meeting.wav \  
  --model mlx-community/whisper-large-v3-mlx \  
  --language en  
deactivate  
```  
  
Check Claude Code Plan Mode from a small test repo.    
**Risk:** read-only if you stay in Plan Mode  
  
```bash  
cd ~/dev/test-repo  
cc  
```  
