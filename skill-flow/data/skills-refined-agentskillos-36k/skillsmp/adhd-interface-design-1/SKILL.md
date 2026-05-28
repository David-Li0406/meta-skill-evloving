---
name: adhd-interface-design
description: Design productivity dashboards, task management interfaces, and market intelligence platforms optimised for ADHD users. Apply when building UIs requiring cognitive load reduction, single-task focus modes, executive function support, or when the user mentions ADHD accessibility. Provides patterns for initiation support, context preservation, time visualisation, energy-based task management, and gamification that emphasises momentum over streaks. Essential for ADHD users but improves UX for everyone.
user-invocable: false
---

# ADHD-Optimised Interface Design

## Purpose

Design interfaces that function as **cognitive prosthetics** — external systems that actively compensate for executive dysfunction. ADHD is a regulation deficit, not an attention deficit.

## Related Skills

- `action-oriented-ux` — For outreach workflow patterns
- `notification-system` — For alert and notification design
- `uk-police-design-system` — For visual tokens and component specs
- `b2b-visualisation` — For data display patterns

---

## Core Principle: The Prosthetic Model

Traditional interfaces assume consistent executive function, linear planning, reliable working memory, and autonomous inhibition control. For ADHD users, these assumptions create active barriers.

**The interface must replace executive functions that the biological brain struggles to provide.**

---

## The Five Core Requirements

| Requirement | Executive Deficit | Design Principle |
|-------------|------------------|------------------|
| **Minimal Friction** | Cognitive load depletes limited reserves | Every click costs energy; reduce to zero |
| **Clear Single Priority** | Inhibition control failure | Show one thing at a time; hide the rest |
| **Batched Delivery** | Context-switching cost | Consolidate updates; deliver at intervals |
| **Context Always Included** | Working memory deficits | Surface relevant information automatically |
| **Reduced Decision Fatigue** | Decision-making depletes energy | System decides; user executes |

---

## Executive Functions to Externalise

| Function | Implementation |
|----------|----------------|
| **Initiation** | Pre-load next action; one-click start; micro-commitment ("just 2 minutes") |
| **Prioritisation** | AI-ranked queue; one recommendation with "why" |
| **Monitoring** | Visual timers; progress bars; task boundary detection |
| **Memory** | Auto-populated sidebar; What/Why/Next/When/Source on every item |

---

## Key Neurocognitive Patterns

### Working Memory ("The Leaky Bucket")

**Problem:** Users can't remember information from one screen to input on another.

**Solution — Context Capsule:** Auto-populate all relevant context alongside the active task. Every item includes What/Why/Next/When/Source.

### Inhibition Control Failure

**Problem:** Complex dashboards create distraction — every element competes for attention.

**Solution — Visual Isolation:** Active task centred, peripheral elements hidden or deeply dimmed. One thing at a time.

### Time Blindness ("Now" vs "Not Now")

**Problem:** Digital clocks require mathematical translation. Deadlines feel abstract.

**Solution — Spatial Time Visualisation:** Depleting bars, shrinking pies, runway views. Make time passage tangible and visible in peripheral vision.

---

## Cognitive Load Management

| Load Type | ADHD Impact | Solution |
|-----------|-------------|----------|
| **Intrinsic** | High baseline blocks initiation | AI-driven task decomposition |
| **Extraneous** | Near-zero buffer available | Radical minimalism, smart defaults |
| **Germane** | Little capacity for learning | Progressive disclosure, just-in-time instruction |

**Critical:** For ADHD users, extraneous load is a friction multiplier — clutter doesn't merely slow, it causes "executive shutdown."

---

## The 2-Second Comprehension Rule

Every interface element must pass: **Can the user understand what to do within 2 seconds?**

Every item shown must include:
- **What** — The task or item
- **Why** — Why it matters / context
- **Next** — The next action verb
- **When** — Time constraint or deadline
- **Source** — Where this came from

---

## Decision Engineering

| Condition | Who Decides | Rationale |
|-----------|-------------|-----------|
| Low stakes + Reversible + Clear dominant option | **System** | Don't waste user energy |
| Can infer from behaviour/preferences | **System** | Use past patterns |
| High stakes + Irreversible | **User** | Respect autonomy |
| Preference unclear + High cost of error | **User** | Ask when it matters |

