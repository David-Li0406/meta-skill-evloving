# Examples of Support Data Analysis

## Example 1: 60-Day Analysis with Trend Comparison

### User Request
```
"Can you analyze this support data and help me prioritize issues?
Focus on the last 60 days and show me how things are trending."

Files: Data Platform data - Code Orange.xlsx
```

### Analysis Process

#### Step 1: Data Loading
```
Loading Data Platform data - Code Orange.xlsx...

Sheets found:
- Ideas Forum: 21 records
- CSAT: 501 records (header fix applied)
- PIT and Roadblocks: 3,875 records
- Support Data: 5,000 records

Date filter: Last 60 days (Sep 1 - Oct 31, 2025)

Filtered results:
- PIT and Roadblocks: 105 records (2.7% of total)
- Support Data: 1,596 records (31.9% of total)
- CSAT: 500 records (99.8% of total - survey launched recently)

Total Issues (60 days): 2,201
```

#### Step 2: Theme Categorization
```
Combining by theme: {Product Area} > {Sub Category}

Top 10 Themes (60 days):
1. Object > Associations: 468 (21 PIT + 447 Support)
2. Properties > Edit Property: 232 (16 PIT + 216 Support)
3. Object > Record Property Value & History: 223 (3 PIT + 220 Support)
4. Object > Timeline: 169 (9 PIT + 160 Support)
5. Properties > Create Property: 162 (11 PIT + 151 Support)
6. Object > Record Customization: 140 (16 PIT + 124 Support)
7. Object > Record Actions: 121 (9 PIT + 112 Support)
8. Properties > Change History: 56 (2 PIT + 54 Support)
9. Object > Subscriptions: 36 (2 PIT + 34 Support)
10. Properties > Delete Property: 30 (0 PIT + 30 Support)

Calculating metrics for each theme...
```

#### Step 3: Priority Assignment
```
Applying prioritization framework:

P0 Candidates (≥150 issues OR ≥$75K MRR OR avg frustration ≥3.5 + volume >100):
- Object > Associations: 468 issues, $141K MRR, 3.38 frustration → P0 ✓
- Properties > Edit Property: 232 issues, $96K MRR, 3.06 frustration → P0 ✓
- Object > Record Property Value & History: 223 issues, $80K MRR, 2.33 frustration → P0 ✓ (high MRR + NEW to top 3)

P1 Candidates (100-149 issues OR frustration 3.0-3.5 + volume >50):
- Object > Timeline: 169 issues, $44K MRR, 2.89 frustration → P1 ✓
- Properties > Create Property: 162 issues, $68K MRR, 2.45 frustration → P1 ✓
- Object > Record Customization: 140 issues, $148K MRR, 2.94 frustration → P1 ✓
- Object > Record Actions: 121 issues, $71K MRR, 3.33 frustration → P1 ✓

P2 Candidates (30-99 issues OR high frustration + lower volume):
- Properties > Change History: 56 issues, $6K MRR, 3.50 frustration → P2 ✓ (high frustration)
- Object > Subscriptions: 36 issues, $37K MRR, 3.50 frustration → P2 ✓ (high frustration)

P3 (remaining <30 issues):
- Properties > Delete Property: 30 issues → P3
- All pipeline issues: 17 total → P3
```

#### Step 4: Customer Examples Selection
```
For P0 > Associations (468 issues):

Selecting 5 examples with diversity:
1. High frustration (5/5) + High MRR: Association Label Limit Increase ($4K MRR)
   - Use case: Complex B2B2B model hitting 50 label limit
2. Support ticket: Association Labels unavailable in reports
   - Most common complaint in support tickets
3. High frustration (4/5) PIT: Retrieve Object Association in Workflows
   - Workflow integration gap
4. Support ticket: Association inconsistency across pipelines
   - User confusion about behavior
5. High frustration (5/5) PIT: Deals-per-Company Limits
   - High-velocity business model blocked

Examples selected cover:
- Different frustration levels (mix of 4s and 5s)
- Different customer sizes (MRR range: $2K-$14K)
- Different sub-issues (limits, reporting, workflows, consistency)
- Mix of strategic (PIT) and tactical (support) feedback
```

