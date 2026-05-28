# Discovery State: Cross-Service Dependency Tracker

**Updated**: 2026-01-18 14:30 UTC
**Iteration**: 3
**Phase**: Story Development

---

## Problem Understanding

### Problem Statement

Engineering teams working on features spanning multiple microservices (typically 2-5 services per feature) lose visibility into cross-service dependencies because each service team uses different project management tools (mix of JIRA, Azure DevOps, Linear, GitHub Projects). This tool fragmentation results in:

1. **Late discovery**: Dependencies found through ad-hoc Slack conversations or during code review, not during planning
2. **Integration failures**: Issues discovered during deployment to staging/production rather than during development
3. **Duplicate effort**: Multiple teams unknowingly work on overlapping changes to shared services
4. **Status blindness**: No single source of truth for feature progress across service boundaries
5. **Coordination overhead**: Feature Developers spend 3-4 hours per week manually tracking down dependency information

This affects approximately 45 Feature Developers across 8 product teams managing 23 microservices in a system handling 2M requests/day.

### Personas

| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| Feature Developer | Software engineer implementing features that span 2-5 microservices. Works on 2-3 features concurrently. Needs to coordinate with 3-6 other developers per feature. | Understand all service dependencies early in development, coordinate changes with relevant Service Owners, deliver integrated features without late-stage integration surprises, minimize time spent on coordination overhead |
| Service Owner | Senior engineer or tech lead responsible for maintaining one specific microservice. Reviews all incoming changes to their service. Plans service roadmap 1-2 quarters ahead. | Know when their service is a dependency for in-flight features, allocate time for reviews without schedule conflicts, maintain service stability and API contract integrity, prevent breaking changes from reaching production |

### Current State vs. Desired State

**Today (without feature)**:
- Each service team uses different project management tools based on team preference
- Dependencies discovered through:
  - Slack messages ("Hey, does anyone know if feature X affects auth-service?")
  - Code review comments ("This needs coordination with the payments team")
  - Architecture review meetings (weekly, but often too late)
- Integration testing happens in shared staging environment
  - Coordination via spreadsheet tracking which features are in staging
  - Test failures traced manually across services
  - Unclear which commit broke integration
- No proactive notifications when dependencies change
- Service Owners learn about dependent features when PR is opened (often too late for planning)
- Average: 8 integration bugs per month reach production
- Feature Developers report spending 3-4 hours/week on coordination

**Tomorrow (with feature)**:
- Automatic dependency detection across all project management tools
- Dependency graph visualization showing:
  - All services affected by a feature
  - All features depending on a service
  - Bidirectional relationship visibility
- Proactive notifications when dependencies change
- Integration test status aggregated across all dependent services
- Service Owners can plan ahead seeing timeline of incoming features
- Target: <30 minutes/week coordination overhead for Feature Developers
- Target: 60% reduction in integration bugs reaching production

### Constraints

- **Technical**: Must integrate with existing tools (JIRA, Azure DevOps, Linear, GitHub Projects, Jenkins, GitHub Actions, CircleCI) - cannot require migration to new systems
- **Business**: 45 Feature Developers and 15 Service Owners across 8 teams are the user base
- **Performance**: System handles 23 microservices currently, but architecture growing to 35-40 services next year
- **Timeline**: P1 features needed for Q2 planning cycle (8 weeks from now)
- **Access**: Some services have restricted visibility - solution must respect existing permission boundaries

---

## Story Landscape

### Story Status Overview

| # | Story | Priority | Status | Confidence | Blocked By |
|---|-------|----------|--------|------------|------------|
| 1 | View cross-service dependencies | P1 | ✅ In SPEC | 100% | - |
| 2 | Get dependency change notifications | P2 | ✅ In SPEC | 100% | - |
| 3 | Track integration test status | P1 | ✅ In SPEC | 100% | - |
| 4 | Visualize feature timeline | P2 | 🔄 In Progress | 85% | Q52 |
| 5 | Export dependency data | P3 | ⏳ Queued | 30% | Story 4 |
| 6 | Service health dashboard | P3 | 🆕 New (emerged from Q54) | 15% | - |

### Story Dependencies

```
Story 1 (View dependencies) ──────┐
                                  ├──► Story 2 (Notifications) - needs dependency data
                                  │
                                  └──► Story 5 (Export) - exports dependency graph

Story 3 (Test status) ──────────────► Independent

Story 4 (Timeline) ──────────────────► Story 5 (Export) - exports timeline data

Story 6 (Health dashboard) ──────────► Independent (but may affect Story 1 - watching)
```

### Proto-Stories / Emerging Themes

*Potential stories not yet crystallized:*
- **API contract diff viewer**: Show API changes between service versions to help Feature Developers understand impact - *Mentioned in Q54, needs more exploration*
- **Slack bot commands**: Quick dependency lookups without opening dashboard - *Needs prioritization discussion*

---

## Completed Stories Summary

