# Badminton CLI Command Reference

Complete reference for all `badminton-cli` commands and their options.

## JSON Output

The `--json` flag is a **global option** that must come BEFORE the command:

```bash
badminton-cli --json <command> [options]
```

## Command Overview

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `update` | Download ranking data from DBV | `--all`, `--force` |
| `search` | Find players by name | `--limit` |
| `player` | Show player details | `--week`, `--age-rank` |
| `compare` | Compare two players | `--week` |
| `team` | Calculate doubles partnership points | `--discipline`, `--week` |
| `top` | Show top-ranked players | `--discipline`, `--limit` |
| `graph` | Historical ranking data | `--discipline`, `--points`, `--since` |
| `history` | List available ranking weeks | (none) |

## Detailed Command Reference

### update - Download Rankings Data

Download and index ranking data from the German Badminton Association (DBV).

```bash
badminton-cli update [OPTIONS]
```

**Options:**
- `--all`: Download all historical ranking weeks (not just latest)
- `--force`: Force re-download of all files even if cached

**Usage Notes:**
- Run this command first before using any other commands
- Without `--all`, only the latest ranking week is downloaded
- Data is cached locally; use `--force` to refresh

### search - Find Players

Fuzzy search for players by name.

```bash
badminton-cli [--json] search "query" [OPTIONS]
```

**Options:**
- `--limit, -n`: Maximum results (default: 10)

**Examples:**
```bash
badminton-cli --json search "Mustermann"
badminton-cli --json search "Max" --limit 20
```

### player - Player Details

Show detailed information for a specific player.

```bash
badminton-cli [--json] player PLAYER_ID [OPTIONS]
```

**Options:**
- `--week, -w`: Specific ranking week (e.g., 'KW2', '2026-KW02')
- `--age-rank, -a`: Include rank within player's age group

**Examples:**
```bash
badminton-cli --json player 01-150083
badminton-cli --json player 01-150083 --week KW2 --age-rank
```

### compare - Compare Players

Side-by-side comparison of two players.

```bash
badminton-cli [--json] compare PLAYER_ID1 PLAYER_ID2 [OPTIONS]
```

**Options:**
- `--week, -w`: Specific ranking week

**Examples:**
```bash
badminton-cli --json compare 01-150083 01-150084
```

### team - Doubles Partnership Points

Calculate combined points for a doubles partnership.

```bash
badminton-cli [--json] team PLAYER_ID1 PLAYER_ID2 [OPTIONS]
```

**Options:**
- `--discipline, -d`: Filter to specific doubles discipline (HD, DD, HM, DM)
- `--week, -w`: Specific ranking week

**Examples:**
```bash
badminton-cli --json team 01-150083 01-150084
badminton-cli --json team 01-150083 01-150084 --discipline HM
```

### top - Top Rankings

Show top-ranked players in a discipline.

```bash
badminton-cli [--json] top [OPTIONS]
```

**Options:**
- `--discipline, -d`: Filter by discipline (HE, HD, DE, DD, HM, DM)
- `--limit, -n`: Number of results (default: 20)
- `--week, -w`: Specific ranking week
- `--age-rank, -a`: Include age-group ranks

**Examples:**
```bash
badminton-cli --json top --discipline HE --limit 20
badminton-cli --json top --discipline DE --age-rank
```

### graph - Historical Data

Get historical ranking data for trend analysis.

```bash
badminton-cli [--json] graph PLAYER_ID [PLAYER_ID...] [OPTIONS]
```

**Options:**
- `--discipline, -d`: Specific discipline
- `--points, -p`: Show points instead of rank
- `--since, -s`: Time filter ('1y', '6m', '3m')
- `--age-rank, -a`: Show age-group rank progression

**Examples:**
```bash
badminton-cli --json graph 01-150083 --discipline HE
badminton-cli --json graph 01-150083 01-150084 --discipline HE --since 6m
```

### history - Available Weeks

List all indexed ranking weeks.

```bash
badminton-cli [--json] history
```

**Examples:**
```bash
badminton-cli --json history
```

## Disciplines Reference

| Code | German | English | Type |
|------|--------|---------|------|
| HE | Herren Einzel | Men's Singles | Singles |
| DE | Damen Einzel | Women's Singles | Singles |
| HD | Herren Doppel | Men's Doubles | Doubles |
| DD | Damen Doppel | Women's Doubles | Doubles |
| HM | Herren Mixed | Mixed (male player) | Mixed |
| DM | Damen Mixed | Mixed (female player) | Mixed |

## Player ID Format

Player IDs follow the format `XX-XXXXXX` where:
- First two digits: District/state code
- Hyphen separator
- Six digit unique identifier

Example: `01-150083`

## Week Format

Ranking weeks can be specified in multiple formats:
- `KW2` - Week 2 of current year
- `2026-KW02` - Week 2 of 2026
- Full format from history output

## Error Handling

### "No data available"
Run `badminton-cli update` to download ranking data first.

### "Player not found"
- Verify player ID format (XX-XXXXXX)
- Use `search` to find the correct ID
- Player may not be in U19 rankings

### "badminton-cli: command not found"
Install with: `uv tool install badminton-cli` or `pipx install badminton-cli`
