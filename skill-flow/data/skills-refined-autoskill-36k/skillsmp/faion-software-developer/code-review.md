---
id: code-review
name: "Code Review"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Code Review

## Overview

Code review is a systematic examination of source code to find bugs, improve quality, ensure consistency, and share knowledge across the team. Effective code reviews balance thoroughness with velocity.

## When to Use

- All code changes before merging
- During pair programming sessions
- Security-sensitive changes (extra review)
- Architectural changes (broader review)
- Junior developer mentoring

## Key Principles

- **Review the code, not the author**: Focus on improvement, not criticism
- **Small, focused reviews**: Large PRs are hard to review well
- **Timely feedback**: Review within hours, not days
- **Constructive comments**: Suggest improvements, explain why
- **Share knowledge**: Reviews are learning opportunities

## Best Practices

### What to Review

```markdown
## Code Review Checklist

### Correctness
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
- [ ] Are there any obvious bugs?

### Design
- [ ] Is the code well-organized?
- [ ] Does it follow project patterns?
- [ ] Is there unnecessary complexity?
- [ ] Are responsibilities properly separated?

### Maintainability
- [ ] Is the code readable?
- [ ] Are names meaningful?
- [ ] Is it properly documented?
- [ ] Would a new team member understand it?

### Testing
- [ ] Are there sufficient tests?
- [ ] Do tests cover edge cases?
- [ ] Are tests readable and maintainable?
- [ ] Do tests actually verify behavior?

### Performance
- [ ] Any obvious performance issues?
- [ ] N+1 queries?
- [ ] Unnecessary allocations?
- [ ] Missing indexes for new queries?

### Security
- [ ] Input validation present?
- [ ] No hardcoded secrets?
- [ ] SQL injection prevented?
- [ ] Proper authentication/authorization?
```

### Writing Good Review Comments

```markdown
## Comment Types

### Blocking (Must Fix)
Use when the code has bugs, security issues, or violates standards.

**Bad:**
"This is wrong."

**Good:**
"This will cause a null pointer exception when `user` is None.
Consider adding a guard clause:
```python
if not user:
    return None
```"

### Suggestion (Should Consider)
Use for improvements that would make code better.

**Bad:**
"Use a different approach."

**Good:**
"Suggestion: Consider using `dict.get()` with a default value
to avoid the KeyError. This is more Pythonic and handles missing
keys gracefully:
```python
# Instead of
value = data['key'] if 'key' in data else 'default'

# Consider
value = data.get('key', 'default')
```"

### Nitpick (Minor)
Use for style issues or personal preferences. Mark as optional.

**Good:**
"Nit: Consider renaming `x` to `user_count` for clarity.
(Not blocking)"

### Question
Use when you don't understand something.

**Good:**
"Question: Why do we need to fetch the user twice here?
Is there a caching issue I'm missing?"

### Praise
Acknowledge good code!

**Good:**
"Nice! This is a clean solution to the caching problem.
The decorator pattern makes it very reusable."
```

### Review Response Guidelines

```markdown
## As a Reviewer

1. **Be timely**: Review within 24 hours (ideally 4 hours)
2. **Be thorough**: Don't just skim
3. **Be respectful**: Critique code, not people
4. **Be specific**: Point to exact lines, suggest fixes
5. **Be proportionate**: Don't block on nitpicks

## As an Author

1. **Keep PRs small**: < 400 lines ideally
2. **Provide context**: Good description, linked issues
3. **Self-review first**: Catch obvious issues
4. **Respond to all comments**: Even if just "Done"
5. **Don't take it personally**: Reviews improve code
```

### PR Description Template

```markdown
## Description
Brief description of what this PR does and why.

## Related Issues
Closes #123
Related to #456

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran to verify your changes.

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)
Add screenshots for UI changes.

## Additional Notes
Any additional information reviewers should know.
```

### Automated Review Assistance

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: make lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test

  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check coverage
        run: |
          pytest --cov=src --cov-fail-under=80

  pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Check PR size
        run: |
          CHANGES=$(git diff --stat origin/main | tail -1 | awk '{print $4}')
          if [ "$CHANGES" -gt 500 ]; then
            echo "::warning::PR has $CHANGES changed lines. Consider splitting."
          fi
```

### Review Scenarios

```python
# Scenario 1: Bug

# Original code
def calculate_discount(price, discount_percent):
    return price - (price * discount_percent)

# Review comment:
"""
Bug: discount_percent should be divided by 100 if passed as a whole number (e.g., 20 for 20%).

Current behavior:
  calculate_discount(100, 20) returns -1900 (wrong)

Expected:
  calculate_discount(100, 20) returns 80

Suggested fix:
  return price - (price * discount_percent / 100)

Or clarify in docstring that discount_percent should be 0-1 range.
"""


