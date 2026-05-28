---
id: financial-planning
name: "Financial Planning"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Financial Planning

## Metadata

| Field | Value |
|-------|-------|
| **ID** | financial-planning |
| **Name** | Financial Planning |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | pricing-strategy, tax-considerations, annual-planning |

---

## Problem

You're building a business, not a hobby. But you don't know your numbers. You don't know your profit margin, your runway, or whether you can afford to invest in growth. Without financial clarity, you're flying blind.

Financial planning means understanding your money so you can make better decisions.

---

## Framework

Financial planning follows this structure:

```
TRACK    -> Know where money goes
ANALYZE  -> Understand unit economics
FORECAST -> Project the future
DECIDE   -> Make informed choices
REVIEW   -> Adjust based on reality
```

### Step 1: Track Everything

**Essential tracking:**

| Category | What to Track | Tool |
|----------|---------------|------|
| Revenue | All income sources | Stripe, accounting |
| Expenses | All costs | Bank, accounting |
| Cash | Bank balance | Bank |
| Receivables | Money owed to you | Invoicing tool |
| Metrics | MRR, churn, CAC | Spreadsheet |

**Revenue tracking:**

| Revenue Type | How to Track |
|--------------|--------------|
| Subscriptions | Stripe dashboard, MRR |
| One-time sales | Payment processor |
| Services | Invoices sent/paid |
| Affiliate/ads | Platform reporting |

**Expense categories:**

| Category | Examples | Typical % |
|----------|----------|-----------|
| Infrastructure | Hosting, tools, domains | 5-15% |
| Marketing | Ads, content, tools | 10-30% |
| Operations | Software, services | 5-10% |
| Contractors | Design, dev, support | 10-30% |
| Administrative | Legal, accounting | 2-5% |
| Owner pay | Your salary | Remainder |

### Step 2: Understand Unit Economics

**Key metrics:**

| Metric | Formula | Healthy Target |
|--------|---------|----------------|
| **LTV** | ARPU / Churn rate | > 3x CAC |
| **CAC** | Marketing spend / New customers | < 1/3 LTV |
| **Gross margin** | (Revenue - COGS) / Revenue | > 70% (SaaS) |
| **Net margin** | Profit / Revenue | > 20% |
| **Payback period** | CAC / (ARPU x Gross margin) | < 12 months |

**Example calculation:**

```
ARPU = $50/month
Churn = 5%/month
LTV = $50 / 0.05 = $1,000

Ad spend = $5,000
New customers = 50
CAC = $5,000 / 50 = $100

LTV:CAC = $1,000 / $100 = 10:1 (excellent)
```

### Step 3: Build Financial Model

**Simple P&L model:**

```markdown
## Monthly P&L

### Revenue
- Subscription: $X
- One-time: $X
- Other: $X
- **Total Revenue: $X**

### Cost of Goods Sold (COGS)
- Hosting: $X
- Transaction fees: $X
- **Total COGS: $X**

### Gross Profit: $X (X%)

### Operating Expenses
- Marketing: $X
- Tools/software: $X
- Contractors: $X
- Other: $X
- **Total OpEx: $X**

### Operating Profit: $X (X%)

### Owner Pay: $X
### Net Profit: $X (X%)
```

**Cash flow projection:**

| Month | Starting | Revenue | Expenses | Ending |
|-------|----------|---------|----------|--------|
| Jan | $10K | $5K | $4K | $11K |
| Feb | $11K | $6K | $4K | $13K |
| Mar | $13K | $7K | $5K | $15K |

### Step 4: Plan for Growth

**Reinvestment framework:**

| Profit Level | Reinvestment | Owner Pay | Reserve |
|--------------|--------------|-----------|---------|
| Breakeven | 0% | 0% | 100% |
| < $5K profit | 50% | 30% | 20% |
| $5-15K profit | 40% | 40% | 20% |
| > $15K profit | 30% | 50% | 20% |

**Investment priorities:**

| Priority | Why | Example |
|----------|-----|---------|
| 1. Retention | Keeps revenue | Product improvements |
| 2. Conversion | More customers | Landing page optimization |
| 3. Acquisition | Growth | Ads, content |
| 4. Operations | Efficiency | Tools, automation |
| 5. Expansion | New revenue | New features, products |

### Step 5: Financial Safety

**Runway calculation:**

```
Runway = Cash on hand / Monthly burn rate

$30,000 cash / $5,000 monthly expenses = 6 months runway
```

**Safety targets:**

| Stage | Minimum Runway |
|-------|----------------|
| Pre-revenue | 12+ months |
| Early revenue | 6+ months |
| Growing | 3+ months |
| Profitable | 3+ months (emergency fund) |

**Emergency fund:**

```
Target: 3 months of operating expenses
If expenses = $5K/month
Emergency fund = $15K (separate account)
```

---

## Templates

### Monthly Financial Review

```markdown
## Financial Review: [Month]

### Revenue
| Source | Amount | vs. Last Month | vs. Target |
|--------|--------|----------------|------------|
| Subscriptions | $X | +X% | X% of goal |
| One-time | $X | +X% | X% of goal |
| **Total** | $X | +X% | X% of goal |

### Expenses
| Category | Amount | vs. Last Month | % of Revenue |
|----------|--------|----------------|--------------|
| Infrastructure | $X | - | X% |
| Marketing | $X | - | X% |
| Contractors | $X | - | X% |
| Other | $X | - | X% |
| **Total** | $X | - | X% |

### Profitability
- Gross profit: $X (X%)
- Operating profit: $X (X%)
- Owner pay: $X

### Key Metrics
- MRR: $X (from $X)
- Customers: X (from X)
- Churn: X%
- CAC: $X
- LTV: $X

### Cash Position
- Starting: $X
- Ending: $X
- Runway: X months

### Next Month Focus
- [Priority 1]
- [Priority 2]
```

