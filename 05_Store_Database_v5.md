# 05_STORE_COMMAND_DATABASE
# TERMINAL LAB — COMMAND DATABASE v4
> Battle-tested commands organized by USE CASE. Add new entries as you go.
> Last updated: March 2026

---

## HOW TO USE

**Add a new entry:** Paste command in-thread → say "SAVE this to 05_Store under [category]"

**Entry format:**
```
### [Descriptive Name]
- **Use Case:** [category tag]
- **OS:** [macOS / Linux / Both]
- **Risk:** 🟢 / 🟡 / 🔴
- **Command:** (code block)
- **What it does:** one-line explanation
- **Tested:** [date] | **Status:** ✅ Verified / ⚠️ Needs testing
- **Notes:** gotchas, alternatives, context
```

**Categories:** `file-ops` · `text-proc` · `sysadmin` · `network` · `git` · `backup` · `dev-tools` · `docker` · `automation` · `security` · `ai-terminal` · `web-scraping`

---

## FILE-OPS

### Find and Delete Old Temp Files
- **Use Case:** file-ops | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  find /tmp -type f -mtime +7 -print          # 🟢 Preview
  find /tmp -type f -mtime +7 -delete         # 🟡 Execute
  ```
- **What it does:** Finds files in /tmp older than 7 days, then deletes them
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Always run `-print` first. Adjust path and days as needed.

---

### Bulk Rename Files with Pattern (bash loop)
- **Use Case:** file-ops | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  for f in *.jpeg; do echo "mv '$f' '${f%.jpeg}.jpg'"; done   # 🟢 Preview
  for f in *.jpeg; do mv "$f" "${f%.jpeg}.jpg"; done           # 🟡 Execute
  ```
- **What it does:** Renames all .jpeg files to .jpg in current directory
- **Tested:** 2026-03-23 | ✅ Verified

---

### Bulk Rename Files with Python Dict Map
- **Use Case:** file-ops | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  python3 script.py --dry-run    # 🟢 Preview
  python3 script.py              # 🟡 Execute
  ```
- **What it does:** Renames N files using a hardcoded `orig → (code, slug)` dict map. Writes backup manifest CSV before touching any file.
- **Key patterns:** `--dry-run` prints all planned renames · manifest written to `_rename_backup_manifest.csv` · pre-flight count check · already-renamed fallback
- **Tested:** 2026-03-23 | ✅ Verified (384/384 renamed)
- **Notes:** Dict map beats glob patterns when filenames are non-uniform. Model for any large bulk rename.

---

### Append PDF into Existing Merged File (pypdf)
- **Use Case:** file-ops | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  python3 -c "
  from pypdf import PdfWriter, PdfReader
  out = PdfWriter()
  for p in PdfReader('existing_merged.pdf').pages: out.add_page(p)
  for p in PdfReader('file_to_append.pdf').pages: out.add_page(p)
  with open('existing_merged.pdf','wb') as fh: out.write(fh)
  print('Done')
  "
  ```
- **What it does:** Reads all pages from existing merged PDF + new source PDF, combines, overwrites in place
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** `"Ignoring wrong pointing object"` warnings are harmless. Install in a venv: `pip install pypdf`

---

## TEXT-PROC

### Extract and Count Log Errors by Type
- **Use Case:** text-proc | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  grep -oE '(ERROR|WARN|FATAL)' app.log | sort | uniq -c | sort -rn
  ```
- **What it does:** Extracts error severity labels and ranks by frequency
- **Tested:** 2026-03-23 | ✅ Verified

---

### Replace String Across Multiple Files
- **Use Case:** text-proc | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  grep -rn "old_string" ./src/                                          # 🟢 Preview
  find . -name "*.py" -exec sed -i '' 's/old_string/new_string/g' {} + # 🟡 macOS
  find . -name "*.py" -exec sed -i 's/old_string/new_string/g' {} +    # 🟡 Linux
  ```
- **What it does:** Replaces all occurrences of a string in matching files in-place
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Use `rg --files-with-matches "old" | xargs sed` for speed on large trees.

---

## SYSADMIN

### Monitor System Resources (M4 Mac)
- **Use Case:** sysadmin | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  btop                                                    # Full system monitor
  mactop                                                  # Apple Silicon CPU/GPU/ANE/RAM
  vm_stat | head -10                                      # Raw memory page stats
  system_profiler SPHardwareDataType | grep "Memory"      # Total RAM
  ```
- **What it does:** Comprehensive system health check for M4 Mac
- **Tested:** 
- See README “Environment & Version Policy” for baseline.
- Known-good combo (as of 2026‑04‑02): Python 3.12 (Homebrew), latest `mlx-whisper`, `ffmpeg` (Homebrew), model `mlx-community/whisper-large-v3-mlx`.
- **Notes:** Run `mactop` before loading any Ollama model — RAM pressure must be below yellow.

---

### Manage Running AI Models (RAM)
- **Use Case:** sysadmin | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  ollama ps                                                                  # Running models + RAM
  ollama list                                                                # Downloaded models + sizes
  ollama stop llama3.1:8b                                                    # Free RAM
  ollama ps | tail -n +2 | awk '{print $1}' | xargs -I {} ollama stop {}    # Stop ALL models
  ```
