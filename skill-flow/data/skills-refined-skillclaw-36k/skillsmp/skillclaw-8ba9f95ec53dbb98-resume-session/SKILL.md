---
name: resume-session
description: Use this skill to seamlessly restore context and resume work from a previous session.
---

# Skill body

## When To Use

- At the **start of any new conversation**
- When context seems missing
- When the user asks "what were we working on?"
- When you need to restore complete project context

## Steps to Resume Session

1. **Check Active Work**
   - List ready todos:
     ```bash
     ls todos/*-ready-*.md 2>/dev/null | head -5
     ```
   - List in-progress plans:
     ```bash
     ls plans/*.md 2>/dev/null
     ```
   - List recent solutions for context:
     ```bash
     ls -t docs/solutions/**/*.md 2>/dev/null | head -3
     ```

2. **Check Recent Git Activity**
   - View recent commits:
     ```bash
     git log --oneline -5
     ```
   - Check for uncommitted changes:
     ```bash
     git status --short
     ```

3. **Restore Project Context**
   - Follow the resume-project workflow located at `@~/.claude/ag4one/workflows/resume-project.md` to handle:
     - Project existence verification
     - Loading or reconstructing `STATE.md`
     - Detecting checkpoints and incomplete work
     - Presenting visual status
     - Offering context-aware next actions

4. **Check System Health**
   ```bash
   ./scripts/compound-dashboard.sh
   ```
   - Review health grade and recommendations before starting work.

5. **Final Summary**
   ```
   📍 Session Context:

   **Active Work:**
   - {X} ready todos waiting
   - Plan in progress: {plan name if any}

   **Recent Activity:**
   - Last commit: {subject}
   - {Changed files if uncommitted}

   **Suggested Next Steps:**
   1. {Most logical next action}
   2. {Alternative}
   ```

## Automatic Triggers

Consider running this skill when you see:
- User starts with "continue", "resume", "where were we"
- First message in a new session
- User seems to lack context