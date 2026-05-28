---
name: server-sdk-snippets
description: Code snippets for the Play.fun Server SDK
metadata:
  tags: playfun, sdk, server, snippets, code
---

# Server SDK Code Snippets

## Installation

```bash
npm install @playfun/server-sdk
```

## Initialize Client

```typescript
import { PlayFunClient } from '@playfun/server-sdk';

const client = new PlayFunClient({
  apiKey: process.env.PLAYFUN_API_KEY!,
  secretKey: process.env.PLAYFUN_SECRET_KEY!,
});
```

## Register a Game

```typescript
const game = await client.games.register({
  name: 'My Awesome Game',
  description: 'A fun play-to-earn game',
  gameUrl: 'https://mygame.com',
  platform: 'web',
  // Anti-cheat limits (recommended)
  maxScorePerSession: 1000,
  maxSessionsPerDay: 10,
  maxCumulativePointsPerDay: 5000,
});

console.log('Game registered:', game.id);
```

## Save Points (Single Player)

```typescript
await client.play.savePoints({
  gameId: 'your-game-uuid',
  playerId: 'player-wallet-or-id',
  points: 100,
});
```

## Save Points (Batch)

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

## Get Player Points

```typescript
const { points } = await client.play.getPoints({
  gameId: 'your-game-uuid',
  playerId: 'player-wallet-or-id',
});

console.log('Player has', points, 'points');
```

## Get Leaderboard

```typescript
const leaderboard = await client.play.getLeaderboard({
  gameId: 'your-game-uuid',
});

leaderboard.forEach((entry, index) => {
  console.log(`${index + 1}. ${entry.playerId}: ${entry.points} points`);
});
```

## Express.js API Endpoint

```typescript
import express from 'express';
import { PlayFunClient } from '@playfun/server-sdk';

const app = express();
app.use(express.json());

const client = new PlayFunClient({
  apiKey: process.env.PLAYFUN_API_KEY!,
  secretKey: process.env.PLAYFUN_SECRET_KEY!,
});

const GAME_ID = process.env.GAME_ID!;

// Submit score endpoint
app.post('/api/submit-score', async (req, res) => {
  try {
    const { playerId, score } = req.body;

    // Validate score (add your own logic)
    if (score < 0 || score > 10000) {
      return res.status(400).json({ error: 'Invalid score' });
    }

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

// Get leaderboard endpoint
app.get('/api/leaderboard', async (req, res) => {
  try {
    const leaderboard = await client.play.getLeaderboard({ gameId: GAME_ID });
    res.json(leaderboard);
  } catch (error) {
    console.error('Failed to get leaderboard:', error);
    res.status(500).json({ error: 'Failed to get leaderboard' });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

## Next.js API Route

```typescript
// app/api/submit-score/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { PlayFunClient } from '@playfun/server-sdk';

const client = new PlayFunClient({
  apiKey: process.env.PLAYFUN_API_KEY!,
  secretKey: process.env.PLAYFUN_SECRET_KEY!,
});

export async function POST(request: NextRequest) {
  try {
    const { playerId, score } = await request.json();

    await client.play.savePoints({
      gameId: process.env.GAME_ID!,
      playerId,
      points: score,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to save points' }, { status: 500 });
  }
}
```

## Session-Based Validation

```typescript
import { PlayFunClient } from '@playfun/server-sdk';

const client = new PlayFunClient({
  apiKey: process.env.PLAYFUN_API_KEY!,
  secretKey: process.env.PLAYFUN_SECRET_KEY!,
});

// In-memory session store (use Redis in production)
const sessions = new Map<string, {
  playerId: string;
  startTime: number;
  events: Array<{ type: string; timestamp: number }>;
}>();

// Start a game session
function startSession(playerId: string): string {
  const sessionId = crypto.randomUUID();
  sessions.set(sessionId, {
    playerId,
    startTime: Date.now(),
    events: [],
  });
  return sessionId;
}

// Record game event
function recordEvent(sessionId: string, eventType: string): boolean {
  const session = sessions.get(sessionId);
  if (!session) return false;

  session.events.push({ type: eventType, timestamp: Date.now() });
  return true;
}

// Validate and submit score
async function submitScore(
  sessionId: string,
  playerId: string,
  score: number
): Promise<boolean> {
  const session = sessions.get(sessionId);

  // Validation checks
  if (!session) throw new Error('Invalid session');
  if (session.playerId !== playerId) throw new Error('Player mismatch');

  // Check if score is reasonable based on session duration
  const duration = Date.now() - session.startTime;
  const maxPossibleScore = Math.floor(duration / 1000) * 10; // 10 points/second max

  if (score > maxPossibleScore) {
    throw new Error('Score exceeds maximum possible for session duration');
  }

  // Submit to Play.fun
  await client.play.savePoints({
    gameId: process.env.GAME_ID!,
    playerId,
    points: score,
  });

  // Clean up session
  sessions.delete(sessionId);

  return true;
}
```

## Error Handling

```typescript
import { PlayFunClient } from '@playfun/server-sdk';

const client = new PlayFunClient({
  apiKey: process.env.PLAYFUN_API_KEY!,
  secretKey: process.env.PLAYFUN_SECRET_KEY!,
});

async function savePointsWithRetry(
  gameId: string,
  playerId: string,
  points: number,
  maxRetries = 3
): Promise<void> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await client.play.savePoints({ gameId, playerId, points });
      return;
    } catch (error: any) {
      if (error.code === 'RATE_LIMITED' && attempt < maxRetries) {
        // Exponential backoff
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)));
        continue;
      }

      if (error.code === 'POINTS_EXCEEDED') {
        console.log('Player hit daily limit');
        throw error;
      }

      throw error;
    }
  }
}
```

## List Your Games

```typescript
const { items: myGames } = await client.games.getMyGames();

myGames.forEach((game) => {
  console.log(`${game.name} (${game.id})`);
  console.log(`  Players: ${game.playerCount}`);
  console.log(`  Rewards Pool: $${game.totalRewardsPoolValueUsd}`);
});
```

## Update Game Settings

```typescript
await client.games.update({
  gameId: 'your-game-uuid',
  maxScorePerSession: 2000,
  maxSessionsPerDay: 15,
  description: 'Updated game description',
});
```
