# Comment Antipatterns

What to avoid when writing comments.

## The Four Excuses (Debunked)

| Excuse | Why It's Wrong |
|--------|----------------|
| "Good code is self-documenting" | Code cannot express rationale, intent, or high-level abstractions. It shows *how*, not *why*. |
| "I don't have time to write comments" | Good comments *save* time. Every future reader pays the cost of missing context. 5 minutes now saves hours later. |
| "Comments get out of date and become lies" | So does code if not maintained. The solution is reviewing comments alongside code, not abandoning them. |
| "All the comments I've seen are worthless" | That's because they were written wrong. Bad comments don't invalidate the need—they demonstrate the need for better ones. |

## Bad Comment Patterns

### 1. Parroting the Code

The comment restates what the code literally does:

```python
# Bad
# Set x to 5
x = 5

# Add item to list
items.append(item)

# Return the result
return result
```

**Why it's bad:** Zero information added. The reader already knows what `x = 5` does.

### 2. Repeating Names

The comment just expands the variable or function name:

```python
# Bad
# The user's email address
user_email = get_email()

# Process the payment
def process_payment(payment):
    ...
```

**Why it's bad:** If the name is clear, the comment adds nothing. If the name is unclear, fix the name.

### 3. Same Abstraction Level

The comment describes the code at the same level of detail:

```python
# Bad
# Loop through users and check if each one is active
for user in users:
    if user.is_active:
        active_users.append(user)
```

**Why it's bad:** This is a prose translation of the code, not an explanation of its purpose.

**Better:**
```python
# Filter to users who can receive notifications (active accounts only)
for user in users:
    if user.is_active:
        active_users.append(user)
```

### 4. Vague or Generic Language

Comments that could apply to almost anything:

```python
# Bad
# Handle the data
def process(data):
    ...

# Do the thing
execute()

# Important logic here
if condition:
    ...
```

**Why it's bad:** These comments acknowledge complexity exists without explaining it.

### 5. Obvious Type Information

Especially in typed languages:

```typescript
// Bad
// The user's age as a number
age: number;

// Returns a string
function getName(): string {
    ...
}
```

**Why it's bad:** The type system already expresses this.

### 6. Change Log Comments

```python
# Bad
# Modified by John on 2023-05-01 to fix bug #1234
# Updated by Jane on 2023-06-15 to add validation
```

**Why it's bad:** Version control tracks this better. Comments should describe current state, not history.

### 7. Commented-Out Code

```python
# Bad
# result = old_calculation(x)
result = new_calculation(x)
```

**Why it's bad:** Creates confusion about intent. Version control preserves old code if needed.

### 8. TODO Without Context

```python
# Bad
# TODO: fix this

# TODO: refactor
```

**Why it's bad:** Doesn't explain what's wrong or what the fix should be.

**Better:**
```python
# TODO: Replace O(n^2) algorithm with hash-based lookup for large datasets
```

## The Litmus Tests

Before writing a comment, ask:

1. **Does this provide information not in the code?** If you're restating the code, delete it.

2. **Would a competent developer need this?** Don't explain language basics.

3. **Is this at a higher abstraction level?** Comments should describe *what* or *why*, not *how*.

4. **Does this use different vocabulary than the code?** If you're using the same words, you're probably parroting.

5. **Will this still be true after the code changes?** Avoid commenting on specific values or implementation details that may drift.

## When No Comment Is Better

Sometimes the best comment is none:

- Trivial operations (`i++`, `return true`)
- Self-explanatory function calls (`user.save()`)
- Well-named code that speaks for itself
- Comments that would just repeat the function name

**The goal is not more comments—it's useful comments.**