- **What it does:** Inspect and free RAM held by local Ollama models
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Models hold RAM indefinitely until stopped.

---

### Find What's Using a Port
- **Use Case:** sysadmin | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  lsof -i :8080          # macOS / Linux
  ss -tlnp | grep 8080   # Linux (faster)
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Follow up with `kill PID` to free the port.

---

### Top 10 Largest Directories
- **Use Case:** sysadmin | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  du -sh */ | sort -rh | head -10      # Subdirs in current directory
  du -ah . | sort -rh | head -20       # All files + dirs, sorted by size
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Use `ncdu` for interactive version (`brew install ncdu`).

---

### Add Execute Permission to Script
- **Use Case:** sysadmin | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  chmod +x script.sh         # Add execute for all
  chmod 755 script.sh        # rwxr-xr-x
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

## NETWORK

### API Health Check
- **Use Case:** network | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health
  curl -s -w "HTTP %{http_code} | Time: %{time_total}s\n" -o /dev/null https://api.example.com
  curl -s https://api.example.com/data | jq '.'
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Test if a Port is Open
- **Use Case:** network | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  nc -zv hostname 22     # Test SSH
  nc -zv hostname 443    # Test HTTPS
  ```
- **What it does:** Checks TCP connectivity without sending data. Exit 0 = open.
- **Tested:** 2026-03-23 | ✅ Verified

---

### DNS Lookup
- **Use Case:** network | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  dig example.com +short    # Just the IP
  dig -x 8.8.8.8            # Reverse DNS
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### POST JSON to an API
- **Use Case:** network | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"key": "value"}' \
    https://api.example.com/v1/resource | jq '.'
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Set `TOKEN` via `export TOKEN="your_token"` first.

---

## GIT

### Initialize Research Vault
- **Use Case:** git | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  cd ~/Research && git init
  cat > .gitignore << 'EOF'
  *.pdf
  *.mp4
  *.zip
  .DS_Store
  *.tmp
  EOF
  git add . && git commit -m "init: research vault"
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Run once. Use `research-close` alias for daily commits.

---

### Daily Session Commit
- **Use Case:** git | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  cd ~/Research && git add . && git commit -m "session: $(date +%Y-%m-%d)"
  cd ~/Research && git add . && git commit -m "session: $(date +%Y-%m-%d)" && git push
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Visual Branch Log
- **Use Case:** git | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  git log --graph --oneline --all
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Stash and Restore Work in Progress
- **Use Case:** git | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  git stash                     # Shelve changes
  git stash list                # All stashes
  git stash pop                 # Restore most recent
  git stash apply stash@{1}     # Restore specific (keeps in list)
  git stash drop stash@{0}      # Delete specific stash
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Undo Last Commit (Safe)
- **Use Case:** git | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  git diff HEAD~1 --stat        # 🟢 Preview what will be undone
  git reset --soft HEAD~1       # 🟡 Undo commit, keep changes staged
  git reset HEAD~1              # 🟡 Undo commit, keep changes unstaged
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Do NOT use `--hard` unless discarding changes is intentional. Use `git reflog` to recover.

---

## BACKUP

### Research Vault Remote Backup
- **Use Case:** backup | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  # Setup (once)
  cd ~/Research
  git remote add origin https://github.com/YOUR-USERNAME/research-vault.git
  git push -u origin main

  # Daily
  cd ~/Research && git add . && git commit -m "backup: $(date '+%Y-%m-%d %H:%M')" --allow-empty && git push
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Use a PRIVATE repo. Authenticate with a personal access token.

---

### Verify Time Machine
- **Use Case:** backup | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  tmutil status           # Running=1 means active
  tmutil latestbackup     # Most recent backup path
  tmutil listbackups      # All backups
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Rsync Directory Backup
- **Use Case:** backup | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  rsync --dry-run -avz source/ user@server:/backup/dest/    # 🟢 Preview
  rsync -avz --progress source/ user@server:/backup/dest/   # 🟡 Execute
  rsync -avz --delete source/ dest/                         # 🟡 Mirror (deletes extras in dest)
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** `--delete` removes files in dest not in source — confirm intent.

---

### Create Compressed Archive
- **Use Case:** backup | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  tar -czf "backup_$(date +%Y%m%d_%H%M%S).tar.gz" ./target/   # Create
  tar -tf backup_*.tar.gz | head -20                            # Verify contents
  tar -xzf backup.tar.gz -C /restore/path/                     # Extract
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

## DEV-TOOLS

### pip Install on Homebrew-Managed macOS (PEP 668)
- **Use Case:** dev-tools | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  # Tier 1: system tools
  brew install ffmpeg jq pipx

  # Tier 2: standalone CLI tools
  pipx install ruff

  # Tier 3: libraries/ML in venvs (preferred)
  python3 -m venv ~/.venvs/tool
  source ~/.venvs/tool/bin/activate
  pip install --upgrade pip
  pip install <pkg>
  deactivate

  # Tier 4: last resort (breaks on brew upgrade python)
  pip3 install --user <pkg>
  ```
