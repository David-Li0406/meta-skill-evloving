# Agent Registry Reference

## Overview

The agent registry (`scripts/lib/agent-registry.json`) is the central database of available agents, their capabilities, token costs, and domain expertise. It enables intelligent agent selection based on detected task domains.

## Registry Structure

```json
{
  "agents": [
    {
      "id": "agent-name",
      "capabilities": ["keyword1", "keyword2"],
      "avg_tokens": 5000,
      "confidence": 0.95,
      "description": "Human-readable description"
    }
  ],
  "domain_keywords": {
    "domain_name": ["keyword1", "keyword2", ...]
  },
  "metadata": {
    "version": "1.0.0",
    "token_multiplier": 15,
    "quality_improvement": 0.90
  }
}
```

## Available Agents

### 1. general-purpose

**Capabilities**: `research`, `exploration`, `multi-step`, `code-search`
**Average Tokens**: 8,000
**Confidence**: 0.90

**When to use**:
- Broad, multi-domain tasks
- Research and exploration
- Tasks that don't fit specific domains
- Coordination and general implementation

**Examples**:
- "Explore the codebase to understand authentication flow"
- "Implement user registration endpoint"
- "Research best practices for API design"

### 2. code-reviewer

**Capabilities**: `code-quality`, `security`, `patterns`, `best-practices`, `vulnerabilities`
**Average Tokens**: 5,000
**Confidence**: 0.95

**When to use**:
- Code quality analysis
- Pattern and best practice validation
- General security review
- Maintainability assessment

**Examples**:
- "Review this PR for code quality issues"
- "Check if code follows project patterns"
- "Identify technical debt in this module"

### 3. security-auditor

**Capabilities**: `security`, `compliance`, `vulnerabilities`, `authentication`, `authorization`, `owasp`
**Average Tokens**: 6,000
**Confidence**: 0.95

**When to use**:
- Security vulnerability scanning
- Authentication/authorization review
- OWASP top 10 compliance
- Security best practices validation

**Examples**:
- "Audit authentication module for vulnerabilities"
- "Check for SQL injection risks"
- "Review OAuth2 implementation for security issues"

### 4. test-automator

**Capabilities**: `testing`, `coverage`, `tdd`, `unit-tests`, `integration-tests`, `quality`
**Average Tokens**: 4,000
**Confidence**: 0.90

**When to use**:
- Test suite creation
- Coverage analysis
- TDD workflows
- Quality assurance

**Examples**:
- "Create comprehensive test suite for user service"
- "Analyze test coverage and identify gaps"
- "Implement TDD workflow for new feature"

### 5. performance-engineer

**Capabilities**: `optimization`, `profiling`, `scalability`, `performance`, `bottlenecks`, `latency`
**Average Tokens**: 5,500
**Confidence**: 0.85

**When to use**:
- Performance optimization
- Bottleneck identification
- Scalability analysis
- Latency reduction

**Examples**:
- "Profile API endpoints and optimize slow queries"
- "Identify performance bottlenecks in data processing"
- "Review caching strategy for scalability"

### 6. architect-review

**Capabilities**: `architecture`, `design`, `patterns`, `scalability`, `system-design`, `ddd`
**Average Tokens**: 7,000
**Confidence**: 0.90

**When to use**:
- Architecture design
- System design review
- Pattern selection
- Scalability planning

**Examples**:
- "Design microservices architecture for e-commerce platform"
- "Review system design for scalability issues"
- "Recommend architectural patterns for event-driven system"

### 7. debugger

**Capabilities**: `debugging`, `errors`, `troubleshooting`, `stack-traces`, `root-cause`
**Average Tokens**: 4,500
**Confidence**: 0.85

**When to use**:
- Error investigation
- Root cause analysis
- Troubleshooting failures
- Stack trace analysis

**Examples**:
- "Debug authentication failure in production"
- "Investigate race condition causing intermittent errors"
- "Analyze stack trace and identify root cause"

### 8. tdd-orchestrator

**Capabilities**: `tdd`, `testing`, `red-green-refactor`, `test-driven`, `quality`
**Average Tokens**: 6,000
**Confidence**: 0.88

**When to use**:
- Test-driven development workflows
- Red-Green-Refactor orchestration
- Quality-first development

**Examples**:
- "Implement feature using TDD approach"
- "Coordinate test-first development workflow"
- "Guide red-green-refactor cycle"

## Domain Keyword Mapping

### Security Domain

**Keywords**: `security`, `vulnerability`, `auth`, `authentication`, `authorization`, `compliance`, `owasp`, `xss`, `sql-injection`, `csrf`

**Primary Agent**: `security-auditor`
**Backup Agent**: `code-reviewer`

### Performance Domain

**Keywords**: `optimize`, `slow`, `bottleneck`, `latency`, `performance`, `speed`, `cache`, `scaling`

**Primary Agent**: `performance-engineer`
**Backup Agent**: `architect-review`

### Testing Domain

**Keywords**: `test`, `coverage`, `jest`, `pytest`, `tdd`, `unit`, `integration`, `e2e`

**Primary Agent**: `test-automator`
**Backup Agent**: `tdd-orchestrator`

### Review Domain

**Keywords**: `review`, `quality`, `refactor`, `clean`, `maintainability`, `code-smell`

