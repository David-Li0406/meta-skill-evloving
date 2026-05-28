# Beancount Query Language (BQL) Reference

BQL is a SQL-like query language for analyzing beancount data.

## Running Queries

```bash
# Interactive mode
bean-query finances/2026.beancount

# Single query
bean-query finances/2026.beancount "SELECT account, sum(position) WHERE account ~ 'Expenses' GROUP BY 1"

# Query from file
bean-query finances/2026.beancount -f query.bql
```

## Query Structure

```sql
SELECT <columns>
FROM <entry-filter>
WHERE <posting-filter>
GROUP BY <columns>
ORDER BY <columns> [ASC|DESC]
LIMIT <n>
```

- **FROM** filters complete transactions (preserves double-entry)
- **WHERE** filters individual postings
- Both clauses are optional

## SELECT Columns

### Posting-Level Columns

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Transaction date |
| `year` | Integer | Year of transaction |
| `month` | Integer | Month (1-12) |
| `day` | Integer | Day of month |
| `flag` | String | Transaction flag (* or !) |
| `payee` | String | Payee name |
| `narration` | String | Description |
| `account` | Account | Posting account |
| `position` | Position | Amount with lot info |
| `balance` | Inventory | Running balance |
| `tags` | Set | Transaction tags |
| `links` | Set | Transaction links |

### Derived Columns

| Column | Description |
|--------|-------------|
| `units(position)` | Just the units and currency |
| `cost(position)` | Cost basis amount |
| `weight(position)` | Balancing weight |
| `value(position)` | Market value |

### Wildcard

```sql
SELECT *
```

Selects default set of useful columns.

## FROM Clause

Filter complete transactions before extracting postings.

### Basic Filters

```sql
-- By year
FROM year = 2026

-- By date range
FROM date >= 2026-01-01 AND date < 2026-07-01

-- By account presence
FROM has_account("Assets:Checking")

-- By flag
FROM flag = "*"

-- By tag
FROM "vacation" IN tags
```

### Statement Operators

**OPEN ON date** - Summarize entries before date as opening balances:
```sql
SELECT account, sum(position)
FROM OPEN ON 2026-01-01
WHERE account ~ "Assets|Liabilities"
GROUP BY 1
```

**CLOSE ON date** - Truncate entries after date:
```sql
SELECT account, sum(position)
FROM CLOSE ON 2026-12-31
WHERE account ~ "Expenses"
GROUP BY 1
```

**CLEAR** - Transfer income/expenses to equity:
```sql
-- Balance sheet with closed period
SELECT account, sum(position)
FROM CLOSE ON 2026-12-31 CLEAR
WHERE NOT account ~ "Income|Expenses"
GROUP BY 1
```

**Combined for financial statements:**
```sql
-- Full year 2026
FROM OPEN ON 2026-01-01 CLOSE ON 2027-01-01
```

## WHERE Clause

Filter individual postings.

### Comparison Operators

| Operator | Description |
|----------|-------------|
| `=` | Equality |
| `!=` | Inequality |
| `<`, `<=`, `>`, `>=` | Comparison |
| `~` | Regex match |
| `IN` | Set membership |

### Account Patterns

```sql
-- Contains string
WHERE account ~ "Expenses"

-- Starts with
WHERE account ~ "^Assets:Checking"

-- Multiple patterns (OR)
WHERE account ~ "Food|Coffee"

-- Exact match
WHERE account = "Assets:Checking:Main"
```

### Date Filters

```sql
WHERE date >= 2026-01-01
WHERE date < 2026-07-01
WHERE year = 2026
WHERE month = 1
WHERE YEAR(date) = 2026 AND MONTH(date) >= 6
```

### Logical Operators

```sql
-- AND
WHERE account ~ "Expenses" AND year = 2026

-- OR
WHERE account ~ "Food" OR account ~ "Coffee"

-- NOT
WHERE NOT account ~ "Taxes"

-- Parentheses
WHERE (account ~ "Food" OR account ~ "Auto") AND year = 2026
```

### Tag and Link Filters

```sql
WHERE "vacation" IN tags
WHERE "invoice-001" IN links
WHERE NOT "reimbursed" IN tags
```

### Payee and Narration

```sql
WHERE payee ~ "Amazon"
WHERE narration ~ "grocery"
WHERE payee = "Starbucks"
```

## Aggregate Functions

| Function | Description |
|----------|-------------|
| `SUM(x)` | Sum of values |
| `COUNT(x)` | Count of values |
| `FIRST(x)` | First value in group |
| `LAST(x)` | Last value in group |
| `MIN(x)` | Minimum value |
| `MAX(x)` | Maximum value |

### With Positions

```sql
SELECT account, SUM(position)
WHERE account ~ "Expenses"
GROUP BY account

SELECT account, COST(SUM(position))
WHERE account ~ "Investments"
GROUP BY account
```

## Position Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `UNITS(p)` | Amount | Raw units and currency |
| `COST(p)` | Amount | Cost basis |
| `WEIGHT(p)` | Amount | Balancing weight |
| `VALUE(p)` | Amount | Market value at latest price |

```sql
-- Holdings at cost
SELECT account, UNITS(SUM(position)), COST(SUM(position))
WHERE account ~ "Assets:Investments"
GROUP BY 1

-- With market value
SELECT account, UNITS(SUM(position)), VALUE(SUM(position))
WHERE account ~ "Assets:Investments"
GROUP BY 1
```

## Date Functions

| Function | Returns | Example |
|----------|---------|---------|
| `YEAR(date)` | Integer | `YEAR(date) = 2026` |
| `MONTH(date)` | Integer | `MONTH(date) = 12` |
| `DAY(date)` | Integer | `DAY(date) = 25` |
| `QUARTER(date)` | Integer | `QUARTER(date) = 4` |
| `WEEKDAY(date)` | Integer | Mon=0, Sun=6 |

