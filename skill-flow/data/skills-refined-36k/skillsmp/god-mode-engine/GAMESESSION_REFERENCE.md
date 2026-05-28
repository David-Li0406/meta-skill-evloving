# GameSession Component Reference

Quick reference for the `GameSession.tsx` React component.

## Location
`/src/components/training/GameSession.tsx` — 900+ lines

## Usage
```tsx
import GameSession from '@/components/training/GameSession';

<GameSession
  userId={currentUser.id}
  gameId="push-fold-mastery"
  gameName="Push/Fold Mastery"
  onSessionComplete={(stats) => console.log(stats)}
  onExit={() => router.back()}
/>
```

## Game Phases

| Phase | Description |
|-------|-------------|
| `LOADING` | Fetching next hand from API |
| `DIRECTOR_INTRO` | Typewriter animation showing action history |
| `USER_TURN` | Waiting for user action (controls unlocked) |
| `VILLAIN_THINKING` | 1.5s delay while villain decides |
| `SHOWING_RESULT` | Correct/incorrect overlay |
| `HAND_COMPLETE` | Ready for next hand |
| `SESSION_COMPLETE` | All 20 hands done |

## Key Features

### 1. Director Mode Intro
- Typewriter text: "Hero (BTN) Raises 2.2bb..."
- Chip slide sound between lines
- 800ms delay per line
- Auto-unlock after all lines complete

### 2. Health Bar
- 100 HP starting value
- Screen shake on damage (framer-motion)
- Color transitions: Green → Orange → Red
- Floating "-X" damage indicator

### 3. Bet Slider Snapping
- User drags freely (0-200% pot)
- Snaps to nearest solver node on release
- Nodes: [0, 25, 33, 50, 66, 75, 100, 150, 200]
- 🧲 Magnet icon feedback

### 4. Active Villain
- "Villain is thinking..." with animated dots
- 1.5s delay before action reveal
- Deals new cards if applicable
- Returns control to user

## 3-Engine Rendering

| Engine | Component | Status |
|--------|-----------|--------|
| PIO | `<PokerTable />` | ✅ Full implementation |
| CHART | `<ChartGrid />` | 🔲 Placeholder |
| SCENARIO | `<MentalDrill />` | 🔲 Placeholder |

## API Endpoints Used

```javascript
// Fetch next hand
POST /api/god-mode/fetch-hand
Body: { userId, gameId, currentLevel }

// Submit action
POST /api/god-mode/submit-action
Body: { userId, gameId, action, sizing, handData }
```

## Animation Library
Uses `framer-motion` for:
- Screen shake
- Typewriter text
- Result overlay transitions
- Slider thumb scaling
