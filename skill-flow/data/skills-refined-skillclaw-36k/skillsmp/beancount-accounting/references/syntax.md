# Beancount Syntax Reference

Complete reference for beancount directives and syntax.

## File Format

- Plain text files with `.beancount` extension
- UTF-8 encoding recommended
- Lines starting with `;` are comments
- Directives follow pattern: `YYYY-MM-DD <directive-type> ...`
- Order of directives does not matter (sorted chronologically after parsing)

## Currencies and Commodities

All uppercase, 1-24 characters:
```
USD, EUR, GBP          ; Fiat currencies
AAPL, MSFT, VTI        ; Stocks/ETFs
VACHR, SICKHR          ; Custom units (vacation hours, etc.)
```

## Amounts

Basic amount:
```
100.00 USD
-50.25 EUR
10 AAPL
```

Arithmetic expressions:
```
((40.00/3) + 5) USD
(100 * 1.08) USD
```

## Account Names

Format: `Type:Component:Component:...`

Rules:
- Must start with one of five root types
- Each component starts with capital letter or number
- Components separated by colons
- No spaces (use dashes instead)
- Can contain letters, numbers, dashes

Valid examples:
```
Assets:US:BofA:Checking
Liabilities:Card:Chase-Freedom
Expenses:Food:Restaurants:Takeout
Income:2026:Bonus
Equity:Opening-Balances
```

## Directives

### open

Declare an account exists starting on a date.

Syntax:
```
YYYY-MM-DD open Account [Currency[,Currency...]] ["booking-method"]
```

Examples:
```beancount
; Basic open
2026-01-01 open Assets:Checking:Main

; With currency constraint (only USD allowed)
2026-01-01 open Assets:Savings:Ally USD

; Multiple currencies allowed
2026-01-01 open Assets:Investments:Fidelity USD,FXAIX,VTI

; With booking method for lot tracking
2026-01-01 open Assets:Investments:Brokerage "FIFO"
```

Booking methods:
- `STRICT` - Exact lot matching required (default)
- `FIFO` - First-in-first-out
- `LIFO` - Last-in-first-out
- `NONE` - No lot tracking

Metadata on open:
```beancount
2026-01-01 open Liabilities:Loan:Mortgage
  rate: "7.353%"
  lender: "Rocket Mortgage"
  account-number: "12345"
```

### close

Close an account. No transactions allowed after this date.

Syntax:
```
YYYY-MM-DD close Account
```

Example:
```beancount
2028-12-31 close Assets:Checking:OldBank
```

### commodity

Declare commodity metadata. Date is when commodity "existed."

Syntax:
```
YYYY-MM-DD commodity Currency
  [metadata]
```

Example:
```beancount
1867-07-01 commodity CAD
  name: "Canadian Dollar"

2010-01-01 commodity BTC
  name: "Bitcoin"
  asset-class: "cryptocurrency"
```

### balance

Assert that an account has exactly this balance at start of day.

Syntax:
```
YYYY-MM-DD balance Account Amount Currency
```

Examples:
```beancount
; Single currency balance check
2026-01-31 balance Assets:Checking:Main 4583.84 USD

; For multi-currency accounts, use one per currency
2026-01-31 balance Assets:Investments:Fidelity 1000.00 USD
2026-01-31 balance Assets:Investments:Fidelity 50 VTI
```

If balance doesn't match, beancount reports an error with the difference.

### pad

Insert automatic transaction to make balance assertion pass.

Syntax:
```
YYYY-MM-DD pad Account PadFromAccount
```

Example:
```beancount
; Pad will auto-generate entry to make balance work
2026-01-01 pad Assets:Checking:Main Equity:Opening-Balances
2026-01-02 balance Assets:Checking:Main 4583.84 USD

; Beancount generates:
; 2026-01-01 P "Pad"
;   Assets:Checking:Main     4583.84 USD
;   Equity:Opening-Balances -4583.84 USD
```

Rules:
- Only pad Assets and Liabilities (not Income/Expenses)
- Pad source is typically Equity:Opening-Balances
- Pad entry appears between pad directive and balance assertion

### note

Attach a dated note to an account.

Syntax:
```
YYYY-MM-DD note Account "Note text"
```

Example:
```beancount
2026-01-15 note Assets:Checking:Main "Called bank about discrepancy"
2026-02-01 note Liabilities:Card:Chase "Reported card stolen, new card ordered"
```

### document

Link external file to an account.

Syntax:
```
YYYY-MM-DD document Account "/path/to/file"
```

Example:
```beancount
2026-01-31 document Assets:Checking:Main "documents/2026/bank-statement-jan.pdf"
2026-02-15 document Expenses:Taxes "documents/w2-2025.pdf"
```

### price

Record market price of a commodity.

Syntax:
```
YYYY-MM-DD price Commodity Price Currency
```

Examples:
```beancount
2026-01-03 price VTI 250.00 USD
2026-01-03 price AAPL 185.50 USD
2026-01-03 price EUR 1.08 USD
```

Used for:
- Mark-to-market valuations
- Currency conversion reporting
- Investment performance tracking

### event

Track variable values over time.

Syntax:
```
YYYY-MM-DD event "event-type" "value"
```

Examples:
```beancount
2026-01-01 event "employer" "Acme Corp"
2026-01-15 event "location" "Austin, TX"
2026-03-01 event "employer" "New Company Inc"
```

Useful for:
- Tracking employer changes
- Location history
- Tax residency
- Any time-varying metadata

### query

Embed named BQL query in the file.

Syntax:
```
YYYY-MM-DD query "query-name" "BQL query string"
```