# Scenario 2: Design Issue

# Original code
class OrderProcessor:
    def process(self, order):
        # Validate
        if not order.items:
            raise ValueError("Empty order")

        # Calculate total
        total = sum(item.price * item.quantity for item in order.items)

        # Apply discount
        if order.user.is_premium:
            total *= 0.9

        # Charge payment
        payment_result = PaymentGateway().charge(order.user.card, total)

        # Send email
        EmailService().send_order_confirmation(order.user.email, order)

        # Update inventory
        for item in order.items:
            InventoryService().decrease(item.product_id, item.quantity)

        return payment_result

# Review comment:
"""
Design concern: This method has too many responsibilities (validation,
calculation, payment, email, inventory). Consider:

1. Extract validation to separate method
2. Inject dependencies (PaymentGateway, EmailService) instead of creating
3. Use events/queue for email and inventory updates (shouldn't block response)

Suggested structure:
```python
class OrderProcessor:
    def __init__(self, payment: PaymentGateway, events: EventBus):
        self.payment = payment
        self.events = events

    def process(self, order: Order) -> PaymentResult:
        self._validate(order)
        total = self._calculate_total(order)
        result = self.payment.charge(order.user.card, total)
        self.events.publish(OrderCompleted(order))  # Async handling
        return result
```
"""


# Scenario 3: Security Issue

# Original code
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

# Review comment:
"""
Security: This endpoint exposes user data without authentication.
Anyone can access any user's data by guessing IDs.

Required fixes:
1. Add authentication
2. Add authorization (users can only access their own data, or admin)
3. Consider using UUIDs instead of sequential IDs

```python
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(User).filter(User.id == user_id).first()
```
"""


# Scenario 4: Performance Issue

# Original code
def get_user_orders(user_id: int) -> list[dict]:
    user = db.query(User).filter(User.id == user_id).first()
    orders = []
    for order in user.orders:
        orders.append({
            "id": order.id,
            "items": [item.name for item in order.items],  # N+1!
            "total": order.total
        })
    return orders

# Review comment:
"""
Performance: This code has an N+1 query problem. For each order,
it makes a separate query for items.

For 100 orders: 1 (user) + 1 (orders) + 100 (items) = 102 queries

Fix with eager loading:
```python
def get_user_orders(user_id: int) -> list[dict]:
    user = db.query(User)\
        .options(
            joinedload(User.orders).joinedload(Order.items)
        )\
        .filter(User.id == user_id)\
        .first()
    # Now only 1 query with JOINs
```

Or use selectinload for better performance with many items:
```python
.options(selectinload(User.orders).selectinload(Order.items))
```
"""
```

### Review Metrics

```markdown
## Healthy Review Metrics

### Time Metrics
- **Time to first review**: < 4 hours
- **Review cycle time**: < 24 hours total
- **Rework rate**: < 20% of PRs need multiple iterations

### Quality Metrics
- **Defect escape rate**: Bugs found in production vs. review
- **Review coverage**: % of code changes reviewed
- **Comment ratio**: Comments per 100 lines changed

### Team Health
- **Review distribution**: Everyone reviews, not just seniors
- **Review load balance**: No one person bottlenecked
- **Tone**: Constructive, educational comments
```

### Code Review Best Practices Summary

```markdown
## For Reviewers

DO:
- Review promptly (within 4 hours)
- Explain the "why" behind suggestions
- Acknowledge good code
- Ask questions when unclear
- Approve when good enough (not perfect)

DON'T:
- Block on style preferences
- Rewrite author's code
- Be condescending
- Rubber stamp without reading
- Leave vague comments

## For Authors

DO:
- Keep PRs small and focused
- Write good descriptions
- Self-review before requesting
- Respond to all comments
- Test before submitting

DON'T:
- Take feedback personally
- Ignore comments
- Submit untested code
- Create massive PRs
- Rush reviewers
```

## Anti-patterns

- **Rubber stamping**: Approving without reading
- **Nitpick blocking**: Holding PRs for trivial issues
- **Inconsistent standards**: Different rules for different people
- **No praise**: Only pointing out problems
- **Delayed reviews**: Taking days to respond
- **Review avoidance**: Finding excuses not to review

## References

- [Google Engineering Code Review](https://google.github.io/eng-practices/review/)
- [Microsoft Code Review Best Practices](https://docs.microsoft.com/en-us/azure/devops/repos/git/about-pull-requests)
- [Thoughtbot Code Review Guide](https://github.com/thoughtbot/guides/tree/main/code-review)
- [Conventional Comments](https://conventionalcomments.org/)
