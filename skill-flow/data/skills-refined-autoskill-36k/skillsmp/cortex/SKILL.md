---
name: cortex
description: Workspace intelligence layer - aggregates communications across all channels into a single queryable event store
homepage: https://github.com/Napageneral/cortex
metadata: {"nexus":{"emoji":"🧠","os":["darwin","linux"],"requires":{"bins":["cortex"]},"install":[{"id":"brew","kind":"brew","formula":"Napageneral/tap/cortex","bins":["cortex"],"label":"Install via Homebrew"},{"id":"go","kind":"shell","script":"go install github.com/Napageneral/cortex/cmd/cortex@latest","bins":["cortex"],"label":"Install via Go"}]}}
---

# Cortex — Workspace Intelligence Layer

Cortex aggregates your communications across all channels (iMessage, Gmail, Slack, AI sessions, etc.) into a single queryable event store with identity resolution.

## Why Cortex?

Your communications are fragmented:
- iMessage threads with some people
- Email conversations with others
- Slack for work
- AI chat sessions in Cursor

Cortex unifies them into one data layer, so you can ask:
- "What did I discuss with Dad across ALL channels?"
- "Show me everything related to the HTAA project"
- "Who have I communicated with most this year?"

## Quick Start

```bash
# Initialize
cortex init

# Configure your identity
cortex me set --name "Tyler Brandt" --phone "+17072876731" --email "tnapathy@gmail.com"

# Connect adapters (requires Eve and gogcli installed)
cortex connect imessage
cortex connect gmail --account tnapathy@gmail.com

# Sync all channels
cortex sync

# Query
cortex events --person "Dad" --since "2025-01-01"
cortex people --top 20
```

## Commands

### Setup

| Command | Description |
|---------|-------------|
| `cortex init` | Initialize config and event store |
| `cortex me set --name "..." --phone "..." --email "..."` | Configure your identity |
| `cortex connect <adapter>` | Configure a channel adapter |
| `cortex adapters` | List configured adapters |

### Sync

| Command | Description |
|---------|-------------|
| `cortex sync` | Sync all enabled adapters |
| `cortex sync imessage` | Sync specific adapter (positional) |
| `cortex sync --adapter imessage` | Sync specific adapter |
| `cortex sync --full` | Force full re-sync |

### Query

| Command | Description |
|---------|-------------|
| `cortex events` | List events with filters |
| `cortex events --person "Dad"` | Filter by person |
| `cortex events --channel imessage` | Filter by channel |
| `cortex events --since 2025-01-01` | Filter by date |
| `cortex people` | List all people |
| `cortex people --top 20` | Top contacts by event count |
| `cortex people "Dad"` | Show person details |
| `cortex timeline 2026-01` | Events in time period |
| `cortex timeline --today` | Today's events |
| `cortex db query <sql>` | Raw SQL access |

### Identity Management

| Command | Description |
|---------|-------------|
| `cortex identify` | List all people + identities |
| `cortex identify --merge "Person A" "Person B"` | Merge two people |
| `cortex identify --add "Dad" --email "dad@example.com"` | Add identity |

### Tags

| Command | Description |
|---------|-------------|
| `cortex tag list` | List all tags |
| `cortex tag add --event <id> --tag "project:htaa"` | Tag an event |
| `cortex tag add --filter "person:Dane" --tag "context:business"` | Bulk tag |

## Adapters

### iMessage (via Eve)

Prerequisites:
```bash
brew install Napageneral/tap/eve
eve init && eve sync
```

Connect:
```bash
cortex connect imessage
```

### Gmail (via gogcli)

Prerequisites:
```bash
brew install steipete/tap/gogcli
gog auth add your@gmail.com
```

Connect:
```bash
cortex connect gmail --account your@gmail.com
```

### AI Sessions (via aix)

Connect:
```bash
cortex connect cursor
```

### X/Twitter (via bird)

Prerequisites:
```bash
brew install steipete/tap/bird
bird check  # Verify auth via Chrome cookies
```

Connect:
```bash
cortex connect x
```

Syncs: bookmarks, likes, mentions

## Output Formats

All commands support `--json` / `-j`:

```bash
cortex events --json | jq '.events[] | select(.channel == "imessage")'
cortex people --top 10 --json
```

## Configuration

Config: `~/.config/cortex/config.yaml`

```yaml
me:
  canonical_name: "Tyler Brandt"
  identities:
    - channel: imessage
      identifier: "+17072876731"
    - channel: email
      identifier: "tnapathy@gmail.com"

adapters:
  imessage:
    type: eve
    enabled: true
  gmail:
    type: gogcli
    enabled: true
    account: tnapathy@gmail.com
```

Data: `~/Library/Application Support/Cortex/cortex.db`

## Bootstrap (for AI agents)

```bash
# Check if installed
which cortex && cortex version

# Install
brew install Napageneral/tap/cortex
# OR: go install github.com/Napageneral/cortex/cmd/cortex@latest

# Setup
cortex init

# Configure identity
cortex me set --name "User Name" --email "user@example.com"

# Connect adapters (assumes Eve/gogcli already set up)
cortex connect imessage
cortex connect gmail --account user@gmail.com

# Sync
cortex sync

# Verify
cortex db query "SELECT COUNT(*) as count FROM events"
cortex people --top 5
```

## Event Schema

Events have these core properties:
- `id` — Unique identifier
- `timestamp` — When it happened
- `channel` — imessage, gmail, slack, cursor, etc.
- `content_types` — ["text"], ["text", "image"], etc.
- `direction` — sent, received, observed
- `participants` — People involved (resolved via identity)

Queryable via:
```bash
cortex db query "SELECT * FROM events WHERE channel = 'imessage' LIMIT 10"
```

## Tips for Agents

1. Use `cortex people --top 10` to understand who the user communicates with most
2. Use `cortex events --person "Name"` to get context on a relationship
3. Use `cortex timeline --today` for recent activity
4. Filter by channel to focus on specific contexts
5. Use `--json` output for programmatic access
6. Raw SQL via `cortex db query` for complex queries

Example agent workflow:
```bash
# "Tell me about my communication with Dad"
cortex people "Dad"                              # Get identity info
cortex events --person "Dad" --since 2025-01-01  # Recent events
cortex db query "SELECT channel, COUNT(*) FROM events e
  JOIN event_participants ep ON e.id = ep.event_id 
  JOIN persons p ON ep.person_id = p.id 
  WHERE p.display_name = 'Dad' 
  GROUP BY channel"                             # Channel breakdown
```
