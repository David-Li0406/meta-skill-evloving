# Universal Coding Guidelines

These rules apply across all programming languages. For language-specific conventions, refer to official style guides:

- **C++**: [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- **Kotlin**: [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- **TypeScript**: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- **Python**: [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/)

## Naming Conventions

### Descriptive Names

- **Classes**: Use nouns that describe the entity (e.g., `UserAccount`, `DatabaseConnection`)
- **Functions**: Use verbs that describe the action (e.g., `calculateTotal`, `fetchUserData`)
- **Variables**: Use meaningful names that indicate purpose (e.g., `connectionTimeout`, `userEmail`)
- **Constants**: Use names that explain the value's purpose (e.g., `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS`)

### Consistent Casing

Choose and maintain a consistent casing style throughout a file or module:

- **C++**: `snake_case` for variables/functions, `PascalCase` for classes
- **Kotlin/Java**: `camelCase` for variables/functions, `PascalCase` for classes
- **Python**: `snake_case` for variables/functions, `PascalCase` for classes
- **TypeScript**: `camelCase` for variables/functions, `PascalCase` for classes/interfaces

## File Organization

### File Header

Begin each file with:

1. **License or copyright notice** (if applicable)
2. **Module description**: Brief summary of file's purpose
3. **Author/maintainer** (optional)

Example:
```cpp
/**
 * Database Connection Pool Manager
 *
 * Manages a pool of reusable database connections to improve
 * performance and resource utilization.
 */
```

### Section Grouping

Organize file contents in this order:

1. **Dependencies/Imports**: External and internal dependencies
2. **Constants/Type Definitions**: Global constants, type aliases, enums
3. **Main Implementation**: Primary classes, functions, or logic
4. **Auxiliary Code**: Helper functions, utilities, internal support code

## Modularity

### Single Responsibility Principle

- **One purpose per unit**: Each class or function should have one well-defined responsibility
- **Split large features**: Break complex functionality into smaller, focused components
- **Cohesion**: Group related functionality together

### Example

❌ **Too much responsibility**:
```cpp
class UserManager {
    void authenticateUser();
    void saveToDatabase();
    void sendEmail();
    void generateReport();
    void processPayment();
};
```

✅ **Single responsibility**:
```cpp
class UserAuthenticator { void authenticate(); };
class UserRepository { void save(); };
class EmailService { void send(); };
class ReportGenerator { void generate(); };
class PaymentProcessor { void process(); };
```

## Comments and Documentation

### Public API Documentation

Document all public classes and functions with:

- **Purpose**: What the code does
- **Parameters**: What inputs it expects
- **Return value**: What it returns
- **Exceptions**: What errors it might throw
- **Usage examples**: How to use it (for complex APIs)

### Example

```cpp
/**
 * Calculates the compound interest on a principal amount.
 *
 * @param principal The initial amount invested
 * @param rate Annual interest rate (as decimal, e.g., 0.05 for 5%)
 * @param years Number of years to compound
 * @return The final amount including interest
 * @throws std::invalid_argument if principal, rate, or years is negative
 *
 * Example:
 *   double final = calculateCompoundInterest(1000.0, 0.05, 10);
 *   // Returns 1628.89
 */
double calculateCompoundInterest(double principal, double rate, int years);
```

### Comment Guidelines

- **Explain why, not what**: Code should be self-explanatory; comments explain reasoning
- **Keep updated**: Update comments when code changes
- **Avoid obvious comments**: Don't comment what's already clear from code
- **Use for complex logic**: Explain non-obvious algorithms or business rules

## Code Style

- **Readability first**: Optimize for humans reading the code, not just machines
- **Consistency**: Follow the project's established patterns
- **Formatting**: Use language-appropriate formatters (e.g., `clang-format`, `black`, `prettier`)
