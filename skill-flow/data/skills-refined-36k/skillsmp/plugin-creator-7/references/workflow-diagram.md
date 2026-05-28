# Plugin Creator Workflow Diagram

This diagram shows the complete agentic workflow for creating Claude Code plugins.

---

## High-Level Flow

```mermaid
flowchart LR
    P0[Phase 0: RT-ICA] --> P1[Phase 1: Research]
    P1 --> P2[Phase 2: Design]
    P2 --> P3[Phase 3: Implementation]
    P3 --> P4[Phase 4: Validation]
    P4 --> P5[Phase 5: Documentation]
    P5 --> P6[Phase 6: Final Verification]

    P0 -.-> |BLOCKED| REQ[Request Missing Info]
    REQ -.-> P0
    P6 -.-> |NOT COMPLETE| P4
```

---

## Phase 0: RT-ICA Prerequisite Check

```mermaid
flowchart TD
    REQ[User Request] --> RTICA[Invoke rt-ica Skill]
    RTICA --> CHECK{Prerequisites Complete?}
    CHECK -->|NO| BLOCKED[BLOCKED: Request missing info]
    BLOCKED --> REQ
    CHECK -->|YES| APPROVED[APPROVED: Continue to Phase 1]

    subgraph Prerequisites
        A[Purpose clarity]
        B[Target users]
        C[Component selection]
        D[Existing solutions]
        E[Source material]
        F[Verification method]
    end
```

---

## Phase 1: Research

```mermaid
flowchart TD
    subgraph "Parallel Research Tasks"
        T1A[Task 1a: Check Existing Solutions]
        T1B[Task 1b: Gather Domain Knowledge]
        T1C[Task 1c: Fetch Official Docs]
    end

    T1A --> E1[Explore Agent]
    T1B --> E2[Explore Agent]
    T1C --> GP[general-purpose Agent + WebFetch]

    E1 --> REPORT[Research Report]
    E2 --> REPORT
    GP --> REPORT

    subgraph "Research Outputs"
        REPORT --> O1[Similar plugins with paths/URLs]
        REPORT --> O2[Authoritative sources with dates]
        REPORT --> O3[Official schema fields verified]
        REPORT --> O4[Discrepancies flagged]
    end
```

---

## Phase 2: Design

```mermaid
flowchart TD
    RESEARCH[Research Report] --> T2A[Task 2a: Architecture Planning]
    T2A --> PLAN1[Plan Agent]
    PLAN1 --> ARCH[Architecture Document]

    ARCH --> COMP[Component list]
    ARCH --> TREE[File tree]
    ARCH --> DEPS[Dependencies]

    ARCH --> T2B[Task 2b: Skill Content Planning]
    T2B --> PLAN2[Plan Agent per skill]
    PLAN2 --> OUTLINE[Content Outlines]

    OUTLINE --> SKILL[SKILL.md structure]
    OUTLINE --> REFS[Reference file list]
    OUTLINE --> FM[Frontmatter values]
```

---

## Phase 3: Implementation

```mermaid
flowchart TD
    DESIGN[Design Documents] --> CHOICE{Implementation Option}

    CHOICE -->|Option A| SCRIPT[Scaffolding Script]
    CHOICE -->|Option B| MANUAL[Manual Creation]

    SCRIPT --> UV["uv run create_plugin.py"]
    MANUAL --> DIRS[Create directories]
    MANUAL --> FILES[Write files]

    UV --> PLUGIN[Plugin Created]
    DIRS --> PLUGIN
    FILES --> PLUGIN

    subgraph "Consider Advanced Features"
        AF1[Dynamic context injection]
        AF2[Subagent execution]
        AF3[Visual output scripts]
        AF4[Hook automation]
        AF5[MCP/LSP integration]
    end
```

---

## Phase 4: Validation

