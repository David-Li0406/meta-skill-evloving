# Coordination Patterns Reference

## Overview

Four proven coordination patterns optimize multi-agent execution based on task complexity, domain dependencies, and desired outcomes. Each pattern has specific use cases, trade-offs, and implementation strategies.

## Research Foundation

**Findings** (from empirical studies):
- Multi-agent achieves **90% better results** on complex tasks
- Token consumption is **15× higher** on average
- Optimal at **30K+ token contexts**
- Token usage explains **80% of performance variance**

**Implication**: Pattern selection must balance quality improvement against token cost.

---

## Pattern 1: Single Agent

### When to Use

- **Complexity**: 0-29 (simple tasks)
- **Domains**: 0-1 (focused scope)
- **Dependencies**: None
- **Token Budget**: Limited or task is straightforward

### Characteristics

✅ **Token Efficient**: Minimal overhead (1× multiplier)
✅ **Fast**: Single agent execution
✅ **Simple**: No coordination needed

❌ **Limited Expertise**: One perspective only
❌ **No Validation**: No specialist review

### Implementation

```javascript
// Use general-purpose or domain-specific agent
Task({
  subagent_type: "general-purpose", // or domain specialist
  description: "Execute user request",
  prompt: userRequest
});
```

### Examples

**Example 1**: "Fix typo in README.md"
- **Agent**: general-purpose
- **Cost**: ~7K tokens
- **Rationale**: Simple edit, no expertise needed

**Example 2**: "Debug authentication error"
- **Agent**: debugger
- **Cost**: ~9K tokens
- **Rationale**: Single domain (debugging), specialist appropriate

### Trade-offs

| Aspect | Single Agent | Multi-Agent Alternative |
|--------|--------------|------------------------|
| Quality | Good for simple tasks | 90% better on complex |
| Speed | Fastest | Slower (multiple phases) |
| Cost | 1× (baseline) | 4-15× |
| Coverage | Single perspective | Multi-specialist |

---

## Pattern 2: Sequential (Pipeline)

### When to Use

- **Complexity**: 30-49 (moderate)
- **Domains**: 1-2 with clear dependencies
- **Dependencies**: Output of Agent A feeds into Agent B
- **Token Budget**: Moderate (4-6× multiplier)

### Characteristics

✅ **Dependency Handling**: A → B → C pipeline
✅ **Validation**: Later agents validate earlier work
✅ **Incremental Quality**: Each phase improves output

❌ **Slower**: Sequential execution (not parallel)
❌ **Higher Cost**: Multiple agents in series

### Implementation

```javascript
// Phase 1: Generator
const result1 = await Task({
  subagent_type: "general-purpose",
  description: "Generate implementation",
  prompt: userRequest
});

// Phase 2: Reviewer (with context from Phase 1)
const result2 = await Task({
  subagent_type: "code-reviewer",
  description: "Review and validate",
  prompt: `${userRequest}\n\nReview this implementation:\n${result1}`
});

// Return final result
return result2;
```

### Workflow Patterns

#### Pattern 2a: Generate → Validate

**Use Case**: Implementation with quality check

```
User Request
    ↓
Generate (general-purpose)
    ↓
Validate (code-reviewer or specialist)
    ↓
Final Result
```

**Example**: "Implement API endpoint and validate security"

#### Pattern 2b: Analyze → Fix

**Use Case**: Problem diagnosis and resolution

```
User Request
    ↓
Analyze (debugger or performance-engineer)
    ↓
Implement Fix (general-purpose)
    ↓
Final Result
```

**Example**: "Find and fix performance bottleneck"

#### Pattern 2c: Design → Implement

**Use Case**: Architecture-first development

```
User Request
    ↓
Design (architect-review)
    ↓
Implement (general-purpose)
    ↓
Final Result
```

**Example**: "Design and implement microservice"

### Examples

**Example 1**: "Create user registration endpoint with security review"

- **Phase 1**: general-purpose implements endpoint (~8K tokens)
- **Phase 2**: security-auditor reviews implementation (~6K tokens)
- **Total**: ~14K base + ~14K agents = **28K tokens (4×)**
- **Benefit**: Security validation catches vulnerabilities

**Example 2**: "Optimize database queries and verify improvement"

- **Phase 1**: performance-engineer optimizes queries (~5.5K tokens)
- **Phase 2**: general-purpose verifies with benchmarks (~5K tokens)
- **Total**: ~10K base + ~10.5K agents = **20.5K tokens (2×)**
- **Benefit**: Empirical verification of optimization

### Trade-offs

| Aspect | Sequential | Single | Parallel |
|--------|-----------|--------|----------|
| Dependency Handling | ✅ Excellent | ❌ N/A | ❌ No dependencies |
| Quality | High (validated) | Moderate | Highest (multi-specialist) |
| Speed | Moderate (serial) | Fastest | Fast (parallel) |
| Cost | 2-6× | 1× | 8-15× |

