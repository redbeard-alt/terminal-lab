# 02_CORE_ADVANCED_WORKFLOWS  
# TERMINAL LAB — ADVANCED WORKFLOWS v4  
> Piping, scripting, automation, remote access, package management, Docker, xargs, tmux.  
> Last updated: April 2026 (macOS Tahoe 26, zsh, M4 MacBook Pro)  
  
---  
  
## Risk Legend  
  
- 🟢 read-only  
- 🟡 modifies state  
- 🔴 destructive or high-risk  
  
Run 🟢 previews first, then decide whether the 🟡/🔴 variant is appropriate.  
  
---  
  
## Part 1: PIPING & CHAINING  
  
Prefer modern tools (`rg`, `fd`, `eza`, `bat`) on the Tahoe workstation; classic tools remain for remote/CI.  
  
```bash  
# Find large files, sort by size, top 10 (preview)  
du -ah . | sort -rh | head -10              # 🟢 Read-only preview  
  
# Count ERROR lines in a log  
rg -c 'ERROR' app.log                        # 🟢 Count matches (ripgrep)  
# Classic:  
# rg 'ERROR' app.log | wc -l                # 🟢 via pipe  
  
# Unique IPs from access log, sorted by frequency  
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20   # 🟢  
```  
  
| Operator | Behavior                          | Use When                    |  
|---------|-----------------------------------|-----------------------------|  
| `&&`    | Run next only if previous succeeds | Safe sequential steps       |  
| `\|\|`  | Run next only if previous fails    | Fallback / error handling   |  
| `;`     | Run next regardless               | Independent commands        |  
| `\|`    | Pipe stdout to next stdin          | Data transformation         |  
  
```bash  
# Compare two command outputs without temp files  
diff <(eza dir1) <(eza dir2)                 # 🟢  
```  
  
---  
  
## Part 2: TEXT PROCESSING PIPELINE  
  
| Tool   | Purpose                   | Key Pattern                          |  
|--------|---------------------------|--------------------------------------|  
| `rg`   | Search/filter lines       | `rg -n "pattern" .`                  |  
| `sed`  | Find & replace, line edit | `sed 's/old/new/g' file`             |  
| `awk`  | Column extraction, math   | `awk '{print $1, $3}' file`          |  
  
### grep / rg  
  
```bash  
rg -i 'error' log.txt                    # 🟢 Case-insensitive search  
rg -n 'TODO' ./src                       # 🟢 Recursive + line numbers  
rg -v 'debug' log.txt                    # 🟢 Exclude lines  
rg -E 'err|warn|crit' log.txt            # 🟢 Extended regex  
rg -A3 -B1 'FATAL' log.txt               # 🟢 Context: 3 after, 1 before  
  
# Classic grep equivalents (remote/CI)  
grep -i 'error' log.txt                  # 🟢  
grep -rn 'TODO' ./src/                   # 🟢  
```  
  
### sed  
  
Use `sed` as a stream editor; avoid tree‑wide in‑place writes without a preview and backup.  
  
```bash  
sed 's/foo/bar/g' file.txt               # 🟢 Replace to stdout (preview)  
sed '/^#/d' config.txt                   # 🟢 Delete comment lines (stdout)  
sed '/^$/d' file.txt                     # 🟢 Delete blank lines (stdout)  
```  
  
In‑place edits — single file, local, after review:  
  
```bash  
# macOS BSD sed  
sed -i '' 's/foo/bar/g' file.txt         # 🟡 In-place (creates no backup by default)  
  
# Linux GNU sed  
sed -i 's/foo/bar/g' file.txt            # 🟡 In-place  
```  
  
Multi‑file replacements — safer pattern:  
  
```bash  
# 🟢 Dry-run: preview matches and files  
rg -n --glob '*.txt' 'old_value' .  
  
# 🟡 Scripted replacement with backups (run only after reviewing matches)  
python3 - <<'PY'  
from pathlib import Path  
for p in Path('.').rglob('*.txt'):  
    s = p.read_text()  
    if 'old_value' in s:  
        backup = p.with_suffix(p.suffix + '.bak')  
        backup.write_text(s)  
        p.write_text(s.replace('old_value', 'new_value'))  
PY  
```  
  
### awk  
  
```bash  
awk '{print $1}' file.txt                      # 🟢 First column  
awk -F',' '{print $2}' data.csv               # 🟢 Second column (CSV)  
awk '$3 > 100 {print $1, $3}' data.txt        # 🟢 Filter by value  
awk '{sum += $1} END {print sum}' numbers.txt  # 🟢 Sum a column  
```  
  
