# Refactoring Examples

Code refactoring examples showing how to identify and fix code smells, extract methods and classes, and improve code quality.

## How to Use

Each example includes:
- **📝 Prompt**: The exact prompt to use
- **🔴 Before Code**: Original code with issues
- **🟢 After Code**: Refactored, improved code
- **💡 Best Practices**: Refactoring guidelines
- **✅ Benefits**: What improved

## Examples

1. [Code Smells](./01-code-smells.md) - Identify and fix common code smells in a large class
2. [Extract Refactoring](./02-extract-refactoring.md) - Extract method and extract class examples

## Common Code Smells

### Bloaters
- **Long Method**: Methods with too many lines
- **Large Class**: Classes doing too much
- **Long Parameter List**: Too many parameters
- **Data Clumps**: Same data appearing together

### Object-Orientation Abusers
- **Switch Statements**: Can often be replaced with polymorphism
- **Temporary Field**: Fields only used sometimes
- **Refused Bequest**: Subclass doesn't use inherited methods

### Change Preventers
- **Divergent Change**: One class changed for many reasons
- **Shotgun Surgery**: One change requires many small edits
- **Parallel Inheritance**: Creating subclass requires creating another

### Dispensables
- **Comments**: Explaining bad code instead of fixing it
- **Duplicate Code**: Same code in multiple places
- **Dead Code**: Unused code
- **Speculative Generality**: Unused flexibility

### Couplers
- **Feature Envy**: Method uses another class more than its own
- **Inappropriate Intimacy**: Classes too dependent on each other
- **Message Chains**: Long chains of method calls

## Refactoring Techniques

### Composing Methods
- Extract Method
- Inline Method
- Extract Variable
- Inline Temp
- Replace Temp with Query
- Split Temporary Variable
- Remove Assignments to Parameters

### Moving Features
- Move Method
- Move Field
- Extract Class
- Inline Class
- Hide Delegate

### Organizing Data
- Encapsulate Field
- Replace Data Value with Object
- Replace Array with Object
- Duplicate Observed Data
- Change Value to Reference

### Simplifying Conditional Logic
- Decompose Conditional
- Consolidate Conditional Expression
- Consolidate Duplicate Conditional Fragments
- Remove Control Flag
- Replace Nested Conditional with Guard Clauses

### Simplifying Method Calls
- Rename Method
- Add Parameter
- Remove Parameter
- Separate Query from Modifier
- Parameterize Method
- Replace Parameter with Explicit Methods

### Dealing with Generalization
- Pull Up Field/Method
- Push Down Field/Method
- Extract Subclass
- Extract Superclass
- Extract Interface
- Collapse Hierarchy

## Best Practices

1. **Test First**: Always have tests before refactoring
2. **Small Steps**: Make small, incremental changes
3. **Run Tests**: After each change
4. **Commit Often**: Commit after each successful refactoring
5. **One Thing**: One refactoring at a time
6. **Code Review**: Get feedback on refactored code

## When to Refactor

### Rule of Three
1. First time - just do it
2. Second time - cringe but duplicate
3. Third time - refactor

### Signs You Need to Refactor
- Adding features is difficult
- Code is hard to understand
- Bugs are frequent
- Code reviews take too long
- Similar code in multiple places
- Tests are brittle

### When NOT to Refactor
- Code works and will never change
- Rewrite is cheaper
- Deadline is tomorrow
- Code you don't understand yet

## Tools

### IDEs with Refactoring
- **IntelliJ IDEA**: Best-in-class refactoring tools
- **VS Code**: Good refactoring extensions
- **Eclipse**: Solid refactoring support
- **Visual Studio**: .NET refactoring

### Static Analysis
- **SonarQube**: Code quality metrics
- **ESLint**: JavaScript linting
- **Pylint**: Python linting
- **RuboCop**: Ruby linting

## Resources

- [Refactoring by Martin Fowler](https://refactoring.com/)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Refactoring Guru](https://refactoring.guru/)
