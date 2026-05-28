---
name: research
description: "Use when performing deep technical research, evaluating libraries, comparing options, or investigating APIs. Covers documentation lookup, issue investigation, version compatibility analysis, and synthesis of findings into actionable recommendations."
---

# Research Skill

Procedural knowledge for conducting comprehensive technical research using documentation tools, search APIs, and GitHub resources.

## Core Research Tools

| Tool                   | Purpose                            | When to Use                                     |
| ---------------------- | ---------------------------------- | ----------------------------------------------- |
| `docs-context7/*`      | Official library documentation     | API reference, usage examples, best practices   |
| `perplexity/search`    | Quick factual lookups              | Version info, simple comparisons, definitions   |
| `perplexity/reason`    | Complex analysis and reasoning     | Trade-offs, architecture decisions, debugging   |
| `perplexity/deep`      | Comprehensive research reports     | Major decisions, unfamiliar domains, deep dives |
| `github/search_issues` | Bug reports and workarounds        | Known issues, community solutions, edge cases   |
| `github/search_code`   | Real-world implementation patterns | Usage examples, integration patterns            |
| `web`                  | Blogs, tutorials, release notes    | Recent updates, tutorials, opinions             |

### Tool Selection Guide

```
IF need quick fact or version check:
    → perplexity/search

IF need to understand trade-offs or debug complex issue:
    → perplexity/reason

IF need comprehensive analysis of unfamiliar domain:
    → perplexity/deep

IF need official API reference or examples:
    → docs-context7/*

IF investigating bugs or looking for workarounds:
    → github/search_issues

IF looking for real-world usage patterns:
    → github/search_code
```

---

## Research Protocol

### Phase 1: Contextualization

**Goal**: Understand how the research topic relates to the current codebase.

1. **Search existing usage**
   - Find current implementations of the topic in codebase
   - Identify patterns, conventions, and constraints
   - Note technology stack (languages, frameworks, versions)

2. **Capture constraints**
   - Architecture patterns that must be followed
   - Dependencies that affect compatibility
   - Team conventions or standards

3. **Define scope**
   - What specific questions need answering?
   - What decisions will this research inform?
   - What are the acceptance criteria for "good enough" research?

### Phase 2: Information Gathering

**Goal**: Collect authoritative information from multiple sources.

#### Documentation Research

```javascript
// Get official docs for a library
resolve - library - id({ libraryName: "react" });
get -
  library -
  docs({
    context7CompatibleLibraryID: "/facebook/react",
    topic: "hooks",
    mode: "code", // or "info" for conceptual content
  });
```

#### Quick Search

```javascript
// Fast lookup for facts, versions, comparisons
perplexity /
  search({
    query: "React 18 vs React 19 concurrent features comparison",
  });
```

#### Deep Analysis

```javascript
// Complex reasoning about trade-offs
perplexity /
  reason({
    query:
      "Compare Redux Toolkit vs Zustand vs Jotai for large-scale React app with complex state dependencies, considering bundle size, learning curve, and TypeScript support",
  });
```

#### Comprehensive Research

```javascript
// In-depth investigation of unfamiliar territory
perplexity /
  deep({
    query:
      "WebSocket vs Server-Sent Events vs HTTP/2 push for real-time financial data streaming",
    focus_areas: [
      "latency",
      "reconnection handling",
      "browser support",
      "server scalability",
    ],
  });
```

#### GitHub Investigation

```javascript
// Find known issues and workarounds
github /
  search_issues({
    query: "memory leak useEffect cleanup",
    repo: "facebook/react",
  });

// Find real-world usage patterns
github /
  search_code({
    query: "useReducer middleware pattern",
    language: "typescript",
  });
```

### Phase 3: Synthesis

**Goal**: Transform raw findings into actionable guidance.

1. **Cross-reference sources**
   - Verify claims across multiple sources
   - Flag contradictions or outdated information
   - Note consensus vs contested findings

