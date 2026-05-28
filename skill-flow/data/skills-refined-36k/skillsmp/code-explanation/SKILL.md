---
name: code-explanation
description: Explain code with visual diagrams and analogies. Use when explaining how code works, teaching about codebase, answering "how does this work", walking through logic, or understanding Budget Buddy architecture.
allowed-tools: [Read, Grep, LSP, Glob]
---

# Code Explanation

Understand code through everyday analogies, ASCII art diagrams, and step-by-step walkthroughs.

## Explanation Framework

When explaining code, always include:

1. **Start with an analogy** - Compare to something from everyday life
2. **Draw a diagram** - Use ASCII art for flow/structure/relationships
3. **Walk through the code** - Step-by-step explanation
4. **Highlight a gotcha** - Common mistakes or misconceptions

Keep explanations conversational. For complex concepts, use multiple analogies.

## Example: Simple Function

**Function**: Calculate transaction similarity

**Analogy**: Like comparing twins - measuring how alike two descriptions are.

**Diagram**:
```
Transaction A: "STARBUCKS #123"
Transaction B: "STARBUCKS #456"
               │
               ▼
         ┌─────────────┐
         │  Compare    │
         │  Character  │
         │  by Character│
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │ Similarity: │
         │    0.92     │
         │   (92%)     │
         └─────────────┘
```

**Walk through**:
```python
from difflib import SequenceMatcher

def calculate_similarity(desc1, desc2):
    # Compare strings character by character
    matcher = SequenceMatcher(None, desc1.lower(), desc2.lower())

    # Get ratio (0.0 to 1.0)
    return matcher.ratio()

# Example
similarity = calculate_similarity(
    "STARBUCKS #123",
    "STARBUCKS #456"
)
# Returns: 0.92 (92% similar)
```

**Gotcha**: Case matters! Always `.lower()` both strings first.

## Quick Explanations

### Data Flow

```
User Input → Validation → Database → Processing → Response
    │            │           │           │           │
    └──────── Error Handling Throughout ────────────┘
```

### API Request Flow

```
Frontend (React)
    │
    ▼ fetch()
Backend (FastAPI)
    │
    ▼ query()
Database (SQLite)
    │
    ▼ results
Backend
    │
    ▼ JSON response
Frontend (updates UI)
```

### Classification Logic

```
Transaction arrives
    │
    ▼
Check history
    │
    ├─ Found? → Reuse category
    │
    └─ Not found? → ML predict
              │
              ▼
         Assign category
```

## Domain Concepts

**Complete Budget Buddy examples with detailed diagrams**: See [DOMAIN_EXAMPLES.md](DOMAIN_EXAMPLES.md)

Includes:
- **Transaction Classification Pipeline** - How transactions get categorized
- **Fuzzy Matching (0.85 threshold)** - Finding similar transactions
- **Budget Allocation Flow** - How monthly budgets work
- **Sinking Funds Mechanics** - Goal-based saving system
- **Buddy AI Insight Generation** - Automated AI analysis workflow

Each example includes:
- Real-world analogy
- ASCII diagram
- Step-by-step code walkthrough
- Common gotchas

## Explaining Process

### Step 1: Start with Analogy

**Bad**: "This function uses SequenceMatcher from difflib..."

**Good**: "Think of this like finding twins in a crowd. We're looking for fraternal twins (similar but not identical) by checking how much they look alike."

### Step 2: Draw the Flow

Use ASCII art to show:
- Data flow (→, ↓, ▼)
- Decision points (├, └)
- Processes (boxes)
- Results (final state)

### Step 3: Code Walkthrough

Show actual code with comments explaining each part:

```python
# Step 1: Get reference transaction
ref_tx = get_transaction(123)

# Step 2: Find candidates
candidates = db.query(Transaction).filter(
    Transaction.bb_category_manual == False  # Only unclassified
).all()

# Step 3: Calculate similarity
for candidate in candidates:
    similarity = calculate_similarity(ref_tx.description, candidate.description)
    if similarity >= 0.85:  # Our threshold
        matches.append(candidate)
```

### Step 4: Point Out Gotchas

"**Gotcha**: The threshold is 0.85 (85%). Lower = more matches but more false positives. Higher = fewer matches but more accurate."

## Common Patterns in Budget Buddy

### Pattern: Transaction Flow

```
Plaid API → Import → Classify → Store → Display
                        │
                        └─→ ML Model (if new merchant)
```

### Pattern: User Action Flow

```
User clicks → React event → API call → Backend processing → Database update → API response → UI update
```

### Pattern: Weekly Cron

```
Cron triggers → Gather data → Call Claude API → Parse response → Save to DB → Display in UI
```

## Tips for Good Explanations

1. **Assume Claude knows basics** - Don't explain what a database is
2. **Focus on "why"** - Why 0.85 threshold? Why this pattern?
3. **Show data transformations** - Input → Processing → Output
4. **Use real examples** - Actual transaction descriptions, real amounts
5. **Mention edge cases** - What if no transactions? What if API fails?

## Integration with Other Skills

- **Transaction Classification Debugger** - Explains fuzzy matching in depth
- **Frontend UI/UX Design** - Explains component structure
- **Buddy AI Setup** - Explains cron and insight generation

## References

- [DOMAIN_EXAMPLES.md](DOMAIN_EXAMPLES.md) - Complete Budget Buddy concept explanations
- `/backend/services/` - Core business logic to explain
- `/frontend/src/components/` - UI components to explain

## Last Updated

January 1, 2026
