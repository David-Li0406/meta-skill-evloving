# Budget Buddy Domain Concept Examples

Detailed code explanations with analogies and ASCII diagrams for Budget Buddy's core features.

## Contents
- Transaction Classification Pipeline
- Fuzzy Matching (0.85 Threshold)
- Budget Allocation Flow
- Sinking Funds Mechanics
- Buddy AI Insight Generation

---

## Example 1: Transaction Classification Pipeline

**Analogy**: Like a sorting hat in Harry Potter - each transaction arrives and the system figures out which "house" (category) it belongs to based on its characteristics.

**ASCII Diagram**:

```
┌─────────────────┐
│ New Transaction │
│  "STARBUCKS"    │
└────────┬────────┘
         │
         ▼
┌────────────────────────┐
│ Step 1: Check History  │
│ "Have we seen this     │
│  merchant before?"     │
└────────┬───────────────┘
         │
    ┌────┴────┐
    │  Yes    │  No
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Reuse  │ │ Step 2: ML   │
│Category│ │ Predict      │
└────┬───┘ │ Category     │
     │     └──────┬───────┘
     │            │
     └────────────┘
                  ▼
         ┌────────────────┐
         │ Assigned:      │
         │ "Food & Dining"│
         └────────────────┘
```

**Step-by-Step Walkthrough**:

1. **Transaction arrives** from Plaid:
   ```python
   transaction = {
       'description': 'STARBUCKS COFFEE #1234',
       'merchant_name': 'Starbucks',
       'amount': -5.50
   }
   ```

2. **Check for existing classification**:
   ```python
   existing = db.query(Transaction).filter(
       Transaction.merchant_name == 'Starbucks',
       Transaction.bb_category.isnot(None)
   ).first()
   ```

3. **If found, reuse category**:
   ```python
   if existing:
       transaction['bb_category'] = existing.bb_category
       transaction['bb_category_manual'] = False
   ```

4. **If not, use ML**:
   ```python
   else:
       category = ml_classifier.predict(transaction['description'])
       transaction['bb_category'] = category
       transaction['bb_category_manual'] = False
   ```

**Gotcha**: Manual changes don't auto-update similar transactions. Use "smart batch update" for that!

---

## Example 2: Fuzzy Matching (0.85 Threshold)

**Analogy**: Finding fraternal twins (similar but not identical) in a crowd. 85% threshold means "at least 85% alike."

**ASCII Diagram**:

```
Reference Transaction:
┌────────────────────────┐
│ "CHECK #1234 - RENT"   │
└────────────────────────┘
           │
           ▼
    Compare with all:
┌─────────────────────────────────┐
│ "CHECK #1235 - RENT"  → 95% ✓  │  Match!
│ "CHECK #9999 - RENT"  → 94% ✓  │  Match!
│ "WIRE TRANSFER RENT"  → 60% ✗  │  Too different
│ "STARBUCKS COFFEE"    → 10% ✗  │  Totally different
└─────────────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ Return matches ≥ 85%   │
│ [Check #1235, #9999]   │
└────────────────────────┘
```

**Step-by-Step**:

1. **Get reference**:
   ```python
   ref_desc = "CHECK #1234 - MONTHLY RENT"
   ```

2. **Compare with candidates**:
   ```python
   from difflib import SequenceMatcher

   for candidate in unclassified_transactions:
       similarity = SequenceMatcher(
           None,
           ref_desc.lower(),
           candidate.description.lower()
       ).ratio()
   ```

3. **Similarity calculation**:
   ```
   "CHECK #1234 - MONTHLY RENT"
   "CHECK #1235 - MONTHLY RENT"
    ^^^^^^^^^^^^^^^^^^^^^ ^^^^  (22/24 chars match)

   similarity = 2 * 22 / (24 + 24) = 0.917 (91.7%)
   ```

4. **Filter by threshold**:
   ```python
   if similarity >= 0.85:
       matches.append(candidate)
   ```

**Gotcha**: Case-insensitive! "CHECK #80" matches "check #81".

---

## Example 3: Budget Allocation Flow

**Analogy**: Monthly income is a pizza. Budget allocation slices it for different purposes (rent, food, fun). At month-end, check if you ate the whole slice or had leftovers.

**ASCII Diagram**:

```
     Monthly Income
     $5,000.00
          │
    ┌─────┴─────┐
    ▼           ▼
┌────────┐  ┌────────────┐
│ Needs  │  │   Wants    │
│ $3,500 │  │   $1,500   │
└───┬────┘  └─────┬──────┘
    │             │
    ├─ Rent: $1,800
    ├─ Groceries: $600
    ├─ Utilities: $300
    ├─ Transport: $400
    ├─ Insurance: $400
    │
    └─ Food & Dining: $500
       ├─ Entertainment: $400
       ├─ Shopping: $300
       └─ Coffee: $300

At Month End:
┌────────────────────┐
│ Check Each Slice:  │
│ - Spent vs Planned │
│ - Over/Under       │
│ - Rollover         │
└────────────────────┘
```

**Step-by-Step**:

1. **Set monthly income**:
   ```python
   monthly_income = MonthlyIncome(
       month=datetime(2026, 1, 1),
       amount=5000.00
   )
   ```

2. **Create allocations**:
   ```python
   allocations = [
       BudgetAllocation(category='Rent', planned_amount=1800),
       BudgetAllocation(category='Groceries', planned_amount=600),
       BudgetAllocation(category='Food & Dining', planned_amount=500),
   ]
   ```

