---
name: transaction-classification-debugger
description: Debug and test Budget Buddy's fuzzy matching transaction classification system using 0.85 similarity threshold. Use when debugging classification issues, understanding fuzzy matching algorithm, testing merchant matching, finding similar transactions, or explaining how the smart batch update feature works.
allowed-tools: [Bash(python*), Read, Grep, LSP]
---

# Transaction Classification Debugger

## Overview

This skill helps you understand and debug Budget Buddy's transaction classification system, which uses fuzzy matching to find similar transactions at an 85% similarity threshold. It's critical for the "smart batch update" feature that suggests applying classifications to similar unclassified transactions.

## Prerequisites

- Database exists with transactions: `budget_buddy.db`
- Backend code accessible
- Understanding of Python's `difflib.SequenceMatcher`

## Quick Start

### Step 1: Understand the Fuzzy Matching Algorithm

The core algorithm is in `/backend/services/database_service.py` - method `get_similar_unclassified_transactions`:

```python
from difflib import SequenceMatcher

def get_similar_unclassified_transactions(
    transaction_id: int,
    similarity_threshold: float = 0.85
):
    # 1. Get reference transaction
    reference_tx = get_transaction_by_id(transaction_id)

    # 2. Find candidates (same merchant OR similar description)
    candidates = session.query(Transaction).filter(
        # Must NOT be manually classified
        Transaction.bb_category_manual == False,
        # Different transaction
        Transaction.id != transaction_id,
        # Either exact merchant match OR similar description
        or_(
            Transaction.merchant_name == reference_tx.merchant_name,
            # Description will be checked with fuzzy matching below
        )
    ).all()

    # 3. Fuzzy match descriptions
    similar_transactions = []
    for candidate in candidates:
        similarity = SequenceMatcher(
            None,
            reference_tx.description.lower(),
            candidate.description.lower()
        ).ratio()

        if similarity >= similarity_threshold:
            similar_transactions.append({
                'transaction': candidate,
                'similarity_score': similarity,
                'match_reason': 'description' if similarity >= 0.85 else 'merchant'
            })

    return similar_transactions
```

### Step 2: Test Fuzzy Matching

**Test with sample descriptions**:

```python
from difflib import SequenceMatcher

# Example: Check similarity between two transaction descriptions
desc1 = "CHECK #80 - MONTHLY RENT"
desc2 = "CHECK #79 - MONTHLY RENT"

similarity = SequenceMatcher(None, desc1.lower(), desc2.lower()).ratio()
print(f"Similarity: {similarity:.2%}")  # Should be ~95%
```

**Test in database**:

```python
import sqlite3

conn = sqlite3.connect('budget_buddy.db')
cursor = conn.cursor()

# Get transaction with ID 123
cursor.execute("SELECT id, description, merchant_name FROM transactions WHERE id = 123")
reference = cursor.fetchone()

print(f"Reference: {reference}")

# Find similar transactions
cursor.execute("""
    SELECT id, description, merchant_name, bb_category_manual
    FROM transactions
    WHERE id != 123
    AND bb_category_manual = 0
    LIMIT 100
""")

from difflib import SequenceMatcher
for tx in cursor.fetchall():
    similarity = SequenceMatcher(None, reference[1].lower(), tx[1].lower()).ratio()
    if similarity >= 0.85:
        print(f"Match: ID={tx[0]}, Similarity={similarity:.2%}, Desc={tx[1]}")

conn.close()
```

### Step 3: Debug Classification Issues

**Check bb_category_manual flag**:

```bash
sqlite3 budget_buddy.db "
SELECT
    id,
    description,
    merchant_name,
    bb_category,
    bb_category_manual
FROM transactions
WHERE merchant_name = 'TARGET'
LIMIT 10;
"
```

**Find unclassified transactions**:

```bash
sqlite3 budget_buddy.db "
SELECT COUNT(*) as unclassified_count
FROM transactions
WHERE bb_category_manual = 0;
"
```

**Check for similar descriptions**:

```python
import sqlite3
from difflib import SequenceMatcher

conn = sqlite3.connect('budget_buddy.db')
cursor = conn.cursor()

# Find transactions similar to "WHOLE FOODS MARKET"
cursor.execute("SELECT id, description FROM transactions LIMIT 1000")
transactions = cursor.fetchall()

target_desc = "WHOLE FOODS MARKET #12345"

for tx_id, desc in transactions:
    similarity = SequenceMatcher(None, target_desc.lower(), desc.lower()).ratio()
    if similarity >= 0.85 and similarity < 1.0:  # Similar but not identical
        print(f"ID {tx_id}: {similarity:.2%} - {desc}")

conn.close()
```

