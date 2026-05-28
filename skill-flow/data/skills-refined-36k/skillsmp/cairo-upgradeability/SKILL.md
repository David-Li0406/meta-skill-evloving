---
name: cairo-upgradeability
description: Explain Starknet upgradeability via class hash replacement and proxy patterns; use when a request involves upgrading contract logic or replace_class_syscall.
---

# Cairo Upgradeability

## Overview
Explain how Starknet upgrades work and the safeguards commonly used.

## Quick Use
- Read `references/upgradeability.md` before answering.
- Mention `replace_class_syscall` and access control.
- Suggest proxy patterns for more flexible upgrades.

## Response Checklist
- Use a protected upgrade entry point that validates the new class hash.
- Explain that upgrades replace the class hash of an instance.
- Note that storage is preserved across upgrades.

## Example Requests
- "How do I upgrade a Starknet contract?"
- "What does replace_class_syscall do?"
- "Why do I need access control for upgrades?"
