---
name: new-chat
description: "Start an AiGov session by reading AGENTS + EVALSETS and proposing the smallest next PR with verification and effort label."
---

## Read (in order)
1) /AGENTS.md
2) /packages/specs/docs/program/EVALSETS.yaml

## Output (required)
- Current state summary (8–12 bullets)
- Ask for single outcome for this session
- Next PR proposal (<=7 steps)
- Verification commands (exact)
- Effort: low / medium / high / xhigh

## Claude check
If the user’s desired outcome implies repo-wide enumeration, independent audit, or long-doc synthesis, propose a Claude lane run (per AGENTS.md) before starting implementation.