2. **Contextualize findings**
   - How do findings apply to our specific codebase?
   - What patterns from our stack align with recommendations?
   - What constraints eliminate certain options?

3. **Prioritize recommendations**
   - Rank options by fit for the specific use case
   - Highlight trade-offs relevant to project constraints
   - Provide clear "if X then Y" guidance

---

## Output Format Template

```markdown
## Research Summary

**Topic**: [What was researched]
**Relevance**: [How this applies to the current project]

## Key Findings

- [Finding 1 — most important discovery]
- [Finding 2 — second most important]
- [Finding 3 — third most important]
- [Additional findings as needed]

## Current Codebase Context

[How the topic relates to existing code, patterns, or dependencies]

## Options Analysis

### Option 1: [Name]

**Description**: [What this approach entails]

| Pros          | Cons             |
| ------------- | ---------------- |
| [Advantage 1] | [Disadvantage 1] |
| [Advantage 2] | [Disadvantage 2] |

**Best For**: [When to choose this option]

### Option 2: [Name]

**Description**: [What this approach entails]

| Pros          | Cons             |
| ------------- | ---------------- |
| [Advantage 1] | [Disadvantage 1] |
| [Advantage 2] | [Disadvantage 2] |

**Best For**: [When to choose this option]

## Recommendation

**Recommended Approach**: [Which option and why]

**Implementation Notes**:

- [Specific guidance for implementing in this codebase]
- [Gotchas or pitfalls to avoid]
- [Migration steps if applicable]

## Code Examples

[Relevant code snippets adapted to the current project's style]

## References

| Source                 | Type         | Date       | Notes               |
| ---------------------- | ------------ | ---------- | ------------------- |
| [URL or doc reference] | Official     | YYYY-MM-DD | [Why it's relevant] |
| [URL or doc reference] | Blog/Article | YYYY-MM-DD | [Why it's relevant] |
| [URL or doc reference] | GitHub Issue | YYYY-MM-DD | [Why it's relevant] |

## Open Questions

- [Anything that couldn't be definitively answered]
- [Areas needing further investigation or user decision]
```

---

## Research Quality Checklist

### Before Starting

- [ ] Understand the specific question or decision to inform
- [ ] Check codebase context before external research
- [ ] Identify what "good enough" research looks like

### During Research

- [ ] Use official documentation as primary source
- [ ] Verify information is current (check dates, versions)
- [ ] Cross-reference 2-3 sources for key claims
- [ ] Check GitHub issues for known problems
- [ ] Note version compatibility requirements

### Before Finalizing

- [ ] Findings are adapted to codebase context
- [ ] Recommendations are actionable, not just informational
- [ ] Uncertainties and open questions are clearly stated
- [ ] All sources are cited with dates
- [ ] Trade-offs are explicit for each option

---

## Common Research Patterns

### Pattern 1: Library Evaluation

**Scenario**: Choosing between competing libraries

```
1. Define evaluation criteria (bundle size, API ergonomics, maintenance, etc.)
2. Quick search for recent comparisons: perplexity/search
3. Check official docs for each: docs-context7
4. Search GitHub for issue patterns: github/search_issues
5. Deep analysis of trade-offs: perplexity/reason
6. Synthesize into comparison matrix
```

### Pattern 2: Bug Investigation

**Scenario**: Debugging an issue with a dependency

```
1. Search codebase for similar issues/workarounds
2. Search GitHub issues in the library repo
3. Search for error messages: perplexity/search
4. Check if fixed in newer versions: docs-context7
5. Look for workarounds in code: github/search_code
6. Document workaround or upgrade path
```

### Pattern 3: API Integration

**Scenario**: Integrating with a new external API

```
1. Get official API documentation: docs-context7 or web
2. Search for integration examples: github/search_code
3. Check for known issues/rate limits: github/search_issues
4. Research authentication patterns: perplexity/search
5. Look for SDK or client libraries
6. Document integration approach with examples
```

