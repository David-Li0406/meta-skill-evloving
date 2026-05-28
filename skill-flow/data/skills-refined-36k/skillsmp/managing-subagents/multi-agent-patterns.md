# Multi-Agent Patterns: Parallel and Sequential Orchestration

Advanced patterns for coordinating multiple subagents to optimize performance and resource usage.

## When to Load This File

Load when:
- User has task requiring multiple independent operations (parallel execution)
- Task involves sequential workflow with handoffs between agents (sequential chains)
- Need to optimize resource usage across multiple agent invocations
- Analyzing opportunities for multi-agent orchestration

## Identifying Multi-Agent Opportunities

### Step 1: Identify Independent Tasks

Scan current context for tasks that:
- Have no data dependencies between them
- Can execute simultaneously
- Each produce discrete outputs

**Examples of parallel opportunities:**
- Searching 3 different modules for patterns (independent searches)
- Analyzing multiple files for different criteria (independent analyses)
- Exploring separate codebases or directories (independent explorations)

**Not suitable for parallelization:**
- Tasks where second depends on first's output
- Interactive refinement based on intermediate results
- Single cohesive analysis requiring unified context

### Step 2: Design Parallel Execution

For independent tasks:

**Invocation pattern:**
- Recommend single message with multiple Task tool calls
- Each Task call receives distinct prompt
- All agents launch simultaneously
- Results return independently, synthesized after completion

**Agent selection per task:**
- Specify different thoroughness levels if using Explore agents (quick/medium/very thorough)
- Match model to each task's complexity (haiku for simple, sonnet for complex)
- Use different agent types if tasks require different tool sets

**Result synthesis guidance:**
- Specify how to combine results after all agents complete
- Identify conflicts or overlaps to reconcile
- Prioritize findings if multiple agents report related information

**Example parallel invocation:**
```
Use three Explore agents in parallel:
1. Agent 1: Search src/api/ for endpoint definitions (thoroughness: medium)
2. Agent 2: Search src/auth/ for authentication patterns (thoroughness: very thorough)
3. Agent 3: Search tests/ for API test coverage (thoroughness: quick)

After all complete, synthesize: map endpoints to auth requirements and test coverage.
```

### Step 3: Design Sequential Chains

For dependent tasks:

**Data flow mapping:**
- Identify what information passes between agents
- Specify handoff points and data formats
- Document how second agent consumes first agent's output

**Execution pattern:**
- Launch first agent with Task tool
- Wait for completion and parse results
- Formulate second agent's prompt incorporating first agent's findings
- Launch second agent
- Continue chain as needed

**Resumable agent patterns:**
- For multi-session workflows, use agent resumption with agentId
- Store intermediate results in conversation context
- Document agent transcript storage for complex chains

**Example sequential chain:**
```
1. Agent 1 (Explore): Find all database query locations → returns list of files
2. Agent 2 (general-purpose): For each file from Agent 1, analyze for SQL injection vulnerabilities → returns vulnerability report
3. Agent 3 (custom security-auditor): Review Agent 2's findings and generate fix recommendations → returns prioritized action plan
```

### Step 4: Optimize Resource Usage

Balance performance factors:

**Model selection strategy:**
- Use haiku agents for simple parallel searches (cost optimization, faster execution)
- Use sonnet for complex reasoning or code generation
- Reserve opus for maximum capability needs (rare in multi-agent patterns)
- Mix models based on each task's requirements

**Context preservation vs latency:**
- Parallel agents: Higher latency (multiple simultaneous executions) but better context preservation
- Sequential agents: Lower latency per step but builds context gradually
- Single complex agent: Lowest latency but may pollute main conversation context

**Cost optimization:**
- Prefer multiple haiku agents over single sonnet agent if tasks decomposable
- Use Explore agent with appropriate thoroughness level (don't default to "very thorough")
- Consider direct tool calls if delegation overhead exceeds benefit

**Throughput patterns:**
- Parallel agents: 3-5 simultaneous agents optimal (more adds coordination complexity)
- Sequential chains: 2-3 agents typical (longer chains increase error propagation risk)
- Hybrid: Parallel agents feeding into single synthesis agent

## Anti-Patterns

**Over-parallelization:**
- Launching 10+ agents simultaneously (coordination overhead, hard to synthesize)
- Parallelizing tasks with hidden dependencies (results inconsistent)
- Using parallel agents when direct tool calls sufficient

**Over-sequencing:**
- Creating 5+ agent chains (error propagation, context loss)
- Sequential agents where parallel execution possible (unnecessary latency)
- Passing entire transcripts between agents (context bloat)

**Resource waste:**
- Using opus for simple searches in multi-agent patterns
- "Very thorough" Explore agents when "quick" sufficient
- Complex multi-agent orchestration for tasks achievable with direct tools

## Practical Examples

### Example 1: Parallel Security Audit
```
Task: Audit Python codebase for security vulnerabilities across multiple categories

Parallel pattern (3 agents, all haiku):
1. Agent 1: Search for SQL injection patterns
2. Agent 2: Search for authentication flaws
3. Agent 3: Search for sensitive data exposure

After completion: Synthesize into unified security report with severity classification.

Benefit: 3x faster than sequential, isolated contexts prevent pattern confusion.
```

### Example 2: Sequential Refactoring Workflow
```
Task: Identify and refactor deprecated API usage

Sequential pattern:
1. Agent 1 (Explore, quick): Find all files importing deprecated API → file list
2. Agent 2 (general-purpose, sonnet): For each file, analyze usage patterns and generate refactoring plan → detailed plan per file
3. Main conversation: Review plans, then apply changes with Edit tool

Benefit: Exploration isolated from analysis, main conversation only sees refined recommendations.
```

### Example 3: Hybrid Pattern
```
Task: Compare authentication implementations across multiple services

Hybrid pattern:
1. Parallel phase (3 Explore agents, medium thoroughness):
   - Agent 1: Analyze service A authentication
   - Agent 2: Analyze service B authentication
   - Agent 3: Analyze service C authentication
2. Sequential synthesis (1 general-purpose agent, sonnet):
   - Agent 4: Compare findings from Agents 1-3, identify inconsistencies, recommend standardization

Benefit: Fast parallel discovery, unified expert comparison.
```

## Decision Framework

**Choose parallel when:**
- 3+ independent tasks identified
- No data dependencies
- Time optimization priority
- Cost acceptable (multiple simultaneous executions)

**Choose sequential when:**
- Strong data dependencies
- Each step refines previous step's output
- Complex reasoning required at each stage
- Cost optimization priority (one agent at a time)

**Choose hybrid when:**
- Initial parallel discovery phase possible
- Synthesis/comparison step benefits from unified context
- Balancing speed and cost

**Choose single agent when:**
- Task cohesive and not decomposable
- Coordination overhead exceeds parallelization benefit
- Direct tool calls insufficient but multi-agent overkill
