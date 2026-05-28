---
name: hardware-change-gate
description: Use when changing anything that touches pins, buses, addresses, or hardware init. Forces citation and test checklist.
---

Requirements:
- Cite the exact file/section you are changing (pins_arduino.h, board json, etc.)
- Provide a minimal verification plan:
  - build
  - flash (approval-gated)
  - smoke test checklist
