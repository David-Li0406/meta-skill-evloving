# Clarifying Questions Phase

After the brain dump, you have raw material. Now you refine it by asking targeted questions.

## Purpose

Fill gaps, challenge assumptions, and build complete understanding.

## Your Mindset

"What do I still not understand? What assumptions might be wrong?"

## Types of Questions

### Gap-Filling
Address information you need but wasn't provided.

- "You mentioned X but not Y. How does Y fit in?"
- "What happens when [situation] occurs?"
- "Who is responsible for [decision/maintenance]?"

### Assumption-Challenging
Question things that were stated as facts.

- "You said users will do X. How confident are we in that?"
- "Why this approach rather than [alternative]?"
- "What if that assumption turns out to be wrong?"

### Edge-Case Exploring
Find the boundaries and exceptions.

- "What happens if X fails?"
- "What about users who [unusual situation]?"
- "How do we handle [extreme case]?"

### Scope-Clarifying
Define what's in and out.

- "Is X part of this work, or a future enhancement?"
- "What's the minimum viable version?"
- "What can we cut if we need to?"

### Priority-Establishing
Understand what matters most.

- "If you had to cut something, what would it be?"
- "What's the most critical part to get right?"
- "What would make this a success vs. just acceptable?"

## Question Formulation Principles

### One Topic at a Time
Bad: "What's the scope, and also how should error handling work, and what about mobile?"

Good: "Let's nail down scope first. What's definitely in vs. definitely out?"

### Multiple Choice When Helpful
Bad: "How should authentication work?"

Good: "For authentication, should we: (A) use existing auth, (B) implement OAuth, (C) API keys, or (D) something else?"

**Pro tip:** Use lettered options (A, B, C, D) so users can respond quickly with "1A, 2C" style answers. This is especially effective for:
- Project type/feature category selection
- Technology choices
- Scope decisions
- Quality gates commands

See `example-conversation.md` for a complete example of this format in action.

### Build on Answers
Don't treat questions as independent. Follow threads.

If they say "we need mobile support" → follow up with mobile-specific questions.

### Challenge Gently
Bad: "That won't work."

Good: "I want to make sure I understand - you're assuming X because of Y. Is that accurate? Have you considered Z?"

## How Many Rounds?

| Task Complexity | Typical Rounds |
|-----------------|----------------|
| Simple bug fix | 1-2 |
| Small feature | 2-3 |
| Medium feature | 4-6 |
| Large feature | 6-10 |
| Complex system | 8+ |

These are guidelines. Stop when you have enough, not when you hit a number.

## When to Stop

**Stop when:**
- You can confidently outline the work
- Additional questions would be diminishing returns
- The user is getting fatigued
- You're asking about details you can figure out yourself

**Don't stop when:**
- Significant gaps remain
- Scope is still fuzzy
- Assumptions haven't been validated
- Critical decisions aren't made

**The test:** Could you write a detailed PRD right now that wouldn't need major revision? If yes, stop. If no, keep going.
