# Documentation Templates

> Ready-to-use templates for common documentation scenarios

## Function Documentation Template

### TypeScript/JavaScript

```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * Applies discount first, then calculates tax on the discounted amount.
 * Rounds to 2 decimal places for currency precision.
 *
 * @param basePrice - The original price before any adjustments
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discountPercent - Optional discount as decimal (0-1)
 * @returns The final calculated price
 * @throws {RangeError} If basePrice is negative
 *
 * @example
 * // Calculate price with 8% tax, 10% discount
 * calculateTotal(100, 0.08, 0.10); // Returns 97.20
 *
 * @example
 * // No discount
 * calculateTotal(50, 0.08); // Returns 54.00
 */
export function calculateTotal(
  basePrice: number,
  taxRate: number,
  discountPercent?: number
): number;
```

### Python

```python
def calculate_total(
    base_price: float,
    tax_rate: float,
    discount_percent: float = 0.0
) -> float:
    """Calculate total price including tax and discounts.
    
    Applies discount first, then calculates tax on the discounted
    amount. Rounds to 2 decimal places for currency precision.
    
    Args:
        base_price: The original price before adjustments.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%).
        discount_percent: Optional discount as decimal (0-1).
        
    Returns:
        The final calculated price rounded to 2 decimals.
        
    Raises:
        ValueError: If base_price is negative.
        
    Example:
        >>> calculate_total(100, 0.08, 0.10)
        97.20
        >>> calculate_total(50, 0.08)
        54.00
    """
```

## README Template

```markdown
# Project Name

[![Build Status](badge-url)](link)
[![License](badge-url)](link)

Brief one-paragraph description of what this project does and why it exists.

## Quick Start

\`\`\`bash
npm install project-name
\`\`\`

\`\`\`typescript
import { main } from 'project-name';
main();
\`\`\`

## Installation

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

\`\`\`bash
git clone https://github.com/org/project-name
cd project-name
npm install
npm run build
\`\`\`

## Usage

### Basic Example

\`\`\`typescript
// Example code here
\`\`\`

### Advanced Configuration

\`\`\`typescript
// More complex example
\`\`\`

## API Reference

| Function | Description |
|----------|-------------|
| `functionA()` | Does X |
| `functionB()` | Does Y |

See [API Documentation](./docs/api.md) for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT - see [LICENSE](./LICENSE)
```

## API Reference Template

```markdown
# API Reference: ModuleName

## Overview

Brief description of what this module provides.

## Functions

### functionName(param1, param2)

Brief description.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | Description |
| param2 | number | No | Description (default: 10) |

**Returns:** `ReturnType` - Description

**Throws:**
- `ErrorType` - When condition occurs

**Example:**

\`\`\`typescript
const result = functionName('input', 5);
\`\`\`

---

### anotherFunction(options)

...
```

## Changelog Entry Template

```markdown
## [1.2.0] - 2026-01-23

### Added
- New feature X for doing Y (#123)
- Support for Z format

### Changed
- Improved performance of function A by 50%
- Updated dependency B to v2.0

### Fixed
- Bug where X happened when Y (#456)
- Memory leak in component Z

### Deprecated
- Old function X, use Y instead

### Removed
- Legacy support for format A
```
