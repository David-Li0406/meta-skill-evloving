---
name: ralph-loop
description: Set up and run the Ralph Loop autonomous coding loop across Windows (WSL2), macOS, and Linux. Use when asked to install or configure ralph-loop, prepare prd.json/prompt/progress files, choose or explain an agent CLI command, or run looped development tasks (long-running/overnight/by-tomorrow, "run the loop", "loop through issues"). Also trigger for Japanese asks like "明日まで進めて", "ループで開発して", "長時間のタスクをこなして" or similar.
---

# Ralph Loop

## Overview

Use this skill to bootstrap and operate the ralph-loop bash automation that drives an AI coding agent over a backlog, from setup through long-running usage.

## Workflow (Setup -> Run)

1) Identify OS and environment:
- Windows: read `references/windows-wsl.md`
- macOS: read `references/macos.md`
- Linux: read `references/linux.md`

2) Confirm prerequisites:
- Project repo exists and has tests (or note missing tests).
- `git` is available.
- The chosen agent CLI is installed and accepts stdin (see `references/agent-commands.md`).

3) Install or update ralph-loop:
- Prefer a `ralph-loop/` folder at the project root.
- If missing: `git clone https://github.com/syuya2036/ralph-loop.git ralph-loop`
- If present: `git -C ralph-loop pull --rebase`

4) Choose working branch:
- Default to the current branch; only create/switch branches if the user requests it.
- If the user says "main is fine", stay on `main`.

5) Prepare inputs:
- Edit `ralph-loop/prd.json` to define user stories.
- Tailor `ralph-loop/prompt.md` with project context and any guardrails.
- Reset or append `ralph-loop/progress.txt` as needed.

Minimal prd.json template:
```json
{
  "branchName": "feat/your-branch",
  "userStories": [
    {
      "id": "US-001",
      "title": "Describe the first story",
      "acceptanceCriteria": [
        "Define clear pass conditions",
        "Ensure tests or checks exist"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

6) Choose the agent command:
- Use a non-interactive mode so the loop can run unattended.
- If the agent does not accept stdin, create a wrapper script (see `references/agent-commands.md`).

7) Run the loop from the project root:
```bash
./ralph-loop/ralph.sh "<AGENT_CMD>" [MAX_ITERATIONS]
```

8) Monitor and resume:
- Watch `ralph-loop/progress.txt` and `ralph-loop/prd.json` for updates.
- If the loop ends early, rerun with a higher max iteration count.

## Guardrails

- Do not run the loop from inside `ralph-loop/`; run from the project root.
- Ensure `ralph.sh` is executable and has LF line endings.
- If the agent command requires complex quoting, use a wrapper script.
- For long-running requests, prefer `tmux`/`screen` or `nohup` on macOS/Linux.
- Do not delete or move files/directories unless explicitly required by the story.
- Avoid destructive git commands: no `git clean`, no `git reset --hard`, no mass-delete commands.
- Avoid `git add -A`; stage only the files you changed.
- If the loop completes immediately and output includes the prompt, the agent is echoing stdin. Use a wrapper/quiet mode or adjust the completion check so prompt text does not trigger `<promise>COMPLETE</promise>`.

## Deliverables

When finishing a request, report:
- OS path used and how ralph-loop was installed/updated
- The chosen agent command and loop settings
- Any changes made to `prd.json`, `prompt.md`, or `progress.txt`
- The branch used (confirm `main` if requested)
