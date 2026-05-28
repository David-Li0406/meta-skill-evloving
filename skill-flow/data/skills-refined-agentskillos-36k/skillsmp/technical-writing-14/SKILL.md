---
name: technical-writing
description: Use when writing for technical audiences — Jira issues, code documentation, design docs, implementation plans, READMEs, CLAUDE files. Ensures clarity, consistency, and global accessibility.
---

# Technical Writing

## Overview

Technical writing succeeds when readers extract information without friction. This skill applies Red Hat's documentation standards: target an 8th-grade reading level (Flesch-Kincaid 60-70), favor clarity over cleverness, and write for global audiences including non-native English speakers and translation systems.

## When to Use

- Writing or editing Jira issues, tickets, or bug reports
- Drafting design documents or implementation plans
- Writing code documentation, READMEs, or inline comments
- Creating user-facing technical content
- Reviewing technical prose for clarity

## Core Pattern

### Clarity First

1. **Keep sentences under 40 words.** If a sentence exceeds this, split it or restructure.
2. **Include "that" in clauses.** "Verify that the service is running" aids translation; "Verify the service is running" creates ambiguity.
3. **Pair demonstratives with nouns.** Write "this configuration" not "this" alone — global readers need explicit antecedents.
4. **Eliminate verbosity.** Cut "in order to" → "to", "due to the fact that" → "because", "at this point in time" → "now".
5. **Use if-then structure.** Follow conditional statements with explicit "then" markers for clarity.

### Language Choices

1. **Active voice, present tense.** "The function returns a string" not "A string will be returned by the function."
2. **User agency over anthropomorphism.** Write "users can configure" not "the system allows users to configure."
3. **No contractions.** Write "do not" not "don't" — contractions complicate translation.
4. **No slang, idioms, or jargon.** Replace "out of the box" with "by default"; replace "gotcha" with "common mistake."
5. **Fewer/less correctly.** Use "fewer" for countable items, "less" for quantities.

### Structure

1. **Introduce lists with complete sentences.** The lead-in establishes context.
2. **Parallel construction in lists.** All items should match grammatically.
3. **Avoid noun stacking.** "System configuration file" → "configuration file for the system."

## Quick Reference

| Instead of | Write |
|------------|-------|
| This allows users to... | Users can... |
| In order to | To |
| Will be created | Is created |
| The system knows... | The system tracks... |
| Make sure | Verify / Ensure |
| This is used for... | This [noun] does... |
| e.g. / i.e. | for example / that is |

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| "This will fail" (no noun) | Ambiguous for translators | "This operation will fail" |
| Future tense throughout | Translates poorly, reads passively | Present tense: "creates" not "will create" |
| "The system allows" | Anthropomorphism obscures user agency | "Users can" or imperative mood |
| Sentences over 40 words | Reduces comprehension, fails readability metrics | Split into multiple sentences |
| Omitting "that" | Creates parsing ambiguity | Include "that" in subordinate clauses |

## Anti-Rationalizations

- "Technical readers can handle complexity" — Complexity costs cognitive load. Clarity respects the reader's time.
- "Adding 'that' sounds stilted" — It aids 40% of readers (non-native speakers) and all translation systems.
- "Active voice sounds repetitive" — Passive voice obscures responsibility and adds words. Active is shorter.
- "This context is obvious" — Not to someone reading at 2am during an incident, or six months from now.

## Summary

When writing technical content, always follow these rules:

1. **Sentences under 40 words.** Split or restructure anything longer.
2. **Active voice, present tense.** "The function returns" not "will be returned."
3. **User agency, not anthropomorphism.** "Users can" not "the system allows."
4. **Demonstratives need nouns.** "This configuration" not "this."
