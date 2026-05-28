---
name: documentation
description:
  Write clear, maintainable code documentation. Use this skill when adding comments, writing
  docstrings, creating README files, or documenting APIs. Covers inline comments, function
  documentation, and project-level documentation.
---

# Code Documentation Best Practices

This skill provides guidance for writing effective documentation that helps developers understand
and maintain code.

## When This Skill Applies

- Adding comments to code
- Writing function/method docstrings
- Creating or updating README files
- Documenting APIs
- Writing architectural documentation

## Documentation Philosophy

Good documentation answers:

- **What**: What does this code do?
- **Why**: Why was this approach chosen?
- **How**: How should this be used? (for APIs)

Focus on **why** over **what**—code shows what, comments explain why.

## Inline Comments

### When to Comment

- Complex algorithms or business logic
- Non-obvious workarounds or edge cases
- Regulatory or compliance requirements
- Performance optimizations that aren't intuitive
- TODO/FIXME for known issues

### When NOT to Comment

- Obvious code that's self-explanatory
- Restating what the code does
- Commented-out code (delete it)
- Explaining bad code (refactor instead)

### Good vs Bad Comments

```python
# Bad: Restates the code
i = i + 1  # increment i by 1

# Good: Explains why
i = i + 1  # Account for 0-based indexing in API response

# Bad: Obvious
# Check if user is admin
if user.is_admin:

# Good: Non-obvious business rule
# Admins bypass rate limiting per SOC2 audit requirement (AUDIT-123)
if user.is_admin:
```

## Function Documentation

### Docstring Format

Use the standard format for your language:

**Python (Google style)**:

```python
def calculate_tax(amount: float, rate: float, exempt: bool = False) -> float:
    """Calculate tax for a given amount.

    Args:
        amount: The base amount before tax.
        rate: Tax rate as a decimal (e.g., 0.08 for 8%).
        exempt: If True, returns 0 regardless of amount.

    Returns:
        The calculated tax amount, or 0 if exempt.

    Raises:
        ValueError: If amount is negative.
    """
```

**TypeScript (JSDoc)**:

```typescript
/**
 * Calculate tax for a given amount.
 *
 * @param amount - The base amount before tax
 * @param rate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @param exempt - If true, returns 0 regardless of amount
 * @returns The calculated tax amount, or 0 if exempt
 * @throws {Error} If amount is negative
 */
function calculateTax(amount: number, rate: number, exempt = false): number;
```

**Go**:

```go
// CalculateTax computes the tax for a given amount.
// It returns 0 if exempt is true. Returns an error if amount is negative.
func CalculateTax(amount, rate float64, exempt bool) (float64, error)
```

**Rust**:

```rust
/// Calculate tax for a given amount.
///
/// # Arguments
///
/// * `amount` - The base amount before tax
/// * `rate` - Tax rate as a decimal (e.g., 0.08 for 8%)
/// * `exempt` - If true, returns 0 regardless of amount
///
/// # Errors
///
/// Returns `TaxError::NegativeAmount` if amount is negative.
pub fn calculate_tax(amount: f64, rate: f64, exempt: bool) -> Result<f64, TaxError>
```

## README Structure

A good README includes:

1. **Title and Description**: What is this project?
2. **Installation**: How to set it up
3. **Quick Start**: Get running in <5 minutes
4. **Usage Examples**: Common use cases
5. **Configuration**: Environment variables, options
6. **Contributing**: How to contribute
7. **License**: Legal information

### README Template

```markdown
# Project Name

Brief description of what this project does.

## Installation

\`\`\`bash npm install my-package \`\`\`

## Quick Start

\`\`\`javascript import { thing } from 'my-package'; thing.doSomething(); \`\`\`

## Configuration

| Variable  | Description  | Default  |
| --------- | ------------ | -------- |
| `API_KEY` | Your API key | Required |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

## API Documentation

For APIs, document:

- Endpoint URL and method
- Request parameters and body schema
- Response format and status codes
- Authentication requirements
- Rate limits
- Example requests and responses

## Architecture Documentation

For complex systems, maintain:

- **Architecture Decision Records (ADRs)**: Why major decisions were made
- **System diagrams**: How components interact
- **Data flow diagrams**: How data moves through the system
- **Runbooks**: How to operate and debug the system

## Maintenance

- Update docs when code changes
- Delete outdated documentation
- Review docs in code reviews
- Treat docs as code—version control them
