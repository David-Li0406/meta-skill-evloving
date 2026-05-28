---
name: med-safety-checker
description: Validates medication data against safety records. Use this before displaying drug info to the user.
---

# Goal
Prevent medical "hallucinations" by checking a local database.

# Instructions
1. Read the medication name provided by the user.
2. Run `python scripts/verify_meds.py [medname]` to check for safety warnings.
3. If a warning exists, display it in a Red Box at the top of the screen.

# Examples
Input: "Adderall"
Action: Runs script and finds "Avoid late-day doses to prevent insomnia."
