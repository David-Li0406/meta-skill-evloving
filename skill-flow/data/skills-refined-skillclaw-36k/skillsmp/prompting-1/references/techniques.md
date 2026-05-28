# Prompt Engineering Techniques

## Few-Shot Prompting

Provide examples of input/output pairs to demonstrate the desired behavior.

**When to use**: Task requires specific format, style, or reasoning pattern.

**Pattern**:
```
Here are examples of the task:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now complete this:
Input: [actual input]
Output:
```

**Tips**:
- Use 2-5 examples (more examples = more consistency, but diminishing returns)
- Choose diverse examples covering edge cases
- Order matters: put most representative examples first

---

## Chain-of-Thought (CoT)

Guide the model to reason step-by-step before answering.

**When to use**: Complex reasoning, math, multi-step logic, analysis.

**Pattern 1 - Explicit instruction**:
```
Think through this step-by-step:
1. First, identify...
2. Then, analyze...
3. Finally, conclude...
```

**Pattern 2 - Zero-shot CoT**:
```
[Question]

Let's think through this step by step.
```

**Pattern 3 - Few-shot CoT**:
```
Q: [example question]
A: Let me work through this:
- Step 1: [reasoning]
- Step 2: [reasoning]
- Therefore: [answer]

Q: [actual question]
A:
```

---

## Role Prompting

Assign a persona or expertise to frame the response.

**When to use**: Domain-specific tasks, particular tone/style, specialized knowledge.

**Pattern**:
```
You are a [role] with expertise in [domain]. Your task is to [action].

[Additional context or constraints]

[The actual request]
```

**Examples**:
- "You are a senior security engineer reviewing code for vulnerabilities..."
- "You are a technical writer creating documentation for developers..."
- "You are a data analyst explaining findings to non-technical stakeholders..."

**Tips**:
- Be specific about expertise level and domain
- Include relevant constraints (tone, audience, format)
- Avoid contradictory roles

---

## Constraint Specification

Explicitly define boundaries, requirements, and limitations.

**When to use**: Precise output requirements, safety constraints, format compliance.

**Pattern**:
```
[Task description]

Requirements:
- Must include: [required elements]
- Must avoid: [prohibited elements]
- Format: [specific format]
- Length: [word/character limits]
- Tone: [formal/casual/technical]
```

**Example**:
```
Write a product description.

Requirements:
- Maximum 150 words
- Include: key features, target audience, call-to-action
- Avoid: technical jargon, superlatives like "best" or "revolutionary"
- Tone: professional but approachable
```

---

## Task Decomposition

Break complex tasks into smaller, manageable subtasks.

**When to use**: Multi-part tasks, complex workflows, reducing errors.

**Pattern**:
```
Complete this task in phases:

Phase 1: [subtask 1]
- Input: [what you'll work with]
- Output: [what to produce]

Phase 2: [subtask 2]
- Input: [output from phase 1]
- Output: [what to produce]

[Continue phases...]

Begin with Phase 1.
```

---

## Output Formatting

Specify exact structure for responses.

**When to use**: Programmatic parsing, consistent reports, structured data.

**Pattern - Markdown**:
```
Format your response as:

## Summary
[1-2 sentence overview]

## Details
- Point 1
- Point 2

## Recommendation
[Actionable next step]
```

**Pattern - JSON**:
```
Return your analysis as JSON:
{
  "summary": "string",
  "score": number,
  "issues": ["string"],
  "recommendation": "string"
}
```

See `references/structured.md` for detailed structured output patterns.

---

## Self-Consistency / Verification

Ask the model to verify or critique its own output.

**When to use**: High-stakes decisions, reducing errors, building confidence.

**Pattern**:
```
[Task]

After completing, verify your work:
1. Check for [specific error type]
2. Confirm [requirement] is met
3. If errors found, correct and show final answer
```

**Pattern - Critique**:
```
[Generate initial response]

Now critique your response:
- What assumptions did you make?
- What could be wrong?
- What would strengthen this answer?

Provide a revised response incorporating your critique.
```

---

## Context Priming

Provide relevant background before the main task.

**When to use**: Domain-specific tasks, maintaining consistency, complex projects.

**Pattern**:
```
Context:
- Project: [brief description]
- Tech stack: [relevant technologies]
- Constraints: [key limitations]
- Previous decisions: [relevant history]

Task:
[The actual request]
```

**Tips**:
- Include only relevant context (avoid information overload)
- Put most important context first
- Reference previous conversation/documents when applicable