- **Tested:** 2026-04-12 | ✅ Updated
- **Notes:** `--user` is last resort. `--break-system-packages` removed from guidance. Pin Python version for ML venvs if needed (`/opt/homebrew/bin/python3.12`). See `02_Core Part 4`.

---

### Quick Local HTTP Server
- **Use Case:** dev-tools | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  python3 -m http.server 8000                          # Serves current dir at localhost:8000
  python3 -m http.server 8000 --bind 127.0.0.1         # localhost only (safer)
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Dev only. For HTTPS/auth use `caddy` or `ngrok`.

---

## DOCKER

### Shell Into a Running Container
- **Use Case:** docker | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  docker exec -it container_name bash    # Bash shell
  docker exec -it container_name sh      # Alpine fallback (no bash)
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Docker Disk Usage + Cleanup
- **Use Case:** docker | **OS:** Both | **Risk:** 🔴 Red (prune step)
- **Command:**
  ```bash
  docker system df                # 🟢 Always run first — shows what will be freed
  docker system prune             # 🟡 Remove stopped containers + dangling images
  docker system prune -af         # 🔴 Remove ALL unused — no recovery
  # -v flag ALSO removes volumes — extreme caution
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Never run `prune -af` without checking `df` first.

---

## AUTOMATION

### launchd: Weekly Homebrew Update
- **Use Case:** automation | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  launchctl load ~/Library/LaunchAgents/com.researcher.brew-update.plist
  launchctl start com.researcher.brew-update    # Test immediately
  launchctl list | grep com.researcher          # Check status
  tail -f ~/logs/brew_update.log                # Watch output
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Full plist template → `02_Core Part 5 Example 1`

---

### Research Session Aliases
- **Use Case:** automation | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command (add to ~/.zshrc):**
  ```bash
  alias research-start='cd ~/Research && mkdir -p ./Notes/sessions && echo "# Session: $(date)" > "./Notes/sessions/$(date +%Y-%m-%d).md" && echo "Session started"'
  alias research-close='cd ~/Research && ollama stop llama3.1:8b 2>/dev/null; git add . && git commit -m "session: $(date +%Y-%m-%d)" && echo "Session closed"'
  alias research-status='cd ~/Research && git status -s && echo "--- Models ---" && ollama ps'
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Cron Job — Run Script on Schedule
- **Use Case:** automation | **OS:** Linux | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  crontab -e
  # Add:
  0 9 * * 1-5 /full/path/to/script.sh >> /full/path/to/script.log 2>&1
  crontab -l    # Verify
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** macOS → use launchd instead. Always use full paths in cron.

---

### Watch a Directory for Changes
- **Use Case:** automation | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  fswatch -o ./src | xargs -n1 -I{} make build                            # macOS
  inotifywait -mr ./src -e modify,create,delete | while read; do make build; done  # Linux
  find src -name '*.py' | entr python3 run.py                              # Cross-platform (brew install entr)
  ```
- **Tested:** 2026-03-23 | ⚠️ Linux needs testing

---

## SECURITY

### Generate Strong Password / Token
- **Use Case:** security | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  openssl rand -base64 32    # ~43 chars, strong password
  openssl rand -hex 32       # 64 hex chars, API key style
  uuidgen                    # UUID (128-bit random)
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### Generate and Manage SSH Keys
- **Use Case:** security | **OS:** Both | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  ssh-keygen -t ed25519 -C "your_email" -f ~/.ssh/id_ed25519_research
  ssh-add --apple-use-keychain ~/.ssh/id_ed25519_research    # macOS Keychain
  cat ~/.ssh/id_ed25519_research.pub | pbcopy                # Copy public key
  ssh-copy-id user@hostname                                  # Deploy to server
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Always use a passphrase on the private key.

---

### Audit Permissions on Sensitive Files
- **Use Case:** security | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  ls -la ~/.ssh/                                   # Should be drwx------ (700)
  chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_*        # Fix if wrong
  ls -la ~/.zshenv                                 # Should be -rw------- (600)
  find ~ -name ".env" 2>/dev/null | xargs ls -la 2>/dev/null
  find . -type f -perm -o+w -print                 # World-writable files (risk)
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** API keys in `~/.zshenv` must be chmod 600.

---

## WEB-SCRAPING

### Create Python venv for Scraping Project
- **Use Case:** web-scraping | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  mkdir -p ~/svvsd-scraper && cd ~/svvsd-scraper
  python3 -m venv venv && source venv/bin/activate
  pip install requests beautifulsoup4 lxml pymupdf pytesseract Pillow
  brew install tesseract
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Always activate venv: `cd ~/svvsd-scraper && source venv/bin/activate`

---

### Verify Python Script Syntax Before Running
- **Use Case:** web-scraping | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  python3 -c "import ast; ast.parse(open('script.py').read()); print('✅ Syntax OK')"
  ```
