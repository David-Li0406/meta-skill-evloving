# Clean Code Checking Rules for Python

This file contains the detailed rules for checking Python code quality. These rules are applied to each file during project review.

## Variable Naming Rules

### Single Letter Variables
**Rule**: Flag all single-letter variable names except:
- Loop counters: `i`, `j`, `k`
- Unused variables: `_`

**Examples to Flag**:
```python
d = datetime.now()  # BAD: What is 'd'?
x = calculate()     # BAD: What is 'x'?
a, b = get_data()   # BAD: What are 'a' and 'b'?
```

**Good Examples**:
```python
created_at = datetime.now()
result = calculate()
username, email = get_data()

# OK in loops
for i in range(10):
    for j in range(5):
```

### Unclear Abbreviations
**Rule**: Flag these common unclear abbreviations:
- `tmp`, `temp` without context
- `val`, `value` without context
- `data`, `info`, `obj` without context
- `num`, `cnt`, `idx` without context
- `str`, `lst`, `dict` (type-based names)

**Examples to Flag**:
```python
tmp = process_data()      # BAD: Temporary what?
val = get_value()         # BAD: Value of what?
data = fetch_data()       # BAD: What kind of data?
num = calculate()         # BAD: Number of what?
```

**Good Examples**:
```python
processed_users = process_data()
discount_percentage = get_value()
customer_orders = fetch_data()
total_items = calculate()
```

### Non-Descriptive Names
**Rule**: Flag generic names that don't reveal purpose:
- `result` (unless genuinely multi-purpose)
- `output` (unless genuinely generic)
- `item` in non-loop contexts
- `thing`, `stuff`

**Examples to Flag**:
```python
result = calculate_total()        # BAD: Result of what?
output = generate_report()        # BAD: Output of what?
item = get_current()              # BAD: What item?
```

**Good Examples**:
```python
order_total = calculate_total()
monthly_report = generate_report()
current_user = get_current()
```

### Intent-Revealing Names
**Rule**: Flag names that don't reveal intent or purpose:
- `flag`, `check` without context
- `handle_data`, `process_data` (too generic)
- Boolean variables not starting with `is_`, `has_`, `should_`, `can_`

**Examples to Flag**:
```python
flag = True                    # BAD: Flag for what?
check = verify()               # BAD: Check what?
active = user.status          # BAD: Active what?

def process_data(data):       # BAD: Process how?
    pass

def handle_request(req):      # BAD: Handle how?
    pass
```

**Good Examples**:
```python
is_authenticated = True
validation_passed = verify()
is_user_active = user.status

def validate_user_data(user_data):
    pass

def process_payment_request(payment_req):
    pass
```

## Function Length Rules

### Maximum Line Count
**Rule**: Functions should not exceed 20 lines (excluding blank lines, comments, and docstrings)

**Counting Rules**:
- Count actual code lines only
- Exclude blank lines
- Exclude docstrings (""" ... """)
- Exclude standalone comments
- Include inline comments in the count

**Example - Flagged Function (25 lines)**:
```python
def process_order(order):
    """Process an order and send confirmation."""  # Not counted
    # Not counted (blank line above)
    if not order.get('items'):                      # 1
        raise ValueError('Empty order')             # 2
                                                    # Not counted
    total = 0                                       # 3
    for item in order['items']:                     # 4
        total += item['price'] * item['quantity']   # 5
                                                    # Not counted
    if order.get('coupon'):                         # 6
        discount = get_discount(order['coupon'])    # 7
        total -= total * discount                   # 8
                                                    # Not counted
    shipping = calculate_shipping(order['address']) # 9
    total += shipping                               # 10
                                                    # Not counted
    tax = calculate_tax(total, order['address'])    # 11
    total += tax                                    # 12
                                                    # Not counted
    saved_order = db.orders.create(                 # 13
        items=order['items'],                       # 14
        total=total,                                # 15
        status='pending'                            # 16
    )                                               # 17
                                                    # Not counted
    email_body = generate_email_body(saved_order)   # 18
    send_email(                                     # 19
        order['email'],                             # 20
        'Order confirmed',                          # 21
        email_body                                  # 22
    )                                               # 23
                                                    # Not counted
    log_order_processed(saved_order.id)             # 24
    return saved_order                              # 25
```