### Pattern 4: Architecture Decision

**Scenario**: Making a significant technical decision

```
1. Define decision criteria and constraints
2. Research current best practices: perplexity/deep
3. Check how similar projects solved it: github/search_code
4. Analyze codebase constraints and patterns
5. Model options with trade-off analysis: perplexity/reason
6. Recommend with clear rationale and migration path
```

### Pattern 5: Version Compatibility

**Scenario**: Upgrading a dependency or checking compatibility

```
1. Check current version in codebase
2. Get changelog/migration guide: docs-context7
3. Search for breaking changes: perplexity/search
4. Check GitHub issues for upgrade problems
5. Identify affected code paths in codebase
6. Document upgrade steps and risks
```

---

## Query Formulation Tips

### For perplexity/search (Quick Facts)

```
# Good: Specific, factual
"What is the minimum Node.js version required for Next.js 14?"
"React 18 automatic batching behavior changes"

# Avoid: Vague, opinion-seeking
"What's the best state management library?"
```

### For perplexity/reason (Analysis)

```
# Good: Complex trade-offs with context
"Compare Prisma vs Drizzle ORM for a TypeScript project with PostgreSQL,
considering type safety, query performance, and migration tooling"

# Avoid: Simple factual questions
"What is Prisma?"
```

### For perplexity/deep (Comprehensive)

```
# Good: Multi-faceted topics needing depth
"Authentication strategies for a multi-tenant SaaS application with
SSO requirements, considering OAuth 2.0, SAML, and JWT patterns"

# Include focus_areas for guidance:
focus_areas: ["security considerations", "implementation complexity", "scalability"]
```

### For github/search_issues

```
# Good: Specific error messages or behaviors
"ECONNRESET during long-running requests"
"useEffect cleanup not called on unmount"

# Include repo for focused results:
repo: "vercel/next.js"
```

---

## Delegation for Complex Research

For large research topics, break into focused sub-tasks:

| Sub-Task                  | Focus Area                             |
| ------------------------- | -------------------------------------- |
| Codebase Context Analysis | Existing usage, patterns, constraints  |
| Documentation Research    | Official docs, API reference, examples |
| GitHub Investigation      | Bugs, workarounds, community solutions |
| Version Compatibility     | Compatibility matrix, migration needs  |
| Research Synthesis        | Cross-reference, recommendations       |

**Handoff Pattern**: Write findings to `specs/{topic}/research-findings.md` for complex research that will inform implementation planning.

---

## Best Practices

### Source Quality

- **Prefer official docs** over blog posts for API details
- **Check dates** — technology moves fast, stale info misleads
- **Verify with code** — if possible, test claims in actual code
- **Note uncertainty** — if sources conflict, say so explicitly

### Research Efficiency

- **Start narrow, then expand** — specific questions first
- **Don't over-research** — know when "good enough" is reached
- **Batch related queries** — group similar questions together
- **Cache findings** — write to files for reuse across sessions

### Actionable Output

- **Always contextualize** — generic advice is less useful
- **Include code examples** — adapted to the current codebase style
- **Specify next steps** — what should happen after reading the research
- **Flag blockers** — what decisions or clarifications are needed

---

## Quick Reference

| Task                 | Tool                   | Query Style               |
| -------------------- | ---------------------- | ------------------------- |
| Version/fact lookup  | `perplexity/search`    | Specific, factual         |
| Trade-off analysis   | `perplexity/reason`    | Comparative, contextual   |
| Deep domain research | `perplexity/deep`      | Broad topic + focus_areas |
| API documentation    | `docs-context7`        | Library ID + topic        |
| Bug investigation    | `github/search_issues` | Error message + repo      |
| Usage patterns       | `github/search_code`   | Pattern + language        |
| Tutorials/guides     | `web`                  | URL fetch                 |