---  
  
## Part 3: BASH SCRIPTING  
  
```bash  
#!/usr/bin/env bash  
set -euo pipefail    # Fail early: errors, undefined vars, pipe failures  
  
readonly APP_NAME='myapp'  
LOG_DIR="${HOME}/logs"  
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"  
  
log() { echo "[$(date '+%H:%M:%S')] $*"; }  
die() { echo "ERROR: $*" >&2; exit 1; }  
  
[[ $# -lt 1 ]] && die "Usage: $0 <target_directory>"  
TARGET_DIR="$1"  
[[ -d "$TARGET_DIR" ]] || die "Directory not found: $TARGET_DIR"  
  
log "Starting $APP_NAME on $TARGET_DIR ..."  
# ... your commands here ...  
log "Done."  
```  
  
### Control flow  
  
```bash  
# Conditional  
if [[ -f "$FILE" ]]; then  
  echo "File exists"  
elif [[ -d "$FILE" ]]; then  
  echo "Directory"  
else  
  echo "Not found"  
fi  
  
# For loop (quote expansion)  
for file in ./*.log; do  
  gzip "$file"  
done  
  
# Read file line by line (no mangling)  
while IFS= read -r line; do  
  echo "Line: $line"  
done < input.txt  
```  
  
### Test operators  
  
| Test         | Meaning                          |  
|-------------|-----------------------------------|  
| `-f file`   | File exists and is regular file   |  
| `-d dir`    | Directory exists                  |  
| `-z "$var"` | String is empty                   |  
| `-n "$var"` | String is not empty               |  
| `$a -eq $b` | Integers equal                    |  
| `"$a" == "$b"` | Strings equal                  |  
  
### Trap / cleanup  
  
```bash  
TMPFILE="$(mktemp)"  
cleanup() { rm -f "$TMPFILE"; }  
trap cleanup EXIT INT TERM      # Auto-cleanup on exit or interrupt  
```  
  
---  
  
## Part 4: PACKAGE MANAGEMENT  
  
| OS       | Manager   | Install                        | Update All                              |  
|----------|-----------|--------------------------------|-----------------------------------------|  
| macOS    | Homebrew  | `brew install pkg`             | `brew update && brew upgrade`           |  
| Ubuntu   | apt       | `sudo apt install pkg`         | `sudo apt update && sudo apt upgrade`   |  
| Fedora   | dnf       | `sudo dnf install pkg`         | `sudo dnf upgrade`                      |  
| Python   | venv+pip  | see below                      | see below                               |  
| Node.js  | npm       | `npm install -g pkg`           | `npm update -g`                         |  
  
macOS PEP 668: Homebrew Python blocks global `pip3 install` system-wide.  
  
| Tier | Method | When | Example |  
|------|--------|------|---------|  
| 1 | `brew install` | System tools, runtimes | `brew install ffmpeg jq tesseract ollama pipx` |  
| 2 | `pipx install` | Standalone CLI Python tools | `pipx install ruff`, `pipx install httpie` |  
| 3 | `python3 -m venv` + `pip` | ML/AI stacks, project deps | mlx-lm, mlx-whisper, chromadb, torch |  
| 4 | `pip3 install --user` | Last resort, one-off library | Breaks on `brew upgrade python` — avoid |  
| ✕ | `--break-system-packages` | Never on Tahoe workstation | Throwaway containers only |  
  
```bash  
# Tier 1 — system tools via brew  
brew install ffmpeg jq pipx  
  
# Tier 2 — global CLI tools via pipx (brew install pipx first)  
pipx install ruff  
pipx install httpie  
  
# Tier 3 — ML/AI in dedicated venvs (preferred for all Python libraries)  
python3 -m venv ~/.venvs/tool  
source ~/.venvs/tool/bin/activate  
pip install --upgrade pip  
pip install <pkg>  
deactivate  
```  
  
Notes:  
- Pin Python version for ML venvs if Homebrew upgrades break wheels:  
  `/opt/homebrew/bin/python3.12 -m venv ~/.venvs/tool`  
- `pip` inside an activated venv is always safe — PEP 668 only blocks global installs.  
  
---  
  
## Part 5: AUTOMATION — launchd (macOS)  
  
**launchd vs cron (local policy):**  
  