**Smart Defaults:** One recommended option (one-tap), alternatives hidden behind "Or choose..."

**Undo as Safety Net:** Every destructive action reversible for 30 seconds. Enables fast, confident decision-making.

---

## Gamification: Momentum Over Streaks

### The Streak Problem

ADHD users exhibit "all-or-nothing" thinking. When streaks break:
- Disproportionate sense of failure
- "What-the-hell effect" — if broken, why continue?
- Total app abandonment

### Safer Patterns

**Cumulative Visualisation ("Jar of Marbles"):** Show total progress (37 tasks completed, 74% of goal). A missed day doesn't break the jar.

**Forgiving Streaks:** Grace days, streak repair without shame, freeze option for planned breaks, no "you broke it" messaging.

**Reward Process:** Celebrate "Planned" → "Started" → "Completed". Activation is hard for ADHD — reward it explicitly.

---

## Energy-Based Task Management

| Tag | Examples |
|-----|----------|
| **High Energy** | Complex analysis, creative work, difficult conversations |
| **Medium Energy** | Routine work, meetings, coordination |
| **Low Energy** | Filing, simple emails, quick admin |

Provide a "Low Energy Mode" menu with quick wins when user has depleted reserves.

---

## Daily Rituals

### Morning Flow Protocol

1. **Energy check:** "How is your energy today?" [LOW] [MEDIUM] [HIGH]
2. **Review:** Yesterday's unfinished items with [ROLL OVER] or [PARK]
3. **Selection:** AI-recommended priorities based on energy + deadlines
4. **Commitment:** Lock in plan, enter Focus Mode on first task

### End-of-Day Ritual

1. **Done List:** Show wins with completion stats
2. **Brain Dump:** Capture anything on mind for tomorrow
3. **Sign Off:** Clear closure, enable disconnection without FOMO

---

## Implementation Checklist

### Core Components (Build First)

| Component | Features |
|-----------|----------|
| **Now Screen** | One task, timer, Done/Stuck buttons, context sidebar |
| **Batch Digest** | Scheduled delivery, urgency tiers, VIP bypass |
| **Context Capsule** | What/Why/Next/When/Source on every item |
| **Autopilot Recommendations** | One default + undo + "why" explanation |
| **Resume Token** | Return-to-state in one tap |

### Supporting Components

- Parking Lot (capture without switching)
- Energy Matrix (match tasks to capacity)
- Time Visualiser (combat time blindness)
- Morning Flow Wizard (overcome initiation)
- End-of-Day Summary (reduce closing anxiety)

---

## Anti-Patterns to Avoid

| Anti-Pattern | Alternative |
|--------------|-------------|
| 10 competing CTAs | One recommendation + "Other options" |
| Frequent interruptions | Batched delivery + VIP bypass |
| Ambiguous state | Clear confirmations, auto-save |
| No undo, lost work | Always undo, state preservation |
| Visual noise, animations | Calm aesthetic, one accent style |
| Busy dashboards | Focus Mode, progressive disclosure |
| Rigid streaks | Momentum maps, forgiving goals |
| Infinite customisation | Opinionated defaults |
| "Maybe" states | Strict states: Todo/In Progress/Done |
| Overdue shaming | Auto-rollover, compassionate language |

---

## Summary Principles

1. **The Interface is a Prosthesis** — Replaces executive functions, not just displays data
2. **One Thing at a Time** — Visual isolation, single priority, hidden backlog
3. **Decisions Are Expensive** — System decides by default
4. **Context is Memory** — Every item includes What/Why/Next/When/Source
5. **Time Must Be Visible** — Analog visualisation, depleting quantities
6. **Interruptions Are Captures** — Quick capture, auto-return
7. **Batched Not Streamed** — Scheduled digests, not real-time
8. **Momentum Over Perfection** — Cumulative progress, not fragile chains
9. **Match Energy to Tasks** — Energy tagging, flexible scheduling
10. **Celebrate Completion** — Show wins, acknowledge progress
