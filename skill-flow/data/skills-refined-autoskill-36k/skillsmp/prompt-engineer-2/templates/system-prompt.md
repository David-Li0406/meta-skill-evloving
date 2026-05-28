# System Prompt Template

## Purpose

Template for creating Claude system prompts with all essential sections.

---

## Complete Template

```xml
<role>
You are a [EXPERTISE] that [CAPABILITY].
You have deep knowledge of [DOMAIN_1], [DOMAIN_2], and [DOMAIN_3].
Your communication style is [STYLE: professional/casual/technical/friendly].
</role>

<context>
## Background
[Relevant background information the model needs to understand]

## Current Situation
[What state the system is in, any prior context]

## Key Constraints
[Environmental or business constraints]
</context>

<instructions>
## Primary Objective
[The main goal of interactions]

## Process
Follow these steps for each interaction:

1. **Understand**: Parse the user's request to identify:
   - Main objective
   - Constraints or preferences
   - Required format

2. **Analyze**: Consider:
   - Relevant context from above
   - Applicable patterns or approaches
   - Potential edge cases

3. **Execute**: Perform the task:
   - [Specific step 1]
   - [Specific step 2]
   - [Specific step 3]

4. **Validate**: Before responding:
   - Check against constraints
   - Verify format compliance
   - Ensure completeness
</instructions>

<format>
## Output Structure

<section name="summary">
Brief summary (1-2 sentences)
</section>

<section name="details">
Detailed response organized by:
- Point 1
- Point 2
- Point 3
</section>

<section name="next_steps" optional="true">
Suggested follow-up actions
</section>
</format>

<examples>
<example name="standard_case">
<user_input>
[Example user request]
</user_input>
<assistant_response>
[Example response following format]
</assistant_response>
</example>

<example name="edge_case">
<user_input>
[Unusual or challenging request]
</user_input>
<assistant_response>
[How to handle gracefully]
</assistant_response>
</example>
</examples>

<constraints>
## Do
- [Positive instruction 1]
- [Positive instruction 2]
- [Positive instruction 3]

## Do NOT
- [Negative instruction 1]
- [Negative instruction 2]
- [Negative instruction 3]

## Limitations
- [What you cannot do]
- [When to escalate or decline]
</constraints>

<error_handling>
## When Uncertain
- Ask clarifying questions before proceeding
- State assumptions explicitly
- Offer alternatives if request is impossible

## When Request is Out of Scope
- Politely explain limitation
- Suggest alternative approaches
- Redirect to appropriate resources
</error_handling>
```

---

## Section Guidelines

### Role Section
- **Length**: 2-4 sentences
- **Include**: Expertise, capabilities, communication style
- **Avoid**: Vague descriptors, contradictions

### Context Section
- **Length**: 3-6 bullet points or short paragraphs
- **Include**: Background, current state, constraints
- **Avoid**: Outdated information, implementation details

### Instructions Section
- **Length**: 3-7 numbered steps
- **Include**: Clear process, decision points
- **Avoid**: Ambiguous language, optional steps without markers

### Format Section
- **Length**: Complete output structure
- **Include**: All expected sections, optional markers
- **Avoid**: Complex nesting, unmarked optional parts

### Examples Section
- **Count**: 2-3 examples
- **Include**: Happy path, edge case
- **Avoid**: Trivial examples, too similar examples

### Constraints Section
- **Length**: 3-5 items per category
- **Include**: Do's, Don'ts, Limitations
- **Avoid**: Redundant constraints, contradictions

---

## Minimal Template (for simpler use cases)

```xml
<role>
You are a [EXPERTISE] that [CAPABILITY].
</role>

<instructions>
1. [Step 1]
2. [Step 2]
3. [Step 3]
</instructions>

<format>
[Expected output structure]
</format>

<example>
Input: [example]
Output: [example]
</example>

<constraints>
- Do NOT [constraint]
- Always [requirement]
</constraints>
```

---

## Version

**Version**: 1.0.0
