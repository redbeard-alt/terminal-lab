# 01_CORE_SHELL_FUNDAMENTALS
# TERMINAL LAB — SHELL FUNDAMENTALS v4
> Command anatomy, shell differences, safety patterns, debugging, environment variables, redirection, `.zshrc` management.
> Last updated: April 2026

---

## Part 1: COMMAND ANATOMY

```bash
command [options/flags] [arguments]
```

| Component | What It Does | Example |
|---|---|---|
| Command | The program, builtin, or subcommand to run | `rg`, `git`, `docker`, `cd` |
| Short flags | Single-letter options with `-` | `-l`, `-a`, `-n` |
| Long flags | Word options with `--` | `--help`, `--verbose`, `--hidden` |
| Arguments | Files, directories, strings, patterns, or targets | `~/Research`, `TODO`, `status` |
| Combined short flags | Multiple one-letter flags together | `-la`, `-xzvf` |
| End-of-options marker | Stops option parsing for filenames beginning with `-` | `rm -- -weird-file` |

**Flag patterns:**
- Boolean: `--verbose`, `--dry-run`
- Value: `--output file.txt` or `--output=file.txt`
- Negation: `--no-color`, `--no-cache`
- Subcommands: `git status`, `docker ps`, `brew services list`

**Getting help:**
```bash
command --help       # Short help
man command          # Full manual
tldr command         # Community examples (npm install -g tldr)
```

---

## Part 2: SHELL DIFFERENCES

| Feature | Bash | Zsh | PowerShell |
|---|---|---|---|
| Config file | `~/.bashrc` | `~/.zshrc` | `$PROFILE` |
| Globbing | Basic | Extended, including recursive `**/*.txt` | `Get-ChildItem -Recurse` |
| Piping passes | Text streams | Text streams | Objects |
| Auto-complete | Tab (basic) | Tab (rich, plugin-enhanced) | Tab (rich) |
| Script extension | `.sh` | `.zsh` or `.sh` | `.ps1` |

**Key zsh extras (macOS default):** `**/*.log` recursive glob · auto-correction · Oh My Zsh plugin ecosystem

**Practical notes:**
- Bash and zsh mostly share syntax, but zsh is more aggressive with globbing.
- PowerShell pipes structured objects, not text — a fundamentally different model.
- On modern macOS, assume zsh unless you explicitly switch shells.
- If a command must be portable to bash, avoid zsh-only syntax or call it out.

---

## Part 3: SAFETY PATTERNS

**Golden rules:**
1. `echo` first — prefix destructive commands with `echo` to preview
2. `-i` flag — interactive mode: `rm -i file.txt`
3. `--dry-run` — many tools support it: `rsync --dry-run`
4. `&&` not `;` — step 2 only runs if step 1 succeeds
5. Quote your variables — `"$FILE"` not `$FILE` (handles spaces)
6. Use `--` before filenames that may begin with `-`
7. Never `sudo` blindly — understand what needs root and why
8. `set -euo pipefail` — add to top of every non-trivial bash script

**Dangerous patterns:**
```bash
rm -rf $UNDEFINED_VAR/    # If var is empty → rm -rf /
dd if=/dev/zero of=/dev/sda
find . -name '*.tmp' -delete   # No preview step
xargs rm                       # Breaks on spaces in filenames
sed -i '' 's/foo/bar/g' *.txt  # Bulk in-place with no backup
```

**Safe delete workflow:**
```bash
🟢 read-only — preview
find ./project -name '*.tmp' -print
```
```bash
🟡 modifies state — delete with confirmation
find ./project -name '*.tmp' -exec rm -i -- {} +
```

**Safer alternative — Trash first:**
```bash
🟢 read-only — confirm trash is available
command -v trash && find ./project -name '*.tmp' -print
```
```bash
🟡 modifies state — move to Trash
find ./project -name '*.tmp' -exec trash -- {} +
```

**Null-safe pattern:**
```bash
find . -type f -name '*.log' -print0 | xargs -0 ls -l
```

Use `-print0` with `xargs -0` whenever filenames may contain spaces, tabs, or newlines.

**Minimal safe script header:**
```bash
#!/usr/bin/env bash
set -euo pipefail
```

- `-e` exits on command failure.
- `-u` exits on undefined variables.
- `pipefail` fails the pipeline if any step fails.

---

## Part 4: DEBUGGING COMMANDS

**When a command fails:**
1. Read the error message — usually says exactly what's wrong
2. Check exit code — `echo $?` (0 = success, non-zero = error)
3. Verbose/debug mode — add `-v`, `--verbose`, or `set -x` in scripts
4. Check permissions — `ls -la file`
5. Check if command exists — `command -v toolname`
6. Check PATH — `echo $PATH`

