---
name: smart-reminder-logic
description: Generates "Nudge" logic for pill reminders. Use this when building notification features.
---

# Goal
Create a persistent reminder system that fights "Time Blindness."

# Instructions
1. Extract the `target_time` from the user's request.
2. Run `python scripts/nudge_engine.py [time]` to generate a schedule.
3. Implement the resulting 3-step notification cycle in the app code.

## Notification Cycle
- **Soft Nudge (+5 min)**: Gentle, low-priority reminder.
- **Medium Nudge (+15 min)**: Standard persistence.
- **CRITICAL Alert (+30 min)**: High intensity to break hyperfocus.