## Key Validation Points

### Matching Criteria

1. **Merchant Name Match** (Exact):
   - `merchant_name` must be identical
   - Case-sensitive comparison
   - Example: "TARGET" ≠ "Target"

2. **Description Match** (Fuzzy, 85%):
   - Uses `difflib.SequenceMatcher`
   - Threshold: 0.85 (85% similarity)
   - Case-insensitive (converted to lowercase)
   - Example: "CHECK #80" ≈ "CHECK #79" (95% similar)

3. **Manual Classification Filter**:
   - `bb_category_manual = False` (REQUIRED)
   - Never suggest already-manually-classified transactions
   - Prevents overwriting user decisions

### Similarity Threshold Analysis

| Threshold | Strictness | Use Case |
|-----------|------------|----------|
| 0.95-1.0  | Very strict | Nearly identical (e.g., "CHECK #80" vs "CHECK #79") |
| **0.85-0.95** | **Balanced (DEFAULT)** | **Similar patterns (e.g., same merchant with different check numbers)** |
| 0.75-0.85 | Loose | Broader matches (may include false positives) |
| < 0.75    | Very loose | Too many false positives |

**Why 0.85?**
- Captures variations like check numbers, dates, locations
- Avoids false positives from unrelated merchants
- Proven effective over 70+ commits

## Common Issues & Solutions

### Issue: No similar transactions found

**Possible Causes**:
1. All similar transactions already manually classified (`bb_category_manual = True`)
2. `merchant_name` is null/empty AND description similarity < 0.85
3. Reference transaction is the only one of its kind

**Debug**:
```bash
# Check if merchant_name exists
sqlite3 budget_buddy.db "
SELECT COUNT(*)
FROM transactions
WHERE merchant_name = 'YOUR_MERCHANT'
AND bb_category_manual = 0;
"

# Check description patterns
sqlite3 budget_buddy.db "
SELECT description
FROM transactions
WHERE description LIKE '%PATTERN%'
LIMIT 20;
"
```

### Issue: Too many false positive matches

**Cause**: Threshold too low or descriptions too generic

**Solution**:
```python
# Test with higher threshold
similar = get_similar_unclassified_transactions(
    transaction_id=123,
    similarity_threshold=0.90  # Increased from 0.85
)
```

**Example False Positives**:
- "PAYMENT THANK YOU" vs "PAYMENT RECEIVED" (85% similar but different meaning)
- Generic descriptions matching unrelated transactions

### Issue: Missing obvious matches

**Cause**: Threshold too high or `merchant_name` mismatch

**Solution**:
```python
# Test with lower threshold
similar = get_similar_unclassified_transactions(
    transaction_id=123,
    similarity_threshold=0.80  # Decreased from 0.85
)
```

**Example Missed Matches**:
- "WHOLE FOODS #123" vs "WHOLE FOODS MARKET #456" (if threshold too high)
- Merchant name variations: "TARGET" vs "TARGET CORP"

### Issue: Manually classified transactions appearing in suggestions

**Cause**: `bb_category_manual` not properly set

**Solution**:
```bash
# Verify flag is set correctly
sqlite3 budget_buddy.db "
SELECT id, description, bb_category, bb_category_manual
FROM transactions
WHERE id IN (123, 456, 789);
"

# Fix if needed
sqlite3 budget_buddy.db "
UPDATE transactions
SET bb_category_manual = 1
WHERE id IN (SELECT id FROM transactions WHERE bb_category IS NOT NULL);
"
```

## Smart Batch Update Workflow

### User Journey

1. **User manually classifies transaction** (inline or modal)
   - Updates `bb_category` and sets `bb_category_manual = True`

2. **Backend checks for similar transactions**
   - Calls `get_similar_unclassified_transactions()`
   - Finds matches with `merchant_name` OR fuzzy `description`
   - Filters to only unclassified (`bb_category_manual = False`)

3. **Frontend shows modal with checkboxes**
   - Lists similar transactions
   - Shows similarity score for each
   - User selects which to update

4. **Batch update endpoint applies classification**
   - Updates selected transactions
   - Sets `bb_category_manual = True` for all
   - Maintains audit trail

### Integration Points

1. **`backend/services/database_service.py`**
   - Method: `get_similar_unclassified_transactions()`
   - Line: ~varies (search for method)

2. **Frontend: `ClassificationManagement.js`**
   - Inline dropdown editing
   - Triggers similarity check on change

3. **Frontend: `EnhancedTransactionModal.js`**
   - Modal form editing
   - OnSaveSuccess callback triggers similarity check

