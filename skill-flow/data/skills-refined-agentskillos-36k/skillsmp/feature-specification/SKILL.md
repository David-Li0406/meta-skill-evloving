---
name: feature-specification
description: Produces a structured, experience-first feature specification following a docs-first approach. Use when defining or refining a single product feature's lifecycle and outcomes.
---

# Feature Specification Authoring

## What is it?

This skill generates a **canonical, experience-first feature specification** that defines a single feature’s intent, user lifecycle, and completion criteria.

It is **docs-first** and **agent-ready**, serving as the single source of truth for planning, review, automation, and execution.

---

## When to Use This Skill

Use this skill when you need to:

- Define a new feature before development planning
- Clarify scope and non-scope for an existing feature
- Align product and engineering on user-centric outcomes
- Create a high-quality prompt/spec for implementation agents

Do **not** use this skill for:

- roadmap planning
- task breakdown (except tasks derived directly from scenarios)
- technical design
- UI or UX design (focus on functional behavior)

---

## Core Principles

1. **Experience-First**: Scenarios must focus on quality of life and the user lifecycle, not just technical mechanics.
2. **Stateless & Portable**: The specification should be understandable without prior system context.
3. **Derived Tasks (Execution-Ready)**: All implementation tasks must be technical, actionable, and map back to specific scenarios for an AI Implementer.
4. **Observable Acceptance (Agent-Verifiable)**: Success must be verifiable by the Execution Agent through tests or observable system states.
5. **Gherkin-in-Markdown**: Scenarios must use Gherkin keywords (**Given**, **When**, **Then**, **And**) rendered as bold Markdown text. Do NOT use code blocks (e.g., ` ```gherkin `).
6. **Human-Centric & Dynamic**: Scenarios should be written as dynamic, narrative journeys from the user's perspective, while maintaining the structural clarity of Gherkin.

---

## Authoring Guidance

When generating a feature specification:

- **Leverage Gherkin Authoring Skill**: Invoke the `gherkin-authoring` skill to maximize the use of Gherkin syntax (e.g., `Background`, `Scenario Outline`, `Examples`, `Data Tables`, `Doc Strings`) to ensure scenarios are precise and comprehensive.
- **Visualize Flows**: Include Mermaid diagrams for complex user flows or state transitions to enhance clarity.
  - **Best Practice**: When a flow, state transition, or cross-context interaction adds clarity, include a Mermaid diagram directly in the spec. Keep diagrams focused (one flow per diagram), label nodes and transitions with user-centric names, and include a short caption that explains the diagram’s purpose. Prefer flowcharts for user journeys and state diagrams for lifecycle/state changes.

Caption: "High-level user journey for <feature>."

- **Autonomous Test Identification & Mapping**: For every scenario, the agent MUST evaluate its complexity and scope to identify and describe the required test types (Unit, Integration, and/or E2E). These must be formatted as **descriptive sub-tasks** (e.g., "[ ] Unit Test: <specific logic>") under Implementation Tasks and Acceptance Criteria, following the pattern in `assets/feature-spec.template.md`. Generic "add tests" checkboxes are prohibited.
- **Format as Gherkin-in-Markdown**: After reasoning with the Gherkin skill, transpose the logic into pure Markdown. Use bold keywords (e.g., **Scenario Outline**, **Examples**, **Given**, **When**, **Then**) without code blocks.
- **Follow Scenarios 1.1 - 1.6**: Ensure every user story covers the full lifecycle (Initial, Returning, Interruption, Error, Performance, Context).
- **Outcome-Oriented**: Describe what the feature enables, not how it is built.
- **Explicit Boundaries**: Clearly state Non-Goals to protect focus.
- **Human-Centric Errors**: Scenario 1.4 must focus on clear, humane communication during failures.
- **Feature Flag Strategy**: Always include a strategy in the Rollout section.

---

## Output Structure

The output MUST follow the canonical structure defined in `assets/feature-spec.template.md`:

0. **Frontmatter**: YAML frontmatter (between `---` markers) containing identity fields only:
   - `feature_name`: Display name of the feature
   - `parent_epic`: Name of the parent epic for linking
   - `bounded_context`: Domain context (e.g., `auth`, `billing`) - **used as Remote Config parameter group**
   - `status`: Current status (draft, approved, in-progress, done)

   > **Note**: Flag configuration is NOT in frontmatter. It lives in the `REMOTE_CONFIG_FLAG` block (Section 11).

1. **Overview**: Purpose and meaningful change.
2. **User Problem**: Lived experience and current friction.
3. **Goals**: Split into UX Goals and Business/System Goals.
4. **Non-Goals**: Boundaries and deferred problems.
5. **Functional Scope**: Conceptual capabilities and system responsibilities.
6. **Dependencies & Assumptions**: Required conditions.
7. **User Stories & Scenarios**: Detailed lifecycle scenarios (1.1 through 1.6).
8. **Edge Cases & Constraints**: Experience-relevant limits.
9. **Implementation Tasks**: Tasks T01-T05 defined as an **Execution Agent Checklist**.
10. **Acceptance Criteria**: Verifiable outcomes (AC1-AC5) for the agent to confirm completion.
11. **Rollout & Risk**: Strategy with **REMOTE_CONFIG_FLAG block** (see below).
12. **History & Status**: Metadata and links.

### REMOTE_CONFIG_FLAG Block Format

The `REMOTE_CONFIG_FLAG` block is the **source of truth** for all flag configuration. It must be placed in Section 11 (Rollout & Risk).

```markdown
<!-- REMOTE_CONFIG_FLAG_START -->
| Context | Type | Namespace | Default (Dev) | Default (Stg) | Default (Prod) | Key |
|---------|------|-----------|---------------|---------------|----------------|-----|
| social_login | BOOLEAN | client | true | false | false | _auto-generated_ |
<!-- REMOTE_CONFIG_FLAG_END -->
```

**Column Definitions:**

- **Context**: Flag context for key naming (e.g., `social_login`, `dark_mode`)
- **Type**: `BOOLEAN`, `STRING`, `NUMBER`, or `JSON`
- **Namespace**: `client` (Firebase client SDK) or `server` (Firebase Admin SDK)
- **Default (Dev)**: Value in development environment
- **Default (Stg)**: Value in staging environment
- **Default (Prod)**: Value in production environment
- **Key**: `_auto-generated_` initially, filled by automation after provisioning

### Dynamic Flag Type Determination

When authoring a feature specification, the agent MUST evaluate **what type of Remote Config parameter is needed** based on the feature's requirements:

| Use Case | Recommended Type | Example |
|----------|------------------|---------|
| On/off toggle for a feature | `BOOLEAN` | `true` / `false` |
| Theme, API endpoint, or text value | `STRING` | `"dark"`, `"https://api.v2.com"` |
| Rate limits, timeouts, counts | `NUMBER` | `100`, `5000` |
| Complex configuration objects | `JSON` | `{"maxRetries": 3, "timeout": 5000}` |

**Important:** The frontmatter is used by automation scripts to:

- Create GitHub issues with proper titles
- Link features to parent epics as sub-issues
- Track status

Flag provisioning uses the `REMOTE_CONFIG_FLAG` block exclusively.

---

### 11. Rollout & Risk (Feature Flag Requirement)

This section is mandatory and must explicitly state the flag strategy:

- **No flag required**: Feature is low risk and does not require a toggle.
- **Temporary flag**: Include the **purpose** and explicit **removal or promotion criteria**.
- **Permanent flag**: Include a **justification** (e.g., experiments, pricing, segmentation, or compliance).

---

## Important Boundaries

This skill **must not**:

- ask clarification questions
- decide sequencing or next steps
- create tasks or tickets (except the T-series tasks in section 9)
- define implementation details
- interact with users

All orchestration and workflow decisions belong to the calling agent.

---

## Output Expectations

- **Tone**: Neutral, precise, and humane.
- **Format**: Clean Markdown following the specific hierarchy.
- **Quality**: Avoid placeholders; provide specific, actionable scenarios.

---

## References

- See the canonical template: [assets/feature-spec.template.md](assets/feature-spec.template.md)
