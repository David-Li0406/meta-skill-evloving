# Root Cause Analysis Tools Reference

## Overview

Root cause analysis requires structured approaches to move from symptoms to true causes. This reference covers the primary tools used in 8D problem solving.

---

## 5-Why Analysis

### Purpose

Drill down from symptom to root cause by repeatedly asking "why" until the fundamental cause is reached.

### When to Use

- Simple, linear cause-effect chains
- Single failure modes
- Quick initial analysis
- When cause relationships are clear

### How to Conduct

1. **State the problem clearly**
2. **Ask "Why did this happen?"**
3. **Answer with a verifiable fact**
4. **Repeat until root cause is reached** (typically 3-7 levels)
5. **Verify each level**

### 5-Why Guidelines

| Do | Don't |
|----|----|
| Use facts, not assumptions | Jump to conclusions |
| Verify each "because" | Stop at blame |
| Stay in your control | Accept "they didn't" |
| Branch when needed | Force exactly 5 whys |
| Stop when actionable | Stop too early |

### Example: Dimension Out of Spec

```
Problem: Shaft OD measures 25.08mm (spec: 25.00 ±0.03mm)

Why 1: Why is the OD oversize?
→ Because the tool cut undersize, leaving extra material

Why 2: Why did the tool cut undersize?
→ Because tool wear offset wasn't updated

Why 3: Why wasn't the offset updated?
→ Because the operator didn't check wear during the run

Why 4: Why didn't the operator check wear?
→ Because the work instruction doesn't specify when to check

Why 5: Why doesn't the WI specify this?
→ Because it was never updated after tooling change last month

ROOT CAUSE: Work instruction gap - no defined wear check interval
```

### Common 5-Why Mistakes

| Mistake | Example | Problem |
|---------|---------|---------|
| Stopping too early | "Operator error" | Not actionable, not root cause |
| Jumping levels | Skipping logical steps | Miss real cause |
| Assumptions | "Because they always do that" | Not verified |
| Blame | "Because Bob didn't care" | Not constructive |
| Too abstract | "Management didn't support" | Not actionable |

---

## Fishbone Diagram (Ishikawa / Cause-and-Effect)

### Purpose

Brainstorm all potential causes in a structured format before narrowing down.

### When to Use

- Complex problems with multiple potential causes
- Team brainstorming sessions
- When root cause is unclear
- To ensure all categories are considered

### Structure (6M Categories)

```
                                    ┌─────────────────┐
                                    │    PROBLEM      │
                                    │   STATEMENT     │
                                    └────────┬────────┘
                                             │
        ┌────────────────┬───────────────────┼───────────────────┬────────────────┐
        │                │                   │                   │                │
   ┌────┴────┐      ┌────┴────┐         ┌────┴────┐         ┌────┴────┐      ┌────┴────┐
   │   MAN   │      │ MACHINE │         │MATERIAL │         │ METHOD  │      │MEASURE │
   └─────────┘      └─────────┘         └─────────┘         └─────────┘      └─────────┘
        │                │                   │                   │                │
   - Training      - Maintenance       - Specification      - Procedure     - Calibration
   - Experience    - Capability        - Lot variation      - Sequence      - Resolution
   - Fatigue       - Settings          - Storage            - Setup         - Method
   - Attention     - Wear              - Contamination      - Handling      - Repeatability

                                    ┌─────────────────┐
                                    │   ENVIRONMENT   │
                                    │ (Mother Nature) │
                                    └─────────────────┘
                                             │
                                   - Temperature
                                   - Humidity
                                   - Vibration
                                   - Cleanliness
```

### 6M Categories Explained

| Category | Also Called | Questions to Ask |
|----------|-------------|------------------|
| **Man** | People | Training? Skill? Experience? Fatigue? New? |
| **Machine** | Equipment | Maintained? Capable? Settings? Wear? |
| **Material** | Input | In-spec? Lot change? Storage? Contamination? |
| **Method** | Process | Procedure? Followed? Clear? Complete? |
| **Measurement** | Inspection | Calibrated? Capable? Resolution? Method? |
| **Mother Nature** | Environment | Temperature? Humidity? Vibration? Clean? |

