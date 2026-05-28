---
name: rust-project-technical-review
description: |
  Comprehensive methodology for conducting technical reviews of Rust projects.
  Use when: (1) reviewing unfamiliar Rust codebases, (2) conducting project
  health assessments, (3) evaluating code quality and architecture, (4) preparing
  project audits or due diligence. Covers structure analysis, code quality
  assessment, security review, and documentation evaluation.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# Rust Project Technical Review Methodology

## Problem
Reviewing large Rust projects requires a systematic approach to thoroughly assess code quality, architecture, security, and maintainability without missing critical aspects.

## Context / Trigger Conditions
- Need to review an unfamiliar Rust codebase
- Conducting project health assessment
- Evaluating open-source project for adoption
- Preparing technical audit or due diligence
- Onboarding to a new Rust project as technical lead

## Solution

### Phase 1: Project Structure Analysis

1. **Initial exploration**:
   ```bash
   ls -la                    # Check root directory structure
   cat README.md            # Understand project purpose
   cat Cargo.toml          # Review workspace structure and dependencies
   ```

2. **Codebase metrics**:
   ```bash
   find . -name "*.rs" -type f | xargs wc -l | tail -1  # Total lines of code
   find . -name "*.md" -type f | wc -l                  # Documentation count
   ```

3. **Architecture assessment**:
   - Review crate organization in Cargo.toml workspace
   - Examine lib.rs files for module structure
   - Identify separation of concerns between crates

### Phase 2: Code Quality Assessment

1. **Compilation check**:
   ```bash
   cargo check --workspace   # Verify clean compilation
   ```

2. **Linting analysis**:
   ```bash
   cargo clippy --workspace  # Identify code quality issues
   ```

3. **Test execution** (if possible):
   ```bash
   cargo test --workspace    # Run test suite
   ```

4. **Dependency analysis**:
   - Review Cargo.toml dependencies for:
     - Version consistency across workspace
     - Security-sensitive crates
     - Maintenance status of dependencies

### Phase 3: Architecture & Design Review

1. **Domain modeling**: Examine domain module organization
2. **Async patterns**: Check for proper tokio/async usage
3. **Error handling**: Verify consistent error handling patterns
4. **Security practices**: Look for:
   - Input validation
   - Secure credential storage
   - Proper use of cryptographic libraries

### Phase 4: Documentation Assessment

1. **User documentation**: README, CONTRIBUTING, ROADMAP
2. **Code documentation**: Inline docs, examples
3. **Security documentation**: SECURITY.md, vulnerability reporting
4. **Development docs**: Build instructions, architecture diagrams

### Phase 5: Report Generation

Structure findings into comprehensive report:

```markdown
# Project Review

## Overview
- Project purpose and scope
- Key statistics (LOC, documentation, etc.)
- License and governance

## Architecture & Design
- Strengths in design patterns
- Technical implementation details
- Code organization assessment

## Code Quality Assessment
- Compilation status
- Clippy warnings analysis
- Test coverage evaluation
- Dependency review

## Strengths
- Technical achievements
- Best practices followed
- Security considerations

## Areas of Concern
- Potential risks or issues
- Technical debt indicators
- Scalability considerations

## Recommendations
- Immediate actions
- Strategic suggestions
- Long-term improvements

## Conclusion
- Overall assessment
- Viability evaluation
- Final recommendation
```

## Verification

A successful review should produce:
- Compile-time verification of code health
- Quantitative metrics (LOC, warning count, documentation coverage)
- Qualitative assessment of architecture and practices
- Actionable recommendations for improvement
- Clear overall evaluation with supporting evidence

## Example

For the Demiarch project review:

```bash
# Structure analysis
ls -la ~/projects/demiarch/
cat README.md
cat Cargo.toml

# Quality checks
cargo check --workspace    # ✅ Clean compilation
cargo clippy --workspace   # 14 minor warnings identified

# Metrics collection
find crates -name "*.rs" | xargs wc -l    # 52,648 lines core code
find . -name "*.md" | wc -l                # 804 documentation files

# Analysis revealed:
# - Well-structured 4-crate workspace
# - Advanced features (GraphRAG, Russian Doll agents)
# - Strong security practices
# - Comprehensive documentation
# - Minor code quality improvements needed
```

## Notes

### Best Practices
- Always run automated tools (check, clippy, test) first
- Document quantitative metrics for objective assessment
- Balance technical depth with readability for stakeholders
- Include both immediate fixes and strategic recommendations
- Consider project maturity when setting expectations

### Limitations
- Cannot assess runtime behavior without execution
- Limited insight into performance without profiling
- Security assessment is surface-level without specialized tools
- Code quality depends on clippy rule configuration

### Adaptations for Different Project Types
- **Libraries**: Focus more on API design and documentation
- **Applications**: Emphasize security and deployment considerations
- **Early-stage**: Be more forgiving of incomplete features
- **Production**: Stricter standards for testing and documentation

## References
- [Rust Code Review Guidelines](https://github.com/rust-lang/rfcs/blob/master/text/1574-more-api-documentation-conventions.md)
- [Cargo Workspace Documentation](https://doc.rust-lang.org/cargo/reference/workspaces.html)
- [Clippy Lint Categories](https://rust-lang.github.io/rust-clippy/stable/index.html)