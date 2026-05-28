# Beancount Examples and Patterns

Common transaction patterns and workflows for personal finance tracking.

## Account Setup Patterns

### Personal Finance Structure

```beancount
; Options
option "title" "Personal Finances"
option "operating_currency" "USD"

; Assets - Checking accounts
2026-01-01 open Assets:Checking:Main USD
2026-01-01 open Assets:Checking:Bills USD

; Assets - Savings
2026-01-01 open Assets:Savings:Emergency USD
2026-01-01 open Assets:Savings:Goals USD

; Assets - Investments
2026-01-01 open Assets:Investments:Brokerage USD,VTI,VXUS,BND
2026-01-01 open Assets:Investments:Retirement:401k USD,VFIAX
2026-01-01 open Assets:Investments:Retirement:IRA USD,VTI

; Liabilities - Credit Cards
2026-01-01 open Liabilities:Card:Chase:Sapphire USD
2026-01-01 open Liabilities:Card:Amex:Gold USD

; Liabilities - Loans
2026-01-01 open Liabilities:Loan:Mortgage USD
  rate: "6.5%"
  lender: "Bank"
2026-01-01 open Liabilities:Loan:Auto USD

; Income
2026-01-01 open Income:Salary
2026-01-01 open Income:Bonus
2026-01-01 open Income:Interest
2026-01-01 open Income:Dividends

; Expenses - Hierarchical categories
2026-01-01 open Expenses:Housing:Mortgage
2026-01-01 open Expenses:Housing:Insurance
2026-01-01 open Expenses:Housing:Utilities:Electric
2026-01-01 open Expenses:Housing:Utilities:Gas
2026-01-01 open Expenses:Housing:Utilities:Water
2026-01-01 open Expenses:Housing:Maintenance

2026-01-01 open Expenses:Food:Groceries
2026-01-01 open Expenses:Food:Restaurants
2026-01-01 open Expenses:Food:Coffee

2026-01-01 open Expenses:Transportation:Gas
2026-01-01 open Expenses:Transportation:Maintenance
2026-01-01 open Expenses:Transportation:Insurance

2026-01-01 open Expenses:Healthcare:Insurance
2026-01-01 open Expenses:Healthcare:Doctor
2026-01-01 open Expenses:Healthcare:Pharmacy

2026-01-01 open Expenses:Subscriptions
2026-01-01 open Expenses:Shopping
2026-01-01 open Expenses:Entertainment

; Equity
2026-01-01 open Equity:Opening-Balances
```

## Opening Balances

### Using Pad (Recommended)

```beancount
2026-01-01 pad Assets:Checking:Main Equity:Opening-Balances
2026-01-02 balance Assets:Checking:Main 5000.00 USD

2026-01-01 pad Assets:Savings:Emergency Equity:Opening-Balances
2026-01-02 balance Assets:Savings:Emergency 10000.00 USD

2026-01-01 pad Liabilities:Card:Chase:Sapphire Equity:Opening-Balances
2026-01-02 balance Liabilities:Card:Chase:Sapphire -1500.00 USD
```

### Explicit Opening Transaction

```beancount
2026-01-01 * "Opening Balances"
  Assets:Checking:Main           5000.00 USD
  Assets:Savings:Emergency      10000.00 USD
  Liabilities:Card:Chase:Sapphire -1500.00 USD
  Liabilities:Loan:Mortgage   -250000.00 USD
  Equity:Opening-Balances
```

## Income Patterns

### Simple Paycheck

```beancount
2026-01-15 * "Employer" "Bi-weekly salary"
  Assets:Checking:Main    3500.00 USD
  Income:Salary          -3500.00 USD
```

### Paycheck with Deductions

```beancount
2026-01-15 * "Employer" "Bi-weekly salary"
  Assets:Checking:Main              2800.00 USD
  Expenses:Taxes:Federal             500.00 USD
  Expenses:Taxes:State               150.00 USD
  Expenses:Taxes:FICA                250.00 USD
  Expenses:Healthcare:Insurance      100.00 USD
  Assets:Investments:Retirement:401k  200.00 USD
  Income:Salary                    -4000.00 USD
```

### Bonus

```beancount
2026-03-15 * "Employer" "Q1 Performance bonus"
  Assets:Checking:Main    4000.00 USD
  Expenses:Taxes:Federal  1200.00 USD
  Expenses:Taxes:State     300.00 USD
  Income:Bonus           -5500.00 USD
```

### Interest Income

```beancount
2026-01-31 * "Ally Bank" "Monthly interest"
  Assets:Savings:Emergency    12.50 USD
  Income:Interest            -12.50 USD
```

### Dividend Income

```beancount
2026-03-15 * "Vanguard" "VTI quarterly dividend"
  Assets:Investments:Brokerage    150.00 USD
  Income:Dividends               -150.00 USD
```

## Expense Patterns

### Simple Purchase

