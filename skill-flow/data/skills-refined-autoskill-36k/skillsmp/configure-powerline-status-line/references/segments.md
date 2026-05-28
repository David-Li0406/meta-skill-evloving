# Powerline Segments Reference

Complete reference for all available segments and their configuration options.

## Available Segments

### directory

Shows current working directory with configurable display format.

**Configuration:**
```json
"directory": {
  "enabled": true,
  "style": "basename"
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `style` (string) - Display format:
  - `"full"` - Complete path (~/projects/claude-powerline)
  - `"fish"` - Shell-style abbreviation (~/p/claude-powerline)
  - `"basename"` - Folder name only (claude-powerline)

**Default:** basename

---

### git

Displays Git branch, status, and repository information.

**Configuration:**
```json
"git": {
  "enabled": true,
  "showSha": false,
  "showWorkingTree": false,
  "showOperation": true,
  "showTag": false,
  "showTimeSinceCommit": true,
  "showStashCount": false,
  "showUpstream": false,
  "showRepoName": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `showSha` (boolean) - Show abbreviated commit SHA
- `showWorkingTree` (boolean) - Show staged/unstaged/untracked file counts
- `showOperation` (boolean) - Show ongoing git operations (MERGE, REBASE, CHERRY-PICK)
- `showTag` (boolean) - Show nearest tag reference
- `showTimeSinceCommit` (boolean) - Show duration since last commit
- `showStashCount` (boolean) - Show number of stashed changes
- `showUpstream` (boolean) - Show upstream branch tracking information
- `showRepoName` (boolean) - Show repository name

**Default:** Only enabled, showOperation, showTimeSinceCommit, and showRepoName are true

---

### model

Shows current Claude model identifier.

**Configuration:**
```json
"model": {
  "enabled": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment

**Display:** Shows model name (e.g., "Sonnet 4.5", "Opus 4", "Haiku 3.5")

---

### metrics

Performance analytics from Claude sessions.

**Configuration:**
```json
"metrics": {
  "enabled": true,
  "showResponseTime": false,
  "showLastResponseTime": false,
  "showDuration": false,
  "showMessageCount": true,
  "showLinesAdded": true,
  "showLinesRemoved": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `showResponseTime` (boolean) - Cumulative API request duration
- `showLastResponseTime` (boolean) - Individual response timing
- `showDuration` (boolean) - Total session elapsed time
- `showMessageCount` (boolean) - Number of user messages sent
- `showLinesAdded` (boolean) - Code lines added this session
- `showLinesRemoved` (boolean) - Code lines removed this session

**Default:** messageCount, linesAdded, and linesRemoved shown

---

### context

Context window usage tracking with optional custom limits.

**Configuration:**
```json
"context": {
  "enabled": true,
  "showPercentageOnly": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `showPercentageOnly` (boolean) - Display only percentage vs. token count + percentage

**Model Context Limits (optional):**
```json
"modelContextLimits": {
  "sonnet": 1000000,
  "opus": 200000,
  "haiku": 200000
}
```

**Default:** Shows percentage only, uses default limits (200K tokens for most models)

---

### session

Real-time current conversation usage.

**Configuration:**
```json
"session": {
  "enabled": true,
  "type": "tokens",
  "costSource": "calculated"
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `type` (string) - Display format:
  - `"cost"` - USD cost only
  - `"tokens"` - Token count only
  - `"both"` - Both cost and tokens
  - `"breakdown"` - Detailed breakdown by model
- `costSource` (string) - Cost calculation method:
  - `"calculated"` - ccusage-style calculation
  - `"official"` - From hook data

**Default:** tokens, calculated

---

### block

Usage within 5-hour billing window.

**Configuration:**
```json
"block": {
  "enabled": true,
  "type": "weighted",
  "burnType": "tokens"
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `type` (string) - Display format:
  - `"cost"` - USD cost only
  - `"tokens"` - Token count only
  - `"both"` - Both cost and tokens
  - `"time"` - Time remaining in block
  - `"weighted"` - Weighted tokens (Opus = 5x, Sonnet/Haiku = 1x)
- `burnType` (string) - Burn rate display:
  - `"cost"` - Cost per hour
  - `"tokens"` - Tokens per hour
  - `"both"` - Both metrics
  - `"none"` - No burn rate

**Default:** weighted, tokens burn rate

**Note:** Weighted tokens means Opus counts 5x compared to Sonnet/Haiku in the total.

---

### today

Daily usage aggregation with budget monitoring.

**Configuration:**
```json
"today": {
  "enabled": true,
  "type": "cost"
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment
- `type` (string) - Display format:
  - `"cost"` - USD cost only
  - `"tokens"` - Token count only
  - `"both"` - Both cost and tokens
  - `"breakdown"` - Detailed breakdown by model

**Default:** cost

---

### tmux

Session and window information when running in tmux.

**Configuration:**
```json
"tmux": {
  "enabled": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment

**Display:** Shows `tmux:session-name` when in tmux session

---

### version

Claude Code application version.

**Configuration:**
```json
"version": {
  "enabled": true
}
```

**Options:**
- `enabled` (boolean) - Whether to display the segment

**Display:** Shows version number (e.g., "v1.0.81")

---

## Budget Configuration

Define spending limits and alert thresholds for session, today, and block segments.

**Configuration:**
```json
"budget": {
  "session": {
    "amount": 10.0,
    "warningThreshold": 80
  },
  "today": {
    "amount": 25.0,
    "warningThreshold": 80
  },
  "block": {
    "amount": 15.0,
    "type": "cost",
    "warningThreshold": 80
  }
}
```

**Options:**
- `amount` (number) - Numeric limit for percentage calculations
- `type` (string) - For block budget only:
  - `"cost"` - USD cost limit
  - `"tokens"` - Token count limit
- `warningThreshold` (number) - Alert threshold percentage (default: 80)

**Display Indicators:**
- 0-49% usage: Normal display
- 50-79% usage: Prefixed with `+` (moderate)
- 80%+ usage: Prefixed with `!` (warning)

---

## Line Configuration

Organize segments across multiple display lines.

**Structure:**
```json
"display": {
  "lines": [
    {
      "segments": {
        "directory": { "enabled": true },
        "git": { "enabled": true }
      }
    },
    {
      "segments": {
        "model": { "enabled": true },
        "context": { "enabled": true }
      }
    }
  ]
}
```

Each line is an object in the `lines` array with a `segments` object containing segment configurations.

**Notes:**
- Segments appear left-to-right in the order defined
- Multiple lines display vertically
- Each segment can only appear once across all lines

---

## Common Segment Combinations

### Development Focus
```json
"segments": {
  "directory": { "enabled": true, "style": "basename" },
  "git": { "enabled": true, "showOperation": true },
  "model": { "enabled": true }
}
```

### Usage Monitoring
```json
"segments": {
  "session": { "enabled": true, "type": "both" },
  "block": { "enabled": true, "type": "cost" },
  "today": { "enabled": true, "type": "cost" }
}
```

### Performance Tracking
```json
"segments": {
  "metrics": {
    "enabled": true,
    "showResponseTime": true,
    "showDuration": true,
    "showMessageCount": true
  },
  "context": {
    "enabled": true,
    "showPercentageOnly": false
  }
}
```

### Minimal
```json
"segments": {
  "directory": { "enabled": true, "style": "basename" },
  "context": { "enabled": true, "showPercentageOnly": true }
}
```
