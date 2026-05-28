---
name: faion-net
description: "Universal orchestrator for software projects: SDD workflow, research, product planning, development, marketing, project/business analysis, UX, HR/recruiting. 60+ agents, 15 skills, 502 methodologies."
user-invocable: true
---

# Faion Network Orchestrator

**Communication: User's language.**

Universal skill for end-to-end software project lifecycle. From idea to production, from research to marketing.

---

## Step 1: Knowledge Freshness Check

**At session start, calculate:** `gap = current_date - model_cutoff` (from system prompt)

**Output:** `Knowledge gap: ~{months} months. WebSearch needed for: {areas}`

**Fast-changing areas (use WebSearch):**
- Package versions (npm, pip, cargo, go)
- Framework APIs (React, Next.js, Django, FastAPI)
- Cloud pricing (AWS, GCP, Azure)
- AI models (new releases, pricing, limits)
- Security (CVEs, vulnerabilities)

---

## Step 2: Execution Mode Selection

**Ask user at session start:**

```python
AskUserQuestion([
    {
        "question": "How should I work on tasks?",
        "header": "Mode",
        "options": [
            {"label": "YOLO Mode (Recommended)", "description": "Maximum autonomy. Execute tasks completely without interruptions. Uses faion-task-YOLO-executor-opus-agent."},
            {"label": "Interactive Mode", "description": "Collaborative dialogue. Ask questions, clarify requirements, validate decisions. Stakeholder interview style."}
        ]
    }
])
```

---

### YOLO Mode (Autonomous)

**Agent:** `faion-task-YOLO-executor-opus-agent`

**Behavior:**
- Execute tasks completely without asking questions
- Make decisions autonomously using best practices
- Use appropriate methodologies from 494 available
- Document assumptions in code/comments
- Complete tasks or report blockers with details

**When to use:**
- Clear, well-defined tasks
- Tasks with SDD documentation (spec, design)
- User trusts AI judgment
- User wants speed over control

**Execution:**
```python
Task(
    prompt="Execute task: {task_description}",
    subagent_type="faion-task-YOLO-executor-opus-agent"
)
```

---

### Interactive Mode (Dialogue)

**Skill:** `faion-communicator` (9 methodologies)

**Behavior:**
- Execute directly in main conversation flow
- Ask clarifying questions before proceeding
- Validate understanding at each step
- Use communication techniques:
  - **Interview:** Gather requirements with probing questions
  - **Brainstorm:** Generate options collaboratively
  - **Clarification:** Resolve ambiguity
  - **Validation:** Confirm before implementing
  - **Socratic:** Deep exploration through questions

**When to use:**
- Vague or incomplete requirements
- User wants to learn/understand
- Complex decisions needing input
- User prefers control over speed

**Communication Protocol:**

```markdown
## For new feature requests → Interview
"I'd like to understand your requirements:
1. What problem are you solving?
2. Who are the users?
3. What's the success criteria?
4. Any constraints?"

## For design decisions → Brainstorm + Validate
"Let's explore options:
- Option A: [pros/cons]
- Option B: [pros/cons]
Which direction feels right?"

## For ambiguous requirements → Clarification
"When you say 'fast', do you mean:
a) Response time < 100ms?
b) Quick to implement?
c) Fast user experience?"

## Before implementation → Validation
"Here's my understanding: [summary]
Is this correct? Shall I proceed?"
```

**Execution:**
- Use tools directly in conversation
- Ask questions via AskUserQuestion or text
- Provide step-by-step visibility
- Confirm before significant changes

---

## Capabilities

**Idea → Validation:**
- Generate startup/product ideas (7 frameworks)
- Research pain points via Reddit, forums, reviews
- Validate problems with evidence (frequency, severity, willingness to pay)
- Evaluate niche viability (market size, competition, barriers)
- Generate product names, check domain availability