#### Step 5: CSAT Analysis
```
CSAT Data (Oct 6-30, 2025):
- 500 responses
- Average score: 4.13/5
- Dissatisfied (<4): 129 (25.8%)

Top event triggers:
1. dealboard_view: 191 (deal pipeline views)
2. create_new_user: 181 (user management)
3. save_property: 128 (property editing)

Correlation with themes:
- "save_property" trigger → Properties > Edit Property (P0 #2)
- "dealboard_view" → Pipeline issues (lower volume in 60 days)
- "create_new_user" → Admin Setup (not in top themes)

Low-score feedback categories:
- Usability: 19 complaints
- Functionality gaps: 7 complaints
- Performance: 3 complaints
```

#### Step 6: Trend Analysis
```
Comparing 60 days vs. Historical (all-time):

Average Frustration:
- 60 days: 3.09/5
- Historical: 2.71/5
- Change: ↑ +14% (WORSENING)

Top Theme Percentage:
- Associations 60 days: 27.5%
- Associations historical: ~24%
- Change: ↑ +3.5pp (WORSENING)

NEW to Top 3:
- "Record Property Value & History" was #4 historically, now #3
- Signals: Data integrity issues increasing

Category Distribution:
- Object issues 60 days: 58%
- Object issues historical: 54%
- Change: ↑ +4pp (core CRM reliability concerns)
```

#### Step 7: Report Generation
```
Generating markdown report...

Structure:
1. Executive Summary
   ✓ Total: 2,201 issues
   ✓ Top 3 P0 with metrics
   ✓ Key changes vs historical
   ✓ Revenue at risk: $684K MRR

2. P0 Issues (3)
   ✓ Associations: Full metrics, 5 examples, "Why P0"
   ✓ Property Edit: Full metrics, 5 examples, "Why P0"
   ✓ Property Values: Full metrics, 5 examples, "Why P0"

3. P1 Issues (4)
   ✓ Timeline, Create Property, Customization, Record Actions

4. P2 Issues (2)
   ✓ Change History, Subscriptions

5. Strategic Recommendations
   ✓ Immediate actions for 3 P0 items
   ✓ High priority for P1 items
   ✓ Cross-cutting initiatives

6. Comparison table (60d vs historical)
7. Revenue priority table
8. Frustration heatmap
9. Methodology
10. Appendix

Report saved to: Data_Platform_Support_Analysis_60_Days.md
```

---

## Example 2: Historical Analysis (All-Time)

### User Request
```
"Analyze all the support data we have and give me the big picture on customer pain."

Files: Data Platform data - Code Orange.xlsx
```

### Key Differences from 60-Day Analysis

#### Priority Thresholds
```
P0: ≥1,000 issues (vs. ≥150 for 60-day)
P1: 700-999 issues (vs. 100-149)
P2: 200-699 issues (vs. 30-99)
P3: <200 issues (vs. <30)
```

#### Top Themes (All-Time)
```
1. Object > Associations: 2,153 issues (24.3%)
2. Properties > Edit Property: 1,137 issues (12.8%)
3. Properties > Create Property: 1,038 issues (11.7%)
4. Object > Record Property Value & History: 897 issues (10.1%)
5. Object > Record Customization: 856 issues (9.6%)

vs. 60-day top 5:
1. Associations: 27.5% (↑ increasing)
2. Edit Property: 13.6% (↑ increasing)
3. Property Values: 13.1% (↑↑ jumped from #4 to #3)
4. Timeline: 9.9%
5. Create Property: 9.5% (↓ decreasing)
```

#### Analysis Focus
- Less emphasis on trends (no recent baseline)
- More emphasis on Ideas Forum upvotes (validates long-term requests)
- Include all P0-P3 themes with full examples
- Revenue impact shown as total MRR across all time

---

## Example 3: Focused Analysis (Single Product Area)

### User Request
```
"Can you deep-dive on just the property management issues?
I want to understand all the sub-themes here."

Files: Data Platform data - Code Orange.xlsx
Time: Last 60 days
```

### Analysis Adjustments

#### Theme Scope
```
Filter to themes starting with "Properties >":
1. Edit Property: 232 issues
2. Create Property: 162 issues
3. Change History: 56 issues
4. Delete Property: 30 issues
5. Field Level Permissions: 27 issues
6. Export: 22 issues

Total Property Issues: 529 (31% of all support)
```

