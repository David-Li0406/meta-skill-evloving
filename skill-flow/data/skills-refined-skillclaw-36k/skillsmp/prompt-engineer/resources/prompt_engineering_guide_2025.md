# LLM Prompt Engineering Reference Guide (November 2025)

Comprehensive guide to effective prompting techniques for modern large language models based on current research and validated best practices.

---

## Table of Contents

1. [Introduction & Current Models](#1-introduction--current-models)
   - [Current Model Landscape](#current-model-landscape)
   - [Model Selection Framework](#model-selection-framework)

2. [Core Prompting Techniques](#2-core-prompting-techniques)
   - [Reasoning & Analysis](#reasoning--analysis)
   - [Structured Output Frameworks](#structured-output-frameworks)
   - [Learning Approaches](#learning-approaches)

3. [Software Engineering Prompts](#3-software-engineering-prompts)
   - [Development Workflows](#development-workflows)
   - [Code Generation Patterns](#code-generation-patterns)
   - [Debugging Strategies](#debugging-strategies)

4. [Advanced Techniques](#4-advanced-techniques)
   - [Agentic Patterns](#agentic-patterns)
   - [RAG & Knowledge Integration](#rag--knowledge-integration)
   - [Multi-Path Analysis](#multi-path-analysis)

5. [Model-Specific Optimizations](#5-model-specific-optimizations)
   - [Claude 4.5 Series](#claude-45-series)
   - [GPT-5 and GPT-4.1](#gpt-5-and-gpt-41)
   - [Reasoning Models (o3, DeepSeek R1)](#reasoning-models-o3-deepseek-r1)
   - [Gemini 2.5](#gemini-25)

6. [Quick Reference](#6-quick-reference)
   - [Validated Techniques](#validated-techniques)
   - [Debunked Myths](#debunked-myths)
   - [Common Pitfalls](#common-pitfalls)
   - [Performance Benchmarks](#performance-benchmarks)

---

## 1. Introduction & Current Models

### Current Model Landscape

| Model | Version | Best For | Context Window | Key Feature |
|-------|---------|----------|----------------|-------------|
| **Claude Sonnet 4.5** | Sept 2025 | Default choice, coding, agents | 200K (1M beta) | Extended thinking, 77.2% SWE-bench |
| **Claude Haiku 4.5** | Oct 2025 | Speed, cost optimization | 200K | 2-5x faster, frontier performance |
| **Claude Opus 4.1** | Aug 2025 | Maximum capability | 200K | Best for complex refactoring |
| **GPT-5** | Oct 2025 | General purpose | Large | 2 trillion parameters |
| **GPT-4.1** | 2025 | Agentic tasks | Large | Optimized for tool use |
| **o3 / o3-mini** | 2025 | Deep reasoning | N/A | Specialized reasoning model |
| **DeepSeek R1** | Jan 2025 | Cost-effective reasoning | 128K | 27x cheaper than o3, open source |
| **Gemini 2.5 Pro** | 2025 | Multimodal | Large | Best pricing ($1.25/$10 per M tokens) |

### Model Selection Framework

**Claude Sonnet 4.5:** Default for most tasks, coding, autonomous agents (30+ hour focus), computer use. Best capability/cost balance.

**Claude Haiku 4.5:** Speed-critical (2-5x faster), high-volume processing, sub-agents, cost optimization. Frontier performance at 1/3 price.

**Claude Opus 4.1:** Maximum capability needs, complex multi-file refactoring, intricate multi-agent frameworks when cost isn't primary concern.

**GPT-5:** Broad general knowledge, non-coding tasks, massive parameter count benefits.

**o3 or DeepSeek R1:** Deep reasoning, mathematical/logical proofs, scientific analysis. DeepSeek for budget constraints (27x cheaper).

**Gemini 2.5 Pro:** Multimodal inputs, cost optimization at high volumes, competitive pricing with strong performance.

---

## 2. Core Prompting Techniques

### Reasoning & Analysis

#### Chain-of-Thought (CoT) Prompting

**What it is:** Instructs the model to show reasoning step-by-step before providing a final answer.

**When to use:** Complex problems requiring logical reasoning, mathematical calculations, multi-step analysis, debugging.

**How to use:**

```
Solve this problem step by step:
A company's revenue was $500K in Q1. In Q2, it increased by 15%.
In Q3, it decreased by 10% from Q2. What was the Q3 revenue?

Show your work:
1. Calculate Q2 revenue
2. Calculate Q3 revenue
3. Provide the final answer
```

**Why it works:** Forces sequential processing, reducing errors. Research: 80.2% accuracy vs 34% baseline. "Take a deep breath and work step-by-step" is validated to improve performance.

**Advanced variants:**
- **Chain-of-Table:** Tabular data analysis, 8.69% improvement over standard CoT
- **Plan-and-Solve:** Generates plan first, then executes, 7-27% gains

#### Tree of Thought (ToT)

**What it is:** Explores multiple reasoning paths simultaneously, then evaluates which leads to the best solution.

**When to use:** Decision-making with multiple options, strategic planning, trade-off analysis.

**How to use:**

```
Analyze this decision using Tree of Thought:

Decision: Should we migrate our database from PostgreSQL to MongoDB?

Explore three paths:
Path 1: Migrate fully to MongoDB
  - List all advantages
  - List all disadvantages
  - Estimate effort and risk

Path 2: Keep PostgreSQL
  - List reasons to stay
  - List current pain points
  - Estimate opportunity cost

Path 3: Hybrid approach (both databases)
  - Describe the hybrid architecture
  - List pros and cons
  - Estimate complexity

After exploring all three paths, evaluate which approach is best and why.
```

**Why it works:** Prevents premature optimization and tunnel vision through systematic exploration.

#### Self-Consistency for Reliability

**What it is:** Generate multiple independent analyses, then identify themes appearing consistently across all.

**When to use:** High-stakes decisions, complex problems with uncertainty, validating outputs, reducing single-path errors.

**How to use:**

```
Generate 3 different analyses of employee retention challenges in tech companies:

Analysis 1: From an organizational psychology perspective
Analysis 2: From a labor economics perspective
Analysis 3: From an HR management perspective

After completing all three, identify convergent themes and recommendations.
```

**Why it works:** Multiple reasoning chains converging on same conclusions catch model uncertainty and single-path errors.

#### Extended Thinking (Claude-Specific)

**What it is:** Claude 4.5 performs additional reasoning before response generation, visible to you.

**When to use:** Complex coding, deep analysis, multi-step logical reasoning, problems requiring careful consideration.

**How to invoke:**

Via API:
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  },
  "messages": [...]
}
```

Via Claude.ai: Toggle "Extended thinking" mode (requires Pro/Max/Team/Enterprise)

**Why it works:** Dedicated computational budget for reasoning achieves 5-7% performance gains. Thinking happens BEFORE response.

**Key notes:** Minimum 1,024 tokens, charged at output rates, supports tool use (beta).

### Structured Output Frameworks

#### CO-STAR Framework for Writing

**Components:** **C**ontext, **O**bjective, **S**tyle, **T**one, **A**udience, **R**esponse format

**When to use:** Marketing copy, technical documentation, business communications, content creation.

**How to use:**

```
Context: Launching new API feature for real-time webhook notifications for payment events.

Objective: Write product announcement blog post generating excitement and driving adoption.

Style: Technical but accessible, conversational yet professional

Tone: Enthusiastic and developer-friendly

Audience: Software developers and engineering teams integrating with our payment API

Response format:
- Catchy headline
- Opening paragraph (2-3 sentences)
- "What's New" section with technical details
- "Why This Matters" section
- "Getting Started" section with code example
- Call-to-action
```

**Why it works:** Won prompt engineering competitions. Ensures all critical dimensions are specified.

#### ROSES Framework for Decisions

**Components:** **R**ole, **O**bjective, **S**cenario, **E**xpected Output, **S**tyle

**When to use:** Strategic business decisions, technical architecture choices, resource allocation, risk assessment.

**How to use:**

```
Role: Act as a CTO evaluating infrastructure decisions

Objective: Decide whether to adopt Kubernetes for our microservices architecture

Scenario:
- Currently running 12 microservices on EC2 with manual deployment
- Team of 8 engineers, 3 have container experience
- Growing 30% quarter-over-quarter
- Need to improve deployment speed and reliability

Expected Output:
- Recommendation (Yes/No/Phased)
- 3-5 key decision factors
- Risk assessment
- Implementation timeline if recommended

Style: Data-driven, practical, focused on team capabilities and business impact
```

**Why it works:** Structures complex decisions with clear boundaries, producing actionable recommendations vs generic analysis.

### Learning Approaches

#### Few-Shot Learning

**What it is:** Providing 3-5 examples of desired input-output pattern before asking model to perform task.

**When to use:** Custom output formats, specific writing styles, pattern matching, domain conventions. **Standard models ONLY** (NOT reasoning models).

**How to use:**

```
Extract key information from product reviews into structured format.

Example 1:
Input: "Great laptop, fast processor but battery life could be better. Worth the price."
Output: {sentiment: "positive", pros: ["fast processor", "good value"], cons: ["battery life"], rating_implied: 4}

Example 2:
Input: "Terrible build quality. Broke after 2 weeks. Don't waste your money."
Output: {sentiment: "negative", pros: [], cons: ["build quality", "durability"], rating_implied: 1}

Now extract information from this review:
"Amazing screen quality and super lightweight. The speakers are weak though. Great for travel."
```

**Why it works:** Shows model exact pattern, reducing ambiguity. Effective with standard models (GPT-4, Claude Sonnet, Gemini).

**CRITICAL WARNING:** Few-shot **harms** reasoning models (o1, o3, DeepSeek R1). Use zero-shot for these models.

#### Zero-Shot Prompting

**What it is:** Task instructions without examples, relying on model's pre-training.

**When to use:** Reasoning models (o1, o3, DeepSeek R1) - **REQUIRED**, simple common tasks, when examples might bias output.

**How to use:**

```
Analyze this code for potential security vulnerabilities:

[CODE HERE]

For each vulnerability found:
- Describe the issue
- Explain the potential impact
- Provide a secure alternative
```

**Why it works:** Adding examples to reasoning models interferes with their internal reasoning process.

**Best practice:** Start zero-shot. Add few-shot only if: (1) NOT using reasoning model, (2) output quality insufficient, (3) need very specific format.

---

## 3. Software Engineering Prompts

### Development Workflows

#### Architecture-First Prompting

**Pattern:** Context → Goal → Constraints → Technical Requirements

**When to use:** New features, refactoring, integrating with existing codebases, complex implementations.

**How to use:**

```
Context: Express.js API with PostgreSQL. JWT tokens stored in PostgreSQL sessions table.

Goal: Implement rate limiting to prevent API abuse on authentication endpoints.

Constraints:
- Must work with existing JWT auth system
- Should not add latency >10ms
- Scale across multiple API server instances
- Cannot require additional database queries per request

Technical Requirements:
- Use Redis for distributed rate limit tracking
- Implement sliding window algorithm
- Different limits for authenticated vs unauthenticated
- Configurable limits per endpoint

Provide architecture design first, then implement core rate limiting middleware.
```

**Why it works:** Prevents code solving wrong problem or violating constraints. Establishes clear boundaries upfront.

#### Security-First Two-Stage Prompting

**What it is:** Generate functional code first, then explicitly harden for security.

**When to use:** Code handling user input, authentication/authorization, payments, database queries, file operations, API integrations.

**How to use:**

Stage 1:
```
Implement user registration endpoint:
- Accept email, password, username
- Validate email format
- Hash password with bcrypt
- Store in PostgreSQL users table
- Return success/error response
```

Stage 2:
```
Review the registration endpoint for security vulnerabilities:

[PASTE CODE FROM STAGE 1]

Harden against: SQL injection, email injection, password policy (min 12 chars, complexity),
rate limiting, input sanitization, error message information disclosure.
```

**Why it works:** 40%+ of AI code has vulnerabilities without security prompting. Two-stage reduces by 50%+. Catches missing input validation (16-18% of code) and hardcoded credentials.

#### Test-Driven Development with AI

**What it is:** Write comprehensive test cases first, then AI implements code until tests pass.

**When to use:** Critical business logic, complex algorithms, reducing hallucination, ensuring correctness, refactoring.

**How to use:**

```
Write comprehensive test cases for a function validating credit card numbers using Luhn algorithm.

Cover: Valid cards (Visa, MasterCard, Amex), invalid cards (wrong checksum), edge cases
(all zeros, all nines, single digit), invalid input (non-numeric, null, undefined, empty),
length validation (too short, too long).

First provide test suite, then implement function making all tests pass.
```

**Why it works:** Tests act as formal specification, dramatically reducing hallucination with concrete pass/fail criteria.

### Code Generation Patterns

#### Explicit Instruction Following (Claude 4)

**Why this matters:** Claude 4 follows instructions precisely but won't infer unstated requirements or add features not requested.

**How to adapt:**

❌ Too implicit: `Create a user profile component`

✅ Explicit:
```
Create a React user profile component with:
- Props: userId (string), onEdit (callback), readOnly (boolean)
- Display: avatar image, username, email, bio
- Edit button (only shown when readOnly=false)
- Loading state while fetching user data
- Error state with retry button if fetch fails
- Use Tailwind for styling
- TypeScript with proper type definitions
```

**Key principles:** State all requirements, specify error handling, define expected behaviors, list edge cases, provide context about WHY.

**Why it works:** Claude 4's architecture prioritizes instruction-following over inference.

#### Iterative Refinement Pattern

**What it is:** Generate initial code, then iteratively improve specific aspects in separate prompts.

**When to use:** Complex implementations, uncertain requirements, performance optimization, code review.

**Pattern:**
1. Basic implementation
2. Add features
3. Optimize
4. Production-ready (error handling, logging, types, docs)

**Why it works:** Breaks complexity into manageable pieces. Each iteration focuses on specific aspects. Validate direction before adding complexity.

### Debugging Strategies

#### Structured Debugging Pattern

**Pattern:** Error Message → Stack Trace → Context → Expected Behavior

**How to use:**

```
Error Message:
TypeError: Cannot read property 'map' of undefined at UserList.render (UserList.jsx:23)

Stack Trace:
  at UserList.render (UserList.jsx:23:15)
  at renderComponent (react-dom.js:1847)

Context:
- React component displaying user list
- Data from API endpoint /api/users
- Renders correctly on initial load
- Error on "Refresh" button click
- API call succeeds (200 with valid JSON)

Code: [PASTE RELEVANT CODE]

Expected: Refresh button fetches fresh data and re-renders without errors.

What's causing this and how do I fix it?
```

**Why it works:** Complete context enables root cause analysis vs guessing.

#### First Principles Debugging

**What it is:** Ask model to explain root cause from first principles rather than jumping to solutions.

**When to use:** Persistent bugs, unexpected behavior in complex systems, learning opportunities.

**How to use:**

```
PostgreSQL query extremely slow (5+ seconds) despite index on queried column.

Query: SELECT * FROM orders WHERE user_id = 123 AND created_at > '2025-01-01'
Index: CREATE INDEX idx_orders_user_id ON orders(user_id)
Table size: 10 million rows

Explain from first principles:
1. How PostgreSQL should be using the index
2. Why the index might not be helping
3. What's actually happening during query execution
4. The root cause of the slowness

Then suggest fix with explanation of why it works.
```

**Why it works:** Forces understanding vs pattern matching. Produces learning and prevents recurrence.

---

## 4. Advanced Techniques

### Agentic Patterns

#### ReAct Pattern (Reason + Act)

**Pattern:** Thought → Action → Observation → Thought → Action → ...

**When to use:** Multi-step tasks with tools, research/information gathering, complex problem-solving, autonomous agents.

**How to use:**

```
You are an agent using tools to answer questions. Follow ReAct pattern:

Thought: [Reason about what you need to do next]
Action: [Tool to use and how]
Observation: [Result from tool]
[Repeat until final answer]

Available tools:
- search(query): Search web
- calculate(expression): Evaluate math
- fetch_url(url): Get content from URL

Question: What was the GDP of the country that hosted the 2020 Olympics in the year they hosted?
```

**Why it works:** 20-30% improvement over direct prompting. Explicit reasoning loop prevents actions without thinking.

**Tips:** Define tools clearly, require "Thought" before "Action", allow multiple iterations, parse observations into loop.

#### Reflexion Pattern

**Pattern:** Attempt → Evaluate → Reflect → Retry

**When to use:** Optimization tasks, learning from errors, iterative improvement.

**How to use:**

```
Solve this using Reflexion pattern:

Problem: Implement function finding longest palindromic substring.

Attempt 1: [Implementation]
Evaluation: Test with "babad", "cbbd", "a", "ac"
Reflection: What worked? Failed? Why? Try differently?
Attempt 2: [Improved implementation]
[Repeat until tests pass]
```

**Why it works:** 91% pass@1 on HumanEval. Self-reflection catches initial errors.

#### Multi-Agent Patterns

**Common patterns:** Hierarchical (manager delegates), Sequential (pipeline), Collaborative (multiple inputs synthesized).

**When to use:** Very complex tasks, quality validation, parallel exploration, large-scale projects.

**Example - Collaborative:**

```
Design new API endpoint for payment processing.

Agent 1 (API Designer): Design endpoint spec (method, path, schemas, status codes, auth)
Agent 2 (Security Reviewer): Review for auth vulnerabilities, authorization, input validation, info disclosure
Agent 3 (Performance Engineer): Analyze latency, query efficiency, caching, scalability
Final Synthesizer: Combine insights into final design balancing all concerns.
```

**Why it works:** Specialization enables deep focus. Multiple perspectives catch more issues. Higher quality but higher token cost.

### RAG & Knowledge Integration

#### Preventing Hallucination with RAG

**What it is:** Provide specific documents and instruct model to answer ONLY from that information.

**When to use:** Questions about specific documents, fact-based responses with citations, domain knowledge, preventing confabulation.

**How to use:**

```
Based ONLY on the following documents, answer the question.
If answer not in documents, say "I cannot answer based on provided documents."

Document 1: [CONTENT]
Document 2: [CONTENT]
Document 3: [CONTENT]

Question: [USER QUESTION]

Answer based only on documents above. Cite which document(s) used.
```

**Why it works:** "Based ONLY on" prevents parametric knowledge use, dramatically reducing hallucination.

**Best practices:** Use "ONLY"/"exclusively", explicitly instruct to say when doesn't know, request citations, keep documents focused (quality > quantity).

#### Context Window Optimization

**Key finding:** Models pay most attention to beginning and end ("lost in the middle" problem).

**Best practices:**

1. **Critical information positioning:** Most important at start, supporting in middle, restate key context with query at end.

2. **Structured with markers:**
```
<critical_information>[Most important]</critical_information>
<background>[Additional context]</background>
<task>[What you want done]</task>
```

3. **Relevance ordering:** Most relevant first, least relevant middle, second-most relevant end.

**Why it works:** Combats attention decay across long contexts.

### Multi-Path Analysis

#### Ensemble Methods

**What it is:** Generate multiple independent solutions and synthesize best answer.

**When to use:** High-stakes decisions, complex problems with multiple approaches, quality assurance, creative tasks.

**How to use:**

```
Generate 5 different database schemas for social media app with users, posts, comments, likes.

Solution 1-5: [GENERATE SCHEMAS]

Analyze all 5:
- Strengths of each?
- Trade-offs?
- Which aspects should be combined?

Provide final synthesized solution combining best elements.
```

**Why it works:** Explores solution space thoroughly. Synthesis catches individual weaknesses. Higher quality than single-shot.

#### Debate Pattern

**What it is:** Model argues different positions before reaching conclusion.

**When to use:** Controversial decisions, trade-off analysis, surfacing hidden assumptions, avoiding bias.

**How to use:**

```
Debate: "Should we use microservices or monolith?"

Round 1: Both advocates make strongest cases
Round 2: Both rebut opposing arguments
Round 3: Identify common ground and key trade-offs
Final synthesis: Nuanced recommendation based on debate
```

**Why it works:** Forces multiple perspectives. Reveals assumptions and argument weaknesses. More balanced conclusions.

---

## 5. Model-Specific Optimizations

### Claude 4.5 Series

**Key characteristics:** Requires explicit prompting. No "above and beyond" behavior. Won't add unstated features. Requires explicit error handling. Needs context about WHY. Responds better to positive framing.

#### XML Tags for Structure

**When to use:** Complex prompts with multiple sections, clear separation of examples/instructions/context, nested hierarchies.

**How to use:**

```
<context>
REST API for e-commerce. JWT authentication. PostgreSQL storage. RESTful conventions.
</context>

<requirements>
Create endpoint for updating product inventory:
- PUT /products/{productId}/inventory
- Requires authentication
- Accepts quantity (integer) in body
- Validates quantity non-negative
- Returns updated product with new inventory
</requirements>

<constraints>
- Use existing auth middleware
- Validate user has "inventory_manager" role
- Use database transactions
- Log inventory changes for audit
</constraints>

<examples>
<example>
<request>PUT /products/123/inventory with quantity: 50</request>
<response>{id: 123, name: "Widget", inventory: 50, updated_at: "2025-11-24T10:00:00Z"}</response>
</example>
</examples>

Implement this endpoint.
```

**Why it works:** Claude's training specifically recognizes XML tags for better parsing.

#### Best Practices

1. **Be extremely explicit:** List all requirements including error handling, loading states, edge cases, styling, types.
2. **Provide WHY context:** Explain reason for requirements (e.g., HIPAA compliance for strict passwords).
3. **Positive framing:** "Return descriptive error messages" not "Don't return error codes".
4. **Match format:** JSON prompts for JSON output, code structure for code output, markdown for markdown.

### GPT-5 and GPT-4.1

**Key characteristics:** Latest general-purpose (GPT-5: 2T parameters). GPT-4.1 optimized for agentic workflows and tool use. Both highly literal.

#### Literal Instruction Following

GPT models execute exactly what you ask without creative interpretation.

**Best practices:**

1. **Specify format precisely:** Show exact output structure with example.
2. **Define boundaries explicitly:** "Exactly 3 paragraphs, 3-4 sentences each".
3. **Use JSON mode:** Provide schema for structured output.

#### Tool Use with GPT-4.1

**Best practices:**

1. **Define tools with precise schemas:** Include descriptions for all parameters.
2. **Provide tool use examples:** Show correct calling in system message or few-shot.
3. **Handle tool errors gracefully:** Clear error messages help model adjust.

### Reasoning Models (o3, DeepSeek R1)

**Critical differences:** Zero-shot > few-shot (examples hurt), minimal prompting better, built-in reasoning (no CoT needed), higher latency, different use cases (deep reasoning not rapid generation).

#### When to Use Reasoning Models

**Use for:** Math problems/proofs, complex logical reasoning, scientific analysis, deep thought problems, multi-step solving.

**Don't use for:** Simple retrieval, content generation, code formatting, quick facts, high-throughput (use standard models).

#### Best Practices

1. **Keep prompts simple:** ✅ "Prove square root of 2 is irrational." ❌ "Think step by step. First consider X..."
2. **Don't provide examples:** ✅ "Solve: [PROBLEM]" ❌ "Example 1: [...] Example 2: [...] Now solve..."
3. **Let model show reasoning:** "Solve this problem and show your reasoning: [PROBLEM]"
4. **Trust thinking time:** 30+ seconds is normal and beneficial.

#### DeepSeek R1 vs o3

**Choose DeepSeek R1:** Budget constraints, self-hosting needs, research projects, high-volume reasoning (27x cheaper, MIT license, 128K context).

**Choose o3:** Maximum accuracy required, enterprise SLAs needed, proprietary data (can't self-host).

### Gemini 2.5

**Key characteristics:** Excellent multimodal, competitive pricing ($1.25/$10 per M tokens), temperature-sensitive, strong benchmarks.

#### Temperature Settings

**Critical:** More sensitive than other models. **Keep at 1.0** unless specific reason to change.

**Effects:** 0.0-0.3 (very deterministic, repetitive), 0.4-0.7 (balanced), 0.8-1.0 (creative, recommended), 1.0+ (increasingly random, caution).

#### Best Practices

1. **Default temperature 1.0**
2. **Leverage multimodal:** Combine images + text for richer context
3. **Cost optimization:** Excellent price/performance for high-volume
4. **Structured output:** Use JSON mode for consistent formatting

---

## 6. Quick Reference

### Validated Techniques

**Core Techniques**
- ✅ Chain-of-Thought: 80.2% vs 34% baseline
- ✅ "Take a deep breath and work step-by-step": Simple effective trigger
- ✅ Few-shot (standard models): 3-5 examples optimal
- ✅ Zero-shot (reasoning models): Required for o3, DeepSeek R1
- ✅ Self-consistency: Multiple analyses → convergent conclusions
- ✅ Tree of Thought: Multi-path exploration

**Frameworks**
- ✅ CO-STAR: Wins competitions for writing
- ✅ ROSES: Structured decision support
- ✅ ReAct: 20-30% improvement for complex tasks
- ✅ Reflexion: 91% pass@1 on HumanEval

**Software Engineering**
- ✅ Security-first two-stage: 50%+ reduction in vulnerabilities
- ✅ Test-driven development: Reduces hallucination significantly
- ✅ Architecture-first: Context → Goal → Constraints → Requirements
- ✅ Explicit instructions (Claude 4): Required for best results

**Model-Specific**
- ✅ XML tags (Claude): Improved structure parsing
- ✅ Extended thinking (Claude 4.5): 5-7% reasoning gains
- ✅ Literal formatting (GPT): Precise output control
- ✅ Temperature 1.0 (Gemini): Optimal default

### Debunked Myths

**Don't Work**
- ❌ $200 tip prompting: No consistent effect
- ❌ "Act as an expert": Zero accuracy improvement
- ❌ Politeness ("please", "thank you"): No performance benefit
- ❌ Emotional appeals: Generally ineffective
- ❌ Few-shot for reasoning models: Actively harms performance
- ❌ Vague instructions: Claude 4 won't fill gaps
- ❌ Negative framing: Less effective than positive

**Outdated**
- ❌ GPT-3 era techniques: Modern models fundamentally different
- ❌ Excessive prompt engineering: Many 2022-2023 "tricks" don't help
- ❌ One-size-fits-all: Model-specific optimization critical

### Common Pitfalls

**Pitfall 1: Few-Shot with Reasoning Models**
Problem: Examples reduce o3/DeepSeek R1 accuracy. Solution: Zero-shot only.

**Pitfall 2: Implicit Requirements with Claude 4**
Problem: Won't infer unstated needs. Solution: Extremely explicit about all requirements.

**Pitfall 3: Ignoring Security**
Problem: 40%+ of AI code has vulnerabilities without security prompting. Solution: Two-stage prompting.

**Pitfall 4: Critical Info in Middle**
Problem: Reduced attention in middle ("lost in the middle"). Solution: Place at beginning or end.

**Pitfall 5: Format Mismatch**
Problem: Messy prompt → messy output. Solution: Structure prompt like desired output.

**Pitfall 6: Wrong Model for Task**
Problem: Reasoning model for simple generation, or standard for deep reasoning. Solution: See Model Selection Framework.

**Pitfall 7: Insufficient Context**
Problem: Model lacks info to complete correctly. Solution: Provide code, constraints, requirements, why it matters.

### Performance Benchmarks

**SWE-bench Verified (Code Generation)**
- Claude Sonnet 4.5: **77.2%** (82.0% high compute)
- Claude Opus 4.1: 74.5%
- Claude Haiku 4.5: 73.3%
- Claude Sonnet 4: 72.7%

**HumanEval (Code Correctness)**
- Reflexion pattern: **91% pass@1**
- Standard prompting: ~65% pass@1

**Reasoning Tasks**
- Chain-of-Thought: 80.2%
- Baseline (no CoT): 34%

**Computer Use (OSWorld)**
- Claude Sonnet 4.5: **61.4%** (45% improvement over Sonnet 4)
- Claude Sonnet 4: 42.2%

**Security Improvements**
- Security-first two-stage: **50%+ reduction** in vulnerabilities
- Input validation coverage: 82-84% (vs 16-18% without security prompting)
