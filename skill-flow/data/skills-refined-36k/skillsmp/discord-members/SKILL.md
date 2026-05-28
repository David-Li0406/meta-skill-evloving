---
name: discord-members
description: "Query existing member data, track churned members, fetch rich profiles (bio, pronouns). NOT for syncing - use discord-bot-connector:discord-bot-members to sync members."
---

# Discord Members

Member queries, churn tracking, profile management, and exports.

## ⚠️ CRITICAL: For Syncing Members

**DO NOT use this skill for syncing members.** User tokens can only see 2-10 cached members.

**For member syncing, ALWAYS use the `discord-bot-connector` plugin:**
```
Skill(skill: "discord-bot-connector:discord-bot-members")
```

If the user asks to "sync members", invoke the discord-bot skill, NOT this one.

## When to Use THIS Skill

Use this skill ONLY for:
- Querying **already synced** member data
- Rich profile fetching (bio, pronouns, connected accounts)
- Churn tracking (who left)
- Silent member detection
- Member search and export

## When to Use discord-bot Skill Instead

Use `discord-bot-connector:discord-bot-members` when:
- User asks to "sync members"
- User asks for "member list" or "get all members"
- User asks "how many members"
- Any operation that needs the complete member list

## How to Execute

**All commands below work with EXISTING synced data. To sync fresh data, use discord-bot plugin first.**

### Query existing member data:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/member_query.py new --server SERVER_ID --since 7d
```

### List churned members:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/churn_tracker.py --server SERVER_ID
```

### List silent members (never posted):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/member_query.py silent --server SERVER_ID
```

### Engagement breakdown:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/member_query.py engagement --server SERVER_ID
```

### Search members by description:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/member_query.py find "developers" --server SERVER_ID
```

### View member profile (with rich data):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/profile_fetcher.py --user USER_ID --server SERVER_ID
```

### Fetch rich profiles (batch):

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/profile_fetcher.py --server SERVER_ID --sample 50
```

### Export to CSV/JSON/Markdown:

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/member_export.py --server SERVER_ID --format csv
```

## Output Location

All paths are relative to cwd:

```
data/discord/{server_id}_{slug}/members/current.yaml
data/discord/{server_id}_{slug}/members/churned/
profiles/discord/{user_id}_{slug}.yaml
reports/discord/exports/members_{timestamp}.csv
```

## Prerequisites

- `.env` with `DISCORD_USER_TOKEN` set
- Python 3.11+ installed
- **For syncing members: Use `discord-bot-connector` plugin with `DISCORD_BOT_TOKEN`**
