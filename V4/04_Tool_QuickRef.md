# 04_TOOL_QUICK_REFERENCE_CARD
# TERMINAL LAB — QUICK REFERENCE CARD v3
> Copy-paste cheat sheets. Ctrl+F friendly.
> Last updated: March 2026

---

## FILE OPERATIONS

```bash
ls -lah                          # All files, human-readable sizes
ls -lt                           # Sort by modification time (newest first)
find . -name "*.txt"             # Find files by name
find . -type f -mtime +30        # Modified more than 30 days ago
find . -size +100M               # Larger than 100MB
find . -empty                    # Empty files and directories
cp -r source/ dest/              # Copy directory recursively
mv old new                       # Rename or move
mkdir -p path/to/nested/dir      # Create nested directories
ln -s /real/path /link/path      # Create symbolic link
tree -L 2                        # Directory tree, 2 levels deep
stat filename                    # Detailed file metadata
file filename                    # Detect file type
```

---

## TEXT PROCESSING

```bash
cat file.txt                     # Print entire file
head -20 file.txt                # First 20 lines
tail -20 file.txt                # Last 20 lines
tail -f logfile.log              # Follow log in real-time
wc -l file.txt                   # Count lines
sort -u file.txt                 # Sort and deduplicate
uniq -c                          # Count consecutive duplicates
cut -d',' -f1,3 data.csv         # Extract columns 1 and 3
diff file1.txt file2.txt         # Compare files
comm <(sort a.txt) <(sort b.txt) # Compare sorted files (common/unique)
jq '.' data.json                 # Pretty-print JSON
jq '.key' data.json              # Extract JSON key
```

---

## PROCESS MANAGEMENT

```bash
ps aux | grep process_name       # Find specific process
kill PID                         # Graceful stop
kill -9 PID                      # Force kill
pkill -f "pattern"               # Kill by pattern match
lsof -i :8080                    # What's using port 8080
nohup command &                  # Run in background, survive logout
jobs && fg %1                    # List jobs, bring job 1 to foreground
```

---

## DISK & STORAGE

```bash
df -h                            # Disk space by filesystem
du -sh *                         # Size of each item in current dir
du -sh -d 1 .                    # Subdirectory sizes (macOS)
du -sh */ | sort -rh | head -10  # Top 10 largest directories
diskutil list                    # List disks (macOS)
```

---

## NETWORKING

```bash
ping -c 4 hostname               # Ping 4 times
dig example.com                  # DNS lookup
nc -zv hostname port             # Test if port is open
lsof -i -P -n                    # Open connections (macOS)
ss -tlnp                         # Open ports (Linux)
traceroute hostname               # Trace network path
```

> **macOS note:** `netstat -tlnp` uses Linux flags. Use `lsof -i -P -n` instead.

---

## REST API PATTERNS

```bash
# GET with auth
curl -s -H "Authorization: Bearer $TOKEN" https://api.example.com/v1/resource

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
curl -s https://api.example.com/v1/resource | jq '.data[0].name'

# Save response + print status code
curl -s -o response.json -w "%{http_code}" https://api.example.com/v1/resource

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
git status && git log --oneline -20      # State + recent history
git log --graph --oneline --all          # Visual branch graph
git diff && git diff --staged            # Unstaged + staged changes
git stash && git stash pop               # Shelve and restore
git branch -a                            # All branches
git checkout -b new-branch               # Create + switch branch
git reset --soft HEAD~1                  # Undo last commit, keep staged
git reflog                               # Recovery tool — history of HEAD

# 🔴 Destructive — preview first:
git diff HEAD~1 --stat                   # 🟢 Preview before reset --hard
git reset --hard HEAD~1                  # 🔴 Undo + discard changes
git clean -fdn                           # 🟢 Preview before clean -fd
git clean -fd                            # 🔴 Remove untracked files/dirs
```

---

## PERMISSIONS & OWNERSHIP

```bash
chmod +x script.sh               # Add execute
chmod 755 script.sh              # rwxr-xr-x
chmod -R 644 directory/          # Set recursively
chown -R user:group directory/   # Recursive ownership change
sudo !!                          # Re-run last command with sudo
```

