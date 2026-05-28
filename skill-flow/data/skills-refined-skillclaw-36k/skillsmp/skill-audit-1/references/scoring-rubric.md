# Scoring Rubric

detailed scoring criteria with examples for skill depth assessment.

## criteria breakdown

### decision trees (weight: ×2)

| score | criteria | example |
|-------|----------|---------|
| 0 | no decision trees | procedural "do this, then that" |
| 1 | 1 simple tree | single branch "if X → do Y" |
| 2 | 2+ trees with branches | full routing with ├── notation, multiple conditions |

**what makes a good decision tree:**
- uses `├──` and `└──` notation
- has 3+ branches
- each branch leads to specific action
- covers common scenarios

**example of 2-point tree:**
```
Should I use this tool?
├── Simple task?
│   ├── Single file change → direct edit
│   └── Multiple files → plan first
├── Complex task?
│   ├── Architectural → consult-deep
│   └── Implementation → loop
└── Unclear scope?
    └── deep-ask first
```

### concrete values (weight: ×2)

| score | criteria | example |
|-------|----------|---------|
| 0 | no numbers or thresholds | "use appropriate timing" |
| 1 | some values, no sources | "200-300ms duration" |
| 2 | values with sources | "200ms (from sonner/src/index.tsx:47)" |

**what counts as concrete:**
- timing values (ms, seconds)
- thresholds (score >= 8)
- counts (3-5 examples)
- percentages (>50% overlap)
- configuration values

**example of 2-point values:**
```markdown
| constant | value | source |
|----------|-------|--------|
| toast duration | 4000ms | sonner/src/index.tsx:23 |
| spring tension | 300 | vaul/src/index.tsx:89 |
| max retries | 3 | internal convention |
```

### anti-patterns (weight: ×1)

| score | criteria | example |
|-------|----------|---------|
| 0 | no anti-patterns section | absent |
| 1 | listed but no fixes | "don't do X, don't do Y" |
| 2 | listed with specific fixes | "pattern \| problem \| fix" table |

**what makes good anti-patterns:**
- specific pattern name
- why it's a problem
- actionable fix

**example of 2-point anti-patterns:**
```markdown
| pattern | problem | fix |
|---------|---------|-----|
| fire-and-forget | task may fail silently | add verification step |
| vague prompt | poor AI output | use XML structure |
```

### references (weight: ×1)

| score | criteria | example |
|-------|----------|---------|
| 0 | none or broken links | references to non-existent files |
| 1 | exist but thin | <50 lines, mostly stubs |
| 2 | substantive | >50 lines each, real content |

**what counts as substantive:**
- >50 lines of actual content
- code examples
- detailed explanations
- not just headers

### tool integration (weight: ×1)

| score | criteria | example |
|-------|----------|---------|
| 0 | no tool examples | "use appropriate tools" |
| 1 | tools mentioned | "use copilot for..." |
| 2 | working code examples | actual command with heredoc |

**example of 2-point integration:**
```bash
cat <<'EOF' | copilot -p --model gemini-3-pro
Your prompt here with actual content.
Output JSON: {field: type}
EOF
```

### when to use (weight: ×1)

| score | criteria | example |
|-------|----------|---------|
| 0 | no guidance | absent |
| 1 | listed but not structured | bullet points |
| 2 | table with use/skip columns | clear decision support |

**example of 2-point when to use:**
```markdown
| use | skip |
|-----|------|
| complex multi-file task | single line fix |
| unclear requirements | obvious implementation |
```

## scoring calculation

1. Rate each criterion 0-2
2. Apply weights:
   - decision trees × 2
   - concrete values × 2
   - anti-patterns × 1
   - references × 1
   - tool integration × 1
   - when to use × 1
3. Sum for raw score (max 16)
4. Convert: `depth = raw / 16 × 10`

## examples

### healthy skill (14/16 = 9/10)

```
decision trees: 2 × 2 = 4
concrete values: 2 × 2 = 4
anti-patterns: 2 × 1 = 2
references: 2 × 1 = 2
tool integration: 1 × 1 = 1
when to use: 1 × 1 = 1
---
raw = 14, depth = 9/10
```

### shallow skill (8/16 = 5/10)

```
decision trees: 0 × 2 = 0
concrete values: 1 × 2 = 2
anti-patterns: 1 × 1 = 1
references: 1 × 1 = 1
tool integration: 2 × 1 = 2
when to use: 2 × 1 = 2
---
raw = 8, depth = 5/10
```

## quick heuristics

for rapid assessment without full calculation:

| signal | likely depth |
|--------|--------------|
| multiple `├──` trees visible | 7+ |
| numbers with file:line citations | 8+ |
| anti-patterns table with fixes | 7+ |
| references/ dir with 2+ files | 7+ |
| no trees, no tables | <5 |
| >200 lines with structure | 7+ |
| <100 lines | likely <6 |