```beancount
2026-01-05 * "Grocery Store" "Weekly groceries"
  Expenses:Food:Groceries    125.00 USD
  Liabilities:Card:Chase:Sapphire
```

### Split Transaction

```beancount
2026-01-10 * "Target" "Mixed purchase"
  Expenses:Food:Groceries     50.00 USD
  Expenses:Shopping           75.00 USD
  Expenses:Healthcare:Pharmacy 25.00 USD
  Liabilities:Card:Chase:Sapphire
```

### Subscription

```beancount
2026-01-01 * "Netflix" "Monthly subscription"
  Expenses:Subscriptions    15.99 USD
  Liabilities:Card:Chase:Sapphire

2026-01-01 * "Spotify" "Monthly subscription"
  Expenses:Subscriptions    10.99 USD
  Liabilities:Card:Chase:Sapphire
```

### Utility Bill

```beancount
2026-01-15 * "Electric Company" "January electric bill"
  Expenses:Housing:Utilities:Electric    125.00 USD
  Assets:Checking:Bills
```

## Housing Patterns

### Mortgage Payment

```beancount
2026-01-01 * "Bank" "January mortgage"
  Liabilities:Loan:Mortgage      800.00 USD  ; Principal
  Expenses:Housing:Mortgage      950.00 USD  ; Interest
  Expenses:Housing:Insurance     100.00 USD  ; Escrow - insurance
  Expenses:Taxes:Property        150.00 USD  ; Escrow - taxes
  Assets:Checking:Main         -2000.00 USD
```

### Rent Payment

```beancount
2026-01-01 * "Landlord" "January rent"
  Expenses:Housing:Rent    1800.00 USD
  Assets:Checking:Main
```

### Home Maintenance

```beancount
2026-01-20 * "Home Depot" "Plumbing repair supplies"
  Expenses:Housing:Maintenance    75.00 USD
  Liabilities:Card:Chase:Sapphire
```

## Credit Card Patterns

### Credit Card Payment

```beancount
2026-01-25 * "Chase" "Credit card payment"
  Liabilities:Card:Chase:Sapphire    1500.00 USD
  Assets:Checking:Main              -1500.00 USD
```

### Statement Balance Check

```beancount
; After recording payment, verify balance
2026-01-26 balance Liabilities:Card:Chase:Sapphire 0.00 USD
```

## Transfer Patterns

### Between Accounts

```beancount
2026-01-05 * "Transfer to savings"
  Assets:Savings:Emergency    500.00 USD
  Assets:Checking:Main       -500.00 USD
```

### To Investment Account

```beancount
2026-01-10 * "Transfer to brokerage"
  Assets:Investments:Brokerage    1000.00 USD
  Assets:Checking:Main           -1000.00 USD
```

## Investment Patterns

### Buy Shares

```beancount
2026-01-15 * "Vanguard" "Buy VTI"
  Assets:Investments:Brokerage    10 VTI {250.00 USD}
  Assets:Investments:Brokerage    -2500.00 USD
  Expenses:Fees:Investment        0.00 USD  ; Commission-free
```

### Sell Shares

```beancount
2026-06-15 * "Vanguard" "Sell VTI"
  Assets:Investments:Brokerage    -5 VTI {250.00 USD} @ 275.00 USD
  Assets:Investments:Brokerage    1375.00 USD
  Income:Investments:Gains        ; Auto-calculated: -125.00 USD
```

### Dividend Reinvestment

```beancount
2026-03-15 * "Vanguard" "VTI dividend reinvested"
  Assets:Investments:Brokerage    0.5 VTI {260.00 USD}
  Income:Dividends               -130.00 USD
```

### 401k Contribution

```beancount
2026-01-15 * "Employer 401k" "Bi-weekly contribution"
  Assets:Investments:Retirement:401k    1.5 VFIAX {200.00 USD}
  Income:Salary                        -300.00 USD  ; Pre-tax
```

## Reimbursement Patterns

### Work Expense Reimbursement

```beancount
; Initial expense
2026-01-10 * "Hotel" "Conference hotel" #work-travel
  Expenses:Travel:Lodging    500.00 USD
  Liabilities:Card:Chase:Sapphire

; Reimbursement received
2026-01-25 * "Employer" "Travel reimbursement" #work-travel
  Assets:Checking:Main    500.00 USD
  Income:Reimbursements  -500.00 USD
```

### Using Links for Tracking

```beancount
2026-01-10 * "Hotel" "Conference hotel" ^conference-jan-2026
  Expenses:Travel:Lodging    500.00 USD
  Liabilities:Card:Chase:Sapphire

2026-01-25 * "Employer" "Travel reimbursement" ^conference-jan-2026
  Assets:Checking:Main    500.00 USD
  Income:Reimbursements  -500.00 USD
```

## Loan Patterns

### Car Loan Payment

