---
name: accounting
description: Double-entry bookkeeping rules, accounting equation validation, entry creation and voiding procedures. Use this skill when working with journal entries, accounts, debits/credits, or any financial transaction recording.
---

# Double-Entry Bookkeeping Domain Model

> **Core Definition**: Accounting equation, account classification, and entry rules for double-entry bookkeeping.

## Accounting Equation

```
Assets = Liabilities + Equity + (Income - Expenses)
```

**At any moment, all `posted` entries must satisfy this equation.**

## Account Classification and Debit/Credit Rules

| Type | Debit Increases | Credit Increases | Normal Balance |
|------|-----------------|------------------|----------------|
| Asset | ✓ | | Debit |
| Liability | | ✓ | Credit |
| Equity | | ✓ | Credit |
| Income | | ✓ | Credit |
| Expense | ✓ | | Debit |

## Design Constraints

### ✅ Recommended Patterns

- **Pattern A**: Each entry has at least 2 lines, debit/credit balanced
- **Pattern B**: Use Decimal for precise calculations, tolerance < 0.01
- **Pattern C**: Posted entries can only be voided, not directly modified

### ⛔ Prohibited Patterns

- **NEVER** use FLOAT to store, calculate, or transfer monetary amounts.
- **NEVER** allow unbalanced debit/credit entries
- **NEVER** skip validation when writing posted status

## Standard Operating Procedures

### SOP-001: Create Manual Entry

```python
def create_manual_entry(user_id, date, memo, lines: list[dict]) -> JournalEntry:
    # 1. Validate debit/credit balance
    total_debit = sum(l["amount"] for l in lines if l["direction"] == "DEBIT")
    total_credit = sum(l["amount"] for l in lines if l["direction"] == "CREDIT")
    if abs(total_debit - total_credit) > Decimal("0.01"):
        raise ValidationError("Debit/credit not balanced")
    
    # 2. Create entry header
    entry = JournalEntry(
        user_id=user_id,
        entry_date=date,
        memo=memo,
        source_type="manual",
        status="draft"
    )
    
    # 3. Create lines
    for line in lines:
        entry.lines.append(JournalLine(**line))
    
    return entry
```

### SOP-002: Post Entry

```python
def post_entry(entry: JournalEntry) -> None:
    # 1. Re-validate balance
    validate_balance(entry)
    
    # 2. Validate accounts are active
    for line in entry.lines:
        if not line.account.is_active:
            raise ValidationError(f"Account {line.account.name} is disabled")
    
    # 3. Update status
    entry.status = "posted"
    entry.updated_at = datetime.utcnow()
```

### SOP-003: Void Entry

```python
def void_entry(entry: JournalEntry, reason: str) -> JournalEntry:
    # 1. Can only void posted entries
    if entry.status != "posted":
        raise ValidationError("Can only void posted entries")
    
    # 2. Create reversal entry
    reverse_entry = JournalEntry(
        user_id=entry.user_id,
        entry_date=date.today(),
        memo=f"Void: {entry.memo} ({reason})",
        source_type="system",
        status="posted"
    )
    
    for line in entry.lines:
        reverse_entry.lines.append(JournalLine(
            account_id=line.account_id,
            direction="CREDIT" if line.direction == "DEBIT" else "DEBIT",
            amount=line.amount,
            currency=line.currency
        ))
    
    # 3. Mark original entry
    entry.status = "void"
    
    return reverse_entry
```

## Source Files

- **Logic**: `apps/backend/src/services/accounting.py`
- **Models**: `apps/backend/src/models/journal.py`
- **Schemas**: `apps/backend/src/schemas/journal.py`