#### Sub-Theme Breakdown
```
Further categorize "Edit Property" issues:
- Cannot edit internal values: 67 issues
- Autosave breaking workflows: 31 issues
- Conditional logic not working: 28 issues
- Sensitive properties in workflows: 19 issues
- Default property changes: 15 issues
- Missing default properties: 12 issues
- Other: 60 issues

Further categorize "Create Property" issues:
- Cannot reference "today": 23 issues
- Calculation limits: 19 issues
- Unique identifier retroactive: 18 issues
- Score properties: 15 issues
- Lookup properties: 14 issues
- Other: 73 issues
```

#### Expanded Examples
```
For focused analysis, provide 7-10 examples per major sub-theme:

"Cannot edit internal values" (67 issues):
1. Lead source to deal source sync (support ticket)
2. Dropdown value mismatch (PIT, 3/5 frustration)
3. Integration breaking from internal value change (PIT, 5/5)
4. Enum property migration (support ticket)
5. Multi-language property values (PIT, 4/5)
6. API integration hardcoded to internal values (support ticket)
7. Cannot fix typo in internal value (support ticket)
```

#### Related Themes Section
```
Add section showing cross-product dependencies:

Property Edit issues relate to:
- Workflow automation (cannot use edited properties)
- Reporting (internal value changes break reports)
- Integrations (external systems reference internal values)
- Data migration (cannot evolve property schemas)
```

---

## Example 4: Customer Feedback Examples Document

### User Request
```
"Can you make a separate doc with lots of customer examples
for each pain point? I want to share this with the product team."

Files: Data Platform data - Code Orange.xlsx
Output: Two files requested
```

### Output Structure

**File 1: Main Analysis** (standard report)
**File 2: Customer Feedback Examples** (detailed quotes)

#### Example Document Structure
```markdown
# Data Platform Customer Feedback - Real Examples

For each major pain point, 5 real customer examples:

## P0 - CRITICAL IMPACT

### 1. Object Associations

#### Example 1: Association Label Limits Breaking Complex Business Models
**Frustration:** 5/5 | **MRR:** $4,049
> "Client wants to be able to have up to 900+ nested relationships..."

**What this means:** [Detailed interpretation]
**Customer impact:** [Business consequences]
**Workaround attempted:** [What customer tried]

[... 4 more detailed examples ...]

### Common Themes Across Feedback
1. Flexibility vs. Configuration Limits
2. Post-Creation Immutability
3. AI Bypassing Governance
[... continued analysis ...]
```

---

## Common Patterns and Anti-Patterns

### ✅ Good Practices

**Clear Customer Voice**
```markdown
❌ Don't synthesize:
> "Customers are frustrated with association limits"

✅ Do use real quotes:
> "Client wants to be able to have up to 900+ nested
   relationships, but we cap our association labels at 50"
```

**Specific Metrics**
```markdown
❌ Don't be vague:
> "Associations are a top issue"

✅ Do be specific:
> "Associations: 468 issues (27.5%), $141K MRR, 3.38/5 frustration"
```

**Actionable Recommendations**
```markdown
❌ Don't be generic:
> "Improve association functionality"

✅ Do be specific:
> "Enable association labels in reports/lists (blocking 468 customers)
   - Timeline: 30 days
   - Impact: $141K MRR"
```

### ❌ Anti-Patterns to Avoid

**Over-Aggregation**
- Don't just say "Property issues: 529"
- Break down into Edit (232), Create (162), etc.

**Missing "What This Means"**
- Don't just quote customers without interpretation
- Always explain the business impact

**Inconsistent Prioritization**
- Don't assign P0 to everything
- Use framework consistently: ~3-5 P0, ~5-7 P1

**Stale Comparisons**
- Don't compare 60-day to Q4 2024 as "historical"
- Use all-time data or clearly recent baseline (prior 60 days)

---

## Validation Checklist

Before delivering report, verify:

- [ ] All customer quotes are real (not paraphrased or generated)
- [ ] Metrics add up correctly (percentages sum to 100%)
- [ ] Priority assignments follow framework rules
- [ ] Each P0/P1 has exactly 5 examples (or noted why fewer)
- [ ] "What this means" interpretation for each example
- [ ] Strategic recommendations are actionable with timelines
- [ ] MRR totals are accurate
- [ ] Trend arrows (↑↓) are correct direction
- [ ] No customer PII in examples that shouldn't be there
- [ ] Report follows template structure
- [ ] Executive summary has specific numbers
- [ ] All referenced data sources are listed in methodology
