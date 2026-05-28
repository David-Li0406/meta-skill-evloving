---
name: faion-researcher
description: "Researcher role: idea generation (SCAMPER, mind maps), market research, competitor analysis, persona building, pricing research, problem validation, niche evaluation, project naming, trend analysis. AI-powered research, Continuous Discovery. 9 research modes. 32 methodologies."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite
---

# Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrate all research and discovery activities for product/startup development. This domain skill combines idea discovery, product research, and project naming into a unified research workflow.

---

## Agents (2)

| Agent | Model | Purpose | Modes |
|-------|-------|---------|-------|
| faion-research-agent | opus | Research orchestrator | ideas, market, competitors, pains, personas, validate, niche, pricing, names |
| faion-domain-checker-agent | sonnet | Domain availability verification | - |

**Mode Mapping:**
| Mode | Replaces | Output |
|------|----------|--------|
| ideas | faion-research-agent (mode: ideas) | 15-20 candidates |
| market | faion-research-agent (mode: market) | market-research.md |
| competitors | faion-research-agent (mode: competitors) | competitive-analysis.md |
| pains | faion-research-agent (mode: pains) | pain-points.md |
| personas | faion-research-agent (mode: personas) | user-personas.md |
| validate | faion-research-agent (mode: validate) | problem-validation.md |
| niche | faion-research-agent (mode: niche) | niche-evaluation.md |
| pricing | faion-research-agent (mode: pricing) | pricing-research.md |
| names | faion-research-agent (mode: names) | name-candidates.md |

---

## Methodologies (20)

| Methodology | Description | Agent (Mode) |
|-------------|-------------|--------------|
| idea-generation | Pain, Passion, Profession, Process, Platform, People, Product | ideas |
| paul-graham-questions | Tedious tasks, surprisingly hard, build for self | ideas |
| pain-point-research | Daily problems, complaints, workarounds | ideas |
| niche-evaluation | Multi-criteria scoring (market, competition, fit) | niche |
| market-research-tam-sam-som | Total, Serviceable, Obtainable market sizing | market |
| trend-analysis | Industry trends, growth drivers, threats | market |
| competitor-analysis | Direct, indirect, substitute competitors | competitors |
| competitive-intelligence | Missing features in competitor products | competitors |
| pricing-research | Competitor pricing models comparison | pricing |
| jobs-to-be-done | Functional, emotional, social jobs | personas |
| persona-building | Demographics, behaviors, pain points, goals | personas |
| problem-validation | Evidence gathering for problem existence | validate |
| pain-point-mining | Reddit, forums, reviews, social listening | pains |
| niche-viability-scoring | 5-criteria scoring (market, competition, barriers, profit, fit) | niche |
| business-model-research | Uncontested market space identification | niche |
| value-proposition-design | Customer profile vs. value map | personas |
| project-naming | Descriptive, invented, compound, metaphor, portmanteau | names |
| domain-availability | .com, .io, .co, social handles | domain-checker |
| user-interviews | Discovery interviews, problem interviews | validate |
| customer-interview-framework | Interview structure, questions, anti-patterns | validate |

> **Full details:** [methodologies-detail.md](methodologies-detail.md)

---

## References

| Reference | Content | Lines |
|-----------|---------|-------|
| [methodologies-detail.md](methodologies-detail.md) | Full methodology templates, examples, frameworks | ~1500 |

---

## Decision Tree: Mode Selection

```
What is your research goal?
|
+-- "I need a startup idea"
|   |
|   +-- Have skills/context? --> YES --> mode: ideas
|   |                       --> NO  --> Gather context first, then mode: ideas
|   |
|   +-- Have idea, need validation? --> mode: pains --> mode: niche
|
+-- "I need to understand the market"
|   |
|   +-- Market size/trends? --> mode: market
|   +-- Competitor landscape? --> mode: competitors
|   +-- Pricing benchmarks? --> mode: pricing
|
+-- "I need to understand users"
|   |
|   +-- Who are they? --> mode: personas
|   +-- What problems do they have? --> mode: pains
|   +-- Does problem exist? --> mode: validate
|
+-- "I need a project name"
|   |
|   +-- Generate names --> mode: names
|   +-- Check availability --> faion-domain-checker-agent
|
+-- "Full research package"
    |
    +-- Run sequentially: market --> competitors --> personas --> validate --> pricing
```

---

## Decision Tree: Methodology Selection

### Idea Generation
```
What's your starting point?
|
+-- "I have skills/expertise" --> idea-generation (7 Ps)
+-- "I face daily frustrations" --> pain-point-research
+-- "I want proven patterns" --> paul-graham-questions
+-- "I have multiple ideas" --> niche-evaluation (score & rank)
```