**Error → Fix map:**

| Error | Likely Cause | Fix |
|---|---|---|
| `command not found` | Not installed or not in PATH | `command -v tool`; install or fix PATH |
| `Permission denied` | No execute/write permission | `ls -l`; `chmod +x` or check ownership |
| `No such file or directory` | Typo or wrong path | Check with `pwd` and `ls`, use tab-complete |
| `Argument list too long` | Too many files matched by glob | Use `find -exec` or `xargs -0` |
| `Connection refused` | Service not running on port | Check service status, firewall |
| `externally-managed-environment` | Homebrew Python blocks pip (PEP 668) | Use a virtual environment |
| `broken pipe` | Downstream closed before upstream | Usually harmless; suppress with `2>/dev/null` |
| `bad substitution` | Shell syntax mismatch | Check whether command expects bash or zsh |

**Trace execution:**
```bash
zsh -x -c 'source ~/.zshrc' 2>&1 | head -50
bash -x script.sh
```

**Emergency clean shell:**
```bash
env -i "$(command -v zsh)" --no-rcs
```

Starts zsh without your config. Fastest way to prove whether `.zshrc` is causing the problem.

---

## Part 5: ENVIRONMENT VARIABLES

```bash
env                        # All env vars
echo $PATH                 # Specific var
export MY_VAR="value"      # Session only
echo 'export MY_VAR="value"' >> ~/.zshrc && source ~/.zshrc  # Permanent
```

| Variable | Purpose |
|---|---|
| `PATH` | Where shell looks for commands |
| `HOME` | User's home directory |
| `SHELL` | Current shell |
| `EDITOR` | Default text editor |
| `LANG` | Locale/language |
| `TERM` | Terminal capabilities |

---

## Part 6: REDIRECTION & FILE DESCRIPTORS

```bash
command > file.txt          # Stdout → file (overwrite)
command >> file.txt         # Stdout → file (append)
command 2> error.log        # Stderr → file
command &> all.log          # Both stdout + stderr → file
command < input.txt         # File → stdin
command > /dev/null 2>&1    # Silence all output
```

**Here document (multi-line input):**
```bash
cat <<'EOF' > config.yaml
name: myapp
version: 1.0
EOF
```

Quote the heredoc marker when you do **not** want variable expansion inside the block.

---

## Part 7: .ZSHRC MANAGEMENT

### Which Config File for What

| File | When It Runs | Use For |
|---|---|---|
| `~/.zshrc` | Every interactive shell | Aliases, functions, plugins, prompt |
| `~/.zprofile` | Login shells only | PATH, Homebrew init |
| `~/.zshenv` | Every shell (scripts too) | API keys and critical env vars |
| `~/.p10k.zsh` | Called from .zshrc | Powerlevel10k config |

**Rules:** Homebrew PATH → `~/.zprofile` · API keys → `~/.zshenv` (never `.zshrc`) · Everything else → `~/.zshrc`

---

### Recommended Block Structure

```bash
# ~/.zshrc — interactive shell config
# Last updated: [date]

# === 1. ZSH FRAMEWORK / THEME ===
source "$(brew --prefix)/opt/powerlevel10k/powerlevel10k.zsh-theme" 2>/dev/null
[ -f ~/.p10k.zsh ] && source ~/.p10k.zsh

# === 2. PLUGINS ===
[ -f ~/.zsh-ai-assist/zsh-ai-assist.plugin.zsh ] && source ~/.zsh-ai-assist/zsh-ai-assist.plugin.zsh
[ -f "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ] && source "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh"

# === 3. SHELL OPTIONS ===
setopt autocd
setopt interactive_comments

# === 4. ENVIRONMENT VARIABLES ===
export EDITOR="nano"
# API keys → ~/.zshenv, not here

# === 5. ALIASES — NAVIGATION ===
alias ..="cd .."
alias ...="cd ../.."
alias reload="source ~/.zshrc"
alias zshconfig='$EDITOR ~/.zshrc'

# === 6. ALIASES — LOCAL SHORTCUTS ===
alias notes="cd ~/Research/Notes && eza --icons"
alias research="cd ~/Research && eza --icons"

# === 7. AI TERMINAL TOOLS ===
# (Full alias set → 06_AI_Terminal Part 5)

# === 8. TOOL INIT (guarded) ===
command -v zoxide >/dev/null && eval "$(zoxide init zsh)"
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# === END ===
```

