# 04_TOOL_QUICK_REFERENCE_CARD  
# TERMINAL LAB — QUICK REFERENCE CARD v4  
> Copy-paste cheat sheets. Ctrl+F friendly. macOS Tahoe 26, zsh, M4 MacBook Pro.  
> Last updated: April 2026  
  
---  
  
## RISK LEGEND  
  
- 🟢 read-only  
- 🟡 modifies state  
- 🔴 destructive or high-risk  
  
On this Space, always run the 🟢 dry-run/preview form before any 🔴 destructive command or bulk write.  
  
---  
  
## FILE OPERATIONS  
  
> Default to modern tools (`eza`, `fd`) locally. Use classic tools mainly on remote hosts, CI, or minimal containers.  
  
```bash  
eza -lah                         # 🟢 List all files, human-readable sizes  
eza -lah --sort=newest           # 🟢 Sort by modification time (newest first)  
  
fd -e txt .                      # 🟢 Find .txt files by extension  
fd pattern .                     # 🟢 Find files whose path matches 'pattern'  
  
fd . --type f --changed-before 30d  # 🟢 Files modified more than 30 days ago  
fd . --type f --size +100m       # 🟢 Files larger than 100MB  
fd . --type f --empty            # 🟢 Empty files  
fd . --type d --empty            # 🟢 Empty directories  
  
cp -R source/ dest/              # 🟡 Copy directory recursively  
mv -- old new                    # 🟡 Rename or move (protects names starting with -)  
mkdir -p path/to/nested/dir      # 🟡 Create nested directories  
ln -s /real/path /link/path      # 🟡 Create symbolic link  
  
eza --tree --level=2             # 🟢 Directory tree, 2 levels deep  
stat filename                    # 🟢 Detailed file metadata  
file filename                    # 🟢 Detect file type  
```  
  
Classic fallbacks:  
  
```bash  
ls -lah                          # 🟢 Classic listing  
find . -name "*.txt"             # 🟢 Classic file search by name  
```  
  
---  
  
## TEXT PROCESSING  
  
```bash  
bat --paging=never file.txt      # 🟢 Print entire file with syntax highlighting  
head -20 file.txt                # 🟢 First 20 lines  
tail -20 file.txt                # 🟢 Last 20 lines  
tail -f logfile.log              # 🟢 Follow log in real time  
  
wc -l file.txt                   # 🟢 Count lines  
sort -u file.txt                 # 🟢 Sort and deduplicate  
uniq -c                          # 🟢 Count consecutive duplicates  
cut -d',' -f1,3 data.csv         # 🟢 Extract columns 1 and 3  
  
diff file1.txt file2.txt         # 🟢 Compare files  
comm <(sort a.txt) <(sort b.txt) # 🟢 Compare sorted files (common/unique)  
  
jq '.' data.json                 # 🟢 Pretty-print JSON  
jq '.key' data.json              # 🟢 Extract JSON key  
```  
  
---  
  
## PROCESS MANAGEMENT  
  
```bash  
pgrep -af process_name           # 🟢 Find processes matching name/command  
ps aux | rg process_name         # 🟢 Classic: process list filtered via rg  
  
kill PID                         # 🟡 Graceful stop  
kill -9 PID                      # 🔴 Force kill (last resort)  
pkill -f "pattern"               # 🔴 Kill by pattern match (dangerous on shared boxes)  
  
lsof -i :8080                    # 🟢 What's using port 8080  
nohup command &                  # 🟡 Run in background, survive logout  
jobs && fg %1                    # 🟡 List jobs, bring job 1 to foreground  
```  
  
---  
  
## DISK & STORAGE  
  
```bash  
df -h                            # 🟢 Disk space by filesystem  
du -sh *                         # 🟢 Size of each item in current dir  
du -sh -d 1 .                    # 🟢 Subdirectory sizes (macOS)  
du -sh */ | sort -rh | head -10  # 🟢 Top 10 largest directories  
  
diskutil list                    # 🟢 List disks (macOS)  
```  
  
---  
  
## NETWORKING  
  
```bash  
ping -c 4 hostname               # 🟢 Ping 4 times  
dig example.com                  # 🟢 DNS lookup  
nc -zv hostname port             # 🟢 Test if port is open  
  
lsof -i -P -n                    # 🟢 Open connections (macOS)  
ss -tlnp                         # 🟢 Open ports (Linux)  
traceroute hostname              # 🟢 Trace network path  
```  
  
> **macOS note:** `netstat -tlnp` uses Linux flags. On macOS use `lsof -i -P -n` instead.  
  
---  
  
## REST API PATTERNS  
  
