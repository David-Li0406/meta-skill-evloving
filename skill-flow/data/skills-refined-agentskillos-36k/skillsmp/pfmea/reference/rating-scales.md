# PFMEA Rating Scales - MNMUK Standard

## Severity (S) - Effect on Customer

Rate based on most serious effect. Severity does not change based on controls.

| Rating | Effect | Customer Impact | MNMUK Manufacturing Examples |
|--------|--------|-----------------|------------------------------|
| **10** | Hazardous without warning | Failure may endanger operator or user without warning | Safety-critical dimension failure (brake caliper bore), structural failure during use |
| **9** | Hazardous with warning | Failure may endanger operator or user with warning | Safety dimension with visual indicator, airbag component failure detectable |
| **8** | Very high | Product inoperable, 100% scrap, customer very dissatisfied | Part cannot function, no rework possible (e.g., cracked housing) |
| **7** | High | Product operable but performance degraded, customer dissatisfied | Reduced performance, customer complaint likely (fit issue, noise) |
| **6** | Moderate | Product operable, comfort/convenience items affected | Cosmetic defect visible to customer, minor inconvenience |
| **5** | Low | Product operable, 50% may require rework | Internal rework required, no customer impact if caught |
| **4** | Very low | Product requires sorting and portion reworked | Sorting operation, some parts reworked |
| **3** | Minor | Product requires minor rework at station | In-station repair, no scrap |
| **2** | Very minor | Slight inconvenience to production | Process adjustment needed, minimal impact |
| **1** | None | No discernible effect | No impact to product or process |

### Severity Notes:
- S=9-10: Regulatory/safety implications - requires immediate action regardless of O and D
- Severity never changes due to detection controls
- Rate worst-case effect if multiple effects exist
- Customer = end user, not next production step

---

## Occurrence (O) - Likelihood of Cause

Rate based on cause occurrence, considering current prevention controls.

| Rating | Frequency | Cpk Equivalent | MNMUK Manufacturing Examples |
|--------|-----------|----------------|------------------------------|
| **10** | Very high: ≥100 per 1,000 | Cpk <0.33 | New process, no controls, known problem |
| **9** | High: 50 per 1,000 | Cpk ≥0.33 | Similar process had frequent failures |
| **8** | High: 20 per 1,000 | Cpk ≥0.51 | Previous quality issues, marginal process |
| **7** | Moderately high: 10 per 1,000 | Cpk ≥0.67 | Occasional failures, process not fully controlled |
| **6** | Moderate: 2 per 1,000 | Cpk ≥0.83 | Infrequent failures, some control |
| **5** | Moderately low: 0.5 per 1,000 | Cpk ≥1.00 | Controlled process, isolated failures |
| **4** | Low: 0.1 per 1,000 | Cpk ≥1.17 | Well-controlled, rare failures |
| **3** | Very low: 0.01 per 1,000 | Cpk ≥1.33 | Capable and controlled (automotive minimum) |
| **2** | Remote: 0.001 per 1,000 | Cpk ≥1.50 | Proven design, excellent controls |
| **1** | Nearly impossible | Cpk ≥1.67 | Failure eliminated through design/prevention |

### Occurrence Notes:
- Use actual data when available (scrap rates, SPC data, Cpk)
- For new processes without data, default to O≥6
- Consider similar process experience
- Rate the cause, not the failure mode
- Effective prevention controls reduce O rating

---

## Detection (D) - Ability to Detect

Rate based on best current detection control, before defect leaves process step.

| Rating | Detection | Control Type | MNMUK Manufacturing Examples |
|--------|-----------|--------------|------------------------------|
| **10** | Almost impossible | No detection opportunity | No inspection, shipped direct to customer |
| **9** | Very remote | Infrequent random check | Occasional spot check, audit sampling |
| **8** | Remote | Visual inspection by operator | 100% visual check, subjective, operator fatigue |
| **7** | Very low | Double visual inspection | Two operator checks, still subjective |
| **6** | Low | Charting/SPC | Control charts, trend monitoring (detects drift) |
| **5** | Moderate | Attribute gauging | Go/No-go gage, pass/fail test |
| **4** | Moderately high | Variable gauging | Measurement with limit checking, 100% |
| **3** | High | Automated test with alarm | Automatic measurement, rejects flagged |
| **2** | Very high | Error-proofing | Poka-yoke detects defect, prevents pass |
| **1** | Almost certain | Error-proofing prevents cause | Design prevents failure from occurring |