**Report Format**:
```
Function Length Issues:
- process_order() (lines 1-30): 25 lines -> Split into smaller functions
```

### Function Responsibility
When flagging long functions, provide guidance:
- Functions doing multiple things should be split
- Suggest breaking into logical sub-functions
- Each function should have single responsibility

## Redundant Comments Rules

### Comments That Repeat Code
**Rule**: Flag comments that simply restate what the code does

**Examples to Flag**:
```python
# Set the name                   # REDUNDANT
user.name = 'John'

# Increment counter              # REDUNDANT
counter += 1

# Loop through items             # REDUNDANT
for item in items:
    pass

# Return the result              # REDUNDANT
return result

# Create empty list              # REDUNDANT
items = []

# Call the function              # REDUNDANT
process_data()

# Check if user exists           # REDUNDANT
if user:
    pass
```

### Comments Explaining Obvious Operations
**Rule**: Flag comments explaining standard Python operations

**Examples to Flag**:
```python
# Convert to string              # REDUNDANT for obvious operation
text = str(number)

# Get the length                 # REDUNDANT
length = len(items)

# Append to list                 # REDUNDANT
items.append(item)

# Open the file                  # REDUNDANT
with open('file.txt') as f:
    pass
```

### Comments That Should Be Function Names
**Rule**: Flag comments that describe what a block of code does (should be extracted to named function)

**Examples to Flag**:
```python
# Calculate the discount based on user tier
if user.tier == 'premium':
    discount = 0.2
elif user.tier == 'gold':
    discount = 0.1
else:
    discount = 0.05
total = subtotal * (1 - discount)

# Should be: discount = calculate_tier_discount(user.tier, subtotal)
```

### Valuable Comments (Don't Flag)
These comment types are valuable and should NOT be flagged:

**1. WHY explanations**:
```python
# Using exponential backoff to avoid API rate limits
await retry(apiCall, max_attempts=3)

# Cache invalidation needed due to upstream data changes
cache.clear()
```

**2. Workarounds and hacks**:
```python
# HACK: API returns None instead of empty list for new users
orders = response.get('data') or []

# FIXME: This breaks with timezones, should use UTC
deadline = datetime(2024, 1, 1)
```

**3. Complex algorithm explanations**:
```python
# Binary search implementation for O(log n) lookup
# Regex matches ISO 8601 format (e.g., 2024-01-15T10:30:00Z)
```

**4. TODOs and FIXMEs**:
```python
# TODO: Add error handling for network failures
# FIXME: Race condition when multiple threads access cache
```

**5. Performance notes**:
```python
# Using set for O(1) lookup instead of list O(n)
unique_ids = set(ids)
```

## Checking Process

For each file:

1. **Parse the file** to identify:
   - Variable assignments and their names
   - Function definitions and their line counts
   - Comments and their context

2. **Apply naming rules** to all variables:
   - Check against single-letter violations
   - Check against abbreviation violations
   - Check against generic name violations
   - Check against intent violations

3. **Apply function length rules**:
   - Count non-blank, non-comment, non-docstring lines
   - Flag if exceeds 20 lines
   - Note the actual line count

4. **Apply comment rules**:
   - Identify redundant comments
   - Keep valuable comments
   - Consider comment context

5. **Generate issue list** with:
   - Issue type (naming, length, comment)
   - Line number
   - Current problem
   - Suggested fix

## Issue Severity

When prioritizing files for refactoring:

**Critical (>10 issues)**:
- File needs significant refactoring
- Multiple categories of issues
- High impact on code maintainability

**High (6-10 issues)**:
- File needs refactoring
- Consider splitting into multiple files
- Medium-high impact

**Medium (3-5 issues)**:
- File needs improvement
- Targeted fixes possible
- Medium impact

**Low (1-2 issues)**:
- Minor improvements
- Quick fixes
- Low impact
