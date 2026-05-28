# PRD Examples

Real-world examples of well-written PRD components.

## Problem Statement Examples

### Example 1: Export Feature

**✅ Strong Problem Statement:**

> **Current State:** Account managers manually compile usage data from multiple dashboard screens into spreadsheets for quarterly business reviews. This process takes 4-6 hours per customer and is error-prone.
>
> **Impact:**
> - 200+ hours/quarter spent on manual reporting across the team
> - 15% of reports contain data errors requiring correction
> - QBRs are delayed by average of 3 days due to report preparation
>
> **Opportunity:** Automated export would save 180+ hours/quarter and eliminate data errors, enabling account managers to focus on strategic customer conversations.

### Example 2: Performance Issue

**✅ Strong Problem Statement:**

> **Current State:** Dashboard load time averages 8.2 seconds for customers with 10,000+ records, compared to our target of <3 seconds.
>
> **Impact:**
> - 23% of enterprise users abandon the dashboard before it loads (analytics data)
> - NPS scores for enterprise segment are 15 points lower than SMB
> - Support tickets about "slow dashboard" increased 40% QoQ
>
> **Opportunity:** Reducing load time to <3 seconds would improve enterprise retention and reduce support burden.

---

## User Story Examples

### Example 1: Report Export

```markdown
**US-1:** As an account manager, I want to export a customer's usage report
as a branded PDF so that I can include it in quarterly business reviews
without manual formatting.

**Acceptance Criteria:**
- [ ] Export button visible on customer dashboard
- [ ] PDF includes company logo and branding
- [ ] PDF contains: usage summary, trend charts, top features, YoY comparison
- [ ] Export completes within 10 seconds for accounts with <100k events
- [ ] PDF is ADA accessible (tagged for screen readers)

**Given-When-Then:**
Given I am logged in as an account manager
And I am viewing a customer's usage dashboard
When I click "Export as PDF"
Then a branded PDF downloads containing all dashboard metrics
And the filename follows pattern: {company}-usage-{date}.pdf
```

### Example 2: Bulk Actions

```markdown
**US-2:** As an admin, I want to bulk update user permissions so that
I can efficiently onboard new teams without editing users one-by-one.

**Acceptance Criteria:**
- [ ] Can select multiple users via checkboxes
- [ ] Bulk action menu appears when users selected
- [ ] Can apply permission template to selected users
- [ ] Confirmation modal shows affected users before applying
- [ ] Audit log records bulk change with all affected user IDs
- [ ] Can undo bulk action within 5 minutes

**Given-When-Then:**
Given I am logged in as an admin
And I have selected 5 users from the user list
When I click "Apply Permission Template"
And I select "Standard User" template
And I confirm the action
Then all 5 users have "Standard User" permissions
And the audit log shows one entry with all 5 user IDs
```

---

## Requirements Examples

### Functional Requirements Table

| ID | Requirement | User Story | Priority | Acceptance Criteria |
|----|-------------|------------|----------|---------------------|
| FR-1 | Users can export dashboard as PDF | US-1 | P0 | PDF contains all visible metrics; downloads in <10s |
| FR-2 | PDF includes company branding | US-1 | P0 | Logo, colors match brand guidelines |
| FR-3 | Users can schedule recurring exports | US-1 | P1 | Daily, weekly, monthly options; email delivery |
| FR-4 | Users can customize PDF sections | US-1 | P2 | Toggle sections on/off; reorder sections |
| FR-5 | Export available in CSV format | US-1 | P2 | Same data as PDF in tabular format |

### Non-Functional Requirements

```markdown
#### Performance
- PDF generation: <10 seconds for accounts with <100k events
- PDF generation: <30 seconds for accounts with <1M events
- Concurrent export limit: 50 per minute (rate limited)

#### Security
- Exports require authenticated session
- PDF watermarked with "Confidential - {Company Name}"
- Export audit logged with user ID, timestamp, customer ID

#### Accessibility
- PDF tagged for screen reader compatibility (PDF/UA standard)
- Charts include alt text descriptions
- Color choices meet WCAG 2.1 AA contrast requirements

#### Reliability
- Export retry on failure (up to 3 attempts)
- Email notification if export fails after retries
- Exports queued during peak load, processed within 5 minutes
```

---

## Success Metrics Examples

### Example 1: Feature Adoption

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Export adoption rate | 0% | 60% of account managers use within 30 days | Analytics: export button clicks / AM logins |
| Time spent on QBR prep | 4-6 hours | <1 hour | Survey: "How long did QBR prep take?" |
| Report accuracy | 85% | 99% | QA audit of exported reports |
| NPS (account managers) | 42 | 55 | Quarterly NPS survey |

### Example 2: Performance Improvement

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Dashboard load time (p95) | 8.2s | <3s | APM: page load duration |
| Dashboard bounce rate | 23% | <5% | Analytics: sessions with <10s duration |
| Support tickets (slow dashboard) | 45/month | <10/month | Zendesk tag: "dashboard-performance" |
| Enterprise NPS | 32 | 45 | Segment-filtered NPS survey |

---

## Risk Table Example

| Risk | Likelihood | Impact | Mitigation | Owner | Status |
|------|------------|--------|------------|-------|--------|
| PDF generation overloads servers during peak hours | Medium | High | Implement queue with rate limiting; scale PDF service independently | @eng-lead | Mitigated |
| Large accounts (>1M events) timeout during export | High | Medium | Implement chunked processing; show progress bar; email when complete | @eng-lead | In Progress |
| Exported data contains PII not approved for export | Low | High | Audit all fields; implement field-level export permissions; legal review | @security-lead | Pending Review |
| Users expect real-time data but export is cached | Medium | Low | Clear messaging: "Data as of {timestamp}"; option to refresh before export | @product | Mitigated |

---

## Timeline Example

### Gantt-Style Timeline

```
Week 1-2:  [====] Design
           [==] Technical Design
Week 3-5:  [======] Core Development
Week 4:        [==] PDF Service
Week 5-6:      [====] Frontend
Week 6:            [==] Integration
Week 7:                [===] QA
Week 8:                    [=] Beta
Week 9:                      [=] Release
```

### Milestone Table

| Milestone | Date | Owner | Deliverable | Dependencies |
|-----------|------|-------|-------------|--------------|
| Design Complete | Jan 15 | @designer | Final mockups in Figma | Stakeholder approval |
| Technical Design | Jan 20 | @tech-lead | Architecture doc, API contracts | Design complete |
| Core Development | Feb 7 | @eng-team | Export service functional | Technical design |
| QA Complete | Feb 21 | @qa-lead | All test cases pass | Development complete |
| Beta Release | Feb 28 | @product | 10% rollout to enterprise | QA sign-off |
| GA Release | Mar 7 | @product | 100% rollout | Beta success metrics |

---

## Out of Scope Example

```markdown
## Out of Scope

The following are explicitly excluded from this release:

| Item | Reason | Future Plan |
|------|--------|-------------|
| Excel (.xlsx) export format | Limited demand; PDF covers 90% of use cases | Evaluate for Phase 2 based on feedback |
| Custom date range selection | Complexity; fixed ranges cover primary use cases | Phase 2 if >20% request via feedback |
| White-label PDF branding | Enterprise-only feature; requires separate pricing | Enterprise tier Phase 2 |
| Real-time data export | Technical complexity; 15-minute cache acceptable | Evaluate infrastructure in Q3 |
| Mobile export | <5% of dashboard usage is mobile | Not planned |

**Note:** Requests for out-of-scope items should be logged in [feedback tracker]
for Phase 2 prioritization.
```

