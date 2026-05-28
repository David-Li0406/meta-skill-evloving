---
name: browser-sdk-snippets
description: Code snippets for the Play.fun Browser SDK
metadata:
  tags: playfun, sdk, browser, snippets, code
---

# Browser SDK Code Snippets

## Installation (CDN)

```html
<script src="https://sdk.play.fun/latest"></script>
<meta name="x-pf-key" content="your-api-key" />
```

## Installation (npm)

```bash
npm install @playfun/game-sdk
```

## Basic Setup

```javascript
const sdk = new PlayFunSDK({
  gameId: 'your-game-uuid',
});

await sdk.init();
console.log('SDK ready!');
```

## With Points Widget

```javascript
const sdk = new PlayFunSDK({
  gameId: 'your-game-uuid',
  ui: {
    usePointsWidget: true,
  },
});

await sdk.init();
```

## Add and Save Points

```javascript
// Add points locally (cached)
sdk.addPoints(10);
sdk.addPoints(25);
sdk.addPoints(5);

// Save all cached points to server
await sdk.savePoints();
```

## Event Listeners

```javascript
sdk.on('OnReady', () => {
  console.log('SDK initialized');
  startGame();
});

sdk.on('pointsSynced', (totalPoints) => {
  console.log('Points saved! Total:', totalPoints);
});

sdk.on('error', (error) => {
  console.error('SDK error:', error);
});
```

## Simple Clicker Game

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Clicker Game</title>
    <script src="https://cdn.play.fun/sdk/latest/game-sdk.min.js"></script>
    <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 50px;
      }
      #click-btn {
        font-size: 24px;
        padding: 20px 40px;
        cursor: pointer;
      }
      #score {
        font-size: 48px;
        margin: 20px;
      }
    </style>
  </head>
  <body>
    <h1>Click the Button!</h1>
    <div id="score">0</div>
    <button id="click-btn">Click Me!</button>

    <script>
      let score = 0;

      const sdk = new PlayFunSDK({
        gameId: 'your-game-uuid',
        ui: { usePointsWidget: true },
      });

      sdk.init().then(() => {
        document.getElementById('click-btn').onclick = () => {
          score += 1;
          document.getElementById('score').textContent = score;
          sdk.addPoints(1);
        };
      });

      // Auto-save every 30 seconds
      setInterval(() => sdk.savePoints(), 30000);

      // Save on page close
      window.addEventListener('beforeunload', () => sdk.savePoints());
    </script>
  </body>
</html>
```

## Canvas Game Integration

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Canvas Game</title>
    <script src="https://cdn.play.fun/sdk/latest/game-sdk.min.js"></script>
  </head>
  <body>
    <canvas id="game" width="800" height="600"></canvas>

    <script>
      const canvas = document.getElementById('game');
      const ctx = canvas.getContext('2d');
      let score = 0;
      let gameOver = false;

      const sdk = new PlayFunSDK({
        gameId: 'your-game-uuid',
        ui: { usePointsWidget: true },
      });

      sdk.init().then(() => {
        startGame();
      });

      function startGame() {
        score = 0;
        gameOver = false;
        gameLoop();
      }

      function addScore(points) {
        score += points;
        sdk.addPoints(points);
      }

      function endGame() {
        gameOver = true;
        sdk.savePoints().then(() => {
          console.log('Final score saved:', score);
        });
      }

      function gameLoop() {
        if (gameOver) return;

        // Your game logic here
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillText(`Score: ${score}`, 10, 30);

        requestAnimationFrame(gameLoop);
      }
    </script>
  </body>
</html>
```

## React Integration

