---
name: review
description: General code review for staged changes or specified files. Use when reviewing pull requests, commits, or code changes across any language.
allowed-tools: ["shell", "read_file", "apply_patch"]
metadata:
  short-description: Review code changes comprehensively
---

# Code Review

**Read these references:**
- `~/.config/agent/domain/review/process.md` - Review workflow
- `~/.config/agent/domain/review/priorities.md` - Review focus areas

## Instructions

Review staged changes (or specified files/diff) in this priority order:

**Note:** When *receiving* review feedback, use the `review-reception` skill instead of this one.

### Review Focus (Priority Order)

1. **Security issues**
   - Injection vulnerabilities (SQL, command, XSS)
   - Secrets exposure (hardcoded keys, tokens)
   - Authentication/authorization bypasses
   - Insecure cryptography, weak randomness

2. **Runtime safety**
   - Nil/null pointer dereferences
   - Race conditions, data races
   - Resource leaks (file handles, connections, memory)
   - Buffer overflows, out-of-bounds access

3. **Code correctness**
   - Logic errors, incorrect algorithms
   - Edge cases not handled
   - Error handling: all errors checked and wrapped
   - State management issues

4. **Language idiomaticity**
   - Go: Uber Go Style Guide, effective Go patterns
   - Rust: ownership patterns, lifetime management
   - Python: PEP 8, pythonic idioms
   - Follow language-specific best practices

5. **Performance**
   - Unnecessary allocations (especially in hot paths)
   - Inefficient algorithms (O(n²) where O(n) possible)
   - Repeated expensive operations
   - Missing caching opportunities

6. **Test coverage**
   - Missing tests for new functionality
   - Untested edge cases
   - Insufficient error case testing

### Review Process

Per AGENT.md Code Review:
- **Be thorough and pedantic** - catch every issue
- **Present interactively** - discuss each issue separately
- **Order by severity** - most critical first
- **Offer fixes** - for each issue, offer to make the change
- **Prove when possible** - run tests/lint to demonstrate issues

## Arguments

Target: ${ARGUMENTS:-staged changes}
