# Agent Templates

Example prompts for spawning specialized investigation agents with clear roles, deliverables, and dynamic writeTodo workflows.

## Template Structure

Each agent prompt should include:
1. **ROLE**: Specialist perspective (e.g., "API Capabilities Analyst")
2. **OBJECTIVE**: Specific investigation goal
3. **CONTEXT**: Background information relevant to investigation
4. **DYNAMIC WRITETODO APPROACH**: Instruction for emergent task creation
5. **INVESTIGATION QUESTIONS**: 5-7 specific questions to answer
6. **DELIVERABLES**: Structured output format
7. **WORKSPACE**: Temporary directory for artifacts

## Example: API Capabilities Agent

```markdown
**ROLE**: API Capabilities Analyst

**OBJECTIVE**: Determine if platform provides queryable API endpoints for serving data without download.

**CONTEXT**:
- Data file: Parquet format (~20 MB)
- Published to: GitHub Releases
- Target users: Developers/engineers
- Requirement: High-efficiency API endpoints

**DYNAMIC WRITETODO APPROACH**:
1. Start with ONE initial writeTodo
2. Complete → Analyze findings → CREATE next writeTodo(s) based on discoveries
3. Mark completed → Execute next → Repeat until questions answered
4. Let writeTodos emerge from findings naturally

**INVESTIGATION QUESTIONS**:
1. Does platform provide API to query asset contents directly?
2. Are there HTTP range request capabilities?
3. What are rate limits and constraints?
4. Can we leverage alternative services (CDN, proxy)?
5. What's implementation complexity (1-10 scale)?
6. What are performance characteristics?
7. Are there cost implications?

**DELIVERABLES**:
Return structured report with:
- API endpoints discovered (if any)
- Rate limits and constraints
- Implementation complexity rating
- Performance characteristics
- Code examples (if applicable)
- Recommendation: Viability for use case

**WORKSPACE**: Use `/tmp/api-investigation/` for test files
```

## Example: Performance Analyst Agent

```markdown
**ROLE**: Performance Analyst

**OBJECTIVE**: Empirically validate performance characteristics and measure latency.

**CONTEXT**:
- Technology: DuckDB with HTTP reads
- File size: ~20 MB Parquet
- Expected queries: Filtered (WHERE clauses), column pruning (SELECT specific)

**DYNAMIC WRITETODO APPROACH**:
1. Start with ONE performance measurement task
2. Complete → Analyze results → CREATE next test based on findings
3. Iterate until comprehensive benchmark complete

**INVESTIGATION QUESTIONS**:
1. What's cold-start query time (first request)?
2. What's warm-cache query time (subsequent requests)?
3. Does technology download full file or use range requests?
4. How does filtering affect performance (full scan vs WHERE)?
5. How does column selection affect performance (SELECT * vs specific)?
6. Are there network dependency impacts?
7. What's the local vs remote performance delta?

**DELIVERABLES**:
- Performance benchmark table (query type, time, bytes transferred)
- Working code examples
- Trade-offs analysis (remote vs local)
- Recommendation with confidence level

**WORKSPACE**: `/tmp/performance-validation/` for benchmark scripts
```

## Example: Documentation Quality Agent

```markdown
**ROLE**: Technical Documentation Analyst

**OBJECTIVE**: Assess documentation quality and identify gaps for developer onboarding.

**CONTEXT**:
- Target user: Developers/engineers
- Success criteria: "Good documentation" (easy to find and use)
- Current state: Comprehensive but potentially hard to navigate

**DYNAMIC WRITETODO APPROACH**:
1. Start with ONE documentation analysis task
2. Complete → Identify gaps → CREATE next task to assess specific gap
3. Iterate until complete quality assessment done

**INVESTIGATION QUESTIONS**:
1. Is there Quick Start section with copy-paste examples?
2. Are prerequisites clearly documented?
3. Do examples cover primary use cases?
4. Are there placeholder URLs or TODOs?
5. Is troubleshooting guidance present?
6. Are performance tips documented?
7. Missing: Any critical workflow examples?
8. Overall rating: X/10 with justification?

**DELIVERABLES**:
- Gap analysis (what's missing?)
- Effectiveness rating (1-10) with justification
- Specific recommendations (prioritized)
- Example improvements (concrete suggestions)

**WORKSPACE**: `/tmp/docs-assessment/` for analysis notes
```

## Example: Feasibility Analysis Agent

```markdown
**ROLE**: Solution Feasibility Engineer

**OBJECTIVE**: Determine technical feasibility and prototype minimal implementation.

**CONTEXT**:
- Proposed solution: CLI tool with uvx installation
- Alternative: Extend existing CLI vs standalone
- Tech stack: Python, uv/uvx, relevant libraries

**DYNAMIC WRITETODO APPROACH**:
1. Start with ONE design/prototype task
2. Complete → Test → CREATE next task based on what works/fails
3. Build incrementally until proof-of-concept complete

**INVESTIGATION QUESTIONS**:
1. What would interface look like (CLI arguments)?
2. Should tool auto-download or use remote queries?
3. How to handle caching (avoid redundant downloads)?
4. What's cold-start time (including install)?
5. Can it be installed via uvx (PEP 723)?
6. Should we integrate with existing tool or standalone?
7. What's implementation effort (hours)?

**DELIVERABLES**:
- Design proposal (interface structure)
- Prototype implementation (minimal working version)
- Performance measurements (install, first query, cached)
- Recommendation: Build vs alternative approach

**WORKSPACE**: `/tmp/feasibility-prototype/` for proof-of-concept
```

## Agent Orchestration Patterns

### Parallel Execution (Recommended)

Spawn all agents in single message using multiple Task tool calls:
```
I'll spawn 4 parallel agents to investigate this question from different perspectives.
[Task tool call 1: API agent]
[Task tool call 2: Performance agent]
[Task tool call 3: Documentation agent]
[Task tool call 4: Feasibility agent]
```

### Sequential Execution (When Dependencies Exist)

Agent 2 depends on Agent 1 findings:
```
I'll start with the API investigation, then use those findings to guide performance testing.
[Task tool call: API agent]
... wait for results ...
[Task tool call: Performance agent using API findings]
```

### Typical Agent Count

- **4 agents**: Balanced coverage (API, Performance, Documentation, Feasibility)
- **5-6 agents**: Deep dive (add Security, Cost, Maintainability specialists)
- **2-3 agents**: Quick investigation (focused on critical dimensions only)

## Agent Role Library

Common specialist roles for crypto/trading data investigations:

1. **API Capabilities Analyst** - Platform API evaluation
2. **Performance Analyst** - Benchmarking and optimization
3. **Documentation Analyst** - Quality assessment, gap identification
4. **Feasibility Engineer** - Prototyping, proof-of-concept
5. **Security Analyst** - Threat modeling, credential management
6. **Cost Analyst** - Pricing, rate limits, resource consumption
7. **Integration Specialist** - Third-party service integration
8. **Data Quality Analyst** - Schema validation, coverage assessment
9. **User Experience Analyst** - Developer friction, onboarding time
10. **Infrastructure Analyst** - Deployment, monitoring, ops requirements
