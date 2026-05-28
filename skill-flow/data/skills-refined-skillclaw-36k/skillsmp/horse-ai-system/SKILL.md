---
name: Horse AI System
description: Manage the 100 AI poker horses for content and gameplay
---

# Horse AI System Skill

## Overview
The Ghost Fleet consists of 100 AI-powered horse personas that:
1. Post social content (clips, news, memes)
2. Play poker using GTO strategies
3. Have persistent memory and relationships

## Database Tables

### content_authors (Horse roster)
- `id`, `name`, `alias`, `avatar_url`
- `specialty`, `voice`, `stakes`
- `is_active`, `profile_id`

### horse_personality (GTO traits)
- `gto_adherence` (0-100%)
- `deviation_trigger` (never/strong_read/weak_opponent/icm_pressure/any_read/always)
- `mixed_strategy_bias` (balanced/aggressive/defensive/survival/max_variance)
- `preferred_stack_depths`, `preferred_game_types`, `preferred_topologies`
- `archetype_name` (GTO_Purist/Balanced/Aggressive_GTO/Passive_GTO/Exploitative/MTT_Specialist/Degen)

### horse_memory (Persistent memory)
- `memory_type` (POST/OPINION/INTERACTION/TOPIC/STORY/CLAIM)
- `content_summary`, `keywords`, `sentiment`
- `strength` (decays over time)

### horse_relationships (Inter-horse dynamics)
- `relationship_type` (friend/rival/mentor/student/neutral)
- `sentiment_score` (-1.0 to 1.0)

## Cron Endpoints

### Content Posting
| Endpoint | Purpose | Schedule |
|----------|---------|----------|
| `/api/cron/horses-clips` | Video clips from YouTube | Hourly |
| `/api/cron/horses-news` | RSS poker news | 2x daily |
| `/api/cron/horses-memes` | Poker humor/memes | 3x daily |
| `/api/cron/horses-avatars` | AI avatar generation | On-demand |

### Poker Playing
| Endpoint | Purpose |
|----------|---------|
| `/api/cron/horses-play` | Execute poker decisions |
| `/api/cron/horses-stats` | Update win/loss stats |

## Playing a Hand

### 1. Get Horse Personality
```javascript
const { data: personality } = await supabase.rpc('get_horse_personality', {
  p_author_id: horseId
});
```

### 2. Query GTO Solution
```javascript
const { data: spot } = await supabase
  .from('solved_spots_gold')
  .select('strategy_matrix')
  .eq('scenario_hash', hash)
  .single();

const strategy = spot.strategy_matrix[heroHand];
```

### 3. Apply Personality Bias
```javascript
const { data: action } = await supabase.rpc('get_horse_action', {
  p_author_id: horseId,
  p_strategy_actions: strategy.actions
});
// Returns 'Raise', 'Call', or 'Fold'
```

## Memory Functions

### Record Memory
```sql
SELECT record_horse_memory(
  1,                    -- author_id
  'OPINION',            -- memory_type
  'Fold equity matters', -- summary
  'strategy',           -- related_topic
  ARRAY['fold', 'equity', 'bluff']  -- keywords
);
```

### Get Memories for Context
```sql
SELECT * FROM get_horse_memories(1, 'strategy', 10);
```

## Archetype Behaviors

| Archetype | GTO % | Deviation | Mixed Bias |
|-----------|-------|-----------|------------|
| GTO_Purist | 95% | Never | Balanced |
| Balanced | 85% | Strong read | Balanced |
| Aggressive_GTO | 80% | Weak opponent | Aggressive |
| Passive_GTO | 80% | Never | Defensive |
| Exploitative | 60% | Any read | Situational |
| MTT_Specialist | 90% | ICM pressure | Survival |
| Degen | 40% | Always | Max variance |

## Best Practices
1. Always fetch personality before making decisions
2. Record memories after significant posts/hands
3. Update relationships after interactions
4. Use topic cooldowns to prevent repetition
