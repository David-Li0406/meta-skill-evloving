---
name: command-diagnostics
description: Diagnose why manny plugin commands failed and suggest specific fixes
tags: [diagnostics, debugging, commands, troubleshooting]
---

# Command Diagnostics Skill

**Purpose:** Automatically diagnose why a manny plugin command failed and provide specific, actionable fixes.

**When to use:**
- Command returns error message (e.g., "NPC not found", "Bank not found", "Spell widget not found")
- Command completes but doesn't produce expected result
- Player gets stuck or enters "Idle" state unexpectedly
- Testing new commands or routines
- User asks "why didn't X work?"

---

## Execution Steps

### 1. Gather Current Context

Always start by collecting the current game state:

```python
# Get current game state
game_state = get_game_state()

# Get recent logs (last 60 seconds)
logs = get_logs(level="ALL", since_seconds=60)

# Get last command response
response = get_command_response()
```

**Extract key information:**
- Player position: `game_state['player']['position']`
- Player animation/state: `game_state['player']['animation']`
- Inventory contents: `game_state['inventory']`
- Equipment: `game_state['equipment']`
- Any error messages in logs or response

### 2. Diagnose by Command Type

Different command types have different common failure modes:

#### NPC Interaction Commands (ATTACK_NPC, INTERACT_NPC, CAST_SPELL_NPC)

**Common Issues:**
1. **"NPC not found"** - Distance too far or name mismatch
2. **Wrong NPC targeted** - Multiple NPCs with similar names
3. **Prerequisites not met** - Tab not open, items missing

**Diagnosis Steps:**
```python
# Check what NPCs are actually nearby
query_nearby(npc_name_filter="<npc_name>")

# Check distance (ATTACK_NPC likely has <5 tile limit)
# If NPCs found at >5 tiles: distance issue
# If no NPCs found: name mismatch or area issue

# For CAST_SPELL_NPC specifically:
scan_widgets(filter_text="<spell_name>")  # Is magic tab open?
# Check game_state['inventory'] for required runes
```

**Fixes:**
- **Distance issue:** Add `GOTO <x> <y> <z>` to get within 3-5 tiles first
- **Name mismatch:** Use `query_nearby()` to get exact NPC name (case-sensitive)
- **Missing prerequisites:** Open magic tab (F6), ensure runes in inventory
- **Alternative:** Use higher-level commands like `KILL_LOOP` instead of `ATTACK_NPC`

#### Banking Commands (BANK_OPEN, BANK_DEPOSIT_ALL, BANK_WITHDRAW)

**Common Issues:**
1. **"Bank not found"** - Too far from bank or wrong location
2. **Bank already open** - Command called when bank UI active
3. **Item not found** - Wrong item name or not in bank

**Diagnosis Steps:**
```python
# Check nearby objects for banks
query_nearby(object_name_filter="Bank")

# Check if bank UI is already open
scan_widgets(filter_text="Bank of")  # Bank title widget

# For withdrawals, check what's actually in bank
# (may need to manually check or use previous state)
```

**Fixes:**
- **Distance issue:** `GOTO` to bank coordinates first (within 3 tiles)
- **Bank already open:** Check state before opening, or just try withdrawal
- **Item name:** Use exact item name from game (case-sensitive, check hyphens/spaces)

#### Navigation Commands (GOTO, WALK_TO)

**Common Issues:**
1. **Player doesn't move** - Obstacle blocking, invalid coordinates
2. **Player moves but stops short** - Pathfinding failed
3. **Loops back and forth** - Stuck on geometry

**Diagnosis Steps:**
```python
# Check current vs target position
current = game_state['player']['position']
target = [x, y, z]  # From command

# Calculate distance
import math
dist = math.sqrt((current[0] - target[0])**2 + (current[1] - target[1])**2)

# Check if player is animating (walking)
animation = game_state['player']['animation']
# If animation != -1: player is moving
# If animation == -1 and dist > 5: stuck or failed
```

**Fixes:**
- **Stuck:** Find intermediate waypoint, break navigation into steps
- **Invalid coords:** Verify coordinates are walkable (not in walls/water)
- **Alternative:** Use higher-level command if available (e.g., `BANK_OPEN` handles pathfinding)

#### Object Interaction (INTERACT_OBJECT, INTERACT_GAME_OBJECT)

