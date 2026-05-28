# Build Roadmap Template

Use this template to create a phased implementation plan optimized for solo builder velocity.

---

## Template

```markdown
# Build Roadmap: {Project Name}

**Created:** {YYYY-MM-DD}
**Target MVP Date:** {YYYY-MM-DD}
**Target V1 Date:** {YYYY-MM-DD}

---

## Executive Summary

| Milestone | Duration | Key Deliverable |
|-----------|----------|-----------------|
| MVP | {X} weeks | {core feature working} |
| V1 | +{X} weeks | {polished product} |
| V2 | +{X} weeks | {growth features} |

**Total to sustainable product:** {X} weeks

---

## MVP Phase ({X} weeks)

### Goal
Get core loop working. Real users can derive value. "Good enough" beats perfect.

### Scope

**Must Have (launch blockers):**
1. {Feature 1} - {brief description}
2. {Feature 2} - {brief description}
3. {Feature 3} - {brief description}

**Explicitly NOT in MVP:**
- {Feature to defer}
- {Feature to defer}
- {Polish item to defer}

### Week-by-Week Plan

#### Week 1: Foundation

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | Project setup | Next.js + Supabase + Vercel configured |
| 3-4 | Auth flow | Login/logout/signup working |
| 5 | Base layout | App shell, navigation, routing |

**Gate:** Can deploy empty authenticated shell

#### Week 2: Core Data

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | Database schema | Core tables + RLS |
| 3-4 | CRUD API | Basic API routes working |
| 5 | UI components | List/detail views for core entity |

**Gate:** Can create, read, update, delete core entity

#### Week 3: Core Feature

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | {Feature 1} backend | Service logic complete |
| 3-4 | {Feature 1} frontend | UI complete |
| 5 | Integration | Feature fully working |

**Gate:** {Feature 1} works end-to-end

#### Week 4: MVP Polish

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | Error handling | User-friendly errors everywhere |
| 3 | Loading states | No blank screens |
| 4 | Edge cases | Empty states, validation |
| 5 | Deploy + test | MVP live |

**Gate:** MVP deployed, core loop validated

### MVP Definition of Done

- [ ] Core feature works end-to-end
- [ ] Auth flow complete
- [ ] Basic error handling
- [ ] Deployed to production
- [ ] Can onboard a real user
- [ ] No critical bugs

---

## V1 Phase (+{X} weeks)

### Goal
Polish the experience. Add secondary features. Make it feel complete.

### Scope

**Features:**
1. {Feature 4} - {description}
2. {Feature 5} - {description}
3. {Polish item} - {description}

**Improvements:**
- Better onboarding flow
- Performance optimization
- Enhanced error messages
- Mobile responsiveness

### Week-by-Week Plan

#### Week 5: Secondary Features

| Task | Duration | Notes |
|------|----------|-------|
| {Feature 4} | 2 days | {notes} |
| {Feature 5} | 2 days | {notes} |
| Integration testing | 1 day | - |

#### Week 6: Polish

| Task | Duration | Notes |
|------|----------|-------|
| Onboarding flow | 1 day | Welcome, tutorial |
| Loading/empty states | 1 day | All screens |
| Error handling | 1 day | Edge cases |
| Performance | 1 day | Optimize slow pages |
| Bug fixes | 1 day | Triage and fix |

#### Week 7: Testing & Launch Prep

| Task | Duration | Notes |
|------|----------|-------|
| E2E tests | 2 days | Critical paths |
| Docs/help | 1 day | Basic docs |
| Analytics | 1 day | Set up tracking |
| Final review | 1 day | Manual testing |

### V1 Definition of Done

- [ ] All MVP features polished
- [ ] Secondary features complete
- [ ] E2E tests passing
- [ ] Analytics configured
- [ ] Documentation exists
- [ ] Ready for public launch

---

## V2 Phase (+{X} weeks)

### Goal
Growth features. Integrations. Scale.

### Scope (Tentative)

Based on learnings from V1:

**Potential Features:**
- {Growth feature 1}
- {Integration 1}
- {Advanced feature}

**Potential Improvements:**
- {Based on user feedback}
- {Based on analytics}

### Planning Note

V2 scope should be determined after V1 launch based on:
- User feedback
- Usage analytics
- Revenue data
- Market changes

---

## Risk Management

### Identified Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | High | High | Strict MVP scope, defer features |
| Technical blockers | Medium | High | Prototype risky parts early |
| Motivation drop | Medium | High | Ship small wins frequently |
| External dependencies | Low | Medium | Have fallback options |

### Contingency Plans

**If behind schedule:**
- Cut scope, not quality
- Defer to V1 phase
- Ship what works

**If blocked on technical issue:**
- Time-box investigation (4 hours max)
- Simplify approach
- Ask for help

---

## Success Metrics

### MVP Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Launch | On time | Date achieved |
| Core loop | Works | Manual testing |
| First user | Onboarded | User count |

### V1 Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Users | {N} | Analytics |
| Retention | {X}% | Return visits |
| NPS | > 30 | Survey |

### V2 Success

| Metric | Target | How to Measure |
|--------|--------|----------------|
| MRR | ${X} | Stripe |
| Growth | {X}%/mo | Analytics |
| Churn | < {X}% | Subscriptions |

---

## Resource Requirements

### Time

| Phase | Hours/Week | Total Hours |
|-------|------------|-------------|
| MVP | {X} | {X} |
| V1 | {X} | {X} |
| V2 | {X} | {X} |

### Budget

| Category | MVP | V1 | V2 |
|----------|-----|----|----|
| Infrastructure | ${X}/mo | ${X}/mo | ${X}/mo |
| Tools | ${X}/mo | ${X}/mo | ${X}/mo |
| Marketing | $0 | ${X} | ${X}/mo |
| **Total** | **${X}** | **${X}** | **${X}/mo** |

### Tools Required

| Tool | Purpose | Cost |
|------|---------|------|
| Vercel | Hosting | Free → $20/mo |
| Supabase | Database | Free → $25/mo |
| Cursor/Claude | AI coding | $20/mo |
| Domain | Brand | $12/year |

---

## Checkpoints & Gates

### Weekly Checkpoint

Every Friday:
- [ ] Review week's accomplishments
- [ ] Update roadmap if needed
- [ ] Plan next week
- [ ] Log progress to tracker

### Phase Gates

Before advancing to next phase:

**MVP → V1:**
- [ ] Core feature works
- [ ] At least 1 real user
- [ ] No critical bugs
- [ ] Deployed to production

**V1 → V2:**
- [ ] V1 features complete
- [ ] User feedback collected
- [ ] Analytics reviewed
- [ ] Decision on V2 scope made

---

## Notes & Decisions

### Design Decisions

| Decision | Choice | Rationale | Date |
|----------|--------|-----------|------|
| {decision} | {choice} | {why} | {date} |

### Lessons Learned

| Date | Lesson | Action |
|------|--------|--------|
| {date} | {lesson} | {what changed} |

### Deferred Items

| Item | Reason | Revisit In |
|------|--------|------------|
| {feature} | {why deferred} | V1/V2/Never |
```

---

## Usage Notes

1. Be realistic about time estimates (then add 50%)
2. Scope ruthlessly for MVP
3. Update weekly as you learn
4. Track deferred items for later
5. Celebrate shipping, even if imperfect
