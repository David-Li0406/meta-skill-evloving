# Sample PRD: Task Time Tracker

This is a complete example of a demo-grade PRD following the 7-section structure.

---

## 1. One-Sentence Problem

> Freelancers struggle to accurately track time spent on client projects because switching between tasks breaks focus and manual logging is forgotten, resulting in unbilled hours and inaccurate invoices.

## 2. Demo Goal (What Success Looks Like)

**Success Criteria:**
- User can start/stop a timer for any project with one click
- Time entries appear in a daily log
- User can see total hours per project
- Timer persists across page refreshes

**Non-Goals:**
- Invoicing or billing integration
- Team collaboration features
- Mobile app (web only)
- Historical reporting beyond current week

## 3. Target User (Role-Based)

| Attribute | Value |
|-----------|-------|
| Role | Freelance developer/designer |
| Context | Works on 2-5 client projects simultaneously |
| Skill Level | Comfortable with web apps, not technical |
| Key Constraint | Context-switching frequently; forgets to log time |

## 4. Core Use Case (Happy Path)

**Start Condition:** User opens app, no timer running

**Flow:**
1. User sees list of their projects
2. User clicks "Start Timer" on a project
3. Timer begins counting (visible in header)
4. User works on project
5. User clicks "Stop Timer" when done
6. Time entry appears in daily log with duration
7. User sees updated total hours for that project

**End Condition:** Time entry saved, totals updated, no timer running

## 5. Functional Decisions (What It Must Do)

| ID | Function | Notes |
|----|----------|-------|
| F1 | Start/stop timer for a project | One active timer at a time |
| F2 | Display running timer in header | Shows project name + elapsed time |
| F3 | Auto-save time entries | Save on stop, persist on refresh |
| F4 | Show daily time log | Grouped by date, sorted newest first |
| F5 | Calculate project totals | Sum of all entries per project |
| F6 | Create/edit projects | Name and optional hourly rate |
| F7 | Edit time entries | Adjust start/end time, delete entry |

## 6. UX Decisions (What the Experience Is Like)

### 6.1 Entry Point
- User lands on dashboard showing:
  - Active timer (if any) in sticky header
  - Project list with quick-start buttons
  - Today's time log below

### 6.2 Inputs
| Input | Type | Validation |
|-------|------|------------|
| Project name | Text | Required, 1-50 chars |
| Hourly rate | Number | Optional, >= 0 |
| Time entry | Duration | Auto-calculated from timer |

### 6.3 Outputs
| Output | Format | Location |
|--------|--------|----------|
| Running timer | HH:MM:SS | Sticky header |
| Time entries | Cards with duration | Daily log |
| Project totals | "X hrs this week" | Project card |

### 6.4 Feedback & States

| State | Visual Treatment |
|-------|------------------|
| Timer running | Pulsing dot + green accent |
| Timer stopped | Static, muted color |
| Saving | Brief toast "Saved" |
| Loading | Skeleton cards |

### 6.5 Errors (Minimum Viable Handling)

| Scenario | Response |
|----------|----------|
| Start timer while one running | Auto-stop current, start new, show toast |
| Delete time entry | Confirm dialog before delete |
| Network error on save | Retry 3x, then show error toast with retry button |
| Page closes with running timer | Timer state persists in localStorage |

## 7. Data & Logic (At a Glance)

### 7.1 Inputs

| Data | Source |
|------|--------|
| Projects | User-created, stored in database |
| Time entries | System-generated from timer |
| Current time | Browser (for timer display) |

### 7.2 Processing

```
Timer Start → Store start timestamp
Timer Stop → Calculate duration → Create entry → Update totals
Page Load → Check localStorage for active timer → Resume if found
```

### 7.3 Outputs

| Data | Destination |
|------|-------------|
| Time entries | Database (permanent) |
| Active timer | localStorage (temporary) |
| UI state | React state (session) |

---

## Scope Summary

### In Scope (Core)
- Timer start/stop
- Time entry creation
- Daily log view
- Project totals

### In Scope (Supporting)
- Edit/delete entries
- Create/edit projects
- Timer persistence

### Out of Scope
- Invoicing
- Team features
- Mobile app
- Reporting beyond current week
- Integrations (calendar, billing)

---

## Implementation Notes

**Risk Assessment:**
| Feature | Risk Level | Gate |
|---------|------------|------|
| Timer logic | Medium | Unit tests |
| Data persistence | High | E2E tests |
| UI components | Low | Visual review |

**Sprint Suggestion:**
1. Foundation: Data models, API routes, basic UI
2. Core: Timer logic, entry creation, daily log
3. Polish: Edit flows, error handling, persistence
