# Pattern: {Memorable Descriptive Name}

## The Story

### Act 1: The Promise

{What the code claims to do or appears to implement correctly at first glance}

**Code example showing the declaration:**

```python
# Example: Class declaration, function signature, type annotation
```

### Act 2: The Betrayal

{Where the implementation violates the promise or type system contract}

**Code example showing the violation:**

```python
# Example: Constructor accepting wrong type, storing incorrect data
```

### Act 3: The Consequences

{Observable symptoms that result from the violation - runtime checks, type suppressions, workarounds}

**Code example showing the symptoms:**

```python
# Example: isinstance() checks, # type: ignore comments, @overload workarounds
```

### Act 4: The Source

{Why the pattern exists - usually heterogeneous storage or type information loss at boundaries}

**Code example showing the origin:**

```python
# Example: Heterogeneous dict, untyped API, external data source
```

## The Fix

{Brief description of the correct solution}

**Code example showing the resolution:**

```python
# Example: Proper type annotations, TypeGuard usage, validation
```

## Detection Criteria

For automated pattern detection, the following must all be present:

1. **{Most distinctive criterion}** - This should eliminate 90%+ of false positives
2. **{Second most distinctive}** - Narrows to true matches
3. **{Verification criterion}** - Confirms the pattern
4. **{Root cause indicator}** - Shows architectural issue

## Impact Assessment

**Severity**: {Low/Medium/High/Critical}

**Consequences if left unfixed**:

- {Consequence 1}
- {Consequence 2}
- {Consequence 3}

**Effort to fix**: {Hours/Days estimate}

## Related Patterns

- **{Related Pattern 1}** - Similar issue in different context
- **{Related Pattern 2}** - May co-occur with this pattern
- **{Related Pattern 3}** - Opposite extreme (different problem)

## References

- {Link to documentation}
- {Link to PEP or specification}
- {Link to related discussions}