- **What it does:** Parses Python as AST without executing — catches syntax errors from bad pastes
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Run after every nano paste. If it fails, `rm` the file and re-paste.

---

### Run Scraper with Checkpoint/Resume
- **Use Case:** web-scraping | **OS:** macOS | **Risk:** 🟡 Yellow
- **Command:**
  ```bash
  cd ~/svvsd-scraper && source venv/bin/activate
  python3 scrape_svvsd.py
  ```
- **Key patterns:** Checkpoint saves to `_checkpoint.json` after each meeting · Re-run resumes from last checkpoint · Corrupt PDFs auto-deleted · Downloads logged to `download_log.csv` / `failed.csv`
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Takes 1–2 hours. Safe to interrupt (Ctrl+C) and resume.

---

### Consolidate PDFs into Yearly Text Files
- **Use Case:** web-scraping | **OS:** macOS | **Risk:** 🟢 Green
- **Command:**
  ```bash
  cd ~/svvsd-scraper && source venv/bin/activate
  python3 consolidate.py
  ```
- **Key patterns:** Groups by year from `YYYY-MM-DD` filename prefix · OCR fallback on pages with <50 chars extractable · Flags files >500K words (NotebookLM limit)
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** 5–15 min vs 1–2 hr scrape. Run separately.

---