- On **macOS Tahoe 26**, use **launchd only** for local scheduling.  
- Use `cron` only on **Linux/remote** systems where launchd is unavailable.  
  
### File locations (macOS)  
  
```bash  
~/Library/LaunchAgents/     # 🟡 Runs as you when logged in (most common)  
 /Library/LaunchAgents/     # 🟡 All users when logged in  
 /Library/LaunchDaemons/    # 🟡 System-level, even without login  
```  
  
### Basic plist template  
  
Save as `~/Library/LaunchAgents/com.yourname.jobname.plist`:  
  
```xml  
<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"  
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">  
<plist version="1.0">  
<dict>  
    <key>Label</key>  
    <string>com.yourname.jobname</string>  
  
    <key>ProgramArguments</key>  
    <array>  
        <string>/bin/bash</string>  
        <string>/Users/YOURNAME/scripts/myscript.sh</string>  
    </array>  
  
    <key>StartCalendarInterval</key>  
    <dict>  
        <key>Hour</key><integer>9</integer>  
        <key>Minute</key><integer>0</integer>  
    </dict>  
  
    <key>StandardOutPath</key>  
    <string>/Users/YOURNAME/logs/myscript.log</string>  
    <key>StandardErrorPath</key>  
    <string>/Users/YOURNAME/logs/myscript_error.log</string>  
  
    <key>RunAtLoad</key><false/>  
</dict>  
</plist>  
```  
  
### Load / test / debug  
  
```bash  
launchctl load ~/Library/LaunchAgents/com.yourname.jobname.plist          # 🟡 Register job  
launchctl start com.yourname.jobname                                      # 🟡 Trigger now for test  
launchctl list | rg com.yourname                                          # 🟢 Check status  
launchctl list com.yourname.jobname                                       # 🟢 Last exit code  
tail -f ~/logs/myscript.log                                               # 🟢 Watch output  
launchctl unload ~/Library/LaunchAgents/com.yourname.jobname.plist        # 🟡 Deactivate  
```  
  
### Scheduling options  
  
```xml  
<!-- Every Monday at 8:00 AM (Weekday 1 = Monday) -->  
<key>StartCalendarInterval</key>  
<dict>  
    <key>Weekday</key><integer>1</integer>  
    <key>Hour</key><integer>8</integer>  
    <key>Minute</key><integer>0</integer>  
</dict>  
  
<!-- Every 15 minutes -->  
<key>StartInterval</key><integer>900</integer>  
  
<!-- Run at login -->  
<key>RunAtLoad</key><true/>  
```  
  
### Example: Weekly Homebrew update (Saturday 9 AM)  
  
```bash  
cat > ~/scripts/brew_update.sh << 'EOF'  
#!/usr/bin/env bash  
set -euo pipefail  
  
LOG="$HOME/logs/brew_update.log"  
mkdir -p "$HOME/logs"  
  
{  
  echo "=== Brew Update: $(date) ==="  
  /opt/homebrew/bin/brew update  
  /opt/homebrew/bin/brew upgrade  
  /opt/homebrew/bin/brew cleanup  
  echo "Done."  
} >> "$LOG" 2>&1  
EOF  
  
chmod +x ~/scripts/brew_update.sh  
```  
  
*(Add a launchd plist pointing at this script; keep cron for Linux only.)*  
  
### cron (Linux / cross‑platform reference only)  
  
```bash  
crontab -e    # 🟡 Edit (remote Linux)  
crontab -l    # 🟢 List  
  
# MIN HOUR DOM MON DOW  command  
# 0 9 * * 1-5   /path/script.sh >> /var/log/job.log 2>&1    # Weekdays 9am  
# */15 * * * *  /path/check.sh  >> /var/log/check.log 2>&1  # Every 15 min  
  
# Always use absolute paths; redirect stdout+stderr to logs.  
```  
  
---  
  
## Part 6: SSH & REMOTE ACCESS  
  
```bash  
ssh user@hostname                              # 🟢 Connect (interactive)  
ssh -i ~/.ssh/mykey user@hostname              # 🟢 With specific key  
ssh user@server "df -h && uptime"              # 🟢 Run remote command  
  
# Copy files  
scp local_file user@server:/remote/path/       # 🟡 Copy (single file)  
rsync -avz --progress local/ user@server:/remote/   # 🟡 Large transfers, resumable  
rsync --dry-run -avz source/ dest/             # 🟢 Preview rsync actions  
  
# Tunnel (access server:3000 via localhost:8080)  
ssh -L 8080:localhost:3000 user@server         # 🟢 Local port forward  
```  
  
