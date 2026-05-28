---
name: jikime-workflow-parallel
description: Parallel subagent execution patterns for multi-perspective analysis, adversarial review, and coordinated task delegation
version: 1.0.0
tags: ["workflow", "parallel", "subagent", "adversarial", "multi-perspective"]
triggers:
  keywords: ["parallel", "adversarial", "perspective", "concurrent", "병렬 실행", "병렬 분석"]
  phases: ["run"]
  agents: ["manager-strategy", "manager-quality"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~4500
user-invocable: false
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Parallel Subagent Execution Patterns

## Quick Reference (30 seconds)

Parallel Subagent Execution - Coordinated multi-agent workflows for comprehensive analysis, adversarial review, and high-throughput task processing.

Core Capabilities:
- Multi-Perspective Analysis: 4 orthogonal perspectives in parallel (Architecture, Security, Performance, Testing)
- Adversarial Review: 3 subagents for false positive filtering, missing issue detection, and context validation
- Dynamic Subagent Prompts: Template-based consistent subagent creation
- TodoWrite Parallel Mode: Multiple in_progress tasks for tracking parallel work
- TaskOutput Collection: Structured result aggregation and synthesis

Key Patterns:
- Single Message, Multiple Tasks: Launch all parallel subagents in ONE tool call
- Background Execution: Use `run_in_background: true` for long-running analyses
- Synthesis Phase: Collect results and generate cross-perspective insights

When to Use:
- Multi-angle code analysis (security + performance + architecture)
- Quality verification with adversarial validation
- Large-scale codebase exploration
- Parallel feature implementation across domains

Quick Commands:
- Multi-perspective: /jikime:perspective @src/
- Adversarial verify: /jikime:verify pre-pr
- Parallel explore: Use Task tool with multiple subagents

---

## Implementation Guide (5 minutes)

### Core Principle: Single Message, Multiple Tasks

The fundamental pattern for parallel execution is launching multiple Task tools in a SINGLE message. This ensures true parallelism.

```markdown
## CRITICAL: Parallel Execution

To launch subagents in parallel, you MUST:
1. Send ONE message containing MULTIPLE Task tool calls
2. Use `run_in_background: true` for each subagent
3. Collect results with TaskOutput after all complete
```

Wrong (Sequential):
```
Message 1: Task("Analyze security")
Message 2: Task("Analyze performance")
```

Correct (Parallel):
```
Single Message:
  - Task("Analyze security", run_in_background: true)
  - Task("Analyze performance", run_in_background: true)
  - Task("Analyze architecture", run_in_background: true)
```

### Pattern 1: Multi-Perspective Analysis

Launch 4 perspective subagents simultaneously:

```yaml
Perspectives:
  Architecture:
    focus: [structure, coupling, SOLID, DRY, layers]
    output: Structure score, coupling metrics, recommendations

  Security:
    focus: [OWASP Top 10, input validation, auth patterns, secrets]
    output: Risk score, vulnerability findings, remediation steps

  Performance:
    focus: [complexity O(n), N+1 queries, caching, memory]
    output: Efficiency score, bottleneck identification, optimizations

  Testing:
    focus: [coverage, edge cases, mocking, E2E paths]
    output: Coverage score, uncovered areas, test recommendations
```

Execution Template:

```markdown
## Launch 4 Perspective Subagents (SINGLE MESSAGE)

Task 1 - Architecture:
  prompt: "You are an Architecture Analyst. Analyze [target] for:
    - Module structure and boundaries
    - Coupling and cohesion metrics
    - SOLID principle compliance
    - DRY violations
    Output: JSON with structure_score, findings[], recommendations[]"
  subagent_type: general-purpose
  run_in_background: true

Task 2 - Security:
  prompt: "You are a Security Analyst. Analyze [target] for:
    - OWASP Top 10 vulnerabilities
    - Input validation gaps
    - Authentication/authorization issues
    - Secret exposure risks
    Output: JSON with risk_score, vulnerabilities[], remediations[]"
  subagent_type: general-purpose
  run_in_background: true

Task 3 - Performance:
  prompt: "You are a Performance Analyst. Analyze [target] for:
    - Algorithm complexity (Big O)
    - Database query efficiency (N+1)
    - Caching opportunities
    - Memory usage patterns
    Output: JSON with efficiency_score, bottlenecks[], optimizations[]"
  subagent_type: general-purpose
  run_in_background: true

Task 4 - Testing:
  prompt: "You are a Testing Analyst. Analyze [target] for:
    - Test coverage gaps
    - Missing edge cases
    - Mocking strategy quality
    - E2E critical path coverage
    Output: JSON with coverage_score, uncovered[], test_recommendations[]"
  subagent_type: general-purpose
  run_in_background: true
```

### Pattern 2: Adversarial Review

3-subagent adversarial validation for quality verification:

```yaml
Adversarial Subagents:
  False Positive Filter:
    purpose: Review findings, identify false positives
    context: [test fixtures, generated code, intentional patterns]
    output: Filtered findings with confidence scores

  Missing Issues Finder:
    purpose: Fresh perspective analysis
    focus: [edge cases, race conditions, error handling, null safety]
    output: Additional issues not caught by standard tools

  Context Validator:
    purpose: Compare findings against original intent
    checks: [pattern consistency, breaking changes, fix alignment]
    output: Contextual assessment with recommendations
```

Execution Template:

```markdown
## Launch 3 Adversarial Subagents (SINGLE MESSAGE)

Task 1 - False Positive Filter:
  prompt: "Review all findings from Phase 1-7:
    [Insert findings here]

    Identify FALSE POSITIVES:
    - Intentional patterns (test fixtures, generated code)
    - Third-party code not under our control
    - Documented technical debt with tracking

    Output: JSON with filtered_findings[], false_positives[], confidence_scores{}"
  subagent_type: general-purpose
  run_in_background: true

Task 2 - Missing Issues Finder:
  prompt: "Analyze code with FRESH perspective:
    [Insert code context here]

    Look for MISSED issues:
    - Race conditions in async code
    - Null/undefined safety gaps
    - Error handling edge cases
    - Boundary condition violations

    Output: JSON with missing_issues[], severity_scores{}, locations[]"
  subagent_type: general-purpose
  run_in_background: true

Task 3 - Context Validator:
  prompt: "Compare findings against original intent:
    Original requirements: [Insert requirements]
    Proposed changes: [Insert changes]
    Findings: [Insert findings]

    Validate:
    - Changes align with requirements
    - No unintended breaking changes
    - Fixes follow codebase patterns

    Output: JSON with alignment_check, breaking_changes[], pattern_violations[]"
  subagent_type: general-purpose
  run_in_background: true
```

### Pattern 3: TodoWrite Parallel Mode

Track multiple in-progress tasks for parallel work visibility:

```markdown
## TodoWrite for Parallel Tracking

When launching parallel subagents, update TodoWrite to show:
- All subagent tasks as "in_progress" simultaneously
- Clear identification of what each subagent is doing

Example:
[
  {"content": "Architecture analysis", "status": "in_progress", "activeForm": "Analyzing architecture"},
  {"content": "Security analysis", "status": "in_progress", "activeForm": "Analyzing security"},
  {"content": "Performance analysis", "status": "in_progress", "activeForm": "Analyzing performance"},
  {"content": "Testing analysis", "status": "in_progress", "activeForm": "Analyzing testing"}
]

Note: This is an exception to the "one in_progress at a time" rule
specifically for parallel subagent execution patterns.
```

### Pattern 4: Result Synthesis

Collect and synthesize results from parallel subagents:

```markdown
## Synthesis Phase

After TaskOutput collection from all subagents:

1. Cross-Reference Findings:
   - Security issue + Untested = CRITICAL priority
   - Performance bottleneck + Architecture coupling = HIGH priority
   - Single-perspective finding = MEDIUM priority

2. Generate Correlation Matrix:
   | Finding | Arch | Sec | Perf | Test | Priority |
   |---------|------|-----|------|------|----------|
   | SQL injection | - | ✓ | - | ✓ (untested) | CRITICAL |
   | N+1 query | ✓ | - | ✓ | - | HIGH |

3. Prioritized Action Items:
   - Immediate: Multi-perspective critical issues
   - Short-term: High priority single-perspective
   - Backlog: Medium priority improvements
```

---

## Advanced Implementation (10+ minutes)

### Dynamic Prompt Templates

Create reusable prompt templates for consistent subagent behavior:

```markdown
## Analyst Prompt Template

You are a [ROLE] Analyst specializing in [DOMAIN].

TARGET: [target_path]
DEPTH: [quick|standard|deep]
CONTEXT: [additional_context]

ANALYSIS REQUIREMENTS:
1. [requirement_1]
2. [requirement_2]
3. [requirement_3]

OUTPUT FORMAT (JSON):
{
  "score": number (0-100),
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "location": "file:line",
      "description": "string",
      "recommendation": "string"
    }
  ],
  "summary": "string",
  "metrics": { ... }
}
```

### Depth-Based Configuration

Adjust parallel execution based on analysis depth:

```yaml
Depth Profiles:
  quick:
    max_subagents: 2
    analysis_scope: surface-level
    timeout: 60s
    focus: obvious issues only

  standard:
    max_subagents: 4
    analysis_scope: balanced
    timeout: 180s
    focus: common patterns + edge cases

  deep:
    max_subagents: 6
    analysis_scope: comprehensive
    timeout: 300s
    focus: all patterns + remediation code
```

### Error Handling in Parallel Execution

Handle subagent failures gracefully:

```markdown
## Error Recovery Pattern

1. Individual Failure:
   - Mark that perspective as "partial"
   - Continue synthesis with available results
   - Note limitation in final report

2. Multiple Failures:
   - If >50% fail, retry with single-threaded execution
   - Report infrastructure issues to user

3. Timeout Handling:
   - Use TaskOutput with timeout parameter
   - Partial results are better than no results
   - Include timeout notice in synthesis
```

---

## Integration Patterns

### With /jikime:verify

```markdown
Verify Command Integration:

1. Standard Phases (1-7): Direct tool execution
2. Phase 8 (Adversarial): Parallel subagent launch
   - 3 adversarial subagents (single message)
   - TaskOutput collection
   - Synthesis into final report
3. Output: Adjusted findings with adversarial validation
```

### With /jikime:perspective

```markdown
Perspective Command Integration:

1. Parse arguments (target, focus, depth)
2. Launch 4 perspective subagents (single message)
3. TaskOutput collection for each
4. Synthesis phase:
   - Cross-perspective correlation
   - Priority matrix generation
   - Action item consolidation
5. Output: Unified multi-perspective report
```

### With manager-strategy

```markdown
Strategy Agent Integration:

For complex planning tasks:
1. Decompose into domain areas
2. Launch parallel exploration subagents
3. Synthesize findings into strategy
4. Validate with adversarial review
```

---

## Works Well With

Commands:
- /jikime:perspective - Multi-perspective parallel analysis
- /jikime:verify - Adversarial review in pre-pr/full modes
- /jikime:analyze - Comprehensive codebase analysis

Skills:
- jikime-foundation-core - Parallel execution principles
- jikime-workflow-testing - Test perspective patterns
- jikime-workflow-spec - SPEC-driven parallel development

Agents:
- manager-strategy - Strategic parallel decomposition
- manager-quality - Quality validation with adversarial review
- Explore - Parallel codebase exploration

---

## Quick Decision Guide

| Scenario | Pattern | Subagents |
|----------|---------|-----------|
| Code review | Multi-Perspective | 4 (Arch, Sec, Perf, Test) |
| Pre-PR verification | Adversarial Review | 3 (Filter, Finder, Validator) |
| Large refactoring | Domain Parallel | N (one per domain) |
| Security audit | Focused + Adversarial | 2 + 3 |
| Performance tuning | Perf + Architecture | 2 |

---

## Resources

Module Deep Dives:
- [Parallel Patterns](modules/parallel-patterns.md) - Detailed execution patterns and templates
- [Synthesis Strategies](modules/synthesis-strategies.md) - Result aggregation and correlation methods

Related Commands:
- `/jikime:perspective` - Multi-perspective analysis command
- `/jikime:verify` - Verification with adversarial review

Related Skills:
- `jikime-foundation-core` - Parallel execution principles
- `jikime-workflow-testing` - Test perspective patterns
- `jikime-workflow-spec` - SPEC-driven parallel development

---

Version: 1.0.0
Last Updated: 2026-01-25
Integration Status: Complete - Multi-Perspective + Adversarial Review patterns
