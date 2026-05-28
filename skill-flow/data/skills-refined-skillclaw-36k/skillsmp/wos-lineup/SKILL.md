---
name: wos-lineup
description: Build optimal Whiteout Survival lineups for specific events. Use when user asks about Bear Trap, Crazy Joe, SvS, garrison, rally, or arena compositions. Provides hero recommendations and troop ratios.
allowed-tools: Read, Glob
---

# WoS Lineup Builder

## Purpose
Provides event-specific lineup recommendations based on verified game mechanics.

## Key Mechanics (VERIFIED)

### March Composition
- **World marches**: 3 heroes (1 Infantry, 1 Lancer, 1 Marksman)
- **Arena only**: 5 heroes

### Rally Structure
- **Leader**: 3 heroes provide 9 expedition skills (all right-side skills)
- **Joiners**: Only LEFTMOST hero's TOP-RIGHT expedition skill contributes
- **Max member skills**: Top 4 highest SKILL LEVEL from all joiners (can stack if same effect)

### Combat Order
Infantry fights first → Lancers → Marksmen

## Instructions

When building a lineup:

1. **Read reference data**:
   ```
   Read file_path="data/WOS_REFERENCE.md"
   ```

2. **Identify the event type** from user request:
   - Bear Trap / Bear Hunt
   - Crazy Joe
   - SvS Castle Attack
   - SvS Castle Defense / Garrison
   - Arena
   - Alliance Championship
   - Field PvP

3. **Provide lineup based on event**:

### Bear Trap Rally
**Leader**: Jeronimo (lead) + Molly + Alonso
**Troop Ratio**: 0% Infantry / 10% Lancer / 90% Marksman
**Why**: Maximum DPS, bear doesn't kill troops quickly

**Joiners**: Use Jessie as first hero (Stand of Arms: +25% DMG dealt)

### Crazy Joe
**Troop Ratio**: 90% Infantry / 10% Lancer / 0% Marksman
**Why**: Infantry engages first and kills before back row attacks

### SvS Castle Attack (Leader)
**Lineup**: Jeronimo (lead) + Molly + Alonso
**Troop Ratio**: 50% Infantry / 20% Lancer / 30% Marksman

### SvS Castle Defense (Garrison)
**Lineup**: Natalia (lead) + Molly + Alonso
**Troop Ratio**: 60% Infantry / 15% Lancer / 25% Marksman

**Joiners**: Use Sergey as first hero (Defenders' Edge: -20% DMG taken)

### Arena (5 Heroes)
**Offense**: Natalia, Flint, Alonso, Molly, Philly
**Defense**: Natalia, Flint, Molly, Alonso, Bahiti

## Troop Ratio Quick Reference

| Event | Infantry | Lancer | Marksman |
|-------|----------|--------|----------|
| Default | 50% | 20% | 30% |
| Castle Battle | 50% | 20% | 30% |
| Bear Hunt | 0% | 10% | 90% |
| Crazy Joe | 90% | 10% | 0% |
| Labyrinth | 60% | 15% | 25% |
| Championship | 45% | 25% | 35% |

## Best Joiner Heroes

| Role | Hero | Top-Right Skill | Effect per Level (1-5) |
|------|------|-----------------|------------------------|
| Attack Joiner | Jessie | Stand of Arms | +5/10/15/20/25% DMG dealt |
| Garrison Joiner | Sergey | Defenders' Edge | -4/8/12/16/20% DMG taken |

## Output Format

Provide:
1. Recommended heroes (with class and role)
2. Troop ratio with explanation
3. Why this composition works
4. Alternative options if user doesn't have recommended heroes
