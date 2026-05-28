# Complexity Scoring Reference

## Overview

Complexity scoring (0-100) determines the optimal agent coordination pattern for a given request. The score combines three factors: token estimate, domain diversity, and structural complexity.

## Scoring Formula

```
Total Score = Token Points + Domain Points + Structural Points
```

Maximum: 100 points

## Scoring Components

### 1. Token-Based Scoring (Max 40 points)

Estimates request size and context requirements:

| Token Estimate | Points | Rationale |
|----------------|--------|-----------|
| > 50,000       | 40     | Very large context, complex multi-domain task |
| 30,000-50,000  | 30     | Large context, benefits from specialization |
| 10,000-30,000  | 20     | Moderate context, may need coordination |
| 5,000-10,000   | 10     | Small context, usually single-agent |
| < 5,000        | 0-5    | Minimal context, simple task |

**How it's calculated**:
```javascript
const baseTokens = text.length / 4;  // Rough approximation

// Adjust for complexity indicators
if (hasCodeBlocks) multiplier += 0.3;
if (hasMultipleSentences > 5) multiplier += 0.2;
if (hasLists > 3) multiplier += 0.1;

estimatedTokens = baseTokens * multiplier;
```

### 2. Domain Diversity (Max 30 points)

Multiple domains suggest need for specialized agents:

| Domains Detected | Points | Coordination Pattern |
|------------------|--------|---------------------|
| 3+               | 30     | Parallel or hierarchical |
| 2                | 20     | Sequential or parallel |
| 1                | 10     | Single or sequential |
| 0                | 0      | Single (general) |

**Domains**:
- **Security**: vulnerability, auth*, compliance, owasp, xss, injection
- **Performance**: optimize, slow, bottleneck, latency, cache, scaling
- **Testing**: test, coverage, jest, pytest, tdd, unit, integration
- **Review**: review, quality, refactor, clean, maintainability
- **Architecture**: architecture, design, pattern, microservices
- **Debugging**: bug, error, fix, debug, crash, exception

### 3. Structural Complexity (Max 30 points)

Task structure indicates coordination needs:

| Indicator | Points | Example Keywords |
|-----------|--------|------------------|
| Multi-step workflow | 10 | "first", "then", "after", "next", "finally" |
| Validation required | 10 | "review", "check", "validate", "verify", "audit" |
| Parallel work viable | 10 | "and", "both", "all", "comprehensive" + multiple domains |

**Maximum**: 30 points (all three indicators present)

## Score Interpretation

### 0-29: Simple Task → Single Agent

**Characteristics**:
- Focused, single-domain request
- Minimal context required
- Clear, straightforward objective
- No coordination needed

**Examples**:
- "Fix typo in README.md" (Score: 12)
- "Add console.log for debugging" (Score: 15)
- "Update version number in package.json" (Score: 8)

**Recommended**: Single agent (general-purpose or domain-specific)

### 30-49: Moderate Task → Sequential

**Characteristics**:
- 1-2 domains with clear dependencies
- Moderate context
- Multi-step workflow (generate → validate)
- Benefits from specialization

**Examples**:
- "Implement API endpoint and add unit tests" (Score: 42)
- "Generate documentation and review for accuracy" (Score: 38)
- "Fix bug and verify with tests" (Score: 35)

**Recommended**: Sequential pattern (2 agents in pipeline)

### 50-69: Complex Task → Parallel

**Characteristics**:
- 2-3 independent domains
- Significant context
- Comprehensive analysis needed
- No strict dependencies between domains

**Examples**:
- "Review PR for security and performance issues" (Score: 58)
- "Audit authentication for vulnerabilities and test coverage" (Score: 62)
- "Comprehensive code review: quality, security, tests" (Score: 68)

**Recommended**: Parallel pattern (2-3 specialists simultaneously)

### 70-100: Very Complex → Hierarchical

**Characteristics**:
- 3+ domains requiring coordination
- Large context (30K+ tokens)
- Complex decomposition needed
- Multi-phase workflow with dependencies

**Examples**:
- "Design and implement OAuth2 with security audit and comprehensive testing" (Score: 85)
- "Full-stack feature: architecture, implementation, security review, performance optimization, test coverage" (Score: 92)
- "Complete refactoring with validation at each phase" (Score: 78)

