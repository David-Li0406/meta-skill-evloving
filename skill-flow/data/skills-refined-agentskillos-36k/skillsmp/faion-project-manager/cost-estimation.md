---
id: cost-estimation
name: "Cost Estimation"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Cost Estimation

## Metadata
- **Category:** Project Management Framework 7 - Planning Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok, #business
- **Read Time:** 7 min
- **Agent:** faion-pm-agent

---

## Problem

Projects fail financially due to:
- Underestimating true costs
- Forgetting indirect costs
- No contingency for surprises
- Scope changes without budget updates

## Framework

### Cost Categories

| Category | Examples |
|----------|----------|
| **Direct Costs** | Salaries, contractors, software licenses |
| **Indirect Costs** | Office space, utilities, management overhead |
| **Fixed Costs** | Subscriptions, base salaries |
| **Variable Costs** | Overtime, cloud usage, contractor hours |

### Step 1: Bottom-Up Estimation

Estimate each work package from WBS:

```
Work Package: User Authentication
├── Design: 16 hours × $75/hr = $1,200
├── Development: 40 hours × $100/hr = $4,000
├── Testing: 8 hours × $60/hr = $480
├── Documentation: 4 hours × $50/hr = $200
└── Total: $5,880
```

### Step 2: Add Resource Costs

| Resource Type | Cost Calculation |
|---------------|------------------|
| **Full-time employee** | (Annual salary × 1.3) / working days |
| **Contractor** | Hourly rate × estimated hours |
| **Software** | License + seats + integration |
| **Infrastructure** | Provisioned + usage estimates |

### Step 3: Apply Three-Point Estimation

For uncertain costs:

```
Expected Cost = (Optimistic + 4×Most Likely + Pessimistic) / 6

Example - Cloud hosting:
O = $200/mo, M = $350/mo, P = $800/mo
Expected = (200 + 4×350 + 800) / 6 = $400/mo
```

### Step 4: Add Contingency Reserve

**Known Unknowns (Contingency):**
- 10-15% for well-defined projects
- 20-25% for innovative projects
- 30-40% for high-uncertainty projects

**Unknown Unknowns (Management Reserve):**
- Additional 5-10% held by sponsors
- Released only for major scope changes

### Step 5: Create Cost Baseline

```
Cost Baseline = Estimated Costs + Contingency Reserve

Budget at Completion (BAC) = Cost Baseline + Management Reserve
```

---

## Templates

### Cost Estimation Worksheet

```markdown
## Cost Estimate - [Project Name]

### Direct Costs

| Category | Item | Quantity | Unit Cost | Total |
|----------|------|----------|-----------|-------|
| Labor | Developer | 480 hrs | $100 | $48,000 |
| Labor | Designer | 80 hrs | $80 | $6,400 |
| Labor | PM | 160 hrs | $85 | $13,600 |
| Software | Figma | 3 months | $45 | $135 |
| Software | GitHub | 3 months | $40 | $120 |
| Cloud | AWS | 3 months | $400 | $1,200 |
| **Subtotal** | | | | **$69,455** |

### Indirect Costs

| Item | Rate | Total |
|------|------|-------|
| Office overhead | 10% of labor | $6,800 |
| Admin support | 5% of total | $3,473 |
| **Subtotal** | | **$10,273** |

### Reserves

| Type | Rate | Amount |
|------|------|--------|
| Contingency | 15% | $11,959 |
| Management Reserve | 5% | $3,986 |
| **Total Reserves** | | **$15,945** |

### Total Budget

| Component | Amount |
|-----------|--------|
| Direct Costs | $69,455 |
| Indirect Costs | $10,273 |
| Contingency | $11,959 |
| **Cost Baseline** | **$91,687** |
| Management Reserve | $3,986 |
| **Total Budget** | **$95,673** |
```

### Quick Estimation Formula

For rapid estimates:

```markdown
## Quick Project Cost

Labor Cost = (Team size × Avg daily rate × Duration in days)

Example:
- Team: 3 people
- Avg rate: $500/day
- Duration: 60 days
- Labor: 3 × $500 × 60 = $90,000

Add:
- Tools/licenses: +5-10%
- Infrastructure: +10-15%
- Contingency: +15-20%

Total estimate: $90,000 × 1.4 = $126,000
```

---

## Examples

### Example 1: SaaS MVP Cost Estimate

| Phase | Labor | Tools | Infra | Total |
|-------|-------|-------|-------|-------|
| Discovery (2 wks) | $8,000 | $200 | $0 | $8,200 |
| Design (2 wks) | $6,000 | $300 | $0 | $6,300 |
| Development (8 wks) | $48,000 | $500 | $400 | $48,900 |
| Testing (2 wks) | $8,000 | $100 | $200 | $8,300 |
| Launch (1 wk) | $4,000 | $0 | $300 | $4,300 |
| **Subtotal** | **$74,000** | **$1,100** | **$900** | **$76,000** |
| Contingency (20%) | | | | $15,200 |
| **Total** | | | | **$91,200** |

### Example 2: Solopreneur Opportunity Cost

For solopreneurs, calculate opportunity cost:

```markdown
## True Cost of Building vs Buying

**Build Option:**
- Your time: 100 hours
- Your hourly rate: $150/hr
- Opportunity cost: $15,000
- Out of pocket: $500 (tools)
- Total: $15,500

**Buy Option:**
- SaaS subscription: $99/mo × 12 = $1,188
- Setup time: 5 hours × $150 = $750
- Total: $1,938

Decision: Buy unless building creates unique competitive advantage
```

---

## Common Mistakes

1. **Forgetting overhead** - Salary ≠ total cost (add 30-50%)
2. **No scope contingency** - Scope always grows
3. **Optimistic estimates** - Take your estimate, add 50%
4. **Ignoring opportunity cost** - Your time has value
5. **Fixed price trap** - Variable scope + fixed price = failure

---

## Related Methodologies

- **Work Breakdown Structure:** Decomposing work into manageable packages
- **Earned Value Management:** Tracking cost and schedule performance
- **Change Control:** Managing changes to budget baseline

---

*Methodology from Project Management Framework 7 - Planning Performance Domain*
