---
name: badminton-cli
description: This skill should be used when the user asks to "search for badminton players", "find a badminton player", "show badminton rankings", "check player ranking", "compare badminton players", "find doubles partners", "show ranking history", "update badminton data", or mentions German U19 badminton, DBV rankings, or badminton player statistics. Enables interaction with the badminton-cli tool for querying German Badminton Association (DBV) U19 rankings.
---

# Badminton CLI Skill

This skill enables interaction with `badminton-cli` for querying German U19 badminton rankings from the German Badminton Association (DBV).

## Prerequisites

Before using any command, verify the tool is installed:

```bash
which badminton-cli || echo "NOT_INSTALLED"
```

If not installed, install with:

```bash
uv tool install badminton-cli
```

Or with pipx:

```bash
pipx install badminton-cli
```

## Core Principle

**Always use the `--json` global flag** when processing data programmatically. This flag must come BEFORE the command:

```bash
badminton-cli --json <command> [options]
```

## Quick Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `update` | Download ranking data | `badminton-cli update` |
| `search` | Find players by name | `badminton-cli --json search "name"` |
| `player` | Show player details | `badminton-cli --json player ID` |
| `compare` | Compare two players | `badminton-cli --json compare ID1 ID2` |
| `team` | Calculate doubles points | `badminton-cli --json team ID1 ID2` |
| `top` | Show top rankings | `badminton-cli --json top --discipline HE` |
| `graph` | Historical data | `badminton-cli --json graph ID --discipline HE` |
| `history` | List available weeks | `badminton-cli --json history` |

## Essential Commands

### Initialize Data

Run this first if data hasn't been downloaded:

```bash
badminton-cli update
```

Add `--all` for historical data:

```bash
badminton-cli update --all
```

### Search for Players

Find players using fuzzy name matching:

```bash
badminton-cli --json search "Max Mustermann"
```

Returns player IDs needed for other commands.

### Get Player Details

Show comprehensive player information:

```bash
badminton-cli --json player 01-150083
```

Add `--age-rank` for age-group ranking:

```bash
badminton-cli --json player 01-150083 --age-rank
```

### View Top Rankings

Show top players in a discipline:

```bash
badminton-cli --json top --discipline HE --limit 20
```

### Historical Trends

Get ranking progression over time:

```bash
badminton-cli --json graph 01-150083 --discipline HE --since 6m
```

## Disciplines

| Code | Name | English |
|------|------|---------|
| HE | Herren Einzel | Men's Singles |
| DE | Damen Einzel | Women's Singles |
| HD | Herren Doppel | Men's Doubles |
| DD | Damen Doppel | Women's Doubles |
| HM | Herren Mixed | Mixed (male player) |
| DM | Damen Mixed | Mixed (female player) |

## Common Workflows

### Find a Player and Show Details

1. Search by name: `badminton-cli --json search "name"`
2. Extract player ID from results
3. Get details: `badminton-cli --json player <id>`

### Compare Ranking Progression

1. Get player IDs via search
2. Query historical data: `badminton-cli --json graph <id1> <id2> --discipline HE --since 6m`
3. Analyze the data points to identify trends

### Find Optimal Doubles Partner

1. Get player's current doubles points: `badminton-cli --json player <id>`
2. Determine discipline (HD/DD for same-gender, HM/DM for mixed)
3. Query top players in complementary position
4. Calculate team points: `badminton-cli --json team <id1> <id2>`
5. Compare team totals across potential partners

### Identify Rising Stars

1. Get top 50 in discipline: `badminton-cli --json top --discipline HE --limit 50`
2. For each player, get 6-month history
3. Calculate rank improvement over time
4. Identify players with consistent upward trajectory

## Error Handling

### "No data available"

Run `badminton-cli update` to download ranking data first.

### "Player not found"

- Verify player ID format (XX-XXXXXX)
- Use `search` command to find correct ID
- Player may not be in U19 rankings

### "Command not found"

Install the tool:

```bash
uv tool install badminton-cli
```

## Additional Resources

### Reference Files

For detailed information, consult:

- **`references/commands.md`** - Complete command reference with all options
- **`references/json-structures.md`** - JSON output schemas for all commands

### Key Notes

- Player IDs follow format `XX-XXXXXX` (e.g., `01-150083`)
- Ranking weeks specified as `KW2` or `2026-KW02`
- U19 has sub-categories: U15, U17, U19
- Age-group ranks computed on-demand (can be slow for large datasets)
