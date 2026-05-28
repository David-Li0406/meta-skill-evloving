---
name: sdk-hybrid
description: Hybrid SDK integration for Play.fun - combining Server and Browser SDKs
metadata:
  tags: playfun, sdk, hybrid, reference, docs
---

## Overview

The Hybrid approach combines the **Server SDK** for secure point submission with the **Browser SDK** for displaying the Play.fun widget. This gives you the best of both worlds: security and user experience.

## Why Hybrid?

| Component   | Purpose                                            |
| ----------- | -------------------------------------------------- |
| Server SDK  | Secure point submission with validation            |
| Browser SDK | Display points widget, leaderboard, wallet connect |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    BROWSER                          │
│  ┌─────────────────────────────────────────────┐   │
│  │  Your Game                                   │   │
│  │  - Game logic runs here                      │   │
│  │  - Sends score to YOUR server for validation │   │
│  └─────────────────────────────────────────────┘   │
│                        │                            │
│  ┌─────────────────────▼───────────────────────┐   │
│  │  Browser SDK (widget only)                   │   │
│  │  - Shows Play.fun widget                     │   │
│  │  - Displays points, leaderboard              │   │
│  │  - Handles wallet connect for claims         │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────────┼────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│                   YOUR SERVER                        │
│  ┌─────────────────────────────────────────────┐    │
│  │  1. Receive score from browser               │    │
│  │  2. VALIDATE the score (anti-cheat)          │    │
│  │  3. Submit via Server SDK                    │    │
│  └─────────────────────────────────────────────┘    │
│                        │                             │
│  ┌─────────────────────▼───────────────────────┐    │
│  │  Server SDK                                  │    │
│  │  client.play.savePoints(...)                 │    │
│  └─────────────────────────────────────────────┘    │
└────────────────────────┼────────────────────────────┘
                         │
                         ▼
                  Play.fun API
```

## Server Setup (Node.js/Express)

Install the Server SDK:

```bash
npm install @playfun/server-sdk
```

Create your score submission endpoint:

```typescript
import express from 'express';
import { OpenGameClient } from '@playfun/server-sdk';

const app = express();
app.use(express.json());

const client = new OpenGameClient({
  apiKey: process.env.OGP_API_KEY!,
  secretKey: process.env.OGP_API_SECRET_KEY!,
});

const GAME_ID = process.env.GAME_ID!;

