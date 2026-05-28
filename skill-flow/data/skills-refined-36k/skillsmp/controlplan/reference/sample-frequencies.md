# Sample Size and Frequency Guidelines - MNMUK

## Frequency Selection Framework

### Decision Factors

1. **Severity** (from PFMEA) - Customer impact
2. **Occurrence** (from PFMEA) - Likelihood of defect
3. **Process Capability** (Cpk) - Process performance
4. **Production Volume** - Parts per hour/shift
5. **Cycle Time** - Time between parts
6. **Setup Sensitivity** - Drift from setup
7. **Tool Wear** - Degradation over time
8. **Customer Requirements** - Specified frequencies

---

## Frequency by Severity

### Critical Characteristics (S = 9-10)

| Scenario | Sample Size | Frequency |
|----------|-------------|-----------|
| Safety critical | 100% | Every piece |
| Regulatory | 100% | Every piece |
| High Cpk (>1.67) | 100% or n≥5 | Per piece or per hour |

**Rationale:** No defective parts can escape. Full inspection or very frequent sampling required.

### High Severity (S = 7-8)

| Scenario | Sample Size | Frequency |
|----------|-------------|-----------|
| High Cpk (>1.67) | n=5 | Per hour |
| Moderate Cpk (1.33-1.67) | n=5 | Per 30 min |
| Low Cpk (<1.33) | 100% or n=5 | Per 15 min or continuous |

**Rationale:** Customer significantly affected. Frequent monitoring needed.

### Moderate Severity (S = 5-6)

| Scenario | Sample Size | Frequency |
|----------|-------------|-----------|
| High Cpk (>1.67) | n=3 | Per shift |
| Moderate Cpk (1.33-1.67) | n=5 | Per hour |
| Low Cpk (<1.33) | n=5 | Per 30 min |

**Rationale:** Moderate impact. Balance inspection cost with risk.

### Low Severity (S = 1-4)

| Scenario | Sample Size | Frequency |
|----------|-------------|-----------|
| Any Cpk | n=1-3 | Per lot or per setup |
| Setup sensitive | n=3 | Per setup + periodic |

**Rationale:** Low customer impact. Focus resources on higher risk items.

---

## Frequency by Process Capability

| Cpk | Process Status | Typical Frequency | Rationale |
|-----|----------------|-------------------|-----------|
| <1.00 | Not capable | 100% or sort | Process doesn't meet spec |
| 1.00-1.17 | Barely capable | Every 15-30 min | High defect risk |
| 1.17-1.33 | Marginally capable | Every hour | Moderate defect risk |
| 1.33-1.50 | Capable | Per shift or 2-hour | Low defect risk |
| 1.50-1.67 | Very capable | Per setup + daily | Very low defect risk |
| >1.67 | Highly capable | Per setup + weekly | Defects nearly impossible |

---

## Frequency by Production Scenario

### High Volume Production (>100 parts/hour)

| Risk Level | Sample | Frequency | Notes |
|------------|--------|-----------|-------|
| Critical | 100% | Continuous | Automated preferred |
| High | n=5 | Every 30 min | SPC charting |
| Medium | n=5 | Every hour | SPC charting |
| Low | n=3 | Per shift | Audit basis |

### Medium Volume (10-100 parts/hour)

| Risk Level | Sample | Frequency | Notes |
|------------|--------|-----------|-------|
| Critical | 100% | Every piece | |
| High | n=5 | Every hour | SPC charting |
| Medium | n=3 | Every 2 hours | Data log |
| Low | n=1 | Per setup | First piece |

### Low Volume (<10 parts/hour)

| Risk Level | Sample | Frequency | Notes |
|------------|--------|-----------|-------|
| Critical | 100% | Every piece | |
| High | 100% | Every piece | May be practical |
| Medium | n=1-3 | Per lot | Lot-based |
| Low | n=1 | Per lot | Lot-based |

### Prototype/Pre-Launch

| Phase | Sample | Frequency | Purpose |
|-------|--------|-----------|---------|
| Prototype | 100% | Every piece | Validate design |
| Pre-Launch | n≥5 | Every lot | Validate process |
| Initial Production | Enhanced | Per plan | Prove capability |

---

## Frequency Terms and Definitions