---

## Pattern 3: Parallel (Independent Specialists)

### When to Use

- **Complexity**: 50-69 (complex)
- **Domains**: 2-3 independent domains
- **Dependencies**: None (analyses are independent)
- **Token Budget**: Large (8-15× multiplier)

### Characteristics

✅ **Comprehensive Coverage**: Multiple specialist perspectives
✅ **Fast**: Agents execute simultaneously
✅ **High Quality**: 90% improvement on complex tasks

❌ **Expensive**: 8-15× token cost
❌ **Requires Synthesis**: Need aggregator to combine results

### Implementation

```javascript
// Launch all agents in parallel (same message, multiple Task calls)
const [result1, result2, result3] = await Promise.all([
  Task({
    subagent_type: "security-auditor",
    description: "Security audit",
    prompt: userRequest
  }),
  Task({
    subagent_type: "performance-engineer",
    description: "Performance analysis",
    prompt: userRequest
  }),
  Task({
    subagent_type: "test-automator",
    description: "Test coverage review",
    prompt: userRequest
  })
]);

// Aggregate results
const finalResult = await Task({
  subagent_type: "multi-agent:aggregator",
  description: "Synthesize parallel results",
  prompt: `Combine findings from:\n
    Security: ${result1}\n
    Performance: ${result2}\n
    Testing: ${result3}`
});

return finalResult;
```

### Workflow Pattern

```
        User Request
             |
      ┌──────┼──────┐
      ↓      ↓      ↓
  Agent A  Agent B  Agent C
  (Security) (Perf) (Test)
      |      |      |
      └──────┼──────┘
             ↓
       Aggregator
             ↓
      Unified Report
```

### Examples

**Example 1**: "Comprehensive review of authentication module"

**Agents**:
- `security-auditor`: Find vulnerabilities (~6K tokens)
- `performance-engineer`: Identify bottlenecks (~5.5K tokens)
- `test-automator`: Analyze coverage (~4K tokens)
- `aggregator`: Synthesize findings (~3K tokens)

**Total**: ~18K base + ~18.5K agents = **36.5K tokens (2×)**
**Note**: Lower multiplier due to moderate base context

**Example 2**: "Full audit of payment processing system"

**Agents**:
- `security-auditor`: PCI compliance, vulnerabilities
- `code-reviewer`: Code quality, patterns
- `test-automator`: Edge cases, coverage

**Total**: ~35K base + ~15K agents = **50K tokens (1.4×)**
**Benefit**: Catches issues across all dimensions (security, quality, testing)

### Aggregation Strategy

The `aggregator` agent:

1. **Collects** all specialist outputs
2. **Identifies** consensus (multiple agents flag same issue)
3. **Detects** conflicts (trade-offs between domains)
4. **Prioritizes** by impact and effort
5. **Integrates** into unified action plan

### Trade-offs

| Aspect | Parallel | Sequential | Single |
|--------|----------|-----------|--------|
| Coverage | Comprehensive | Focused | Limited |
| Speed | Fast (simultaneous) | Moderate | Fastest |
| Quality | Highest (90%) | High | Moderate |
| Cost | 8-15× | 2-6× | 1× |

---

## Pattern 4: Hierarchical (Coordinated Supervision)

### When to Use

- **Complexity**: 70-100 (very complex)
- **Domains**: 3+ with coordination needs
- **Dependencies**: Mixed (some serial, some parallel)
- **Token Budget**: Very large (10-20× multiplier)

### Characteristics

✅ **Handles Complexity**: Multi-phase workflows with dependencies
✅ **Quality Gates**: Validation at each phase
✅ **Adaptive**: Coordinator adjusts based on results

❌ **Most Expensive**: Highest token cost
❌ **Slower**: Multiple sequential phases
❌ **Complex**: Requires sophisticated orchestration

### Implementation

```javascript
// Invoke coordinator agent
const result = await Task({
  subagent_type: "multi-agent:coordinator",
  description: "Coordinate complex multi-agent workflow",
  prompt: `${userRequest}\n
    Required specialists: architect-review, general-purpose,
    security-auditor, test-automator\n
    Expected workflow: Design → Implement → Validate (parallel) → Synthesize`
});

return result;
```

The **coordinator** internally handles:
- Task decomposition
- Specialist delegation
- Dependency management
- Progress tracking
- Result synthesis

### Workflow Pattern

```
                User Request
                     ↓
              Coordinator (decompose)
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    Phase 1:     Phase 2:     Phase 3:
    Design       Implement    Validate (parallel)
        ↓            ↓            ↓
  Architect    General      ┌─────┼─────┐
   -review     -purpose     ↓     ↓     ↓
                          Sec   Perf  Test
        └────────────┼────────────┘
                     ↓
           Coordinator (synthesize)
                     ↓
              Unified Report
```

