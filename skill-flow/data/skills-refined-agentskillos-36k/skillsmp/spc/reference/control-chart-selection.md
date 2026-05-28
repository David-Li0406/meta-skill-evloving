# Control Chart Selection Guide

## Decision Flowchart

```
Start: What type of data?
           │
           ├─────────────────────────────────────┐
           │                                     │
    VARIABLE                               ATTRIBUTE
   (measurements)                         (counts/categories)
           │                                     │
           │                                     │
    Subgroup size?                    What are you counting?
           │                                     │
     ┌─────┴─────┐                    ┌─────────┼─────────┐
     │           │                    │         │         │
   n=1         n≥2                Defectives  Defects  Categories
     │           │                    │         │         │
  I-MR        n<10?               Sample      Sample     (rare)
  Chart         │                  size?       size?
              ┌─┴─┐                  │           │
            Yes   No              ┌──┴──┐     ┌──┴──┐
              │     │           Fixed Vary  Fixed Vary
          X-bar/R  X-bar/S         │     │      │     │
                                  np    p      c     u
                                Chart Chart  Chart Chart
```

---

## Variable Data Charts

### X-bar/R Chart

**Use when:**
- Measuring variable data (dimensions, weight, temperature, etc.)
- Can collect subgroups of 2-9 samples
- Want to monitor both mean and variation

**Advantages:**
- Most common, well-understood
- Sensitive to shifts in mean
- Range easy to calculate

**Limitations:**
- Requires rational subgrouping
- Range less efficient for larger subgroups

**Typical applications:**
- Machining dimensions
- Filling operations
- Temperature monitoring
- Any repetitive measurement process

### X-bar/S Chart

**Use when:**
- Subgroup size ≥10
- Need more efficient estimate of variation
- Using computerized data collection

**Advantages:**
- More efficient than Range for large n
- Standard deviation is better estimator

**Limitations:**
- Requires calculation (not mental math)
- Same subgrouping requirements as X-bar/R

**Typical applications:**
- High-volume processes
- Automated inspection
- Multiple cavity/spindle where n is large

### I-MR (Individuals and Moving Range) Chart

**Use when:**
- Only one measurement per time period
- Long cycle time
- Destructive testing
- Batch processes
- Expensive sampling

**Advantages:**
- Don't need to wait for subgroup
- Works with any sample size
- Simple to implement

**Limitations:**
- Less sensitive than X-bar charts
- Assumes approximately normal data
- More affected by non-normality

**Typical applications:**
- Chemical batch properties
- Long-cycle machining
- Laboratory test results
- Monthly/weekly metrics

---

## Attribute Data Charts

### p Chart (Proportion Defective)

**Use when:**
- Counting defective units (pass/fail)
- Sample size varies
- Reporting as percentage/proportion

**Formula:**
```
CL = p̄
UCL = p̄ + 3√(p̄(1-p̄)/n)
LCL = p̄ - 3√(p̄(1-p̄)/n)
```

**Typical applications:**
- Go/No-go inspection
- Final inspection pass rate
- Any varying sample inspection

### np Chart (Count of Defectives)

**Use when:**
- Counting defective units
- Sample size is constant
- Reporting as count

**Formula:**
```
CL = n̄p̄
UCL = n̄p̄ + 3√(n̄p̄(1-p̄))
LCL = n̄p̄ - 3√(n̄p̄(1-p̄))
```

**Typical applications:**
- Fixed lot inspection
- Production run with constant batch size

### c Chart (Count of Defects)

**Use when:**
- Counting number of defects (not defective units)
- Sample size (area of opportunity) is constant
- Multiple defects per unit possible

**Formula:**
```
CL = c̄
UCL = c̄ + 3√c̄
LCL = c̄ - 3√c̄
```

**Typical applications:**
- Defects per PCB
- Defects per weld length
- Errors per document

### u Chart (Defects per Unit)

**Use when:**
- Counting number of defects
- Sample size (area of opportunity) varies
- Reporting as rate (defects per unit)

**Formula:**
```
CL = ū
UCL = ū + 3√(ū/n)
LCL = ū - 3√(ū/n)
```

**Typical applications:**
- Defects per unit of varying size
- Defects per meter of varying length
- Complaints per varying number of shipments

---

## Quick Reference Table

| Data Type | Sample Size | Chart | When to Use |
|-----------|-------------|-------|-------------|
| Variable | n = 1 | I-MR | Long cycle, destructive, batch |
| Variable | n = 2-9 | X-bar/R | Standard variable data |
| Variable | n ≥ 10 | X-bar/S | Large subgroups |
| Attribute - Defectives | Varies | p | Proportion defective |
| Attribute - Defectives | Constant | np | Count defective |
| Attribute - Defects | Constant | c | Defects per constant unit |
| Attribute - Defects | Varies | u | Defects per varying unit |

---

## Special Situations

### Multiple Characteristics

**Option 1:** Separate chart for each characteristic
- More sensitive
- More charts to maintain
- Use for critical characteristics

**Option 2:** Multivariate chart (T² chart)
- Single chart for multiple characteristics
- Requires specialized software
- Use when characteristics are correlated

### Short Runs

**Challenge:** Not enough data to establish limits

**Options:**
- DNOM (Deviation from Nominal) chart
- Pre-control
- Standardized chart
- Accept wider limits initially

### Setup-Dominant Processes

**Challenge:** Most variation is at setup

**Options:**
- Focus on first piece approval
- Pre-control
- Control setup parameters
- Setup verification chart

### Automated High-Speed

**Challenge:** Thousands of parts per hour

**Options:**
- Sample from each cavity/position
- Time-based sampling
- Real-time SPC software
- Automated 100% inspection

---

## Subgroup Size Selection

| Situation | Recommended n | Rationale |
|-----------|---------------|-----------|
| Standard machining | 5 | Balance of sensitivity and practicality |
| Quick measurement | 3-5 | Time efficiency |
| Multi-cavity | 1 per cavity | Detect cavity differences |
| Expensive testing | 1 (I-MR) | Cost control |
| Setup-sensitive | 3-5 at setup | Verify setup |

---

## Chart Sensitivity Comparison

For detecting a 1σ shift in mean:

| Chart Type | Subgroup Size | Average Run Length (ARL) |
|------------|---------------|--------------------------|
| I-MR | n=1 | 44 samples |
| X-bar | n=3 | 8 subgroups |
| X-bar | n=5 | 5 subgroups |
| X-bar | n=10 | 3 subgroups |

**Interpretation:** Larger subgroups detect shifts faster, but require more samples per subgroup.

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using I-MR when subgroups possible | Less sensitive | Use X-bar/R |
| Mixing different sources in subgroup | Inflated R̄ | Rational subgrouping |
| Using variable chart for pass/fail | Meaningless | Use attribute chart |
| Using p chart when n is constant | Less straightforward | Use np chart |
| Confusing defects vs defectives | Wrong chart | Clarify: unit bad vs. count of flaws |
