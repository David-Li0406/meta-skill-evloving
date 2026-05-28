# Practical Workflow for Writing Comments

How to apply commenting principles in day-to-day development.

## Comments-First Development

Write comments before implementing code:

### Step 1: Document the Interface

Before writing any implementation, describe what you're building:

```python
def calculate_shipping_cost(order, destination):
    """
    Determine shipping cost based on order weight, dimensions, and destination.

    Uses tiered pricing: standard ground rates for domestic orders under 5kg,
    dimensional weight pricing for larger packages, and carrier-specific
    international rates.

    Args:
        order: Order object containing items with weight and dimensions
        destination: Address object with country and postal code

    Returns:
        Decimal cost in USD, or None if destination is not serviceable

    Raises:
        InvalidAddressError: If destination cannot be validated
    """
    pass  # Implement after documenting
```

### Step 2: Check Your Design

Read your comments critically:

- Is the interface clear enough to use without reading implementation?
- Are there awkward things to explain? (May indicate design problems)
- Would another developer understand the purpose and constraints?

**If comments are hard to write, the design may need work.**

### Step 3: Implement

Now write code that fulfills the documented contract. The comments guide implementation decisions.

### Step 4: Add Implementation Comments

As you write complex logic, annotate non-obvious parts:

```python
def calculate_shipping_cost(order, destination):
    """..."""  # Interface comment from Step 1

    total_weight = sum(item.weight for item in order.items)

    # Use dimensional weight if package is bulky but light
    # (carrier charges by whichever is greater)
    dim_weight = calculate_dimensional_weight(order)
    billable_weight = max(total_weight, dim_weight)

    # International orders route through specific carriers based on
    # destination country agreements - see shipping_partners.md
    if destination.country != 'US':
        return get_international_rate(billable_weight, destination)

    ...
```

### Step 5: Verify Alignment

After implementing, re-read your interface comments:

- Does the implementation match what's documented?
- Did you discover edge cases that should be documented?
- Are there new side effects or constraints to note?

## Comment Review Checklist

Use during code review or self-review:

### Interface Comments

- [ ] **Purpose is clear** - Can someone use this without reading the implementation?
- [ ] **Parameters explained** - Not just types, but meaning and constraints
- [ ] **Return value described** - What it represents, not just the type
- [ ] **Side effects documented** - State changes, I/O, external calls
- [ ] **Errors/exceptions listed** - What can go wrong and why
- [ ] **Different vocabulary** - Doesn't just repeat function/parameter names

### Implementation Comments

- [ ] **Explains "why"** - Rationale for non-obvious decisions
- [ ] **Highlights complexity** - Marks tricky or subtle code
- [ ] **Documents constraints** - Things that must remain true
- [ ] **Warns about gotchas** - What would break if changed carelessly
- [ ] **Avoids parroting** - Doesn't restate what code literally does

### General Quality

- [ ] **Matches current code** - No stale or misleading information
- [ ] **Appropriate detail level** - Not too verbose, not too sparse
- [ ] **Standalone clarity** - Makes sense without reading the code first
- [ ] **No commented-out code** - Dead code removed, not hidden

## When to Write Each Comment Type

### Write Interface Comments When:

- Creating a new function, method, class, or module
- The name alone doesn't fully explain usage
- There are non-obvious parameters, return values, or side effects
- Other developers will use this code

### Write Implementation Comments When:

- The algorithm is non-obvious
- You're working around a bug or limitation
- Performance considerations drove the approach
- There are temporal or ordering dependencies
- Future you would ask "why did I do this?"

### Skip Comments When:

- The code is genuinely trivial
- A well-chosen name makes intent clear
- You'd just be restating the code
- The comment would be more confusing than the code

## Maintenance Workflow

### When Modifying Code:

1. **Read existing comments first** - Understand documented intent
2. **Update comments with code** - Keep them synchronized
3. **Add comments for new complexity** - Don't leave future readers guessing
4. **Remove obsolete comments** - Delete rather than leave stale

### During Code Review:

1. Review comments as carefully as code
2. Flag missing comments on complex logic
3. Flag misleading or stale comments
4. Verify interface documentation is complete
