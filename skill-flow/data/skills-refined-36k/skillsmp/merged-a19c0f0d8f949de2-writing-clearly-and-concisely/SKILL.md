---
name: writing-clearly-and-concisely
description: Use this skill when writing prose for humans—documentation, commit messages, error messages, explanations, reports, or UI text. Apply Strunk's timeless rules for clearer, stronger, and more professional writing.
---

# Writing Clearly and Concisely

## Overview

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write clearly and cut ruthlessly. This skill covers what to do (Strunk) and what not to do (AI patterns).

## When to Use This Skill

Use this skill whenever you write prose for humans:

- Documentation, README files, technical explanations
- Commit messages, pull request descriptions
- Error messages, UI copy, help text, comments
- Reports, summaries, or any explanation
- Editing to improve clarity

**If you're writing sentences for a human to read, use this skill.**

## Limited Context Strategy

When context is tight:

1. Write your draft using judgment.
2. Dispatch a subagent with your draft and the relevant section file.
3. Have the subagent copyedit and return the revision.

Loading a single section (~1,000-4,500 tokens) instead of everything saves significant context.

## Structure Principles

### BLUF (Bottom Line Up Front)

Put your conclusion first, then explain. Your first sentence should answer what you need and by when, allowing the reader to act without reading further.

**Test:** Can someone act on your message after reading only the first sentence?

### Explain Concepts Before Using Them

Information must be disclosed in the correct order. Never reference a term, concept, or acronym before you've defined it.

## Elements of Style

### Rules

**Elementary Rules of Usage (Grammar/Punctuation)**:

1. Form possessive singular by adding 's.
2. Use a comma after each term in a series except the last.
3. Enclose parenthetic expressions between commas.
4. Comma before conjunction introducing a co-ordinate clause.
5. Don't join independent clauses by a comma.
6. Don't break sentences in two.
7. Participial phrase at the beginning refers to the grammatical subject.

**Elementary Principles of Composition**:

8. One paragraph per topic.
9. Begin paragraph with a topic sentence.
10. **Use active voice.**
11. **Put statements in positive form.**
12. **Use definite, specific, concrete language.**
13. **Omit needless words.**
14. Avoid succession of loose sentences.
15. Express co-ordinate ideas in similar form.
16. **Keep related words together.**
17. Keep to one tense in summaries.
18. **Place emphatic words at the end of the sentence.**

## AI Writing Patterns to Avoid

Avoid generic, puffy prose produced by LLMs:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy.
- **Empty "-ing" phrases:** ensuring reliability, showcasing features, highlighting capabilities.
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge.
- **Overused AI vocabulary:** delve, leverage, multifaceted, foster, realm, tapestry.
- **Formatting overuse:** excessive bullets, emoji decorations, bold on every other word.

Be specific, not grandiose. Say what it actually does.

## Bottom Line

Writing for humans? Apply the rules from *The Elements of Style*. For most tasks, focus on the principles of composition to enhance clarity and effectiveness.