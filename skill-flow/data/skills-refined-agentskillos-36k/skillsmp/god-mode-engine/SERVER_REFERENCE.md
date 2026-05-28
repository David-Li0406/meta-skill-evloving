# FastAPI Server Reference

Quick reference for the `server.py` FastAPI server.

## Location
`/server.py` — 500+ lines

## Run Server
```bash
# Development (with auto-reload)
uvicorn server:app --reload --port 8000

# Production
uvicorn server:app --host 0.0.0.0 --port 8000
```

## Environment Variables
```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx  # Service key
```

## Endpoints

### POST /api/session/start
Start a new training session.
```json
// Request
{ "user_id": "uuid", "game_id": "push-fold-mastery" }

// Response
{
  "session_id": "uuid",
  "game_name": "Push/Fold Mastery",
  "engine_type": "CHART",
  "current_level": 1,
  "current_hp": 100
}
```

### POST /api/hand/next
Fetch next hand with Director Mode narrative.
```json
// Request
{ "session_id": "uuid", "user_id": "uuid" }

// Response
{
  "status": "HAND_READY",  // or "LEVEL_COMPLETE", "SESSION_COMPLETE"
  "hand_id": "uuid",
  "engine_type": "PIO",
  "hand_data": { ... },
  "narrative_summary": "Hero (BTN) Raises 2.2bb...",
  "current_hp": 100
}
```

### POST /api/hand/action
Submit user action (THE GAME LOOP).
```json
// Request
{
  "session_id": "uuid",
  "user_id": "uuid", 
  "hand_id": "uuid",
  "action_type": "BET",  // CHECK, CALL, BET, RAISE, FOLD
  "amount": 50  // % of pot
}

// Response
{
  "is_correct": true,
  "damage": 0,
  "ev_loss": 0.0,
  "feedback": "✅ Correct!",
  "villain_move": null,
  "is_hand_over": true,
  "current_hp": 100,
  "xp_earned": 10
}
```

### GET /api/games
List all games from game_registry.

### GET /api/games/{slug}
Get specific game details.

### GET /api/leaderboard/{slug}
Get leaderboard for a game.

### GET /api/health
Health check endpoint.

## Game Loop Flow

```
1. POST /api/session/start
        ↓
2. POST /api/hand/next  ←─────┐
        ↓                     │
3. POST /api/hand/action      │
        ↓                     │
   is_hand_over? ─── No ──→  │
        ↓ Yes                 │
   hands_remaining? ─ Yes ────┘
        ↓ No
   SESSION_COMPLETE
```
