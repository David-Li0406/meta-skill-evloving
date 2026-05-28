---
name: calculator
description: Perform basic arithmetic operations (addition, subtraction, multiplication, division). Use when the user asks to calculate or solve math problems.
argument-hint: <operation> <number1> <number2>
---

When this skill is invoked with $ARGUMENTS:

1. Parse the arguments to extract:
   - `operation`: one of "add", "subtract", "multiply", or "divide"
   - `a`: the first number
   - `b`: the second number

2. Perform the requested calculation:
   - **add**: Return a + b
   - **subtract**: Return a - b
   - **multiply**: Return a × b
   - **divide**: Return a ÷ b (check for division by zero)

3. Format the response clearly showing the operation and result

4. Handle edge cases:
   - If b is 0 for division, return an error message
   - If invalid numbers are provided, ask for valid numeric inputs
   - If operation is not recognized, list the available operations

5. Present the result in a clear, readable format

## Examples

**Addition:**
```
User: /calculator add 15 27
Result: 15 + 27 = 42
```

**Division:**
```
User: /calculator divide 144 12
Result: 144 ÷ 12 = 12
```
