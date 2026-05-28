---
name: action-oriented-ux
description: Use this skill when designing sales engagement interfaces and workflows that prioritize quick actions on leads, aiming for a time-to-action of under 2 minutes.
---

# Action-Oriented Dashboard Design

## Purpose

Build action-oriented market intelligence dashboards where the primary output is **personalised outreach**. The goal is to reduce time-to-action to **under 2 minutes** per lead while maintaining quality and personalisation.

## Core Philosophy: From Insight to Orchestration

Traditional dashboards often lead users to spend 80% of their time navigating and only 20% acting. **Modern platforms invert this ratio.** The interface functions less like a library and more like a **playlist**, where AI-driven prioritisation pre-loads the next best action.

### The "System of Action" Philosophy

| Decision | Legacy (User Decides) | Modern (System Decides) |
|----------|----------------------|------------------------|
| **Who** | Browse list, pick someone | AI-ranked priority queue |
| **When** | Check calendar, guess timing | Timing signals + decay |
| **What** | Write from scratch | Pre-drafted with variables |
| **How** | Choose channel | Recommended based on context |

**The user executes, not manages.**

---

## The 2-Minute Lead Loop

| Time | Activity |
|------|----------|
| 0:00-0:05 | System highlights next prioritised lead (auto-selected, context pre-loaded) |
| 0:05-0:30 | User scans "Why now" signals + last touch |
| 0:30-1:30 | User reviews draft + edits 1-3 fields (opener, hook, CTA) |
| 1:30-2:00 | Send/log/advance with non-blocking feedback |

---

## Layout Architecture: The Three-Zone Model

### The Split-Screen Player

```
┌──────────┬─────────────────────────┬───────────────────┐
│  QUEUE   │        CONTEXT          │      ACTION       │
│  (Left)  │        (Centre)         │   (Right/Dock)    │
│  30-40%  │        40-50%           │      20-30%       │
└──────────┴─────────────────────────┴───────────────────┘
```

| Zone | Purpose | Key Features |
|------|---------|--------------|
| **Queue** | Prioritised lead list | "Why now" chips, channel badge, signal badges |
| **Context** | Lead intelligence | Profile, history, talking points, research tiles |
| **Action** | Execution workspace | Composer, dialer, or LinkedIn task panel |

### Why Split-Screen Wins

- **Co-existence:** See list (macro) and details (micro) simultaneously
- **Referenceability:** Look at data while typing message
- **Stability:** Navigation controls stay fixed for muscle memory
- **Portability:** Same pattern works as browser extension overlay

---

## The Focus Zone: Tasks, Not Charts

Replace "Dashboard of Charts" with **Dashboard of Tasks**.

- Ingest signals from buyer intent, CRM, communications
- Prioritise into a single AI-ranked list
- Emphasise *next step* rather than account history
- Present as imperative: "Call John Doe - High Intent Signal"

### Signal Badging

Prioritise **Urgency** and **Impact** over **Recency**.

| Badge | Meaning |
|-------|---------|
| 🔥 Fire | High intent |
| ⏰ Clock | Scheduled follow-up |
| 💰 Money | Funding event |
| 📈 Chart | Growth signal |
| 🔄 Refresh | Re-engaged after cold |

### Grouping Strategies

| Grouping | Benefit |
|----------|---------|
| **By Account** | Static context, reduced cognitive load |
| **By Sequence** | Same script, calling rhythm |
| **By Channel** | Tool switching minimised |
| **By Time Zone** | Real-time availability |

---

## Inline Actions vs Modals vs Sidebars

| Pattern | Use When | Speed |
|---------|----------|-------|
| **Inline** | Binary/single-click (star, skip, snooze) | Fastest |
| **Sidebar/Drawer** | Reference context while acting | Fast |
| **Modal** | High-attention confirmations only | Slow |
| **Full Page** | Complex editing (sequence builder) | Slowest |

**Rule:** If a task is repeatable, make it completable on the main page. Modals block context and interrupt workflow.

---

## Message Composition UX

### The "Review-First" Model

Users **review and augment** pre-drafted content, not write from scratch.

**Variable States:**
- ✅ **Resolved (blue):** `[John]` — data merged correctly
- ⚠️ **Missing (yellow/red):** `[job_title]` — requires manual fix
- 🔒 **Send blocked** until all required variables resolved

### Structured Personalisation ("Mad Libs")

Present 2-4 high-leverage editable fields:
- Opening line
- Why reaching out
- Call to action

