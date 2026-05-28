# Daily View Template

## Purpose

The daily view is the primary interface for managing today's work across all domains.

---

## Template

```markdown
# Today: {YYYY-MM-DD}

## Context Check
- **Energy:** {1-10}
- **Volume:** {Light/Medium/Heavy}
- **Available hours:** {X}
- **Method:** {selected method}

---

## Top 3 (Non-negotiable)

1. [ ] {P1 task} — {domain}
2. [ ] {P2 task} — {domain}
3. [ ] {P3 task} — {domain}

---

## By Domain

### ID8 Projects
| Task | Project | Est | Priority | Status |
|------|---------|-----|----------|--------|
| {task} | {project-slug} | {time} | P{n} | [ ] |
| {task} | {project-slug} | {time} | P{n} | [ ] |
| {task} | {project-slug} | {time} | P{n} | [ ] |

### TV Production
| Task | Show/Project | Est | Priority | Status |
|------|--------------|-----|----------|--------|
| {task} | {show} | {time} | P{n} | [ ] |
| {task} | {show} | {time} | P{n} | [ ] |

### Life Admin
| Task | Category | Est | Priority | Status |
|------|----------|-----|----------|--------|
| {task} | {category} | {time} | P{n} | [ ] |
| {task} | {category} | {time} | P{n} | [ ] |

---

## Time Blocks

| Time | Block Type | Focus |
|------|------------|-------|
| {HH:MM} - {HH:MM} | {Deep/Shallow/Meeting} | {task or batch} |
| {HH:MM} - {HH:MM} | {Deep/Shallow/Meeting} | {task or batch} |
| {HH:MM} - {HH:MM} | {Deep/Shallow/Meeting} | {task or batch} |
| {HH:MM} - {HH:MM} | {Deep/Shallow/Meeting} | {task or batch} |

---

## Parking Lot
{Tasks captured during day - process during review}

- {captured item}
- {captured item}

---

## Day Log

### Morning
- {time}: {what happened}
- {time}: {what happened}

### Afternoon
- {time}: {what happened}
- {time}: {what happened}

### Blockers
- {blocker and what it blocked}

---

## End of Day Review

### Completed
- [x] {completed task}
- [x] {completed task}

### Not Completed
- [ ] {incomplete task} → {action: tomorrow/next week/delegate}
- [ ] {incomplete task} → {action}

### Metrics
- **Tasks planned:** {count}
- **Tasks completed:** {count}
- **Completion rate:** {%}
- **Biggest win:** {what}
- **Biggest blocker:** {what}

### Tomorrow's Top Priority
{The one thing to start with tomorrow}

---

*Last updated: {HH:MM}*
```

---

## Field Explanations

### Context Check
Quick assessment to calibrate the day:
- **Energy:** 1-10 scale of current capacity
- **Volume:** Light (<5 tasks), Medium (5-10), Heavy (10+)
- **Available hours:** Realistic working hours today
- **Method:** Which productivity method to apply

### Top 3
The non-negotiable priorities. These must get done.
- Maximum 3 items
- Should span domains appropriately
- First task should be ready to start immediately

### By Domain Sections
Tasks organized by work domain:
- **ID8 Projects:** Links to ID8Tracker project
- **TV Production:** Reality TV work
- **Life Admin:** Personal tasks

### Time Blocks
Optional scheduling by time:
- **Deep:** Protected focus work (90-120 min)
- **Shallow:** Admin, email, quick tasks (30-60 min)
- **Meeting:** Calls, collaboration

### Parking Lot
Capture zone for thoughts during the day:
- Don't organize, just capture
- Process during end-of-day review

### Day Log
Optional running log of what happened:
- Helps reconstruct the day
- Useful for patterns

### End of Day Review
Closing ritual:
- Mark what's done
- Decide fate of incomplete items
- Identify tomorrow's first task

---

## Usage

### Morning Setup (5 min)
1. Copy template to today.md
2. Fill context check
3. Set Top 3
4. Add tasks by domain
5. Optional: Add time blocks
6. Start first task

### During Day
1. Work from Top 3 first
2. Capture new items to Parking Lot
3. Update log if helpful
4. Check off completed items

### Evening Close (5 min)
1. Complete End of Day Review
2. Process Parking Lot
3. Set tomorrow's first task
4. Archive to weekly summary

---

## Variations

### Minimal Daily View
Just the essentials:
```markdown
# Today: {date}

## Top 3
1. [ ]
2. [ ]
3. [ ]

## Other
- [ ]
- [ ]

## Captured
-
```

### Time-Blocked View
When schedule is strict:
```markdown
# Today: {date}

6:00 -
7:00 -
8:00 -
9:00 -
10:00 -
11:00 -
12:00 -
1:00 -
2:00 -
3:00 -
4:00 -
5:00 -
```

### Domain-First View
When domains are clearly separated:
```markdown
# Today: {date}

## ID8 (Morning)
- [ ]
- [ ]

## TV (Afternoon)
- [ ]

## Life (Evening)
- [ ]
```
