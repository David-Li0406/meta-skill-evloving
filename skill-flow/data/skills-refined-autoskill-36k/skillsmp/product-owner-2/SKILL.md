---
name: product-owner
description: Product Owner assistant for Bakery Hub. Analyzes gaps between docs and implementation, looks up requirements, and learns from user feedback. Triggers on /po-gaps, /po-requirements [feature], /po-learn [feedback].
allowed-tools: Read, Glob, Grep, Write, Task
---

# Product Owner Skill

## Overview

This skill helps maintain alignment between product documentation and implementation. It provides three main capabilities:

1. **Gap Analysis** (`/po-gaps`) - Compare implementation vs product docs
2. **Requirements Lookup** (`/po-requirements [feature]`) - Find requirements for a feature
3. **Learning** (`/po-learn [feedback]`) - Store user preferences and feedback

## Key Documentation Files

When analyzing requirements or gaps, always search these files:

- **Product Vision**: `docs/product/PRODUCT-VISION.md`
  - User personas (lines ~50-150)
  - MVP features and priorities (lines ~200-400)
  - Activity definitions (lines ~300-500)

- **Technical Spec**: `docs/product/TECHNICAL-SPEC.md`
  - API endpoints (lines ~500-700)
  - Database models (lines ~200-500)
  - Implementation patterns (lines ~600-800)

- **Reference Design**: `docs/bakery-app-reference/`
  - UI patterns and design system
  - Component examples

## Commands

### /po-gaps - Gap Analysis

Analyzes the gap between documented requirements and actual implementation.

**Process:**
1. Read product documentation files (PRODUCT-VISION.md, TECHNICAL-SPEC.md)
2. Use Glob to scan implementation directories (app/, components/, api/)
3. Compare documented features vs implemented features
4. Generate a structured report

**Output Format:**
```markdown
## Gap Analysis Report

### Implemented Features
- [x] Feature A - `path/to/implementation`
- [x] Feature B - `path/to/implementation`

### Missing Features (Not Yet Implemented)
- [ ] Feature C - Priority: P1, Requirement: [from docs]
- [ ] Feature D - Priority: P2, Requirement: [from docs]

### Partially Implemented
- [~] Feature E - Missing: [specific aspect]

### Recommendations
1. [Next steps based on priorities]
```

### /po-requirements [feature] - Requirements Lookup

Search documentation for requirements related to a specific feature.

**Usage:**
- `/po-requirements inventory` - Find inventory-related requirements
- `/po-requirements sales` - Find sales tracking requirements
- `/po-requirements alerts` - Find notification/alert requirements
- `/po-requirements expenses` - Find expense management requirements

**Process:**
1. Use Grep to search product docs for feature keyword
2. Extract user stories, acceptance criteria, technical requirements
3. Cross-reference with TECHNICAL-SPEC.md for implementation details
4. Return structured requirements

**Output Format:**
```markdown
## Requirements: [Feature Name]

### User Stories
From PRODUCT-VISION.md:
- As a [user], I want to [action] so that [benefit]

### MVP Scope
- Priority: P1/P2/P3
- [x] In MVP: [feature aspect]
- [ ] Phase 2: [deferred feature]

### Technical Requirements
From TECHNICAL-SPEC.md:
- API Endpoints: [list]
- Database Models: [list]
- Components: [list]

### Related Features
- [Related feature 1]
- [Related feature 2]
```

### /po-learn [feedback] - Store Learning

Store user preferences, decisions, and feedback for future reference.

**Usage:**
- `/po-learn "User prefers immediate stock deduction over deferred"`
- `/po-learn "Dashboard should show profit margin prominently"`
- `/po-learn "French is the primary language for staff"`
- `/po-learn "Priority: Expense charts before inventory alerts"`

**Process:**
1. Parse the feedback to identify category (UX, business rule, technical, priority)
2. Read existing preferences.json
3. Append new learning with timestamp and context
4. Write updated preferences.json
5. Confirm storage

**Categories:**
- `ux` - User experience preferences
- `business` - Business rules and logic
- `technical` - Technical decisions and patterns
- `priority` - Feature priorities and roadmap decisions

## Preferences Storage

Learnings are stored in `.claude/skills/product-owner/preferences.json`:

```json
{
  "version": "1.0.0",
  "lastUpdated": "2026-01-09T12:00:00Z",
  "preferences": [
    {
      "id": "uuid-here",
      "date": "2026-01-09",
      "category": "ux",
      "feedback": "User prefers immediate stock deduction",
      "context": "Settings page discussion"
    }
  ]
}
```

## MVP Feature Checklist

Based on PRODUCT-VISION.md Section 9, here's the MVP checklist to compare against:

### P0 - Critical (Must Have)
- [ ] Google OAuth authentication
- [ ] Email whitelist for access control
- [ ] Manager/Editor roles
- [ ] Basic inventory CRUD
- [ ] Stock level tracking

### P1 - High Priority
- [ ] Low stock alerts (in-app)
- [ ] Daily production logging
- [ ] Ingredient usage tracking
- [ ] Auto-deduct stock on production
- [ ] Daily sales entry
- [ ] Payment method breakdown (Cash/Orange Money/Card)
- [ ] Approval workflow for sales
- [ ] Expense submission and approval
- [ ] Expense categories
- [ ] Dashboard with KPIs
- [ ] French/English i18n
- [ ] PWA support

### P2 - Medium Priority
- [ ] Sales trend charts
- [ ] Expense breakdown charts
- [ ] Receipt upload for expenses
- [ ] Link expenses to inventory purchases
- [ ] Stock movement history
- [ ] Reorder point alerts

### P3 - Nice to Have
- [ ] SMS notifications
- [ ] Production planning
- [ ] Supplier management
- [ ] Multi-restaurant support

## Tips for Effective Use

1. **Gap Analysis**: Run `/po-gaps` at the start of a session to see what's missing
2. **Requirements First**: Before implementing a feature, use `/po-requirements [feature]` to understand the full scope
3. **Document Decisions**: Use `/po-learn` to capture important decisions for future sessions
4. **Check Priorities**: Focus on P0/P1 items before P2/P3

## Integration with Other Skills

This skill works well with:
- **summary-generator**: Include gap analysis in session summaries
- **frontend-design**: Reference requirements when designing new pages
