---
name: article-verification
description: Use this skill when you need to systematically deconstruct written content into verifiable claims and validate each one to ensure high-integrity content.
---

# Article Verification Workflow

## Purpose

Help writers produce high-integrity content by identifying and validating every factual claim, opinion, and assertion in an article. This skill systematically deconstructs content into verifiable components, validates each claim, and facilitates informed discourse through structured interviewing.

## When to Use

- **Pre-publication review**: Verify content before publishing.
- **Editor fact-checking**: Flag concerns before content goes public.
- **AI output verification**: Validate LLM-generated text before use.
- **Content audit**: Retrospective verification of published content.
- **Quality assurance**: Automated claim extraction and selective human verification.

## Input

- Raw article text (provided directly), or
- File path to markdown/text file to analyze.

## Output

- Verification report saved to `.agent/docs/verification-report-{timestamp}.md`.
- Summary in `.agent/focus.md`.

---

## Phase 1: Claim Extraction & Atomization

### Purpose

Break content into granular, verifiable units for systematic analysis.

### Process

1. **Read the entire text** for full context.
2. **Extract claims** using the Claimify framework:
   - **Selection**: Filter out unverifiable content (pure opinion, conjecture, aesthetic judgments).
   - **Disambiguation**: Clarify ambiguous statements using context.
   - **Decomposition**: Break complex statements into atomic claims.

### Claim Categories

| Category      | Description                                           | Example                                      |
|---------------|-------------------------------------------------------|----------------------------------------------|
| `FACTUAL`     | Verifiable against objective evidence                 | "Python was released in 1991."              |
| `EMPIRICAL`   | Claims about measurable phenomena, scientific findings| "Studies show X increases Y by 30%."        |
| `OPINION`     | Author's interpretation or stance                     | "React is the best framework."               |
| `EXPERT_CLAIM`| Requires domain expertise to verify                   | "This architecture prevents race conditions."|
| `LOGICAL`     | Causal claims, conditional statements                 | "If X then Y because Z."                     |

### Extraction Output Format

For each claim, record:

```markdown
### Claim #{N}

**Original text:** "[exact quote from article]"
**Section:** [paragraph/header reference]
```