# Create / add a Terminal Space manual file

Create this as a new core file in the Terminal Lab repo, e.g. `01_Core_Terminal_Space_Warp_AI_Guide.md`. It’s just a relocation/retitle of the existing manual, not a rewrite.[^1]

```markdown
# Terminal Space Manual: Warp Terminal + Local AI Stack

> Canonical guide for running Terminal Space on macOS Tahoe (Apple Silicon) with Warp, local AI tools, and Claude Code/zsh‑ai‑assist.

## 0. Relationship to Terminal Lab

- This file is the single source of truth for:
  - Warp Terminal usage in Terminal Space.
  - Local AI tools (Ollama, MLX, MLX Whisper) from the shell.
  - Claude Code CLI and zsh‑ai‑assist usage from Warp.
- Prompting strategy, research frameworks, and Perplexity Computer / Prompt Lab workflows live in Prompt Lab, not here.
- Space instructions and safety rules in `Space_Instructions_Compact.md` apply to all commands here.

---

# Warp Terminal + Terminal Space AI Guide

## Overview

This guide shows you how to turn Warp Terminal into a reliable, AI‑augmented operations console on an Apple Silicon Mac. It covers local and cloud AI tools, safe configuration, and complete workflows for logs, meetings, research, and code.

You will learn how to install and wire the stack, run start‑to‑finish workflows, and keep performance and safety under control. The emphasis is on predictable, repeatable procedures and clear risk boundaries.

## Who this guide is for

This guide is for operators and engineers who:

- Work on an M‑series Mac and live in the terminal.
- Want to combine Warp, local models, and selected cloud tools without leaking secrets or destabilizing their machine.
- Prefer explicit procedures, risk labels, and dry‑run patterns over “magic” automation.

---

# Table of Contents

1. Overview and Goals  
1.1 What Warp Terminal is and why use it with AI  
1.2 What “Terminal Space” is and scope of this guide  
1.3 When to use local AI vs cloud AI in Warp  

2. Prerequisites and Baseline Setup  
2.1 Environment assumptions (Tahoe, hardware, OS)  
2.2 What this manual assumes from Terminal Lab  
2.3 Required CLI tools  
2.4 Baseline safety rules: risk levels and credential handling  

3. Quick Start Checklist  
3.1 Install Warp, Homebrew, and modern CLI tools  
3.2 Install core AI tools (Ollama, MLX + Whisper, Claude Code, zsh‑ai‑assist)  
3.3 Drop in the recommended `.zshrc` AI alias block  
3.4 Minimal end‑to‑end tests (logs, meetings, Claude Code)  

4. Warp Terminal Basics for this Workflow  
4.1 Installing and updating Warp on macOS  
4.2 Configuring Warp for `zsh` and Tahoe  
4.3 Warp UX features that help AI workflows (panes, blocks, command search)  
4.4 Data boundary warning for cloud AI  

5. Terminal Space Concept in Warp  
5.1 What a Space is (Terminal Lab vs Prompt Lab)  
5.2 Routing tasks: Terminal Space vs Prompt Lab  
5.3 How the AI assistant behaves inside Terminal Space  

6. AI Stack Overview in Terminal Space  
6.1 Local AI tools: Ollama, MLX, MLX Whisper  
6.2 Cloud AI tools: Claude Code, zsh‑ai‑assist  
6.3 Data‑privacy tiers and when to stay local  

7. Installing and Wiring the AI Tools  
7.1 Installing Ollama and pulling baseline models  
7.2 Installing MLX / mlx‑lm and verifying GPU use  
7.3 Setting up MLX Whisper for local transcription  
7.4 Installing Claude Code CLI and running health checks  
7.5 Installing zsh‑ai‑assist and loading it from `.zshrc`  

8. Configuring Warp + `zsh` for AI Workflows  
8.1 Recommended `.zshrc` structure for AI aliases and functions  
8.2 AI alias block (ai‑fast, ai‑think, ai‑14b, ai‑models, ai‑status, ai‑stop‑all, mlx8b, cc, etc.)  
8.3 Environment variables and API keys in `.zshenv`  
8.4 Default safety posture for new tools  

9. Using the AI Assistant Inside Warp  
9.1 Pattern: “Explain → dry‑run → execute” in Terminal Space  
9.2 Asking for one‑liners and pipelines: good vs bad prompts  
9.3 Using AI to fix failing commands and error messages  
9.4 Using AI for script generation with safety rails  

10. Warp + Claude Code Sessions  
10.1 Installing and launching Claude Code from Warp  
10.2 Core commands and session workflow  
10.3 Modes: Normal, Auto‑Accept, Plan Mode  
10.4 Rewind, checkpoints, and git  
10.5 Using MCP servers with Claude Code  
10.6 Safety: deny rules, hooks, and containment  
10.7 When to use Claude Code vs plain Warp  

11. Warp + zsh‑ai‑assist at the Prompt  
11.1 The `ai` and `??` patterns  
11.2 Generating commands, then reviewing before running  
11.3 Common zsh‑ai‑assist issues inside Warp  

12. Warp + Local Models (Ollama / MLX)  
12.1 Why use local models in Warp  
12.2 Installing and verifying Ollama  
12.3 Calling Ollama from Warp blocks  
12.4 Choosing models and context sizes by task  
12.5 Using MLX / mlx‑lm from Warp  
12.6 Resource monitoring and stability  

13. End‑to‑End AI Workflows in Warp  
13.1 Log triage: tail logs → local model → action list  
13.2 Meeting transcription: `ffmpeg` → MLX Whisper → local model summary  
13.3 Research mode: local RAG from Warp (start‑to‑finish)  
13.4 Code review with Claude Code plus local models  

14. Scheduling and Automation from Warp  
14.1 Using launchd to schedule AI jobs  
14.2 Prerequisites for the nightly Whisper job  
14.3 Safe batch scripts for Whisper, scraping, model updates  
14.4 Logging, retries, and failure handling  

15. Safety Playbook for Warp + AI  
15.1 Risk levels: read‑only, modifies state, destructive  
15.2 “Never do this” list  
15.3 AI model privacy tiers and when to stay local  
15.4 Checklists before and after an AI‑assisted session  

16. Performance and Resource Management  
16.1 Monitoring CPU, RAM, GPU from Warp  
16.2 Context windows, RAM, and unified memory  
16.3 Quantization and inference speed  
16.4 Monitoring token generation rates  
16.5 MLX GPU prioritization and tuning  
16.6 When to scale back  

17. Troubleshooting Index and Playbook  
17.1 Troubleshooting index (Ollama, Claude Code, MLX/Whisper, Warp)  
17.2 Ollama issues (hangs, OOM, wrong model, slow runs)  
17.3 MLX / Whisper issues (CPU fallback, repetitions, missing packages)  
17.4 Claude Code issues (auth, CLI, scope, hooks)  
17.5 zsh‑ai‑assist issues (plugin load, API keys)  
17.6 Warp issues (GPU/CPU load, shell integration)  

18. Extending the Setup  
18.1 Adding new AI tools and keeping configs organized  
18.2 Updating models and libraries with rollback paths  
18.3 Documenting new Warp + AI workflows in the command database  

19. Appendices  
19.1 Reference: core aliases, functions, and scripts  
19.2 Reference: Warp keybindings and layout patterns  
19.3 Reference: version policy and known‑good combos  
19.4 Version and source files  

---

# 1. Overview and Goals

## 1.1 What Warp Terminal is and why use it with AI

Warp is a GPU‑accelerated terminal for macOS that adds modern UI features (panes, blocks, searchable history) on top of your existing shell. Combined with local and cloud AI tools, Warp becomes a control surface for analysis, summarization, and code operations directly from your terminal.

## 1.2 What “Terminal Space” is and scope of this guide

Terminal Space is the Warp Space where you run shell commands, scripts, and local AI workflows. This guide only covers Terminal Space and related tools, not Prompt Lab or other Spaces.

Scope:

- Set up Warp + `zsh` + AI tools on an M‑series Mac.
- Run specific, repeatable workflows (logs, meetings, research, code).
- Keep safety, performance, and troubleshooting in one operator‑friendly manual.

<!-- From here down, inline contents are identical to Warp-Terminal-Terminal-Space-AI-Guide.md -->
```

You can now:

- Drop this file into the repo as `01_Core_Terminal_Space_Warp_AI_Guide.md`.
- Update `00_Index_and_Router_v3.md` to point “Terminal Space / AI terminal workflows” to this file.[^2][^1]

<div align="center">⁂</div>

[^1]: Warp-Terminal-Terminal-Space-AI-Guide.md

[^2]: 00_Index_and_Router_v3.md

