# God Mode Engine - Quick Setup

## 1. Run Database Migration

```bash
# In Supabase Dashboard SQL Editor, run:
cat database/migrations/god_mode_engine.sql
```

## 2. Seed 100 Games

```bash
# Generate SQL
python3 scripts/seed_games.py --output database/migrations/seed_game_registry.sql

# View distribution
python3 scripts/seed_games.py --stats
# Output: PIO=56, CHART=20, SCENARIO=24
```

## 3. Test Engine Core

```bash
python3 src/engine/engine_core.py
# Runs suit rotation, villain, and damage tests
```

## 4. Start Dev Server

```bash
npm run dev
# Visit: http://localhost:3000/hub/training
```

## 5. Use GameSession Component

```tsx
import { GameSession } from '@/components/training/GameSession';

<GameSession
  gameId="short-stack-ninja"
  userId={user.id}
  onSessionComplete={(stats) => console.log(stats)}
/>
```
