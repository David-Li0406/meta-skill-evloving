---
name: notification-system
description: Design alert systems, notification delivery, and digest emails that surface important signals without overwhelming users. Apply when building notification infrastructure, batched digests, alert classification systems, or morning brief interfaces. Critical for ADHD users and high-volume information environments. Covers multi-axis alert classification, four-tier severity models, batched delivery, ambient awareness patterns, and alert fatigue prevention.
---

# Notification System Design

## Purpose

Design notification systems that surface important buying signals while respecting cognitive limits. Core philosophy: **"Never miss something important" without "constant interruption anxiety."**

## Related Skills

- `adhd-interface-design` — For cognitive load and batching patterns
- `action-oriented-ux` — For toast notifications and undo patterns
- `b2b-visualisation` — For alert severity badges
- `uk-police-design-system` — For semantic colour system

---

## The Core Problem

Standard notification architectures prioritise real-time delivery and uniform visual urgency, inadvertently triggering:
- Executive dysfunction
- Alert fatigue
- Decision paralysis
- Platform abandonment

---

## The Solution: Neuro-Adaptive Signal Engine

Shift from "Push-First" to a system that:
- Treats attention as a **finite, non-renewable resource**
- Adapts the **"Quiet Cockpit" philosophy** from aviation
- Distinguishes between **immediate intervention**, **ambient awareness**, and **scheduled consumption**
- Decouples **information availability** from **interruption**

### Two Goals in Tension (Resolved)

| Goal | Traditional | Our Approach |
|------|-------------|--------------|
| **Don't miss important signals** | Push everything immediately | Persistent placement + escalation ladders |
| **Don't create anxiety** | Let users disable notifications | Batching + ambient awareness + rare interruptions |

---

## Multi-Axis Alert Classification

### The Five Classification Axes

| Axis | Definition |
|------|------------|
| **Urgency** | Time available to respond |
| **Severity/Impact** | Expected impact intensity |
| **Certainty/Confidence** | Probability the alert is "real" |
| **Actionability** | Does it require human action? |
| **Context/Workload** | Is this a bad moment to interrupt? |

### Priority Score Calculation

```
Priority Score = (0.45 × Urgency) + (0.35 × Impact) + (0.20 × Confidence)
```

**Urgency Scores:**
- Hiring surge: 0.9 (24-48h window)
- Follow-up overdue: 0.9
- Follow-up due today: 0.7
- Job posting: 0.6 (≤7d window)
- Market trend: 0.2

**Impact Scores:**
- Key account (strong relationship): 1.0
- Target account (some relationship): 0.7
- General account: 0.4

**Lane Assignment:**
- **Lane A (Interruptive):** Score ≥ 0.80 AND Actionable = true
- **Lane B (Digest):** Score 0.40-0.79
- **Lane C (Ambient):** Score < 0.40

---

## Four-Tier Severity Model

| Tier | Examples | Delivery | Interrupts? |
|------|----------|----------|-------------|
| **Tier 1: Critical** | Key account hiring surge | Push + persistent badge. Bypasses Focus Mode. | **Yes** |
| **Tier 2: High** | Relationship health drop | Top of inbox + Morning Brief | No |
| **Tier 3: Medium** | New job posting | Daily Digest only | No |
| **Tier 4: Low** | Market trends | Dashboard widget only | Never |

---

## Alert Fatigue Prevention

### Causes of Alert Fatigue

| Cause | Impact |
|-------|--------|
| Too many signals | Missed responses |
| Non-actionable alerts | Desensitisation |
| Poor signal quality | Users ignore everything |
| Non-standard presentation | Confusion, delayed recognition |
| High-workload interruptions | Cognitive disruption |

### ADHD-Specific Challenges

- **Compromised filtering** — Difficulty distinguishing relevant from irrelevant
- **Executive function load** — Manual categorisation drains limited resources
- **Time blindness** — Critical alerts "meant to get to" but never acted upon
- **Object permanence** — Dismissed notifications cease to exist mentally

### Prevention Strategies

**From Clinical Alarm Management:**
- Reduce non-actionable alarms at source
- Tune thresholds and require confidence levels
- Make interruptive alerts rare and highly trustworthy

**From Aviation:**
- Reserve "Red" strictly for immediate danger
- Suppress alerts during high workload
- Indicate if alerts are suppressed

---

## Batched Notification Delivery

### Research Evidence

Predictable batches 3×/day improve well-being outcomes versus "endless stream."

**Critical:** Turning notifications off entirely can increase anxiety/FOMO. Batching provides safety net without interruption.

### The Three-Batch Model

