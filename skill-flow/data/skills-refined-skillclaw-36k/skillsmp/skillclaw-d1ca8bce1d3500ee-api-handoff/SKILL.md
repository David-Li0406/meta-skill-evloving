---
name: api-handoff
description: Use this skill when backend work is complete and needs to be documented for frontend integration, or when the user requests 'create handoff', 'document API', 'frontend handoff', or 'API documentation'.
---

# API Handoff Mode

> **No Chat Output**: Produce the handoff document only. No discussion, no explanation—just the markdown block saved to the handoff file.

You are a backend developer completing API work. Your task is to produce a structured handoff document that gives frontend developers (or their AI) full business and technical context to build integration/UI without needing to ask backend questions.

> **When to use**: After completing backend API work—endpoints, DTOs, validation, business logic—run this mode to generate handoff documentation.

> **Simple API shortcut**: If the API is straightforward (CRUD, no complex business logic, obvious validation), skip the full template—just provide the endpoint, method, and example request/response JSON. Frontend can infer the rest.

## Goal
Produce a copy-paste-ready handoff document with all context a frontend AI needs to build UI/integration correctly and confidently.

## Inputs
- Completed API code (endpoints, controllers, services, DTOs, validation).
- Related business context from the task/user story.
- Any constraints, edge cases, or gotchas discovered during implementation.

## Workflow

1. **Collect context** — confirm feature name, relevant endpoints, DTOs, auth rules, and edge cases.
2. **Create/update handoff file** — write the document to `docs/ai/<feature-name>/api-handoff.md`. Increment the iteration suffix (`-v2`, `-v3`, …) if rerunning after feedback.
3. **Paste template** — fill every section below with concrete data. Omit subsections only when truly not applicable (note why).
4. **Double-check** — ensure payloads match actual API behavior, auth scopes are accurate, and enums/validation reflect backend logic.

## Output Format

Produce a single markdown block structured as follows. Keep it dense—no fluff, no repetition.

---

```markdown
# API Handoff: [Feature Name]

## Business Context
[2-4 sentences: What problem does this solve? Who uses it? Why does it matter? Include any domain terms the frontend needs to understand.]

## Endpoints

### [METHOD] /path/to/endpoint
- **Purpose**: [1 line: what it does]
- **Auth**: [required role/permission, or "public"]
- **Request**:
  ```json
  {
    "field": "type — description, constraints, etc."
  }
  ```
- **Response**:
  ```json
  {
    "field": "type — description, etc."
  }
  ```
```