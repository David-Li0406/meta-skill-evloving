# SPC - Extended Guidance

**Deep-dive content for comprehensive SPC implementation and analysis.**

---

## Table of Contents

1. [SPC Program Implementation](#spc-program-implementation)
2. [Rational Subgrouping](#rational-subgrouping)
3. [Control Chart Construction](#control-chart-construction)
4. [Interpreting Control Charts](#interpreting-control-charts)
5. [Process Capability Deep Dive](#process-capability-deep-dive)
6. [Handling Non-Normal Data](#handling-non-normal-data)
7. [SPC for Different Process Types](#spc-for-different-process-types)
8. [Continuous Improvement with SPC](#continuous-improvement-with-spc)

---

## SPC Program Implementation

### Prioritizing Characteristics for SPC

Not all characteristics need SPC. Prioritize based on:

| Priority | Characteristic Type | SPC Requirement |
|----------|---------------------|-----------------|
| 1 | Critical (CC) - Safety/Regulatory | Mandatory |
| 2 | Significant (SC) - Customer specified | Mandatory |
| 3 | High PFMEA RPN | Strongly recommended |
| 4 | Customer complaints/returns | Strongly recommended |
| 5 | High scrap/rework | Recommended |
| 6 | Process-sensitive | Recommended |
| 7 | Other | Optional |

### SPC Implementation Checklist

- [ ] Characteristic selected and documented
- [ ] Measurement system validated (MSA acceptable)
- [ ] Subgroup strategy defined
- [ ] Data collection method established
- [ ] Control limits calculated (trial)
- [ ] Operators trained
- [ ] Reaction plan documented
- [ ] Initial capability calculated
- [ ] Control limits validated and finalized
- [ ] Ongoing monitoring established

### Training Requirements

**Operators should understand:**
- Purpose of SPC
- How to collect and plot data
- How to recognize patterns
- When to call for help
- Reaction procedures

**Engineers should understand:**
- All of the above, plus:
- Control limit calculations
- Capability calculations
- Root cause analysis
- Chart interpretation
- Process improvement methods

---

## Rational Subgrouping

### Principle

Subgroups should be formed so that:
- Variation **within** subgroups represents common cause only
- Variation **between** subgroups can reveal special causes

### Guidelines

**Good Subgrouping:**
- Consecutive parts from same cavity/spindle
- Parts from same batch of material
- Parts from same setup
- Parts from short time period

**Poor Subgrouping:**
- Parts from different machines mixed
- Parts from different shifts mixed
- Parts from different materials mixed
- Random samples over long period

### Examples

| Scenario | Good Subgroup | Poor Subgroup |
|----------|---------------|---------------|
| Multi-cavity mold | 5 parts from cavity 1, then cavity 2 | 1 part from each of 5 cavities |
| Multi-spindle lathe | 5 consecutive from spindle A | Mix of spindles A, B, C |
| Batch process | 5 parts from same batch | Mix from different batches |
| 24-hour production | 5 consecutive every hour | Random selection through day |

### Subgroup Frequency

| Situation | Typical Frequency |
|-----------|-------------------|
| New process | Every 30 min or more often |
| Stable process | Every 1-2 hours |
| Very stable, capable | Every 2-4 hours or per setup |
| After setup/changeover | Immediately, then normal |
| After adjustment | Immediately, then normal |

---

## Control Chart Construction

### Step-by-Step: X-bar/R Chart

**1. Collect Data**
- Minimum 20-25 subgroups
- Under normal operating conditions
- Record in time sequence

**2. Calculate Subgroup Statistics**
```
X̄ᵢ = (x₁ + x₂ + ... + xₙ) / n
Rᵢ = max(x₁...xₙ) - min(x₁...xₙ)
```

**3. Calculate Grand Mean and Average Range**
```
X̄̄ = (X̄₁ + X̄₂ + ... + X̄ₖ) / k
R̄ = (R₁ + R₂ + ... + Rₖ) / k
```

**4. Calculate Control Limits**

R Chart (do first):
```
UCL_R = D₄ × R̄
CL_R = R̄
LCL_R = D₃ × R̄
```

X-bar Chart:
```
UCL_X̄ = X̄̄ + A₂ × R̄
CL_X̄ = X̄̄
LCL_X̄ = X̄̄ - A₂ × R̄
```

**5. Plot Initial Data**
- Plot all points
- Draw control limits
- Note any out-of-control points

**6. Investigate Out-of-Control Points**
- Identify assignable causes
- Document findings
- Remove points with identified causes from limit calculation

**7. Recalculate Limits (if needed)**
- Exclude points with assignable causes
- Recalculate
- Verify remaining points are in control

**8. Finalize Limits**
- Use these for ongoing monitoring
- Recalculate periodically (monthly, quarterly)
- Recalculate after process changes

### Step-by-Step: I-MR Chart

**1. Collect Data**
- Minimum 30 individual observations
- Under normal conditions
- In time sequence

**2. Calculate Moving Ranges**
```
MRᵢ = |Xᵢ - Xᵢ₋₁|
```

**3. Calculate Averages**
```
X̄ = (X₁ + X₂ + ... + Xₙ) / n
MR̄ = (MR₂ + MR₃ + ... + MRₙ) / (n-1)
```

**4. Calculate Control Limits**

MR Chart:
```
UCL_MR = 3.267 × MR̄
CL_MR = MR̄
LCL_MR = 0
```

I Chart:
```
UCL_X = X̄ + 2.66 × MR̄
CL_X = X̄
LCL_X = X̄ - 2.66 × MR̄
```

---

## Interpreting Control Charts

### Common Patterns and Their Causes

**Pattern: Point Beyond Control Limit**
- Single extreme value
- Causes: Measurement error, broken tool, wrong material, incorrect setup

**Pattern: Run (7+ points same side of CL)**
- Sustained shift in process mean
- Causes: Tool wear, new material lot, new operator, equipment drift

**Pattern: Trend (6+ points steadily increasing or decreasing)**
- Gradual process change
- Causes: Tool wear, temperature drift, material depletion

**Pattern: Cycles (regular up-down pattern)**
- Periodic influence
- Causes: Shift changes, temperature cycles, batch changes

**Pattern: Hugging Center Line**
- Suspiciously little variation
- Causes: Data manipulation, wrong measurement, calculation error

**Pattern: Hugging Control Limits**
- Two or more processes mixed
- Causes: Different machines, different operators, different materials

**Pattern: Sudden Shift**
- Step change in process
- Causes: New setup, adjustment, new material, equipment change

### Action Guidelines

| Pattern | Immediate Action | Investigation |
|---------|------------------|---------------|
| Point out of control | Verify measurement, check process | 5-Why analysis |
| Run | Check for process change | What changed? When? |
| Trend | Anticipate and prevent | Tool wear? Drift? |
| Cycle | Identify cycle timing | Match to known cycles |
| Hugging CL | Verify data collection | Audit process |
| Hugging limits | Separate streams | Stratify data |

---

## Process Capability Deep Dive

### When to Calculate Capability

| Study Type | Requirement | Use |
|------------|-------------|-----|
| Initial | 30-50 samples, one batch | Preliminary assessment |
| Short-term | 50+ samples, stable process | Process potential (Cp, Cpk) |
| Long-term | 100+ samples, multiple conditions | Process performance (Pp, Ppk) |
| PPAP | Per customer requirement | Production approval |

### Capability Study Execution

**Pre-Study:**
1. Verify MSA acceptable (ndc ≥5)
2. Verify process is representative
3. Plan sample collection
4. Notify operators (no special care)

**During Study:**
1. Collect samples per plan
2. Record in time order
3. Note any unusual events
4. Don't adjust process during study

**Post-Study:**
1. Plot histogram
2. Test for normality
3. Create control chart
4. Verify statistical control
5. Calculate indices

### Interpreting Cp vs Cpk

| Scenario | Cp | Cpk | Interpretation |
|----------|----|----|----------------|
| Centered, capable | 2.0 | 2.0 | Excellent |
| Centered, barely capable | 1.0 | 1.0 | Marginal |
| Off-center, capable spread | 2.0 | 1.5 | Good but could be better |
| Off-center, tight spread | 1.5 | 0.5 | Center the process! |
| Wide spread, centered | 0.8 | 0.8 | Reduce variation |

**Key insight:**
- If Cp >> Cpk: Process is off-center, centering will improve
- If Cp ≈ Cpk: Process is centered, must reduce variation to improve

### One-Sided Specifications

For unilateral tolerances:

**USL only (example: maximum runout):**
```
Cpu = (USL - X̄) / 3σ
Cpk = Cpu
```

**LSL only (example: minimum hardness):**
```
Cpl = (X̄ - LSL) / 3σ
Cpk = Cpl
```

---

## Handling Non-Normal Data

### Detecting Non-Normality

**Visual methods:**
- Histogram shape
- Normal probability plot

**Statistical tests:**
- Anderson-Darling
- Shapiro-Wilk
- Kolmogorov-Smirnov

### Options for Non-Normal Data

**Option 1: Transform the Data**
- Log transformation for right-skewed data
- Square root transformation
- Box-Cox transformation (find optimal)
- Calculate capability on transformed data

**Option 2: Non-Normal Distribution Analysis**
- Identify distribution (Weibull, lognormal, etc.)
- Calculate percentiles from fitted distribution
- Estimate capability from percentiles

**Option 3: Use Ppk Instead**
- Ppk based on actual performance
- Less sensitive to distribution assumptions
- More conservative estimate

**Option 4: Non-Parametric Methods**
- Use percentiles directly
- No distribution assumption
- Requires larger sample size

### Common Non-Normal Situations

| Data Type | Typical Distribution | Approach |
|-----------|---------------------|----------|
| Surface finish | Right-skewed | Log transform or Weibull |
| Runout/TIR | Right-skewed (bounded at 0) | Weibull or lognormal |
| Position | Usually normal | Standard |
| Hardness | Usually normal | Standard |
| Concentricity | May be skewed | Check normality |
| Flatness | Right-skewed | Log transform |

---

## SPC for Different Process Types

### High-Volume, Short Cycle

- Traditional X-bar/R charts
- Real-time monitoring possible
- Automated data collection ideal
- Frequent subgroups (hourly or more)

### Low-Volume, Long Cycle

- I-MR charts
- Each piece may be a subgroup
- Pre-control may be alternative
- Focus on setup verification

### Batch Processes

- Within-batch variation vs. batch-to-batch
- May use batch means chart
- Consider nested designs
- Time-based control within batch

### Multiple Streams (Cavities, Spindles)

**Option 1: Combined Chart**
- Single chart for all streams
- Subgroup = one from each stream
- Detects average shifts

**Option 2: Separate Charts**
- Individual chart per stream
- More sensitivity
- More charts to manage

**Option 3: Target Charts**
- Plot deviation from target
- Centerline at 0
- Easier comparison between streams

### CNC Machining

- Setup-dominant variation
- Focus first piece verification
- Pre-control often sufficient
- Monitor tool wear trends
- May need chart per tool position

---

## Continuous Improvement with SPC

### Using SPC for Improvement

**Phase 1: Bring to Control**
- Identify and eliminate special causes
- Stabilize the process
- Establish baseline

**Phase 2: Assess Capability**
- Calculate Cpk
- Identify gap to requirement
- Prioritize improvement

**Phase 3: Reduce Variation**
- Design of Experiments (DOE)
- Parameter optimization
- Equipment upgrades
- Process standardization

**Phase 4: Monitor and Maintain**
- Ongoing SPC
- Periodic capability review
- React to signals
- Prevent regression

### Reducing Variation

Common sources of variation and actions:

| Source | Actions |
|--------|---------|
| Equipment | Maintenance, upgrade, replacement |
| Method | Standardize, simplify, error-proof |
| Material | Tighter specs, better suppliers |
| Environment | Control temp, humidity, vibration |
| Measurement | Better gages, training, MSA |
| Operator | Training, standardization, aids |

### Recalculating Control Limits

**When to recalculate:**
- After process improvement
- After process change
- Periodically (monthly, quarterly)
- When current limits don't make sense

**How to recalculate:**
- Collect new data under current conditions
- Exclude data from before change
- Follow initial limit calculation process

**Document:**
- Old limits
- Reason for change
- New limits
- Effective date

---

## Software and Tools

### SPC Software Options

| Tool | Type | Features |
|------|------|----------|
| Minitab | Commercial | Full SPC, capability, analysis |
| JMP | Commercial | Full SPC, DOE integration |
| InfinityQS | Commercial | Real-time SPC, enterprise |
| Excel | Custom | Basic charting, manual |
| QI Macros | Excel add-in | Templates, analysis |

### Manual Charting Tips

- Use graph paper or templates
- Pre-print control limits
- Use different colors for limits, data
- Include specification limits (dashed)
- Note out-of-control points
- Document actions taken

### Automated Data Collection

**Benefits:**
- Reduces transcription errors
- Real-time monitoring
- Historical database
- Automatic alerts
- Easier analysis

**Considerations:**
- Integration with gages
- Operator interface
- Data storage/backup
- System maintenance
