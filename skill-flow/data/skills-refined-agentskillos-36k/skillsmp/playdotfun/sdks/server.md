---
name: sdk-server
description: Server SDK reference for Play.fun - recommended for production games
metadata:
  tags: playfun, sdk, server, reference, docs
---

## Overview

The Server SDK (`@playfun/server-sdk`) is the **recommended** way to integrate with Play.fun for production games. It handles HMAC authentication automatically and provides secure server-side point tracking.

## When to Use

| Use Server SDK                          | Use Browser SDK Instead             |
| --------------------------------------- | ----------------------------------- |
| Production games with token rewards     | Quick prototypes                    |
| Games where cheating prevention matters | "Vibe coded" simple games           |
| When you need to validate scores        | Game jam entries                    |
| Any game with real value at stake       | Demos where accuracy doesn't matter |

## Architecture

```
Browser Game → Your Server (validates) → Server SDK → Play.fun API
```

## Installation

```bash
npm install @playfun/server-sdk
```

## Initialize Client

```typescript
import { OpenGameClient } from '@opusgamelabs/server-sdk';

const client = new OpenGameClient({
  apiKey: process.env.OGP_API_KEY!,
  secretKey: process.env.OGP_API_SECRET_KEY!,
});
```

## Games API

### List Games

```typescript
const { items } = await client.games.get({
  limit: 50,
  query: 'search term',
});
```

### Get Game by ID

```typescript
const game = await client.games.getById({ gameId: 'your-game-uuid' });
```

### Register a New Game

```typescript
const game = await client.games.register({
  name: 'My Game', // required
  description: 'An awesome game', // required
  gameUrl: 'https://mygame.com', // required
  platform: 'web', // web|ios|android|steam|itch
  // Optional anti-cheat limits (recommended):
  maxScorePerSession: 1000,
  maxSessionsPerDay: 10,
  maxCumulativePointsPerDay: 5000,
});

console.log('Game ID:', game.id);
```

### Update a Game

```typescript
await client.games.update({
  gameId: 'your-game-uuid',
  name: 'New Name',
  maxScorePerSession: 2000,
});
```

## Points API

### Save Points (Single Player)

```typescript
await client.play.savePoints({
  gameId: 'your-game-uuid',
  playerId: 'player-123',
  points: 100,
});
```

### Batch Save Points (Multiple Players)

```typescript
await client.play.batchSavePoints({
  gameId: 'your-game-uuid',
  pointsRecord: {
    'player-1': 100,
    'player-2': 250,
    'player-3': 75,
  },
});
```

### Get Player Points

```typescript
const { points } = await client.play.getPoints({
  gameId: 'your-game-uuid',
  playerId: 'player-123',
});
```

### Get Leaderboard

```typescript
const leaderboard = await client.play.getLeaderboard({
  gameId: 'your-game-uuid',
});
```

## User API

```typescript
const user = await client.users.me();
```

## Express.js Integration Example

```typescript
import express from 'express';
import { OpenGameClient } from '@opusgamelabs/server-sdk';

const app = express();
app.use(express.json());

const client = new OpenGameClient({
  apiKey: process.env.OGP_API_KEY!,
  secretKey: process.env.OGP_API_SECRET_KEY!,
});

const GAME_ID = process.env.GAME_ID!;

app.post('/api/submit-score', async (req, res) => {
  const { playerId, score, sessionId } = req.body;

  // YOUR VALIDATION LOGIC HERE
  // - Verify the player actually earned this score
  // - Check for suspicious patterns
  // - Validate session data
  // - Apply your own anti-cheat rules

  try {
    await client.play.savePoints({
      gameId: GAME_ID,
      playerId,
      points: score,
    });

    res.json({ success: true });
  } catch (error) {
    console.error('Failed to save points:', error);
    res.status(500).json({ error: 'Failed to save points' });
  }
});

app.get('/api/leaderboard', async (req, res) => {
  const leaderboard = await client.play.getLeaderboard({ gameId: GAME_ID });
  res.json(leaderboard);
});

app.listen(3000);
```

## Important Notes

- **Always validate scores server-side** before submitting to Play.fun
- **Set anti-cheat limits** when registering your game to prevent abuse
- **Store credentials in environment variables**, never in code
- **The SDK handles HMAC authentication** automatically
