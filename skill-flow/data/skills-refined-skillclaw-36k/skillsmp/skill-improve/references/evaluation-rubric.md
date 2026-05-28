# evaluation rubric

detailed scoring criteria for skill self-evaluation.

## scoring dimensions

### decision trees (weight: high)

| score | criteria |
|-------|----------|
| 9-10 | covers 90%+ scenarios, nested logic, edge cases handled |
| 7-8 | covers common scenarios, clear if/then structure |
| 5-6 | basic decision tree present but incomplete |
| 3-4 | vague guidance, no clear branching logic |
| 1-2 | pure philosophy, no actionable decisions |

**example of 9-10:**
```
Should I animate this?
├── Is it purely decorative? → No animation
├── Does it aid comprehension?
│   ├── State change? → 200ms ease-out
│   └── Content reveal? → 150ms fade
├── Is it user-initiated?
│   ├── Button press? → Immediate (50ms)
│   └── Navigation? → 300ms slide
└── Default → Consider if animation adds value
```

**example of 3-4:**
```
Use animation thoughtfully. Consider whether it adds value.
```

### concrete values (weight: high)

| score | criteria |
|-------|----------|
| 9-10 | values from source code with file/line references |
| 7-8 | values from official docs with URLs |
| 5-6 | values present but source unclear |
| 3-4 | ranges given without specifics (e.g., "200-300ms") |
| 1-2 | no specific values, all qualitative |

**example of 9-10:**
```
| constant | value | source |
|----------|-------|--------|
| TOAST_DURATION | 4000ms | sonner/src/index.tsx:42 |
| SWIPE_THRESHOLD | 45px | sonner/src/index.tsx:18 |
| VELOCITY_DISMISS | 0.11px/ms | sonner/src/index.tsx:23 |
```

**example of 3-4:**
```
Toast duration should be 3-5 seconds.
Swipe threshold varies by implementation.
```

### primary sources (weight: high)

| score | criteria |
|-------|----------|
| 9-10 | read source code, extracted constants, understood internals |
| 7-8 | read official documentation thoroughly |
| 5-6 | read tutorials and guides |
| 3-4 | read blog posts and summaries |
| 1-2 | general knowledge, no specific research |

**evidence of primary source research:**
- file paths to source code
- specific function/constant names
- internal implementation details
- version-specific information

### tool integration (weight: medium)

| score | criteria |
|-------|----------|
| 9-10 | integrates with user's specific tools, references their codebase |
| 7-8 | mentions how to use with common tools in user's stack |
| 5-6 | generic tool suggestions |
| 3-4 | mentions tools exist but no integration guidance |
| 1-2 | no tool context |

**example of 9-10:**
```
## integration with ~/Developer/components

this skill works with your existing component library:

| component | location | how to apply |
|-----------|----------|--------------|
| menu | ~/Developer/components/menu | use 150ms for item hover |
| tabs | ~/Developer/components/tabs | use spring for indicator |

consult-light validation:
copilot -p --model gemini-3-pro "validate emil-kowalski principles in $FILE"
```

### anti-patterns (weight: medium)

| score | criteria |
|-------|----------|
| 9-10 | specific patterns with root cause and concrete fix |
| 7-8 | patterns listed with fixes |
| 5-6 | patterns listed without clear fixes |
| 3-4 | vague "don't do this" warnings |
| 1-2 | no anti-patterns section |

**example of 9-10:**
```
| pattern | problem | fix |
|---------|---------|-----|
| ease-in for entrance | feels sluggish, unnatural | use ease-out (fast start, slow end) |
| >400ms duration | breaks perceived performance | cap at 300ms for UI, 400ms for page |
| transform: scale(0) | jarring pop-in effect | start at scale(0.95) minimum |
```

### references depth (weight: medium)

| score | criteria |
|-------|----------|
| 9-10 | each reference >100 lines, substantive content |
| 7-8 | references 50-100 lines, useful detail |
| 5-6 | references 20-50 lines, basic content |
| 3-4 | references exist but are stubs (<20 lines) |
| 1-2 | no references or empty files |

## composite scoring

```
weighted_score = (
  decision_trees * 0.25 +
  concrete_values * 0.25 +
  primary_sources * 0.20 +
  tool_integration * 0.15 +
  anti_patterns * 0.10 +
  references_depth * 0.05
)
```

**interpretation:**
- 8.0+: mature skill, periodic review only
- 6.0-7.9: functional but needs improvement
- 4.0-5.9: requires significant work
- <4.0: needs complete rewrite

## how to score

1. read the skill top-to-bottom once
2. score each dimension based on evidence, not intent
3. compute weighted score
4. assign priority and action
5. document gaps with evidence

**quick score (5-10 min):**
- skim decision trees and values tables
- check references depth
- confirm tool integration exists
- score based on visible evidence

**deep score (15-30 min):**
- cross-check sources and constants
- verify decision trees match common scenarios
- check that anti-pattern fixes are concrete

## evidence checklist

| dimension | evidence signals |
|-----------|------------------|
| decision trees | 1+ multi-branch tree, concrete actions, default path |
| concrete values | table with constants + sources |
| primary sources | source code URLs or file paths with lines |
| tool integration | commands or file paths in user's stack |
| anti-patterns | table with fixes that can be applied |
| references depth | 50+ lines in each reference |

## common scoring errors

- scoring intent instead of evidence
- counting a paragraph as a decision tree
- accepting ranges without sources as concrete values
- ignoring missing tool integration
- skipping references depth entirely

## example evaluations

**example: shallow skill (score ~4.6)**
```
Decision trees: 3/10
Concrete values: 2/10
Primary sources: 3/10
Tool integration: 4/10
Anti-patterns: 2/10
References depth: 3/10
Weighted: 4.6 -> full rewrite
```

**example: mid skill (score ~6.8)**
```
Decision trees: 7/10
Concrete values: 6/10
Primary sources: 6/10
Tool integration: 7/10
Anti-patterns: 6/10
References depth: 6/10
Weighted: 6.8 -> improve
```

**example: mature skill (score ~8.6)**
```
Decision trees: 9/10
Concrete values: 8/10
Primary sources: 9/10
Tool integration: 8/10
Anti-patterns: 8/10
References depth: 8/10
Weighted: 8.6 -> periodic review
```

## quick evaluation template

```
Skill: [name]
Date: [YYYY-MM-DD]

| dimension | score | notes |
|-----------|-------|-------|
| decision trees | /10 | |
| concrete values | /10 | |
| primary sources | /10 | |
| tool integration | /10 | |
| anti-patterns | /10 | |
| references depth | /10 | |

Weighted: /10
Priority: [high/medium/low]
Next action: [specific improvement]
```

## delta tracking

track before/after to prove improvement:

```
Before weighted: 6.2
After weighted: 8.4
Delta: +2.2
Evidence: added decision tree, sourced constants, artifact
```