### Market Understanding
```
What do you need to know?
|
+-- "How big is the market?" --> market-research-tam-sam-som
+-- "Is the market growing?" --> trend-analysis
+-- "Who are competitors?" --> competitor-analysis
+-- "What features are missing?" --> competitive-intelligence
+-- "What should we charge?" --> pricing-research
```

### User Research
```
What stage are you at?
|
+-- "Who is the user?" --> persona-building
+-- "What jobs do they have?" --> jobs-to-be-done
+-- "What pains exist?" --> pain-point-mining
+-- "Is the problem real?" --> problem-validation
+-- "What do they value?" --> value-proposition-design
+-- "Need interview structure?" --> customer-interview-framework / user-interviews
```

### Niche & Business Model
```
What decision do you need?
|
+-- "Is this niche viable?" --> niche-viability-scoring
+-- "How to differentiate?" --> business-model-research (Blue Ocean)
+-- "Score multiple ideas" --> niche-evaluation
```

### Naming
```
What do you need?
|
+-- "Generate name ideas" --> project-naming
+-- "Check if available" --> domain-availability
```

---

## Workflow: Idea Discovery

```
1. Gather Context (AskUserQuestion)
   - Skills, interests, resources
   |
   v
2. Generate Ideas (mode: ideas)
   - Apply 7 Ps framework + other methods
   |
   v
3. User Selection (AskUserQuestion)
   - Pick 3-5 ideas to research
   |
   v
4. Pain Point Research (mode: pains)
   - Reddit, forums, reviews mining
   |
   v
5. Niche Evaluation (mode: niche)
   - Market size, competition, barriers
   |
   v
6. Present Results
   |
   +-- User selects idea? --> YES --> Write to product_docs/idea-validation.md
   |                      --> NO  --> Loop back to step 2
```

### Context Gathering Questions

```
Question 1: "What are your skills/experience?"
Options: Software development | Design/UX | Marketing/Sales | Domain expertise

Question 2: "What motivates you?"
Options: Solve my own problem | Big market opportunity | Passion project | Side income

Question 3: "How much time can you invest?"
Options: Nights & weekends | Part-time (20h/week) | Full-time
```

---

## Workflow: Product Research

```
1. Parse project from ARGUMENTS
2. Read: constitution.md, roadmap.md
3. AskUserQuestion: modules + mode (quick/deep)
4. Run agents SEQUENTIALLY (not parallel)
5. Write executive-summary.md
```

### Module Selection

```python
AskUserQuestion(
    questions=[{
        "question": "Which modules to run?",
        "multiSelect": True,
        "options": [
            {"label": "Market Research", "description": "TAM/SAM/SOM, trends"},
            {"label": "Competitors", "description": "Features, pricing"},
            {"label": "Personas", "description": "Pain points, JTBD"},
            {"label": "Validation", "description": "Problem evidence"},
            {"label": "Pricing", "description": "Benchmarks"}
        ]
    }]
)
```

### Research Modes

| Mode | Searches | Depth |
|------|----------|-------|
| Quick | 3-5 | Surface-level trends |
| Deep | 8-12 | Detailed analysis |

---

## Workflow: Project Naming

```
1. Gather Concept (AskUserQuestion)
   - Description, tone (Professional/Playful/Technical/Premium)
   |
   v
2. Generate Names (mode: names)
   - 15-20 candidates using 7 strategies
   |
   v
3. User Selection (AskUserQuestion, multiSelect)
   - Select favorites or "generate more"
   |
   v
4. Check Domains (faion-domain-checker-agent)
   - .com, .io, .co, GitHub, Twitter
   |
   v
5. Present Results
   |
   +-- Final selected? --> YES --> Update constitution.md
   |                   --> NO  --> Loop to step 2
```

### Naming Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| Descriptive | What it does | DropBox |
| Invented | Made-up word | Spotify |
| Compound | Two words | Facebook |
| Metaphor | Symbolic meaning | Amazon |
| Portmanteau | Blended words | Pinterest |
| Alliteration | Same sound | PayPal |
| Acronym | Letter combination | IBM |

### Name Scoring

| Factor | Points |
|--------|--------|
| .com available | 10 |
| .io available | 5 |
| No trademark | 5 |
| GitHub available | 3 |
| Twitter available | 3 |
| Easy to spell | 2 |
| **Max Total** | **28** |

---

## Quick Reference: Frameworks

### 7 Ps of Ideation

