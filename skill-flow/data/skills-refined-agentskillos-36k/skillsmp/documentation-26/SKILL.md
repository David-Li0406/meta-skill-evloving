---
name: documentation
description: Generate and maintain high-quality technical documentation including API docs, README files, architecture documentation, user guides, and code comments. Use when creating documentation, writing README files, documenting APIs, or when user mentions documentation, docs, or technical writing.
---

# Documentation

A comprehensive documentation skill that helps create, maintain, and improve technical documentation across various formats and purposes.

## Quick Start

Basic documentation workflow:

```python
# Read existing code/project structure
# Identify documentation needs
# Generate appropriate documentation format
# Include examples and usage patterns
```

## Core Capabilities

### 1. API Documentation

Generate comprehensive API documentation:

- **REST APIs**: Endpoints, parameters, responses, examples
- **Function/Method Documentation**: Parameters, return values, exceptions
- **Type Definitions**: Interfaces, classes, data structures
- **Authentication**: Auth methods, security considerations
- **Error Handling**: Status codes, error messages, troubleshooting

### 2. README Files

Create clear and complete README files:

- **Project Overview**: Purpose, features, benefits
- **Installation**: Prerequisites, setup steps, configuration
- **Quick Start**: Minimal example to get started
- **Usage Examples**: Common use cases with code samples
- **Configuration**: Environment variables, config files
- **Contributing**: Guidelines for contributors
- **License**: License information

### 3. Code Documentation

Improve inline code documentation:

- **Docstrings**: Function/class documentation following conventions
- **Comments**: Explanatory comments for complex logic
- **Type Hints**: Type annotations (Python, TypeScript)
- **JSDoc**: JavaScript documentation comments
- **Javadoc**: Java documentation comments

### 4. Architecture Documentation

Document system architecture:

- **Architecture Diagrams**: System components and relationships
- **Design Decisions**: ADRs (Architecture Decision Records)
- **Data Flow**: How data moves through the system
- **Technology Stack**: Technologies used and why
- **Deployment**: Infrastructure and deployment processes

### 5. User Guides

Create user-facing documentation:

- **Getting Started**: First steps for new users
- **Tutorials**: Step-by-step learning paths
- **How-To Guides**: Task-focused instructions
- **Reference**: Complete feature documentation
- **Troubleshooting**: Common issues and solutions

## Documentation Standards

### Python Docstrings (Google Style)

```python
def calculate_total(items: list[dict], tax_rate: float = 0.1) -> float:
    """Calculate total price including tax for a list of items.
    
    Takes a list of items with prices and calculates the total cost
    including the specified tax rate.
    
    Args:
        items: List of item dictionaries with 'price' keys
        tax_rate: Tax rate as decimal (default: 0.1 for 10%)
    
    Returns:
        Total price including tax, rounded to 2 decimal places
    
    Raises:
        ValueError: If items list is empty or contains invalid prices
        TypeError: If items is not a list
    
    Examples:
        >>> items = [{'price': 10.0}, {'price': 20.0}]
        >>> calculate_total(items)
        33.0
        
        >>> calculate_total(items, tax_rate=0.2)
        36.0
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    if not items:
        raise ValueError("items list cannot be empty")
    
    subtotal = sum(item['price'] for item in items)
    total = subtotal * (1 + tax_rate)
    return round(total, 2)
```

### JavaScript/TypeScript JSDoc

```typescript
/**
 * Fetches user data from the API with error handling and caching
 * 
 * @param {string} userId - The unique identifier for the user
 * @param {Object} options - Configuration options
 * @param {boolean} options.useCache - Whether to use cached data (default: true)
 * @param {number} options.timeout - Request timeout in milliseconds (default: 5000)
 * 
 * @returns {Promise<User>} Promise resolving to User object
 * 
 * @throws {UserNotFoundError} When user doesn't exist
 * @throws {NetworkError} When network request fails
 * @throws {TimeoutError} When request exceeds timeout
 * 
 * @example
 * // Basic usage
 * const user = await fetchUser('user123');
 * 
 * @example
 * // With options
 * const user = await fetchUser('user123', {
 *   useCache: false,
 *   timeout: 10000
 * });
 */
async function fetchUser(
  userId: string,
  options: FetchOptions = {}
): Promise<User> {
  // Implementation...
}
```

### Java Javadoc

```java
/**
 * Processes payment transactions with validation and fraud detection.
 * 
 * <p>This method validates the payment details, checks for fraudulent activity,
 * and processes the transaction through the payment gateway. All operations
 * are performed within a database transaction for consistency.
 * 
 * @param payment the payment details including amount and method
 * @param customer the customer making the payment
 * @return a {@link PaymentResult} containing transaction ID and status
 * 
 * @throws InsufficientFundsException if the payment amount exceeds available funds
 * @throws FraudDetectedException if the transaction is flagged as fraudulent
 * @throws PaymentGatewayException if the payment gateway returns an error
 * 
 * @see PaymentValidator
 * @see FraudDetector
 * @since 2.0
 * 
 * @example
 * <pre>
 * Payment payment = new Payment(100.0, PaymentMethod.CREDIT_CARD);
 * Customer customer = customerService.findById("customer123");
 * PaymentResult result = paymentProcessor.process(payment, customer);
 * System.out.println("Transaction ID: " + result.getTransactionId());
 * </pre>
 */
public PaymentResult process(Payment payment, Customer customer)
    throws InsufficientFundsException, FraudDetectedException, PaymentGatewayException {
    // Implementation...
}
```

## README Template

Use this template for comprehensive README files:

```markdown
# Project Name

Brief description of what this project does and why it's useful.

[![Build Status](badge-url)](link)
[![Coverage](badge-url)](link)
[![License](badge-url)](link)

## Features

- 🚀 Feature 1: Description
- 📦 Feature 2: Description
- 🔒 Feature 3: Description

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Node.js >= 14.0.0
- Python >= 3.8
- PostgreSQL >= 12

### Setup

```bash
# Clone the repository
git clone https://github.com/username/project.git

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
npm run migrate

# Start development server
npm run dev
```

## Quick Start

Here's a minimal example to get you started:

```javascript
const Client = require('project-name');

const client = new Client({
  apiKey: 'your-api-key'
});

const result = await client.doSomething();
console.log(result);
```

## Usage

### Basic Example

[Detailed example with explanation]

### Advanced Usage

[Complex example showing advanced features]

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Your API key | - | Yes |
| `PORT` | Server port | 3000 | No |
| `DATABASE_URL` | Database connection | - | Yes |

### Configuration File

```json
{
  "setting1": "value1",
  "setting2": "value2"
}
```

## API Documentation

### `method(param1, param2)`

Description of what the method does.

**Parameters:**
- `param1` (string): Description
- `param2` (number): Description

**Returns:** Description of return value

**Example:**
```javascript
const result = client.method('value', 42);
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Documentation: [link]
- Issues: [link]
- Discussions: [link]
```

## Architecture Decision Records (ADR)

Template for documenting architecture decisions:

```markdown
# ADR-001: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue we're facing? What are the constraints?

## Decision
What decision are we making? What alternative did we choose?

## Consequences
What are the positive and negative consequences of this decision?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Neutral
- Consideration 1

## Alternatives Considered

### Alternative 1
- Description
- Why it was rejected

### Alternative 2
- Description
- Why it was rejected

## References
- Link to relevant discussions
- Link to related documentation
```

## Workflows

### Workflow 1: Generate API Documentation

1. **Analyze Code**: Identify all public APIs, functions, classes
2. **Extract Information**: Parameters, return types, exceptions
3. **Generate Examples**: Realistic usage examples
4. **Format Documentation**: Following language conventions
5. **Add Cross-References**: Link related functions/classes

### Workflow 2: Create README from Project

1. **Scan Project Structure**: Files, dependencies, scripts
2. **Identify Key Features**: Main functionality
3. **Extract Setup Requirements**: Dependencies, environment
4. **Find Usage Examples**: Test files, examples directory
5. **Generate Sections**: Installation, usage, configuration
6. **Add Badges**: Build status, coverage, version

### Workflow 3: Document Architecture

1. **Identify Components**: Services, modules, databases
2. **Map Relationships**: Dependencies, data flow
3. **Document Decisions**: Why things are designed this way
4. **Create Diagrams**: System architecture, data flow
5. **Add Context**: Technology choices, trade-offs

### Workflow 4: Improve Code Comments

1. **Analyze Code**: Identify complex sections
2. **Identify Documentation Gaps**: Missing or unclear docs
3. **Add Docstrings**: Functions without documentation
4. **Clarify Complex Logic**: Add explanatory comments
5. **Update Existing Docs**: Fix outdated documentation

## Best Practices

1. **Be Clear and Concise**: Use simple language, avoid jargon
2. **Include Examples**: Show, don't just tell
3. **Keep Updated**: Documentation should match current code
4. **Consider Audience**: Adjust detail level for target users
5. **Use Consistent Format**: Follow project conventions
6. **Link Related Content**: Cross-reference related documentation
7. **Test Examples**: Ensure code examples actually work
8. **Use Visual Aids**: Diagrams, screenshots when helpful
9. **Document Why**: Not just what, but why decisions were made
10. **Make Discoverable**: Clear organization and search

## Documentation Structure

```
docs/
├── README.md                 # Project overview
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── architecture/
│   ├── overview.md         # System architecture
│   ├── adr/                # Architecture decisions
│   │   ├── 001-database-choice.md
│   │   └── 002-api-design.md
│   └── diagrams/           # Architecture diagrams
├── api/
│   ├── reference.md        # Complete API reference
│   └── examples.md         # API usage examples
├── guides/
│   ├── getting-started.md  # Quick start guide
│   ├── tutorials/          # Step-by-step tutorials
│   └── how-to/             # Task-specific guides
└── reference/
    ├── configuration.md    # Configuration reference
    └── troubleshooting.md  # Common issues
```

## Tools and Formats

### Supported Formats

- **Markdown**: README, documentation files
- **reStructuredText**: Python projects (Sphinx)
- **AsciiDoc**: Complex documentation
- **OpenAPI/Swagger**: REST API documentation
- **GraphQL Schema**: GraphQL API documentation

### Documentation Generators

- **Sphinx**: Python documentation
- **JSDoc**: JavaScript documentation
- **Javadoc**: Java documentation
- **GoDoc**: Go documentation
- **Rustdoc**: Rust documentation
- **Swagger/OpenAPI**: API documentation
- **MkDocs**: Project documentation sites

## When to Use This Skill

Use this skill when:
- Creating new project documentation
- Writing or updating README files
- Documenting APIs or functions
- Creating user guides or tutorials
- Recording architecture decisions
- Improving code comments
- Generating API reference documentation
- Documenting deployment processes
- Creating troubleshooting guides
- Writing contributing guidelines

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete documentation examples across different project types and languages.

For documentation templates, see [templates/](templates/).

For automated documentation generation, see [scripts/generate_docs.py](scripts/generate_docs.py).
