---
name: when-stuck
description: Use this skill when you're stuck and unsure which problem-solving technique to apply for your specific type of stuck-ness.
---

# When Stuck - Problem-Solving Dispatch

## Overview

Different stuck-types need different techniques. This skill helps you quickly identify which problem-solving skill to use.

**Core principle:** Match stuck-symptom to technique.

## Quick Dispatch

```dot
digraph stuck_dispatch {
    rankdir=TB;
    node [shape=box, style=rounded];

    stuck [label="You're Stuck", shape=ellipse, style=filled, fillcolor=lightblue];

    complexity [label="Same thing implemented 5+ ways?\nGrowing special cases?\nExcessive if/else?"];
    innovation [label="Can't find fitting approach?\nConventional solutions inadequate?\nNeed breakthrough?"];
    patterns [label="Same issue in different places?\nFeels familiar across domains?\nReinventing wheels?"];
    assumptions [label="Solution feels forced?\n'This must be done this way'?\nStuck on assumptions?"];
    scale [label="Will this work at production?\nEdge cases unclear?\nUnsure of limits?"];
    bugs [label="Code behaving wrong?\nTest failing?\nUnexpected output?"];

    stuck -> complexity;
    stuck -> innovation;
    stuck -> patterns;
    stuck -> assumptions;
    stuck -> scale;
    stuck -> bugs;

    complexity -> simp [label="yes"];
    innovation -> collision [label="yes"];
    patterns -> meta [label="yes"];
    assumptions -> invert [label="yes"];
    scale -> scale_skill [label="yes"];
    bugs -> debug [label="yes"];

    simp [label="skills/problem-solving/\nsimplification-cascades", shape=box, style="rounded,filled", fillcolor=lightgreen];
    collision [label="skills/problem-solving/\ncollision-zone-thinking", shape=box, style="rounded,filled", fillcolor=lightgreen];
    meta [label="skills/problem-solving/\nmeta-pattern-recognition", shape=box, style="rounded,filled", fillcolor=lightgreen];
    invert [label="skills/problem-solving/\ninversion-exercise", shape=box, style="rounded,filled", fillcolor=lightgreen];
    scale_skill [label="skills/problem-solving/\nscale-game", shape=box, style="rounded,filled", fillcolor=lightgreen];
    debug [label="skills/debugging/\nsystematic-debugging", shape=box, style="rounded,filled", fillcolor=lightyellow];
}
```

## Stuck-Type → Technique

| How You're Stuck | Use This Skill |
|------------------|----------------|
| **Complexity spiraling** - Same thing 5+ ways, growing special cases | skills/problem-solving/simplification-cascades |
| **Need innovation** - Can't find fitting approach, conventional solutions inadequate | skills/problem-solving/collision-zone-thinking |
| **Patterns repeating** - Same issue in different places, feels familiar across domains | skills/problem-solving/meta-pattern-recognition |
| **Assumptions limiting** - Solution feels forced, stuck on assumptions | skills/problem-solving/inversion-exercise |
| **Scaling concerns** - Will this work at production, edge cases unclear | skills/problem-solving/scale-game |
| **Bugs present** - Code behaving wrong, test failing | skills/debugging/systematic-debugging |