| P | Question | Example |
|---|----------|---------|
| **Pain** | What frustrates you daily? | Scheduling meetings across timezones |
| **Passion** | What do you love doing? | Teaching coding to kids |
| **Profession** | What's broken in your industry? | Medical billing complexity |
| **Process** | What workflow is inefficient? | Code review bottlenecks |
| **Platform** | What can be improved on existing platform? | Better Slack integrations |
| **People** | Who do you know with problems? | Freelancers need invoicing |
| **Product** | What product do you wish existed? | AI meeting summarizer |

### Paul Graham's Questions

- What's tedious but necessary?
- What's surprisingly hard to do?
- What do you find yourself building for yourself?
- What would you pay for that doesn't exist?

### Niche Evaluation Criteria

| Criterion | 1-3 | 4-6 | 7-10 |
|-----------|-----|-----|------|
| **Market size** | <$10M | $10M-100M | >$100M |
| **Competition** | Red ocean | Moderate | Blue ocean |
| **Barriers** | High (capital, regulatory) | Medium | Low |
| **Profitability** | Thin margins | Ok margins | High margins |
| **Fit** | No relevant skills | Some skills | Perfect match |

**Total score interpretation:**
- 40-50: Excellent opportunity
- 30-39: Good potential
- 20-29: Proceed with caution
- <20: Consider other ideas

### Validation Criteria

| Criterion | Threshold | How to Measure |
|-----------|-----------|----------------|
| Frequency | Weekly+ | "How often do you face this?" |
| Intensity | 7+/10 | "How painful is this? (1-10)" |
| WTP | Yes | "Would you pay to solve this?" |
| Search | Exists | Check search volume |
| Competition | Exists | Someone trying to solve it |

---

## Quick Reference: Agent Invocation

### Idea Generation
```python
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt="Generate ideas using 7 Ps framework for: {context}"
)
```

### Market Research
```python
Task(
    subagent_type="faion-research-agent (mode: market)",
    prompt="Research TAM/SAM/SOM for {product}"
)
```

### Competitor Analysis
```python
Task(
    subagent_type="faion-research-agent (mode: competitors)",
    prompt="Analyze competitors for {product}"
)
```

### Pain Point Mining
```python
Task(
    subagent_type="faion-research-agent (mode: pains)",
    prompt="Research pain points for: {idea}"
)
```

### Persona Building
```python
Task(
    subagent_type="faion-research-agent (mode: personas)",
    prompt="Create personas using JTBD for {product}"
)
```

### Problem Validation
```python
Task(
    subagent_type="faion-research-agent (mode: validate)",
    prompt="Validate problem: {problem_statement}"
)
```

### Niche Evaluation
```python
Task(
    subagent_type="faion-research-agent (mode: niche)",
    prompt="Evaluate niche viability for: {idea}"
)
```

### Pricing Research
```python
Task(
    subagent_type="faion-research-agent (mode: pricing)",
    prompt="Research pricing for {product}"
)
```

### Project Naming
```python
Task(
    subagent_type="faion-research-agent (mode: names)",
    prompt="Generate names for {product_description}"
)
```

### Domain Check
```python
Task(
    subagent_type="faion-domain-checker-agent",
    prompt="Check availability for: {name}"
)
```

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Idea Discovery | idea-validation.md |
| Market Research | market-research.md |
| Competitors | competitive-analysis.md |
| Personas | user-personas.md |
| Validation | problem-validation.md |
| Pricing | pricing-research.md |
| Summary | executive-summary.md |
| Naming | Updates constitution.md |

---

## Error Handling

| Error | Action |
|-------|--------|
| No ideas resonate | Try different framework, ask about hobbies |
| No pain points found | Broaden search, try adjacent problems |
| High competition | Look for underserved segment |
| User rejects all ideas | Generate more with different angle |
| All .com taken | Suggest .io, check premium domains |
| Trademark conflict | Remove name, note reason |
| Data not found | Mark as "Data not available", continue |

---

## Integration

### Entry Point

This skill is invoked via `/faion-net` when user intent is research-related:

```python
if intent in ["idea", "research", "market", "competitors", "naming", "personas", "pricing"]:
    invoke("faion-researcher")
```

### Next Steps After Research

After research complete, offer:
- "Create GTM Manifest?" --> Call `faion-marketing-manager`
- "Create spec.md?" --> Call `faion-sdd`
- "Start development?" --> Call `faion-software-developer`

---

## Rules

- Run agents ONE BY ONE (sequential, not parallel)
- Agents cite sources with URLs
- If data not found --> "Data not available"
- Quick mode: 3-5 searches, Deep mode: 8-12 searches

---

*faion-researcher v1.2*
*Optimized: methodology details extracted to methodologies-detail.md*
*Methodologies: 20 total (semantic names)*
*Agents: 2 (faion-research-agent, faion-domain-checker-agent)*
