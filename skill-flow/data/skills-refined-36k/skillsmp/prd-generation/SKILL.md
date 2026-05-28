---
name: prd-generation
description: "Generate detailed Product Requirements Documents. Use when creating PRDs, planning features, or writing specifications."
---

# PRD Generation Skill

Expert guidance for creating clear, actionable Product Requirements Documents.

## When to Use

- User asks to create a PRD
- User wants to plan a feature
- User needs to write specifications
- User mentions "requirements document"

## PRD Quality Checklist

### User Stories Must Be:
- **Small**: Completable in one focused session
- **Independent**: No dependencies on later stories
- **Verifiable**: Clear acceptance criteria

### Acceptance Criteria Must Be:
- **Specific**: Not vague ("works correctly" is bad)
- **Testable**: Can be checked programmatically or visually
- **Complete**: Include typecheck/lint requirements

### Structure Must Include:
1. Introduction/Overview
2. Goals (measurable)
3. User Stories (with acceptance criteria)
4. Functional Requirements (numbered)
5. Non-Goals (explicit scope boundaries)
6. Technical Considerations (if relevant)
7. Success Metrics

## Story Sizing Guide

### Right Size (1 iteration):
- Add a database column
- Create a single component
- Implement one API endpoint
- Add form validation

### Too Big (split it):
- "Build the dashboard" -> schema + queries + UI + filters
- "Add authentication" -> schema + middleware + login + sessions
- "Refactor the API" -> one story per endpoint

## Question Framework

Ask 3-5 clarifying questions with options:

```
1. What problem does this solve?
   A. [Option]
   B. [Option]
   C. Other: [specify]

2. Who is the target user?
   A. [Option]
   B. [Option]
```

Allow "1A, 2B" style responses for efficiency.

## Output Location

Save to: `tasks/prd-[feature-name].md`