### Examples

**Example 1**: "Design and implement OAuth2 authentication with comprehensive validation"

**Phases**:
1. **Design**: architect-review creates architecture (~7K tokens)
2. **Implement**: general-purpose builds based on design (~10K tokens)
3. **Validate** (parallel):
   - security-auditor: OWASP compliance (~6K tokens)
   - test-automator: Test coverage (~4K tokens)
4. **Synthesize**: coordinator creates action plan (~5K tokens)

**Total**: ~45K base + ~32K agents + ~5K coordinator = **82K tokens (1.8×)**

**Example 2**: "Complete refactoring of payment system with validation at each phase"

**Phases**:
1. **Analyze**: performance-engineer + architect-review identify issues
2. **Plan**: coordinator creates refactoring roadmap
3. **Implement**: general-purpose executes refactoring in phases
4. **Validate**: security-auditor + test-automator verify each phase
5. **Finalize**: coordinator produces final report

**Total**: ~60K base + ~45K agents = **105K tokens (1.75×)**

### Coordination Strategies

#### Strategy 1: Sequential Phases with Parallel Validation

Best for: Design → Implement → Review workflows

```
Design (architect)
    ↓
Implement (general-purpose)
    ↓
Validate (parallel)
├─ Security audit
├─ Performance review
└─ Test coverage
    ↓
Synthesize (coordinator)
```

#### Strategy 2: Iterative with Feedback Loops

Best for: Complex problem-solving with unknowns

```
Analyze (specialist)
    ↓
Propose Solution (general-purpose)
    ↓
Validate (reviewer) ──── feedback ───┐
    ↓                                  │
If issues: Refine ────────────────────┘
If OK: Finalize
```

#### Strategy 3: Divide-and-Conquer

Best for: Large-scale refactoring or multi-component work

```
Decompose (coordinator)
    ↓
┌────────┼────────┐
Component A  B    C (parallel implementation)
    └────────┼────────┘
         ↓
    Integration (coordinator)
         ↓
    Validation (specialists)
```

### Trade-offs

| Aspect | Hierarchical | Parallel | Sequential | Single |
|--------|-------------|----------|-----------|--------|
| Complexity Handling | Excellent | Limited | Moderate | Poor |
| Quality | Highest | Highest | High | Moderate |
| Coordination | Sophisticated | Simple (aggregator) | None | None |
| Cost | 10-20× | 8-15× | 2-6× | 1× |
| Speed | Slowest | Fast | Moderate | Fastest |

---

## Pattern Selection Matrix

| Complexity Score | Domains | Dependencies | Budget | Recommended Pattern |
|-----------------|---------|--------------|--------|-------------------|
| 0-29 | 0-1 | None | Limited | **Single** |
| 30-49 | 1-2 | Clear pipeline | Moderate | **Sequential** |
| 50-69 | 2-3 | Independent | Large | **Parallel** |
| 70-100 | 3+ | Mixed | Very large | **Hierarchical** |

## Cost-Benefit Analysis

### When Multi-Agent is Worth It

✅ **Complexity > 50**: Quality improvement (90%) justifies cost
✅ **Multiple domains**: Specialists catch domain-specific issues
✅ **High stakes**: Critical features, security, production systems
✅ **Large context (30K+ tokens)**: Already high token usage
✅ **User explicitly wants comprehensive review**

### When Single Agent is Better

✅ **Complexity < 30**: Simple tasks don't benefit from multi-agent
✅ **Budget constrained**: Token efficiency matters
✅ **Time sensitive**: Speed over thoroughness
✅ **Single domain**: Specialist not needed
✅ **Low stakes**: Non-critical code, internal tools

## Pattern Evolution

Tasks can evolve between patterns:

### Example Evolution

**Request**: "Implement user authentication"

**Initial (greenfield)**:
- Complexity: 75 (needs design)
- Pattern: Hierarchical
- Phases: Design → Implement → Validate

**After architecture exists**:
- Complexity: 35 (follow pattern)
- Pattern: Sequential
- Phases: Implement → Review

**Bug fix later**:
- Complexity: 20 (specific fix)
- Pattern: Single
- Agent: debugger

**Key Insight**: Same feature, different patterns over time.

---

## Summary

| Pattern | Complexity | Cost | Speed | Use Case |
|---------|-----------|------|-------|----------|
| **Single** | 0-29 | 1× | Fastest | Simple, focused tasks |
| **Sequential** | 30-49 | 2-6× | Moderate | Generate → validate pipelines |
| **Parallel** | 50-69 | 8-15× | Fast | Independent multi-domain analysis |
| **Hierarchical** | 70-100 | 10-20× | Slowest | Complex coordinated workflows |

Choose the **simplest pattern** that achieves quality requirements within budget constraints. When in doubt, prefer simpler over more complex.
