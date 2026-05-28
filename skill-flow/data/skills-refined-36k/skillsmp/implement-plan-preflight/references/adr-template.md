**Skill**: [Implement Plan Preflight](../SKILL.md)

# ADR Template (MADR 4.0)

Complete template for Architecture Decision Records following MADR 4.0 standards.

## YAML Frontmatter (MANDATORY)

Every ADR MUST begin with this frontmatter:

```yaml
---
status: proposed | accepted | rejected | deprecated | superseded | implemented
date: YYYY-MM-DD
decision-maker: [User Name]
consulted: [Agent-Perspective-1, Agent-Perspective-2]
research-method: 9-agent-parallel-dctl | single-agent | human-only
clarification-iterations: N
perspectives: [PerspectiveType1, PerspectiveType2]
---
```

### Field Descriptions

| Field                      | Required | Description                                                          |
| -------------------------- | -------- | -------------------------------------------------------------------- |
| `status`                   | Yes      | Current state (use `implemented` after release)                      |
| `date`                     | Yes      | Decision date (YYYY-MM-DD)                                           |
| `decision-maker`           | Yes      | Human who approved the plan (singular, accountable)                  |
| `consulted`                | Yes      | Agent perspectives that researched in prior session (string[])       |
| `research-method`          | Yes      | How prior research was conducted (enum)                              |
| `clarification-iterations` | Yes      | AskUserQuestion rounds before plan written to `~/.claude/plans/*.md` |
| `perspectives`             | Yes      | Decision context types (see Perspectives Taxonomy)                   |

---

## Required Sections

| Section                           | Required | Content                                                                    |
| --------------------------------- | -------- | -------------------------------------------------------------------------- |
| **Title** (H1)                    | Yes      | `# ADR: Descriptive Title`                                                 |
| **Context and Problem Statement** | Yes      | Problem description + Before/After diagram                                 |
| **Research Summary**              | Yes      | Agent perspectives and findings from prior session                         |
| **Decision Log**                  | Yes      | Synthesized decisions table + trade-offs (from AskUserQuestion iterations) |
| **Considered Options**            | Yes      | **Minimum 2 alternatives** with descriptions                               |
| **Decision Outcome**              | Yes      | What was decided + rationale from AskUserQuestion iterations               |
| **Synthesis**                     | Yes      | How divergent agent findings were reconciled                               |
| **Consequences**                  | Yes      | Positive/Negative trade-offs                                               |
| **Architecture**                  | Yes      | Use Skill tool to invoke `adr-graph-easy-architect` for diagrams           |
| Decision Drivers                  | Optional | Forces influencing the choice                                              |
| References                        | Optional | Related ADRs, external docs                                                |

---

## Formatting Rules

1. **Blank lines**: Required between all content blocks (prevents GitHub rendering issues)
2. **Links**: Use repository-relative format (`/docs/adr/...`), never `./` or `../`
3. **Design spec link**: Include in header: `**Design Spec**: [Implementation Spec](/docs/design/YYYY-MM-DD-slug/spec.md)`

---

## Complete Template

```markdown
---
status: proposed
date: YYYY-MM-DD
decision-maker: [User Name]
consulted: [Agent-Perspective-1, Agent-Perspective-2]
research-method: 9-agent-parallel-dctl
clarification-iterations: N
perspectives: [PerspectiveType1, PerspectiveType2]
---

# ADR: [Descriptive Title]

**Design Spec**: [Implementation Spec](/docs/design/YYYY-MM-DD-slug/spec.md)

## Context and Problem Statement

[What is the problem? Why does it need a decision?]

### Before/After

<!-- Use Skill tool to invoke adr-graph-easy-architect for Before/After visualization -->

## Research Summary

<!-- Extract from prior session: agent perspectives and material findings -->

| Agent Perspective | Key Finding | Confidence   |
| ----------------- | ----------- | ------------ |
| [Perspective 1]   | [Finding]   | High/Med/Low |
| [Perspective 2]   | [Finding]   | High/Med/Low |

## Decision Log

<!-- Synthesize AskUserQuestion iterations into decision table -->

| Decision Area | Options Evaluated | Chosen | Rationale         |
| ------------- | ----------------- | ------ | ----------------- |
| [Topic 1]     | A, B, C           | A      | [Why A over B, C] |
| [Topic 2]     | X, Y              | Y      | [Why Y over X]    |

### Trade-offs Accepted

| Trade-off | Choice | Accepted Cost                    |
| --------- | ------ | -------------------------------- |
| [X vs Y]  | X      | [What Y offered that we gave up] |

## Decision Drivers

- [Driver 1]
- [Driver 2]

## Considered Options

- **Option A**: [Description]
- **Option B**: [Description]
- **Option C**: [Description] <- Selected

## Decision Outcome

Chosen option: **Option C**, because [rationale from AskUserQuestion iterations + synthesis].

## Synthesis

<!-- Summarize how agent findings were reconciled during prior session -->

**Convergent findings**: [What all perspectives agreed on]
**Divergent findings**: [Where perspectives differed]
**Resolution**: [How user resolved conflicts]

## Consequences

### Positive

- [Benefit 1]

### Negative

- [Trade-off 1]

## Architecture

<!-- Use Skill tool to invoke adr-graph-easy-architect for system architecture diagram -->

## References

- [Related ADR](/docs/adr/YYYY-MM-DD-related.md)
- [Upstream: github.com/org/repo] (if UpstreamIntegration perspective)
```

---

## ADR ID Convention

**Format**: `YYYY-MM-DD-slug`

**Examples**:

- `2025-12-01-clickhouse-aws-ohlcv-ingestion`
- `2025-11-28-telegram-bot-network-aware-supervision`

**File Path**: `/docs/adr/$ADR_ID.md`

---

## Slug Word Economy Rule

Each word in the slug MUST convey unique meaning. Avoid redundancy.

| Example                          | Verdict | Reason                                                           |
| -------------------------------- | ------- | ---------------------------------------------------------------- |
| `clickhouse-database-migration`  | Bad     | "database" redundant (ClickHouse IS a database)                  |
| `clickhouse-aws-ohlcv-ingestion` | Good    | clickhouse=tech, aws=platform, ohlcv=data-type, ingestion=action |
| `user-auth-token-refresh`        | Good    | user=scope, auth=domain, token=artifact, refresh=action          |
| `api-endpoint-rate-limiting`     | Good    | api=layer, endpoint=target, rate=metric, limiting=action         |
