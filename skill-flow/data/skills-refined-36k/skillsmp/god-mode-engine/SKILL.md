---
name: God Mode Engine
description: Build and manage the 100-game poker training RPG with 3-engine architecture (PIO, CHART, SCENARIO)
---

# God Mode Engine Skill

Complete implementation of the Smarter.Poker "God Mode" training system.

## Quick Reference

| Component | File | Lines |
|-----------|------|-------|
| Database Schema | `database/migrations/god_mode_engine.sql` | 322 |
| Game Seeder | `scripts/seed_games.py` | 450 |
| Engine Core | `src/engine/engine_core.py` | 733 |
| GameSession | `src/components/training/GameSession.tsx` | 900+ |
| LevelSelector | `src/components/training/LevelSelector.tsx` | 400+ |
| ChartGrid | `src/components/training/ChartGrid.tsx` | 500+ |
| MentalGym | `src/components/training/MentalGym.tsx` | 400+ |
| GameArena | `src/components/training/GameArena.tsx` | 850+ |
| RoundSummary | `src/components/training/RoundSummary.tsx` | 500+ |
| Card | `src/components/training/Card.tsx` | 280+ |
| Chip | `src/components/training/Chip.tsx` | 230+ |
| API Server | `server.py` | 500+ |
| GameCard | `src/components/training/GameCard.jsx` | 295 |
| Training Page | `pages/hub/training.js` | 1108 |
| Play Page | `pages/hub/training/play/[gameId].js` | 100+ |
| Arena Page | `pages/hub/training/arena/[gameId].js` | 150+ |

---

## Architecture

```
     GameSession.tsx
           │ REST
     ┌─────▼─────┐
     │ server.py │ FastAPI
     └─────┬─────┘
           │
     ┌─────▼─────┐
     │engine_core│ GameEngine
     └─────┬─────┘
     ┌─────┼─────┐
    PIO  CHART SCENARIO
    (60)  (19)   (21)
```

### Component Flow

```
/hub/training
     │
     ▼
GameCard (click)
     │
     ▼
/hub/training/play/[gameId] ──► LevelSelector
     │
     ▼ (select level)
/hub/training/arena/[gameId] ──► GameArena
     │                              │
     │                    ┌─────────┼─────────┐
     │                    ▼         ▼         ▼
     │              PokerTable  ChartGrid  MentalGym
     │                 (PIO)     (CHART)  (SCENARIO)
     │
     ▼ (session complete)
RoundSummary ──► Victory/Defeat screen
```

---

## Run Commands

```bash
# API Server
uvicorn server:app --reload --port 8000

# Frontend
npm run dev

# Seed games
python3 scripts/seed_games.py --stats

# Setup dummy data
python3 scripts/setup_dummy_data.py
```

---

## Implementation Steps

### Step 1-6: Core Engine (Completed)
- [x] Database schema
- [x] Game seeder (100 games)
- [x] Engine core backend
- [x] Frontend GameSession component
- [x] FastAPI server
- [x] Training Hub enhancements

### Step 7: Level Select Screen
- [x] `LevelSelector.tsx` - 10-level progression display
- [x] Visual indicators: locked/unlocked/current/passed
- [x] Difficulty curve display (85%-100% passing grades)
- [x] XP rewards preview

### Step 8: Engine Components
- [x] `ChartGrid.tsx` - 13x13 push/fold chart
  - Interactive cell selection
  - Color-coded actions (PUSH=green, FOLD=red, 3BET=blue)
  - Position and stack depth display
  - Visual feedback for correct/wrong answers
- [x] `MentalGym.tsx` - Mental game scenarios
  - Large scenario text display
  - Countdown timer with pressure
  - Emotional type badges
  - Timed decision making

### Step 9: Game HUD (GameArena)
- [x] `GameArena.tsx` - Full game session wrapper
- [x] Health bar with heart icons
- [x] Hand counter (hand X of 20)
- [x] XP display with streak bonus
- [x] Conditional engine rendering
- [x] Demo mode for testing without API

### Step 10: Victory/Defeat Screen
- [x] `RoundSummary.tsx` - Session completion screen
- [x] Phased reveal animation (SCORE → XP → BLUNDERS → ACTIONS)
- [x] Confetti celebration on pass
- [x] Animated score counter
- [x] Top 3 blunders review
- [x] Next level / Retry / Exit buttons