| Batch | Time | Content | Function |
|-------|------|---------|----------|
| **Morning Brief** | 8:00-8:30 AM | Tier 2 + Tier 3 overnight; Top 3 priorities | "Start Ritual" |
| **Midday Check** | 12:00-12:30 PM | New opportunities since morning | Maintains awareness |
| **End of Day** | 4:30-5:00 PM | Lower-priority trends; Loose ends | "Closure" |

### The Rule of Three

Each digest highlights **maximum three** critical items at top. Additional items accessible via expansion.

### Two-Lane Delivery Model

```
INCOMING SIGNAL
      │
      ▼
┌─────────────────┐
│ Priority Calc   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
INTERRUPTIVE  DIGEST
(Score ≥0.80) (Score <0.80)
    │         │
    ▼         ▼
Push + Badge  Batched 3×/day
```

### Debouncing

Wait for **Debounce Window** (e.g., 15 minutes) to group related events:

```
Bad:  "Microsoft posted 1 job" → "posted 2 jobs" → ... (15 notifications)
Good: [Wait 15 min] → "Microsoft: 15 New Roles (3 Engineering, 2 Sales...)"
```

---

## Ambient Awareness vs Active Notification

| Surface | Purpose | Interruption |
|---------|---------|--------------|
| **Push notification** | Critical only (Tier 1) | High |
| **Badge on app icon** | Unread count | Medium |
| **In-app inbox** | All alerts, user pulls | Low |
| **Dashboard widget** | Passive awareness | None |
| **Email digest** | Asynchronous consumption | None |

---

## Nagging Protocol for Critical Alerts

For Tier 1 alerts that remain unacknowledged:

| Time Since Alert | Escalation |
|------------------|------------|
| 0-4 hours | Persistent badge in app |
| 4-8 hours | Secondary push notification |
| 8-24 hours | Email reminder |
| 24-48 hours | Highlight in Morning Brief |
| 48+ hours | Manager notification (optional) |

**User Controls:**
- "I've handled this externally" → Resolves without logging
- "Not relevant" → Dismisses with feedback

---

## Noise Control Rules

| Rule | Implementation |
|------|----------------|
| **Threading** | Group by account + signal type + 24h window |
| **Cooldowns** | Max 1 push per account per 24h |
| **Attention budget** | Max 2-3 interruptive pushes/day |
| **Confidence gating** | Low-confidence → never Lane A |
| **Context suppression** | If user viewing account → inline update only |

---

## Visual Design System

### Semantic Colour System

| Tier | Colour | Hex | Usage |
|------|--------|-----|-------|
| **Tier 1 (Critical)** | Coral Red | #FF6B6B | High urgency |
| **Tier 2 (High)** | Amber | #F59E0B | Caution |
| **Tier 3 (Medium)** | Slate Blue | #3B82F6 | Informational |
| **Tier 4 (Low)** | Cool Grey | #6B7280 | Ambient |

### Dual-Coding Requirement

All colour cues must be accompanied by iconography:
- Warning Triangle for critical
- Arrow Up/Down for changes
- Info Circle for informational

---

## User Preference Framework

### Mode Presets

| Mode | Tier 1 | Tier 2 | Best For |
|------|--------|--------|----------|
| **Calm** | Morning Brief only | Morning Brief only | Deep focus |
| **Balanced** | Real-time push | Morning Brief | Most users |
| **Real-Time** | Real-time push | Real-time push | Always-on roles |

---

## Default Configuration

| Signal Type | Delivery | Push? |
|-------------|----------|-------|
| Hiring surge @ key account | Immediate | Yes (budgeted) |
| New job posting | Daily digest | No |
| Relationship decay | Morning Brief | No |
| Market trend | Dashboard widget | Never |
| Follow-up due | Task queue | No |

**"Quiet Cockpit" Default:** Low noise. Only Tier 1 interrupts. User can opt into more.

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Time to Action** | <5 min for Tier 1 |
| **Snooze Rate** | <20% |
| **Digest Open Rate** | >60% |
| **Dismiss Rate (Not Relevant)** | <10% |
| **Interruptive Volume** | ≤2/day |

---

## Summary Principles

1. **Attention is finite** — Defend it, don't exploit it
2. **Quiet Cockpit** — Only anomalies generate alarms
3. **Predictability beats cleverness** — 3 batches/day > ML-optimised timing
4. **Persistence over pinging** — Items stay visible until resolved
5. **Opportunity framing** — Never punitive, always supportive
6. **One-click actions** — Bridge knowing and doing
7. **Dual coding** — Colour + icon for every state
8. **Rare and trustworthy** — Interruptive alerts must earn credibility
9. **Context-aware snoozing** — "When I view this account" > "In 2 hours"
10. **Cross-device sanity** — One source of truth, no duplicate badges
