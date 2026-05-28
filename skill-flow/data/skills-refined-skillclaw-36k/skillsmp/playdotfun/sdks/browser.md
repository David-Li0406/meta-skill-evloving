---
name: sdk-browser
description: Browser SDK reference for Play.fun - for simple games and prototypes
metadata:
  tags: playfun, sdk, browser, reference, docs, vanilla-js
---

## Overview

The Browser SDK (`@opusgamelabs/game-sdk`) provides client-side integration for Play.fun games. It includes a points widget and simple API for tracking gameplay.

## When to Use

| Use Browser SDK                                  | Use Server SDK Instead                  |
| ------------------------------------------------ | --------------------------------------- |
| Simple prototypes and demos                      | Production games with token rewards     |
| "Vibe coded" games                               | Games where cheating prevention matters |
| Game jam entries                                 | When you need to validate scores        |
| Quick integrations where accuracy doesn't matter | Any game with real value at stake       |

**For production games, use the [Server SDK](server.md) instead.**

## Architecture

```
Browser Game → Vanilla SDK → Play.fun API (no server-side validation)
```

## Installation

### CDN (Recommended for simple games)

```html
<script src="https://sdk.play.fun/latest"></script>
```

### npm

```bash
npm install @playfun/game-sdk
```

## Basic Usage

```javascript
// Initialize SDK
const sdk = new OpenGameSDK({
  gameId: 'your-game-uuid',
});

await sdk.init();
console.log('SDK ready!');

// Add points during gameplay (cached locally)
sdk.addPoints(100);

// Save points to server
await sdk.savePoints();
```

## Configuration Options

```javascript
const sdk = new OpenGameSDK({
  gameId: 'your-game-uuid',
  ui: {
    usePointsWidget: true, // Show Play.fun points widget
  },
});
```

## Events

```javascript
sdk.on('OnReady', () => {
  console.log('SDK initialized and ready');
});

sdk.on('pointsSynced', (points) => {
  console.log('Points saved to server:', points);
});

sdk.on('error', (err) => {
  console.error('SDK error:', err);
});
```

## Complete Example

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Simple Game</title>
    <script src="https://sdk.play.fun/latest"></script>
  </head>
  <body>
    <h1>Click the Button!</h1>
    <button id="click-btn">Click Me (+10 points)</button>
    <p>Points: <span id="points">0</span></p>

    <script>
      let totalPoints = 0;

      const sdk = new OpenGameSDK({
        gameId: 'your-game-uuid',
        ui: { usePointsWidget: true },
      });

      sdk.init().then(() => {
        console.log('SDK ready!');

        document.getElementById('click-btn').onclick = () => {
          totalPoints += 10;
          document.getElementById('points').textContent = totalPoints;
          sdk.addPoints(10);
        };
      });

      // Auto-save every 30 seconds
      setInterval(() => {
        sdk.savePoints();
      }, 30000);

      // Save on page unload
      window.addEventListener('beforeunload', () => {
        sdk.savePoints();
      });
    </script>
  </body>
</html>
```

## Points Widget

The SDK includes a built-in widget that displays:

- Current points
- Leaderboard position
- Reward information
- Wallet connection for claiming rewards

Enable it with:

```javascript
const sdk = new OpenGameSDK({
  gameId: 'your-game-uuid',
  ui: { usePointsWidget: true },
});
```

## API Reference

### `new OpenGameSDK(config)`

Creates a new SDK instance.

| Option               | Type    | Description                 |
| -------------------- | ------- | --------------------------- |
| `gameId`             | string  | Your game's UUID (required) |
| `ui.usePointsWidget` | boolean | Show the points widget      |

### `sdk.init()`

Initialize the SDK. Returns a Promise.

### `sdk.addPoints(points)`

Add points to local cache. Points are not sent to the server until `savePoints()` is called.

### `sdk.savePoints()`

Save cached points to the Play.fun server. Returns a Promise.

### `sdk.on(event, callback)`

Listen for SDK events.

| Event          | Description            |
| -------------- | ---------------------- |
| `OnReady`      | SDK initialized        |
| `pointsSynced` | Points saved to server |
| `error`        | An error occurred      |

## Important Notes

- **No server-side validation**: Points are submitted directly from the browser
- **Vulnerable to cheating**: Users can manipulate point submissions
- **Use for prototypes only**: For production games, use the Server SDK
- **Save frequently**: Call `savePoints()` periodically to avoid losing progress
