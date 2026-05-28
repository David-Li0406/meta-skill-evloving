# Control Plan - Extended Guidance

**Deep-dive content for complex Control Plan development and maintenance.**

---

## Table of Contents

1. [Control Plan Development Process](#control-plan-development-process)
2. [PFMEA Integration Details](#pfmea-integration-details)
3. [Special Characteristics Management](#special-characteristics-management)
4. [Sample Size Determination](#sample-size-determination)
5. [Control Method Selection](#control-method-selection)
6. [Reaction Plan Development](#reaction-plan-development)
7. [Control Plan Review and Maintenance](#control-plan-review-and-maintenance)
8. [Common Mistakes and Solutions](#common-mistakes-and-solutions)
9. [Audit Preparation](#audit-preparation)

---

## Control Plan Development Process

### Prerequisites

Before starting Control Plan development:

1. **Process Flow Diagram** - Finalized with all operations
2. **PFMEA** - Complete with all failure modes and controls
3. **Engineering Drawings** - Current revision with dimensions/specs
4. **Customer Requirements** - CSRs, special characteristics
5. **MSA Plan** - Identified gages, MSA status

### Development Steps

**Step 1: Extract from Process Flow**
- List all operations from PFD
- Include all inspection operations
- Note machine/equipment for each

**Step 2: Identify Characteristics**
- Product characteristics from drawing
- Process characteristics from PFMEA
- Customer-specified characteristics
- Internal quality characteristics

**Step 3: Classify Characteristics**
- Mark CC/SC per drawing and PFMEA
- Verify customer concurrence on classifications
- Document classification rationale

**Step 4: Define Controls**
- Select inspection method
- Determine sample size
- Set frequency
- Choose recording method
- Write reaction plan

**Step 5: Validate with PFMEA**
- Cross-reference all items
- Verify coverage of high-risk items
- Confirm special characteristics match

**Step 6: Review and Approve**
- Cross-functional review
- Customer approval (if required)
- Management sign-off

---

## PFMEA Integration Details

### Mapping Table

| PFMEA Element | Control Plan Element |
|---------------|---------------------|
| Process Step | Part/Process Number |
| Function | Product Characteristic |
| Process Parameter | Process Characteristic |
| S Rating | Drives Sample Frequency |
| D Rating | Validates Control Method |
| Current Detection Control | Control Method |
| Special Characteristic | Special Char Class |
| Recommended Action (Detection) | May add new control |

### Coverage Requirements

**Every Control Plan line should address:**
- At least one PFMEA failure mode
- High-risk items (S≥7 or RPN≥80)
- All special characteristics
- Customer-specified inspections

**Every high-risk PFMEA item should have:**
- Corresponding Control Plan entry
- Appropriate frequency for risk level
- Effective detection method
- Defined reaction plan

### When PFMEA Has No Corresponding Control Plan Entry

Valid reasons:
- Prevention control only (no inspection needed)
- Characteristic verified in different operation
- Inspection combined with another characteristic

Invalid reasons:
- Oversight (must add to Control Plan)
- "We always check it" without documentation
- Inspection exists but not documented

---

## Special Characteristics Management

### Customer Designation

Customers may use different symbols:
| Customer | CC Symbol | SC Symbol |
|----------|-----------|-----------|
| GM | Shield | Diamond |
| Ford | Inverted Delta | Inverted Delta |
| FCA | CC | SC |
| Toyota | Special | Important |
| VW/Audi | S | - |

**Best Practice:** Use customer symbol on their parts; internally standardize.

### Internal Identification

MNMUK may identify additional characteristics:
- Key Product Characteristics (KPC)
- Key Control Characteristics (KCC)
- Safety Characteristics
- Regulatory Characteristics

### Enhanced Control Requirements

**For CC (Critical):**
- 100% inspection or verified capable process (Cpk ≥1.67)
- SPC mandatory
- MSA completed (GR&R <10%)
- Error-proofing preferred
- Traceable records
- Annual review minimum

**For SC (Significant):**
- Appropriate sampling frequency
- SPC recommended
- MSA completed (GR&R <30%)
- Traceable records
- Annual review minimum

---

## Sample Size Determination

### Statistical Basis

Sample size depends on:
- Defect rate to detect
- Confidence level required
- Process capability

### AIAG Sampling Tables (Simplified)

**For Variables Data (measurement):**

| AQL | Sample Size (Lot ≤1000) | Sample Size (Lot >1000) |
|-----|-------------------------|-------------------------|
| 1.0% | 13 | 20 |
| 0.65% | 20 | 32 |
| 0.4% | 32 | 50 |
| 0.25% | 50 | 80 |

**For Attributes Data (pass/fail):**
Standard sampling plans per ANSI/ASQ Z1.4

### Practical Guidelines

| Scenario | Sample Size | Rationale |
|----------|-------------|-----------|
| New process, unproven | 100% | Validate capability |
| High Severity (9-10) | 100% | Safety critical |
| SPC capable (Cpk >1.33) | 5 per subgroup | Statistical control |
| Setup-sensitive | 3-5 at setup | Verify setup |
| Stable process | 1 per lot | Periodic verification |

### Sample Size for SPC

Standard subgroup sizes:
- X-bar/R chart: n=3 to 5
- X-bar/S chart: n≥10
- Individual/Moving Range: n=1

Frequency determined separately from size.

---

## Control Method Selection

### Method Selection Matrix

| Characteristic Type | Preferred Method | Alternative |
|--------------------|------------------|-------------|
| Dimension (tight tol) | CMM, Gage | Caliper |
| Dimension (loose tol) | Caliper | Visual with template |
| Position | CMM | Fixture gage |
| Surface finish | Profilometer | Comparison standard |
| Thread | Go/No-go | Thread gage |
| Hardness | Hardness tester | Certification |
| Presence/absence | Poka-yoke | Visual check |
| Torque | Torque wrench | Joint analysis |
| Leak | Leak tester | Pressure test |
| Appearance | Visual standard | Boundary samples |

### Control Method Effectiveness

| Method | Detection Rating (D) | Notes |
|--------|---------------------|-------|
| Poka-yoke (prevention) | 1-2 | Best - prevents defect |
| Poka-yoke (detection) | 2-3 | Flags defect |
| Automated 100% test | 2-3 | High reliability |
| Automated measurement + alarm | 3-4 | Good reliability |
| Variable gage (100%) | 4-5 | Operator dependent |
| Go/No-go gage (100%) | 5-6 | Binary decision |
| SPC with limits | 5-6 | Detects trends |
| Visual (100%) | 7-8 | Subjective |
| Sampling inspection | 8-9 | May miss defects |

### Recording Method Selection

| Scenario | Method | Format |
|----------|--------|--------|
| SPC characteristic | Control chart | X-bar/R, I-MR |
| Traceability required | Data log | Spreadsheet, database |
| Simple pass/fail | Check sheet | Form with checkboxes |
| Operator self-check | Work instruction | Embedded checkpoints |
| High volume | Electronic/MES | Automated capture |
| Error-proofed | None required | Poka-yoke record |

---

## Reaction Plan Development

### Reaction Plan Categories

**Type 1: Stop and Contain**
- For safety/critical characteristics
- Immediate production stop
- 100% sort of suspect material
- Root cause required before restart

**Type 2: Evaluate and Contain**
- For significant characteristics
- May continue if isolated
- Sort since last known good
- Investigation required

**Type 3: Adjust and Continue**
- For standard characteristics
- In-process adjustment
- Verify correction
- Document adjustment

### Standard Reaction Plan Elements

1. **Immediate Action**
   - What to do with current production
   - Who to notify

2. **Containment**
   - Scope of suspect material
   - Disposition of quarantined parts

3. **Root Cause Investigation**
   - Who investigates
   - Tools/methods to use

4. **Corrective Action**
   - Fix implementation
   - Verification method

5. **Documentation**
   - What to record
   - Where to record

### Reaction Plan Examples by Scenario

**Dimension Out of Tolerance (CC):**
```
REACTION PLAN RP-CC-001
1. STOP production immediately
2. SEGREGATE from last good part to current
3. NOTIFY Supervisor and Quality within 15 min
4. QUARANTINE all suspect parts (red tag, hold area)
5. INVESTIGATE root cause (5-Why)
6. CORRECTIVE ACTION before restart
7. FIRST PIECE approval required
8. 100% SORT all suspect material
9. DOCUMENT on NCR and Control Chart
10. UPDATE PFMEA if new failure mode
```

**SPC Out of Control (SC):**
```
REACTION PLAN RP-SPC-002
1. MARK control chart (circle point, note rule)
2. CHECK if within specification
3. IF within spec: Continue, investigate cause
4. IF out of spec: Follow RP-DIM-xxx
5. IDENTIFY assignable cause
6. IMPLEMENT correction
7. DOCUMENT cause and action on chart
8. VERIFY next 5 points in control
```

---

## Control Plan Review and Maintenance

### Review Triggers

**Mandatory Review:**
- Engineering change (ECO)
- Process change
- Customer complaint related to characteristic
- Internal quality issue
- PPAP resubmission
- Annual review

**Recommended Review:**
- New similar part launch
- Equipment change
- Supplier change
- After capability study
- Audit finding

### Review Process

1. Compare to current process
2. Verify PFMEA alignment
3. Confirm MSA status current
4. Review reaction plan effectiveness
5. Update revision and date
6. Obtain approvals
7. Distribute updated version
8. Train affected personnel

### Version Control

- Control Plan revision should match or reference PFMEA revision
- Changes should be traceable to cause
- Previous versions archived
- Current version at point of use

---

## Common Mistakes and Solutions

### Mistake 1: Generic Reaction Plans

**Problem:** "Contact supervisor" doesn't provide guidance
**Solution:** Specific steps with responsibilities and timing

### Mistake 2: Inconsistent with PFMEA

**Problem:** Control Plan doesn't reflect PFMEA controls
**Solution:** Side-by-side review, formal linkage process

### Mistake 3: Missing Special Characteristics

**Problem:** CC/SC not identified or controlled
**Solution:** Drawing review, customer confirmation, enhanced controls

### Mistake 4: Unrealistic Frequencies

**Problem:** 100% inspection can't be sustained
**Solution:** Match frequency to capability, verify sustainability

### Mistake 5: Outdated Control Plan

**Problem:** Actual process differs from document
**Solution:** Regular audits, change control process

### Mistake 6: Vague Control Methods

**Problem:** "Inspect per print" doesn't specify how
**Solution:** Specific gage, method, criteria

---

## Audit Preparation

### What Auditors Look For

1. **Current revision at work area**
   - Matches master list
   - Signed/approved

2. **Alignment with process**
   - Actual inspection matches Control Plan
   - Frequencies being met
   - Records exist

3. **PFMEA linkage**
   - High-risk items covered
   - Special characteristics identified
   - Controls effective

4. **Reaction plan evidence**
   - Out-of-spec events documented
   - Reaction plan followed
   - Effectiveness verified

5. **MSA status**
   - Gages in Control Plan have MSA
   - MSA results acceptable
   - Calibration current

### Common Audit Questions

- "How do you know this Control Plan is current?"
- "Show me the PFMEA linkage for this characteristic"
- "What's your reaction if this measurement is out of spec?"
- "Show me evidence the frequency is being met"
- "Where's the MSA for this gage?"
- "How do you verify reaction plans are followed?"

### Pre-Audit Checklist

- [ ] Control Plan revision current
- [ ] Copy at point of use
- [ ] PFMEA cross-referenced
- [ ] All gages calibrated
- [ ] MSA current for all gages
- [ ] Inspection records available
- [ ] Reaction plan records available
- [ ] Training records for inspectors
- [ ] Evidence of periodic review

---

## Advanced Topics

### Family Control Plans

For similar parts:
- Identify common characteristics
- Note part-specific variations
- Reference family plan plus supplement
- Maintain traceability to individual parts

### Digital Control Plans

Modern systems allow:
- Electronic at workstation
- Auto-populated from CAD/CAM
- Linked to real-time SPC
- Automated reaction notifications
- Revision control automated

### Customer-Specific Requirements

Some customers require:
- Specific format
- Additional columns
- Particular reaction plans
- Regular submission
- Pre-approval of changes

Check customer portal/requirements before finalizing.

---

## Integration Summary

```
Engineering Drawing
        ↓
   ┌────┴────┐
   ↓         ↓
 DFMEA    PFMEA
   ↓         ↓
   └────┬────┘
        ↓
   Control Plan  ←→  MSA
        ↓
   Work Instruction
        ↓
   Operator Execution
        ↓
   Quality Records
```

The Control Plan is the central document linking:
- Design requirements (what to control)
- Process risks (why to control)
- Measurement capability (how to control)
- Operator instructions (who controls)
- Quality evidence (proof of control)