**Common Issues:**
1. **"Object not found"** - Distance, name mismatch, or object not spawned
2. **Wrong object clicked** - Multiple similar objects nearby
3. **Action not available** - Object doesn't support that action

**Diagnosis Steps:**
```python
# Check nearby objects
query_nearby(object_name_filter="<object_name>")

# Verify object has the action you want
# query_nearby returns available actions for each object
```

**Fixes:**
- **Distance:** GOTO within 3-5 tiles
- **Name/action mismatch:** Use exact name and action from `query_nearby` output
- **Not spawned:** Object may be on different tick cycle, wait and retry

#### Skill/Combat Commands (FISH_SPOT, KILL_LOOP, MINE_ROCK)

**Common Issues:**
1. **"No fishing spots found"** - Wrong area or spots not spawned
2. **Loop exits immediately** - No valid targets
3. **Stuck in combat** - Target too strong or healing

**Diagnosis Steps:**
```python
# Check for resource spots/NPCs
query_nearby(npc_name_filter="<target>")
query_nearby(object_name_filter="<target>")

# Check player stats
hp_current = game_state['player']['skills']['hitpoints']['boosted']
hp_max = game_state['player']['skills']['hitpoints']['level']

# For fishing/mining, check if spot is visible
# For combat, check combat level vs NPC level
```

**Fixes:**
- **Wrong area:** GOTO correct coordinates for that resource
- **No targets:** Wait for spawn (spots/rocks respawn on cycles)
- **Combat issues:** Use food, adjust combat style, or find weaker NPCs

### 3. Check Prerequisites

Many commands have hidden prerequisites:

**Common Prerequisites:**
- **Magic commands:** Magic tab open (F6), runes in inventory, spell unlocked
- **Prayer commands:** Prayer tab open (F5), prayer points > 0, prayer unlocked
- **Combat commands:** Weapon equipped, combat style set, auto-retaliate setting
- **Skill commands:** Correct tool equipped, required level, in correct area
- **Banking:** Close enough to bank (<3 tiles), bank not already open

**Diagnosis:**
```python
# Check tabs (widget visibility)
scan_widgets(filter_text="<tab_identifier>")

# Check inventory for required items
inv = game_state['inventory']
# Look for tools, runes, food, etc.

# Check skills for level requirements
skills = game_state['player']['skills']
# Verify player meets level requirement
```

### 4. Analyze Logs for Clues

Recent logs often contain the exact error:

```python
logs = get_logs(level="ERROR", since_seconds=60)
# Look for patterns:
# - "not found" → distance or name issue
# - "null pointer" → plugin bug, needs code fix
# - "timeout" → action took too long, may need retry
# - "interrupted" → shouldInterrupt triggered, normal
```

**Common log patterns:**
- `NPC <name> not found` → Use query_nearby to verify name and distance
- `Could not find widget` → Tab not open or UI state wrong
- `Player is busy` → Previous action still executing, wait
- `Path not found` → Unreachable location, use waypoints

### 5. Generate Actionable Fix

Based on diagnosis, provide ONE of these fix patterns:

**Fix Pattern 1: Add Prerequisites**
```yaml
steps:
  # Add before failing command
  - GOTO: [3092, 3243, 0]  # Get closer
  - OPEN_TAB: MAGIC        # Open magic tab
  - <original_command>
```

**Fix Pattern 2: Use Alternative Command**
```yaml
# Instead of:
- ATTACK_NPC: Goblin

# Use:
- KILL_LOOP: Goblin 10  # Handles distance automatically
```

**Fix Pattern 3: Fix Command Syntax**
```yaml
# Wrong:
- CAST_SPELL_NPC: Fire Bolt Goblin  # Space in spell name

# Right:
- CAST_SPELL_NPC: fire_bolt Goblin  # Underscore
```

**Fix Pattern 4: Add Verification Step**
```yaml
steps:
  - BANK_OPEN: null
  - WAIT: 2                # Give bank time to open
  - BANK_DEPOSIT_ALL: null # Now deposit
```

---

## Output Format

### Summary Section
```
Command Diagnostics Report
==========================
Failed Command: <command_name> <args>
Error: <error_message>

Root Cause: [Distance | Prerequisites | Syntax | Timing | Other]
```

