# Out-of-Control Rules Reference

## Western Electric Rules (Standard Set)

The original and most commonly used rules. Apply to X-bar chart, I chart, and other variable charts.

### Rule 1: Point Beyond Control Limits

**Pattern:** One point beyond 3σ (outside UCL or LCL)

```
UCL ────────────────────────
                    ●        ← OUT OF CONTROL
                 ╱
────────────────────────────

LCL ────────────────────────
```

**Probable Causes:**
- Measurement error
- One-time disturbance
- Tool breakage
- Wrong material
- Incorrect setup

**Action:** Stop, investigate immediately. This is a clear signal of a special cause.

---

### Rule 2: Run (Shift)

**Pattern:** 9 points in a row on the same side of the center line

```
UCL ────────────────────────
     ● ● ● ● ● ● ● ● ●      ← OUT OF CONTROL (run above)
CL  ────────────────────────

LCL ────────────────────────
```

**Probable Causes:**
- Process shift
- New material lot
- New operator
- Tool wear
- Environment change
- Measurement drift

**Action:** Investigate what changed. Check for sustained shift in process mean.

---

### Rule 3: Trend

**Pattern:** 6 points in a row steadily increasing or decreasing

```
UCL ────────────────────────
                         ●
                      ●      ← OUT OF CONTROL (trend up)
                   ●
CL  ────────────────────────
                ●
             ●
          ●
LCL ────────────────────────
```

**Probable Causes:**
- Tool wear
- Temperature drift
- Material depletion
- Gradual equipment degradation
- Operator fatigue

**Action:** Investigate cause of gradual change. May predict future out-of-control condition.

---

### Rule 4: Alternating Pattern

**Pattern:** 14 points in a row alternating up and down

```
UCL ────────────────────────
       ●   ●   ●   ●   ●   ●   ●
CL  ──────────────────────────── ← OUT OF CONTROL
         ●   ●   ●   ●   ●   ●   ●
LCL ────────────────────────────
```

**Probable Causes:**
- Over-adjustment (tampering)
- Two alternating processes
- Sampling from alternating sources
- Systemic oscillation

**Action:** Check for over-adjustment. Often indicates operator "chasing" numbers.

---

## Nelson Rules (Extended Set)

Additional rules for more sensitive detection. Use for critical characteristics or when standard rules are not sufficient.

### Rule 5: Zone A Test

**Pattern:** 2 of 3 consecutive points beyond 2σ (Zone A), same side

```
UCL ──────────────────────── (3σ)
     ── Zone A ──
                  ●          ← 2 of 3 in Zone A
           ●
──────────────────────────── (2σ)
     ── Zone B ──
           ●
──────────────────────────── (1σ)
     ── Zone C ──
CL  ────────────────────────
```

**Probable Causes:** Similar to Rule 2 (shift), but catches earlier

**Action:** Investigate potential shift

---

### Rule 6: Zone B Test

**Pattern:** 4 of 5 consecutive points beyond 1σ (Zone B), same side

```
UCL ──────────────────────── (3σ)
     ── Zone A ──
──────────────────────────── (2σ)
     ── Zone B ──
              ● ● ● ●        ← 4 of 5 in Zone B or beyond
──────────────────────────── (1σ)
     ── Zone C ──    ●
CL  ────────────────────────
```

**Probable Causes:** Small sustained shift in process mean

**Action:** Investigate subtle shift

---

### Rule 7: Stratification

**Pattern:** 15 consecutive points within 1σ of center line (Zone C)

```
UCL ────────────────────────
──────────────────────────── (2σ)
──────────────────────────── (1σ)
     ●●●●●●●●●●●●●●●          ← OUT OF CONTROL (too little variation)
CL  ────────────────────────
──────────────────────────── (-1σ)
──────────────────────────── (-2σ)
LCL ────────────────────────
```

**Probable Causes:**
- Incorrect control limits
- Data manipulation or selection
- Measurement resolution too coarse
- Multiple streams averaged

**Action:** Verify control limits, audit data collection

---

### Rule 8: Mixture

**Pattern:** 8 consecutive points beyond 1σ (either side)

```
UCL ────────────────────────
     ●   ●   ●   ●          ← Points in outer zones
──────────────────────────── (1σ)
──────────────────────────── (1σ)
         ●   ●   ●   ●       ← Points in outer zones
LCL ────────────────────────
```