3. **Track spending**:
   ```python
   groceries_spent = sum(
       t.amount for t in transactions
       if t.bb_category == 'Groceries'
       and t.date.month == current_month
   )
   ```

4. **Calculate at month-end**:
   ```python
   for allocation in allocations:
       spent = get_spent_for_category(allocation.category)
       remaining = allocation.planned_amount - spent
       status = 'over' if remaining < 0 else 'under'
   ```

**Gotcha**: Negative = spending, positive = income. So -$50 means you spent $50!

---

## Example 4: Sinking Funds Mechanics

**Analogy**: Piggy banks for specific goals. Each month, drop coins into multiple piggy banks (vacation, car repair). When needed, break open that specific bank.

**ASCII Diagram**:

```
Monthly Contribution: $300
          │
    ┌─────┴─────┬──────────┬─────────┐
    │           │          │         │
    ▼           ▼          ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐
│Vacation│ │Car Fund│ │Holiday │ │Buffer│
│  $100  │ │  $100  │ │  $50   │ │  $50 │
└───┬────┘ └────┬───┘ └───┬────┘ └───┬──┘
    │           │         │          │
    ▼           ▼         ▼          ▼
  $800        $650      $200       $150
  /1000      /1000      /500       /500

  When needed:
  ┌──────────────┐
  │ Book Vacation│
  │  Cost: $800  │
  └──────┬───────┘
         │ Withdraw from Vacation fund
         ▼
  ┌──────────────┐
  │ Vacation: $0 │
  │ /1000        │
  └──────────────┘
```

**Step-by-Step**:

1. **Create fund**:
   ```python
   vacation_fund = SinkingFund(
       name='Summer Vacation',
       target_amount=1000.00,
       target_date=datetime(2026, 7, 1),
       current_balance=0.00
   )
   ```

2. **Monthly contribution**:
   ```python
   contribution = SinkingFundTransaction(
       fund_id=vacation_fund.id,
       amount=100.00,  # Positive = deposit
       transaction_type='contribution'
   )
   vacation_fund.current_balance += 100.00
   ```

3. **Track progress**:
   ```python
   progress = (vacation_fund.current_balance / vacation_fund.target_amount) * 100
   # 800 / 1000 = 80%
   ```

4. **Withdrawal**:
   ```python
   withdrawal = SinkingFundTransaction(
       fund_id=vacation_fund.id,
       amount=-800.00,  # Negative = withdrawal
       transaction_type='withdrawal'
   )
   vacation_fund.current_balance -= 800.00
   ```

**Gotcha**: Multiple funds compete for monthly budget. Prioritize!

---

## Example 5: Buddy AI Insight Generation

**Analogy**: Financial advisor who reviews spending weekly and emails advice. Like if your accountant sent: "Hey, noticed you spent a lot on coffee this week..."

**ASCII Diagram**:

```
Trigger: Monday 6 AM (cron)
          │
          ▼
┌────────────────────────┐
│ 1. Gather Data         │
│  - Last 7 days txns    │
│  - Budget status       │
│  - Goals progress      │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ 2. Build Prompt        │
│  "Analyze spending:    │
│   Food: $150/100       │
│   Transport: $50/80"   │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ 3. Call Claude API     │
│  Model: sonnet-4       │
│  Max tokens: 1024      │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ 4. Parse Response      │
│  Extract insights      │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ 5. Save to Database    │
│  weekly_reflections    │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ 6. Display in Frontend │
│  BuddyInsightsPanel    │
└────────────────────────┘
```

**Step-by-Step**:

1. **Cron triggers**:
   ```bash
   0 6 * * 1 python generate_buddy_weekly.py
   ```

2. **Gather data**:
   ```python
   week_start = get_last_monday()
   transactions = db.query(Transaction).filter(
       Transaction.date >= week_start,
       Transaction.date < week_start + timedelta(days=7)
   ).all()
   ```

3. **Build prompt**:
   ```python
   prompt = f"""
   Analyze this week's spending ({week_start}):

   Transactions: {format_transactions(transactions)}
   Budget Status: {format_budget_status(allocations)}

   Provide insights and recommendations.
   """
   ```

4. **Call API**:
   ```python
   import anthropic
   client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
   response = client.messages.create(
       model='claude-sonnet-4-20250514',
       max_tokens=1024,
       messages=[{'role': 'user', 'content': prompt}]
   )
   ```

5. **Save**:
   ```python
   reflection = WeeklyReflection(
       week_start_date=week_start,
       spending_summary=response.content[0].text
   )
   db.add(reflection)
   db.commit()
   ```

6. **Frontend displays**:
   ```javascript
   const response = await fetch('/api/v2/buddy/weekly-reflection');
   const data = await response.json();
   setBuddyInsight(data);
   ```

**Gotcha**: Rate limiting! Only 1 refresh per insight type per day. Otherwise you'd burn through API quota!

---

## Budget Buddy Data Flow

```
Banks (via Plaid)
      │
      ▼
┌──────────────┐
│ Transactions │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Classification│ ─── ML Model
└──────┬───────┘     └─ Training Data
       │
       ▼
┌──────────────┐
│ Budget       │
│ Tracking     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Insights     │ ─── Buddy AI (Claude)
│ Generation   │
└──────────────┘
```

## Common Patterns

**Pattern**: Transaction → Classification → Budget Impact

**Pattern**: Manual Override → Find Similar → Batch Update

**Pattern**: Weekly Data → AI Analysis → Insight Display