| Term | Definition | When to Use |
|------|------------|-------------|
| **100%** | Every piece inspected | Critical, no capability |
| **Continuous** | Real-time monitoring | Automated inspection |
| **Per piece** | Same as 100% | Critical characteristics |
| **Per cycle** | After each machine cycle | Multi-cavity, batch |
| **Per hour** | At least once per hour | SPC, high volume |
| **Per 30 min** | At least twice per hour | Marginal capability |
| **Per shift** | At start and end of shift | Stable processes |
| **Per setup** | After each setup/changeover | Setup-sensitive |
| **First piece** | First part after setup | Setup verification |
| **Last piece** | Last part before changeover | Confirm sustained |
| **Per lot** | Once per production lot | Incoming, low volume |
| **Per container** | Once per packaging unit | Packaging verification |
| **Daily** | At least once per day | Very stable |
| **Weekly** | At least once per week | Periodic audit |

---

## SPC Sample Size Guidelines

### Subgroup Size Selection

| Scenario | Subgroup Size (n) | Rationale |
|----------|-------------------|-----------|
| High volume, short cycle | n=5 | Standard for X-bar/R |
| Medium volume | n=3-5 | Balance cost/sensitivity |
| Low volume | n=1 (I-MR) | Can't wait for subgroup |
| Batch process | n=3-5 per batch | Within-batch variation |
| Long cycle (>30 min) | n=1 (I-MR) | Can't delay |

### Subgroup Frequency

| Characteristic Type | Typical Frequency |
|--------------------|-------------------|
| Dimension affected by tool wear | Every 30 min to 1 hour |
| Dimension affected by setup | First + every 2-4 hours |
| Temperature sensitive | Every 1-2 hours |
| Stable characteristic | Per shift |

---

## Special Situations

### After Process Change

| Change Type | Frequency Adjustment | Duration |
|-------------|---------------------|----------|
| New operator | Enhanced first shift | Until proficient |
| Tool change | First piece + next 3 | Until confirmed |
| Setup/Changeover | First 3-5 pieces | Until stable |
| Material lot change | First 5 pieces | Until confirmed |
| Process adjustment | Enhanced next hour | Until stable |
| After downtime (>4 hr) | First 3-5 pieces | Until confirmed |

### Customer Requirements

Some customers specify:
- Minimum inspection frequencies
- SPC requirements for specific characteristics
- Safe launch requirements (enhanced initial)
- Ongoing reporting requirements

**Always check customer-specific requirements (CSR).**

---

## Sample Size for Incoming Inspection

Based on ANSI/ASQ Z1.4 (Attributes) or Z1.9 (Variables)

### Typical AQL Levels

| Material Type | AQL | Inspection Level |
|---------------|-----|------------------|
| Critical components | 0.65% | Level II |
| Standard components | 1.0% | Level II |
| Non-critical | 2.5% | Level I |
| Packaging materials | 4.0% | Level I |

### Quick Reference (Level II, Single Sampling)

| Lot Size | n (AQL 1.0%) | Accept | Reject |
|----------|--------------|--------|--------|
| 2-8 | 2 | 0 | 1 |
| 9-15 | 3 | 0 | 1 |
| 16-25 | 5 | 0 | 1 |
| 26-50 | 8 | 0 | 1 |
| 51-90 | 13 | 1 | 2 |
| 91-150 | 20 | 1 | 2 |
| 151-280 | 32 | 2 | 3 |
| 281-500 | 50 | 3 | 4 |
| 501-1200 | 80 | 5 | 6 |
| 1201-3200 | 125 | 7 | 8 |

---

## Frequency Adjustment Based on Performance

### Reduce Frequency When:
- 20+ consecutive lots/samples conforming
- Cpk consistently >1.67
- No customer complaints for 6 months
- Process demonstrated stable

### Increase Frequency When:
- Nonconformance detected
- Cpk drops below 1.33
- Customer complaint
- Process change
- New operator

### Tightened Inspection Triggers (per Z1.4)
- 2 of 5 lots rejected
- Erratic production
- Customer request

### Reduced Inspection Criteria (per Z1.4)
- 10 consecutive lots accepted
- Process proven capable
- Quality history established

---

## Documentation Requirements

### For Each Characteristic in Control Plan:

1. **Sample Size**: Specific number (not "per plan")
2. **Frequency**: Specific timing (not "as needed")
3. **Basis**: Rationale for selection
4. **Review Trigger**: When to reconsider

### Review Schedule

| Situation | Review Frequency |
|-----------|------------------|
| New product | After 3 months production |
| Established product | Annually |
| After quality issue | Immediately |
| After process change | Immediately |
| Capability improvement | As data available |
