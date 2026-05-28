---
name: mcp-quickstart
description: Quickstart guide for using the Play.fun MCP Server
metadata:
  tags: playfun, mcp, quickstart, tutorial
---

## Overview

The Play.fun MCP Server provides AI assistants with tools to interact with the Play.fun platform. It enables listing games, managing points, launching playcoins, and more.

## Authentication

### Public Tools (No credentials required)

- `list_games`, `get_game`, `get_game_leaderboard` - Browse games and leaderboards
- `list_tokens`, `get_token`, `get_token_snapshot` - Browse playcoins
- All documentation resources (`docs://`)
- All code templates (`template://`)

### Authenticated Tools (Credentials required)

- `register_game`, `update_game`, `get_my_games` - Manage your games
- `launch_playcoin`, `check_playcoin_launch_status` - Launch tokens
- `save_player_points`, `batch_save_player_points`, `get_player_points` - Track points
- `get_user_profile`, `get_user_balance`, `get_user_stats` - Account management

### Setting Up Credentials

1. Go to [https://app.play.fun](https://app.play.fun) and sign in
2. Navigate to **Creator Dashboard > Creator Credentials**
3. Add your credentials to your MCP client configuration:

```json
{
  "mcpServers": {
    "play-fun": {
      "command": "npx",
      "args": ["-y", "@anthropic/play-fun-mcp"],
      "env": {
        "x-api-key": "your-api-key",
        "x-secret-key": "your-secret-key"
      }
    }
  }
}
```

## Available Tools

### Game Management

| Tool                   | Purpose                               |
| ---------------------- | ------------------------------------- |
| `list_games`           | List games with filtering and sorting |
| `get_game`             | Get game details by UUID              |
| `register_game`        | Create a new game                     |
| `update_game`          | Modify game settings                  |
| `get_my_games`         | List your registered games            |
| `get_game_leaderboard` | Get daily leaderboard                 |

### Points Management

| Tool                       | Purpose                          |
| -------------------------- | -------------------------------- |
| `save_player_points`       | Save points for a single player  |
| `batch_save_player_points` | Save points for multiple players |
| `get_player_points`        | Get a player's current points    |
| `get_dev_leaderboard`      | Get developer leaderboard        |

### Token Operations

| Tool                           | Purpose                   |
| ------------------------------ | ------------------------- |
| `launch_playcoin`              | Launch a game token       |
| `check_playcoin_launch_status` | Check launch job status   |
| `list_tokens`                  | List all playcoins        |
| `get_token`                    | Get token by mint address |
| `get_token_snapshot`           | Get token snapshot info   |

### User & Utility

| Tool                 | Purpose                |
| -------------------- | ---------------------- |
| `get_user_profile`   | Get your account info  |
| `get_user_balance`   | Get wallet balances    |
| `get_user_stats`     | Get your statistics    |
| `get_player_rewards` | Get claimable rewards  |
| `test_connection`    | Verify API credentials |

## Available Resources

### Documentation

| Resource                 | Description                |
| ------------------------ | -------------------------- |
| `docs://system-overview` | Complete platform overview |
| `docs://server-sdk`      | Server SDK reference       |
| `docs://browser-sdk`     | Browser SDK reference      |
| `docs://authentication`  | Authentication guide       |
| `docs://api-reference`   | API endpoint reference     |
| `docs://playcoin-guide`  | Playcoin launch guide      |

### Code Templates

| Template                | Description                           |
| ----------------------- | ------------------------------------- |
| `template://server-sdk` | Server-side integration (recommended) |
| `template://vanilla-js` | Simple browser games                  |
| `template://hybrid`     | Server + Browser combined             |

## Common Workflows

### Register a New Game

```
1. Use get_user_profile to verify credentials
2. Use register_game with:
   - name: "My Game"
   - description: "Game description"
   - gameUrl: "https://mygame.com"
   - platform: "web"
   - maxScorePerSession: 1000
   - maxSessionsPerDay: 10
```

### Launch a Playcoin

```
1. Use get_my_games to find your game ID
2. Use launch_playcoin with:
   - gameId: "your-game-uuid"
   - emissionDays: 7 (or 30)
   - gameCoinSymbol: "GAME"
3. Use check_playcoin_launch_status with the returned jobId
```

### Track Player Points

```
1. Use save_player_points with:
   - gameId: "your-game-uuid"
   - playerId: "player-identifier"
   - points: 100
2. Use get_player_points to verify
3. Use get_dev_leaderboard to see rankings
```

### Check Platform Stats

```
1. Use list_games to see all games
2. Use list_tokens to see all playcoins
3. Use get_game_leaderboard for specific game rankings
```

## Testing Your Setup

Run `test_connection` to verify your credentials are working:

```
Tool: test_connection
Result: { "success": true, "userId": "..." }
```

If authentication fails, double-check your `x-api-key` and `x-secret-key` values.
