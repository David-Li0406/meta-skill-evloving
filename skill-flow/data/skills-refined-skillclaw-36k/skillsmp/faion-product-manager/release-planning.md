---
id: release-planning
name: "Release Planning"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Release Planning

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #release, #planning |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-impl-planner-agent |

---

## Problem

Releases are chaotic, missed, or anticlimactic. Common issues:
- No clear release strategy
- Features ready but not shipped
- Broken releases to customers
- No communication plan

**The root cause:** No structured approach to bundling, planning, and executing releases.

---

## Framework

### What is Release Planning?

Release planning is deciding what goes into each release, when it ships, and how it's communicated. It answers: "What are we shipping, when, and to whom?"

### Release Types

| Type | Frequency | Scope | Risk |
|------|-----------|-------|------|
| Major | Quarterly | Large features, breaking changes | High |
| Minor | Monthly | New features, improvements | Medium |
| Patch | Weekly/As needed | Bug fixes, security | Low |
| Hotfix | Immediate | Critical fixes | Very Low |

### Release Planning Process

#### Step 1: Define Release Goals

**Questions:**
- What user outcomes does this release enable?
- What business metrics should it move?
- What's the theme or story?

**Template:**
```
Release [Version]
Goal: [Primary outcome]
Success Metric: [How we'll measure]
Theme: [Optional narrative]
```

#### Step 2: Select Release Contents

**Include:**
- Completed features meeting definition of done
- Related bug fixes
- Documentation updates
- Configuration changes

**Exclude:**
- Half-finished features
- Unrelated bug fixes (next release)
- "Just one more thing" scope creep

#### Step 3: Assess Release Readiness

**Checklist:**
- [ ] All features code complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Migrations tested
- [ ] Rollback plan exists
- [ ] Support team briefed
- [ ] Release notes written

#### Step 4: Plan Communication

**Stakeholders to notify:**
- Internal: Team, support, sales
- External: Customers, partners, public

**Communication assets:**
- Release notes
- Blog post / changelog
- Email to customers
- Social media
- In-app notifications

#### Step 5: Execute Release

**Release process:**
1. Final testing in staging
2. Announce maintenance window (if needed)
3. Deploy to production
4. Verify deployment
5. Monitor metrics
6. Announce release

#### Step 6: Post-Release

- Monitor for issues
- Gather feedback
- Retrospective
- Update roadmap

---

## Templates

### Release Plan

```markdown
## Release Plan: v[X.Y.Z]

### Metadata
- **Release Date:** [Date]
- **Release Manager:** [Name]
- **Type:** [Major/Minor/Patch]

### Release Goal
[What this release achieves for users]

### Success Metrics
| Metric | Current | Target | Tracking |
|--------|---------|--------|----------|
| [Metric] | [X] | [Y] | [How] |

### Contents

#### Features
| Feature | Ticket | Owner | Status |
|---------|--------|-------|--------|
| [Feature 1] | [#123] | [Name] | Ready |
| [Feature 2] | [#456] | [Name] | Ready |

#### Bug Fixes
| Fix | Ticket | Priority |
|-----|--------|----------|
| [Bug 1] | [#789] | High |

#### Other Changes
- [Config change]
- [Dependency update]

### Excluded (Next Release)
| Item | Reason |
|------|--------|
| [Feature] | Not ready |

### Dependencies
- [ ] [Dependency 1]
- [ ] [Dependency 2]

### Risks
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Plan] |

### Rollback Plan
[How to rollback if issues occur]

### Communication Plan

| Audience | What | When | Who |
|----------|------|------|-----|
| Internal team | Release notes | Day before | PM |
| Customers | Email + changelog | Day of | Marketing |
| Public | Blog post | Day of | Marketing |

### Timeline

| Time | Action | Owner |
|------|--------|-------|
| [T-1 day] | Final testing | QA |
| [Release day 9am] | Deploy to staging | Eng |
| [Release day 10am] | Deploy to production | Eng |
| [Release day 11am] | Send communications | Mkt |
| [Release day +1] | Monitor and retro | Team |
```

### Release Notes Template

```markdown
# Release Notes: v[X.Y.Z]
**Released:** [Date]

## Highlights
[1-2 sentence summary of the most exciting change]

## New Features

### [Feature Name]
[Brief description of what it does and why it matters]

**How to use:** [Quick instructions]

### [Feature Name]
...

## Improvements
- [Improvement 1]
- [Improvement 2]

## Bug Fixes
- Fixed [issue description]
- Resolved [issue description]

## Breaking Changes
[If any, with migration instructions]

## Known Issues
- [Issue 1] - Workaround: [Solution]

## Coming Soon
[Teaser of what's next]

---
Questions? [Contact/Support link]
```

---

## Examples

### Example 1: SaaS Monthly Release

**v2.4.0 Release Plan:**

**Goal:** Enable team collaboration

**Contents:**
- Real-time collaboration (feature)
- Comments on tasks (feature)
- 15 bug fixes

**Timeline:**
- Mon: Feature freeze, testing
- Wed: Staging deploy, final QA
- Thu: Production deploy 2pm
- Thu: Customer email + blog post

**Success:** Team features used by 20% of active users in first week.

### Example 2: Solo Product Patch Release

**v1.2.3 Release Plan:**

**Goal:** Fix critical payment bug

**Contents:**
- Payment processing fix
- 2 minor UI bugs

**Timeline:**
- Same day deploy
- Quick changelog update
- Email to affected customers

**Success:** Zero payment failures.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Shipping on Fridays | Monday-Wednesday releases |
| No rollback plan | Always have one-click rollback |
| Last-minute additions | Feature freeze 24-48h before |
| No communication | Always announce, even small releases |
| Skipping testing | Staging deploy is mandatory |
| No monitoring | Watch metrics for 24h post-release |
| Monster releases | Smaller, more frequent is better |

---

## Related Methodologies

- **roadmap-design:** Roadmap Design
- **task-creation-parallelization:** Task Creation & Parallelization
- **schedule-development:** Schedule Development
- **change-control:** Change Control
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

## Agent

**faion-mlp-impl-planner-agent** helps with release planning. Invoke with:
- "Plan a release for [feature list]"
- "Create release notes for [changes]"
- "What should be in release [version]?"
- "Review my release plan: [content]"

---

*Methodology | Product | Version 1.0*
