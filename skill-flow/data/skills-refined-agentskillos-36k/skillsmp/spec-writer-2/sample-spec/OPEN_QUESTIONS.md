# Open Questions: Cross-Service Dependency Tracker

## 🔴 Blocking

### Story 4: Visualize Feature Timeline
- **Q52**: How should timeline visualization handle features that don't have firm deployment dates (still in planning phase)?
  - *Context*: Many features start with rough estimates ("sometime in Q2") that firm up over time. Need to show these without misleading Service Owners about confidence level.
  - *Blocking*: Can't finalize acceptance scenario 2 and 4 for Story 4 without knowing how to represent uncertain dates
  - *Options considered*: (1) Show as "TBD" with quarter estimate, (2) Show with low-confidence visual indicator (dotted line), (3) Don't show until date is firm
  - *Preference*: Option 2 - show with confidence indicator - but need user validation

## 🟡 Clarifying

### Story 4: Visualize Feature Timeline
- **Q53**: What's the maximum number of features we should optimize for in a Service Owner's timeline view?
  - *Context*: Some popular services (auth-service, user-service) might have 15-20 dependent features concurrently. Need to know performance target.
  - *Story*: Story 4
  - *Not blocking*: Can graduate Story 4 with assumption of <20 features, document as constraint

- **Q55**: Should timeline visualization support filtering by Feature Owner or just by date range?
  - *Context*: Service Owner might want to see "all features owned by Engineering Team A" that affect their service
  - *Story*: Story 4
  - *Not blocking*: Can add as enhancement after graduation if needed

### Story 5: Export Dependency Data
- **Q56**: What export formats do users need? (CSV, JSON, PDF, PNG image?)
  - *Context*: Different use cases: CSV for spreadsheet analysis, JSON for tooling integration, PNG for presentations
  - *Story*: Story 5 (queued)
  - *Can wait*: Story 5 not yet in active development

## 🔵 Research Pending

### Story 6: Service Health Dashboard (New)
- **Q57**: What health metrics are most valuable to Service Owners for planning?
  - *Context*: Emerged from Q54 discussion about showing more service context. Need to research what metrics matter.
  - *Research needed*: Interview 3-5 Service Owners about current pain points
  - *Story*: Story 6 (new, not yet prioritized)

## 🟠 Watching (May Affect Graduated)

### Cross-Cutting / Affects Graduated Stories
- **Q54**: Should dependency view (Story 1) show API contract changes between service versions to help Feature Developers understand impact of dependencies?
  - *Context*: During Story 4 development, user mentioned "would be helpful to see what changed in the API"
  - *Affects*: Story 1 (may need revision to add contract diff view)
  - *Also affects*: Story 2 (may need to notify about contract changes specifically)
  - *Watching*: If answer is "Yes" and it's P1/P2 → Story 1 and Story 2 need additive revisions
  - *If "No" or P3*: Capture as future enhancement, no revision needed now

### Proto-Story Scope Overlap
- **Q58**: Does Story 6 (Service Health Dashboard) overlap too much with Story 1 (View Dependencies)?
  - *Context*: Story 6 might show service status, versions, recent changes - which partially overlaps with dependency view
  - *Affects*: Story 1 (may need revision to clarify scope boundaries)
  - *Watching*: Need to crystallize Story 6 scope before knowing if revision needed

---

## Question Log Summary

- **Total questions tracked**: 58 (Q1-Q58)
- **Currently open**: 7 (Q52-Q58)
- **Resolved in this iteration**: 4 (Q49-Q51 resolved during Story 3 development, Q48 resolved during Story 4 planning)
- **Blocking current work**: 1 (Q52)
- **May affect graduated stories**: 2 (Q54, Q58)
