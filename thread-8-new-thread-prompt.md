# Thread 8 — New Thread Opening Prompt

Paste this verbatim into the new thread alongside the attached `thread-8-context.md`:

---

```
Context: research-agent (redbeard-alt/research-agent) is the third of three AI
agents being aligned to AGENT_SPEC.md (canonical at redbeard-alt/terminal-lab/AGENT_SPEC.md).
audio-agent and newsletter-agent are already 🟢 compliant. This thread closes
the final compliance work on research-agent.

See attached: thread-8-context.md — full state, verified import map, ready-to-paste
Copilot prompts for both PRs, and quick-start steps.

Task: Drive research-agent to 🟢 compliant status.

Step 1 — Verify current state on main:
- List redbeard-alt/research-agent root
- Confirm agent/ still exists
- Confirm cli.py still imports `from agent import X`
- Confirm requirements.txt still uses >= ranges

Step 2 — Queue Copilot PR A (package rename + _paths.py + imports + CLAUDE.md).
Use the exact prompt provided in thread-8-context.md.

Step 3 — When PR A is ready, review:
- All 14 files moved to research_agent/
- agent/ directory deleted
- `from agent` returns no grep hits
- _paths.py exists with the template
- CLAUDE.md references rewritten

Step 4 — Merge PR A.

Step 5 — Queue Copilot PR B (requirements.txt pinning) using the prompt
in thread-8-context.md. Do NOT queue B before A merges (avoids merge conflicts).

Step 6 — Merge PR B.

Step 7 — Update terminal-lab/AGENT_SPEC.md:
- §9 row: research-agent → 🟢 compliant
- §10 research-agent checklist: tick all items
- Note in commit message that the original §10 checklist was stale (FAISS
  migration was unnecessary, CLAUDE.md was already present)

After Step 7, all three agents (audio-agent, newsletter-agent, research-agent)
are 🟢 compliant. Project complete.

Constraints:
- One PR per logical change. Do not bundle.
- Push directly only for deterministic <5-line edits.
- For anything requiring import rewrites or multi-file coordination, use Copilot.
```
