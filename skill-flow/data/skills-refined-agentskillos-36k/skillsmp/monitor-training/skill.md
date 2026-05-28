---
name: monitor-training
description: Monitor combat training with cool visual display and adaptive intervals
tags: [combat, training, monitor, xp, progress]
---

# Monitor Training Skill

Monitor combat training progress with a visual display and adaptive check intervals.

## Usage

```
/monitor-training [account] [goal_level]
```

- `account`: Account to monitor (default: aux)
- `goal_level`: Target level (default: 40)

## Display Format

Use this EXACT format for the progress display:

```
┌──────────────────────────────────────────────────────────┐
│  {name} @ {location}      ❤️ {hp}/{max}    🍖 {food_count} {food_type}   │
├──────────────────────────────────────────────────────────┤
│  Skill   Lvl   Progress to {goal}            Remaining       │
├──────────────────────────────────────────────────────────┤
│  ⚔️ Att   {lvl}   [{bar}] {pct}%    {remaining} XP       │
│  💪Str    {lvl}   [{bar}] {pct}%     {remaining} XP       │
│  🛡️ Def   {lvl}   [{bar}] {pct}%    {remaining} XP       │
│  ❤️ HP    {lvl}   [{bar}] {pct}%    {remaining} XP       │
├──────────────────────────────────────────────────────────┤
│  📈 Session: +{gained} Att   ~{rate}/hr   ETA {goal}: ~{eta} hrs       │
│  🙏 Bonus:   +{prayer_gained} Prayer  (Big Bones)                    │
└──────────────────────────────────────────────────────────┘

Status: {status_emoji} {status_text} | Next check: {interval}
```

### Critical Emoji Spacing Rules
- `⚔️ Att` - space AFTER emoji
- `💪Str` - NO space after emoji
- `🛡️ Def` - space AFTER emoji
- `❤️ HP` - space AFTER emoji

### Progress Bar
16 characters total using `#` and `-`:
- 17% = `[###-------------]`
- 85% = `[#############---]`

## Execution Steps

### 1. Get Initial State
```python
get_game_state(account_id=account, fields=["skills", "health", "inventory", "location"])
```

Store session start values:
- Starting XP for Attack, Strength, Defence, Hitpoints, Prayer
- Session start time

### 2. XP Calculations

Level 40 requires **37,224** total XP.

```
progress_pct = (current_xp / 37224) * 100
remaining_xp = 37224 - current_xp
xp_per_hour = (gained_xp / session_minutes) * 60
eta_hours = remaining_xp / xp_per_hour
```

### 3. Adaptive Monitoring Intervals

Use **FOREGROUND** sleeps with `Bash("sleep {seconds}")`.

| Condition | Interval |
|-----------|----------|
| HP < 50% or food < 5 | 2 min |
| XP not changing | 2 min |
| Session < 10 min | 2 min |
| Session 10-20 min | 5 min |
| Session 20-40 min | 10 min |
| Session 40-60 min | 15 min |
| Session 60+ min | 30 min |

### 4. Health Checks Each Interval

- **State file stale > 30s**: Alert user, try `auto_reconnect`
- **HP = 0**: Character may be dead
- **Food = 0 and HP < 50%**: Warn user
- **XP unchanged 2 checks**: Restart kill loop
- **Combat IDLE with no XP gain**: Restart kill loop

### 5. Auto-Recovery Actions

```python
# Kill loop stopped
send_command(account_id=account, command="KILL_LOOP Giant_frog 1000")

# Client frozen
check_health(account_id=account)
# If stale, alert user

# Disconnected
auto_reconnect(account_id=account)
```

### 6. Monitoring Loop

```
LOOP FOREVER:
  1. get_game_state()
  2. Calculate gains since session start
  3. Display progress table
  4. Check health/status
  5. Determine next interval
  6. Print "Status: ✅ Training normally | Next check: X min"
  7. Bash("sleep {seconds}")  # FOREGROUND sleep
  8. Repeat
```

## Status Messages

- `✅ Training normally` - XP increasing, HP good
- `⚠️ Low HP/food` - HP < 50% or food < 5
- `🔄 Restarted loop` - Kill loop was restarted
- `❌ Needs attention` - Frozen/disconnected

## Example Output

```
┌──────────────────────────────────────────────────────────┐
│  LOSTimposter @ Giant Frogs      ❤️ 29/31    🍖 15 Tuna   │
├──────────────────────────────────────────────────────────┤
│  Skill   Lvl   Progress to 40            Remaining       │
├──────────────────────────────────────────────────────────┤
│  ⚔️ Att   22   [###-------------] 17%    31,024 XP       │
│  💪Str    38   [#############---] 85%     5,616 XP       │
│  🛡️ Def   20   [##--------------] 12%    32,676 XP       │
│  ❤️ HP    31   [######----------] 41%    22,118 XP       │
├──────────────────────────────────────────────────────────┤
│  📈 Session: +1,676 Att   ~3k/hr   ETA 40: ~10 hrs       │
│  🙏 Bonus:   +285 Prayer  (Big Bones)                    │
└──────────────────────────────────────────────────────────┘

Status: ✅ Training normally | Next check: 5 min
```

## XP Reference Table

| Level | Total XP |
|-------|----------|
| 20 | 4,470 |
| 30 | 13,363 |
| 40 | 37,224 |
| 50 | 101,333 |
| 60 | 273,742 |
