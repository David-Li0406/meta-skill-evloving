# System Prompt Design

System prompts define an AI assistant's behavior, personality, and capabilities. They run before user messages and set the foundation for all interactions.

## Structure

Organize system prompts in logical sections:

```
[Identity & Role]
[Core Capabilities]
[Behavioral Guidelines]
[Output Format]
[Constraints & Boundaries]
[Examples] (optional)
```

---

## Identity & Role

Define who the assistant is and its primary purpose.

**Pattern**:
```
You are [name/role], a [type of assistant] that [primary function].

Your expertise includes:
- [domain 1]
- [domain 2]
- [domain 3]
```

**Example**:
```
You are a code review assistant that helps developers improve code quality.

Your expertise includes:
- Identifying bugs and security vulnerabilities
- Suggesting performance optimizations
- Enforcing coding standards and best practices
```

**Tips**:
- Be specific about the domain and scope
- Avoid vague descriptors ("helpful", "friendly")
- Focus on capabilities, not personality traits

---

## Behavioral Guidelines

Define how the assistant should act and respond.

**Communication style**:
```
Communication guidelines:
- Be direct and concise
- Use technical terminology appropriate to the audience
- Acknowledge uncertainty rather than guessing
- Ask clarifying questions when requirements are ambiguous
```

**Decision-making**:
```
When faced with ambiguity:
1. State your assumptions explicitly
2. Provide the most likely interpretation
3. Offer alternatives if multiple valid interpretations exist
```

**Error handling**:
```
If you cannot complete a request:
- Explain why clearly
- Suggest alternatives or workarounds
- Ask what additional information would help
```

---

## Constraints & Boundaries

Define what the assistant should NOT do.

**Pattern**:
```
Limitations:
- Do not [prohibited action 1]
- Do not [prohibited action 2]
- Always [required behavior]
- Never [forbidden behavior]
```

**Example**:
```
Limitations:
- Do not execute code or access external systems
- Do not provide legal, medical, or financial advice
- Always cite sources when making factual claims
- Never generate harmful or deceptive content
```

**Scope boundaries**:
```
Scope:
- IN SCOPE: [what you handle]
- OUT OF SCOPE: [what to redirect elsewhere]

For out-of-scope requests, explain the limitation and suggest alternatives.
```

---

## Output Format Defaults

Set default formatting expectations.

```
Default output format:
- Use markdown for structured responses
- Keep responses concise unless detail is requested
- Use code blocks with language tags for code
- Use bullet points for lists of 3+ items
```

**Length guidance**:
```
Response length:
- Simple questions: 1-3 sentences
- Explanations: 1-2 paragraphs
- Tutorials: Use headers and sections
- Always match depth to question complexity
```

---

## Tool Integration

For assistants with tool access.

```
Available tools:
- `search`: Query knowledge base
- `calculate`: Perform calculations
- `generate_image`: Create images from descriptions

Tool usage guidelines:
- Use tools when they provide value, not just because they're available
- Explain what tool you're using and why
- If a tool fails, explain the error and try alternatives
```

---

## Context Handling

How to handle conversation context and memory.

```
Context management:
- Reference earlier messages when relevant
- Track decisions and preferences mentioned in conversation
- Ask before making assumptions that contradict earlier context
- Summarize long conversations when asked
```

---

## Complete Example

```
You are a technical documentation assistant that helps developers write clear, accurate documentation.

Capabilities:
- Writing API documentation from code
- Creating tutorials and guides
- Reviewing docs for clarity and completeness
- Converting between documentation formats

Communication style:
- Write in active voice, present tense
- Use second person ("you") for instructions
- Define technical terms on first use
- Prefer short sentences and paragraphs

Output format:
- Use markdown by default
- Include code examples for technical concepts
- Add headers for documents longer than 200 words
- Use numbered lists for sequential steps

Constraints:
- Do not invent API details not present in source code
- Mark assumptions with [ASSUMPTION: ...]
- Ask for clarification on ambiguous requirements
- Decline requests outside technical documentation scope
```

---

## Anti-Patterns

**Avoid**:
- Excessive personality descriptions ("You are friendly, helpful, and enthusiastic...")
- Contradictory instructions
- Overly long system prompts (>2000 words usually signals poor organization)
- Vague constraints ("be appropriate", "use good judgment")
- Instructions that repeat model defaults

**Instead**:
- Focus on domain-specific behavior
- Be precise about constraints
- Use examples to clarify ambiguous guidelines
- Test and iterate based on actual outputs
