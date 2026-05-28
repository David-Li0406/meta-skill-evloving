---
name: prd-generator
description: Use this skill when you need to create a Product Requirements Document (PRD) for a new feature, ensuring clarity and actionable details for implementation.
---

# PRD Generator

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation.

## The Job

1. Receive a feature description from the user.
2. Ask 3-5 essential clarifying questions (with lettered options).
3. Generate a structured PRD based on answers.
4. Save to `tasks/prd-[feature-name].md`.

**Important:** Do NOT start implementing. Just create the PRD.

## Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?

### Format Questions Like This:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the scope?
   A. Minimal viable version
   B. Full-featured implementation
   C. Just the backend/API
   D. Just the UI
```

This lets users respond with "1A, 2C, 3B" for quick iteration.

## Step 2: PRD Structure

Generate the PRD with these sections:

### 1. Introduction/Overview
Brief description of the feature and the problem it solves.

### 2. Goals
Specific, measurable objectives (bullet list).

### 3. User Stories
Each story needs:
- **Title:** Short descriptive name.
- **Description:** "As a [user], I want [feature] so that [benefit]."
- **Acceptance Criteria:** Verifiable checklist of what "done" means.

Each story should be small enough to implement in one focused session.

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck/lint passes
- [ ] **[UI stories only]** Verify in browser using dev-browser skill
```

**Important:** 
- Acceptance criteria must be verifiable, not vague. "Works correctly" is bad. "Button shows confirmation dialog before deleting" is good.
- Each story should be completable in one focused session (typically 10-20 minutes of work).