### Annual Budget Template

```markdown
## Annual Budget: [Year]

### Revenue Forecast
| Quarter | Target | Assumption |
|---------|--------|------------|
| Q1 | $X | X customers @ $X ARPU |
| Q2 | $X | X% growth |
| Q3 | $X | X% growth |
| Q4 | $X | X% growth |
| **Annual** | $X | - |

### Expense Budget
| Category | Q1 | Q2 | Q3 | Q4 | Annual |
|----------|----|----|----|----|--------|
| Infrastructure | $X | $X | $X | $X | $X |
| Marketing | $X | $X | $X | $X | $X |
| Tools | $X | $X | $X | $X | $X |
| Contractors | $X | $X | $X | $X | $X |
| **Total** | $X | $X | $X | $X | $X |

### Target Profit
- Revenue: $X
- Expenses: $X
- Profit: $X (X%)

### Investment Plan
- [Investment 1]: $X
- [Investment 2]: $X
- [Investment 3]: $X
```

### Unit Economics Dashboard

```markdown
## Unit Economics: [Product]

### Current Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| ARPU | $X | $X | On track |
| CAC | $X | <$X | Needs work |
| LTV | $X | >$X | On track |
| LTV:CAC | X:1 | >3:1 | On track |
| Payback | X mo | <12 mo | On track |
| Churn | X% | <X% | At risk |

### Trend
| Month | ARPU | CAC | LTV:CAC |
|-------|------|-----|---------|
| [Month] | $X | $X | X:1 |
| [Month] | $X | $X | X:1 |
| [Month] | $X | $X | X:1 |

### Actions
- To improve CAC: [Action]
- To improve churn: [Action]
```

---

## Examples

### Example 1: SaaS Financial Planning

**Situation:** SaaS tool, $10K MRR

**Monthly P&L:**
```
Revenue: $10,000
- Hosting: $500 (5%)
- Transaction fees: $300 (3%)
Gross profit: $9,200 (92%)

- Marketing: $2,000 (20%)
- Tools: $300 (3%)
- Contractor: $1,500 (15%)
Operating profit: $5,400 (54%)

- Owner pay: $4,000
Net profit: $1,400 (14%)
```

**Analysis:**
- Healthy gross margin (92%)
- Good operating margin (54%)
- CAC of $100 with LTV of $800 = 8:1 ratio
- 6 months runway

### Example 2: Info Product Business

**Situation:** Online course, variable revenue

**Monthly average:**
```
Revenue: $8,000 (varies $3K-15K)
- Platform fees: $800 (10%)
Gross profit: $7,200 (90%)

- Ads: $1,500 (19%)
- Tools: $200 (3%)
- Content: $500 (6%)
Operating profit: $5,000 (63%)

- Owner pay: $3,500
Net profit: $1,500 (19%)
```

**Analysis:**
- High variability requires larger cash reserve
- Target: 6 months expenses in reserve
- Reinvest profits in evergreen content

---

## Implementation Checklist

### Setup
- [ ] Set up accounting (QuickBooks, Wave, spreadsheet)
- [ ] Connect payment processors
- [ ] Create expense categories
- [ ] Set up monthly review

### Tracking
- [ ] Track all revenue sources
- [ ] Categorize all expenses
- [ ] Monitor cash position
- [ ] Calculate unit economics

### Planning
- [ ] Create monthly budget
- [ ] Build 12-month forecast
- [ ] Set profit targets
- [ ] Plan investments

### Review
- [ ] Weekly: Check cash position
- [ ] Monthly: Full financial review
- [ ] Quarterly: Update forecast
- [ ] Annually: Budget planning

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Not tracking | Flying blind | Track from day 1 |
| Mixing personal | Tax and legal issues | Separate accounts |
| No runway | One bad month = crisis | Maintain 3+ months |
| Ignoring unit economics | Scaling unprofitable | Know your numbers |
| No owner pay | Burnout, undervalue | Pay yourself first |
| Over-investing | Cash flow problems | Reinvest from profit |

---

## Financial Ratios Quick Reference

| Ratio | Formula | Target |
|-------|---------|--------|
| Gross margin | (Revenue - COGS) / Revenue | > 70% |
| Operating margin | Operating profit / Revenue | > 20% |
| Net margin | Net profit / Revenue | > 10% |
| LTV:CAC | LTV / CAC | > 3:1 |
| Rule of 40 | Revenue growth % + Profit margin % | > 40% |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Accounting | QuickBooks, Wave, Xero |
| Invoicing | Stripe, PayPal, Invoice Ninja |
| Metrics | Baremetrics, ProfitWell |
| Spreadsheets | Google Sheets, Excel |
| Banking | Mercury, Relay |

---

## Related Methodologies

- **pricing-strategy:** Pricing Strategy (revenue optimization)
- **tax-considerations:** Tax Considerations (tax planning)
- **annual-planning:** Annual Planning (yearly financial planning)
- **metrics-dashboards:** Metrics & Dashboards (tracking setup)

---

*Methodology: financial-planning | Operations & Business | faion-growth-agent*
