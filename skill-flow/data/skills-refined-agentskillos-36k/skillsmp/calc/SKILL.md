---
name: calc
description: This skill should be used when the user asks to "calculate", "compute", "convert units", "do math", or needs arithmetic/percentage/financial calculations.
---

# /calc

Perform calculations, unit conversions, and mathematical operations.

## Instructions

When the user provides a calculation request:

1. **Arithmetic**: Evaluate expressions, percentages, ratios
   - Show the calculation steps for complex operations
   - Round appropriately (2 decimals for money, significant figures for science)

2. **Unit Conversions**: Convert between units
   - Length: km, m, cm, mm, mi, ft, in
   - Weight: kg, g, lb, oz
   - Temperature: C, F, K
   - Data: B, KB, MB, GB, TB (use 1024 for binary, 1000 for SI)
   - Time: seconds, minutes, hours, days

3. **Financial**:
   - Compound interest: A = P(1 + r/n)^(nt)
   - Percentage change: ((new - old) / old) × 100
   - Tax calculations

4. **Programming-related**:
   - Binary/hex/decimal conversions
   - Bitwise operations
   - Memory calculations

## Output Format

```
Input: [what user asked]
Result: [answer with units]
Steps: [if complex, show work]
```

Always clarify ambiguous units (e.g., "GB - binary or SI?").
