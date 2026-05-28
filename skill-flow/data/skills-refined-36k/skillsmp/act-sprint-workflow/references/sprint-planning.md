# Sprint Planning Reference

## Velocity Calculation

```typescript
// Fetch velocity from last 3 sprints
const velocity = await fetch('/api/dashboard/velocity').then(r => r.json());
const avgVelocity = velocity.averageVelocity;

// Fetch backlog issues
const query = `query { ... filter Sprint = "Backlog", sort Priority desc }`;
const backlogIssues = await fetchGitHubProjects(query);

// Recommend top N by priority
const recommended = backlogIssues.slice(0, avgVelocity);
```

## Expected Output Format

```
📊 Sprint Planning for Sprint 5

Historical Velocity:
  Sprint 2: 12 issues
  Sprint 3: 10 issues
  Sprint 4: 11 issues
  → Average: 11 issues/sprint

📋 Backlog Analysis:
  Total: 47 issues
  Critical: 2, High: 12, Medium: 23, Low: 10

🎯 Recommended for Sprint 5 (11 issues):
  [Critical]
  #45 - Security: Add webhook signature verification

  [High Priority]
  #33 - Enhancement: Add velocity chart component
  ...

Breakdown:
  By Type: Enhancement: 7, Bug: 2, Task: 2
  By Project: Empathy Ledger: 3, ACT Studio: 5
```

## Capacity Planning

- Standard sprint: 2 weeks
- Average velocity: ~11 issues/sprint
- Buffer for emergent work: 20%
- Recommended load: 9 planned + 2 buffer