**Primary Agent**: `code-reviewer`
**Backup Agent**: `general-purpose`

### Architecture Domain

**Keywords**: `architecture`, `design`, `pattern`, `microservices`, `scalability`, `system-design`, `ddd`

**Primary Agent**: `architect-review`
**Backup Agent**: `general-purpose`

### Debugging Domain

**Keywords**: `bug`, `error`, `fix`, `debug`, `crash`, `exception`, `stack-trace`

**Primary Agent**: `debugger`
**Backup Agent**: `general-purpose`

## Agent Selection Algorithm

### Step 1: Detect Domains

Scan request for domain keywords:

```javascript
const domains = [];
const text = request.toLowerCase();

for (const [domain, keywords] of Object.entries(domain_keywords)) {
  const matches = keywords.filter(kw => text.includes(kw));
  if (matches.length > 0) {
    domains.push({
      name: domain,
      confidence: matches.length / keywords.length,
      matchedKeywords: matches
    });
  }
}
```

### Step 2: Match Agents to Domains

For each detected domain, select primary agent:

```javascript
const selectedAgents = [];

domains.forEach(domain => {
  const agent = agents.find(a =>
    a.capabilities.some(cap =>
      domain_keywords[domain.name].includes(cap)
    )
  );

  if (agent && !selectedAgents.includes(agent.id)) {
    selectedAgents.push(agent.id);
  }
});
```

### Step 3: Apply Pattern Limits

Limit agents based on coordination pattern:

| Pattern | Max Agents | Rationale |
|---------|-----------|-----------|
| Single | 1 | One agent handles everything |
| Sequential | 2 | Pipeline (A → B) |
| Parallel | 3 | Independent specialists |
| Hierarchical | 5 | Coordinated by supervisor |

### Step 4: Prioritize by Confidence

If more agents than limit, select highest confidence:

```javascript
agents
  .sort((a, b) => b.confidence - a.confidence)
  .slice(0, pattern_limit);
```

## Cost Estimation

### Token Cost Formula

```javascript
const estimateCost = (agents, baseTokens) => {
  const avgTokensPerAgent = agents.reduce((sum, id) => {
    const agent = registry.agents.find(a => a.id === id);
    return sum + (agent?.avg_tokens || 5000);
  }, 0) / agents.length;

  const singleCost = baseTokens + 5000; // Base + overhead
  const multiCost = baseTokens + (avgTokensPerAgent * agents.length);

  return {
    single: singleCost,
    multi: multiCost,
    multiplier: Math.round(multiCost / singleCost) + 'x'
  };
};
```

### Research-Based Metrics

From empirical analysis:
- **Token Multiplier**: 15× (on average for complex multi-agent)
- **Quality Improvement**: 90% better results
- **Optimal Context**: 30K+ tokens

## Extending the Registry

### Adding New Agents

1. Add agent definition to `agents` array:

```json
{
  "id": "new-agent-name",
  "capabilities": ["capability1", "capability2"],
  "avg_tokens": 5000,
  "confidence": 0.85,
  "description": "What this agent does"
}
```

2. Update domain keywords if new domain:

```json
"domain_keywords": {
  "new_domain": ["keyword1", "keyword2"]
}
```

3. Update selection algorithm if custom logic needed

### Tracking Actual Performance

Collect metrics to improve estimates:

```javascript
{
  "agent_id": "security-auditor",
  "executions": 150,
  "avg_tokens_actual": 6200,
  "avg_tokens_estimated": 6000,
  "success_rate": 0.96,
  "user_satisfaction": 0.92
}
```

Use this data to:
- Tune `avg_tokens` estimates
- Adjust `confidence` scores
- Refine capability mappings
- Improve keyword detection

## Best Practices

### DO:
✅ Use primary agent for their specialty domain
✅ Fall back to general-purpose for multi-domain tasks
✅ Limit agents to avoid diminishing returns
✅ Track actual vs estimated tokens
✅ Update registry based on performance data

### DON'T:
❌ Invoke >3 agents for parallel pattern (diminishing returns)
❌ Use specialists outside their domain (lower confidence)
❌ Ignore token estimates (budget control)
❌ Skip domain detection (suboptimal agent selection)

## Example Selection Sessions

### Example 1: Security + Performance

**Request**: "Review authentication for security vulnerabilities and performance issues"

**Domains Detected**: `security`, `performance`
**Agents Selected**: `security-auditor`, `performance-engineer`
**Pattern**: Parallel (2 agents)
**Cost**: Base (15K) + (6K + 5.5K) = 26.5K tokens

### Example 2: Complex Multi-Domain

**Request**: "Comprehensive review: security, performance, testing, code quality"

**Domains Detected**: `security`, `performance`, `testing`, `review`
**Agents Selected**: `security-auditor`, `performance-engineer`, `test-automator`
**Pattern**: Parallel (limited to 3)
**Cost**: Base (20K) + (6K + 5.5K + 4K) = 35.5K tokens
**Note**: `code-reviewer` excluded due to 3-agent limit

### Example 3: Simple Task

**Request**: "Fix typo in README"

**Domains Detected**: None
**Agents Selected**: `general-purpose`
**Pattern**: Single
**Cost**: Base (2K) + 5K = 7K tokens

---

The agent registry is the foundation for intelligent orchestration, ensuring the right specialists are matched to the right tasks with accurate cost estimates.
