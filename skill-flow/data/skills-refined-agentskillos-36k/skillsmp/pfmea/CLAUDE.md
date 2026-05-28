# PFMEA - Extended Guidance

**Deep-dive content for complex PFMEA scenarios and advanced analysis.**

---

## Table of Contents

1. [AIAG-VDA Alignment](#aiag-vda-alignment)
2. [Team Composition](#team-composition)
3. [Structure and Function Analysis Deep Dive](#structure-and-function-analysis-deep-dive)
4. [Failure Mode Identification Techniques](#failure-mode-identification-techniques)
5. [Rating Calibration Sessions](#rating-calibration-sessions)
6. [Control Effectiveness Evaluation](#control-effectiveness-evaluation)
7. [PFMEA to Control Plan Linkage](#pfmea-to-control-plan-linkage)
8. [Common Pitfalls and How to Avoid Them](#common-pitfalls-and-how-to-avoid-them)
9. [PFMEA Review and Update Triggers](#pfmea-review-and-update-triggers)

---

## AIAG-VDA Alignment

The AIAG-VDA FMEA Handbook (1st Edition, 2019) aligns US and European approaches. Key changes from legacy AIAG 4th Edition:

### Action Priority vs RPN

**Old Approach (RPN):**
- RPN = S × O × D
- Single threshold (e.g., >100)
- All combinations treated equally

**New Approach (Action Priority):**
- Tables for High/Medium/Low priority
- Severity-weighted decisions
- S=9-10 always triggers action

**MNMUK Position:** Use both. Calculate RPN for historical comparison but apply AP for decision-making.

### Six Steps to Seven Steps

AIAG-VDA added "Planning and Preparation" as Step 1, emphasizing upfront scoping and team formation.

### Process Flow as Foundation

PFMEA must be built on documented process flow:
1. Process Flow Diagram (PFD) defines steps
2. Each PFD step becomes PFMEA row(s)
3. Process parameters linked to product characteristics

---

## Team Composition

### Required Team Members

| Role | Responsibility | MNMUK Position |
|------|----------------|----------------|
| PFMEA Lead | Facilitates sessions, documents | Quality Engineer |
| Process Engineer | Process knowledge, parameters | Manufacturing Engineer |
| Product Engineer | Design intent, specifications | Design Engineer |
| Quality Engineer | Control methods, inspection | Quality Engineer |
| Production | Practical operation knowledge | Cell Leader/Operator |
| Maintenance | Equipment reliability | Maintenance Tech |
| Supplier Quality | Incoming material risks | SQE (if applicable) |

### Team Size
- Ideal: 4-6 members
- Minimum: 3 members (multidisciplinary)
- Maximum: 8 members (becomes unwieldy)

### Session Management
- Sessions: 2-4 hours maximum
- Frequency: Weekly during development
- Preparation: Distribute process flow 48 hours prior
- Documentation: Real-time capture, distribute within 24 hours

---

## Structure and Function Analysis Deep Dive

### Building the Process Tree

**Level 1: System** (Overall process)
- Example: "Engine Piston Machining Process"

**Level 2: Sub-system** (Process phases)
- Example: "Rough Turning", "Finish Turning", "Inspection"

**Level 3: Process Element** (Individual operations)
- Example: "Face first end", "Bore center", "Turn OD"

### Function Statement Writing

Good function statements are:
- **Specific**: Measurable outcome
- **Observable**: Can be verified
- **Complete**: Includes requirements

**Format**: [Action verb] + [Object] + [Requirement/Specification]

**Examples**:
- ✓ "Machine piston OD to 85.00mm ±0.02mm"
- ✓ "Apply sealant in continuous bead, 3mm ±0.5mm width"
- ✗ "Machine piston" (too vague)
- ✗ "Good surface finish" (not measurable)

### Linking to Requirements

Each function should trace to:
- Customer specification
- Engineering drawing
- Internal standard
- Regulatory requirement

Document reference: "Per drawing 12345, revision C, zone A3"

---

## Failure Mode Identification Techniques

### Brainstorming Framework

For each function, ask:
1. **Complete failure**: What if it doesn't happen at all?
2. **Partial failure**: What if it happens incompletely?
3. **Excessive**: What if it happens too much?
4. **Intermittent**: What if it happens inconsistently?
5. **Wrong**: What if something else happens instead?
6. **Unintended**: What else might happen?

### Historical Data Sources

Check these for known failure modes:
- Previous PFMEA (similar products/processes)
- Customer complaints
- Warranty returns
- Scrap/rework reports
- 8D/CAPA records
- Supplier quality data
- Audit findings

### Failure Mode Categories

**Dimensional Failures**:
- Oversize / Undersize
- Out of tolerance
- Out of location
- Out of roundness/flatness

**Assembly Failures**:
- Missing component
- Wrong component
- Reversed/misoriented
- Incorrect quantity
- Loose/over-tightened

**Surface Failures**:
- Scratched/damaged
- Contaminated
- Incorrect finish
- Corrosion

**Material Failures**:
- Wrong material
- Defective material
- Material handling damage

---

## Rating Calibration Sessions

### Purpose

Ensure team alignment on ratings before PFMEA sessions. Different team members often rate the same scenario differently.

### Calibration Exercise

1. Select 10 diverse failure scenarios
2. Each team member rates S, O, D independently
3. Compare ratings
4. Discuss discrepancies
5. Agree on rating rationale
6. Document calibration decisions

### Handling Disagreements

When team disagrees on rating:
1. Return to criteria definitions
2. Cite specific examples from MNMUK experience
3. If still unclear, use higher rating (conservative)
4. Document rationale for future reference

### Common Calibration Issues

**Severity:**
- "Customer" = end user, not next operation
- Consider worst-case failure effect
- Don't reduce S based on detection

**Occurrence:**
- Rate the cause, not the failure mode
- Consider historical data if available
- New process with no data = higher O

**Detection:**
- Rate current controls, not proposed
- Consider false pass risk
- Visual inspection rarely better than D=7

---

## Control Effectiveness Evaluation

### Current Control Types

**Prevention Controls** (Reduce Occurrence):
- Error-proofing (poka-yoke)
- Process capability (Cpk)
- Tool condition monitoring
- Preventive maintenance
- Training/certification

**Detection Controls** (Improve Detection):
- 100% inspection
- Statistical sampling
- SPC monitoring
- Automated gauging
- Final test

### Control Effectiveness Matrix

| Control Type | Typical D Rating | Effectiveness |
|--------------|------------------|---------------|
| Poka-yoke (physical prevention) | 1-2 | Very High |
| Automated 100% test | 2-3 | High |
| Automated measurement + alarm | 3-4 | High |
| Variable gage, 100% | 4-5 | Moderate |
| Go/No-go gage, 100% | 5-6 | Moderate |
| SPC with control limits | 5-6 | Moderate |
| Visual inspection, 100% | 7-8 | Low |
| Sampling inspection | 8-9 | Very Low |
| No inspection | 10 | None |

### Validating Controls

Before rating Detection, verify:
- Control is actually performed (observe)
- Gage/equipment is calibrated
- Operator trained on method
- Sampling adequate for defect rate
- Records demonstrate effectiveness

---

## PFMEA to Control Plan Linkage

### Required Linkage

Every Control Plan entry should trace to PFMEA:
- PFMEA process step → Control Plan operation
- PFMEA characteristic → Control Plan characteristic
- PFMEA detection control → Control Plan control method

### Special Characteristics Flow

```
PFMEA                          Control Plan
───────                        ────────────
SC/CC identified      →        SC/CC marked
Enhanced controls     →        Specific methods
Detection rating      →        Inspection frequency
Prevention rating     →        Process controls
```

### When PFMEA Changes

PFMEA update triggers Control Plan review:
- New failure mode added → New control needed?
- Rating changes → Inspection frequency change?
- New control implemented → Add to Control Plan
- Countermeasure completed → Update Control Plan

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Analysis Paralysis

**Problem**: Team spends excessive time debating ratings
**Solution**: Set time limits (5 min max per failure mode), use "parking lot" for complex items

### Pitfall 2: PFMEA as Paperwork Exercise

**Problem**: Completed to check a box, not used for decisions
**Solution**: Link to real actions, review in management meetings, track countermeasure completion

### Pitfall 3: Copying from Similar PFMEA

**Problem**: Blindly copying without validation
**Solution**: Use as starting point, verify each item applies, add process-specific items

### Pitfall 4: Rating Inflation/Deflation

**Problem**: Consistently rating too high or too low
**Solution**: Calibration sessions, benchmark against known issues, management review

### Pitfall 5: Ignoring Low-RPN Items

**Problem**: Only focusing on high RPN
**Solution**: Also review any S≥8 regardless of RPN, review all items periodically

### Pitfall 6: Static Document

**Problem**: PFMEA never updated after initial creation
**Solution**: Define update triggers, assign owner, periodic review schedule

---

## PFMEA Review and Update Triggers

### Mandatory Updates

- Customer complaint related to process
- Internal quality issue (scrap, rework)
- Process change (equipment, method, material)
- Engineering change order (ECO)
- Supplier change
- New similar part (review applicability)

### Periodic Review

- Minimum: Annually
- Recommended: Quarterly for high-volume production
- Required: Before PPAP resubmission

### Update Process

1. Identify trigger event
2. Locate affected PFMEA item(s)
3. Re-evaluate ratings
4. Add new failure modes if applicable
5. Update countermeasures
6. Revise document
7. Communicate changes to team
8. Update Control Plan if needed

---

## Advanced Topics

### Design FMEA vs Process FMEA Interface

| Aspect | DFMEA | PFMEA |
|--------|-------|-------|
| Focus | Product design | Manufacturing process |
| Failure Modes | Design flaws | Process failures |
| Causes | Design decisions | Process variables |
| Controls | Design features | Process controls |

**Interface Points:**
- DFMEA special characteristics → PFMEA inputs
- DFMEA failure modes → Process must handle
- PFMEA feedback → Design improvements

### Reverse FMEA

Use when quality issues occur:
1. Start with known failure (scrap, complaint)
2. Identify which process step
3. Determine actual cause
4. Review PFMEA for that step
5. Add if missing, update if found
6. Implement countermeasures
7. Track effectiveness

### FMEA Software Tools

For complex PFMEAs, consider:
- APIS IQ-Software
- Relyence FMEA
- PTC Windchill Quality Solutions
- Excel (basic, but accessible)

**MNMUK Current State:** Excel-based templates with consideration for software migration as volume increases.

---

## Templates and Examples

See `~/.claude/skills/Pfmea/templates/pfmea-template.md` for standard format.
See `~/.claude/skills/Pfmea/reference/common-failure-modes.md` for examples by department.

---

## Key Principles

1. **Cross-functional team** - Not a solo activity
2. **Process flow foundation** - No PFMEA without process flow
3. **Living document** - Update throughout product lifecycle
4. **Action-oriented** - Drives countermeasures, not just documentation
5. **Customer focus** - Severity always from customer perspective
6. **Data-driven** - Use actual failure data when available
7. **Linked system** - PFMEA → Control Plan → Work Instruction
