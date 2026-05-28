---
name: data-analysis
description: Data analysis and reporting patterns for LogiAccounting Pro. Use when generating reports, analyzing trends, or creating visualizations.
tools:
  - read
  - write
  - bash
metadata:
  version: "1.0"
  category: analytics
  libraries: pandas, chart.js
---

# Data Analysis Skill

This skill provides patterns for analyzing and reporting on LogiAccounting Pro data.

## Quick API Queries

```bash
# Get auth token first
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@logiaccounting.demo","password":"Demo2024!Admin"}' \
  | jq -r '.token')

# Dashboard metrics
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/reports/dashboard | jq

# Cash flow (12 months)
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5000/api/v1/reports/cash-flow?months=12" | jq

# Expenses by category
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/reports/expenses-by-category | jq

# Project profitability
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/reports/project-profitability | jq

# Inventory summary
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/reports/inventory-summary | jq

# Payment summary
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/reports/payment-summary | jq
```

## Key Metrics

### Financial KPIs

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Gross Margin | (Revenue - COGS) / Revenue | >40% healthy |
| Net Margin | Net Profit / Revenue | >10% good |
| Current Ratio | Current Assets / Current Liabilities | >1.5 healthy |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | >1 good |

### Operational KPIs

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Inventory Turnover | COGS / Avg Inventory | Higher = better |
| Days Payable Outstanding | (AP / COGS) × 365 | Lower = faster payment |
| Days Receivable Outstanding | (AR / Revenue) × 365 | Lower = faster collection |

## Chart.js Data Formatting

### Bar Chart (Cash Flow)

```javascript
const cashFlowData = {
  labels: data.map(d => d.month), // ['Jan', 'Feb', ...]
  datasets: [
    {
      label: 'Income',
      data: data.map(d => d.income),
      backgroundColor: '#10b981',
    },
    {
      label: 'Expenses',
      data: data.map(d => d.expenses),
      backgroundColor: '#ef4444',
    }
  ]
};
```

### Doughnut Chart (Category Breakdown)

```javascript
const expenseData = {
  labels: data.map(d => d.category),
  datasets: [{
    data: data.map(d => d.amount),
    backgroundColor: [
      '#667eea', '#10b981', '#f59e0b', 
      '#ef4444', '#8b5cf6', '#06b6d4'
    ]
  }]
};
```

### Line Chart (Trend)

```javascript
const trendData = {
  labels: data.map(d => d.month),
  datasets: [{
    label: 'Net Profit',
    data: data.map(d => d.income - d.expenses),
    borderColor: '#667eea',
    fill: true,
    backgroundColor: 'rgba(102, 126, 234, 0.1)',
    tension: 0.4
  }]
};
```

## Export Patterns

### CSV Export

```javascript
const exportToCSV = (data, filename) => {
  const headers = Object.keys(data[0]).join(',');
  const rows = data.map(row => Object.values(row).join(','));
  const csv = [headers, ...rows].join('\n');
  
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}.csv`;
  a.click();
};
```

### JSON Export

```javascript
const exportToJSON = (data, filename) => {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}.json`;
  a.click();
};
```

## Python Analysis (Optional)

```python
import pandas as pd
import json

# Load data from API
with open('cash_flow.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Calculate metrics
df['profit'] = df['income'] - df['expenses']
df['margin'] = (df['profit'] / df['income'] * 100).round(2)

# Summary statistics
print(df.describe())

# Monthly averages
print(f"Avg Monthly Income: ${df['income'].mean():,.2f}")
print(f"Avg Monthly Expenses: ${df['expenses'].mean():,.2f}")
print(f"Avg Profit Margin: {df['margin'].mean():.1f}%")
```
