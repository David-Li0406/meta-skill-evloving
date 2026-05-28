# Python Code Review Checklist

## Type Hints
- [ ] All public functions have type hints
- [ ] mypy passes with no errors
- [ ] Return types specified

## Error Handling
- [ ] Specific exceptions caught
- [ ] No bare except clauses
- [ ] Errors logged appropriately

## Testing
- [ ] Tests exist for new code
- [ ] Edge cases covered
- [ ] >80% code coverage

## Style
- [ ] Follows PEP 8
- [ ] ruff/black formatted
- [ ] No unused imports
- [ ] Docstrings on public functions

## Security
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] Dependency vulnerabilities checked

## Performance
- [ ] Async for I/O operations
- [ ] No N+1 queries
- [ ] Efficient data structures

## Anti-Patterns to Avoid

```python
# Bad: Mutable default arguments
def append_to(element, to=[]):  # Bug!
    to.append(element)
    return to

# Good
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```
