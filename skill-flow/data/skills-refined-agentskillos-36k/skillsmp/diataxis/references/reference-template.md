# Reference Template

**Purpose**: Describe the machinery accurately and completely. User consults it, doesn't read it.

**Key Characteristics**:
- Neutral, objective, factual
- Structured by the system, not by use case
- Standard patterns and format
- Comprehensive but concise
- Examples for illustration, not instruction

## Structure

```markdown
# [Component/API/Feature] Reference

[One sentence: what this thing is]

Example: "The Configuration API provides programmatic access to all 
settings for the MyApp service."

## Overview

[Technical description of what this does, how it fits into the system]

Example: "Authentication in MyApp uses JWT tokens issued by the 
Identity Service and validated by all API endpoints."

## [Category 1: Organized by system structure]

### [Item]

[Description]

**Parameters** (if applicable)
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | [Description] |
| param2 | boolean | No | [Description] |

**Returns** (if applicable)
[Description of what is returned]

**Example**
```
[Concrete example showing usage]
```

**Notes**
- [Important limitation or constraint]
- [When to use vs. alternative]

### [Next item]

[Same structure]

## [Category 2: Another section]

[Repeat structure]

## Error messages

| Error | Meaning | Solution |
|-------|---------|----------|
| 401 Unauthorized | [What this means] | [How to fix] |
| 404 Not Found | [What this means] | [How to fix] |

## Constraints

- [Limitation or boundary]
- [Edge case to be aware of]

## Related references

- [Other reference pages]
```

## Language Patterns

Use these patterns consistently throughout your reference:

| Pattern | Example |
|---------|---------|
| **X is a [type] that [describes function]** | "The logger is a singleton object that handles all event logging." |
| **X inherits from Y, defined in Z** | "RequestHandler inherits from BaseHandler, defined in core/handlers.py." |
| **Sub-commands are: a, b, c** | "Commands are: list, create, delete, update." |
| **You must X. You must not Y unless Z** | "You must authenticate with OAuth2. You must not use API keys on public networks." |
| **May contain. Default: X** | "May contain traces of X. Default value: 1000ms" |

## Key Principles to Remember

✓ **Describe and only describe** — No instructions or explanations

✓ **Neutral and objective** — No opinions, preferences, or guidance

✓ **Precise and accurate** — No approximations or "mostly correct"

✓ **Structured by machinery** — Mirror how the system is actually built

✓ **Adopt standard patterns** — Use consistent structure throughout

✓ **Comprehensive** — Include all significant options and parameters

✓ **Wholly authoritative** — No doubt or ambiguity

✓ **Examples for illustration** — Show without instructing

## Example

See [examples.md](examples.md#example-3-reference) for a complete working example: "POST /api/articles Reference"
