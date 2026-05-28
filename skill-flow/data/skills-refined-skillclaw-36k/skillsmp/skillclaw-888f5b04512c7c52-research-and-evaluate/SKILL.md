---
name: research-and-evaluate
description: Use this skill when researching best practices, evaluating technologies, or comparing approaches to make informed decisions based on evidence and authoritative sources.
---

# Skill body

## Research

Systematic investigation → evidence-based analysis → authoritative recommendations.

### When to Use

- Technology evaluation and comparison
- Documentation discovery and troubleshooting
- Best practices and industry standards research
- Implementation guidance with authoritative sources

**NOT for:** quick lookups, well-known patterns, time-critical debugging without investigation phase.

### Phases

Track with a task management system. Phases advance only, never regress.

| Phase               | Trigger               | activeForm                     |
|---------------------|----------------------|--------------------------------|
| Analyze Request     | Session start        | "Analyzing research request"   |
| Discover Sources     | Criteria defined     | "Discovering sources"          |
| Gather Information   | Sources identified    | "Gathering information"        |
| Synthesize Findings  | Information gathered  | "Synthesizing findings"        |
| Compile Report       | Synthesis complete    | "Compiling report"             |

### Workflow

- **Start:** Create "Analyze Request" as `in_progress`.
- **Transition:** Mark current `completed`, add next `in_progress`.
- **Simple queries:** Skip directly to "Gather Information" if unambiguous.
- **Gaps during synthesis:** Add new "Gather Information" task.
- **Early termination:** Skip to "Compile Report" with caveats.

### Methodology

Five-phase systematic approach:

**1. Question Phase** — Define scope
- Decision to be made?
- Evaluation parameters? (performance, maintainability, security, adoption)
- Constraints? (timeline, expertise, infrastructure)

**2. Discovery Phase** — Multi-source retrieval

| Use Case          | Primary         | Secondary       | Tertiary         |
|-------------------|-----------------|------------------|-------------------|
| Official docs     | context7        | octocode         | firecrawl         |
| Troubleshooting    | octocode issues | firecrawl community | context7 guides   |
| Code examples      | octocode repos  | firecrawl tutorials | context7 examples |
| Technology eval    | Parallel all    | Cross-reference  | Validate          |

**3. Evaluation Phase** — Analyze against criteria

| Criterion     | Metrics                                   |
|---------------|-------------------------------------------|
| Performance   | Benchmarks, latency, throughput, memory   |
| Maintainability| Code complexity, docs quality, community activity |
| Security      | CVEs, audits, compliance                   |
| Adoption      | Downloads, production usage, industry patterns |

**4. Comparison Phase** — Systematic tradeoff analysis

For each option, analyze based on the defined criteria and metrics to make informed recommendations.