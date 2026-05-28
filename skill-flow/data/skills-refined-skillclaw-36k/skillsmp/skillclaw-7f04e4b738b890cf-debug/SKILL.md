---
name: debug
description: Use this skill when you need to investigate issues by examining logs, database state, and git history during manual testing or implementation.
---

# Skill body

You are tasked with helping debug issues during manual testing or implementation. This command allows you to investigate problems by examining logs, database state, and git history without editing files. Think of this as a way to bootstrap a debugging session without using the primary window's context.

## Initial Response

When invoked WITH a plan/ticket file:
```
I'll help debug issues with [file name]. Let me understand the current state.

What specific problem are you encountering?
- What were you trying to test/implement?
- What went wrong?
- Any error messages?

I'll investigate the logs, database, and git state to help figure out what's happening.
```

When invoked WITHOUT parameters:
```
I'll help debug your current issue.

Please describe what's going wrong:
- What are you working on?
- What specific problem occurred?
- When did it last work?

I can investigate logs, database state, and recent changes to help identify the issue.
```

## Environment Information

You have access to these key locations and tools:

**Logs**:
- Application logs (check project-specific locations)
- Common locations: `./logs/`, `~/.local/share/{app}/`, `/var/log/`

**Database** (if applicable):
- SQLite databases can be queried with `sqlite3`
- Check project config for database locations

**Git State**:
- Check current branch, recent commits, uncommitted changes
- Similar to how `commit` and `describe_pr` commands work

**Service Status**:
- Check running processes: `ps aux | grep {service}`
- Check listening ports: `lsof -i :{port}`

## Process Steps

### Step 1: Understand the Problem

After the user describes the issue:

1. **Read any provided context** (plan or ticket file):
   - Understand what they're implementing/testing
   - Note which phase or step they're on
   - Identify expected vs actual behavior

2. **Quick state check**:
   - Current git branch and recent commits
   - Any uncommitted changes
   - When the issue started occurring

### Step 2: Investigate the Issue

Spawn parallel Task agents for efficient investigation:

```
Task 1 - Check Recent Logs:
Find and analyze the most recent logs for errors:
1. Find latest logs: ls -t ./logs/*.log | head -1 (or project-specific location)
2. Search for errors, warnings, or issues around the problem timeframe
3. Note the working directory if shown
4. Look for stack traces or repeated errors
Return: Key errors and warnings found.
```