### Fishbone Construction Steps

1. **Write problem statement** at fish head (right)
2. **Draw main spine** and category branches
3. **Brainstorm causes** under each category
4. **Add sub-causes** branching from main causes
5. **Circle likely causes** for investigation
6. **Verify circled causes** with data

### Example: Surface Finish Defect

```
                                    ┌─────────────────┐
                                    │ Surface finish  │
                                    │ Ra >3.2 μm      │
                                    └────────┬────────┘
                                             │
   MAN                MACHINE            MATERIAL            METHOD
   - New operator     - Spindle wear     - Material hardness - Feed rate too high
   - Training gap     - Vibration        - Bar stock finish  - Wrong insert
   - Fatigue          - Coolant flow     - Heat treat var.   - Depth of cut
                      - Insert wear ●    - Contamination     - Speed setting ●

   MEASUREMENT         ENVIRONMENT
   - Ra gage error     - Temperature
   - Surface std       - Coolant temp
   - Inspection freq   - Chips buildup ●

   ● = Likely causes to investigate
```

---

## IS / IS NOT Analysis

### Purpose

Define problem boundaries precisely by comparing what the problem IS versus what it IS NOT (but could be).

### When to Use

- Complex problems with unclear scope
- When similar items are not affected
- To narrow down potential causes
- D2 problem definition

### IS / IS NOT Template

| Factor | IS | IS NOT | Distinction |
|--------|-----|--------|-------------|
| **WHAT - Object** | What has the problem? | What similar doesn't? | What's different? |
| **WHAT - Defect** | What is wrong exactly? | What could be wrong but isn't? | |
| **WHERE - On object** | Where on the part? | Where isn't it? | |
| **WHERE - Geographic** | Where found/produced? | Where isn't it found? | |
| **WHEN - First observed** | When first seen? | When not seen? | |
| **WHEN - Lifecycle** | When in process? | When not in process? | |
| **WHEN - Pattern** | Trend? Cycle? | Constant? Random? | |
| **EXTENT - How many** | How many affected? | How many not affected? | |
| **EXTENT - How much** | Size of defect? | What would be larger? | |

### Example: Thread Damage

| Factor | IS | IS NOT | Distinction |
|--------|-----|--------|-------------|
| **WHAT - Object** | Part #12345 | Part #12346 (same thread) | Different lot dates |
| **WHAT - Defect** | Stripped threads | Cross-threaded, undersized | Force applied after formed |
| **WHERE - On part** | First 3 threads | Middle/bottom threads | Assembly entry point |
| **WHERE - Found** | Customer assembly | Our inspection, in-transit | Handling at customer |
| **WHEN - First** | Jan 15 shipment | Before Jan 15 | Something changed |
| **WHEN - Process** | After threading op | During threading | Post-process damage |
| **EXTENT - How many** | 12 of 500 (2.4%) | Other 488 (97.6%) | Intermittent |

**Distinctions point to:** Handling at customer, assembly process, intermittent occurrence

---

## Comparative Analysis

### Purpose

Identify differences between good and bad items or conditions.

### When to Use

- When identical parts have different results
- When problem is intermittent
- When process seems unchanged
- To isolate variables

### Comparison Factors

| Factor | Good | Bad | Difference |
|--------|------|-----|------------|
| Machine | | | |
| Operator | | | |
| Shift | | | |
| Material lot | | | |
| Date/time | | | |
| Setup | | | |
| Tooling | | | |
| Parameters | | | |

### Example

| Factor | Good Parts | Bad Parts | Difference |
|--------|------------|-----------|------------|
| Machine | DMU 50 | DMU 50 | Same |
| Operator | A, B, C | A, B, C | Same |
| Shift | Day, Night | Day, Night | Same |
| Material lot | Lot 2024-A | Lot 2024-B | **Different** |
| Date | Jan 10-14 | Jan 15-16 | **Different** |
| Tool | T12 insert | T12 insert | Same |

