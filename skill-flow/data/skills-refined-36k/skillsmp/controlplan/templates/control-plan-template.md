# Control Plan Template

## Header Information

| Field | Value |
|-------|-------|
| **Control Plan Number** | CP-[DEPT]-[SEQ] |
| **Revision** | |
| **Date** | |
| **Part Number** | |
| **Part Name/Description** | |
| **Customer** | |
| **Program** | |
| **Plant/Location** | MNMUK |

### Control Plan Phase

| Phase | Selected |
|-------|----------|
| Prototype | [ ] |
| Pre-Launch | [ ] |
| Production | [ ] |

### Key Contacts

| Role | Name | Phone |
|------|------|-------|
| Customer Engineering Contact | | |
| Supplier Engineering Contact | | |
| Quality Contact | | |

### Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Engineering | | | |
| Quality | | | |
| Customer (if required) | | | |

---

## Reference Documents

| Document Type | Number | Revision |
|---------------|--------|----------|
| Process Flow Diagram | | |
| PFMEA | | |
| Engineering Drawing | | |
| Customer Specifications | | |

---

## Control Plan Matrix

### Operation: [Number] - [Name]

**Machine/Device/Jig/Tool**: [Equipment used]

| Char No. | Characteristic | Prod/Proc | Class | Spec/Tolerance | Eval Method | Sample Size | Frequency | Control Method | Reaction Plan |
|----------|----------------|-----------|-------|----------------|-------------|-------------|-----------|----------------|---------------|
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |

---

### Operation: [Number] - [Name]

**Machine/Device/Jig/Tool**: [Equipment used]

| Char No. | Characteristic | Prod/Proc | Class | Spec/Tolerance | Eval Method | Sample Size | Frequency | Control Method | Reaction Plan |
|----------|----------------|-----------|-------|----------------|-------------|-------------|-----------|----------------|---------------|
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |

---

## Column Definitions

| Column | Description | Examples |
|--------|-------------|----------|
| **Char No.** | Unique identifier for characteristic | 1.1, 1.2, 2.1 |
| **Characteristic** | Feature being controlled | Diameter, Torque, Presence |
| **Prod/Proc** | Product or Process characteristic | Product / Process |
| **Class** | Special characteristic class | CC, SC, or blank |
| **Spec/Tolerance** | Requirement with units | 25.00 ±0.05 mm |
| **Eval Method** | Gage or measurement device | Micrometer, CMM, Visual |
| **Sample Size** | Quantity per check | 1, 5, 100% |
| **Frequency** | How often to check | Per pc, Per hr, Per setup |
| **Control Method** | Recording/charting method | SPC, Check sheet, Data log |
| **Reaction Plan** | Reference to reaction plan | RP-001, See below |

---

## Special Characteristics Summary

| Char No. | Characteristic | Class | Specification | Control Method |
|----------|----------------|-------|---------------|----------------|
| | | CC | | |
| | | SC | | |

---

## Reaction Plans

### RP-001: Dimension Out of Spec (Standard)

1. **STOP** - Halt production
2. **SEGREGATE** - Isolate suspect parts since last good
3. **NOTIFY** - Inform Supervisor within 30 min
4. **QUARANTINE** - Red tag, move to hold area
5. **INVESTIGATE** - Identify root cause
6. **CORRECT** - Implement fix
7. **VERIFY** - First piece approval
8. **SORT** - 100% inspect suspect parts
9. **DOCUMENT** - Record on NCR

### RP-002: Dimension Out of Spec (Critical)

1. **STOP** - Halt production immediately
2. **NOTIFY** - Inform Quality and Supervisor immediately
3. **QUARANTINE** - Red tag all suspect material
4. **CONTAIN** - Check downstream, notify customer if shipped
5. **INVESTIGATE** - Root cause analysis (5-Why)
6. **CORRECT** - Corrective action required before restart
7. **APPROVE** - Quality approval to restart
8. **VERIFY** - First piece + enhanced monitoring
9. **SORT** - 100% inspect all suspect
10. **DOCUMENT** - NCR, update PFMEA, 8D if customer affected

### RP-003: SPC Out of Control

1. **MARK** - Circle point on control chart
2. **CHECK** - Verify if within specification
3. **IF** within spec: Continue, investigate cause
4. **IF** out of spec: Follow RP-001 or RP-002
5. **IDENTIFY** - Determine assignable cause
6. **CORRECT** - Implement correction
7. **DOCUMENT** - Note cause and action on chart
8. **MONITOR** - Verify next 5 points in control

### RP-004: Visual Defect

1. **REJECT** - Place defective part in red bin
2. **ASSESS** - Isolated or trend?
3. **IF** isolated: Continue with enhanced attention
4. **IF** trend: Notify Supervisor, halt if needed
5. **IDENTIFY** - Root cause (tool, material, handling)
6. **CORRECT** - Implement fix
7. **DOCUMENT** - Scrap log, investigation if trend

### RP-005: Missing/Wrong Component

1. **STOP** - Halt production immediately
2. **SEGREGATE** - Isolate all units since last verification
3. **NOTIFY** - Inform Supervisor and Quality
4. **INVESTIGATE** - Wrong bin, wrong label, poka-yoke failure?
5. **VERIFY** - 100% of suspect units
6. **CORRECT** - Fix root cause
7. **RESTART** - With enhanced monitoring
8. **DOCUMENT** - NCR, update error-proofing if needed

---

## Gage List

| Gage ID | Description | Characteristic(s) | Calibration Due | MSA Status |
|---------|-------------|-------------------|-----------------|------------|
| | | | | |
| | | | | |
| | | | | |

---

## Revision History

| Rev | Date | Description | Author | Approved |
|-----|------|-------------|--------|----------|
| A | | Initial release | | |
| | | | | |

---

## Notes

1. This Control Plan must be reviewed and updated upon any engineering change, process change, or quality issue.
2. All gages listed must have current calibration and acceptable MSA.
3. Reaction plans must be followed exactly; deviations require Quality approval.
4. Special characteristics (CC/SC) require enhanced controls as specified.
5. Control Plan revision must match or exceed PFMEA revision.
