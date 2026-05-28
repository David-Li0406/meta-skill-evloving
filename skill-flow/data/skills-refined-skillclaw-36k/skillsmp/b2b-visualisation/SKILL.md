---
name: b2b-visualisation
description: Design data visualisations for B2B dashboards displaying buying signals, composite scores, trends, and alerts. Apply when building charts, sparklines, score breakdowns, heatmaps, or any interface requiring rapid comprehension of multivariate data. Covers the 2-second rule, pre-attentive processing, visualisation selection by data type, trend surge detection, score explainability, and mobile-responsive patterns.
---

# B2B Market Intelligence Visualisation

## Purpose

Design visualisations for B2B buying signals with **time-to-insight** as the primary imperative. In high-velocity environments, the interface must facilitate comprehension of complex multivariate signals in **under two seconds**.

## Related Skills

- `adhd-interface-design` — For cognitive load patterns
- `action-oriented-ux` — For lead card and queue designs
- `uk-police-design-system` — For colour tokens and typography
- `notification-system` — For alert severity and badging

---

## Cognitive Foundations

### Pre-Attentive Processing

Visual properties detected in under **200 milliseconds**, before conscious attention engages:

| Attribute | Detection Speed | Best Use Case |
|-----------|-----------------|---------------|
| **Colour intensity/hue** | ~50ms | Status, urgency, category |
| **Position on common scale** | ~100ms | Comparison, ranking |
| **Length** | ~100ms | Magnitude, progress |
| **Size** | ~150ms | Importance, volume |
| **Orientation/slope** | ~150ms | Trend direction |
| **Motion/flicker** | Immediate | Critical alerts (use sparingly) |

### Accuracy Hierarchy

Visual encodings ranked by reliability for accurate value judgement:

1. **Position on common scale** — Most accurate (bar charts, dot plots)
2. **Length** — Very accurate (bars, bullet graphs)
3. **Angle/slope** — Moderate (line charts)
4. **Area** — Poor (bubble charts, pie charts)
5. **Colour saturation** — Least accurate for precise values

**Implication:** For comparison tasks, prefer bar charts and dot plots over pie charts and gauges.

### Cognitive Load Management

Every pixel must serve a data-communicating purpose. Eliminate:
- Unnecessary gridlines
- 3D effects
- Heavy borders
- Decorative backgrounds
- Redundant legends

---

## The 2-Second Rule

A user must answer **"Is this account interested?"** and **"Why?"** within two seconds.

### 2-Second Test Checklist

1. **What is it?** — Clear label
2. **Is it good/bad/urgent?** — Direction + threshold indicator
3. **What changed?** — Delta value
4. **What should I do?** — CTA or driver hint visible

If any answer requires a legend, tooltip, or reading axis ticks, move that information to a detail view.

---

## Visualisation Selection by Data Type

| User Task | Visualisation Type | Rationale |
|-----------|-------------------|-----------|
| **Scan/triage many entities** | Sparklines, micro-charts | Word-sized, pattern recognition |
| **Diagnose/explain one entity** | Full charts with axes | Precision, interaction |
| **Compare values** | Bar charts, dot plots | Position on common scale |
| **Show progress vs target** | Bullet graphs | Length encoding, compact |
| **Indicate status category** | Badges, colour coding | Pre-attentive, categorical |
| **Show exact value** | Number + delta | Precision with context |

### Sparklines vs Full Charts

**Use Sparklines When:**
- Task is "up/down/volatile?" not "what was the value on April 12?"
- Displaying many rows (account list, territory list)
- Paired with number + delta
- Time window is consistent

**Use Full Charts When:**
- User needs to answer "why did this spike happen?"
- Axes, annotations, or event markers required
- Interaction expected (zoom, filter)

**Practical Pattern:**
- **List view (scan):** Number + delta + sparkline + 1 badge
- **Detail view (explain):** Full chart with baseline band, annotations

### Gauges vs Progress Bars vs Numbers

| Element | Best For | Efficiency |
|---------|----------|------------|
| **Numbers** | Exact values needed quickly | High precision |
| **Progress/Bullet bars** | Value vs target/thresholds | High comparison |
| **Gauges** | Capacity/utilisation metaphor | Low (use rarely) |

Research shows bullet graphs support more efficient reading than gauge graphs.

---

## Trend Visualisation: Showing Surge at a Glance

### Making "Surge" Binary First

For sales scanning, "surge" should read as a **state** (Yes/No + severity), then users inspect magnitude.

