# Chain Examples

annotated skill chain patterns for common scenarios.

## delegation chains

### pair with external agents
```
pair
   │
   ├── context gathering (layer, outline)
   ├── prompt engineering (metaprompt-factory patterns)
   ├── delegate to codex/copilot (auto-routed)
   ├── verify output (outline --diff, verify)
   └── iterate or accept
```
**when**: user says "pair with codex", "delegate this", complex implementation
**depth**: varies (1 min - hours depending on mode)

### loop with delegation
```
issue-context → loop + pair → pr-audit
      │              │            │
      │              │            └── final review
      │              └── claude orchestrates, pair delegates heavy work
      └── enrich issue first
```
**when**: autonomous work with external agent collaboration
**depth**: very deep (hours)

---

## creation chains

### new skill from scratch
```
ask-deep → skill-create → pair quick
   │           │              │
   │           │              └── validate structure
   │           └── scaffold with archetype
   └── gather requirements via questionnaire
```
**when**: user wants new skill, requirements unclear
**depth**: moderate (30-45 min)

### new feature implementation
```
issue-context → loop → pr-audit
      │           │        │
      │           │        └── validate before merge
      │           └── autonomous implementation
      └── enrich Linear issue with codebase context
```
**when**: Linear issue exists, needs implementation
**depth**: deep (1-3 hours)

### new dashboard
```
ask-deep → dashboard → emil-kowalski
   │          │            │
   │          │            └── apply Linear-style design
   │          └── scaffold convex dashboard
   └── clarify data requirements
```
**when**: admin interface needed
**depth**: moderate-deep (40-90 min)

---

## improvement chains

### skill to 10/10
```
skill-improve → pair thorough → skill-audit
      │              │              │
      │              │              └── verify in context of all skills
      │              └── thorough validation via codex
      └── self-eval → research → rewrite
```
**when**: skill scoring below 10/10
**depth**: deep (30-60 min per skill)

### batch skill improvement
```
skill-audit → [skill-improve × N] → pair thorough
     │               │                    │
     │               │                    └── final validation
     │               └── improve each flagged skill
     └── identify skills needing work
```
**when**: multiple skills need attention
**depth**: very deep (hours)

### code refinement
```
pair quick → loop → pr-audit
      │         │        │
      │         │        └── validate changes
      │         └── implement refinements
      └── quick assessment of approach
```
**when**: existing code needs improvement
**depth**: moderate (30-60 min)

---

## research chains

### quick question
```
pair quick
     │
     └── fast answer via copilot
```
**when**: simple question, high confidence
**depth**: shallow (1-2 min)

### deep analysis
```
pair thorough
     │
     └── thorough analysis via codex
```
**when**: complex question, architectural implications
**depth**: moderate-deep (10-30 min)

### uncertain question
```
pair quick → [escalate within pair]
      │
      └── auto-escalates to thorough if confidence < 7
```
**when**: unknown complexity
**depth**: varies (2-30 min)

---

## communication chains

### notify with context
```
loop → slack
  │      │
  │      └── send completion notification
  └── autonomous work
```
**when**: long-running task, user wants updates
**depth**: n/a (notification is instant)

### structured update
```
pair thorough → slack
      │          │
      │          └── format and send findings
      └── thorough analysis
```
**when**: analysis results need sharing
**depth**: moderate (10-30 min + notification)

---

## validation chains

### pre-merge validation
```
pr-audit
    │
    └── security, perf, test coverage review
```
**when**: PR ready for review
**depth**: moderate (5-15 min)

### progress validation
```
pair quick → [continue | adjust | escalate]
      │
      └── quick check on trajectory
```
**when**: mid-task, need sanity check
**depth**: shallow (1-2 min)

### architectural validation
```
pair thorough → [proceed | redesign | escalate to HIL]
      │
      └── thorough review of approach
```
**when**: significant architectural decision
**depth**: deep (15-30 min)

---

## meta chains

### which skills to use (plan mode)
```
skill-compose (plan mode) → [proceed | clarify | pair quick]
      │
      ├── high confidence (≥7): proceed with chain
      ├── medium confidence (5-6): ask 1 clarifying question
      └── low confidence (<5): invoke pair quick
```
**when**: unclear optimal approach
**depth**: shallow (instant)

### skill composition
```
skill-compose (execute mode) → [parallel | sequential | conditional]
      │
      └── orchestrate multi-skill workflow
```
**when**: complex task requiring multiple skills
**depth**: varies by composition

---

## anti-pattern chains

### don't do these

```
❌ pair thorough → pair quick
   (never downgrade validation tier)

❌ skill-improve → skill-create
   (create first, improve later)

❌ loop → loop
   (don't nest autonomous loops)

❌ ask-deep → ask-deep
   (don't chain question flows)
```

---

## chain selection heuristics

| context signal | chain pattern |
|----------------|---------------|
| Linear issue mentioned | issue-context → loop |
| "improve" + skill name | skill-improve → pair thorough |
| new feature request | ask-deep → [appropriate skill] |
| PR URL mentioned | pr-audit |
| "quick" or "fast" | pair quick |
| "thorough" or "deep" | pair thorough |
| notification needed | [work] → slack/imessage |
| unclear requirements | ask-deep → [TBD] |
| "pair with codex" | pair (implement mode) |
| "delegate this" | pair (implement mode) |
| "get second opinion" | pair (consult mode) |
| "review this" | pair (review mode) |
