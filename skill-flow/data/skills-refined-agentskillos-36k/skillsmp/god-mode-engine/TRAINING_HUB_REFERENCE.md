# Training Hub Reference

Quick reference for the Training Hub (`/hub/training`) enhancements.

## GameCard Enhancements

### Added Features
1. **Visual Progress Bar**
   - Shows "Level X/10" with percentage
   - Animated fill using framer-motion
   - Green gradient for in-progress, cyan for new

2. **Action Button States**
   - `▶ START` (cyan) — New game, not played
   - `▶ RESUME` (green) — In progress
   - `✓ MASTERED` (gold) — All 10 levels complete

### GameCard Props
```jsx
<GameCard
  game={gameObject}        // Required: game from TRAINING_LIBRARY
  progress={progressData}  // { levelsCompleted, bestScore, streakBest }
  onClick={handleClick}    // Click handler
  index={i}               // For staggered animation
  image={imageUrl}        // Optional override
/>
```

### Progress States
| levelsCompleted | State | Button | Border |
|-----------------|-------|--------|--------|
| 0 | New | START | Category color |
| 1-9 | In Progress | RESUME | Category color |
| 10 | Mastered | MASTERED | Gold |

## Training Page Structure

```
TrainingPage
├── UniversalHeader
├── PromoSection (Daily Challenge)
├── StreaksBadge
├── FilterBar (5 categories)
└── GameLanes
    ├── TODAY'S DAILY CHALLENGE
    ├── FIX YOUR LEAKS
    └── Category Lanes (MTT, CASH, SPINS, PSYCHOLOGY, ADVANCED)
```

## Files Modified
- `src/components/training/GameCard.jsx` — 295 lines
