# GitHub Monitor Skill

A Claude Code skill for managing the StayAtHomen GitHub trending projects monitoring system.

## Commands

### /gh-monitor update
Trigger a manual update of GitHub data.

**What it does:**
- Fetches latest trending and popular repositories from GitHub API
- Updates the local database with new data
- Creates new snapshots for tracking growth

**Example:**
```
/gh-monitor update
```

### /gh-monitor status
Check the current status of the monitoring system.

**What it does:**
- Shows total number of repositories being tracked
- Displays last update time
- Shows backend server status

**Example:**
```
/gh-monitor status
```

### /gh-monitor rankings [type]
View different types of rankings.

**Parameters:**
- `type` (optional): Type of ranking to view
  - `star-growth`: Star增长最快榜单
  - `hot-trending`: 热度最高榜单 (default)
  - `fork-growth`: Fork增长最快榜单
  - `new-projects`: 新项目榜单

**Example:**
```
/gh-monitor rankings star-growth
```

### /gh-monitor stats
View statistics about tracked repositories.

**What it does:**
- Shows language distribution
- Shows topic distribution
- Displays overall statistics

**Example:**
```
/gh-monitor stats
```

### /gh-monitor start
Start the backend server and frontend development server.

**Example:**
```
/gh-monitor start
```

### /gh-monitor stop
Stop the running servers.

**Example:**
```
/gh-monitor stop
```

## Installation

This skill is automatically available in the StayAtHomen project directory.

## Requirements

- Node.js 18+
- GitHub Personal Access Token (for API access)
- Backend and frontend dependencies installed