### Verify Downloaded PDF Integrity
- **Use Case:** web-scraping | **OS:** Both | **Risk:** 🟢 Green
- **Command:**
  ```bash
  ls svvsd_board_pdfs/*.pdf | wc -l                       # Count
  for f in svvsd_board_pdfs/*.pdf; do
    head -c 4 "$f" | grep -q '%PDF' || echo "BAD: $f"
  done                                                     # Check headers
  wc -w svvsd_combined/*.txt                              # Word counts
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

## AI-TERMINAL

### Pipe File to Local Model (Ollama)
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟢 Green (data stays local)
- **Command:**
  ```bash
  # RAM check first
  mactop   # must be below yellow
  ollama ps

  # Model selection:
  # Small file / quick Q&A  → llama3.1:8b
  # Long doc / synthesis    → qwen2.5:14b
  # JSON / structured output → qwen2.5:14b

  # Pipe file to model
  cat notes.md | ollama run llama3.1:8b "Summarize in 5 bullet points"
  cat meeting.txt | ollama run qwen2.5:14b "Extract all action items and owners"
  cat data.csv | ollama run qwen2.5:14b "What are the 3 most significant patterns?"

  # Multi-file
  cat file1.md file2.md | ollama run qwen2.5:14b "What are the biggest contradictions?"

  # Save output
  cat report.md | ollama run llama3.1:8b "Write an executive summary" > exec-summary.md

  # Free RAM when done
  ollama stop llama3.1:8b
  ```
- **What it does:** Pipes local files to an on-device Ollama model for summarization, extraction, or Q&A. All data stays local. Model choice depends on file size and task complexity.
- **Tested:** 2026-04-27 | ✅ Verified
- **Notes:** Run mactop before loading. Use qwen2.5:14b for docs >10k tokens — llama3.1:8b degrades on long context. Always stop the model when done.

---

### Batch Transcription — MLX Whisper (macOS Apple Silicon)
- **Use Case:** ai-terminal | **OS:** macOS Apple Silicon only | **Risk:** 🟡 Yellow (writes transcript files)
- **Command:**
  ```bash
  # Activate venv
  source ~/.venvs/whisper/bin/activate

  # RAM check
  mactop   # must be below yellow before loading Whisper

  # Dry-run first — preview what will be processed, no files written
  PROJECTROOT="/path/to/meeting-videos"   # change to your folder
  for inpath in "$PROJECTROOT"/*.mp4 "$PROJECTROOT"/*.flv; do
    [ -e "$inpath" ] || continue
    stem=$(basename "${inpath%.*}")
    echo "WOULD PROCESS: $inpath"
    echo "  → cleaned WAV: $PROJECTROOT/cleaned/${stem}.cleaned.wav"
    echo "  → transcript:  $PROJECTROOT/transcripts/${stem}.large-v3.txt"
  done
  echo "DRY RUN COMPLETE — no files written."

  # Live run (after confirming dry-run output)
  mkdir -p "$PROJECTROOT/cleaned" "$PROJECTROOT/transcripts"
  for inpath in "$PROJECTROOT"/*.mp4 "$PROJECTROOT"/*.flv; do
    [ -e "$inpath" ] || continue
    stem=$(basename "${inpath%.*}")
    cleaned="$PROJECTROOT/cleaned/${stem}.cleaned.wav"
    outtxt="$PROJECTROOT/transcripts/${stem}.large-v3.txt"
    [ -f "$outtxt" ] && [ $(wc -w < "$outtxt") -gt 50 ] && continue   # skip if good transcript exists
    ffmpeg -i "$inpath" -vn -ac 1 -ar 16000 \
      -af "afftdn=nr=25,loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=80" \
      "$cleaned" -y
    mlx_whisper "$cleaned" \
      --model mlx-community/whisper-large-v3-mlx \
      --language en \
      --output-dir "$PROJECTROOT/transcripts"
  done

  deactivate
  ```
- **What it does:** Batch transcribes meeting videos to text using MLX Whisper on Apple Silicon. Cleans audio with ffmpeg first. Skips files that already have a good transcript (>50 words). Dry-run previews all actions before writing.
- **Tested:** 2026-04-03 | ✅ Verified M4 48GB
- **Notes:** Run mactop first — peak RAM ~3GB. Known-good combo: mlx-whisper latest, ffmpeg Homebrew, model mlx-community/whisper-large-v3-mlx. Always dry-run first.

### Image → Text with Local VLM (MLX-VLM)

- **Use Case:** ai-terminal | **OS:** macOS (Apple Silicon only) | **Risk:** 🟢 Green (data stays local)
- **Command:**
  ```bash
  source ~/.venvs/vlm312/bin/activate
  mlx_vlm.generate \
    --model mlx-community/Qwen2-VL-2B-Instruct-4bit \
    --max-tokens 64 \
    --temperature 0.0 \
    --prompt "Describe this image in one short paragraph." \
    --image "/path/to/image.png"
  deactivate
  ```
- **Tested:** 2026-04-03 | ✅ Verified (M4, 48GB)
- **Notes:** Requires `mlx-vlm==0.4.3` plus `torch==2.5.1` and `torchvision==0.20.1` in `~/.venvs/vlm312`. Peak RAM ~2.5GB. Use for screenshots, scanned pages, diagrams when tesseract struggles.

---

### Local RAG Query (Ollama + ChromaDB)
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟡 Yellow (re-embeds on refresh, review before running)
- **Command:**
  ```bash
  # Activate RAG venv
  source ~/.venvs/rag/bin/activate

  # RAM check
  mactop   # must be below yellow

  # Incremental ingest (only re-embeds changed files)
  rag-refresh --yes

  # Query the vault
  rag ask "Summarize the main upgrade ideas for Terminal Lab."
  rag ask "What safety rules does Terminal Lab enforce?"
  rag ask "What is the current status of the SVVSD board meeting pipeline?"

  # Use a faster/lighter model for quick queries
  RAGMODEL=llama3.1:8b rag ask "Quick summary of last session notes."

  # Full index rebuild (only if embeddings are stale or corrupted)
  rag ingest --full

  deactivate

  # Free RAM when done
  ollama stop qwen2.5:14b
  ollama stop nomic-embed-text
  ```
- **What it does:** Queries the local Research vault using a fully on-device RAG pipeline. Chunks and embeds .md/.txt files with nomic-embed-text via Ollama, stores vectors in ChromaDB at ~/.local/share/rag/chroma, answers with qwen2.5:14b by default. Hash manifest at ~/.local/share/rag/hashes.json ensures only changed files are re-embedded.
- **Tested:** 2026-04-03 | ✅ Verified M4 48GB
- **Notes:** Uses .venvs/rag for isolation. RAGMODEL env var swaps answer model without editing scripts. Run rag-refresh before querying after any new notes. Stop both models when done — nomic-embed-text also holds RAM.

---

### Claude Code Research Synthesis
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟡 Yellow (can write files)
- **Command:**
  ```bash
  # Shift+Tab FIRST → activates Plan Mode before any file-writing task
  claude "Read all .md files in ~/Research/Notes. Identify 3 biggest themes. Draft synthesis memo. Save to ~/Research/synthesis.md"
  claude --continue              # Resume last session
  claude --doctor                # Health check
  git -C ~/Research diff         # Review changes after Claude writes files
  ```
- **Tested:** 2026-03-23 | ✅ Verified
- **Notes:** Never skip Plan Mode for file-writing. Always review `git diff` after session.

---

### Claude Code Code-Edit Session (Standard)
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟡 Yellow (writes files)
- **Command:**
  ```bash
  # 1. Enter project root and start Claude Code
  cd <project-root> && claude

  # 2. In Claude Code — Shift+Tab to Plan Mode
  # 3. Prompt:
  # "Scan <src/> for <task>. Propose a numbered todo list. Wait for my approval before touching any file."

  # 4. After approval and edits:
  git diff
  git status

  # 5. If run was successful and repeatable:
  # Ask Claude: "Summarize what you just did as a .claude-skills-*.md skill file (name, description, numbered steps). Save it to .claude-skills-<name>.md"
  ```
- **What it does:** Controlled file-edit session using Plan Mode, explicit plan approval, and mandatory git review before committing. Safe pattern for any code change via Claude Code.
- **Tested:** 2026-04-27 | ✅ Verified
- **Notes:** Never skip Plan Mode for file-writing. Always run git diff before committing. Promote reliable sessions to a skill file.

---

### Claude Code Multi-File Research Synthesis
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟡 Yellow (writes synthesis file)
- **Command:**
  ```bash
  # 1. Enter research root and start Claude Code
  cd ~/Research && claude

  # 2. Shift+Tab to Plan Mode
  # 3. Prompt:
  # "List all .md and .txt files in <subfolder> modified since <date>. Show me the list and wait for my approval before reading any file."

  # 4. Approve/prune the file list.
  # 5. Let Claude read, compact, and synthesize.
  # 6. Ask Claude to save output to a named file:
  # "Write the synthesis to synthesis-$(date +%Y-%m-%d).md"

  # 7. Review result:
  git -C ~/Research diff
  git status

  # 8. Promote to a skill:
  # "Summarize this workflow as a .claude-skills-research-synthesis.md skill."
  ```
- **What it does:** Scoped multi-file research synthesis with Plan Mode approval gate on the file list. Prevents context blowout by having Claude list and wait before reading. Ends with a named artifact and git review.
- **Tested:** 2026-04-27 | ✅ Verified
- **Notes:** Always approve the file list before Claude reads. Use `compact` command if context gets large. Review synthesis before committing.

---

### AI Command Generation (zsh-ai-assist)
- **Use Case:** ai-terminal | **OS:** macOS | **Risk:** 🟡 Yellow (review before running)
- **Command:**
  ```bash
  ai "find all PDF files in ~/Research modified in the last 7 days"
  ai "compress all .log files in ~/logs older than 30 days using gzip"
  ai "search all .md files in ~/Research for lines containing TODO"
  ??    # Auto-fix the last failed command
  ```
- **Tested:** 2026-03-23 | ✅ Verified

---

### MLX Inference (Apple Silicon)
- **Use Case:** ai-terminal | **OS:** macOS Apple Silicon only | **Risk:** 🟢 Green
- **Command:**
  ```bash
  # Install (one-time)
  mkdir -p ~/.venvs
  /opt/homebrew/bin/python3.12 -m venv ~/.venvs/mlx
  source ~/.venvs/mlx/bin/activate
  pip install --upgrade pip
  pip install mlx-lm
  python3 -c "import mlx.core as mx; print(mx.default_device())"  # Expected: Device(gpu, 0)
  deactivate

  # Inference
  source ~/.venvs/mlx/bin/activate
  mlx_lm.generate \
    --model mlx-community/Llama-3.1-8B-Instruct-4bit \
    --prompt "Summarize key AI trends for Mac researchers in 2026:" \
    --max-tokens 512
  deactivate
  ```
- **Tested:** 2026-03-23 | macOS M4 | ✅ Verified
- **Notes:** Faster than Ollama for single-shot tasks. Model downloads on first run. Pins Python 3.12 — mlx-lm wheels may lag behind Homebrew’s latest Python. If `python3.12` is missing: `brew install python@3.12`

---

## WORKFLOW PLAYBOOKS

### Workflow: Project Bootstrap (Dev)
**Goal:** Initialize a new project with git, virtualenv, and basic structure.
```bash
mkdir -p myproject/{src,tests,docs} && cd myproject
git init && echo '__pycache__/\n.venv/\n*.pyc' > .gitignore
python3 -m venv .venv && source .venv/bin/activate
pip install <base_deps> && pip freeze > requirements.txt
touch README.md && git add . && git commit -m "Initial commit"
```

---

### Workflow: Log Triage
**Goal:** Quickly find and rank errors in large log trees.
```bash
find ./logs -name "*.log" -mtime -1 -print                     # Recent logs
grep -rn "ERROR\|FATAL" ./logs/ | head -50                     # Surface errors
grep -oE '(ERROR|WARN|FATAL)' app.log | sort | uniq -c | sort -rn  # Rank by frequency
grep -A3 -B1 "FATAL" app.log > fatal_context.txt               # Extract context
```

---

### Workflow: AI Research Session
**Goal:** Start and close an AI-assisted research session cleanly.

**START:**
```bash
cd ~/Research && mkdir -p ./Notes/sessions
echo "# Session: $(date)" > "./Notes/sessions/$(date +%Y-%m-%d).md"
mactop          # Check RAM before loading models
ollama run llama3.1:8b
glow ./Notes/   # Browse recent notes
```

**DURING:**
```bash
rg "keyword" ~/Research/ --type md                        # Search all notes
cat source.md | ollama run llama3.1:8b "Key claims here?"
claude "Synthesize all files in ./Sources"                # Multi-file synthesis
```

**CLOSE:**
```bash
ollama ps | tail -n +2 | awk '{print $1}' | xargs -I {} ollama stop {}
cd ~/Research && git add . && git commit -m "session: $(date +%Y-%m-%d) — [topic]"
git push 2>/dev/null || true
```

---

### Workflow: Remote Server Setup (New VPS)
**Goal:** Secure and configure a fresh Linux server.
```bash
ssh root@server
adduser deploy && usermod -aG sudo deploy
ssh-copy-id deploy@server
# Edit /etc/ssh/sshd_config: PasswordAuthentication no · PermitRootLogin no
ufw allow 22 && ufw allow 80 && ufw allow 443 && ufw enable
sudo apt update && sudo apt upgrade -y
```

---

### Workflow: SVVSD Board Docs Pipeline (Scrape → Consolidate → NotebookLM)
**Goal:** Download all SVVSD board meeting PDFs (2011–2026), extract text, upload to NotebookLM.

**PHASE 1 — Setup (once):**
```bash
mkdir -p ~/svvsd-scraper && cd ~/svvsd-scraper
python3 -m venv venv && source venv/bin/activate
pip install requests beautifulsoup4 lxml pymupdf pytesseract Pillow
brew install tesseract
```

**PHASE 2 — Scrape (1–2 hrs):**
```bash
cd ~/svvsd-scraper && source venv/bin/activate
nano scrape_svvsd.py    # Paste script → Ctrl+O → Enter → Ctrl+X
python3 -c "import ast; ast.parse(open('scrape_svvsd.py').read()); print('✅ Syntax OK')"
python3 scrape_svvsd.py
```

**PHASE 3 — Consolidate (5–15 min):**
```bash
nano consolidate.py     # Paste script → Ctrl+O → Enter → Ctrl+X
python3 -c "import ast; ast.parse(open('consolidate.py').read()); print('✅ Syntax OK')"
python3 consolidate.py
```

**PHASE 4 — Upload:**
NotebookLM → New Notebook → Add Source → Upload
Finder: ⌘+Shift+G → `~/svvsd-scraper/svvsd_combined/` → ⌘+A → Open

- Full guide: `~/svvsd-scraper/SVVSD_Complete_Guide_v2.md`

---

### Workflow: Brewfile Setup (Tool Version Lock)
**Goal:** Lock tool versions, enable one-command restore on any Mac.
```bash
brew install ripgrep fzf zoxide eza bat glow btop lazygit jq csvlens mactop fd yq
brew install --cask ghostty raycast
brew bundle dump --file=~/Brewfile --force           # Save state
cp ~/Brewfile ~/Research/ && cd ~/Research && git add Brewfile && git commit -m "chore: update Brewfile"
brew bundle --file=~/Brewfile                        # Restore on new Mac
brew bundle check --file=~/Brewfile                 # Check for drift
```

---

### Workflow: Bulk File Rename (Python Dict Map)
**Goal:** Rename dozens–hundreds of files from original names to structured `CODE_Slug.ext` format.
1. Build `RENAME` dict: `orig_name → (code, slug)` for every file
2. Run `--dry-run` and review full output — touch nothing yet
3. Confirm pre-flight count matches expected
4. Execute — backup manifest CSV written before first `os.rename()`
5. Verify post-run file list against expected names

---

## SCRIPT SWIPE FILE INDEX

| # | Script Name | Purpose | Language | Location |
|---|---|---|---|---|
| 1 | backup.sh | Simple backup with rotation | bash | [link/path] |
| 2 | svvsd_all_in_one_v2.py | Bulk rename + PDF merge + CSV catalog | Python | ~/Documents/SVVSD_Policies/ |
| 3 | scrape_svvsd.py | Crawl SVVSD board meetings, download PDFs, checkpoint/resume | Python | ~/svvsd-scraper/ |
| 4 | consolidate.py | Extract text from PDFs, OCR fallback, yearly .txt output | Python | ~/svvsd-scraper/ |

---

## TESTING LOG

| Date | Command | OS | Result | Notes |
|---|---|---|---|---|
| 2026-03-23 | find + delete old tmp files | macOS | ✅ Pass | -print first |
| 2026-03-23 | bulk rename .jpeg → .jpg | macOS | ✅ Pass | echo preview confirmed |
| 2026-03-23 | grep error count | macOS | ✅ Pass | |
| 2026-03-23 | Bulk rename 384 PDFs via Python dict map | macOS zsh | ✅ Pass | --dry-run + manifest verified |
| 2026-03-23 | Append PDF to existing merged (pypdf) | macOS zsh | ✅ Pass | Harmless warnings confirmed |
| 2026-03-23 | venv pip install pypdf | macOS zsh | ✅ Pass | PEP 668 resolved |
| 2026-03-23 | ollama ps / stop | macOS zsh | ✅ Pass | RAM freed |
| 2026-03-23 | cat file pipe to ollama | macOS zsh | ✅ Pass | llama3.1:8b + qwen2.5:14b |
| 2026-03-23 | git init research vault | macOS zsh | ✅ Pass | .gitignore verified |
| 2026-03-23 | launchd brew update | macOS zsh | ✅ Pass | launchctl start tested |
| 2026-03-23 | openssl rand -base64 32 | macOS zsh | ✅ Pass | |
| 2026-03-23 | ssh-keygen ed25519 | macOS zsh | ✅ Pass | |
| 2026-03-23 | mlx_lm.generate | macOS M4 zsh | ✅ Pass | 8B 4-bit model |
| 2026-03-23 | python3 -m venv + scraping deps | macOS zsh | ✅ Pass | venv isolates from Homebrew Python |
| 2026-03-23 | ast.parse() syntax gate | macOS zsh | ✅ Pass | Catches heredoc contamination |
| 2026-03-23 | scrape_svvsd.py full run | macOS zsh | ✅ Pass | Checkpoint/resume verified |
| 2026-03-23 | consolidate.py full run | macOS zsh | ✅ Pass | OCR fallback confirmed |
| 2026-03-23 | PDF header integrity check | macOS zsh | ✅ Pass | 0 bad files |

---

## METRICS

- **Total stored commands:** 50+
- **Categories covered:** 12 / 12
- **Workflow playbooks:** 6
- **Last updated:** March 2026 (v4)

---

---
TITLE TERMINAL LAB COMMAND DATABASE v4 - WORKFLOW PLAYBOOKS - Workflow Local Meeting Videos → Whisper Transcripts (MLX, macOS) DRY-RUN

Goal
Simulate the MLX Whisper batch pipeline over a folder of meeting videos without writing any cleaned WAVs or transcripts. Use this to verify filenames, counts, and ffmpeg/Whisper behavior before a real run.

- Use Case ai-terminal
- OS macOS
- Risk Green (read-only, no files created)
- Dependencies
  - Same as full workflow: Python, ffmpeg, mlx-whisper installed.

Assumptions
- PROJECT_ROOT points at your meeting folder (same convention as the main workflow).

bash
PROJECT_ROOT="/Volumes/ExternalSSD/boardmeetings"  # change to your path
cd "$PROJECT_ROOT"

cat > batch_whisper_meetings_dry_run.sh <<'EOF'
#!/usr/bin/env zsh
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
VENV="${HOME}/.venvs/whisper"
CLEAN_DIR="${PROJECT_ROOT}/cleaned"
TXT_DIR="${PROJECT_ROOT}/transcripts"

if [[ ! -d "$VENV" ]]; then
  echo "ERROR: venv not found at $VENV" >&2
  exit 1
fi

echo "DRY RUN: no cleaned WAVs or transcripts will be written."
echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "VENV: $VENV"
echo

mkdir -p "$CLEAN_DIR" "$TXT_DIR"

source "$VENV/bin/activate"

for inpath in "$PROJECT_ROOT"/*.mp4 "$PROJECT_ROOT"/*.flv; do
  [[ -e "$inpath" ]] || continue

  stem="${inpath##*/}"
  stem="${stem%.*}"

  cleaned="${CLEAN_DIR}/${stem}_cleaned.wav"
  outtxt_default="${cleaned%.*}.txt"
  outtxt="${TXT_DIR}/${stem}_largev3.txt"

  echo "=== WOULD PROCESS: $inpath ==="
  echo "  cleaned WAV  -> $cleaned"
  echo "  default TXT  -> $outtxt_default"
  echo "  final TXT    -> $outtxt"

  if [[ -f "$outtxt" ]]; then
    words=$(wc -w < "$outtxt" 2>/dev/null || echo 0)
    if (( words >= 50 )); then
      echo "  ACTION: would SKIP (existing transcript, ${words} words)"
    else
      echo "  ACTION: would RETRY (existing transcript too short: ${words} words)"
    fi
  else
    echo "  ACTION: would RUN:"
    echo "    ffmpeg -i \"$inpath\" -vn -ac 1 -ar 16000 -af \"afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11,highpass=f=80\" \"$cleaned\""
    echo "    mlx_whisper \"$cleaned\" --model mlx-community/whisper-large-v3-mlx --language en"
  fi

  echo
done

deactivate

echo "DRY RUN COMPLETE."
EOF

chmod +x batch_whisper_meetings_dry_run.sh

# Run dry-run
./batch_whisper_meetings_dry_run.sh

*Add new commands: paste in-thread → "SAVE this to 05_Store under [category]"*