```beancount
2026-01-15 * "Auto Lender" "Monthly car payment"
  Liabilities:Loan:Auto               400.00 USD  ; Principal
  Expenses:Transportation:Interest     50.00 USD  ; Interest
  Assets:Checking:Main               -450.00 USD
```

### Student Loan Payment

```beancount
2026-01-05 * "Student Loan Servicer" "Monthly payment"
  Liabilities:Loan:Student    200.00 USD  ; Principal
  Expenses:Education:Interest  50.00 USD  ; Interest
  Assets:Checking:Main       -250.00 USD
```

## Travel Patterns

### Vacation Tracking with Tags

```beancount
pushtag #vacation-hawaii-2026

2026-02-01 * "United Airlines" "Flights to Hawaii"
  Expenses:Travel:Flights    800.00 USD
  Liabilities:Card:Chase:Sapphire

2026-02-05 * "Marriott" "Hotel 5 nights"
  Expenses:Travel:Lodging    1500.00 USD
  Liabilities:Card:Chase:Sapphire

2026-02-06 * "Restaurant" "Dinner"
  Expenses:Travel:Food    150.00 USD
  Liabilities:Card:Chase:Sapphire

poptag #vacation-hawaii-2026
```

### Business Trip

```beancount
2026-03-01 * "Delta" "Flight to conference" #business #conference-2026
  Expenses:Travel:Flights    400.00 USD
  Liabilities:Card:Amex:Gold

2026-03-03 * "Hilton" "Conference hotel" #business #conference-2026
  Expenses:Travel:Lodging    300.00 USD
  Liabilities:Card:Amex:Gold
```

## Cash Handling

### ATM Withdrawal

```beancount
2026-01-10 * "ATM" "Cash withdrawal"
  Assets:Cash    200.00 USD
  Assets:Checking:Main
```

### Cash Expense

```beancount
2026-01-12 * "Farmers Market" "Produce"
  Expenses:Food:Groceries    35.00 USD
  Assets:Cash
```

### Cash Reconciliation

```beancount
; Periodic balance assertion
2026-01-31 balance Assets:Cash 165.00 USD
```

## Multi-Currency

### Foreign Currency Transaction

```beancount
2026-01-15 * "European Hotel" "Hotel in Paris"
  Expenses:Travel:Lodging    200 EUR @ 1.08 USD
  Liabilities:Card:Chase:Sapphire  -216.00 USD
```

### Currency Exchange

```beancount
2026-01-10 * "Currency Exchange" "Buy euros for trip"
  Assets:Cash:EUR    500 EUR @ 1.10 USD
  Assets:Checking:Main  -550.00 USD
```

## File Organization

### Main File (2026.beancount)

```beancount
; -*- mode: beancount; coding: utf-8; -*-
option "title" "Personal Finances"
option "operating_currency" "USD"

; Account definitions
include "accounts.beancount"

; Monthly transactions
include "2026/01-january.beancount"
include "2026/02-february.beancount"
; ... etc

; Prices (optional, for investments)
include "prices.beancount"
```

### Accounts File (accounts.beancount)

```beancount
; All account open directives
2026-01-01 open Assets:Checking:Main USD
2026-01-01 open Assets:Savings:Emergency USD
; ... all accounts
```

### Monthly File (2026/01-january.beancount)

```beancount
; January 2026 Transactions

2026-01-01 * "Opening Balance"
  ; ...

2026-01-05 * "Grocery Store" "Weekly groceries"
  ; ...

; Month-end balance assertions
2026-01-31 balance Assets:Checking:Main 4500.00 USD
```

## Reconciliation Workflow

### Monthly Bank Reconciliation

```beancount
; 1. Download statement, note ending balance

; 2. Enter any missing transactions

; 3. Add balance assertion
2026-01-31 balance Assets:Checking:Main 4583.84 USD

; 4. Run bean-check to verify
; If error, difference shows amount to investigate
```

### Credit Card Reconciliation

```beancount
; Statement closing date
2026-01-25 balance Liabilities:Card:Chase:Sapphire -1234.56 USD

; After payment posts
2026-01-30 balance Liabilities:Card:Chase:Sapphire 0.00 USD
```

## Common Queries for These Patterns

### Monthly Spending by Category

```sql
SELECT MONTH(date), ROOT(account, 2), SUM(position)
WHERE account ~ "Expenses" AND year = 2026
GROUP BY 1, 2
ORDER BY 1, 2
```

### Credit Card Balance

```sql
SELECT account, SUM(position)
WHERE account ~ "Liabilities:Card"
GROUP BY 1
```

### Vacation Total

```sql
SELECT SUM(position)
WHERE "vacation-hawaii-2026" IN tags
```

### Investment Performance

```sql
SELECT account, UNITS(SUM(position)), COST(SUM(position)), VALUE(SUM(position))
WHERE account ~ "Assets:Investments"
GROUP BY 1
```

### Net Worth

```sql
SELECT SUM(position)
FROM CLOSE
WHERE account ~ "Assets|Liabilities"
```