**Probable Causes:**
- Two or more processes mixed
- Different materials mixed
- Different machines/operators mixed
- Over-adjustment creating bimodal pattern

**Action:** Stratify data by source, separate streams

---

## Zone Definitions

Control charts are divided into zones for rule evaluation:

```
UCL ──────────────────────── (+3σ)
     ┌── Zone A ──┐
     │            │
──────────────────────────── (+2σ)
     ┌── Zone B ──┐
     │            │
──────────────────────────── (+1σ)
     ┌── Zone C ──┐
     │            │
CL  ────────────────────────
     │            │
     └── Zone C ──┘
──────────────────────────── (-1σ)
     │            │
     └── Zone B ──┘
──────────────────────────── (-2σ)
     │            │
     └── Zone A ──┘
LCL ──────────────────────── (-3σ)
```

---

## Rule Summary Table

| Rule | Name | Pattern | Sensitivity |
|------|------|---------|-------------|
| 1 | Beyond limits | 1 point > 3σ | High (obvious) |
| 2 | Run | 9 points same side of CL | Medium |
| 3 | Trend | 6 points monotonically up/down | Medium |
| 4 | Alternating | 14 alternating up/down | Low |
| 5 | Zone A | 2 of 3 beyond 2σ, same side | High |
| 6 | Zone B | 4 of 5 beyond 1σ, same side | Medium |
| 7 | Stratification | 15 within 1σ of CL | Low |
| 8 | Mixture | 8 beyond 1σ (either side) | Medium |

---

## MNMUK Standard Application

### Standard Application (All Characteristics)

Use Rules 1-4 (Western Electric):
- Rule 1: Point beyond limits
- Rule 2: Run of 9
- Rule 3: Trend of 6
- Rule 4: Alternating 14

### Enhanced Application (Critical Characteristics)

Add Rules 5-6 for earlier detection:
- Rule 5: 2 of 3 in Zone A
- Rule 6: 4 of 5 in Zone B

### Special Investigation

Use Rules 7-8 when:
- Suspecting data issues
- Investigating unusual patterns
- Verifying control limit appropriateness

---

## False Alarm Rates

Each rule has an associated false alarm rate (probability of signal when process is in control):

| Rule | False Alarm Rate | Average Run Length (In Control) |
|------|------------------|--------------------------------|
| Rule 1 | 0.27% | 370 |
| Rule 2 | 0.39% | 256 |
| Rule 3 | 0.14% | 714 |
| Rule 4 | 0.01% | 10,000 |

**Combined Rules 1-4:** ~0.8% false alarm rate

**Note:** Using more rules increases sensitivity but also increases false alarms. Balance based on cost of investigation vs. cost of missed detection.

---

## Reaction Guidelines

| Signal Type | Immediate Action | Investigation Focus |
|-------------|------------------|---------------------|
| Rule 1 | Stop, verify measurement | One-time event or sustained? |
| Rule 2 | Continue but investigate | What changed ~9 points ago? |
| Rule 3 | Continue but investigate | Wear, drift, environmental? |
| Rule 4 | Review adjustment practice | Are we over-adjusting? |
| Rule 5-6 | Continue but investigate | Small shift occurring? |
| Rule 7 | Audit data and limits | Are limits/data correct? |
| Rule 8 | Stratify data | Multiple sources mixed? |

---

## Common Mistakes

| Mistake | Problem | Correct Approach |
|---------|---------|------------------|
| Reacting to every point near limits | Over-adjustment | Only react to rule violations |
| Ignoring patterns (only checking Rule 1) | Miss early warnings | Check all applicable rules |
| Applying attribute rules to variable charts | Wrong statistics | Use appropriate rules for chart type |
| Using all 8 Nelson rules routinely | Too many false alarms | Use extended rules selectively |
| Not documenting actions | No learning | Record all signals and actions |

---

## Documentation Requirements

When a control rule is violated, document:

1. **Date/Time** of signal
2. **Which rule** was violated
3. **Chart and characteristic** affected
4. **Investigation findings**
5. **Root cause** (if identified)
6. **Action taken**
7. **Verification** of action effectiveness
