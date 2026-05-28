---
name: excel-lbo-modeler
description: Use this skill when you need to create leveraged buyout (LBO) models in Excel, including sources & uses, debt schedules, cash flow waterfalls, and IRR calculations for private equity analysis.
---

# Skill body

Builds comprehensive LBO models for private equity transactions following industry-standard practices.

## When to Invoke This Skill

Automatically load this Skill when the user asks to:
- "Create an LBO model"
- "Build a leveraged buyout model"
- "Private equity analysis for [company]"
- "Calculate IRR for acquisition"
- "LBO for [company]"
- "Buyout model"
- "What returns can we get on this deal?"

## Model Structure

This Skill creates a complete 6-sheet Excel LBO model:

### Sheet 1: Transaction Summary
- **Deal Terms**: Purchase price, entry multiple, equity check
- **Sources & Uses**: How the deal is financed
- **Returns Summary**: IRR, MoM, hold period

### Sheet 2: Sources & Uses

**Uses of Funds:**
```
Purchase Equity Value
+ Estimated Net Debt
= Enterprise Value
+ Transaction Fees (2-3%)
+ Financing Fees (2-3%)
= Total Uses
```

**Sources of Funds:**
```
Revolver (typically 0% at close)
+ Term Loan A (2-3x EBITDA)
+ Term Loan B (2-3x EBITDA)
+ Subordinated Debt (1-2x EBITDA)
+ Preferred Equity (optional)
+ Sponsor Equity (remainder)
= Total Sources
```

### Sheet 3: Operating Model (5 Years)
```
Revenue
  × Revenue Growth %
  × EBITDA Margin %
= EBITDA
  - CapEx
  - Change in NWC
  - Cash Taxes
= Cash Flow Available for Debt Service
```

### Sheet 4: Debt Schedule

**For Each Debt Tranche:**
```
Beginning Balance
+ Draws (if revolver)
- Mandatory Amortization
- Excess Cash Flow Sweep
- Optional Prepayment
= Ending Balance

Interest Expense = Avg Balance × Interest Rate
```

**Debt Paydown Waterfall:**
1. Revolver paydown
2. Term Loan A amortization
3. Term Loan B amortization
4. Excess cash → Revolver
5. Remaining excess → Optional prepayments

### Sheet 5: Returns Analysis

**Exit Valuation:**
```
Exit Year EBITDA
  × Exit Multiple
= Exit Enterprise Value
  - Net Debt at Exit
= Exit Equity Value
```

**Returns Calculation:**
```
Exit Equity Value
  ÷ Initial Equity Investment
= Money-on-Money Multiple (MoM)

IRR = ((Exit Value / Entry Value)^(1/Years)) - 1
```

**Sensitivity Tables:**
- Exit Multiple vs Hold Period → IRR
- Exit Multiple vs Entry Multiple → IRR
- EBITDA Growth vs Exit Multiple → MoM

### Sheet 6: Debt Covenants

**Leverage Covenants:**
```
Total Debt / EBITDA (typically ≤ [threshold])
```