```sql
-- Monthly breakdown
SELECT YEAR(date), MONTH(date), SUM(position)
WHERE account ~ "Expenses:Food"
GROUP BY 1, 2
ORDER BY 1, 2

-- Quarterly summary
SELECT YEAR(date), QUARTER(date), SUM(position)
WHERE account ~ "Income"
GROUP BY 1, 2
```

## Account Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `ROOT(account, n)` | Account | First n components |
| `LEAF(account)` | String | Last component |
| `PARENT(account)` | Account | All but last component |

```sql
-- Group by top-level category
SELECT ROOT(account, 2), SUM(position)
WHERE account ~ "Expenses"
GROUP BY 1

-- Get leaf account names
SELECT LEAF(account), SUM(position)
WHERE account ~ "Expenses:Food"
GROUP BY 1
```

## GROUP BY

Required when using aggregate functions:

```sql
-- By column name
SELECT account, SUM(position)
WHERE account ~ "Expenses"
GROUP BY account

-- By position (1-indexed)
SELECT account, SUM(position)
WHERE account ~ "Expenses"
GROUP BY 1

-- Multiple columns
SELECT YEAR(date), account, SUM(position)
WHERE account ~ "Expenses"
GROUP BY 1, 2
```

## ORDER BY

```sql
-- Ascending (default)
ORDER BY date

-- Descending
ORDER BY date DESC

-- Multiple columns
ORDER BY account, date DESC

-- By position
ORDER BY 1, 2 DESC
```

## DISTINCT

Remove duplicate rows:
```sql
SELECT DISTINCT account
WHERE account ~ "Expenses"
```

## LIMIT

Restrict output:
```sql
SELECT date, narration, position
WHERE account ~ "Expenses"
ORDER BY date DESC
LIMIT 10
```

## Common Query Patterns

### Account Register (Journal)

```sql
SELECT date, narration, payee, position, balance
WHERE account = "Assets:Checking:Centennial:Joint"
ORDER BY date
```

### Monthly Expense Summary

```sql
SELECT MONTH(date) AS month, SUM(position) AS total
WHERE account ~ "Expenses" AND year = 2026
GROUP BY 1
ORDER BY 1
```

### Expenses by Category

```sql
SELECT account, SUM(position) AS total
WHERE account ~ "Expenses" AND year = 2026
GROUP BY 1
ORDER BY 2 DESC
```

### Top-Level Category Breakdown

```sql
SELECT ROOT(account, 2) AS category, SUM(position)
WHERE account ~ "Expenses" AND year = 2026
GROUP BY 1
ORDER BY 2 DESC
```

### Payee Analysis

```sql
SELECT payee, account, COST(SUM(position)), LAST(date)
WHERE account ~ "Expenses"
GROUP BY 1, 2
ORDER BY 3 DESC
```

### Income vs Expenses

```sql
SELECT
  ROOT(account, 1) AS type,
  SUM(position) AS total
WHERE account ~ "Income|Expenses" AND year = 2026
GROUP BY 1
```

### Balance Sheet

```sql
SELECT account, SUM(position)
FROM CLOSE ON 2026-12-31 CLEAR
WHERE account ~ "Assets|Liabilities|Equity"
GROUP BY 1
ORDER BY 1
```

### Income Statement

```sql
SELECT account, SUM(position)
FROM OPEN ON 2026-01-01 CLOSE ON 2027-01-01
WHERE account ~ "Income|Expenses"
GROUP BY 1
ORDER BY 1
```

### Net Worth

```sql
SELECT SUM(position)
FROM CLOSE
WHERE account ~ "Assets|Liabilities"
```

### Holdings Report

```sql
SELECT account, UNITS(SUM(position)), COST(SUM(position))
WHERE account ~ "Assets:Investments"
GROUP BY 1
ORDER BY 1
```

### Tag-Based Queries

```sql
-- All vacation expenses
SELECT date, payee, narration, account, position
WHERE "vacation" IN tags
ORDER BY date

-- Total by tagged trip
SELECT account, SUM(position)
WHERE "trip-hawaii-2026" IN tags
GROUP BY 1
```

### Transactions to Review

```sql
SELECT date, payee, narration, account, position
WHERE flag = "!"
ORDER BY date
```

### Recent Transactions

```sql
SELECT date, payee, narration, account, position
ORDER BY date DESC
LIMIT 20
```

### Credit Card Spending

```sql
SELECT MONTH(date), SUM(position)
WHERE account ~ "Liabilities:Card" AND year = 2026
GROUP BY 1
ORDER BY 1
```

### Specific Payee History

```sql
SELECT date, account, position, balance
WHERE payee ~ "Starbucks"
ORDER BY date
```

## High-Level Shortcuts

BQL provides shortcuts for common reports:

### JOURNAL

```sql
JOURNAL "Assets:Checking:Main"
JOURNAL "Assets:Checking:Main" AT COST
```

### BALANCES

```sql
BALANCES
BALANCES AT COST
BALANCES FROM CLOSE ON 2026-12-31
```

### PRINT

Output in beancount format:
```sql
PRINT
PRINT FROM flag = "!"
PRINT FROM "trip" IN tags
```

## NULL Handling

BQL uses simplified NULL logic:
- `NULL = NULL` returns `TRUE` (unlike SQL)
- Useful for filtering unset metadata

## Tips

1. Use `EXPLAIN SELECT ...` to see query execution plan
2. Interactive mode: Type `help` for available commands
3. Use `help targets` to see all available columns
4. Regex patterns use Python regex syntax
5. Dates must be in `YYYY-MM-DD` format
6. Account names are case-sensitive
