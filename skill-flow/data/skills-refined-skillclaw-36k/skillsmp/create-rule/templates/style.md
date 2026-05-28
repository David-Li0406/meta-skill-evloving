# Code Style Guide

Style conventions for this codebase. Match the existing style.

## Formatting

### Line Length

Maximum line length: [X] characters.

### Indentation

Use [spaces/tabs], [N] per level.

### Trailing Commas

[Always/Never/Multiline only] use trailing commas.

## Imports

Order imports in these groups, separated by blank lines:

1. [First group - e.g., standard library]
2. [Second group - e.g., external packages]
3. [Third group - e.g., internal modules]
4. [Fourth group - e.g., relative imports]

```language
# Example
import standard_lib

import external_package

import internal_module

from . import relative
```

## Comments

### When to Comment

- Explain WHY, not WHAT
- Document non-obvious business logic
- [Add your conventions]

### When NOT to Comment

- Obvious code
- Commented-out code (delete it)
- [Add your conventions]

## Whitespace

### Blank Lines

- [N] blank lines between top-level definitions
- [N] blank line between method definitions in a class
- [Add more conventions]

### Spaces

- [Spaces around operators: yes/no]
- [Spaces after commas: yes/no]
- [Add more conventions]

## Quick Reference

| Element | Style |
|---------|-------|
| Line length | [X] chars |
| Indentation | [N] spaces |
| Quotes | [single/double] |
| Trailing commas | [yes/no/multiline] |
