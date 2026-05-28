# Pattern Template

Use this template for documenting successful code patterns, reusable solutions, or techniques that worked particularly well.

## When to Use

- Documenting a code pattern that can be reused
- Capturing a technique that solved a problem elegantly
- Recording a best practice discovered during development
- Sharing a solution approach that others should follow

## Template Structure

```markdown
# {pattern_name}

## Metadata

- **Timestamp**: {YYYY-MM-DD HH:MM:SS}
- **Project**: {project_name}
- **Category**: Pattern
- **Tags**: {comma_separated_tags}
- **Related Commit**: {commit_hash if available}

## Context

Brief description of the problem or situation that led to using this pattern.

## Pattern Description

Detailed pattern description:

- What problem does it solve?
- When should it be used?
- When should it NOT be used?

## Implementation

### Code Example

\`\`\`{language}
// Code example showing the pattern
\`\`\`

### Files Involved

- `path/to/file1.ext` - Description of its role
- `path/to/file2.ext` - Description of its role

### Key Components

List of key pattern components:

1. Component 1: description
2. Component 2: description

## Benefits

- Benefit 1
- Benefit 2
- Benefit 3

## Trade-offs

- Trade-off 1: description
- Trade-off 2: description

## Related Patterns

- Related pattern 1
- Related pattern 2

## References

- Relevant external documentation
- Blog posts or articles
```

## Field Descriptions

### Metadata
- **Timestamp**: Auto-generated current date/time
- **Project**: Auto-detected from directory or git repo
- **Category**: Always "Pattern"
- **Tags**: Relevant tags for search (technology, area, type)
- **Related Commit**: Current git commit hash if available

### Context
Brief explanation of what prompted this pattern. Keep it concise (2-3 sentences).

### Pattern Description
Core explanation of the pattern. Include:
- **Problem solved**: What issue does this address?
- **When to use**: Specific scenarios where this pattern fits
- **When NOT to use**: Anti-patterns or situations to avoid

### Implementation
Concrete code example and details:
- **Code Example**: Working code snippet showing the pattern
- **Files Involved**: List of affected files with their role
- **Key Components**: Breaking down the pattern into parts

### Benefits
Clear advantages of using this pattern (3-5 bullet points).

### Trade-offs
Honest assessment of costs or limitations (2-4 bullet points).

### Related Patterns
Links to similar or complementary patterns.

### References
External resources, documentation, or articles.