### Step 11: Navigation Wiring
- [x] `/hub/training/play/[gameId].js` → LevelSelector
- [x] `/hub/training/arena/[gameId].js` → GameArena
- [x] Session params via URL (level, session)

### Step 12: Graphics Engine
- [x] `Card.tsx` - Playing card component
  - SVG suit symbols
  - Color coding (red/black)
  - Sizes: small, medium, large
  - Flip/deal animations
  - CardGroup for hand display
- [x] `Chip.tsx` - Poker chip component
  - Denomination colors (1=white, 5=red, 25=green, 100=black, 500=purple, 1000=gold)
  - ChipStack for stacking effect
  - PotDisplay for pot visualization

### Step 13: Mock Data
- [x] `scripts/setup_dummy_data.py` - Data setup script
- [x] `/data/charts/push_fold_ranges.json` - Push/fold charts
- [x] `/data/charts/3bet_ranges.json` - 3-bet/call ranges
- [x] `/data/charts/icm_bubble_ranges.json` - ICM bubble charts
- [x] `/data/scenarios/mental_game.json` - Mental game scenarios
- [x] Validation system for data files

---

## Data Files

| File | Engine | Count |
|------|--------|-------|
| `push_fold_ranges.json` | CHART | 5 charts |
| `3bet_ranges.json` | CHART | 2 charts |
| `icm_bubble_ranges.json` | CHART | 3 charts |
| `mental_game.json` | SCENARIO | 10 scenarios (5 categories) |
| `sample_hands.json` | PIO | 20 demo hands |

---

## Component Props

### ChartGrid
```typescript
interface ChartGridProps {
  chartType: 'PUSH_FOLD' | '3BET_CALL' | 'ICM_BUBBLE';
  heroPosition: string;
  stackBB: number;
  phase: 'DISPLAY' | 'SELECT' | 'RESULT';
  selectedCell?: string;
  correctCell?: string;
  resultFeedback?: 'CORRECT' | 'WRONG';
  onAction: (action: string) => void;
}
```

### MentalGym
```typescript
interface MentalGymProps {
  scenario: {
    title: string;
    context: string;
    prompt: string;
    options: Array<{
      id: string;
      text: string;
      type: 'rational' | 'impulsive' | 'passive' | 'aggressive';
      correct: boolean;
      feedback: string;
    }>;
    timeout_seconds: number;
  };
  onAnswer: (optionId: string, timedOut: boolean) => void;
  timeRemaining?: number;
}
```

### GameArena
```typescript
interface GameArenaProps {
  gameId: string;
  level: number;
  sessionId: string;
  engineType: 'PIO' | 'CHART' | 'SCENARIO';
  onSessionComplete: (result: SessionResult) => void;
  onExit: () => void;
}
```

### RoundSummary
```typescript
interface RoundSummaryProps {
  result: {
    passed: boolean;
    score: number;
    totalHands: number;
    correctHands: number;
    xpEarned: number;
    streakBonus: number;
    blunders: Array<{
      hand: number;
      heroCards: string[];
      board: string[];
      yourAction: string;
      correctAction: string;
      evLoss: number;
    }>;
  };
  level: number;
  gameName: string;
  onNextLevel: () => void;
  onRetry: () => void;
  onExit: () => void;
}
```

---

## Deployment Checklist

- [x] Database schema
- [x] Game seeder (100 games)
- [x] Engine core backend
- [x] Frontend component
- [x] FastAPI server
- [x] Training Hub enhancements
- [x] Level Select screen
- [x] Engine components (ChartGrid, MentalGym)
- [x] Game HUD (GameArena)
- [x] Victory/Defeat screen (RoundSummary)
- [x] Navigation wiring
- [x] Graphics engine (Card, Chip)
- [x] Mock data setup
- [ ] Production deploy

---

## Skill Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main guide (this file) |
| `ENGINE_CORE_REFERENCE.md` | Python backend |
| `GAMESESSION_REFERENCE.md` | React frontend |
| `SERVER_REFERENCE.md` | FastAPI endpoints |
| `SEEDER_REFERENCE.md` | Game seeding |
| `TRAINING_HUB_REFERENCE.md` | Training Hub UI |
| `DATABASE_DEPLOYMENT.md` | Browser automation |
