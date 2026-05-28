---
name: generating-multiple-choice-questions
description: Apply this skill generate multiple choice questions
---

Produce multiple choice questions with four possible answers and two alternate distractors. The first answer should aways be the correct option. A variety of questions should be provided focusing different levels of Bloom's revised taxonomy (remember, understand, apply, analyze, evaluate, create).

## Format

Output format should look like this for each question:

```markdown
## What is a function in Python?

---

- A named sequence of statements performing a computation
- A value returned from a computation
- A file containing Python definitions
- A variable used to store data

### Alternate Distractors

- A template for objects
- A mechanism used to view backtraces
```

Questions should be no more than 30 words. Answers should be no more than 8 words.