**Conclusion:** Material lot change correlates with defect

---

## Fault Tree Analysis (FTA)

### Purpose

Systematic top-down analysis of all failure paths for complex systems.

### When to Use

- Complex failure modes
- Safety-critical analysis
- Multiple potential failure paths
- System-level problems

### Symbols

| Symbol | Name | Meaning |
|--------|------|---------|
| Rectangle | Event | Failure being analysed |
| Circle | Basic Event | Root cause (no further breakdown) |
| AND gate | AND | All inputs required for output |
| OR gate | OR | Any input causes output |
| Diamond | Undeveloped | Not analysed further |

### Example: Machine Stop

```
                    ┌─────────────────┐
                    │  Machine Stop   │
                    │    (TOP)        │
                    └────────┬────────┘
                             │
                          ┌──┴──┐
                          │ OR  │
                          └──┬──┘
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────┴──────┐ ┌─────┴─────┐ ┌──────┴──────┐
       │ Power Loss  │ │  Alarm    │ │ Mechanical  │
       └──────┬──────┘ └─────┬─────┘ └──────┬──────┘
              │              │              │
           ┌──┴──┐        ┌──┴──┐        ┌──┴──┐
           │ OR  │        │ OR  │        │ OR  │
           └──┬──┘        └──┬──┘        └──┬──┘
              │              │              │
        ┌─────┼─────┐   ┌────┼────┐   ┌────┼────┐
        │     │     │   │    │    │   │    │    │
        ○     ○     ○   ○    ○    ○   ○    ○    ○
      Mains Breaker UPS Tool Temp Part Way  Ball Lube
      fail  trip  fail  wear alarm jam  screw fail
                                      wear
```

---

## Timeline Analysis

### Purpose

Map sequence of events to identify when problem started and what changed.

### When to Use

- Process-related problems
- When "something changed"
- To correlate events with defect onset
- Investigation of complex sequences

### Timeline Format

```
Date/Time    Event                                    Significance
─────────────────────────────────────────────────────────────────────
Jan 10       Last known good production               Baseline
Jan 11       New material lot received                Potential change
Jan 12 AM    Maintenance replaced spindle bearing    Potential change
Jan 12 PM    First defect detected                   Problem start
Jan 13       Defect continues at 5% rate             Confirms pattern
Jan 14       Containment initiated                   Response
```

### Questions for Timeline

1. When was last known good?
2. What changed between good and bad?
3. When was defect first produced (not detected)?
4. Is there a pattern (shift, day, batch)?
5. Did anything else change at that time?

---

## Tool Selection Guide

| Situation | Recommended Tool(s) |
|-----------|---------------------|
| Simple, single cause | 5-Why |
| Complex, unknown causes | Fishbone → 5-Why |
| Good vs bad comparison | IS/IS NOT, Comparative |
| Intermittent problem | IS/IS NOT, Timeline |
| System failure | Fault Tree |
| Something changed | Timeline, Comparative |
| Team brainstorming | Fishbone |

---

## Combining Tools

Typical analysis flow:

1. **Timeline** - Establish sequence of events
2. **IS/IS NOT** - Define problem boundaries
3. **Fishbone** - Brainstorm all potential causes
4. **Comparative** - Compare good vs bad
5. **5-Why** - Drill down on likely causes
6. **Verify** - Reproduce or eliminate to confirm

---

## Verification Summary

| Verification Type | Description | Confidence |
|-------------------|-------------|------------|
| **Reproduction** | Re-create defect by applying cause | Highest |
| **Elimination** | Remove cause, verify defect stops | High |
| **Correlation** | Statistical relationship in data | Medium-High |
| **Expert judgment** | SME agrees cause is likely | Medium |
| **Literature** | Known failure mode | Medium |

Always prefer reproduction or elimination verification when possible.
