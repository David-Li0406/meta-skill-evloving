---
name: wos-recommend
description: Generate hero upgrade recommendations based on user's profile, heroes, and priorities. Use when user asks what to upgrade, invest in, or prioritize. Uses rules-based logic with verified game data.
allowed-tools: Read, Glob, Bash(python:*)
---

# WoS Recommendation Engine

## Purpose
Analyzes user's saved heroes and profile to provide prioritized upgrade recommendations based on verified game mechanics.

## Data Sources

1. **User Profile**: `wos.db` via SQLite (server age, priorities, furnace level)
2. **User Heroes**: `wos.db` (owned heroes with levels, stars, skills)
3. **Hero Data**: `data/heroes.json` (tier ratings, classes, generations)
4. **Verified Mechanics**: `data/WOS_REFERENCE.md`
5. **Upgrade Costs**: `data/upgrades/*.json` (cost-aware recommendations)
6. **Explanation System**: `data/explanation_builder.json` (how to explain recs)
7. **Confidence Scoring**: `data/confidence_scoring.json` (grade recommendations)
8. **Combat Synergy**: `data/synergy_model.json` (context-aware weights)

## Instructions

When generating recommendations:

1. **Load user data** by reading the database or asking user for current state

2. **Apply priority weights** based on user's settings:
   - SvS priority → weight expedition skills higher
   - Rally priority → weight rally leader/joiner roles
   - Exploration priority → weight exploration skills
   - Gathering priority → lowest priority upgrades

3. **Score each hero** using:
   ```
   Score = TierScore × GenerationRelevance × PriorityWeight × CurrentInvestmentGap
   ```

4. **Apply verified mechanics**:

### Joiner Role Bonus
- If user prioritizes Rally/SvS AND doesn't have Jessie leveled → HIGH priority
- If user prioritizes Garrison AND doesn't have Sergey leveled → HIGH priority
- Reason: Only their expedition skill matters when joining (leftmost hero)

### Leader Role Bonus
- Jeronimo gets bonus if user prioritizes Rally (his 9 skills buff entire rally)
- Natalia gets bonus for garrison leading

### Generation Relevance
```
Gen diff = CurrentGen - HeroGen
0 or negative: 1.0 (current/future gen)
1: 0.9 (still very relevant)
2: 0.7 (moderately relevant)
3: 0.5 (getting outdated)
4+: 0.3 (old hero)

Exception: S+ tier heroes add +0.2 relevance
```

### Hero Skill System
Each hero has two skill types:
- **Exploration skills** (left side of screen) - Upgraded with Exploration Manuals - for PvE
- **Expedition skills** (right side of screen) - Upgraded with Expedition Manuals - for PvP
- Both scale 1-5 with equal % increments per level
- Manual costs increase per level

### Skill Priority (for PvP-focused users)
- Expedition skills > Exploration skills
- Leftmost hero's TOP-RIGHT expedition skill (joiner role) is CRITICAL

## Recommendation Categories

### HIGH Priority
- S/S+ tier heroes below level 50
- Missing key joiner heroes (Jessie/Sergey) for rally-focused users
- Expedition skills below level 3 for PvP-focused users

### MEDIUM Priority
- A tier heroes
- Stars/ascension for top heroes
- Exploration skills for PvE-focused users

### LOW Priority
- B/C tier heroes
- Old generation heroes (3+ gens behind)
- Gathering-focused upgrades

## Output Format

```
## Top Recommendations

### 1. [HIGH] Level Jeronimo to 60
**Current**: Lv 45 | **Target**: Lv 60
**Reason**: S+ tier rally leader. His expedition skills buff your entire rally.
**Resources**: Hero EXP items

### 2. [HIGH] Unlock Jessie
**Reason**: Best attack joiner. Her expedition skill (+25% DMG) applies when joining rallies (leftmost slot).
**Resources**: Hero shards from events

### 3. [MEDIUM] Upgrade Natalia's Expedition Skill 1 to Lv 4
**Current**: Lv 3 | **Target**: Lv 4
**Reason**: Your main tank. Higher expedition skills = better SvS performance.
**Resources**: Skill manuals
```

## DO NOT Use OpenAI

This skill uses RULES-BASED recommendations only. Do NOT call OpenAI API.
Reasons:
- OpenAI doesn't have verified WoS knowledge
- OpenAI hallucinates skill effects and hero names
- Rules-based is more reliable for game-specific advice

## Fallback

If database is not accessible, ask user to provide:
1. Server age (days) or generation
2. Top 5 heroes with levels
3. Main priority (SvS, Rally, PvE, etc.)

Then apply the scoring rules manually.
