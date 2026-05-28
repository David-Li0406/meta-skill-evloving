---
name: user-diary
description: Generate user activity diary from Claude Code history. Use when user asks to create diary, summarize activities, or when launchd triggers daily generation.
---

# User Diary - Activity History Diary

This is `{SKILL_DIR}/SKILL.md`
Scripts: `{SKILL_DIR}/scripts/`
Data: `~/.local/share/idea-storage/user-diary/`
Source: `~/.claude/history.json`

## Overview

Extracts and organizes user's daily activities from Claude Code history.json into readable diary entries.
Groups by date, categorizes activities, and creates structured diary files.

## Data Structure

```
~/.local/share/idea-storage/user-diary/
└── YYYY/
    └── YYYY-MM-DD.md
```

## History.json Location

```
~/.claude/history.json
```

## Diary Entry Format

```markdown
---
date: YYYY-MM-DD
generated: {ISO8601}
session_count: {number}
---

# YYYY-MM-DD (Day of Week)

## Sessions

### Session 1: {time} - {project/directory}
- {activity summary}
- {files touched}
- {commands run}

### Session 2: {time} - {project/directory}
...

## Summary
- Total sessions: N
- Projects worked on: [list]
- Main activities: [categories]

## Notable Events
- {anything interesting or unusual}
```

## Scripts

| Script | Description |
|--------|-------------|
| `generate.sh [date]` | Generate diary for date (default: yesterday) |
| `list.sh [-n N] [-y year]` | List diary entries |
| `read.sh <date>` | Read specific diary entry |
| `stats.sh [month]` | Show activity statistics |

## Usage

```bash
# Generate yesterday's diary
bash {SKILL_DIR}/scripts/generate.sh

# Generate specific date
bash {SKILL_DIR}/scripts/generate.sh 2026-01-15

# List recent diaries
bash {SKILL_DIR}/scripts/list.sh -n 7

# Read specific diary
bash {SKILL_DIR}/scripts/read.sh 2026-01-15
```

## Launchd Integration

Create `~/Library/LaunchAgents/com.idea-storage.user-diary.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.idea-storage.user-diary</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>~/.local/share/idea-storage/scripts/generate-user-diary.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>0</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
</dict>
</plist>
```

Load with: `launchctl load ~/Library/LaunchAgents/com.idea-storage.user-diary.plist`

## Activity Categories

When generating diary, categorize activities:

| Category | Indicators |
|----------|------------|
| Coding | Write, Edit, file changes |
| Debugging | error, fix, debug, test |
| Research | Read, Grep, Glob, web searches |
| Configuration | config, settings, env, dotfiles |
| Git | git commands, commits, PRs |
| Documentation | README, docs, comments |
