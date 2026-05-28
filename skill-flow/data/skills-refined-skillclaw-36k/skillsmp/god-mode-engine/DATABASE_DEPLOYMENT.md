# God Mode Engine - Database Deployment

Quick procedure for deploying the God Mode database schema and seeding 100 games.

## Automated Browser Deployment

```bash
# 1. Copy schema SQL to clipboard
cat database/migrations/god_mode_engine.sql | pbcopy

# 2. Use browser_subagent to execute in Supabase SQL Editor:
#    - Navigate to: https://supabase.com/dashboard/project/kuklfnapbkmacvwxktbh/sql/new
#    - Paste SQL (Cmd+V) 
#    - Click Run
#    - Verify: SELECT COUNT(*) FROM game_registry;

# 3. Seed 100 games
cat database/migrations/seed_game_registry.sql | pbcopy
# Repeat paste & run in SQL Editor
```

## Verification Query

```sql
-- Expected: SCENARIO=24, CHART=20, PIO=56
SELECT COUNT(*), engine_type 
FROM game_registry 
GROUP BY engine_type;
```

## Manual Fallback

If browser automation fails, manually copy SQL files to Supabase Dashboard:
1. Open `database/migrations/god_mode_engine.sql`
2. Open `database/migrations/seed_game_registry.sql`
3. Execute both in SQL Editor

## Tables Created

| Table | Rows |
|-------|------|
| game_registry | 100 games |
| god_mode_user_session | Empty (user data) |
| god_mode_hand_history | Empty (hand logs) |
| god_mode_leaderboard | Empty (rankings) |
