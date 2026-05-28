# Flashcard Generation Guide

## Before Generating Cards

1. **Read the SR context:** Always read `~/.claude/context/spaced-repetition.md` first
2. **Load existing decks:** List `.md` files in `~/Documents/2026/Cards/` and read contents
3. **Identify the deck:** Ask user which deck to add to, or infer from topic

## Card Principles

### Atomic Cards

Each card tests ONE piece of knowledge. Break complex topics into multiple cards.

**Bad:** "Explain the substitution model of evaluation"
**Good:**

- "What is the substitution model?"
- "What are the steps of the substitution model?"
- "When does the substitution model break down?"

### Two-Way Questions

For term/definition pairs, create both directions:

- Term → Definition: "What is a closure?"
- Definition → Term: "What do you call a procedure bundled with its environment?"

### Brief Answers

If you can't answer in a few seconds, the card is too complex.

## Card Formats

### Question-Answer (Q/A)

```
Q: What is referential transparency?
A: An expression is referentially transparent if it can be replaced with its value without changing program behavior.
```

Use for: explanations, comparisons, "why" questions, complex answers

### Cloze Deletion (C:)

```
C: In Lisp, [car] returns the first element and [cdr] returns the rest of a list.
```

Multiple deletions create sibling cards (one per gap).

Use for: fill-in-the-blank, key terms, definitions, syntax patterns

## What to Extract

From the conversation, identify:

- New definitions and terminology
- Distinctions between similar concepts
- Core ideas and mental models
- How things work at a conceptual level

Do NOT create cards for:

- Specific commands typed (unless conceptually important)
- Debugging steps or errors encountered
- Implementation details that aren't conceptual

## Deduplication

Before adding cards:

1. Read the selected deck's contents
2. Check if concepts are already covered
3. Skip cards that duplicate existing knowledge
4. Match the style/depth of existing cards

## Interactive Review

Present each card using AskUserQuestion:

```
Card X of N:

Q: [question]
A: [answer]
```

Options:

- **Accept** - Add to deck as-is
- **Edit** - User provides corrected version
- **Skip** - Don't add this card

## Writing to Deck

Append accepted cards to `~/Documents/2026/Cards/<deck-name>.md`:

- Add a blank line between cards
- If file doesn't exist, create it
- Report count and file path when done
