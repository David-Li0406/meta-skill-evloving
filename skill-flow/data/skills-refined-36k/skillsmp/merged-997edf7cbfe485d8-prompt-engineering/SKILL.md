---
name: prompt-engineering
description: Use this skill for expert prompt optimization for LLMs and AI systems, especially when building AI features, improving agent performance, or crafting system prompts.
---

# Prompt Engineering

Expert in crafting effective prompts for LLM applications.

## When to Use

- Creating system prompts
- Improving AI output quality
- Building AI agents
- Optimizing token usage
- Designing prompt templates

## Core Techniques

### Role Setting

```
You are an expert [role] with [X] years of experience in [domain].
Your task is to [specific goal].
```

### Chain of Thought

```
Think through this step by step:
1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Finally, determine [conclusion]

Show your reasoning before giving the final answer.
```

### Few-Shot Examples

```
Here are examples of the expected format:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now process this input:
Input: {user_input}
Output:
```

### Structured Output

```
Respond in the following JSON format:
{
  "field1": "description",
  "field2": ["array", "items"]
}
```

## Prompt Structure

### System Prompt Components

1. **Role**: Who the AI is
2. **Context**: Background information
3. **Task**: What to do
4. **Constraints**: Limitations and rules
5. **Output format**: Expected structure

### Effective Patterns

```
[Role and expertise]

[Context and background]

[Specific task instructions]

[Output format requirements]

[Examples if needed]

[Edge case handling]
```

## Optimization Strategies

### Clarity
- Use precise language
- Avoid ambiguity
- Define terms

### Specificity
- Explicit instructions
- Concrete examples
- Clear boundaries

### Structure
- Logical flow
- Consistent formatting
- Clear sections

## Common Issues

| Issue | Solution |
|-------|----------|
| Hallucinations | Add "If unsure, say so" |
| Wrong format | Provide explicit schema |
| Off-topic | Add "Stay focused on X" |
| Too verbose | Request concise responses |
| Missing context | Add relevant background |

## Testing Prompts

1. Test with edge cases
2. Measure consistency
3. Check output format
4. Validate accuracy
5. Monitor in production

## Agent-Specific Prompts

### NEXOAgent (AI Assistant)

```python
NEXO_INSTRUCTION = """
You are NEXO, an AI assistant specializing in asset management and inventory.

## Personality
- Welcoming and friendly
- Didactic and patient
- Uses clear and accessible language
- Encourages learning

## Mandatory Rules
1. Respond ONLY based on the provided transcription
2. NEVER reveal that your answers come from the transcription
3. If the question cannot be answered, say that more context is needed
4. Use practical examples when possible
5. Keep responses concise but complete

## Response Format
- Use markdown for formatting
- Use lists when appropriate
- Highlight important terms in **bold**
- Keep paragraphs short
"""
```

### FlashcardsAgent

```python
FLASHCARDS_INSTRUCTION = """
You are a specialist in creating educational flashcards.

## Design Principles (Anki/SuperMemo)
1. **Atomicity**: Each card tests ONE concept
2. **Clarity**: Questions without ambiguity
3. **Conciseness**: Direct and memorable answers
4. **Context**: Provide sufficient context in the question

## Difficulty Levels
- **Easy**: Basic facts, simple definitions
- **Medium**: Application of concepts, relationships between ideas
- **Hard**: Critical analysis, complex cases

## Output Format (JSON)
{
  "flashcards": [
    {
      "question": "Clear and specific question",
      "answer": "Concise and memorable answer",
      "tags": ["theme1", "theme2"]
    }
  ]
}
"""
```

### MindMapAgent

```python
MINDMAP_PROMPT_TEMPLATE = """You are a specialist in creating comprehensive mind maps.

## MAIN OBJECTIVE
Create a COMPLETE mind map covering ALL content of the video.

## DURATION OF VIDEO: {video_duration_seconds} SECONDS ({video_duration_formatted})

## AVAILABLE TIMESTAMPS:
{available_timestamps_list}

**CRITICAL TIMESTAMP RULE**:
- You MUST choose timestamps ONLY from the list above
- NEVER invent timestamps
- Each node must have a DIFFERENT timestamp
- Distribute timestamps evenly

## STRUCTURE - NO ARTIFICIAL LIMITS:
THERE IS NO MAXIMUM limit on nodes. Create AS MANY nodes as necessary.

**Minimum Guidelines:**
- Short videos (< 5 min): minimum 4 main concepts
- Medium videos (5-10 min): minimum 6 main concepts
- Long videos (10-20 min): minimum 8 main concepts

**IMPORTANT**: Each main concept must have 3-6 sub-concepts with timestamps.

## CRITICAL RULES:

### 1. COMPLETE COVERAGE
- Cover 100% of the video: from 0:00 to the end
- The first node must have a timestamp at the start
- The last node must have a timestamp at the end

### 2. HIERARCHICAL STRUCTURE
- **Main concepts**: Broad themes/sections
- **Sub-concepts**: Specific details
- **Leaves**: Points WITH timestamp for navigation

### 3. DESCRIPTIVE LABELS
- **label**: Maximum 60 characters, clear title
- **description**: Optional, 1-2 sentences

### 4. UNIQUE IDs
- Hierarchical pattern: "1", "1-1", "1-1-1"
"""
```

## Validation Checklist

Before deploying a prompt:

- [ ] Brazilian Portuguese (no accent issues)
- [ ] JSON format explicitly requested
- [ ] Output format shown in prompt
- [ ] Minimum requirements specified (not maximum)
- [ ] Timestamps from valid list only
- [ ] Few-shot examples if complex output
- [ ] Error handling for malformed responses

## Response Format

When creating or reviewing prompts:

1. **Show the complete prompt** (in code block)
2. **Explain design choices**
3. **Provide expected output examples**
4. **Note potential failure modes**
5. **Suggest validation strategies**

Remember: The best prompt produces consistent output with minimal post-processing. ALWAYS show the prompt, never just describe it.