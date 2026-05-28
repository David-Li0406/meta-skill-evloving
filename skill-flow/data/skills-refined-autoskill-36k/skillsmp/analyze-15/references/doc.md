# Documentation Analysis Reference

## Analysis Criteria

Check documentation against actual code. Verify claims before marking as incorrect.

### Outdated Information

- Does not match current code behavior
- References removed features or APIs
- Uses deprecated patterns or syntax

### Incorrect Content

- Factually wrong statements
- Wrong API signatures or parameters
- Incorrect behavior descriptions
- Security-related misinformation

### Missing Documentation

- Undocumented public APIs
- Missing feature documentation
- No setup/installation instructions
- Missing configuration options

### Broken References

- Dead links (internal and external)
- Invalid file paths
- References to non-existent sections

### Inconsistencies

- Contradictory information across files
- Different explanations for same concept
- Version mismatches

### Incomplete Examples

- Non-working code samples
- Examples missing required imports
- Outdated syntax in examples

## Verification Process

1. Compare API documentation with actual implementations
2. Check if documented features exist
3. Verify code examples compile/run
4. Ensure types match documented signatures
5. Consider documentation may be ahead of code (planned features)

## Severity Guidelines

- **Critical**: Wrong or misleading - will confuse/mislead users, security misinformation
- **High**: Outdated or incomplete - significant gaps, missing important sections
- **Medium**: Moderate issues - outdated examples, unclear explanations
- **Low**: Minor improvements - typos, grammar, organization suggestions

## Notes

Include in the `notes` field when relevant:

- Code reference: the source file that contradicts the documentation
- Additional files affected by the same issue
- Whether documentation might be ahead of code (planned feature)
- Correct information that should replace the incorrect content