```bash  
# GET with auth  
curl -s \  
  -H "Authorization: Bearer $TOKEN" \  
  https://api.example.com/v1/resource  
  
# POST JSON  
curl -s -X POST \  
  -H "Authorization: Bearer $TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"key": "value"}' \  
  https://api.example.com/v1/resource  
  
# Upload file  
curl -s -X POST \  
  -H "Authorization: Bearer $TOKEN" \  
  -F "file=@/path/to/file.pdf" \  
  https://api.example.com/v1/upload  
  
# Parse response  
curl -s https://api.example.com/v1/resource | jq '.data.name'  
  
# Save response + print status code  
curl -s -o response.json -w "%{http_code}\n" \  
  https://api.example.com/v1/resource  
  
# Verbose (shows headers + response)  
curl -v -X GET https://api.example.com/v1/health  
  
# Paginate all pages  
page=1  
while true; do  
  result=$(curl -s "https://api.example.com/v1/items?page=$page&per_page=100" \  
    -H "Authorization: Bearer $TOKEN")  
  count=$(echo "$result" | jq '.data | length')  
  echo "$result" | jq '.data[]' >> all_items.jsonl  
  [[ $count -lt 100 ]] && break  
  ((page++))  
done  
```  
  
---  
  
## GIT OPERATIONS  
  
```bash  
git status && git log --oneline -20      # 🟢 State + recent history  
git log --graph --oneline --all          # 🟢 Visual branch graph  
  
git diff && git diff --staged            # 🟢 Unstaged + staged changes  
git stash                                # 🟡 Shelve changes  
git stash pop                            # 🟡 Restore stashed changes  
  
git branch -a                            # 🟢 All branches  
git switch -c new-branch                 # 🟡 Create + switch branch  
  
git reset --soft HEAD~1                  # 🟡 Undo last commit, keep changes staged  
git reflog                               # 🟢 Recovery tool — history of HEAD  
```  
  
Destructive cleanup/reset — always preview first:  
  
```bash  
git diff HEAD~1 --stat                   # 🟢 Preview impact before reset --hard  
git reset --hard HEAD~1                  # 🔴 Undo + discard changes  
  
git clean -fdn                           # 🟢 Preview what clean -fd would remove  
git clean -fd                            # 🔴 Remove untracked files/directories  
```  
  
---  
  
## PERMISSIONS & OWNERSHIP  
  
```bash  
chmod +x script.sh               # 🟡 Add execute bit to script  
chmod 755 script.sh              # 🟡 rwxr-xr-x  
  
chmod -R 644 directory/          # 🔴 Recursive mode change (be very sure)  
chown -R user:group directory/   # 🔴 Recursive ownership change (root-only usually)  
  
sudo !!                          # 🟡 Re-run last command with sudo  
```  
  
| Number | Permission              |  
|--------|-------------------------|  
| 7      | rwx (read + write + execute) |  
| 6      | rw- (read + write)     |  
| 5      | r-x (read + execute)   |  
| 4      | r-- (read only)        |  
  
---  
  
## COMPRESSION & ARCHIVES  
  
```bash  
tar -czf archive.tar.gz directory/      # 🟡 Create .tar.gz  
tar -xzf archive.tar.gz                 # 🟡 Extract  
tar -tf archive.tar.gz                  # 🟢 List contents without extracting  
  
zip -r archive.zip directory/           # 🟡 Create .zip  
unzip archive.zip                       # 🟡 Extract .zip  
  
gzip file.txt                           # 🟡 Compress (replaces original)  
```  
  
---  
  
## SYSTEM INFO  
  
```bash  
uname -a                         # 🟢 System info  
uptime                           # 🟢 How long running  
  
sw_vers                          # 🟢 macOS version  
sysctl -n hw.memsize             # 🟢 Total RAM in bytes (macOS)  
vm_stat | head -5                # 🟢 Memory stats (macOS)  
```  
  
---  
  
## PYTHON FROM TERMINAL  
  
```bash  
pip3 install --user package_name                      # 🟡 Safe install (PEP 668)  
python3 -m venv ~/.venvs/tools && \  
  source ~/.venvs/tools/bin/activate                  # 🟡 Create + activate venv  
  
python3 -c "import pypdf; print(pypdf.__version__)"   # 🟢 Check package version  
python3 script.py --dry-run                           # 🟢 Preview behavior if script supports it  
python3 -m http.server 8000                          # 🟡 Quick HTTP server  
```  
  
> PEP 668: Homebrew Python blocks `pip3 install` system-wide. Use `--user` or a venv. See `02_Core_Advanced.md` Part 4.  
  
---  
  
## USEFUL ONE-LINERS  
  
```bash  
openssl rand -base64 32                              # 🟢 Random password  
time command_to_benchmark                            # 🟢 Benchmark command runtime  
  
fd . --type f | wc -l                                # 🟢 Count files under current tree  
fd . --type d | wc -l                                # 🟢 Count directories  
```  
  