**Research → Strategy:**
- Market research (TAM/SAM/SOM, trends, growth drivers)
- Competitor analysis (features, pricing, positioning)
- User personas from real feedback
- Pricing strategies and models
- Problem validation with evidence

**Product Planning:**
- MVP scope from competitor analysis
- MLP planning (gap analysis, WOW moments)
- Feature prioritization (RICE, MoSCoW)
- Roadmap design, release planning
- User story mapping, OKRs

**SDD Workflow:**
- Project bootstrap (constitution, roadmap)
- Specification writing with acceptance criteria
- Technical design documents
- Implementation plans with task parallelization
- Task execution with quality gates
- Reflexion learning (patterns, mistakes)

**Development:**
- Code generation (Python, JS/TS, Go, Ruby, PHP, Java, C#, Rust)
- Code review and refactoring
- Testing (unit, integration, E2E, TDD)
- API design (REST, GraphQL, OpenAPI)
- DevOps (CI/CD, Docker, K8s, Terraform, AWS)
- Browser automation (Puppeteer, Playwright)

**AI/LLM:**
- RAG pipelines (document Q&A, knowledge bases)
- Embeddings (generation, indexing, search)
- Fine-tuning (LoRA, QLoRA, PEFT)
- Prompt engineering and optimization
- Multimodal (image, video, audio generation)
- Voice agents (STT, TTS, real-time)
- Autonomous agents (LangGraph, ReAct)

**Marketing:**
- GTM strategy and execution
- Landing pages with high conversion
- Content marketing and SEO
- Paid ads (Meta, Google)
- Email campaigns and automation
- Social media strategy

**Project Management (Project Management Framework 7/8):**
- Stakeholder management
- Risk management
- Earned Value Management (EVM)
- Change control
- Agile, Waterfall, Hybrid delivery

**Business Analysis (Business Analysis Framework):**
- Requirements elicitation
- Traceability matrices
- Solution assessment
- 6 Knowledge Areas, 30 tasks

**UX:**
- User research (interviews, surveys, contextual inquiry)
- Usability testing (moderated, unmoderated)
- Heuristic evaluation (10 Usability Heuristics)
- Personas, journey mapping
- Wireframing, prototyping

---

## Domain Skills (14)

| Skill | Purpose |
|-------|---------|
| `faion-sdd` | SDD orchestrator: specs, designs, implementation plans, constitutions, task lifecycle, quality gates, reflexion |
| `faion-feature-executor` | SDD feature executor: sequential tasks with quality gates, tests/coverage, code review |
| `faion-researcher` | Idea generation (SCAMPER), market research, competitors, personas, pricing, validation. 20 methodologies |
| `faion-product-manager` | MVP/MLP planning, RICE/MoSCoW prioritization, roadmaps, backlog, user stories, OKRs. 18 methodologies |
| `faion-software-developer` | Python, JS/TS, Django, FastAPI, React, APIs, testing, DevOps, UI design. 111 methodologies |
| `faion-devops-engineer` | Docker, K8s, Terraform, AWS/GCP/Azure, CI/CD, monitoring, IaC, nginx. 20 methodologies |
| `faion-ml-engineer` | LLM APIs, RAG, embeddings, fine-tuning, LangChain, vector DBs, prompt engineering. 30 methodologies |
| `faion-marketing-manager` | GTM, landing pages, SEO/SEM, content, ads, email, social media. 74 methodologies |
| `faion-project-manager` | Project Management Framework 7/8 (8 Domains, 12 Principles), PM tools, risk, EVM, agile. 36 methodologies |
| `faion-business-analyst` | Business Analysis Framework: 6 Knowledge Areas, requirements, stakeholders, process modeling. 30 tasks |
| `faion-ux-ui-designer` | 10 Usability Heuristics, UX research, usability testing, personas, journey mapping. 32 methodologies |
| `faion-communicator` | Stakeholder dialogue, Mom Test, conflict resolution, feedback, selling ideas, storytelling, negotiation. 10 methodologies |
| `faion-claude-code` | Claude Code config: skills, agents, commands, hooks, MCP servers, IDE integrations |
| `faion-net` | This orchestrator (recursive for complex multi-domain tasks) |

---

## Step 3: Skill Selection

Use the [Decision Trees](decision-trees.md) to select the appropriate skill.

### Quick Decision Flowchart

```
User Intent                         → Skill to Invoke
─────────────────────────────────────────────────────
Research/Discovery                  → faion-researcher
Architecture/Design Patterns        → faion-software-architect
Product Planning (MVP, roadmap)     → faion-product-manager
Writing Code                        → faion-software-developer
Infrastructure/Deployment           → faion-devops-engineer
AI/ML/LLM                          → faion-ml-engineer
Marketing/GTM                       → faion-marketing-manager
UX/UI Design                        → faion-ux-ui-designer
Project Management                  → faion-project-manager
Business Analysis                   → faion-business-analyst
Communication/Stakeholders          → faion-communicator
Hiring/HR                          → faion-hr-recruiter
SDD Workflow                        → faion-sdd
Claude Code Setup                   → faion-claude-code
```

### Multi-Skill Orchestration

For complex tasks spanning multiple domains, use orchestration patterns:

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Sequential** | Tasks have dependencies | Research → Product → Dev → Deploy |
| **Parallel** | Independent tasks | Dev + Marketing + DevOps (launch prep) |
| **Iterative** | Feedback cycles | UX ↔ Dev (design-dev loop) |

See [Decision Trees](decision-trees.md) for detailed guidance.

---

## Methodologies Catalog

**502 methodologies** organized by domain. Full catalog: [methodologies-catalog.md](methodologies-catalog.md)

| Category | Count | Domain Skill |
|----------|-------|--------------|
| Research | 14 | faion-researcher |
| Product | 18 | faion-product-manager |
| Development | 68 | faion-software-developer |
| DevOps | 20 | faion-devops-engineer |
| ML/AI | 30 | faion-ml-engineer |
| Marketing | 40 | faion-marketing-manager |
| Growth | 12 | faion-marketing-manager |
| Advertising | 16 | faion-marketing-manager |
| Business Operations | 14 | faion-marketing-manager |
| Project Management | 32 | faion-project-manager |
| Business Analysis | 12 | faion-business-analyst |
| UX/UI | 32 | faion-ux-ui-designer |
| SDD | 12 | faion-sdd |
| Communication | 10 | faion-communicator |
| HR/Recruiting | 45 | faion-hr-recruiter |

---

## References

**Core:**
- [Decision Trees](decision-trees.md) - Skill and methodology selection
- [Methodologies Catalog](methodologies-catalog.md) - Full 502 methodologies

**SDD Workflow:**
- [Workflow](workflow.md) - Phases, project/feature selection
- [Directory Structure](directory-structure.md) - SDD folder layout
- [Quality Assurance](quality-assurance.md) - Confidence checks, reflexion

**Domains:**

| Domain | Reference | Skill |
|--------|-----------|-------|
| SDD | [sdd-domain.md](sdd-domain.md) | faion-sdd |
| Research | [research-domain.md](research-domain.md) | faion-researcher |
| Product | [product-domain.md](product-domain.md) | faion-product-manager |
| Development | [development-domain.md](development-domain.md) | faion-software-developer |
| DevOps | [development-domain.md](development-domain.md) | faion-devops-engineer |
| Marketing | [marketing-domain.md](marketing-domain.md) | faion-marketing-manager |
| PM | [pm-domain.md](pm-domain.md) | faion-project-manager |
| BA | [ba-domain.md](ba-domain.md) | faion-business-analyst |
| UX/UI | [ux-domain.md](ux-domain.md) | faion-ux-ui-designer |
| AI/LLM | [ai-llm-domain.md](ai-llm-domain.md) | faion-ml-engineer |

---

*Faion Network v2.1*
*15 Domain Skills | 502 Methodologies | 60+ Agents*