**Recommended**: Hierarchical coordination (supervisor orchestrates 3-5 specialists)

## Calibration Examples

### Example 1: Simple Task

**Request**: "Add a TODO comment to the authentication function"

**Analysis**:
- **Tokens**: ~1,500 (0 points)
- **Domains**: None (0 points)
- **Structure**: Simple, no multi-step (0 points)
- **Score**: 0

**Pattern**: Single (general-purpose)

### Example 2: Lower Moderate

**Request**: "Create user registration endpoint and add input validation"

**Analysis**:
- **Tokens**: ~6,000 (10 points)
- **Domains**: 1 (architecture) (10 points)
- **Structure**: Multi-step ("create and add") (10 points)
- **Score**: 30

**Pattern**: Sequential (general-purpose → code-reviewer)

### Example 3: Upper Moderate

**Request**: "Implement password reset flow with comprehensive security review"

**Analysis**:
- **Tokens**: ~12,000 (20 points)
- **Domains**: 2 (architecture, security) (20 points)
- **Structure**: Multi-step + validation (20 points)
- **Score**: 60

**Pattern**: Sequential (general-purpose → security-auditor)
*Could use parallel if domains are truly independent*

### Example 4: Complex

**Request**: "Comprehensive audit of authentication module including security vulnerabilities, performance bottlenecks, and test coverage gaps"

**Analysis**:
- **Tokens**: ~18,000 (20 points)
- **Domains**: 3 (security, performance, testing) (30 points)
- **Structure**: Validation + parallel ("including") (20 points)
- **Score**: 70

**Pattern**: Parallel (security-auditor + performance-engineer + test-automator) → aggregator

### Example 5: Very Complex

**Request**: "Design and implement OAuth2 authentication system with JWT tokens, including: architecture design, implementation with best practices, comprehensive security audit covering OWASP top 10, performance optimization for high-concurrency scenarios, and full test coverage with integration and edge case tests"

**Analysis**:
- **Tokens**: ~45,000 (30 points)
- **Domains**: 4+ (architecture, security, performance, testing) (30 points)
- **Structure**: Multi-step + validation + parallel (30 points)
- **Score**: 90

**Pattern**: Hierarchical (coordinator orchestrates: architect-review → general-purpose → parallel(security-auditor, performance-engineer, test-automator) → synthesis)

## Boundary Cases

### Borderline Scores (28-32, 48-52, 68-72)

When score is near a threshold:
1. Consider context and user intent
2. Default to simpler pattern (avoid over-engineering)
3. Provide alternatives in analysis
4. Let user choose if ambiguous

**Example**: Score 31 (just over "simple" threshold)
- Could use single agent if request is straightforward
- Or sequential if clear two-phase workflow exists
- **Recommendation**: Offer both, explain trade-offs

### Keyword Inflation

Some requests use complex language but are simple tasks:

**Request**: "Comprehensive review and optimization of this one-line function"

**Raw Score**: 42 (keywords: "comprehensive", "review", "optimization")
**Actual Complexity**: 15 (it's a one-line function!)

**Solution**: Apply common sense override in task-analyzer agent
- Note inflated score in `reasoning`
- Recommend simpler pattern
- Explain why keywords are misleading

### Context Matters

Same request, different scores based on codebase:

**Request**: "Add authentication"

- **Greenfield project**: Score 75 (design everything from scratch)
- **Existing pattern**: Score 35 (follow established pattern)

**Solution**: Task-analyzer considers context and provides reasoning

## Continuous Calibration

The scoring system improves over time through:

1. **Metrics tracking**: Log score vs actual complexity
2. **User feedback**: Approval/rejection rates by score
3. **Token accuracy**: Estimated vs actual token usage
4. **Pattern effectiveness**: Success rate of pattern recommendations

This data feeds back into threshold tuning and keyword weighting.

## Summary

| Score Range | Pattern | Agents | Use Case |
|-------------|---------|--------|----------|
| 0-29 | Single | 1 | Simple, focused tasks |
| 30-49 | Sequential | 2 | Moderate, dependent workflow |
| 50-69 | Parallel | 2-3 | Complex, independent analyses |
| 70-100 | Hierarchical | 3-5 | Very complex, coordinated workflow |

Scoring ensures optimal agent utilization: simple tasks use minimal tokens, complex tasks get comprehensive multi-specialist coverage.