Safer multi-file text replacement pattern:  
  
```bash  
# 🟢 Dry-run: preview Python files and matching lines before replacement  
rg -n --glob '*.py' 'old_value' .  
  
# 🟡 Live path: script replacements with backups (run only after reviewing matches)  
python3 - <<'PY'  
from pathlib import Path  
  
for p in Path('.').rglob('*.py'):  
    s = p.read_text()  
    if 'old_value' in s:  
        backup = p.with_suffix(p.suffix + '.bak')  
        backup.write_text(s)  
        p.write_text(s.replace('old_value', 'new_value'))  
PY  
```  
  
Watch-and-build loop (no `watch` installed):  
  
```bash  
fswatch -o ./src | xargs -n1 -I{} make build        # 🟡 Rebuild on changes (macOS)  
while true; do clear; df -h; sleep 2; done          # 🟢 Simple disk-usage watcher  
```  
  
---  
  
## REGEX QUICK REFERENCE  
  
| Pattern    | Meaning                    |  
|-----------|----------------------------|  
| `.`       | Any single char            |  
| `*`       | 0+ of previous             |  
| `+`       | 1+ of previous (with `-E`) |  
| `?`       | 0 or 1 of previous         |  
| `[abc]`   | One of set                 |  
| `[^abc]`  | Not in set                 |  
| `^`       | Start of line              |  
| `$`       | End of line                |  
| `\b`      | Word boundary (with `-E`)  |  
  
```bash  
rg '^ERROR' app.log                                # 🟢 Lines starting with ERROR  
rg -o -N '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' file   # 🟢 Extract email-ish strings  
sed -E 's/\bfoo\b/bar/g' file.txt                  # 🟢 Replace whole-word in stream/output review  
```  
  
---  
  
## MODERN CLI ALTERNATIVES  
  
| Classic | Modern   | Install                    | Why                                      |  
|--------|----------|----------------------------|------------------------------------------|  
| `grep` | `rg`     | `brew install ripgrep`     | 10x faster, respects `.gitignore`        |  
| `find` | `fd`     | `brew install fd`          | Simpler, sane defaults                   |  
| `ls`   | `eza`    | `brew install eza`         | Icons, git status, colors                |  
| `cat`  | `bat`    | `brew install bat`         | Syntax highlighting, pager               |  
| `cd`   | `zoxide` | `brew install zoxide`      | Smart jump: `z research`                 |  
| `less` (.md) | `glow` | `brew install glow`    | Render Markdown nicely                   |  
| `top`  | `btop`   | `brew install btop`        | CPU/GPU/RAM/network/disk overview        |  
| `top` (M4) | `mactop` | `brew install mactop`  | Apple Silicon RAM pressure               |  
| `git` TUI | `lazygit` | `brew install lazygit` | Stage/commit/diff in one view            |  
| `less` (.csv) | `csvlens` | `brew install csvlens` | Column nav, filter                   |  
  
**Install full toolkit:**  
  
```bash  
brew install ripgrep fzf zoxide eza bat glow btop lazygit jq csvlens mactop fd yq  
brew install --cask ghostty raycast  
```  
  
**Brewfile (version-lock toolkit):**  
  
```bash  
brew bundle dump --file=~/Brewfile --force   # Save  
brew bundle --file=~/Brewfile               # Restore on new Mac  
brew bundle check --file=~/Brewfile         # Check drift  
brew pin ripgrep                            # Prevent accidental upgrade  
```  
  
---  
  
## COMMON MISTAKES & FIXES  
  
| Mistake                            | Why It Hurts                        | Fix                                       |  
|------------------------------------|-------------------------------------|-------------------------------------------|  
| `rm -rf $DIR` with unset var       | Could expand to `/`                 | Validate: `[[ -n "$DIR" ]] || exit 1`     |  
| Unquoted `$FILE`                   | Breaks on spaces/globs              | Always `"${FILE}"`                        |  
| `;` instead of `&&`                | Later steps run on failure          | Use `cmd1 && cmd2`                        |  
| `cmd file > file`                  | Truncates file before read          | Use temp file + `mv`                      |  
| `chmod 777` everywhere             | Security risk                       | Least privilege: 755 / 644                |  
| No `set -euo pipefail` in scripts  | Silent failures                     | Add at top of every non-trivial bash script |  
| No `trap` cleanup                  | Temp files left on crash            | `trap cleanup EXIT INT TERM`              |  
| `git reset --hard` w/out preview   | Irreversible                        | `git diff HEAD~1 --stat` first            |  
  
---  
  
*Last updated: April 2026 (v4)*  