### Detection Notes:
- Rate current controls only, not proposed
- Consider false pass risk (defect passes inspection)
- Location matters: Detection at source > downstream detection
- Automated > manual inspection
- Variable > attribute gauging
- 100% > sampling

---

## Action Priority (AP) Matrix

Use this matrix instead of or alongside RPN thresholds.

### High Priority - Immediate action required

| Severity | Occurrence | Detection | Action |
|----------|------------|-----------|--------|
| 9-10 | Any | Any | Action required - safety critical |
| 7-8 | ≥4 | ≥4 | Action required |
| 5-8 | ≥6 | ≥6 | Action required |

### Medium Priority - Action recommended

| Severity | Occurrence | Detection | Action |
|----------|------------|-----------|--------|
| 5-8 | 4-5 | Any | Action recommended |
| 5-8 | Any | 4-5 | Action recommended |
| 4-6 | ≥6 | ≥6 | Action recommended |

### Low Priority - Monitor

All other combinations - document and monitor.

---

## RPN Thresholds (MNMUK Standard)

| RPN Range | Priority Level | Required Action |
|-----------|----------------|-----------------|
| **≥120** | Critical | Immediate countermeasure required, cannot ship without action |
| **80-119** | High | Countermeasure required before PPAP approval |
| **40-79** | Medium | Countermeasure recommended |
| **<40** | Low | Monitor, no immediate action required |

### Special Cases

Regardless of RPN:
- **S ≥ 8**: Requires action
- **O ≥ 8**: Review prevention controls
- **D ≥ 8**: Review detection methods

---

## Rating Calibration Examples

### Example 1: Machined Bore Diameter

**Failure Mode**: Bore diameter undersized
**Effect**: Part will not assemble, 100% scrap
**Cause**: Tool wear, incorrect offset

| Factor | Rating | Rationale |
|--------|--------|-----------|
| S | 8 | Product inoperable, 100% scrap |
| O | 4 | Tool wear monitored, offsets controlled (Cpk 1.2) |
| D | 4 | 100% CMM check with limit alarms |
| RPN | 128 | S×O×D = 8×4×4 |
| AP | High | S=8 with O≥4 and D≥4 |

### Example 2: Missing O-Ring

**Failure Mode**: O-ring not installed
**Effect**: Leak at customer, warranty claim
**Cause**: Operator missed step, no visual cue

| Factor | Rating | Rationale |
|--------|--------|-----------|
| S | 7 | Customer dissatisfaction, warranty |
| O | 6 | Manual operation, no poka-yoke |
| D | 7 | Visual check only, easy to miss |
| RPN | 294 | S×O×D = 7×6×7 |
| AP | High | High RPN, needs countermeasure |

**After adding presence sensor (poka-yoke):**

| Factor | Rating | Rationale |
|--------|--------|-----------|
| S | 7 | Effect unchanged |
| O | 2 | Poka-yoke prevents assembly without O-ring |
| D | 2 | Sensor verifies presence |
| RPN | 28 | S×O×D = 7×2×2 |
| AP | Low | Risk reduced |

### Example 3: Surface Scratch

**Failure Mode**: Scratch on machined surface
**Effect**: Cosmetic reject, customer complaint
**Cause**: Handling damage, chip interference

| Factor | Rating | Rationale |
|--------|--------|-----------|
| S | 5 | Rework possible (polish) |
| O | 5 | Occasional occurrence, handling controlled |
| D | 8 | Visual inspection, subjective |
| RPN | 200 | S×O×D = 5×5×8 |
| AP | Medium | Improve detection |

---

## Using This Reference

1. **Before PFMEA session**: Review scales with team
2. **During rating**: Reference specific criteria, not just numbers
3. **When disagreements**: Return to examples and criteria
4. **For calibration**: Use examples to align team understanding
5. **After actions**: Re-rate using same criteria
