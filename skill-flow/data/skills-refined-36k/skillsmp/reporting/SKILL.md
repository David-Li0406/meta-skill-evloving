---
name: reporting
description: Financial report generation including balance sheet, income statement, and cash flow. Use this skill when working with financial reports, multi-currency consolidation, or report calculations.
---

# Financial Reporting

> **Core Definition**: Financial report generation logic, report types, and calculation rules.

## Report Types

### Balance Sheet
Shows assets, liabilities, and equity at a point in time.
- **Validation**: `Total Assets = Total Liabilities + Total Equity`

### Income Statement (P&L)
Shows income and expenses over a period.
- **Calculation**: `Net Income = Total Income - Total Expenses`

### Cash Flow Statement
Shows cash movements by category:
- Operating Activities
- Investing Activities
- Financing Activities

## Multi-Currency Consolidation

- **Base Currency**: User configurable (default: SGD)
- **Balance Sheet**: Use period-end FX rate
- **Income Statement**: Use average FX rate
- Record unrealized FX gains/losses separately

```python
def consolidate_amount(amount: Decimal, currency: str, target: str, date: date) -> Decimal:
    if currency == target:
        return amount
    rate = get_fx_rate(currency, target, date)
    return (amount * rate).quantize(Decimal("0.01"))
```

## Design Constraints

### Recommended Patterns
- Report generation is read-only, never modifies ledger
- Always validate accounting equation before rendering
- Cache report results with date-based invalidation
- Pre-fetch all FX rates in bulk to avoid N+1 queries
- Cap trend data points at 366 to prevent memory issues

### Prohibited Patterns
- **NEVER** hardcode account codes in report logic
- **NEVER** generate reports without FX rate data

## Source Files

- **Logic**: `apps/backend/src/services/reporting.py`
- **Templates**: `apps/frontend/src/app/reports/`
- **Charts**: `apps/frontend/src/components/charts/`
