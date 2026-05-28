---
name: sdk-best-practices
description: Best practices for integrating with Play.fun SDKs
metadata:
  tags: playfun, sdk, best-practices, guide
---

## SDK Selection Guide

| Scenario                                 | Recommended SDK               |
| ---------------------------------------- | ----------------------------- |
| Production game with token rewards       | **Server SDK**                |
| Game where cheating would be problematic | **Server SDK**                |
| Want both security and Play.fun widget   | **Hybrid** (Server + Browser) |
| Quick prototype / demo                   | Browser SDK                   |
| "Vibe coded" simple game                 | Browser SDK                   |
| Game jam entry                           | Browser SDK                   |

## Core Concepts

### Games

A **Game** is your registered application on Play.fun. Each game has:

- Unique UUID identifier
- Anti-cheat configuration (score limits)
- Metadata (name, description, URLs)
- Optional playcoin (game token)

### Points

**Points** are the in-game scores tracked per player. They:

- Form the basis for token rewards
- Are tracked per player per game
- Should be validated server-side for production games

### Playcoins

A **Playcoin** is a game-specific Solana token that:

- Has a bonding curve for trading
- Rewards players based on gameplay points
- Can "graduate" to full DEX trading

## Anti-Cheat Configuration

When registering your game, set these limits to prevent abuse:

```typescript
await client.games.register({
  name: 'My Game',
  description: 'Description',
  gameUrl: 'https://mygame.com',
  platform: 'web',
  // Anti-cheat limits:
  maxScorePerSession: 1000, // Max points per play session
  maxSessionsPerDay: 10, // Max sessions per player per day
  maxCumulativePointsPerDay: 5000, // Hard daily cap per player
});
```

### Choosing Limits

| Game Type        | maxScorePerSession | maxSessionsPerDay | maxCumulativePointsPerDay |
| ---------------- | ------------------ | ----------------- | ------------------------- |
| Casual clicker   | 100-500            | 20-50             | 2,000-5,000               |
| Skill-based game | 500-2,000          | 5-10              | 5,000-10,000              |
| Competitive game | 1,000-5,000        | 3-5               | 10,000-20,000             |

## Security Best Practices

### Credential Management

```typescript
// GOOD: Use environment variables
const client = new OpenGameClient({
  apiKey: process.env.OGP_API_KEY!,
  secretKey: process.env.OGP_API_SECRET_KEY!,
});

// BAD: Never hardcode credentials
const client = new OpenGameClient({
  apiKey: 'abc123', // DON'T DO THIS
  secretKey: 'xyz789',
});
```

### Server-Side Validation

Always validate scores before submitting to Play.fun:

```typescript
app.post('/api/submit-score', async (req, res) => {
  const { playerId, score, sessionId } = req.body;

  // 1. Validate session exists
  const session = await getSession(sessionId);
  if (!session) return res.status(400).json({ error: 'Invalid session' });

  // 2. Check session ownership
  if (session.playerId !== playerId) {
    return res.status(400).json({ error: 'Session mismatch' });
  }

  // 3. Validate score is reasonable
  const maxPossible = calculateMaxPossibleScore(session);
  if (score > maxPossible) {
    return res.status(400).json({ error: 'Score too high' });
  }

  // 4. Check for replay attacks
  if (session.submitted) {
    return res.status(400).json({ error: 'Already submitted' });
  }

  // 5. Submit to Play.fun
  await client.play.savePoints({ gameId, playerId, points: score });
  await markSessionSubmitted(sessionId);

  res.json({ success: true });
});
```

### Rate Limiting

Implement rate limiting on your server:

```typescript
import rateLimit from 'express-rate-limit';

const scoreLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 requests per minute
  message: 'Too many score submissions',
});

app.post('/api/submit-score', scoreLimiter, async (req, res) => {
  // ... handler
});
```

## Player Identification

### Wallet-Based (Recommended for Web3)

```typescript
// Player ID is their wallet address
const playerId = walletAddress;
```

### Account-Based

```typescript
// Player ID is your internal user ID
const playerId = user.id;
```

### Anonymous (Browser SDK only)

```typescript
// Generate and persist a UUID
let playerId = localStorage.getItem('playerId');
if (!playerId) {
  playerId = crypto.randomUUID();
  localStorage.setItem('playerId', playerId);
}
```

## Error Handling

```typescript
try {
  await client.play.savePoints({ gameId, playerId, points });
} catch (error) {
  if (error.code === 'RATE_LIMITED') {
    // Retry with backoff
  } else if (error.code === 'INVALID_GAME') {
    // Check game ID
  } else if (error.code === 'POINTS_EXCEEDED') {
    // Player hit daily limit
  } else {
    // Log and handle unexpected errors
    console.error('Failed to save points:', error);
  }
}
```

## Batch Operations

For efficiency, batch multiple point saves:

```typescript
// Instead of multiple single saves:
await client.play.savePoints({ gameId, playerId: 'p1', points: 100 });
await client.play.savePoints({ gameId, playerId: 'p2', points: 200 });
await client.play.savePoints({ gameId, playerId: 'p3', points: 150 });

// Use batch save:
await client.play.batchSavePoints({
  gameId,
  pointsRecord: {
    p1: 100,
    p2: 200,
    p3: 150,
  },
});
```

## Testing

### Development Mode

Use a test game for development:

```typescript
const GAME_ID =
  process.env.NODE_ENV === 'production' ? process.env.PROD_GAME_ID : process.env.DEV_GAME_ID;
```

### Verifying Integration

```typescript
// Test connection
const user = await client.users.me();
console.log('Connected as:', user.id);

// Test game access
const game = await client.games.getById({ gameId: GAME_ID });
console.log('Game:', game.name);

// Test point submission
await client.play.savePoints({
  gameId: GAME_ID,
  playerId: 'test-player',
  points: 1,
});
console.log('Points saved successfully');
```
