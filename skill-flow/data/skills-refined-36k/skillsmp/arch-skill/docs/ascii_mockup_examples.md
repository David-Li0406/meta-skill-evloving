# ASCII Mockup References (UI Work)

These are real examples pulled from existing docs to serve as reference patterns when an architecture plan includes UI changes.

---

## Betting controls — action row + sizing popover
Source: `/Users/aelaguiz/workspace/sandbox1/psmobile/docs/play-vs-ai-skia-action-controls.md`

Base controls:
```ascii
┌─────────────────────────────────────────────┐
│ [ Fold ]     [ Check / Call ]     [ Bet/Raise ] │
└─────────────────────────────────────────────┘
```

Sizing popover (structure):
```ascii
                         ┌──────────────────────┐
                         │  ALL-IN   980        │
                         │  POT      30         │
                         │  3 BB     60   ┃     │
                         │  2 BB     40   ┃  ●  │
                         │  MIN      20   ┃     │
                         └──────────────────────┘
                                        ▲
                           vertical slider w/ thumb
```

---

## Post‑puzzle results — bottom sheet (collapsed)
Source: `/Users/aelaguiz/workspace/psmobile4/docs/post_puzzle_ux.md`

```ascii
┌──────────────────────────────────┐
│  ★★☆  GOOD PLAY                  │
│  +18 XP            Skill +2      │
│──────────────────────────────────│
│ Your choice: CALL                │
│ Best line:  FOLD ✅              │
│                                  │
│ Key takeaway:                    │
│ "Reverse implied odds OOP."      │
│                                  │
│ [ View breakdown ▾ ]      [i]    │
│──────────────────────────────────│
│  [ Continue ]                    │
│  Practice this spot   Try again  │
└──────────────────────────────────┘
```

---

## Notes for arch_skill usage
- ASCII mocks are **contract-level**, not just illustrative.
- Include both **current** and **target** states when proposing UI changes.
- Keep ASCII aligned with actual layout constraints (spacing, hierarchy, labels).

