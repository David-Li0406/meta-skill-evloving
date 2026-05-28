---
name: error-recovery
description: Session resumption after unexpected CLI closures. Activated automatically when .claude-state.md exists. Restores original prompt, classification, sequence and progress position. Skill-agnostic — only cares about sequence index and basic context.
priority: highest (pre-sequence execution)
triggers: always (via classifier if state file detected)
---

# Error Recovery – Crash-Resistant Session Resume

You are the persistence & resumption layer.

Goal: Let user continue exactly where they left off after CLI crash / restart.

## Rules
- File: .claude-state.md (root level, gitignored)
- Never modify other skills' behavior
- Only read/write/delete this one file
- Minimal content: prompt + class + sequence + progress pointer + key side-effects
- On resume: inject recovered state, jump to next pending step
- Cleanup: delete file on successful commit-orchestrator or explicit /clearstate

## Process (strict)

1. Classifier already detected file → CLASS: RESUME → you are first step
2. Read ".claude-state.md"
3. Parse sections (fail gracefully if malformed)
4. Show user summary of recovered state
5. Ask: Resume this session? [y/n]
   - y → output instruction to continue from next step
   - n → delete ".claude-state.md" → reply "State cleared. Normal classification will run next."
6. If resuming:
   - Inject recovered prompt + classification + sequence as context
   - Tell main loop: "Continue sequence from step N: <tool name> <arguments if any>"

## Output Format – On detection

Detected resume file: .claude-state.md

Recovered state:
- Timestamp:     <date>
- Original prompt: <first few lines or summary>
- Classification: <class>
- Sequence length: <n> steps
- Last completed: step <k> (<tool name>)
- Next step:      step <k+1> (<tool name>)
- Branch:         <branch or none>
- Modified files: <list or none>
- Pending approval: <yes/no – last question if yes>

Resume from here? [y/n]

(After user answer)

If y:
Continuing from step <k+1>: <tool> <args if known>

If n:
State file deleted. Re-classify normally.