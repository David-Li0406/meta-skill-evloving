---
name: effort-estimator
description: Analyze feature requests and provide technical effort estimates with risk assessment
level: 2
---

# Effort Estimator Skill

> **Note**: This is a sample skill that estimates technical effort for feature requests. Your version should be tailored to your team's velocity and complexity factors.

## Purpose

This skill analyzes feature descriptions (written in product/business language) and provides:
- Effort estimates with confidence levels
- Breakdown by discipline (backend, frontend, testing, etc.)
- Risk identification and complexity factors
- Recommendations for breaking down large features

## When to Apply

Use this skill when:
- Product managers describe a new feature
- Stakeholders ask "How long will this take?"
- Planning sprint capacity
- Prioritizing backlog items by effort vs. value

## Effort Categories

### 🟢 Small (< 3 days, 1-5 story points)

- Single component or endpoint change
- No database schema changes
- No new dependencies
- Existing patterns can be reused
- Limited testing scope

**Example**: Add social media share buttons to character pages

### 🟡 Medium (3-7 days, 8-13 story points)

- Multiple component changes
- Minor database changes (new columns, simple migrations)
- Some new patterns or integrations
- Moderate testing requirements
- May touch 2-3 layers (e.g., backend + frontend)

**Example**: Add episode filtering by genre on the browse page

### 🟠 Large (1-2 weeks, 21+ story points)

- New feature area
- Database schema changes with migrations
- New API endpoints
- New frontend pages or complex components
- Comprehensive testing required
- Multiple team members involved

**Example**: Episode Detail pages with transcripts, character appearances, and streaming links

### 🔴 Extra Large (> 2 weeks, requires breakdown)

- New subsystem or service
- Significant infrastructure changes
- External service integrations
- Performance or scaling implications
- Should be broken into smaller deliverables

**Example**: Full-text search across all content with autocomplete

## Complexity Factors

When estimating effort, consider these complexity multipliers:

### Data Complexity

| Factor | Impact |
|--------|--------|
| New table(s) required | +50% effort |
| Many-to-many relationships | +30% effort |
| Data migration needed | +25% effort |
| External data sources | +40% effort |

### Integration Complexity

| Factor | Impact |
|--------|--------|
| New external API | +50% effort |
| Authentication changes | +30% effort |
| Real-time updates needed | +40% effort |
| Third-party service | +25% effort |

### Frontend Complexity

| Factor | Impact |
|--------|--------|
| Complex state management | +25% effort |
| Animations/transitions | +20% effort |
| Offline support | +40% effort |
| Accessibility requirements | +15% effort |

### Testing Complexity

| Factor | Impact |
|--------|--------|
| E2E testing required | +20% effort |
| Performance testing | +25% effort |
| Security testing | +30% effort |
| Edge case coverage | +15% effort |

## Estimation Framework

When analyzing a feature request:

### Step 1: Identify Components

Reference `docs/ARCHITECTURE.md` to understand:
- Which backend routes need changes
- Which frontend pages/components are affected
- Database table impacts
- API contract changes

### Step 2: Break Down by Layer

```
Feature: [Feature Name]

Backend:
- Routes: [list changes needed]
- Services: [business logic changes]
- Database: [schema changes, migrations]
- Estimate: [Small/Medium/Large]

Frontend:
- Pages: [new or modified pages]
- Components: [new or modified components]
- State: [state management changes]
- Estimate: [Small/Medium/Large]

Testing:
- Unit tests: [scope]
- Integration tests: [scope]
- E2E tests: [if applicable]
- Estimate: [Small/Medium/Large]

Infrastructure:
- Changes needed: [if any]
- Estimate: [None/Small/Medium]
```

### Step 3: Identify Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk name] | High/Medium/Low | High/Medium/Low | [How to reduce] |

### Step 4: Output Estimate

```
## Effort Estimate: [Feature Name]

**Overall**: [Small/Medium/Large/Extra Large]
**Confidence**: [High/Medium/Low]
**Story Points**: [Range, e.g., 13-21]
**Calendar Time**: [Range, e.g., 1-2 weeks]

### Breakdown
| Area | Effort | Notes |
|------|--------|-------|
| Backend | [Small/Medium] | [Key work] |
| Frontend | [Small/Medium] | [Key work] |
| Testing | [Small/Medium] | [Scope] |
| Infrastructure | [None/Small] | [If needed] |

### Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### Recommendations
- [Break down suggestion if Large/XL]
- [Dependencies to resolve first]
- [Spikes or research needed]
```

## Example Estimates

### Example: Episode Detail Pages

**Feature**: "Users want to click on an episode and see full details including synopsis, character appearances, memorable quotes, and streaming links."

**Analysis**:
- Backend: New `/episodes/:id/full` endpoint with joined data (Medium)
- Frontend: New EpisodeDetail page, multiple components (Medium)
- Database: No schema changes, but complex joins (Low complexity)
- Testing: Component tests, API tests, E2E for navigation (Medium)

**Overall**: Large (1-2 weeks)
**Confidence**: High (similar to Character Detail)
**Story Points**: 21-34
**Risks**: 
- Many-to-many relationships (characters in episodes) add complexity
- Streaming links may require external API integration

### Example: Full-Text Search

**Feature**: "Users want to search for anything - characters, quotes, episodes - from a single search box."

**Analysis**:
- Backend: New search service, indexing strategy, query optimization (Large)
- Frontend: Search bar, results page, autocomplete, filters (Medium)
- Database: May need search index (PostgreSQL full-text or external) (Large)
- Infrastructure: Consider dedicated search service at scale (Medium)

**Overall**: Extra Large (> 2 weeks, break down required)
**Confidence**: Medium (depends on search technology choice)
**Story Points**: 55-89
**Recommendations**:
- Spike: Evaluate PostgreSQL full-text vs. Elasticsearch
- Phase 1: Basic search without autocomplete
- Phase 2: Autocomplete and advanced filtering
- Phase 3: Search relevance tuning

## Confidence Levels

- **High**: Feature is similar to something we've built before
- **Medium**: Some unknowns, but architecture is understood
- **Low**: Significant unknowns, new technology, or unclear requirements

When confidence is Low, recommend a spike or research phase before committing to timeline.
