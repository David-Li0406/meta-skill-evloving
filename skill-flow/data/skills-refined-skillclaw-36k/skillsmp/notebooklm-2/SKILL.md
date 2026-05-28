---
name: notebooklm
description: "Use the nlm CLI to talk to NotebookLM notebooks. Activate when the user mentions NotebookLM, notebook, knowledge base, or asks to chat with their notebooks."
---

# NotebookLM CLI

Use `nlm` to list notebooks, select a target, and ask questions via `generate-chat` or `chat`.

## Workflow

1) Verify CLI
   - `command -v nlm` (if missing, ask how they want to install)

2) Verify auth
   - Check `~/.nlm/env` or env vars `NLM_AUTH_TOKEN`, `NLM_COOKIES`
   - If missing, run:
     - `nlm auth --all --notebooks`
     - If profiles are locked: `NLM_USE_ORIGINAL_PROFILE=1 nlm auth --all --notebooks --debug`
   - If auth still fails, **fail fast** and ask the user to complete browser login manually

3) Select notebook
   - `nlm list` (shows recent)
   - Ask user to pick an ID if not provided

4) Interact
   - Headless single question: `nlm generate-chat <notebook-id> "<prompt>"`
   - Interactive session: `nlm chat <notebook-id>`
   - Source-based transformations: ask for source IDs, then use `summarize`, `explain`, `outline`, `faq`, `briefing-doc`, `timeline`, `toc`

5) Guardrails
   - Always confirm before destructive operations: `rm`, `rm-source`, `rm-note`, `delete-artifact`, `audio-rm`
   - Confirm before privacy-impacting actions: `share` (public) and `share-private`

## Quick commands

```bash
nlm list
nlm generate-chat <notebook-id> "Question about my knowledge base"
nlm chat <notebook-id>
```

## Notes

- If user says "talk to my knowledge base", ask which notebook ID to use.
- No implicit state: do not assume a last-used notebook.
