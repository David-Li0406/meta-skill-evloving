---
name: jira-cli
description: Use when querying or automating Jira - sprints, issues, epics, stories, boards, or correlating Jira data with external systems
---

> **CRITICAL:** You MUST use the Task tool with `subagent_type: "general"` to execute Jira CLI commands. NEVER run `jira` commands directly in your bash session.

Example Task invocation:
```
Task(subagent_type="general", prompt="Use jira CLI to list current sprint issues: jira sprint list --current --plain")
```

This preserves conversation context and isolates CLI output.

---

# Jira CLI

Command-line interface for Jira. **Always use `--plain` flag when available** for scriptable, parseable output.

## Default Project

Primary project: **MDBIM**. Override with `-p PROJECT` for other projects.

## Quick Reference

| Task | Command |
|------|---------|
| List my issues | `jira issue list -a$(jira me) --plain` |
| View issue | `jira issue view ISSUE-KEY --plain` |
| Create issue | `jira issue create -tTask -s"Summary" --no-input` |
| Edit issue | `jira issue edit ISSUE-KEY -s"New summary"` |
| Move/transition | `jira issue move ISSUE-KEY "In Progress"` |
| Assign issue | `jira issue assign ISSUE-KEY $(jira me)` |
| Current sprint | `jira sprint list --current --plain` |
| List epics | `jira epic list --plain` |
| Open in browser | `jira open ISSUE-KEY` |
| Who am I | `jira me` |

For detailed flags and examples, see issue-commands.md, sprint-commands.md, epic-commands.md, and other-commands.md in this skill directory.

## Global Flags

| Flag | Description |
|------|-------------|
| `-p, --project` | Project key (default: configured project) |
| `-c, --config` | Config file path |
| `--debug` | Enable debug output |
| `-h, --help` | Help for any command |

## Output Flags (for commands with `--plain`)

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output (use this!) |
| `--no-headers` | Hide table headers (with --plain) |
| `--no-truncate` | Show all columns (with --plain) |
| `--columns` | Select columns to display |
| `--raw` | Raw JSON output |
| `--csv` | CSV format output |

For board, project, release, and shell completion commands, see other-commands.md in this skill directory.
