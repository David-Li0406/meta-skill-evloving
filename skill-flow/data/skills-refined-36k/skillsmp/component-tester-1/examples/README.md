# Test Examples

This directory contains example projects and expected outputs for component testing.

## Directory Structure

```
examples/
├── README.md (this file)
├── test-project/           # Sample project for code generation tests
├── expected-code-outputs/  # Reference outputs for code-with-codex
└── expected-design-outputs/# Reference outputs for ux-design-gemini
```

## Usage

### Test Project

The `test-project/` directory contains a minimal project structure for testing:
- Used by integration tests
- Contains sample code for refactoring tests
- Provides fixtures for test scenarios

### Expected Outputs

Compare test execution outputs against these references:

**Code Outputs** (`expected-code-outputs/`):
- Simple function implementations
- Class definitions
- Multi-file project structures

**Design Outputs** (`expected-design-outputs/`):
- Component wireframes
- Design system specifications
- Responsive layout guides

## Creating New Examples

To add new test examples:

1. Create subdirectory: `mkdir examples/my-new-example`
2. Add sample files with clear naming
3. Document purpose in subdirectory README
4. Reference in test scenarios

## Validation

Examples are used by validation scripts:
- `scripts/validate-code-output.py`
- `scripts/validate-design-output.py`

These scripts compare test outputs against expected examples.
