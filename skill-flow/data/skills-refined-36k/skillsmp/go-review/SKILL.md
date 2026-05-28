---
name: go-review
description: Review Go code for style, idioms, safety, and correctness. Use when reviewing Go code changes, pull requests, or auditing Go codebase quality.
allowed-tools: ["shell", "read_file", "apply_patch"]
metadata:
  short-description: Review Go code comprehensively
---

# Go Code Review

**Read these references before reviewing:**
- `references/process.md` - Review workflow and interactivity
- `references/priorities.md` - Review focus areas (safety first)
- `~/.config/agent/domain/coding/go/style.md` - Go style guidelines
- `~/.config/agent/domain/coding/go/idioms.md` - Go best practices
- `~/.config/agent/domain/coding/safety.md` - Runtime and security safety

## Instructions

Apply all guidance from references when reviewing Go code. Follow the review workflow from AGENT.md:

### Review Focus (Priority Order)

1. **Runtime safety** - nil dereferences, race conditions, panics
2. **Code correctness** - logic errors, edge cases, error handling
3. **Language idiomaticity** - Go conventions, proper use of features
4. **Runtime performance** - unnecessary allocations, inefficient patterns
5. **Code style** - Uber Go Style Guide compliance
6. **Local conventions** - Project-specific patterns

### Review Process

Per AGENT.md Code Review section:
- Be thorough, pedantic, and highly detailed
- Discuss each discrete point of feedback interactively
- Order feedback from most to least critical
- Prove issues empirically when possible (via tests, lint, etc.)
- Qualify confidence level for issues that can't be proven
- Pause after each issue to ask user what they'd like to do

### Common Go Review Points

- Error handling: proper wrapping, meaningful messages
- Concurrency: race conditions, proper mutex usage, channel patterns
- Resource cleanup: defers, context cancellation
- Testing: table-driven tests, edge cases, race detector
- Performance: unnecessary allocations, slice capacity

## Arguments

Target files/packages: ${ARGUMENTS}