### Talking Points as One-Click Inserts

Clicking a talking point chip inserts a pre-formatted sentence at cursor position.

---

## Keyboard Navigation

Every action accessible via keyboard:

| Shortcut | Action |
|----------|--------|
| `J` / `K` | Move down/up in list |
| `Enter` | Select lead / Open detail |
| `E` | Compose email |
| `C` | Log call |
| `L` | Open LinkedIn |
| `S` | Skip (with reason) |
| `Z` | Snooze |
| `⌘Enter` | Send message |
| `Esc` | Close panel / Cancel |
| `⌘K` | Command palette |

---

## Non-Blocking Feedback

### Toast Notifications

- **Placement:** Bottom-left (avoids navigation)
- **Content:** Action + recipient name
- **Actions:** Undo button, dismiss
- **Duration:** 5-30 seconds (configurable)
- **Stacking:** Multiple toasts stack or aggregate

### Visual Momentum

Instead of modal confirmation:
- Completed item slides out
- Progress bar increments
- Next item slides in
- Motion conveys completion

### Micro-Analytics

```
Today: 12/50 tasks ████████░░░░░░░░░░░ 24%  •  Avg: 1:42/lead
```

---

## Undo and Error Recovery

### Undo Send Buffer

1. User clicks "Send"
2. System delays actual API call for 5-30 seconds
3. Toast shows countdown with Undo button
4. Clicking Undo stops send, reopens draft
5. After buffer expires, message transmits

### Undo Restores Full State

- Restore lead as "active" in queue
- Reopen composer with last draft
- Restore cursor position and selection

### Non-Blocking Error States

Validation errors should NOT throw blocking modals:
1. Mark item as "Skipped/Error" in list (red badge)
2. Auto-advance to next valid lead
3. User returns to "Error Bucket" at session end
4. Separates "Flow time" from "Fix time"

---

## Queue and Batch Processing

### Flow Mode vs Batch Mode

| Mode | Best For |
|------|----------|
| **Flow Mode** | First touch (needs personalisation) |
| **Batch Mode** | Follow-ups, breakup emails (generic) |

### Skip and Snooze

Reasons feed prioritisation and suppression rules:
- [No contact info] [Not ICP] [Already engaged] [Later]

Snooze options:
- [1 hour] [Tomorrow] [3 days] [Next week] [Custom...]

---

## Pre-Computation of Intent

| Pre-Computation | User Benefit |
|-----------------|--------------|
| **Pre-selection** | No channel choice needed |
| **Pre-population** | No blank page |
| **Pre-flagging** | No embarrassing `{First_Name}` sends |
| **Pre-fetching** | Zero transition latency |
| **Auto-navigation** | No "Next" button required |

**The "Lean-Back" Experience:** Software drives the pace. User executes pre-curated tasks.

---

## Implementation Checklist

### Phase 1: Core Loop (Week 1-2)
- Queue + detail + docked composer (no page navigation)
- One recommended channel with split-button for others
- Review-first drafted message with variable highlighting
- Non-blocking toast confirmation with auto-advance
- Basic j/k navigation + Enter to select

### Phase 2: Speed Features (Week 3-4)
- ⌘K command palette
- Full keyboard shortcut set
- Undo send buffer (configurable 5-30s)
- Skip/Snooze with reason tracking
- Pre-fetch next lead

### Phase 3: Personalisation (Week 5-6)
- Structured personalisation fields
- Talking points as one-click inserts
- Diff from template view
- Missing variable blocking

### Phase 4: Flow Optimisation (Week 7+)
- Account grouping for context preservation
- Error bucket for post-session resolution
- Micro-analytics in header

---

## Summary Principles

1. **Dashboard of Tasks, Not Charts** — Present imperatives, not data
2. **Pre-compute Intent** — Anticipate user needs before expressed
3. **Sidebar Over Modal** — Maintain context visibility during action
4. **Review-First Composition** — Users augment, not write from scratch
5. **One Default Channel** — Reduce choice paralysis
6. **Keyboard-First** — Every action accessible without mouse
7. **Optimistic UI** — Assume success, process in background
8. **Non-Blocking Feedback** — Toast + Undo, not confirmation modals
9. **Undo as Safety Net** — Enable speed by enabling recovery
10. **Flow Over Batch** — Emphasise quality for first touch

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Time to Action** | <2 minutes |
| **Actions per Hour** | 30+ |
| **Skip Rate** | <15% |
| **Undo Rate** | <5% |
| **Error Rate** | <2% |