```tsx
import { useEffect, useRef, useState } from 'react';

declare global {
  interface Window {
    PlayFunSDK: any;
  }
}

export function usePlayFun(gameId: string) {
  const sdkRef = useRef<any>(null);
  const [ready, setReady] = useState(false);
  const [points, setPoints] = useState(0);

  useEffect(() => {
    // Load SDK script
    const script = document.createElement('script');
    script.src = 'https://cdn.play.fun/sdk/latest/game-sdk.min.js';
    script.onload = async () => {
      const sdk = new window.PlayFunSDK({
        gameId,
        ui: { usePointsWidget: true },
      });

      await sdk.init();
      sdkRef.current = sdk;
      setReady(true);

      sdk.on('pointsSynced', (total: number) => setPoints(total));
    };
    document.head.appendChild(script);

    return () => {
      script.remove();
    };
  }, [gameId]);

  const addPoints = (amount: number) => {
    if (sdkRef.current) {
      sdkRef.current.addPoints(amount);
      setPoints((p) => p + amount);
    }
  };

  const savePoints = async () => {
    if (sdkRef.current) {
      await sdkRef.current.savePoints();
    }
  };

  return { ready, points, addPoints, savePoints };
}

// Usage
function Game() {
  const { ready, points, addPoints, savePoints } = usePlayFun('your-game-uuid');

  if (!ready) return <div>Loading...</div>;

  return (
    <div>
      <p>Points: {points}</p>
      <button onClick={() => addPoints(10)}>+10 Points</button>
      <button onClick={savePoints}>Save</button>
    </div>
  );
}
```

## Phaser 3 Integration

```javascript
import Phaser from 'phaser';

class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene');
    this.sdk = null;
    this.score = 0;
  }

  async create() {
    // Initialize Play.fun SDK
    this.sdk = new PlayFunSDK({
      gameId: 'your-game-uuid',
      ui: { usePointsWidget: true },
    });
    await this.sdk.init();

    // Score text
    this.scoreText = this.add.text(16, 16, 'Score: 0', {
      fontSize: '32px',
      fill: '#fff',
    });

    // Example: award points on enemy kill
    this.events.on('enemyKilled', (points) => {
      this.score += points;
      this.scoreText.setText(`Score: ${this.score}`);
      this.sdk.addPoints(points);
    });
  }

  gameOver() {
    // Save points when game ends
    this.sdk.savePoints().then(() => {
      this.scene.start('GameOverScene', { score: this.score });
    });
  }
}
```

## Auto-Save with Debounce

```javascript
const sdk = new PlayFunSDK({
  gameId: 'your-game-uuid',
  ui: { usePointsWidget: true },
});

await sdk.init();

let saveTimeout = null;
let unsavedPoints = 0;

function addPointsWithAutoSave(points) {
  sdk.addPoints(points);
  unsavedPoints += points;

  // Clear existing timeout
  if (saveTimeout) clearTimeout(saveTimeout);

  // Save after 5 seconds of inactivity, or immediately if 100+ unsaved points
  if (unsavedPoints >= 100) {
    sdk.savePoints();
    unsavedPoints = 0;
  } else {
    saveTimeout = setTimeout(() => {
      sdk.savePoints();
      unsavedPoints = 0;
    }, 5000);
  }
}
```

## Hybrid: Browser Widget + Server Validation

```javascript
// Browser code - widget display only, scores go to YOUR server
const sdk = new PlayFunSDK({
  gameId: 'your-game-uuid',
  ui: { usePointsWidget: true },
});

await sdk.init();

let sessionId = null;
let score = 0;

// Start game session via your server
async function startGame() {
  const res = await fetch('/api/start-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ playerId: getPlayerId() }),
  });
  const data = await res.json();
  sessionId = data.sessionId;
  score = 0;
}

// Add score locally (display only)
function addScore(points) {
  score += points;
  updateScoreDisplay(score);
}

// Submit score to YOUR server (not directly to Play.fun)
async function endGame() {
  await fetch('/api/submit-score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      playerId: getPlayerId(),
      score: score,
      sessionId: sessionId,
    }),
  });
}

function getPlayerId() {
  let id = localStorage.getItem('playerId');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('playerId', id);
  }
  return id;
}
```

## Player ID Management

```javascript
// Get or create persistent player ID
function getPlayerId() {
  let playerId = localStorage.getItem('playfun_player_id');

  if (!playerId) {
    playerId = crypto.randomUUID();
    localStorage.setItem('playfun_player_id', playerId);
  }

  return playerId;
}

// Or use wallet address if available
async function getPlayerIdFromWallet() {
  if (window.solana && window.solana.isPhantom) {
    const response = await window.solana.connect();
    return response.publicKey.toString();
  }
  return getPlayerId(); // Fallback to UUID
}
```
