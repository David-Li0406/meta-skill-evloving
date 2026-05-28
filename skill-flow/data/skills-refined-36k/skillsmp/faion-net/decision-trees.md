# Decision Trees for Skill and Methodology Selection

## Overview

This document provides decision trees for:
1. **Skill Selection** - Which domain skill to invoke for a given task
2. **Methodology Selection** - Which methodology to apply within a skill

**Pattern:** Coordinator-Worker (faion-net orchestrates, domain skills execute)

**Reference:** [Azure AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

---

## Part 1: Skill Selection Decision Tree

### Primary Question Flow

```
Q1: What is the PRIMARY intent?
    │
    ├─ "Research/Discovery" ───────────────────────────────────────────────────┐
    │   Q2: What type of research?                                             │
    │       ├─ Idea generation, market, competitors, personas ── faion-researcher
    │       ├─ Technical feasibility, architecture options ──── faion-software-architect (NEW)
    │       └─ User experience, usability ────────────────────── faion-ux-ui-designer
    │
    ├─ "Planning/Strategy" ────────────────────────────────────────────────────┐
    │   Q2: What domain?                                                       │
    │       ├─ Product (MVP, roadmap, features) ──────────────── faion-product-manager
    │       ├─ Project (schedule, risks, resources) ──────────── faion-project-manager
    │       ├─ Marketing (GTM, campaigns) ────────────────────── faion-marketing-manager
    │       ├─ Requirements (business analysis) ──────────────── faion-business-analyst
    │       └─ Architecture (system design) ──────────────────── faion-software-architect (NEW)
    │
    ├─ "Development/Execution" ────────────────────────────────────────────────┐
    │   Q2: What type of work?                                                 │
    │       ├─ Writing code, testing, APIs ───────────────────── faion-software-developer
    │       ├─ Infrastructure, CI/CD, deployment ─────────────── faion-devops-engineer
    │       ├─ AI/ML, LLMs, RAG, embeddings ──────────────────── faion-ml-engineer
    │       ├─ UI components, design systems ─────────────────── faion-ux-ui-designer
    │       └─ SDD workflow (specs, tasks, features) ─────────── faion-sdd
    │
    ├─ "Communication/Stakeholders" ───────────────────────────────────────────┐
    │   Q2: What interaction type?                                             │
    │       ├─ Requirements gathering, interviews ────────────── faion-communicator
    │       ├─ Conflict resolution, negotiation ──────────────── faion-communicator
    │       ├─ Selling ideas, presentations ──────────────────── faion-communicator
    │       └─ Hiring, onboarding ────────────────────────────── faion-hr-recruiter
    │
    └─ "Claude Code Setup" ────────────────────────────────────────────────────┐
        Q2: What to configure?                                                 │
            ├─ Skills, agents, commands ──────────────────────── faion-claude-code
            ├─ MCP servers, hooks ────────────────────────────── faion-claude-code
            └─ IDE integration ───────────────────────────────── faion-claude-code
```

---

### Quick Reference Matrix

| User Intent Keywords | Primary Skill | Secondary Skills |
|---------------------|---------------|------------------|
| idea, brainstorm, market, competitors, naming | faion-researcher | faion-product-manager |
| MVP, MLP, roadmap, features, prioritize | faion-product-manager | faion-researcher |
| architecture, design, patterns, scalability | faion-software-architect | faion-software-developer |
| code, implement, test, API, build | faion-software-developer | faion-devops-engineer |
| deploy, CI/CD, Docker, K8s, infra | faion-devops-engineer | faion-software-developer |
| LLM, RAG, embeddings, AI, ML | faion-ml-engineer | faion-software-developer |
| GTM, marketing, SEO, ads, landing | faion-marketing-manager | faion-researcher |
| schedule, risk, EVM, project plan | faion-project-manager | faion-business-analyst |
| requirements, use cases, stakeholders | faion-business-analyst | faion-product-manager |
| UX, UI, usability, wireframes | faion-ux-ui-designer | faion-software-developer |
| interview, feedback, conflict, negotiate | faion-communicator | - |
| hire, recruit, onboard | faion-hr-recruiter | - |
| spec, design doc, implementation plan | faion-sdd | faion-software-architect |
| skill, agent, hook, command, MCP | faion-claude-code | - |

---

### Project Phase Decision Tree

```
Q1: What project phase?
    │
    ├─ "0. Idea/Discovery" ────────────────────────────────────────────────────┐
    │   Primary: faion-researcher                                              │
    │   Sequence:                                                              │
    │   1. idea-generation (7 Ps, Paul Graham questions)                       │
    │   2. pain-point-research (Reddit, forums)                                │
    │   3. niche-evaluation (scoring)                                          │
    │   4. problem-validation (evidence gathering)                             │
    │
    ├─ "1. Planning/Specification" ────────────────────────────────────────────┐
    │   Q2: Planning type?                                                     │
    │       ├─ Product scope ─── faion-product-manager → mvp-scoping           │
    │       ├─ Architecture ──── faion-software-architect → system-design      │
    │       ├─ Project plan ──── faion-project-manager → wbs-creation          │
    │       └─ SDD bootstrap ─── faion-sdd → constitution-guidelines           │
    │
    ├─ "2. Design/Architecture" ───────────────────────────────────────────────┐
    │   Q2: Design type?                                                       │
    │       ├─ System architecture ─── faion-software-architect                │
    │       ├─ API design ──────────── faion-software-developer → api-rest     │
    │       ├─ UX/UI design ────────── faion-ux-ui-designer → wireframing      │
    │       └─ Database design ─────── faion-software-architect → data-modeling│
    │
    ├─ "3. Development" ───────────────────────────────────────────────────────┐
    │   Q2: What to develop?                                                   │
    │       ├─ Feature code ──── faion-software-developer                      │
    │       ├─ Tests ─────────── faion-software-developer → testing-*          │
    │       ├─ Infrastructure ── faion-devops-engineer                         │
    │       └─ AI/ML features ── faion-ml-engineer                             │
    │
    ├─ "4. Launch/GTM" ────────────────────────────────────────────────────────┐
    │   Primary: faion-marketing-manager                                       │
    │   Sequence:                                                              │
    │   1. gtm-strategy                                                        │
    │   2. landing-page-design                                                 │
    │   3. seo-* / ads-*                                                       │
    │   4. product-hunt-launch                                                 │
    │
    └─ "5. Maintenance/Growth" ────────────────────────────────────────────────┐
        Q2: Focus area?                                                        │
            ├─ Feature iteration ─── faion-product-manager → backlog-*         │
            ├─ Performance ───────── faion-devops-engineer → monitoring-*      │
            ├─ Growth metrics ────── faion-marketing-manager → aarrr-*         │
            └─ User feedback ─────── faion-ux-ui-designer → user-interviews    │
```

---

### Task Complexity Decision Tree

```
Q1: How complex is the task?
    │
    ├─ "Simple" (single domain, clear outcome) ────────────────────────────────┐
    │   Action: Invoke skill directly in main conversation                     │
    │   Example: "Add a login button" → faion-software-developer              │
    │
    ├─ "Moderate" (single domain, multiple steps) ─────────────────────────────┐
    │   Action: Use Task tool with appropriate agent                           │
    │   Example: "Implement auth feature" → faion-task-YOLO-executor-opus-agent     │
    │
    └─ "Complex" (multi-domain, unclear outcome) ──────────────────────────────┐
        Action: Multi-skill orchestration                                      │
        Q2: Domains involved?                                                  │
            ├─ Research + Product ── faion-researcher THEN faion-product-manager
            ├─ Architecture + Dev ── faion-software-architect THEN faion-software-developer
            ├─ Product + Marketing ─ faion-product-manager THEN faion-marketing-manager
            └─ Full lifecycle ────── faion-sdd orchestration
```

---

## Part 2: Per-Skill Methodology Decision Trees

### Pattern for Methodology Selection

Each skill has internal decision trees for methodology selection based on:
1. **Problem Type** - What problem are we solving?
2. **Context** - Project constraints, team, timeline
3. **Deliverable** - Expected output format

---

### faion-researcher Methodology Decision Tree

```
Q1: What research goal?
    │
    ├─ "Generate new ideas" ───────────────────────────────────────────────────┐
    │   Q2: Source of ideas?                                                   │
    │       ├─ Personal experience ───── idea-generation (7 Ps)                │
    │       ├─ Existing problems ─────── pain-point-research                   │
    │       ├─ Reflection questions ──── paul-graham-questions                 │
    │       └─ Industry trends ───────── trend-analysis                        │
    │
    ├─ "Validate existing idea" ───────────────────────────────────────────────┐
    │   Q2: What to validate?                                                  │
    │       ├─ Problem exists ────────── problem-validation                    │
    │       ├─ Market opportunity ────── niche-evaluation + market-research    │
    │       └─ Competition level ─────── competitor-analysis                   │
    │
    ├─ "Understand users" ─────────────────────────────────────────────────────┐
    │   Q2: Depth needed?                                                      │
    │       ├─ Quick profile ─────────── persona-building                      │
    │       ├─ Deep motivation ───────── jobs-to-be-done                       │
    │       └─ Value alignment ───────── value-proposition-design              │
    │
    └─ "Name/brand project" ───────────────────────────────────────────────────┐
        Sequence:                                                              │
        1. project-naming (generate candidates)                                │
        2. domain-availability (check .com, .io, socials)                      │
```

---

### faion-product-manager Methodology Decision Tree

```
Q1: What product decision?
    │
    ├─ "Define scope" ─────────────────────────────────────────────────────────┐
    │   Q2: Product stage?                                                     │
    │       ├─ Initial MVP ───────────── mvp-scoping                           │
    │       ├─ MVP → MLP ─────────────── mlp-planning                          │
    │       └─ Feature expansion ─────── feature-prioritization-rice           │
    │
    ├─ "Prioritize features" ──────────────────────────────────────────────────┐
    │   Q2: Stakeholder alignment?                                             │
    │       ├─ Objective scoring needed ── feature-prioritization-rice         │
    │       ├─ Quick categorization ────── feature-prioritization-moscow       │
    │       └─ Impact-based ────────────── stakeholder-management              │
    │
    ├─ "Create roadmap" ───────────────────────────────────────────────────────┐
    │   Q2: Timeline clarity?                                                  │
    │       ├─ Uncertain (Now/Next/Later) ── roadmap-design                    │
    │       ├─ Sprint-based ────────────── release-planning                    │
    │       └─ User journey based ──────── user-story-mapping                  │
    │
    └─ "Set goals" ────────────────────────────────────────────────────────────┐
        Q2: Goal type?                                                         │
            ├─ Company/team goals ───── okr-setting                            │
            ├─ Root cause analysis ──── product-discovery (5 Whys)             │
            └─ Business model ───────── business-model-research (Lean Canvas)  │
```

---

### faion-software-developer Methodology Decision Tree

```
Q1: What development task?
    │
    ├─ "Write new code" ───────────────────────────────────────────────────────┐
    │   Q2: Language/Framework?                                                │
    │       ├─ Python + Django ───────── python-django-standards               │
    │       ├─ Python + FastAPI ──────── python-fastapi-standards              │
    │       ├─ TypeScript + React ────── react-component-architecture          │
    │       ├─ TypeScript + Node ─────── nodejs-service-layer                  │
    │       ├─ Go ────────────────────── go-project-structure                  │
    │       └─ Other (Rust, Ruby, PHP, Java, C#) ── backend-* methodologies    │
    │
    ├─ "Design API" ───────────────────────────────────────────────────────────┐
    │   Q2: API type?                                                          │
    │       ├─ REST ──────────────────── api-rest-design                       │
    │       ├─ GraphQL ───────────────── api-graphql-design                    │
    │       └─ OpenAPI spec ──────────── api-openapi-specification             │
    │
    ├─ "Write tests" ──────────────────────────────────────────────────────────┐
    │   Q2: Test level?                                                        │
    │       ├─ Unit tests ────────────── testing-unit                          │
    │       ├─ Integration tests ─────── testing-integration                   │
    │       ├─ E2E tests ─────────────── testing-e2e                           │
    │       └─ TDD workflow ──────────── testing-tdd-workflow                  │
    │
    └─ "Improve code quality" ─────────────────────────────────────────────────┐
        Q2: Improvement type?                                                  │
            ├─ Refactoring ───────────── refactoring-patterns                  │
            ├─ Code review ───────────── code-review                           │
            ├─ Technical debt ────────── technical-debt                        │
            └─ Documentation ─────────── documentation + claude-md-creation    │
```

---

### faion-devops-engineer Methodology Decision Tree

```
Q1: What infrastructure task?
    │
    ├─ "Containerization" ─────────────────────────────────────────────────────┐
    │   Q2: Scale?                                                             │
    │       ├─ Single service ────────── docker-containerization               │
    │       ├─ Multi-service ─────────── docker-compose                        │
    │       └─ Production cluster ────── kubernetes-deployment                 │
    │
    ├─ "CI/CD pipeline" ───────────────────────────────────────────────────────┐
    │   Q2: Platform?                                                          │
    │       ├─ GitHub ────────────────── cicd-github-actions                   │
    │       ├─ GitLab ────────────────── cicd-gitlab                           │
    │       └─ Jenkins ───────────────── cicd-jenkins                          │
    │
    ├─ "Infrastructure as Code" ───────────────────────────────────────────────┐
    │   Q2: Cloud provider?                                                    │
    │       ├─ AWS ───────────────────── aws-architecture + terraform-iac      │
    │       ├─ GCP ───────────────────── gcp-architecture + terraform-iac      │
    │       └─ Azure ─────────────────── azure-architecture + terraform-iac    │
    │
    └─ "Monitoring/Observability" ─────────────────────────────────────────────┐
        Q2: Focus?                                                             │
            ├─ Metrics ───────────────── monitoring-prometheus + grafana       │
            ├─ Logs ──────────────────── logging-elk-stack                     │
            └─ Security ──────────────── secrets-management + ssl-tls-setup    │
```

---

### faion-ml-engineer Methodology Decision Tree

```
Q1: What AI/ML task?
    │
    ├─ "Use LLM API" ──────────────────────────────────────────────────────────┐
    │   Q2: Which provider?                                                    │
    │       ├─ OpenAI (GPT) ──────────── llm-openai-api                        │
    │       ├─ Anthropic (Claude) ────── llm-claude-api                        │
    │       ├─ Google (Gemini) ───────── llm-gemini-api                        │
    │       └─ Local (Ollama) ────────── llm-local-ollama                      │
    │
    ├─ "Build RAG system" ─────────────────────────────────────────────────────┐
    │   Sequence:                                                              │
    │   1. chunking-strategies                                                 │
    │   2. embedding-generation                                                │
    │   3. vector-database-setup                                               │
    │   4. rag-pipeline-design                                                 │
    │   5. hybrid-search + reranking (optional)                                │
    │   6. rag-evaluation                                                      │
    │
    ├─ "Fine-tune model" ──────────────────────────────────────────────────────┐
    │   Q2: Approach?                                                          │
    │       ├─ OpenAI fine-tuning ────── fine-tuning-openai                    │
    │       └─ LoRA/QLoRA ────────────── fine-tuning-lora                      │
    │
    └─ "Build agent" ──────────────────────────────────────────────────────────┐
        Q2: Agent type?                                                        │
            ├─ Single agent with tools ── function-calling + langchain-patterns
            ├─ Multi-agent system ─────── multi-agent-systems                  │
            └─ Voice agent ────────────── voice-agents + speech-to-text        │
```

---

### faion-marketing-manager Methodology Decision Tree

```
Q1: What marketing goal?
    │
    ├─ "Launch product" ───────────────────────────────────────────────────────┐
    │   Sequence:                                                              │
    │   1. icp-definition                                                      │
    │   2. value-proposition-design                                            │
    │   3. positioning-statement + messaging-framework                         │
    │   4. gtm-strategy                                                        │
    │   5. landing-page-design                                                 │
    │   6. product-hunt-launch (if B2C tech)                                   │
    │
    ├─ "Drive traffic" ────────────────────────────────────────────────────────┐
    │   Q2: Budget?                                                            │
    │       ├─ No budget (organic) ───── seo-* + content-marketing + social-*  │
    │       └─ Paid ads ──────────────── google-ads-* OR meta-ads-*            │
    │
    ├─ "Optimize conversion" ──────────────────────────────────────────────────┐
    │   Q2: Stage?                                                             │
    │       ├─ Landing page ──────────── above-the-fold + cta-optimization     │
    │       ├─ Funnel ────────────────── funnel-optimization                   │
    │       └─ Testing ───────────────── ab-testing-framework                  │
    │
    └─ "Retain/grow users" ────────────────────────────────────────────────────┐
        Q2: Focus?                                                             │
            ├─ Metrics ───────────────── aarrr-pirate-metrics + cohort-analysis│
            ├─ Email ─────────────────── welcome-sequence + nurture-sequence   │
            └─ Community ─────────────── community-building                    │
```

---

### faion-ux-ui-designer Methodology Decision Tree

```
Q1: What UX/UI task?
    │
    ├─ "Understand users" ─────────────────────────────────────────────────────┐
    │   Q2: Research type?                                                     │
    │       ├─ Qualitative ───────────── user-interviews + contextual-inquiry  │
    │       ├─ Quantitative ──────────── surveys                               │
    │       └─ Synthesis ─────────────── personas + journey-mapping            │
    │
    ├─ "Design solution" ──────────────────────────────────────────────────────┐
    │   Q2: Fidelity?                                                          │
    │       ├─ Low-fi ────────────────── wireframing + information-architecture│
    │       ├─ High-fi ───────────────── prototyping                           │
    │       └─ System ────────────────── design-tokens + component-library     │
    │
    ├─ "Evaluate design" ──────────────────────────────────────────────────────┐
    │   Q2: Method?                                                            │
    │       ├─ Expert review ─────────── heuristic-evaluation (10 Heuristics)  │
    │       ├─ User testing ──────────── usability-testing                     │
    │       └─ A/B testing ───────────── ab-testing                            │
    │
    └─ "Ensure accessibility" ─────────────────────────────────────────────────┐
        Primary: accessibility-evaluation (WCAG 2.2)                           │
```

---

### faion-project-manager Methodology Decision Tree

```
Q1: What PM task?
    │
    ├─ "Plan project" ─────────────────────────────────────────────────────────┐
    │   Sequence:                                                              │
    │   1. stakeholder-register + stakeholder-analysis-matrix                  │
    │   2. development-approach-selection (Agile/Waterfall/Hybrid)             │
    │   3. wbs-creation                                                        │
    │   4. schedule-development + cost-estimation                              │
    │   5. communication-management-plan                                       │
    │
    ├─ "Manage execution" ─────────────────────────────────────────────────────┐
    │   Q2: Focus area?                                                        │
    │       ├─ Team ──────────────────── team-charter + raci-matrix            │
    │       ├─ Progress ──────────────── earned-value-management               │
    │       ├─ Quality ───────────────── quality-management-plan               │
    │       └─ Change ────────────────── change-management-process             │
    │
    ├─ "Handle risks" ─────────────────────────────────────────────────────────┐
    │   Sequence:                                                              │
    │   1. risk-register (identify)                                            │
    │   2. risk-response-planning (mitigate)                                   │
    │
    └─ "Close/retrospect" ─────────────────────────────────────────────────────┐
        Sequence:                                                              │
        1. lessons-learned                                                     │
        2. project-closure-checklist                                           │
```

---

### faion-business-analyst Methodology Decision Tree

```
Q1: What BA task?
    │
    ├─ "Plan analysis" ────────────────────────────────────────────────────────┐
    │   Primary: ba-planning (Business Case)                                   │
    │   Secondary: stakeholder-analysis                                        │
    │
    ├─ "Gather requirements" ──────────────────────────────────────────────────┐
    │   Q2: Format needed?                                                     │
    │       ├─ Use cases ─────────────── use-case-modeling                     │
    │       ├─ User stories ──────────── user-story-mapping                    │
    │       ├─ Acceptance criteria ───── acceptance-criteria                   │
    │       └─ Mixed ─────────────────── elicitation-techniques               │
    │
    ├─ "Analyze/design" ───────────────────────────────────────────────────────┐
    │   Q2: Focus?                                                             │
    │       ├─ Process ───────────────── business-process-analysis (BPMN)      │
    │       ├─ Data ──────────────────── data-analysis (ERD)                   │
    │       └─ Strategy ──────────────── strategy-analysis (Gap Analysis)      │
    │
    └─ "Validate/trace" ───────────────────────────────────────────────────────┐
        Q2: Need?                                                              │
            ├─ Traceability ──────────── requirements-traceability             │
            ├─ Feasibility ───────────── requirements-validation               │
            └─ Solution fit ──────────── solution-assessment                   │
```

---

## Part 3: Multi-Skill Orchestration Patterns

### Pattern 1: Sequential Pipeline

Use when tasks have clear dependencies.

```
Skill A (output) → Skill B (input) → Skill C (input) → Final Output

Example: Full Product Development
faion-researcher (market-research.md)
    → faion-product-manager (mvp-scope.md)
    → faion-software-architect (architecture.md)
    → faion-software-developer (code)
    → faion-devops-engineer (deployment)
    → faion-marketing-manager (launch)
```

### Pattern 2: Parallel Branches

Use when independent tasks can run simultaneously.

```
                    ┌── Skill A ──┐
faion-net ──────────┼── Skill B ──┼──────── Aggregate Results
                    └── Skill C ──┘

Example: Launch Preparation
                    ┌── faion-software-developer (final fixes)
faion-net ──────────┼── faion-marketing-manager (landing page)
                    └── faion-devops-engineer (production setup)
```

### Pattern 3: Iterative Loop

Use when feedback cycles are needed.

```
Skill A ←→ Skill B (iterate until done)

Example: Design-Development Cycle
faion-ux-ui-designer (wireframes)
    ↔ faion-software-developer (implementation)
    ↔ faion-ux-ui-designer (usability test)
    → Repeat until quality threshold met
```

---

## Part 4: Execution Mode Selection

```
Q1: Task clarity?
    │
    ├─ Clear, well-defined ────────────────────────────────────────────────────┐
    │   Use: YOLO Mode (faion-task-YOLO-executor-opus-agent)                        │
    │   - Maximum autonomy                                                     │
    │   - No interruptions                                                     │
    │   - Best for: SDD tasks with spec/design                                 │
    │
    └─ Unclear, needs exploration ─────────────────────────────────────────────┐
        Use: Interactive Mode (faion-communicator patterns)                    │
        - Collaborative dialogue                                               │
        - Clarifying questions                                                 │
        - Best for: New features, vague requirements                           │
```

---

## Quick Decision Flowchart

```
START
  │
  ▼
Is this about Claude Code setup? ─── YES ──► faion-claude-code
  │
  NO
  │
  ▼
Is this research/discovery? ─── YES ──► faion-researcher
  │
  NO
  │
  ▼
Is this about architecture/design patterns? ─── YES ──► faion-software-architect
  │
  NO
  │
  ▼
Is this product planning? ─── YES ──► faion-product-manager
  │
  NO
  │
  ▼
Is this writing code? ─── YES ──► faion-software-developer
  │
  NO
  │
  ▼
Is this infrastructure/deployment? ─── YES ──► faion-devops-engineer
  │
  NO
  │
  ▼
Is this AI/ML/LLM? ─── YES ──► faion-ml-engineer
  │
  NO
  │
  ▼
Is this marketing/GTM? ─── YES ──► faion-marketing-manager
  │
  NO
  │
  ▼
Is this UX/UI? ─── YES ──► faion-ux-ui-designer
  │
  NO
  │
  ▼
Is this project management? ─── YES ──► faion-project-manager
  │
  NO
  │
  ▼
Is this business analysis? ─── YES ──► faion-business-analyst
  │
  NO
  │
  ▼
Is this communication/stakeholders? ─── YES ──► faion-communicator
  │
  NO
  │
  ▼
Is this hiring/HR? ─── YES ──► faion-hr-recruiter
  │
  NO
  │
  ▼
Is this SDD workflow? ─── YES ──► faion-sdd
  │
  NO
  │
  ▼
faion-net (analyze further)
```

---

*Decision Trees v1.0*
*Reference: Azure AI Agent Design Patterns, InfoQ Architectural Decisions Framework*
