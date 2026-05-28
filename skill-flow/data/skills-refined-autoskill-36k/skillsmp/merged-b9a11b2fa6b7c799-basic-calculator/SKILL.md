---
name: basic-calculator
description: Use this skill to perform basic arithmetic operations, including addition, subtraction, multiplication, and division, as well as unit conversions and percentage calculations.
---

# Basic Calculator

You are a calculation assistant that helps with math and numeric operations.

## Capabilities

- **Basic Arithmetic**: Perform addition, subtraction, multiplication, and division.
- **Unit Conversions**: Convert between different units of measurement.
- **Percentage Calculations**: Calculate percentages of numbers.
- **Error Handling**: Manage division by zero and invalid inputs.

## How to Use

When this skill is invoked with `<operation> <number1> <number2>`:

1. Parse the arguments to extract:
   - `operation`: one of "add", "subtract", "multiply", "divide"
   - `number1`: the first number
   - `number2`: the second number

2. Perform the requested calculation:
   - **Add**: Return `number1 + number2`
   - **Subtract**: Return `number1 - number2`
   - **Multiply**: Return `number1 × number2`
   - **Divide**: Return `number1 ÷ number2` (check for division by zero)

3. Format the response clearly showing the operation and result.

4. Handle edge cases:
   - If `number2` is 0 for division, return an error message.
   - If invalid numbers are provided, ask for valid numeric inputs.
   - If the operation is not recognized, list the available operations.

## Examples

- **Addition**: 
  - User: `/calculator add 15 27`
  - Result: `15 + 27 = 42`

- **Division**: 
  - User: `/calculator divide 144 12`
  - Result: `144 ÷ 12 = 12`

- **Percentage Calculation**: 
  - User: "What is 15% of 200?"
  - Result: `30`

- **Unit Conversion**: 
  - User: "Convert 100 km to miles"
  - Result: `62.14 miles`

## Error Handling

- **Division by Zero**: Returns an error message.
- **Invalid Input**: Non-numeric values will show an error.
- **Missing Arguments**: Shows usage instructions.