| Number | Permission |
|---|---|
| 7 | rwx (read + write + execute) |
| 6 | rw- (read + write) |
| 5 | r-x (read + execute) |
| 4 | r-- (read only) |

---

## COMPRESSION & ARCHIVES

```bash
tar -czf archive.tar.gz directory/      # Create .tar.gz
tar -xzf archive.tar.gz                 # Extract
tar -tf archive.tar.gz                  # List contents without extracting
zip -r archive.zip directory/           # Create .zip
unzip archive.zip                       # Extract .zip
gzip file.txt                           # Compress (replaces original)
```

---

## SYSTEM INFO

```bash
uname -a                         # System info
uptime                           # How long running
sw_vers                          # macOS version
sysctl -n hw.memsize             # Total RAM in bytes (macOS)
vm_stat | head -5                # Memory stats (macOS)
```

---

## PYTHON FROM TERMINAL

```bash
pip3 install --user package_name                      # Safe install (PEP 668)
python3 -m venv ~/.venvs/tools && source ~/.venvs/tools/bin/activate  # Venv
python3 -c "import pypdf; print(pypdf.__version__)"  # Check package version
python3 script.py --dry-run                           # Preview before execute
python3 -m http.server 8000                           # Quick HTTP server
```

> PEP 668: Homebrew Python blocks `pip3 install` system-wide. Use `--user` or venv. See `02_Core Part 4`.

---

## USEFUL ONE-LINERS

```bash
openssl rand -base64 32                              # Random password
time command_to_benchmark                            # Benchmark
find . -type f | wc -l                               # Count files
find . -name "*.py" -exec sed -i '' 's/old/new/g' {} +  # Replace in files (macOS)
fswatch -o ./src | xargs -n1 -I{} make build        # Watch for changes (macOS)
while true; do clear; df -h; sleep 2; done          # Watch command (no watch installed)
```

---

## REGEX QUICK REFERENCE

| Pattern | Meaning |
|---|---|
| `.` | Any single char |
| `*` | 0+ of previous |
| `+` | 1+ of previous (grep -E) |
| `?` | 0 or 1 of previous |
| `[abc]` | One of set |
| `[^abc]` | Not in set |
| `^` | Start of line |
| `$` | End of line |
| `\b` | Word boundary (grep -E) |

```bash
grep '^ERROR' app.log                              # Lines starting with ERROR
grep -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' file  # Email-ish strings
sed -E 's/\bfoo\b/bar/g' file.txt                 # Replace whole-word
```

---

## MODERN CLI ALTERNATIVES

| Classic | Modern | Install | Why |
|---|---|---|---|
| `grep` | `rg` | `brew install ripgrep` | 10x faster, ignores .git |
| `find` | `fd` | `brew install fd` | Simpler, ignores .git |
| `ls` | `eza` | `brew install eza` | Icons, git status, colors |
| `cat` | `bat` | `brew install bat` | Syntax highlighting, pager |
| `cd` | `zoxide` | `brew install zoxide` | Smart jump: `z research` |
| `less` (.md) | `glow` | `brew install glow` | Renders Markdown |
| `top` | `btop` | `brew install btop` | CPU/GPU/RAM/network/disk |
| `top` (M4) | `mactop` | `brew install mactop` | Apple Silicon RAM pressure |
| `git` TUI | `lazygit` | `brew install lazygit` | Stage/commit/diff in one view |
| `less` (.csv) | `csvlens` | `brew install csvlens` | Column nav, filter |

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

| Mistake | Why It Hurts | Fix |
|---|---|---|
| `rm -rf $DIR` with unset var | Expands to `rm -rf /` | Validate: `[[ -n "$DIR" ]] \|\| die` |
| Unquoted `$FILE` | Breaks on spaces/globs | Always `"$FILE"` |
| `;` instead of `&&` | Later steps run on failure | Use `cmd1 && cmd2` |
| `cmd file > file` | Truncates file before read | Use temp file + mv |
| `chmod 777` everywhere | Security risk | Least privilege: 755/644 |
| No `set -euo pipefail` | Silent failures | Add at top of every bash script |
| No `trap` cleanup | Temp files left on crash | `trap cleanup EXIT INT TERM` |
| `git reset --hard` without preview | Irreversible | `git diff HEAD~1 --stat` first |

---

*Last updated: March 2026 (v3)*