```mermaid
flowchart TD
    PLUGIN[Created Plugin] --> T4A[Task 4a: Automated Validation]
    PLUGIN --> T4B[Task 4b: Verify vs Official Docs]

    T4A --> SCRIPTS["create_plugin.py validate + validate_frontmatter.py"]
    T4B --> GP[general-purpose Agent + WebFetch]

    SCRIPTS --> RESULTS[Validation Results]
    GP --> RESULTS

    RESULTS --> T4C[Task 4c: Quality Assessment]
    T4C --> ASSESSOR[plugin-assessor Agent]
    ASSESSOR --> REPORT[Validation Report]

    REPORT --> S1[Schema OK?]
    REPORT --> S2[Frontmatter valid?]
    REPORT --> S3[Quality score]
```

---

## Phase 5: Documentation

```mermaid
flowchart TD
    VALIDATED[Validated Plugin] --> DOCS[plugin-docs-writer Agent]

    DOCS --> README[README.md]
    DOCS --> SKILLS_DOC[docs/skills.md]
    DOCS --> CONFIG[Configuration guide]
```

---

## Phase 6: Final Verification

```mermaid
flowchart TD
    DOCUMENTED[Documented Plugin] --> VERIFY[Invoke verify Skill]

    VERIFY --> CHECKLIST{Verification Checklist}

    CHECKLIST --> W[Works Check: validation passed?]
    CHECKLIST --> Q[Quality Gates: no critical issues?]
    CHECKLIST --> D[Docs Check: README accurate?]
    CHECKLIST --> H[Honesty Check: sources cited?]

    W --> DECISION{All Passed?}
    Q --> DECISION
    D --> DECISION
    H --> DECISION

    DECISION -->|NO| NOTCOMPLETE[NOT COMPLETE: Fix issues]
    NOTCOMPLETE --> FIXPHASE[Return to relevant phase]

    DECISION -->|YES| COMPLETE[COMPLETE: Plugin ready]
```

---

## Agent Delegation Map

```mermaid
flowchart LR
    subgraph Research
        R1[Explore] --> R1T[Code discovery]
        R2[Explore] --> R2T[Domain knowledge]
        R3[general-purpose] --> R3T[Official docs fetch]
    end

    subgraph Design
        D1[Plan] --> D1T[Architecture]
        D2[Plan] --> D2T[Content structure]
    end

    subgraph Validate
        V1[Scripts] --> V1T[Schema validation]
        V2[general-purpose] --> V2T[Docs verification]
        V3[plugin-assessor] --> V3T[Quality assessment]
    end

    subgraph Document
        DOC[plugin-docs-writer] --> DOCT[README generation]
    end
```

---

## Orchestrator Rules

```mermaid
flowchart TD
    subgraph "DELEGATE TO"
        A1[Explore agent] --> A1T[Domain research]
        A2[Explore agent] --> A2T[Code discovery]
        A3[WebFetch/Explore] --> A3T[Official docs]
        A4[Validation scripts] --> A4T[Schema checks]
        A5[plugin-assessor] --> A5T[Quality review]
        A6[plugin-docs-writer] --> A6T[Documentation]
    end

    subgraph "NEVER DO DIRECTLY"
        B1[Read docs yourself]
        B2[Grep/search yourself]
        B3[Assume from training]
        B4[Manual field checking]
        B5[Review own work]
        B6[Write README yourself]
    end
```

---

## Failure Recovery Paths

```mermaid
flowchart TD
    F0[Phase 0 BLOCKED] --> F0R[Request missing info] --> F0A[Re-run RT-ICA]

    F1[Phase 1 Incomplete] --> F1R[Spawn more Explore agents]
    F1 --> F1B[Fetch more official docs]

    F4[Phase 4 Validation Failures] --> F4A[Schema errors] --> F4AF[Fix plugin.json]
    F4 --> F4B[Frontmatter errors] --> F4BF[Fix SKILL.md]
    F4 --> F4C[Quality issues] --> F4CF[Improve content]

    F4AF --> REVAL[Re-validate]
    F4BF --> REVAL
    F4CF --> REASSESS[Re-assess]

    F6[Phase 6 NOT COMPLETE] --> F6A[Identify failing check]
    F6A --> F6B[Return to relevant phase]
    F6B --> F6C[Fix and re-verify]
```

---

## Source

This workflow diagram documents the agentic plugin creation process defined in [SKILL.md](../SKILL.md).