app.post('/api/submit-score', async (req, res) => {
  const { playerId, score, gameSessionId } = req.body;

  // YOUR VALIDATION LOGIC HERE
  // Example validations:
  // - Check if session exists and is valid
  // - Verify score is within expected range
  // - Check for replay attacks
  // - Apply rate limiting
  const isValid = await validateScore(playerId, score, gameSessionId);

  if (!isValid) {
    return res.status(400).json({ error: 'Invalid score' });
  }

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

async function validateScore(playerId: string, score: number, sessionId: string): Promise<boolean> {
  // Implement your validation logic:
  // - Check session validity
  // - Verify score is reasonable
  // - Check for duplicate submissions
  return true;
}

app.listen(3000);
```

## Browser Setup

Add the Browser SDK for the widget:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Game</title>
    <script src="https://sdk.play.fun/latest"></script>
  </head>
  <body>
    <div id="game-container"></div>

    <script>
      // SDK for widget display only - NOT for point submission
      const sdk = new OpenGameSDK({
        gameId: 'your-game-uuid',
        ui: { usePointsWidget: true },
      });

      await sdk.init();

      // Your game logic here...
      let currentSessionId = generateSessionId();

      // Submit scores to YOUR server (not directly to Play.fun)
      async function submitScore(score) {
        const response = await fetch('/api/submit-score', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            playerId: getCurrentPlayerId(),
            score: score,
            gameSessionId: currentSessionId,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to submit score');
        }

        return response.json();
      }

      function getCurrentPlayerId() {
        // Return the player's unique identifier
        // This could come from wallet address, game account, etc.
        return localStorage.getItem('playerId') || generatePlayerId();
      }

      function generateSessionId() {
        return crypto.randomUUID();
      }

      function generatePlayerId() {
        const id = crypto.randomUUID();
        localStorage.setItem('playerId', id);
        return id;
      }
    </script>
  </body>
</html>
```

## Complete Example

### Server (server.ts)

```typescript
import express from 'express';
import { OpenGameClient } from '@opusgamelabs/server-sdk';

const app = express();
app.use(express.json());
app.use(express.static('public'));

const client = new OpenGameClient({
  apiKey: process.env.OGP_API_KEY!,
  secretKey: process.env.OGP_API_SECRET_KEY!,
});

const GAME_ID = process.env.GAME_ID!;

// In-memory session store (use Redis in production)
const sessions = new Map<string, { playerId: string; startTime: number; maxScore: number }>();

// Start a game session
app.post('/api/start-session', (req, res) => {
  const { playerId } = req.body;
  const sessionId = crypto.randomUUID();

  sessions.set(sessionId, {
    playerId,
    startTime: Date.now(),
    maxScore: 0,
  });

  res.json({ sessionId });
});

// Submit score with validation
app.post('/api/submit-score', async (req, res) => {
  const { playerId, score, gameSessionId } = req.body;

  const session = sessions.get(gameSessionId);

  // Validation checks
  if (!session) {
    return res.status(400).json({ error: 'Invalid session' });
  }

  if (session.playerId !== playerId) {
    return res.status(400).json({ error: 'Player mismatch' });
  }

  const sessionDuration = Date.now() - session.startTime;
  const maxPossibleScore = Math.floor(sessionDuration / 1000) * 10; // 10 points per second max

  if (score > maxPossibleScore) {
    return res.status(400).json({ error: 'Score too high for session duration' });
  }

  // Save to Play.fun
  await client.play.savePoints({
    gameId: GAME_ID,
    playerId,
    points: score,
  });

  // Clean up session
  sessions.delete(gameSessionId);

  res.json({ success: true });
});

app.listen(3000);
```

### Browser (public/index.html)

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Hybrid Game</title>
    <script src="https://cdn.play.fun/sdk/latest/game-sdk.min.js"></script>
  </head>
  <body>
    <h1>Click Game</h1>
    <button id="start-btn">Start Game</button>
    <button id="click-btn" disabled>Click Me!</button>
    <button id="end-btn" disabled>End Game</button>
    <p>Score: <span id="score">0</span></p>

    <script>
      const sdk = new OpenGameSDK({
        gameId: 'your-game-uuid',
        ui: { usePointsWidget: true },
      });

      let playerId = localStorage.getItem('playerId');
      if (!playerId) {
        playerId = crypto.randomUUID();
        localStorage.setItem('playerId', playerId);
      }

      let sessionId = null;
      let score = 0;

      sdk.init();

      document.getElementById('start-btn').onclick = async () => {
        const res = await fetch('/api/start-session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ playerId }),
        });
        const data = await res.json();
        sessionId = data.sessionId;
        score = 0;
        document.getElementById('score').textContent = '0';
        document.getElementById('click-btn').disabled = false;
        document.getElementById('end-btn').disabled = false;
        document.getElementById('start-btn').disabled = true;
      };

      document.getElementById('click-btn').onclick = () => {
        score += 10;
        document.getElementById('score').textContent = score;
      };

      document.getElementById('end-btn').onclick = async () => {
        await fetch('/api/submit-score', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ playerId, score, gameSessionId: sessionId }),
        });

        document.getElementById('click-btn').disabled = true;
        document.getElementById('end-btn').disabled = true;
        document.getElementById('start-btn').disabled = false;
        sessionId = null;
      };
    </script>
  </body>
</html>
```

## Important Notes

- **Server validates, browser displays**: Never trust client-side scores
- **Session management**: Track game sessions to prevent replay attacks
- **Widget is display-only**: The browser SDK shows the widget but doesn't submit points
- **Rate limiting**: Implement server-side rate limiting to prevent abuse