Key management:  
  
```bash  
ssh-keygen -t ed25519 -C "you@example.com" -f ~/.ssh/id_ed25519_name   # 🟡 Generate key  
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_name                    # 🟡 macOS Keychain  
ssh-copy-id user@hostname                                              # 🟡 Copy public key to server  
cat ~/.ssh/id_ed25519_name.pub | pbcopy                                # 🟢 Copy pubkey to clipboard  
```  
  
`~/.ssh/config`:  
  
```sshconfig  
Host myserver  
  HostName 192.168.1.100  
  User deploy  
  IdentityFile ~/.ssh/deploy_key  
  Port 22  
```  
  
---  
  
## Part 7: DOCKER ESSENTIALS  
  
```bash  
# Images  
docker pull image:tag                    # 🟡 Download image  
docker images                            # 🟢 List images  
docker rmi image_id                      # 🟡 Remove image  
  
# Containers  
docker run -d --name myapp -p 8080:80 image:tag   # 🟡 Start container  
docker ps                                        # 🟢 Running containers  
docker ps -a                                     # 🟢 All containers  
docker logs -f container                         # 🟢 Follow logs  
docker exec -it container bash                   # 🟡 Shell into container  
docker stop container && docker rm container     # 🟡 Stop + remove  
  
# Compose  
docker compose up -d                             # 🟡 Start stack  
docker compose down                              # 🟡 Stop + remove stack  
docker compose logs -f service_name              # 🟢 Logs for service  
  
# Cleanup — PREVIEW FIRST  
docker system df                                 # 🟢 Show disk usage  
# 🔴 High-risk cleanup; use sparingly and only after docker system df  
docker system prune -af                          # 🔴 Remove all unused (containers, networks, images)  
# Add -v to also remove volumes — very dangerous on shared hosts  
```  
  
---  
  
## Part 8: XARGS POWER PATTERNS  
  
Default to **null-delimited** patterns and preview first.  
  
```bash  
# Basic: run command on each line from stdin  
cat files.txt | xargs -I{} echo "Processing {}"          # 🟢 Preview  
  
# From find: null-delimited, handles spaces/newlines safely  
find . -name "*.log" -print0 | xargs -0 -I{} gzip "{}"   # 🟡 Compress logs  
  
# Parallel execution (-P = number of parallel jobs)  
find . -name "*.png" -print0 | xargs -0 -P 4 -I{} optipng "{}"   # 🟡 Parallel optimize  
```  
  
**xargs vs -exec**  
  
- Prefer `find ... -exec cmd {} +` for portable one-liners.  
- Use `xargs -0 -P` when you need parallelism and can tolerate more complexity.  
  
Dangerous patterns to avoid:  
  
- `find . -type f -name "*.tmp" -delete` — 🔴 no preview, no confirmation.  
- `find . -print0 | xargs -0 rm` — 🔴 unbounded deletion.  
  
Turn them into:  
  
```bash  
find . -type f -name "*.tmp" -print              # 🟢 Preview  
find . -type f -name "*.tmp" -print0 | xargs -0 rm -i   # 🟡 Interactive delete  
```  
  
---  
  
## Part 9: TMUX — TERMINAL SESSIONS  
  
```bash  
# Install  
brew install tmux                             # 🟡 Once per machine  
  
# Sessions  
tmux new -s research                          # 🟡 New named session  
tmux attach -t research                       # 🟢 Reattach  
tmux ls                                       # 🟢 List sessions  
tmux kill-session -t research                 # 🟡 Kill session  
```  
  
Inside tmux (prefix = `Ctrl+b`):  
  
| Action                | Keys              |  
|-----------------------|-------------------|  
| New window            | `prefix + c`      |  
| Next/prev window      | `prefix + n/p`    |  
| Split pane horizontal | `prefix + %`      |  
| Split pane vertical   | `prefix + "`      |  
| Switch pane           | `prefix + arrow`  |  
| Detach                | `prefix + d`      |  
| Kill pane             | `prefix + x`      |  
| Scroll mode           | `prefix + [` then arrows/PgUp |  
  
Minimal `~/.tmux.conf`:  
  
```bash  
set -g mouse on              # Enable mouse scrolling/clicking  
set -g history-limit 50000   # Larger scrollback  
set -g base-index 1          # Windows start at 1 not 0  
```  
  
---  
  
*Last updated: April 2026 (v4)*  
