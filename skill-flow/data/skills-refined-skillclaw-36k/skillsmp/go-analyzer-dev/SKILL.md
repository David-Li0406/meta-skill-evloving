---
name: go-analyzer-dev
description: Develop, maintain, and audit Go analyzers (go/analysis). Use when creating/updating analyzers, suggested fixes, analysistest golden files, or integration analyzer harnesses.
allowed-tools: ["shell", "apply_patch", "read_file", "write_file", "update_plan"]
metadata:
  short-description: Go analyzer development workflow
---

# Go Analyzer Development

**Read these reference files before proceeding:**
- `references/style.md` - Go code style guidelines
- `references/idioms.md` - Go conventions and best practices
- `references/concurrency.md` - Go thread safety and race conditions
- `references/testing.md` - Go test practices
- `references/tooling.md` - Go tooling commands
- `references/organization.md` - Go code structure and package design
- `references/performance.md` - Go optimization guidance
- `~/.config/agent/core/behavior.md` - Critical thinking and evidence requirements
- `~/.config/agent/core/methodology.md` - 5-phase problem-solving framework
- `~/.config/agent/core/efficiency.md` - Parallelization and throughput
- `~/.config/agent/core/task-management.md` - TODO discipline
- `~/.config/agent/core/principles.md` - Engineering principles
- `~/.config/agent/core/communication.md` - Communication standards
- `~/.config/agent/domain/coding/workflow.md` - Universal coding workflow
- `~/.config/agent/domain/coding/quality.md` - Quality priorities
- `~/.config/agent/domain/coding/safety.md` - Runtime and security safety
- `~/.config/agent/domain/testing/unit.md` - Unit testing strategy
- `~/.config/agent/domain/testing/coverage.md` - Coverage expectations

## Instructions

Apply all guidance from the reference files listed above.

Use this workflow when building or modifying analyzers:

1. **Analyzer Contract**
   - Define purpose, scope, and explicit non-goals.
   - Specify diagnostics, messages, and when fixes are allowed.
   - Document generated-file handling and nolint handling.

2. **AST/Types Strategy**
   - Enumerate the AST node kinds you will visit.
   - State required TypesInfo behavior and guard nil/partial info.
   - Prefer inspector with narrow node filters.

3. **Fix Safety Rules**
   - Only emit fixes when correctness is provable from local context.
   - Preserve comments/formatting; avoid whole-decl rewrites unless necessary.
   - Ensure edits are minimal, scoped, and stable with token boundaries.

4. **Scenario Matrix**
   - Maintain a scenario/edge-case matrix per analyzer.
   - Mark supported/unsupported cases and expected behavior.
   - Map each matrix row to a test (positive or negative).

5. **Testing Strategy**
   - Use analysistest for diagnostics and RunWithSuggestedFixes for fixes.
   - Update golden files to reflect expected fixes.
   - Add tests for error-prone contexts (selectors, generics, comments, blank identifiers, control-flow variations).

6. **Integration & Performance**
   - Ensure analyzers run together without panics or conflicts.
   - Avoid O(n^2) traversals where possible; reuse computed maps.

7. **Risk & Unknowns**
   - Explicitly list policy decisions needed (e.g., generics, selector derefs).
   - Document residual risks and the rationale for unsupported scenarios.

**Deliverables (as applicable):**
- Updated analyzer contract (doc or comments)
- Scenario/edge-case matrix with test mapping
- Tests (diagnostics + suggested-fix golden files)
- Integration test coverage confirmation
- Evidence notes for Verified vs Unverified behavior

## Arguments

Target: ${ARGUMENTS}
