---
name: skill-template
description: Use this skill when you need a structured template for creating skills, including setup, implementation, and best practices.
---

# Skill Template

## Overview

This skill template provides a comprehensive structure for documenting skills, including key capabilities, prerequisites, instructions, examples, and best practices.

## Prerequisites

Before using this skill, ensure you have:

### Required
- Requirement 1 (e.g., Python 3.8+)
- Requirement 2 (e.g., Node.js 14+)

### Optional
- Optional tool 1
- Optional tool 2

## When to use this skill

- **Scenario 1**: Describe when to use this skill.
- **Scenario 2**: Another use case with context.
- **Scenario 3**: Additional context for usage.

## Quick Start

Get started quickly with this basic example:

```bash
# Setup
./scripts/setup.sh

# Basic usage
python scripts/main.py --config config.yaml

# Verify
./scripts/verify.sh
```

## Instructions

### Step 1: Environment Preparation
Prepare your environment:

```bash
# Create directory structure
mkdir -p project/{src,tests,config}

# Initialize configuration
cp templates/config.yaml project/config/
```

### Step 2: Configuration
Edit the configuration file:

```yaml
# config.yaml
setting1: value1
setting2: value2
options:
  option1: true
  option2: false
```

### Step 3: Core Implementation
Implement the main functionality:

```language
# Detailed implementation example
class MainImplementation:
    def __init__(self, config):
        self.config = config
        self.state = {}

    def process(self, input_data):
        """
        Process input data according to configuration.

        Args:
            input_data: Data to process

        Returns:
            Processed result

        Raises:
            ValueError: If input is invalid
        """
        # Validation
        if not self.validate(input_data):
            raise ValueError("Invalid input")

        # Processing
        result = self.transform(input_data)

        # Post-processing
        return self.finalize(result)

    def validate(self, data):
        # Validation logic
```

## Best Practices

1. **Practice 1**: Explain why this is important.
   - Sub-point about implementation.
   - Common mistake to avoid.

2. **Practice 2**: Another key principle.
   - How to implement correctly.
   - When to apply this principle.

## Common Pitfalls

- **Pitfall 1**: What to avoid and why.
- **Pitfall 2**: Another common mistake.

## Troubleshooting

### Issue 1: [Problem Description]
**Symptoms**: What you might observe.  
**Cause**: Why this happens.  
**Solution**: How to fix it.

### Issue 2: [Another Problem]
**Symptoms**: Observable behavior.  
**Cause**: Root cause.  
**Solution**: Resolution steps.

## References

- [Official Documentation](https://example.com/docs)
- [Related Tutorial](https://example.com/tutorial)
- [Best Practices Guide](https://example.com/guide)

## Additional Resources

- [Internal Reference](REFERENCE.md) (if exists)
- [More Examples](EXAMPLES.md) (if exists)