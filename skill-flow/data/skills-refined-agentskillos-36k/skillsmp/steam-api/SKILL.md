---
name: steam-api
description: Steam Web API development for n8n workflows. Use when creating n8n HTTP Request nodes for Steam API, validating Steam API parameters, or building workflows with Steam player/game data. Triggers on Steam API, Steam stats, player summaries, game achievements, friend list, owned games.
---

# Steam API for n8n

## Quick Start

Base URL: `https://api.steampowered.com`

### No API Key Required
- `GetNewsForApp` - Game news
- `GetGlobalAchievementPercentagesForApp` - Achievement stats

### API Key Required (use HTTP Query Auth)
- `GetPlayerSummaries` - Player profiles
- `GetFriendList` - Friends
- `GetPlayerAchievements` - Player achievements
- `GetOwnedGames` - Owned games
- `GetRecentlyPlayedGames` - Recent games
- `GetUserStatsForGame` - Game stats

## Tools

Query API info:
```bash
node scripts/steam-api-tools.mjs list                    # List all endpoints
node scripts/steam-api-tools.mjs info <endpoint>         # Endpoint details
```

Validate & generate:
```bash
node scripts/steam-api-tools.mjs validate <endpoint> '<json>'
node scripts/steam-api-tools.mjs generate <endpoint> '<json>'
node scripts/workflow-generator.mjs validate <file.json>
```

## References

- **n8n patterns**: See [references/n8n-patterns.md](references/n8n-patterns.md)
- **API spec (raw)**: `steam-api-spec.json` in project root

## Workflow Checklist

1. Validate params with `steam-api-tools.mjs validate`
2. Use HTTP Query Auth for API key (name: `key`)
3. Steam ID format: 17 digits (e.g., `76561198128580289`)
4. `steamids` param: comma-separated, max 100
5. Check `communityvisibilitystate === 3` for public profiles
