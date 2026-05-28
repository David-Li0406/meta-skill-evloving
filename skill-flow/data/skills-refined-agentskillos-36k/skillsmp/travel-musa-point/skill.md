---
name: travel-musa-point
description: Travel from Port Sarim to Musa Point (Karamja) via boat
tags: [travel, karamja, musa-point, boat, fishing, lobster]
---

# Travel to Musa Point Skill

**Purpose:** Travel from Port Sarim to Musa Point (Karamja) for lobster fishing.

**When to use:**
- Need to get to Karamja for fishing (lobsters, tuna, swordfish)
- Starting a fishing trip from the mainland

**Cost:** 30 coins (fare)

---

## CRITICAL: Right-Click Travel Pattern

**IMPORTANT:** To travel via boat NPCs, you must **right-click** and select **"Travel"**.

The dock workers (Captain Tobias, etc.) have multiple actions:
- Talk-to (default left-click - DON'T USE)
- Travel (right-click menu - USE THIS)
- Examine

The `INTERACT_NPC` command handles this correctly by selecting the specified action from the right-click menu.

---

## Route Details

| From | To | NPC | Action | Cost |
|------|-----|-----|--------|------|
| Port Sarim (3027, 3217) | Musa Point (2954, 3147) | Captain_Tobias | Travel | 30gp |
| Musa Point (2954, 3147) | Port Sarim (3027, 3217) | Customs_officer | Travel | 30gp |

---

## Execution Steps

### 1. Verify Starting Location

Check if player is at Port Sarim docks:
```
get_game_state()
# Should be near (3027, 3217, plane 0)
```

If not at Port Sarim, navigate there first or handle appropriately.

### 2. Walk Close to Captain Tobias

**IMPORTANT:** The NPC must be visible in the viewport for clicks to work.

```
send_and_await(
    command="GOTO 3027 3217 0",
    await_condition="location:3027,3217",
    timeout_ms=10000
)
```

Captain Tobias is at approximately (3027, 3216).

### 3. Right-Click Travel on Captain Tobias

```
send_and_await(
    command="INTERACT_NPC Captain_Tobias Travel",
    await_condition="location:2954,3147",
    timeout_ms=20000
)
```

**Key points:**
- Use underscores for multi-word NPC names: `Captain_Tobias`
- The action is `Travel` (not "Pay-fare" or "Talk-to")
- Wait for arrival at Musa Point coordinates

### 4. Verify Arrival

After the boat ride, player should be at Musa Point:
- Location: ~(2954, 3146, plane 0)
- Nearby: Fishing spots, Stiles (note exchange NPC), Luthas (banana plantation)

---

## Common Failures

### NPC Outside Viewport
```
WARN: NPC 'Captain Tobias' is outside viewport bounds
```
**Fix:** Walk closer to the NPC first with GOTO command.

### Wrong Action Name
```
ERROR: Menu option not found: option='Pay-fare'
```
**Fix:** The action is `Travel`, not `Pay-fare`.

### Insufficient Coins
If you have < 30 coins, the travel will fail. Ensure inventory has coins.

---

## Return Trip (Musa Point → Port Sarim)

To return from Karamja:
```
send_and_await(
    command="GOTO 2953 3146 0",
    await_condition="location:2953,3146",
    timeout_ms=8000
)

send_and_await(
    command="INTERACT_NPC Customs_officer Travel",
    await_condition="location:3027,3217",
    timeout_ms=20000
)
```

---

## Full Example

```python
# 1. Get close to dock
send_and_await("GOTO 3027 3217 0", "location:3027,3217", timeout_ms=8000)

# 2. Right-click Travel on Captain Tobias
send_and_await(
    "INTERACT_NPC Captain_Tobias Travel",
    "location:2954,3147",
    timeout_ms=20000
)

# 3. Verify arrival
state = get_game_state()
# state.player.location should be ~(2954, 3146)

# Now at Musa Point - ready for lobster fishing!
```

---

## Related Locations

After arriving at Musa Point:
- **Fishing spots:** East along the dock (~2924, 3178)
- **Stiles (note exchange):** North of dock for banking fish as notes
- **Banana plantation:** West for Banana picking (quest/money)