| # | Story | Priority | Completed | Key Decisions | Revision Risk |
|---|-------|----------|-----------|---------------|---------------|
| 1 | View cross-service dependencies | P1 | 2026-01-16 | D1, D3, D7 | 🟢 Low |
| 2 | Get dependency change notifications | P2 | 2026-01-17 | D4, D8, D9 | 🟡 Medium - watching Q54 |
| 3 | Track integration test status | P1 | 2026-01-18 | D5, D10, D11 | 🟢 Low |

*Full stories in SPEC.md*

---

## In-Progress Story Detail

### Story 4: Visualize Feature Timeline (Priority: P2)

**One-line**: As a Service Owner, I want to see a timeline visualization of when features affecting my service are planned for development, testing, and deployment, so that I can plan my service's roadmap and allocate time for reviews without scheduling conflicts.

**Current Confidence**: 85%

**Working Understanding**:

Service Owners (15 users) need forward visibility into when features will affect their service. Currently they learn about dependent features only when PRs are opened, which is too late to plan their time or raise concerns about service roadmap conflicts.

Timeline should show:
- Features that depend on Service Owner's service
- Estimated start, testing, and deployment dates for each feature
- Feature owners for coordination
- Confidence level in timeline (firm dates vs. rough estimates)

This enables Service Owners to:
- Block time for code reviews
- Flag conflicts with service roadmap early
- Reach out to Feature Owners proactively

**Draft Acceptance Scenarios**:

1. **Given** Service Owner Mike owns user-service, and 3 features are planned that depend on user-service, **When** Mike views timeline, **Then** he sees:
   - All 3 features on timeline with estimated date ranges
   - Current phase for each feature (Planning, Development, Testing, Deployment)
   - Feature owners' names and contact info
   - Option to filter by date range or phase
   - *Confidence*: High
   - *Open questions*: None

2. **Given** a feature "User Auth v2" has firm deployment date (2026-02-15), **When** Service Owner views timeline, **Then**:
   - Feature shown with solid line/high confidence indicator
   - Deployment date clearly marked
   - Lead time visible (how many days until deployment)
   - *Confidence*: Medium
   - *Open questions*: Q52 (how to handle features without firm dates?)

3. **Given** Service Owner's service (user-service) is a dependency for 8 features spanning 3 months, **When** viewing timeline, **Then**:
   - Timeline doesn't become visually overwhelming
   - Features grouped by month or week
   - Can expand/collapse groups for detail
   - Export timeline for sharing with team
   - *Confidence*: Medium
   - *Open questions*: Q52, Q53 (performance with many features)

4. **Given** a feature's timeline changes (deployment moved from Feb 15 to Mar 1), **When** Service Owner next views timeline, **Then**:
   - Updated date reflected immediately
   - Change highlighted or indicated with "Recently updated" badge
   - Optional notification of timeline changes (connects to Story 2)
   - *Confidence*: Low
   - *Open questions*: Q52, Q53 (connects to notification preferences from Story 2 - might need revision)

**Blocking Questions**: Q52
**Clarifying Questions**: Q53, Q55

**Draft Edge Cases**:
- Feature has no deployment date (in planning phase) — *Handling: Show as "Date TBD" with estimated quarter, Q52*
- Timeline spans more than 6 months — *Handling: Default view shows next 3 months, expandable, Q53*
- Service has zero dependent features — *Handling: Show "No upcoming features" with helpful message*
- User lacks permission to view certain features — *Handling: Show count of restricted features, no details*

**Draft Requirements**:
- FR-014: System MUST support timeline visualization for Service Owners — *Confidence: High*
- FR-015: System MUST display timelines with up to 20 features without performance degradation — *Confidence: Medium, depends on Q53*
- FR-016: System MUST update timeline within 30 seconds when feature dates change — *Confidence: Low, depends on Q52*
- FR-017: System MUST support date filtering (next week, next month, next quarter, custom range) — *Confidence: High*

---

## Watching List

*Items that might affect graduated stories:*

- **Q54**: "Should we show API contract changes in dependency view?" — *If yes, Story 1 may need revision to add contract diff visualization*
- **Story 6 scope**: Service health dashboard may overlap with Story 1 dependency view - *need to clarify boundaries*

---

## Glossary

- **Feature**: A unit of work spanning one or more microservices, tracked in project management tools. Has owner, status, timeline, and dependencies.
- **Service**: A microservice in the system architecture. Has owner (Service Owner), version, API contract, deployment status.
- **Service Owner**: Person responsible for maintaining a specific microservice. Reviews all changes, plans roadmap.
- **Feature Developer**: Person implementing a feature that may span multiple services. Coordinates with Service Owners.
- **Dependency**: Relationship between a Feature and a Service it modifies or depends on.
- **Integration Test**: Automated test verifying a Feature works correctly across all its dependent Services.
- **Significant Change**: Version bump, API contract change, or status change to Ready for Testing/Deployed.
- **Timeline Confidence**: Indicator of how firm a feature's schedule is (firm date vs. rough estimate vs. TBD).

---

## Next Actions

- Resolve Q52 to finalize Story 4 scenarios with date handling
- Validate Story 4 scenarios with 2-3 Service Owners for feedback
- Check graduation criteria for Story 4
- If ready: Graduate Story 4 to SPEC.md
- Then: Begin Story 5 development
