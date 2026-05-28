# JSON Output Structures

The `badminton-cli` tool supports a `--json` global flag for structured output. **Important**: The flag must come BEFORE the command.

```bash
badminton-cli --json <command> [options]
```

## search

Search results with fuzzy match scores.

```json
[
  {
    "player_id": "07-042475",
    "name": "Thomas Schuster",
    "score": 81.82,
    "club": "TSV 1906 Freystadt",
    "best_rank": 268,
    "best_discipline": "HM"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `player_id` | string | Unique player identifier (XX-XXXXXX format) |
| `name` | string | Player's full name |
| `score` | float | Fuzzy match score (0-100, higher = better match) |
| `club` | string | Player's club name |
| `best_rank` | int | Best ranking across all disciplines |
| `best_discipline` | string | Discipline with best ranking |

## player

Detailed player information with all discipline rankings.

```json
{
  "player_id": "01-150083",
  "first_name": "Leon",
  "last_name": "Kaschura",
  "full_name": "Leon Kaschura",
  "birth_year": 2008,
  "club": "SC Union 08 Lüdinghausen",
  "district": "NRW-Bezirk Nord 1",
  "age_class_1": "U19-2",
  "age_class_2": "U19",
  "ranking_week": "KW 2 2026",
  "rankings": [
    {
      "discipline": "HE",
      "rank": 1,
      "federation_rank": 1,
      "points": 198.256,
      "tournaments": 17,
      "age_group_rank": 1
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `player_id` | string | Unique player identifier |
| `first_name` | string | Player's first name |
| `last_name` | string | Player's last name |
| `full_name` | string | Player's full name |
| `birth_year` | int | Year of birth |
| `club` | string | Current club |
| `district` | string | German state/region |
| `age_class_1` | string | Primary age class (e.g., "U19-2") |
| `age_class_2` | string | Secondary age class (e.g., "U19") |
| `ranking_week` | string | Which ranking week this data is from |
| `rankings` | array | Array of discipline rankings |

### Rankings Array Entry

| Field | Type | Description |
|-------|------|-------------|
| `discipline` | string | Discipline code (HE/DE/HD/DD/HM/DM) |
| `rank` | int | National ranking position |
| `federation_rank` | int | Federation-level ranking |
| `points` | float | Total ranking points |
| `tournaments` | int | Number of counted tournaments |
| `age_group_rank` | int | Rank within age group (only present if `--age-rank` used) |

## compare

Comparison structure for two players (combines two player objects).

```json
{
  "player1": {
    "player_id": "01-150083",
    "first_name": "Leon",
    "last_name": "Kaschura",
    "full_name": "Leon Kaschura",
    "birth_year": 2008,
    "club": "SC Union 08 Lüdinghausen",
    "district": "NRW-Bezirk Nord 1",
    "age_class_1": "U19-2",
    "age_class_2": "U19",
    "ranking_week": "KW 2 2026",
    "rankings": [...]
  },
  "player2": {
    "player_id": "06-153539",
    "first_name": "Mats",
    "last_name": "Wohlers",
    "full_name": "Mats Wohlers",
    ...
  }
}
```

Both `player1` and `player2` have the same structure as the `player` command output.

## team

Combined points for doubles partnerships.

```json
{
  "player1": {
    "player_id": "01-150083",
    "full_name": "Leon Kaschura"
  },
  "player2": {
    "player_id": "06-153539",
    "full_name": "Mats Wohlers"
  },
  "team": [
    {
      "discipline": "HD",
      "player1_points": 126.834,
      "player2_points": 90.177,
      "team_total": 217.011
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `player1` | object | First player info (player_id, full_name) |
| `player2` | object | Second player info (player_id, full_name) |
| `team` | array | Combined points per discipline |

### Team Array Entry

| Field | Type | Description |
|-------|------|-------------|
| `discipline` | string | Doubles discipline (HD/DD/HM/DM) |
| `player1_points` | float | Player 1's points in discipline |
| `player2_points` | float | Player 2's points in discipline |
| `team_total` | float | Sum of both players' points |

## top

Array of top-ranked players.

```json
[
  {
    "rank": 1,
    "player_id": "01-150083",
    "name": "Leon Kaschura",
    "club": "SC Union 08 Lüdinghausen",
    "points": 198.256,
    "birth_year": 2008,
    "tournaments": 17,
    "discipline": "HE"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `rank` | int | National ranking position |
| `player_id` | string | Player identifier |
| `name` | string | Player name |
| `club` | string | Club name |
| `points` | float | Ranking points |
| `birth_year` | int | Year of birth |
| `tournaments` | int | Tournament count |
| `discipline` | string | Discipline code |

## graph

Historical ranking data for visualization.

```json
{
  "discipline": "HE",
  "y_axis": "rank",
  "players": [
    {
      "name": "Leon Kaschura",
      "data": [
        {
          "week": 42,
          "year": 2025,
          "label": "KW 42 2025",
          "rank": 1,
          "points": 162.975
        }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `discipline` | string | Discipline being graphed |
| `y_axis` | string | What's being tracked ("rank" or "points") |
| `players` | array | Array of player data |

### Player Data Entry

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Player name |
| `data` | array | Historical data points |

### Data Point Entry

| Field | Type | Description |
|-------|------|-------------|
| `week` | int | Week number |
| `year` | int | Year |
| `label` | string | Human-readable week label |
| `rank` | int | Rank at that week |
| `points` | float | Points at that week |

## history

List of available ranking weeks.

```json
[
  {
    "year": 2026,
    "week": 2
  },
  {
    "year": 2026,
    "week": 1
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `year` | int | Year |
| `week` | int | Week number |

Results are ordered from most recent to oldest.