4. **Frontend: Batch Edit Modal**
   - Checkbox selection
   - Batch update API call

## Testing the Fuzzy Matcher

### Test Case 1: Check Numbers

```python
from difflib import SequenceMatcher

desc1 = "CHECK #1234 - MONTHLY RENT"
desc2 = "CHECK #1235 - MONTHLY RENT"

similarity = SequenceMatcher(None, desc1.lower(), desc2.lower()).ratio()
print(f"Similarity: {similarity:.2%}")  # ~95% - MATCH

# Should be found as similar (> 0.85)
assert similarity >= 0.85
```

### Test Case 2: Merchant Variations

```python
desc1 = "WHOLE FOODS MARKET #12345"
desc2 = "WHOLE FOODS MARKET #67890"

similarity = SequenceMatcher(None, desc1.lower(), desc2.lower()).ratio()
print(f"Similarity: {similarity:.2%}")  # ~88% - MATCH

assert similarity >= 0.85
```

### Test Case 3: Unrelated Transactions

```python
desc1 = "STARBUCKS COFFEE #123"
desc2 = "TARGET STORE #456"

similarity = SequenceMatcher(None, desc1.lower(), desc2.lower()).ratio()
print(f"Similarity: {similarity:.2%}")  # ~20% - NO MATCH

assert similarity < 0.85
```

### Test Case 4: Date Variations

```python
desc1 = "PAYMENT DUE 01/15/2026"
desc2 = "PAYMENT DUE 02/15/2026"

similarity = SequenceMatcher(None, desc1.lower(), desc2.lower()).ratio()
print(f"Similarity: {similarity:.2%}")  # ~90% - MATCH

assert similarity >= 0.85
```

## Advanced Debugging

### Visualize Similarity Scores

```python
import sqlite3
from difflib import SequenceMatcher
import matplotlib.pyplot as plt  # if available

conn = sqlite3.connect('budget_buddy.db')
cursor = conn.cursor()

# Get reference transaction
ref_id = 123
cursor.execute("SELECT description FROM transactions WHERE id = ?", (ref_id,))
ref_desc = cursor.fetchone()[0]

# Get all other transactions
cursor.execute("SELECT id, description FROM transactions WHERE id != ?", (ref_id,))
transactions = cursor.fetchall()

# Calculate similarities
similarities = []
for tx_id, desc in transactions:
    score = SequenceMatcher(None, ref_desc.lower(), desc.lower()).ratio()
    similarities.append((tx_id, score, desc))

# Sort by score
similarities.sort(key=lambda x: x[1], reverse=True)

# Print top 10
print(f"\nTop 10 matches for: {ref_desc}\n")
for tx_id, score, desc in similarities[:10]:
    print(f"{score:.2%} - ID {tx_id}: {desc}")

conn.close()
```

### Test Threshold Variations

```python
thresholds = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

for threshold in thresholds:
    similar = get_similar_unclassified_transactions(
        transaction_id=123,
        similarity_threshold=threshold
    )
    print(f"Threshold {threshold:.2f}: {len(similar)} matches")
```

## Technical Details

### difflib.SequenceMatcher

```python
from difflib import SequenceMatcher

# Create matcher
matcher = SequenceMatcher(None, "string1", "string2")

# Get similarity ratio (0.0 to 1.0)
ratio = matcher.ratio()

# Get matching blocks
blocks = matcher.get_matching_blocks()

# Get opcodes (insert, delete, replace, equal)
opcodes = matcher.get_opcodes()
```

**Ratio Calculation**:
```
ratio = 2 * M / T

Where:
M = number of matching characters
T = total number of characters in both strings
```

### Database Schema

**Transactions Table**:
- `id` - Primary key
- `description` - Original transaction description
- `merchant_name` - Extracted merchant (from Plaid or manual)
- `bb_category` - Assigned budget category
- `bb_category_manual` - Boolean (0=auto, 1=manual)
- `amount` - Transaction amount
- `date` - Transaction date

**Key Insight**: Only transactions with `bb_category_manual = 0` (False) are suggested for batch updates.

## Integration with Other Skills

- **Code Explanation** - Can explain fuzzy matching algorithm visually
- **Development Diagnostics** - Validates database has transactions to classify
- **Testing & Validation Suite** - Can include fuzzy matching tests

## References

- `/backend/services/database_service.py` - `get_similar_unclassified_transactions()` method
- `/frontend/src/components/transactions/ClassificationManagement.js` - Inline classification
- `/frontend/src/components/transactions/EnhancedTransactionModal.js` - Modal classification
- Python docs: https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher

## Last Updated

January 1, 2026
