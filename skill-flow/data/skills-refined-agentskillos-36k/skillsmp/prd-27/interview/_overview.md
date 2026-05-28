# Interview Process Overview

The interview is the foundation of a good PRD. Your goal is to extract enough information to create a document that can be executed autonomously.

## Mental Model

Think of the interview as building understanding in layers:

```
Layer 4: How do we verify it works?
Layer 3: How do we build it?
Layer 2: What do we need first?
Layer 1: What exactly are we building?
```

Start at the bottom and work up. Don't discuss implementation until you understand the spec. Don't discuss verification until you understand implementation.

## The Four Phases

### Phase 1: Task Type Identification
Understand what kind of work this is. Different types have different approaches.

See `categories/_overview.md` for guidance on selecting and understanding task types.

### Phase 2: Brain Dump
Let the user share everything they know without imposing structure.

See `brain-dump.md` for detailed guidance.

### Phase 3: Clarifying Questions
Based on what they shared, identify gaps and challenge assumptions.

See `clarifying-questions.md` for detailed guidance.

### Phase 4: Confirmation
Present your understanding and get explicit approval before generating.

See `confirmation.md` for detailed guidance.

## Adapting the Process

The interview process adapts to the situation:

| Situation | Adaptation |
|-----------|------------|
| Simple task | Fewer rounds, combine phases |
| Complex task | More rounds, deeper exploration |
| User knows exactly what they want | Move quickly to confirmation |
| User is exploring ideas | Spend more time in clarifying |
| Technical user | Use technical language, fewer explanations |
| Non-technical user | Plain language, more context |

## Quality Indicators

**Good interview:**
- User feels understood
- No significant gaps remain
- Assumptions have been validated
- Scope is clear
- You could write a detailed PRD

**Needs more work:**
- "I think I understand" but can't articulate clearly
- User seems uncertain about your understanding
- Major decisions haven't been made
- Scope is fuzzy

## Key Principles

1. **Listen more than you talk** - The user has the knowledge, you're extracting it
2. **One topic at a time** - Don't overwhelm with multiple questions
3. **Build on answers** - Let the conversation flow naturally
4. **Challenge assumptions** - What they say isn't always complete
5. **Know when to stop** - More questions aren't always better
