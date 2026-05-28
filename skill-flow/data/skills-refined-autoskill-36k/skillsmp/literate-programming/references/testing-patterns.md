# Testing Patterns in Literate Programs

This reference describes best practices for organizing and writing tests in literate programs.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Test Placement: After Implementation](#test-placement-after-implementation)
3. [Distributed Test Organization](#distributed-test-organization)
4. [Main Test File Structure](#main-test-file-structure)
5. [Framing Test Sections](#framing-test-sections)
6. [Testing Dependencies](#testing-dependencies)
7. [Anti-Patterns](#anti-patterns)

---

## Core Principles

### Tests Should Verify Implementation, Not Precede It

**CRITICAL PRINCIPLE:** Tests should appear AFTER the functionality they verify, not before.

**Pedagogical flow:**
1. **Explain** the problem and approach
2. **Implement** the solution
3. **Verify** it works with tests

This ordering allows readers to:
- Understand what's being built before seeing verification
- See tests as proof/validation rather than mysterious code
- Follow a natural learning progression

### Keep Tests Close to Implementation

Tests should be within ~10 lines of their implementation, distributed throughout the document rather than grouped at the beginning or end.

---

## Test Placement: After Implementation

### Why Order Matters

When tests appear before implementation:
- Readers don't know what's being tested
- Tests feel unmotivated and disconnected
- Must scroll back hundreds of lines to understand context

When tests appear after implementation:
- Readers understand the code first
- Tests serve as proof/verification
- Natural pedagogical flow

### Example: Correct Placement

```noweb
\section{Make Classes Comparable}

We need a decorator that adds comparison methods to classes...

<<implementation>>=
def make_comparable(cls):
    """Add comparison methods to a class."""
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    cls.__eq__ = __eq__
    return cls
@

\subsection{Verifying Comparability}

Now let's verify the decorator works correctly:

<<test functions>>=
def test_users_equal():
    @make_comparable
    class User:
        def __init__(self, name):
            self.name = name

    assert User("Alice") == User("Alice")
    assert not (User("Alice") == User("Bob"))
@
```

---

## Distributed Test Organization

### Pattern: Build Up `<<test functions>>`

Define the main test file structure early, then accumulate test functions throughout the document:

```noweb
\section{Testing Overview}

Tests are distributed throughout this document, appearing after
each implementation section.

<<test [[module.py]]>>=
"""Tests for module functionality"""
import pytest
from module import *

<<test functions>>
@

\section{Feature A Implementation}

<<implementation of feature a>>=
def feature_a():
    return "a"
@

\subsection{Verifying Feature A}

<<test functions>>=
class TestFeatureA:
    def test_basic_case(self):
        assert feature_a() == "a"
@

\section{Feature B Implementation}

<<implementation of feature b>>=
def feature_b():
    return "b"
@

\subsection{Verifying Feature B}

<<test functions>>=
class TestFeatureB:
    def test_another_case(self):
        assert feature_b() == "b"
@
```

### Key Principles

1. **Use `from module import *`** - Import everything from the module being tested. This allows freely adding to `<<test functions>>` without updating imports.

2. **Single `<<test functions>>` chunk** - All test chunks use the same name. Noweb concatenates them in order of appearance.

3. **Tests stay close to implementations** - Each `<<test functions>>=` chunk appears immediately after the implementation it verifies.

### Test Organization Roadmap

For files with many test sections, provide a roadmap early:

```latex
\subsection{Test Organization}

Tests are distributed throughout this file:
\begin{description}
\item[Feature A tests] Appear after implementation (\cref{sec:featureA})
\item[Feature B tests] Appear after implementation (\cref{sec:featureB})
\item[Integration tests] Appear after all features (\cref{sec:integration})
\end{description}
```

---

## Main Test File Structure

### Standard Pattern

```noweb
<<test [[module.py]]>>=
"""Tests for module functionality"""
import pytest
from module import *

<<test functions>>
@
```

### With Poetry Projects

If using Poetry for dependency management, run tests with `poetry run pytest`:

```makefile
test: all
    poetry run pytest -v --cov=packagename --cov-report=term-missing
```

Without `poetry run`, pytest won't find your test dependencies.

---

## Framing Test Sections

Use pedagogical framing to introduce test sections:

### Good Framing Language

- "Now let's verify this works correctly..."
- "Let's prove this implementation handles edge cases..."
- "We can demonstrate correctness with these tests..."
- "To ensure reliability, we test..."

### What to Avoid

- Starting tests with no context
- Separating tests completely from what they test
- Grouping unrelated tests together

---

## Testing Dependencies

### Why Test Assumptions About Dependencies

When your code uses a dependency in a certain way, test that the dependency supports that usage. This catches breaking changes early.

### Example: Return Type Change

**Initial implementation** returns a list:
```python
def filter_objects(objects, pattern):
    results = []
    for obj in objects:
        if pattern.match(obj):
            results.append(obj)
    return results
```

**Refactored implementation** returns a generator:
```python
def filter_objects(objects, pattern):
    for obj in objects:
        if pattern.match(obj):
            yield obj
```

**Test that catches the change:**
```noweb
We want to test that [[filter_objects]] fulfills our expectations.
The calling code assumes the result is indexable:

<<test functions>>=
def test_filter_returns_indexable():
    results = filter_objects(sample_objects, pattern)
    # These assertions assume list behavior
    assert len(results) == 3
    assert results[0].name == "apple"
@
```

This test fails after refactoring because generators don't support `len()` or indexing.

### Types of Dependencies to Test

**Return type changes:**
- List vs generator
- List vs iterator vs iterable
- Single value vs collection
- None vs empty collection

**Behavior changes:**
- Raising exceptions vs returning None
- Eager vs lazy evaluation
- Mutable vs immutable returns

**Interface changes:**
- Available methods or attributes
- Parameter signatures
- State requirements

### Best Practices

1. **Test contracts when you depend on them**: If your code uses `results[0]`, test that the dependency returns something indexable.

2. **Test iteration behavior**: If you iterate twice, test that the dependency supports it (generators don't).

3. **Place tests near usage**: Keep dependency tests within ~10 lines of where the dependency is used.

4. **Frame pedagogically**: Explain why you're testing this assumption.

5. **Make implicit contracts explicit**: Document assumptions with tests.

---

## Anti-Patterns

### Tests Before Implementation (300 Lines Away)

**BAD:**
```noweb
\section{Testing}
<<test module.py>>=
import module

<<test equality>>=    # Reader doesn't know what this tests yet!
def test_users_equal():
    ...
@

[300 lines of other content]

\section{Make Classes Comparable}  # Implementation finally appears!
<<implementation>>=
def make_comparable(cls):
    ...
@
```

**Reader confusion:**
- "What does `test_users_equal` test?"
- Must scroll back hundreds of lines
- Tests feel unmotivated

### All Tests Grouped at Beginning

**BAD:**
```noweb
\section{All Tests}
<<test functions>>=
def test_feature_a():
    ...

def test_feature_b():
    ...

def test_feature_c():
    ...
@

[Rest of document with implementations]
```

**Problems:**
- Tests divorced from implementation
- Hard to maintain correspondence
- Violates pedagogical principle

### Tests Without Context

**BAD:**
```noweb
<<test functions>>=
def test_edge_case():
    assert func(None) is None
@
```

**GOOD:**
```noweb
\subsection{Handling None Input}

The function should gracefully handle None input by returning None:

<<test functions>>=
def test_handles_none_input():
    """Verify None input returns None without error."""
    assert func(None) is None
@
```

---

## When to Use This Pattern

**Use distributed test placement when:**
- Tests verify specific implementations in the same file
- Pedagogical clarity is important
- Tests serve as proof/examples of correctness
- File is meant to be read by humans

**Consider grouped tests when:**
- Tests are integration tests spanning multiple modules
- Test file is separate from implementation
- Tests don't directly correspond to specific code sections
