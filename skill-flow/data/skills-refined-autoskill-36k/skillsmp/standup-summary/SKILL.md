---
name: Standup Summary
description: This skill should be used when the user asks to "summarize my work", "generate standup update", "what did I do yesterday", "summarize my GitHub activity", "create work summary", "weekly summary", or needs to generate a summary of their GitHub contributions for sharing with their team.
version: 1.0.0
---

# Standup Summary

Generate a concise summary of GitHub activity (commits, pull requests, branches) across all repositories in an organization for sharing with a team.

## Arguments

This skill requires an organization name as an argument. If not provided, prompt the user for it.

## Workflow

### Step 1: Detect Day of Week

First, determine what day of the week it is using:
```bash
date +%u  # Returns 1=Monday through 7=Sunday
```

### Step 2: Gather User Preferences

Use the AskUserQuestion tool with options based on the current day of week:

**If today is Monday (day 1):**
Show time period options (header: "Time period"):
- "Friday" - Just Friday's work
- "Weekend" - Saturday and Sunday combined
- "Friday + Weekend" - All three days since last standup
- "Yesterday" - Just Sunday

**If today is any other weekday (day 2-5, Tuesday-Friday):**
Show time period options (header: "Time period"):
- "Yesterday" - Previous day's work
- "Last week" - The full previous week

**If today is Saturday or Sunday (day 6-7):**
Show time period options (header: "Time period"):
- "Yesterday" - Previous day
- "This week" - Week so far
- "Friday" - Last Friday

**Then ask summary length (header: "Length"):**
- "1-2 sentences" - Brief, high-level summary
- "1 paragraph" - More detailed with specific items mentioned

### Step 3: Calculate Date Range

GitHub interprets plain date queries in UTC, which causes timezone issues. To query dates in the user's local timezone, use ISO 8601 datetime format with timezone offset.

**First, get the timezone offset:**
```bash
TZ_OFFSET=$(date +%z)  # Returns e.g., "-0800" or "+0530"
# Format for ISO 8601: insert colon -> "-08:00" or "+05:30"
TZ_FORMATTED="${TZ_OFFSET:0:3}:${TZ_OFFSET:3:2}"
```

**For "Yesterday":**
```bash
YESTERDAY=$(date -v-1d +%Y-%m-%d)
DATE_RANGE="${YESTERDAY}T00:00:00${TZ_FORMATTED}..${YESTERDAY}T23:59:59${TZ_FORMATTED}"
```

**For "Friday":**
```bash
# Calculate based on current day
# Monday: 3 days ago, Sunday: 2 days ago, Saturday: 1 day ago
# Other days: go back to previous Friday
FRIDAY=$(date -v-friday +%Y-%m-%d)  # Adjust offset as needed
DATE_RANGE="${FRIDAY}T00:00:00${TZ_FORMATTED}..${FRIDAY}T23:59:59${TZ_FORMATTED}"
```

**For "Weekend" (Saturday + Sunday):**
```bash
SATURDAY=$(...)
SUNDAY=$(...)
DATE_RANGE="${SATURDAY}T00:00:00${TZ_FORMATTED}..${SUNDAY}T23:59:59${TZ_FORMATTED}"
```

**For "Friday + Weekend":**
```bash
FRIDAY=$(...)
SUNDAY=$(...)
DATE_RANGE="${FRIDAY}T00:00:00${TZ_FORMATTED}..${SUNDAY}T23:59:59${TZ_FORMATTED}"
```

**For "This week":**
```bash
MONDAY=$(...)  # Most recent Monday
TODAY=$(date +%Y-%m-%d)
DATE_RANGE="${MONDAY}T00:00:00${TZ_FORMATTED}..${TODAY}T23:59:59${TZ_FORMATTED}"
```

**For "Last week":**
```bash
LAST_MONDAY=$(...)  # Monday of previous week
LAST_SUNDAY=$(...)  # Sunday of previous week
DATE_RANGE="${LAST_MONDAY}T00:00:00${TZ_FORMATTED}..${LAST_SUNDAY}T23:59:59${TZ_FORMATTED}"
```

### Step 4: Query GitHub Activity

Execute the following gh CLI commands to gather activity:

**Search for commits:**
```bash
gh search commits --author=@me --owner=<org> --committer-date="${DATE_RANGE}" --json repository,sha,commit --limit 100
```

**Search for authored PRs:**
```bash
gh search prs --author=@me --owner=<org> --updated="${DATE_RANGE}" --json title,repository,state,url --limit 50
```

**Search for reviewed PRs:**
```bash
gh search prs --reviewed-by=@me --owner=<org> --updated="${DATE_RANGE}" --json title,repository,state,url --limit 50
```

Where `DATE_RANGE` is the timezone-aware range calculated in Step 3 (e.g., `2026-01-22T00:00:00-08:00..2026-01-22T23:59:59-08:00`).

### Step 5: Analyze and Summarize

Group the activity by theme or repository. Identify:
- Major features or fixes completed
- PRs merged or reviewed
- Cross-cutting themes across repos

### Step 6: Generate Summary

Format the summary based on the selected length:

**For 1-2 sentences:**
Create a single, high-level summary that captures the main themes without listing individual items. Use active voice, past tense. Start with the time period label followed by a colon.

Example format:
```
Yesterday: Fixed MQTT race conditions across firmware and backend, added real-time device info updates to the full stack, and squashed several iOS bugs.
```

**For 1 paragraph:**
Provide more detail including specific PR names, repos affected, and individual accomplishments. Still concise but comprehensive.

Example format:
```
Yesterday: Completed a major reliability improvement by fixing MQTT subscription race conditions in both the door firmware (PR #39) and cloud infrastructure (PR #78) that were causing weather data to be lost on device connect. Added real-time device info updates across the stack - new DeviceInfoUpdate message type in doma-common, backend broadcast in infra, and iOS app handling. Also fixed several iOS issues including token refresh authentication errors, device list interaction bugs, and WebRTC reconnection problems when returning from settings.
```

### Step 7: Copy to Clipboard

Use pbcopy (macOS) or equivalent to copy the final summary:
```bash
echo '<summary>' | pbcopy
```

Confirm to the user that the summary has been copied to their clipboard.

## Output Format Requirements

- Start with the time period label and colon (e.g., "Yesterday:", "Last week:", "Friday:")
- Use active voice, past tense
- No first person pronouns ("I", "my")
- No markdown formatting (plain text for Slack/chat compatibility)
- Focus on outcomes and themes, not individual commits
- Group related work together

## Example Invocation

```
User: /standup doma-home
```

This triggers the command with "doma-home" as the organization, then prompts for time period and length preferences based on the current day of week.
