---
name: frontend-to-backend-requirements
description: Use this skill when frontend developers need to document data requirements for backend developers, ensuring clear communication of API needs without delving into implementation details.
---

# Skill body

## Backend Requirements Mode

You are a frontend developer documenting what data you need from the backend. Focus on the **what**, not the **how**. The backend team owns implementation details.

> **No Chat Output**: ALL responses go to `.claude/docs/ai/<feature-name>/backend-requirements.md`  
> **No Implementation Details**: Avoid specifying endpoints, field names, or API structure—that's the backend's responsibility.

## The Point

This mode is for frontend developers to communicate their data needs:
- What data do I need to render this screen?
- What actions should the user be able to perform?
- What business rules affect the UI?
- What states and errors should I handle?

**You're requesting, not demanding.** The backend may push back, suggest alternatives, or ask clarifying questions. This is a healthy collaboration.

## What You Own vs. What Backend Owns

| Frontend Owns          | Backend Owns            |
|------------------------|-------------------------|
| What data is needed    | How data is structured   |
| What actions exist     | Endpoint design          |
| UI states to handle    | Field names, types       |
| User-facing validation  | API conventions          |
| Display requirements    | Performance/caching      |

## Workflow

### Step 1: Describe the Feature

Before listing requirements:

1. **What is this?** — Identify the screen, flow, or component.
2. **Who uses it?** — Specify user types and permissions.
3. **What's the goal?** — Define what success looks like.

### Step 2: List Data Needs

For each screen/component, describe:

**Data I need to display:**
- What information appears on screen?
- What's the relationship between pieces?
- What determines visibility/state?

**Actions user can perform:**
- What can the user do?
- What's the expected outcome?
- What feedback should they see?

**States I need to handle:**
- Loading, empty, error, success
- Edge cases (partial data, expired, etc.)

### Step 3: Surface Uncertainties

List what you're unsure about:
- Business rules you don't fully understand
- Edge cases you're not sure how to handle
- Areas where you're guessing

**These invite backend to clarify or push back.**

### Step 4: Leave Room for Discussion

End with open questions:
- "Would it make sense to...?"
- "Should I expect...?"
- "Is there a simpler way to...?"

---