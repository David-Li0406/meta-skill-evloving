---
name: basic-calculator
description: Use this skill to perform basic arithmetic operations such as addition, subtraction, multiplication, and division when the user needs to calculate or solve math problems.
---

# Basic Calculator

This skill provides fundamental arithmetic operations via a command-line interface or direct invocation.

## How to Use

When this skill is invoked with `<operation> <number1> <number2>`:

1. Parse the arguments to extract:
   - `operation`: one of "add", "subtract", "multiply", or "divide"
   - `number1`: the first number
   - `number2`: the second number (or more for addition and multiplication)

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

## Example Commands

### Addition
```bash
# Simple addition
python scripts/calculator.py add 15 27
# Output: 15 + 27 = 42
```

### Subtraction
```bash
# Chain subtraction
python scripts/calculator.py subtract 1000 250 150 100
# Output: 500
```

### Multiplication
```bash
# Multiply decimals
python scripts/calculator.py multiply 3.14 2
# Output: 6.28
```

### Division
```bash
# Division with decimals
python scripts/calculator.py divide 22 7
# Output: 3.142857142857143
```

## Error Handling

- **Division by zero**: Returns an error message.
- **Invalid input**: Non-numeric values will show an error.
- **Missing arguments**: Shows usage instructions.

This skill can be used in various contexts where arithmetic calculations are needed.