# Design Ops Freshness System Guide

> Keeping Design Ops current with agentic engineering developments

---

## Overview

The Freshness System ensures Design Ops stays aligned with the latest developments in agentic engineering. It uses a hybrid approach:

- **Bash scripts**: Handle scheduling, file I/O, source health checks
- **Claude Code**: Performs research, validation, and analysis via `/design freshness`

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRESHNESS SYSTEM                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────────┐   │
│  │   launchd    │──────│ run-monthly  │────▶│ Notification │   │
│  │  (1st/month) │      │     .sh      │     │   (MacOS)    │   │
│  └──────────────┘      └──────────────┘     └──────────────┘   │
│                               │                                  │
│                               ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     Pre-gathered Context                  │   │
│  │  • scan-design-ops.sh → current-state.md                 │   │
│  │  • check-source-health.sh → source-health-YYYY-MM.md     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                               │                                  │
│                               ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              /design freshness (Claude Code)              │   │
│  │                                                           │   │
│  │  1. Load pre-gathered context                            │   │
│  │  2. Research landscape (web search)                      │   │
│  │  3. Validate against Anthropic-anchored framework        │   │
│  │  4. Generate impact analysis                             │   │
│  │  5. Create prioritized action plan                       │   │
│  │  6. Update dashboard                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Quick Install

```bash
cd /path/to/DesignOps
./tools/freshness/install.sh
```

This will:
1. Create directory structure in `docs/freshness/`
2. Initialize source registry in `config/source-registry.yaml`
3. Install launchd plist for monthly reminders (1st of month at 10:00 AM)
4. Run initial state scan
5. Create dashboard

### Manual Installation

If you prefer to install components individually:

```bash
# Create directories
mkdir -p docs/freshness/{discoveries,validated,impact,actions,reports,trends}

# Run initial scan
./tools/freshness/scan-design-ops.sh --output docs/freshness/current-state.md

# Check source health
./tools/freshness/check-source-health.sh
```

## Usage

### Monthly Workflow (Recommended)

1. **Receive notification** (1st of month at 10:00 AM)
2. **Open Claude Code** in Design Ops directory
3. **Run freshness check**:
   ```
   /design freshness full
   ```
4. **Review generated artifacts** in `docs/freshness/`
5. **Implement high-priority actions**

### Quick Check

For a rapid freshness assessment without full research:

```
/design freshness quick
```

### Manual Trigger

Run the monthly process manually:

```bash
./tools/freshness/run-monthly.sh
```

## Directory Structure

```
DesignOps/
├── config/
│   ├── source-registry.yaml      # Tracked sources with tiers
│   └── .last-freshness-scan      # Date of last scan
│
├── docs/freshness/
│   ├── dashboard.md              # Current status overview
│   ├── current-state.md          # Design Ops inventory
│   ├── freshness-context-YYYY-MM.md  # Monthly context files
│   ├── source-health-YYYY-MM.md  # Source health reports
│   │
│   ├── discoveries/              # New developments found
│   │   └── YYYY-MM-DD-*.md
│   │
│   ├── validated/                # Verified developments
│   │   └── YYYY-MM-DD-*.md
│   │
│   ├── impact/                   # Impact assessments
│   │   └── YYYY-MM-DD-*.md
│   │
│   ├── actions/                  # Action plans
│   │   └── YYYY-MM-DD-*.md
│   │
│   ├── reports/                  # Full monthly reports
│   │   └── YYYY-MM-report.md
│   │
│   └── trends/                   # Pattern analysis
│       └── YYYY-Q#-trends.md
│
└── tools/freshness/
    ├── install.sh                # Install system
    ├── uninstall.sh              # Remove system
    ├── run-monthly.sh            # Monthly orchestrator
    ├── scan-design-ops.sh        # State scanner
    ├── check-source-health.sh    # Source validator
    └── send-notification.sh      # MacOS notifications
```

## Source Registry

### Tier Structure

| Tier | Description | Validation |
|------|-------------|------------|
| **Tier 1** | Anthropic Official | Always trusted (docs, cookbook, blog) |
| **Tier 2** | Validated Sources | Proven reliable, tracked decay |
| **Tier 3** | Watching | Potential, not yet validated |
| **Archived** | Previously valid | Stale or deprecated |

### Source Validation Framework

Each source is scored on:

| Criterion | Range | Description |
|-----------|-------|-------------|
| Anthropic Alignment | 0-3 | How well it aligns with official Anthropic guidance |
| Community Traction | 0-3 | Adoption and peer validation |
| Design Ops Fit | 0-3 | Relevance to Design Ops scope |
| Freshness | 0-1 | Recency of information |

**Threshold**: Combined score ≥7 for Tier 2 promotion

### Decay Mechanism

Tier 2 sources lose reliability over time without revalidation:
- Default decay: 0.5 points/month
- Sources dropping below 5 are flagged for review
- Sources dropping below 3 are archived

## Validation Process

### Research Query Structure

The freshness check uses a semi-dynamic query:

```
What are the most significant developments in agentic AI engineering
since [LAST_SCAN_DATE]?

Focus areas:
1. Anthropic official updates (docs, cookbook, blog, research)
2. MCP (Model Context Protocol) ecosystem changes
3. Claude Code feature updates and best practices
4. Agentic workflow patterns gaining traction

For each development:
- Source with URL
- Publication/discovery date
- Key insight or change
- Relevance to building AI-assisted systems

Exclude: General LLM news, non-Anthropic model releases, speculative content
```

### Anthropic-Anchored Validation

All findings are validated against:

1. **Does Anthropic documentation support this?**
2. **Does the Anthropic Cookbook demonstrate this pattern?**
3. **Has Anthropic research discussed this approach?**
4. **Is this consistent with Claude's known capabilities?**

## Uninstallation

### Full Removal

```bash
./tools/freshness/uninstall.sh
```

### Keep Data

```bash
./tools/freshness/uninstall.sh --keep-data
```

This removes the launchd schedule but preserves freshness data.

## Troubleshooting

### Notification Not Appearing

1. Check System Preferences → Notifications → Script Editor
2. Verify launchd is loaded:
   ```bash
   launchctl list | grep designops
   ```

### Launchd Not Running

Reload the plist:
```bash
launchctl unload ~/Library/LaunchAgents/com.designops.freshness.plist
launchctl load ~/Library/LaunchAgents/com.designops.freshness.plist
```

### Source Health Check Failing

- Verify network connectivity
- Check if `yq` is installed for YAML parsing:
  ```bash
  brew install yq
  ```

### View Logs

```bash
tail -f ~/Library/Logs/design-ops-freshness.log
```

## Best Practices

1. **Run freshness check within 3 days of notification** — Context stays relevant
2. **Review dashboard before full check** — Know current state
3. **Document validation reasoning** — Future you will thank you
4. **Archive aggressively** — Better to re-validate than trust stale sources
5. **Track implementation** — Use action plans as checklists

---

_Part of Design Ops v2.0 — Self-Maintaining AI Operations Infrastructure_
