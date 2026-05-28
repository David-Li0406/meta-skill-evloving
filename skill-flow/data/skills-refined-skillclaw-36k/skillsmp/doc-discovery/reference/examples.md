# Doc Discovery Examples

## Example 1: Bug in course progress

```
User: "Course progress isn't saving correctly"

Discovery:
- Primary: course-player-and-progress (High risk)
- Coupled: collections-and-context, dashboard
- Invariants:
  - Progress must persist across sessions
  - Watch time triggers credit accrual
  - Progress is scoped to user + course
- High-risk: Yes (data integrity)
- Workflows: employee-workflows.md (Learning Journey)

Ready: Yes
```

## Example 2: Add filter to dashboard

```
User: "Add a date filter to the learning dashboard"

Discovery:
- Primary: dashboard (Medium risk)
- Coupled: course-player-and-progress (read-only)
- Invariants:
  - Dashboard must load < 2s
  - Filters persist in URL params
- High-risk: No
- Workflows: employee-workflows.md (Dashboard Overview)

Ready: Yes
```

## Example 3: New AI tutor feature

```
User: "Add a quiz generation feature to the AI tutor"

Discovery:
- Primary: course-ai (High risk)
- Coupled: ai-context-engine, prometheus-chat, tools
- Invariants:
  - AI responses must cite course content
  - Context window must not exceed limits
  - User permissions gate AI access
- High-risk: Yes (AI/prompts, billing if credits involved)
- Workflows: employee-workflows.md (AI Tutor Interaction)

Ready: Yes
```

## Anti-Patterns

- Don't skip discovery for "simple" tasks — hidden coupling is common
- Don't load all docs upfront — load lazily based on actual coupling
- Don't ignore workflow docs — feature changes often break user journeys
- Don't proceed without invariants — if you can't find 3, docs may need updating
