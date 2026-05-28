# Prioritization Framework

## Overview

This framework provides objective criteria for assigning priority levels (P0, P1, P2, P3) to customer support themes based on multiple impact factors.

## Priority Criteria

### P0 - CRITICAL IMPACT

**Assign P0 when ANY of these conditions are met:**

1. **High Volume (Primary):**
   - Last 60 days: ≥150 total issues
   - Historical/All-time: ≥1,000 total issues
   - OR: Theme represents ≥20% of all issues in the period

2. **High Frustration + Substantial Volume:**
   - Average frustration ≥3.5/5 AND
   - Volume ≥100 issues

3. **Significant Revenue at Risk:**
   - Last 60 days: ≥$75,000 MRR
   - Historical/All-time: ≥$4,000,000 MRR

4. **Increasing Trend (Worsening):**
   - Volume increased >20% vs. baseline period OR
   - Moved into top 5 from outside top 10 historically OR
   - Frustration increased >0.5 points vs. baseline

**Typical P0 Themes:**
- Core CRM functionality (associations, properties, records)
- Data integrity issues (sync failures, calculation errors)
- Blocking issues (cannot complete workflows, data loss)

---

### P1 - HIGH IMPACT

**Assign P1 when ANY of these conditions are met:**

1. **Moderate-High Volume:**
   - Last 60 days: 100-149 total issues
   - Historical/All-time: 700-999 total issues
   - OR: Theme represents 10-20% of all issues

2. **Moderate Frustration + Good Volume:**
   - Average frustration 3.0-3.49/5 AND
   - Volume ≥50 issues

3. **Moderate Revenue at Risk:**
   - Last 60 days: $25,000-$74,999 MRR
   - Historical/All-time: $1,500,000-$3,999,999 MRR

4. **High Frustration + Lower Volume:**
   - Average frustration ≥3.5/5 AND
   - Volume 30-99 issues

**Typical P1 Themes:**
- Daily productivity features (record customization, activities)
- Advanced features with moderate adoption
- Integration issues affecting multiple customers

---

### P2 - MEDIUM IMPACT

**Assign P2 when ANY of these conditions are met:**

1. **Moderate Volume:**
   - Last 60 days: 30-99 total issues
   - Historical/All-time: 200-699 total issues

2. **High Frustration, Low Volume (Specialized):**
   - Average frustration ≥3.5/5 AND
   - Volume 10-29 issues
   - Indicates: High pain when encountered, but affects specialized use cases

3. **Moderate Revenue, Lower Volume:**
   - Last 60 days: $10,000-$24,999 MRR
   - Historical/All-time: $500,000-$1,499,999 MRR

**Typical P2 Themes:**
- Power user features (advanced automation, complex reporting)
- Specialized object types or workflows
- Administrative features (audit logs, permissions)

---

### P3 - LOWER IMPACT

**Assign P3 when ALL of these are true:**

1. **Low Volume:**
   - Last 60 days: <30 total issues
   - Historical/All-time: <200 total issues

2. **Lower Frustration OR Very Specialized:**
   - Average frustration <3.0/5 OR
   - Affects only specific edge cases or rare workflows

3. **Lower Revenue:**
   - Last 60 days: <$10,000 MRR
   - Historical/All-time: <$500,000 MRR

**Typical P3 Themes:**
- Administrative tasks (property cleanup, bulk operations)
- Rare edge cases
- Nice-to-have enhancements

---

## Tie-Breaking Rules

When a theme has conflicting signals (e.g., high volume but low frustration), apply these rules:

### Rule 1: Volume Trumps Frustration for Top Issues
- If volume places theme in top 5, assign at least P1 even if frustration is low
- **Rationale:** High volume indicates widespread impact regardless of individual pain level

### Rule 2: Frustration Elevates Priority When High
- If frustration ≥3.5/5, bump priority up one level (P2 → P1, P1 → P0)
- **Rationale:** High frustration indicates severe pain that risks churn