### The Baseline Band Pattern

To show "surging relative to normal," add a typical-range band behind the line:

- **Upward breakout** → Green highlight, "SURGE" badge
- **Downward breakout** → Red highlight, "DECLINE" badge

**Band Calculation:**
- Median ± IQR (interquartile range)
- Mean ± 2σ (standard deviations)
- Rolling average ± percentage threshold

### Period-over-Period Comparisons

**Ghost Bar (Fastest in Lists):**
- Solid bar = current period
- Light/outlined bar = previous period
- Delta text adjacent

**Indexed Line (100 Baseline):**
- Convert each series to index = 100 at start
- Divergence shows acceleration

---

## Score Visualisation: Explainability

### The Opacity Problem

Composite scores are often "black boxes." Teams disregard scores they don't understand.

**Principle:** Separate the score for triage (one glance) from the reasons for action (one click/expand).

### Progressive Disclosure Architecture

**Layer 1: Score (Always Visible)**
- Large number + categorical label (Cold/Warm/Hot)
- Delta from previous period
- Optional percentile

**Layer 2: Top Drivers (Compact)**
- Up to 3 driver chips
- Each shows direction + contribution magnitude

**Layer 3: Full Breakdown (Expanded)**
- Sorted contribution bar list
- Waterfall chart showing how components sum
- Top positive and negative factors

---

## Alert Design and Anomaly Highlighting

### The Highlight Budget

**Only ONE strong highlight per row/card:**
- Badge OR border OR background tint OR icon — not all four

Reserve pre-attentive cues for top-priority signals only.

### Severity Coding

| Severity | Colour | Icon | Use Case |
|----------|--------|------|----------|
| **Critical** | Red/Orange | ⚠️ | Competitor contract signed, Champion left |
| **Warning** | Yellow/Amber | ⚡ | Usage dropped 10%, Stalled in stage |
| **Info** | Blue/Gray | ℹ️ | New CFO hired, Press mention |

**Motion:** Use sparingly. Reserve for states requiring immediate action.

### Avoiding Alert Fatigue

**Gate alerts by:**
- Persistence: 2-3 consecutive periods above threshold
- Impact: Score contribution ≥ X points

**Throttle display:**
- Show "Top 5 today" by default
- Provide "view all" expansion

---

## Sparklines and Small Multiples

### Sparkline Specifications

- **Aspect Ratio:** Wide and short (4:1)
- **Start point:** Gray dot (anchor)
- **End point:** Coloured dot (current state)
- **High/Low points:** Optional markers
- **Smoothing:** Slight curve, avoid over-smoothing

### Small Multiples

Use when comparing many entities with the same question.

**Consistency Requirements:**
- Same time window everywhere
- Shared Y-scale when magnitude matters
- Normalised Y-scale when shape matters
- 1 series ideal, 2 maximum

**Coordinated Highlighting:** Hover one account → highlight same time region across ALL sparklines.

---

## Mobile-Responsive Data Visualisation

### Adaptation Playbook

| Desktop | Mobile |
|---------|--------|
| Horizontal bar chart | Vertical list of bars |
| Multi-series line chart | Single series + toggle |
| Data table | Card stack |
| Dashboard grid | Vertical scroll of cards |
| Detailed chart | Sparkline + tap to expand |

### Touch-First Interactions

**The Scrubber Pattern:** Dragging anywhere on chart snaps to nearest data point; readout updates above.

---

## Technical Implementation

### Rendering Performance

| Technology | Use Case |
|------------|----------|
| **SVG** | Interactive elements, <1000 elements |
| **Canvas** | High-density plots, >1000 elements |

### Progressive Loading

1. Render chart skeleton immediately
2. Load macro trend line first
3. Progressively enhance with high-resolution data

---

## Summary Principles

1. **Velocity over Static State** — Show rate of change, not just current value
2. **Context over Raw Counts** — Always provide baseline or comparison
3. **Binary First, Quantitative Second** — State (Hot/Cold) before magnitude
4. **Progressive Disclosure** — Triage → Detail → Full analysis
5. **Pre-attentive for Priority** — Reserve colour/size/motion for what matters
6. **Position over Angle** — Bars and dots over pies and gauges
7. **Explain the Score** — Show drivers, not just the number
8. **Respect Cognitive Load** — Every pixel earns its place
9. **Mobile as Primary** — Design for glanceability
10. **2 Seconds or Less** — If it requires legend/tooltip, simplify