Example:
```beancount
2026-01-01 query "monthly-expenses" "
  SELECT MONTH(date), account, sum(position)
  WHERE account ~ 'Expenses' AND year = 2026
  GROUP BY 1, 2
  ORDER BY 1, 2
"
```

### custom

Generic directive for plugins and extensions.

Syntax:
```
YYYY-MM-DD custom "directive-name" [values...]
```

Example:
```beancount
2026-01-01 custom "budget" Expenses:Food 500.00 USD
2026-01-01 custom "fava-option" "fiscal-year-end" "06-30"
```

### option

Configure beancount behavior.

Syntax:
```
option "option-name" "value"
```

Common options:
```beancount
option "title" "My Finances"
option "operating_currency" "USD"
option "documents" "documents/"
option "name_assets" "Assets"           ; Customize root name
option "name_liabilities" "Liabilities"
option "name_equity" "Equity"
option "name_income" "Income"
option "name_expenses" "Expenses"
```

### plugin

Load a beancount plugin.

Syntax:
```
plugin "module.path" ["config"]
```

Example:
```beancount
plugin "beancount.plugins.auto_accounts"
plugin "beancount.plugins.implicit_prices"
plugin "beancount_share.share" "{"share_tag": "shared"}"
```

### include

Include another beancount file.

Syntax:
```
include "path/to/file.beancount"
```

Example:
```beancount
include "accounts.beancount"
include "2026/january.beancount"
include "2026/february.beancount"
```

Paths are relative to the including file.

## Transaction Syntax

### Basic Structure

```
YYYY-MM-DD [txn|*|!] ["Payee"] "Narration" [#tag...] [^link...]
  [metadata: value]
  Account1    Amount [Currency] [{Cost}] [@ Price] [; comment]
  Account2    [Amount] [Currency]
  ...
```

### Flags

| Flag | Meaning |
|------|---------|
| `*` or `txn` | Completed/cleared |
| `!` | Incomplete/pending review |

### Payee and Narration

```beancount
; Both payee and narration
2026-01-03 * "Starbucks" "Morning coffee"

; Narration only (no payee)
2026-01-03 * "Morning coffee"

; Empty narration (just payee)
2026-01-03 * "Starbucks" ""
```

### Posting Syntax

Basic posting:
```
  Account    Amount Currency
```

With inline comment:
```
  Account    Amount Currency  ; comment here
```

Posting-level metadata:
```
  Account    Amount Currency
    category: "value"
    receipt: "path/to/receipt.jpg"
```

### Costs (for lots/positions)

Per-unit cost:
```
  Assets:Investments    10 VTI {250.00 USD}
```

Total cost:
```
  Assets:Investments    10 VTI {{2500.00 USD}}
```

With acquisition date:
```
  Assets:Investments    10 VTI {250.00 USD, 2026-01-15}
```

With label:
```
  Assets:Investments    10 VTI {250.00 USD, "lot1"}
```

Full cost spec:
```
  Assets:Investments    10 VTI {250.00 USD, 2026-01-15, "lot1"}
```

### Prices (for currency conversion)

Per-unit price:
```
  Assets:EUR    100 EUR @ 1.08 USD
```

Total price:
```
  Assets:EUR    100 EUR @@ 108 USD
```

### Selling with Cost Basis

```beancount
2026-06-15 * "Fidelity" "Sell shares"
  Assets:Investments:Fidelity   -10 VTI {250.00 USD} @ 275.00 USD
  Assets:Investments:Cash       2750.00 USD
  Income:Investments:Gains       ; Auto-calculated: -250.00 USD
```

### Tags and Links

Tags (categorization):
```beancount
2026-01-15 * "Hotel" "Conference" #business #travel #conference-2026
  Expenses:Travel    500.00 USD
  Liabilities:Card:Amex
```

Links (connect related transactions):
```beancount
2026-01-15 * "Send invoice" ^invoice-2026-001
  Income:Consulting    -5000.00 USD
  Assets:Receivables    5000.00 USD

2026-02-01 * "Payment received" ^invoice-2026-001
  Assets:Checking        5000.00 USD
  Assets:Receivables    -5000.00 USD
```

### Block Tags

Apply tags to multiple transactions:
```beancount
pushtag #vacation-2026

2026-03-15 * "Flight" "To Hawaii"
  Expenses:Travel:Flights    500.00 USD
  Liabilities:Card:Chase

2026-03-20 * "Hotel" "Beach Resort"
  Expenses:Travel:Lodging    1500.00 USD
  Liabilities:Card:Chase

poptag #vacation-2026
```

## Metadata

### Transaction-Level

```beancount
2026-01-03 * "Amazon" "Office supplies"
  order-id: "123-456-789"
  tracking: "1Z999..."
  Expenses:Office    100.00 USD
  Liabilities:Card:Chase
```

### Posting-Level

```beancount
2026-01-03 * "Store" "Mixed purchase"
  Expenses:Food:Groceries    50.00 USD
    aisle: "produce"
  Expenses:Household    25.00 USD
    aisle: "cleaning"
  Liabilities:Card:Chase
```

### Metadata Types

- Strings: `key: "value"`
- Numbers: `amount: 123.45`
- Dates: `purchased: 2026-01-15`
- Accounts: `source: Assets:Checking`
- Tags: `category: #food`
- Currencies: `currency: USD`
- Booleans: Not directly supported, use strings

## Comments

```beancount
; Full line comment

2026-01-03 * "Store" "Purchase"  ; Inline comment
  Expenses:Food    50.00 USD     ; Posting comment
  Assets:Checking

;; Section header comment
;; ======================

* Org-mode style headers work too
** Subsection
```