### Diagnosis Section
```
Current State:
- Player Position: [x, y, z]
- Distance to Target: <tiles> tiles
- Prerequisites: [✅ OK | ❌ MISSING: <what>]
- Nearby Entities: <count> found

Investigation:
<what you checked and what you found>
```

### Fix Section
```
Recommended Fix:

Option 1: <description>
[code/yaml block]

Option 2 (Alternative): <description>
[code/yaml block]

Why: <explanation of why this fix works>
```

### Verification Section
```
To Verify Fix:
1. <step to test>
2. <what to observe>
3. <how to confirm success>
```

---

## Cross-References

Use these docs for command details:

- **COMMAND_REFERENCE.md** - All 90 commands with syntax
- **TOOLS_USAGE_GUIDE.md** - MCP tool usage patterns
- **ROUTINE_CATALOG.md** - Working routine examples
- **manny_src/CLAUDE.md** - Plugin implementation details

---

## Known Issues Database

Reference known issues from TODO.md:

### Issue: ATTACK_NPC "NPC not found"
- **Symptom:** NPCs visible in query_nearby but ATTACK_NPC fails
- **Cause:** Distance limit (~5 tiles)
- **Fix:** Use GOTO to get within 3 tiles, or use KILL_LOOP instead

### Issue: CAST_SPELL_NPC "Spell widget not found"
- **Symptom:** Spell command fails despite having runes
- **Cause:** Magic tab not open
- **Fix:** Send F6 keypress or use OPEN_TAB before casting

### Issue: BANK_WITHDRAW "Item not found"
- **Symptom:** Item exists in bank but withdrawal fails
- **Cause:** Item name mismatch (case-sensitive, special characters)
- **Fix:** Use exact item name from query, check for trailing spaces

---

## Success Criteria

✅ **Skill is successful when:**
- Root cause identified within 60 seconds
- Specific fix provided (copy-paste ready)
- Fix is verified to work (or alternatives provided)
- User understands WHY it failed, not just HOW to fix

❌ **Skill fails when:**
- Says "check the logs" without analyzing them
- Suggests "try different coordinates" without calculating distance
- Provides generic advice ("make sure prerequisites are met")
- Doesn't use query_nearby/scan_widgets to verify diagnosis

---

## Example Invocations

### User: "ATTACK_NPC Goblin is failing"

**Workflow:**
```python
1. get_game_state() → player at (3163, 3301, 0)
2. query_nearby(npc_name_filter="Goblin") → 10 goblins found, distances 2-15 tiles
3. get_logs(level="ERROR") → "NPC Goblin not found"
4. Diagnosis: Distance limit, goblins exist but closest is 2 tiles (might need <1 tile?)
5. Fix: Use KILL_LOOP Goblin 10 instead (handles distance automatically)
```

### User: "Why won't my bank routine work?"

**Workflow:**
```python
1. get_game_state() → player at (3000, 3200, 0)
2. query_nearby(object_name_filter="Bank") → No banks found
3. Diagnosis: Player not at bank location
4. Fix: Add GOTO [3092, 3243, 0] before BANK_OPEN
5. Verify: Check distance is <3 tiles after GOTO
```

### User: "CAST_SPELL_NPC fire_bolt Goblin not working"

**Workflow:**
```python
1. scan_widgets(filter_text="Fire Bolt") → Not found
2. Diagnosis: Magic tab not open
3. Check inventory for runes → chaos runes: 0, air runes: 0
4. Diagnosis: ALSO missing runes
5. Fix:
   - BANK_OPEN, withdraw runes
   - Send F6 to open magic tab
   - Retry CAST_SPELL_NPC
```

---

## Important Notes

- **Always verify with tools** - Don't assume, use query_nearby/scan_widgets/get_game_state
- **Check distance first** - Most failures are distance-related (<3-5 tiles)
- **Provide runnable fixes** - User should copy-paste and run immediately
- **Know the 90 commands** - Use list_available_commands() to discover alternatives
- **Test your diagnosis** - If possible, verify the fix works before responding

---

## Testing This Skill

Before deploying, test with these known failures:

1. **ATTACK_NPC failure** - Player too far from NPC
2. **CAST_SPELL_NPC failure** - Magic tab closed
3. **BANK_OPEN failure** - Not near bank
4. **Invalid command syntax** - Typo in command name

Each test should complete diagnosis + provide fix in <60 seconds.