### Rule 3: Revenue Protects Critical Accounts
- If single theme affects >$100K MRR in 60 days, assign P0 regardless of volume
- **Rationale:** Enterprise/strategic account retention is critical

### Rule 4: Trends Override Snapshots
- If theme is rapidly worsening (>30% increase), bump up one level
- **Rationale:** Catching problems early prevents escalation

### Rule 5: "NEW to Top 5" Requires Investigation
- If theme wasn't in top 10 historically but now in top 5, assign at least P1
- **Rationale:** Sudden emergence suggests new product issue or changing customer needs

---

## Special Considerations

### Data Integrity Issues
**Always assign P0 if:**
- Property values syncing incorrectly
- Calculation properties showing wrong values
- Data loss occurring (activities not logging, merge losing data)

**Rationale:** Data integrity undermines trust in entire platform.

### Workflow Blockers
**Assign P0 if:**
- Issue prevents completing core workflows (creating records, associations, etc.)
- Workaround requires custom code or manual intervention at scale

**Rationale:** Blocking issues force customers to abandon features or churn.

### Product Changes Causing Regression
**Assign P1 minimum if:**
- Recent product change caused spike in issues
- Customers report "this used to work"

**Rationale:** Regressions erode customer trust and indicate product quality issues.

### Audit/Compliance Gaps
**Assign P2 minimum if:**
- Missing change history/audit logs
- Cannot track who made changes
- Compliance requirement for customer industry

**Rationale:** Compliance blockers prevent enterprise adoption.

---

## Edge Case Guidance

### Low PIT Volume, High Support Volume
- Weight support tickets equally with PIT for prioritization
- **Example:** 5 PIT + 300 support tickets = 305 total (likely P0)

### High Volume, Low Frustration
- Still assign high priority (P0/P1) based on volume
- Note in report: "High volume but lower frustration suggests usability issue vs. blocker"

### High Frustration, Low Volume
- Assign P2 and investigate if specialized use case
- Flag for potential feature gap or edge case fix

### Missing MRR Data
- Use volume + frustration only
- Note in report: "MRR data incomplete, prioritization based on volume and frustration"

### Support-Only Themes (No PIT Data)
- Valid for prioritization (support tickets = customer pain)
- Lack of PIT data may mean:
  - Too tactical for strategic feedback
  - Self-service issues (not reaching account team)
  - Recent issue (hasn't reached quarterly reviews)

---

## Example Prioritization Decisions

### Example 1: Associations
- Volume: 468 issues (27.5%)
- Frustration: 3.38/5
- MRR: $141K
- **Decision:** P0 (volume >150, represents >20% of issues, high MRR)

### Example 2: Change History
- Volume: 56 issues (3.3%)
- Frustration: 3.50/5
- MRR: $6K
- **Decision:** P2 (low volume but high frustration = specialized high-pain)

### Example 3: Property Values (60-day analysis)
- Volume: 223 issues (13.1%)
- Frustration: 2.33/5
- MRR: $80K
- Trend: NEW to top 3
- **Decision:** P0 (high volume + high MRR + worsening trend + data integrity)

### Example 4: Pipeline Customization
- Volume: 4 issues (0.2%)
- Frustration: 3.75/5
- MRR: $7K
- **Decision:** P3 (very low volume despite high frustration = edge case)

---

## Validation Checklist

After assigning priorities, verify:

- [ ] All themes >150 issues (60-day) assigned P0 or P1
- [ ] Top 5 themes by volume are P0 or P1
- [ ] Any theme with avg frustration ≥3.5 is P2 minimum
- [ ] Data integrity issues are P0
- [ ] Workflow blockers are P0
- [ ] At least 3 themes in each priority level (unless insufficient data)
- [ ] Priority distribution is reasonable (~5-10 P0, ~5-10 P1, rest P2/P3)

## Notes

- **Be Conservative with P0:** Reserve for truly critical issues. Over-assigning P0 dilutes urgency.
- **Document Rationale:** Always include "Why P0/P1/P2" explanation in report
- **Update Framework:** If new patterns emerge, propose updates to this framework