**Why this order:** Prompt and plugins load early so later aliases and inits can depend on them. Tool inits at the bottom are easy to isolate during debugging. Every optional source or init is guarded so a missing tool does not break startup.

For the full AI-terminal alias set, see **06_AI_Terminal Part 5**.

---

### Optional Terminal Lab Aliases

If you keep Terminal Lab docs in `~/Terminal-Lab`, add these to section 6:

```bash
alias t-core='cd ~/Terminal-Lab && bat 01_Core_Shell_v5.md'
alias t-store='cd ~/Terminal-Lab && bat 05_Store_Database_v5.md'
alias t-ai='cd ~/Terminal-Lab && bat 06_Tool_AI_Terminal_v5.md'
```

---

### Backup Before Every Edit

```bash
🟡 modifies state
cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d_%H%M%S)
```
```bash
🟢 read-only — list backups
ls -1t ~/.zshrc.backup.* | head
```
```bash
🟡 modifies state — restore
cp ~/.zshrc.backup.YYYYMMDD_HHMMSS ~/.zshrc && exec zsh
```

---

### Debugging a Broken .zshrc

```bash
env -i "$(command -v zsh)" --no-rcs          # Emergency clean shell
zsh -n ~/.zshrc                               # Syntax check only
zsh -x -c 'source ~/.zshrc' 2>&1 | head -50  # Trace mode
```

**Bisect method:** Comment out bottom half → reload → if OK, problem is in bottom half → repeat until bad line found.

---

### Shell Startup Performance

```bash
🟢 read-only
time zsh -i -c exit
```

If startup is slow:
```bash
🟢 read-only
zmodload zsh/zprof
zsh -i -c exit
zprof | head -40
```

Common culprits: `nvm`, `conda init`, large Oh My Zsh plugin sets, repeated `brew shellenv` calls.

---

### Quick Utilities

```bash
alias zedit='nano ~/.zshrc && source ~/.zshrc'   # Edit and reload in one step
alias aliases='alias | sort'                      # Show all aliases sorted
alias what='type -a'                              # Check if alias/function/binary
alias path='print -l -- ${(s/:/)PATH}'            # Show PATH entries one per line
```

---

## Part 8: MODERN CLI DEFAULTS

These are preferred interactive tools on the M4 workstation, not requirements.

| Task | Preferred | Classic Fallback |
|---|---|---|
| Search text | `rg` | `grep` |
| Find files | `fd` | `find` |
| List files | `eza` | `ls` |
| View files | `bat` | `cat` or `less` |
| Jump directories | `zoxide` | `cd` |
| System monitor | `btop` | `top` |

Use the modern tool first for interactive work, but know the classic fallback for portability, scripts, and remote hosts.

---

### Sensitive File Permissions

```bash
🟢 read-only — check
ls -ld ~/.ssh
ls -l ~/.zshenv
```
```bash
🟡 modifies state — fix
chmod 700 ~/.ssh
chmod 600 ~/.zshenv
```

Never pipe secrets, SSH keys, or `.zshenv` contents into any model, local or cloud.

---

*Last updated: April 2026 (v4)*

## Safety Additions — April 2026

### Dry-run gates for destructive one-liners

Before any `rm`, `find -delete`, `mv` (bulk), or `sed -i` targeting more than one file, always run the read-only equivalent first.

| Destructive | Safe preview first |
|---|---|
| `rm *.log` | `ls *.log` or `echo *.log` |
| `find . -name '*.tmp' -delete` | `find . -name '*.tmp'` (no -delete) |
| `mv src/* dst/` | `ls src/` then `echo "mv src/* dst/"` |
| `sed -i 's/old/new/g' *.md` | `grep -n 'old' *.md` first, then `perl -0pi` with backup |
| `git clean -fd` | `git clean -fdn` (dry-run flag) first |

### Glob scope rule

Never use `**/*`, `~/`, or `/` as the target of a write or delete operation. Always scope to a named subdirectory:

```bash
# WRONG
rm -rf ~/
find / -name '*.bak' -delete

# RIGHT
rm -rf ~/Projects/myproject/tmp/
find ~/Projects/myproject -name '*.bak'
```

### set -euo pipefail for every script

Every shell script that writes, moves, or deletes files must begin with:

```bash
#!/usr/bin/env bash
set -euo pipefail
trap 'echo "ERROR at line $LINENO — exiting" >&2' ERR
```

`set -e`: exit on first error. `set -u`: error on undefined variable. `set -o pipefail`: catch failures inside pipes. The `trap` prints the line number so you can find the failure fast.
