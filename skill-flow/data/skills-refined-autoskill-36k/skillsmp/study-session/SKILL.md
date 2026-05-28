---
name: study-session
description: Assists with study sessions. Activates when reading PDFs or notes from ~/Documents/2026/References/, during concept Q&A about SICP, Lisp, programming theory, or other study material. Offers explanations, quizzes, flashcard extraction, and daily journal logging.
---

# Study Session Skill

Help the user study effectively by offering assistance at session start, tracking concepts discussed, extracting flashcards after Q&A, and logging to the daily journal.

## Phase 1: Session Start

When the user reads a file from `~/Documents/2026/References/`:

1. Note the filename and topic
2. Offer assistance: "I see you're studying [filename]. Want me to explain concepts, quiz you, or just answer questions as you go?"
3. If user wants a quiz, ask questions based on the material
4. If user wants explanations, provide context and break down difficult concepts

## Phase 2: During Session

As you answer questions about the material:

- Keep mental note of key concepts discussed
- Focus on understanding - explain "why" not just "what"
- When the user seems confused, offer alternative explanations
- Connect new concepts to ones already discussed

## Phase 3: After Q&A Exchange

After substantial concept discussion (roughly 3+ back-and-forth exchanges about a topic):

1. Offer flashcard extraction: "We've covered some good concepts. Want me to extract flashcards from this discussion?"
2. If user agrees, follow the [Flashcard Guide](flashcard-guide.md) to generate cards
3. Use AskUserQuestion to review cards one at a time:
   - Show the card (Q/A or C: format)
   - Options: Accept, Edit, Skip
   - If Edit: ask for corrected version, confirm, then proceed
4. Append accepted cards to the appropriate deck in `~/Documents/2026/Cards/`

## Phase 4: Journal Logging

After extracting flashcards OR when the session seems to be wrapping up:

1. Offer to log: "Should I add this study session to your daily journal?"
2. If user agrees, follow the [Journal Format](journal-format.md) to append an entry
3. Add a bullet point summarizing what was studied

## Key Paths

- **References:** `~/Documents/2026/References/`
- **Cards:** `~/Documents/2026/Cards/`
- **Daily Journal:** `~/Documents/2026/Journal/Daily/`
- **SR Best Practices:** `~/.claude/context/spaced-repetition.md`

## Important Notes

- Always read the spaced-repetition.md context before generating flashcards
- Check existing decks to avoid duplicate cards
- Match the style of existing cards in the selected deck
- Never auto-create cards without user review
- Journal entries should be brief (one bullet point)
