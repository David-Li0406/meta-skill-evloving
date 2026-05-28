---
name: calculator
description: Use this skill when you need to perform basic arithmetic operations such as addition, subtraction, multiplication, or division.
---

# Skill body

When this skill is invoked with `<operation> <number1> <number2>`:

1. Parse the arguments to extract:
   - `operation`: one of "add", "subtract", "multiply", or "divide"
   - `number1`: the first number
   - `number2`: the second number (or more for addition and subtraction)

2. Perform the requested calculation:
   - **add**: Return the sum of all provided numbers.
   - **subtract**: Return the result of subtracting all subsequent numbers from the first number.
   - **multiply**: Return the product of all provided numbers.
   - **divide**: Return the result of dividing the first number by all subsequent numbers (check for division by zero).

3. Format the response clearly showing the operation and result.

4. Handle edge cases:
   - If division by zero is attempted, return an error message.
   - If invalid numbers are provided, ask for valid numeric inputs.
   - If the operation is not recognized, list the available operations.

## Examples

**Addition:**
```
User: /calculator add 15 27
Result: 15 + 27 = 42
```

**Subtraction:**
```
User: /calculator subtract 100 25 15
Result: 100 - 25 - 15 = 60
```

**Multiplication:**
```
User: /calculator multiply 6 7
Result: 6 × 7 = 42
```

**Division:**
```
User: /calculator divide 144 12
Result: 144 ÷ 12 = 12
```