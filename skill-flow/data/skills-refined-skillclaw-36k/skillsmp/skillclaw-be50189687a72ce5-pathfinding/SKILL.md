---
name: pathfinding
description: Use this skill when requirements are unclear, brainstorming ideas, or when "pathfind", "brainstorm", "figure out", "clarify requirements", or "work through" are mentioned.
---

# Pathfinding

Adaptive Q&A → unclear requirements → clear path.

<when_to_use>

- Ambiguous/incomplete requirements
- Complex features needing exploration
- Greenfield projects with open questions
- Collaborative brainstorming or problem solving

NOT for: time-critical bugs, well-defined tasks, obvious questions

</when_to_use>

<confidence>

| Bar | Lvl | % | Name | Action |
|-----|-----|---|------|--------|
| `░░░░░` | 0 | 0–19 | Prepping | Gather foundational context |
| `▓░░░░` | 1 | 20–39 | Scouting | Ask broad questions |
| `▓▓░░░` | 2 | 40–59 | Exploring | Ask focusing questions |
| `▓▓▓░░` | 3 | 60–74 | Charting | Risky to proceed; gaps remain |
| `▓▓▓▓░` | 4 | 75–89 | Mapped | Viable; push toward 5 |
| `▓▓▓▓▓` | 5 | 90–100 | Ready | Deliver |

Start honest. Clear request → level 4–5. Vague → level 0–2.

At level 4: "Can proceed, but 1–2 more questions would reach full confidence. Continue or deliver now?"

Below level 5: include `△ Caveats` section.

</confidence>

<phases>

Track with TodoWrite. Phases advance only, never regress.

| Phase | Trigger | activeForm |
|-------|---------|------------|
| Prep | level 0–1 | "Prepping" |
| Explore | level 2–3 | "Exploring" |
| Clarify | level 4 | "Clarifying" |
| Deliver | level 5 | "Delivering" |

TodoWrite format — each phase gets context-specific title:

```text
- Prep { domain } requirements
- Explore { approach } options
- Clarify { key unknowns, 3-4 words }
- Deliver { artifact type }
```

Situational (insert before Deliver when triggered):
- Resolve Conflicts → `◆ Caution` or `◆◆ Hazard` pushback
- Validate Assumptions → high-risk assumptions before delivery

Workflow:
- Start: Create phase matching initial confidence `in_progress`
- Transition: Mark current `completed`, add next `in_progress`
- High start (4+): Skip directly to `Clarify` or `Deliver`
- Early delivery: Skip to `Deliver` + `△ Caveats`

</phases>

<gather>

Calibrate first — user may have already provided context (docs, prior conversation, pointed you at files). If enough context exists, skip to level 3–4. Don't re-ask what's already clear.

If gaps remain, explore focus areas (pick what's relevant):
- Purpose: What problem? Why now?
- Constraints: Time, tech, team, dependencies
- Success: How will you measure it?

</gather>