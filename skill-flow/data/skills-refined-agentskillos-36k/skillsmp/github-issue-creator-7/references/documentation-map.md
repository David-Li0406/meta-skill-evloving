# ROLESENSE.ai Documentation Map

## Core Product Documents

| Document | Path | Purpose | When to Read |
|----------|------|---------|--------------|
| **PRD** | `docs/PRD.md` | Product requirements, user stories, business goals | Understanding product context |
| **FRD** | `docs/FRD.md` | Detailed functional requirements with acceptance criteria | Writing FR issues, defining scope |
| **Architecture** | `docs/architecture.md` | System design, microservices, data flow | Technical implementation issues |
| **UI/UX Design Spec** | `docs/UI-UX-Design-Spec.md` | Design tokens, components, layouts, flows | Frontend issues, UI components |
| **Technology Stack** | `docs/Technology-Stack.md` | Tech choices, frameworks, libraries | Technical decisions |

## Sprint Planning Documents

| Document | Path | Purpose |
|----------|------|---------|
| **Master Sprint Plan** | `docs/project_sprint_plan.md` | 6-sprint roadmap overview |
| **Sprint Plan** | `docs/sprint-{N}/sprint-plan.md` | Sprint goals, deliverables, success criteria |
| **Backlog** | `docs/sprint-{N}/backlog.md` | Detailed tasks with estimates |
| **Issue Description** | `docs/sprint-{N}/issue-description.md` | Sprint summary for GitHub |

## Epic Documents

| Epic ID | Path | Domain |
|---------|------|--------|
| `EPIC-SYS-01` | `docs/epics/EPIC-SYS-01.md` | System & Authentication |
| `EPIC-IAM-01` | `docs/epics/EPIC-IAM-01.md` | Identity & Access Management |
| `EPIC-ING-01` | `docs/epics/EPIC-ING-01.md` | Resume Ingestion & Parsing |
| `EPIC-JOB-01` | `docs/epics/EPIC-JOB-01.md` | Job Description Management |
| `EPIC-TLR-01` | `docs/epics/EPIC-TLR-01.md` | Resume Tailoring |
| `EPIC-EXP-01` | `docs/epics/EPIC-EXP-01.md` | Export & Output |
| `EPIC-CMP-01` | `docs/epics/EPIC-CMP-01.md` | Compliance & Privacy |
| `EPIC-ACC-01` | `docs/epics/EPIC-ACC-01.md` | Accessibility |

## Workflow Documents

| Workflow ID | Path | Description |
|-------------|------|-------------|
| `WF-00-001` | `docs/workflows/WF-00-001-user-auth.md` | User authentication flow |
| `WF-00-002` | `docs/workflows/WF-00-002-rate-limiting.md` | Rate limiting |
| `WF-00-003` | `docs/workflows/WF-00-003-email-notifications.md` | Email notifications |
| `WF-00-004` | `docs/workflows/WF-00-004-fusionauth-login.md` | FusionAuth OIDC login |
| `WF-01-001` | `docs/workflows/WF-01-001-resume-upload-parsing.md` | Resume upload & parsing |
| `WF-01-002` | `docs/workflows/WF-01-002-linkedin-import.md` | LinkedIn import |
| `WF-01-003` | `docs/workflows/WF-01-003-master-resume-verification.md` | Resume verification |
| `WF-01-004` | `docs/workflows/WF-01-004-resume-version-history.md` | Version history |
| `WF-02-001` | `docs/workflows/WF-02-001-job-ingestion-analysis.md` | Job ingestion |
| `WF-02-002` | `docs/workflows/WF-02-002-job-dashboard.md` | Job dashboard |
| `WF-03-001` | `docs/workflows/WF-03-001-match-scoring.md` | Match scoring |
| `WF-03-002` | `docs/workflows/WF-03-002-content-tailoring.md` | Content tailoring |
| `WF-03-003` | `docs/workflows/WF-03-003-user-verification.md` | Human-in-the-loop |
| `WF-03-004` | `docs/workflows/WF-03-004-manual-mode-tailoring.md` | Manual fallback |
| `WF-04-001` | `docs/workflows/WF-04-001-pdf-export.md` | PDF export |
| `WF-04-002` | `docs/workflows/WF-04-002-application-history.md` | Application tracking |
| `WF-05-001` | `docs/workflows/WF-05-001-consent-management.md` | Consent management |
| `WF-05-002` | `docs/workflows/WF-05-002-audit-logging.md` | Audit logging |
| `WF-05-003` | `docs/workflows/WF-05-003-data-subject-rights.md` | GDPR rights |
| `WF-06-001` | `docs/workflows/WF-06-001-accessibility-audit.md` | WCAG audit |

## Sprint-Specific Documents

### Sprint 1 (Auth + Shell) ✅ Completed

| Document | Path |
|----------|------|
| Epic | `docs/sprint-1/EPIC-Sprint-1.md` |
| Implementation Plan | `docs/sprint-1/Implementation-Plan.md` |
| FR-SYS-001 | `docs/sprint-1/FR-SYS-001-User-Authentication.md` |
| FR-SYS-002 | `docs/sprint-1/FR-SYS-002-Session-Management.md` |
| FR-SYS-003 | `docs/sprint-1/FR-SYS-003-Rate-Limiting.md` |
| FR-SYS-004 | `docs/sprint-1/FR-SYS-004-Nuxt-App-Shell.md` |
| FR-SYS-005 | `docs/sprint-1/FR-SYS-005-CICD-Observability.md` |

### Sprint 1.5 (FusionAuth Refactor) 🚀 Active

| Document | Path |
|----------|------|
| Epic | `docs/sprint-1.5/EPIC-Sprint-1.5.md` |
| Sprint Plan | `docs/sprint-1.5/sprint-plan.md` |
| Backlog | `docs/sprint-1.5/backlog.md` |
| FR-IAM-001 | `docs/sprint-1.5/FR-IAM-001-FusionAuth-Integration.md` |

### Sprint 2 (Resume Ingestion v1) 📅 Planned

| Document | Path |
|----------|------|
| Sprint Plan | `docs/sprint-2/sprint-plan.md` |
| Backlog | `docs/sprint-2/backlog.md` |
| Issue Description | `docs/sprint-2/issue-description.md` |
| FR-ING-001 | `docs/sprint-2/FR-ING-001-Multi-Format-Resume-Upload.md` |
| GitHub Issues | `docs/sprint-2/github-issues/` |

### Sprint 3-6 (Planned)

| Sprint | Path |
|--------|------|
| Sprint 3 | `docs/sprint-3/sprint-plan.md`, `docs/sprint-3/backlog.md` |
| Sprint 4 | `docs/sprint-4/sprint-plan.md`, `docs/sprint-4/backlog.md` |
| Sprint 5 | `docs/sprint-5/sprint-plan.md`, `docs/sprint-5/backlog.md` |
| Sprint 6 | `docs/sprint-6/sprint-plan.md`, `docs/sprint-6/backlog.md` |

## UI/UX Design Spec Sections

| Section | Description | When to Reference |
|---------|-------------|-------------------|
| **4A.1** | Main App Dashboard | Dashboard components |
| **4A.2** | Resume Manager | Resume list/table UI |
| **4A.3** | Resume Creation Modal | Upload modal |
| **4A.4** | New Scan Interface | Scan page, drop zone |
| **4A.5** | Scan Results Dashboard | Results display |
| **4A.6** | Resume Score Report | Score/feedback UI |
| **4A.7** | Job Tracker Kanban | Job tracking board |
| **5.1** | Design Tokens | Colors, typography, spacing |
| **5.2** | Interaction Patterns | Animations, states |
| **6.1** | Conversion Flows | User journeys |

## Document Reading Strategy

### For Sprint Epic Issues

```
1. docs/project_sprint_plan.md          # Roadmap context
2. docs/sprint-{N}/sprint-plan.md       # Sprint goals
3. docs/sprint-{N}/issue-description.md # Summary
4. docs/epics/EPIC-*.md                 # Epic details
```

### For Feature/FR Issues

```
1. docs/sprint-{N}/FR-*-*.md            # FR specification
2. docs/sprint-{N}/backlog.md           # Task breakdown
3. docs/workflows/WF-*.md               # Related workflow
4. docs/UI-UX-Design-Spec.md            # UI requirements (if frontend)
5. docs/FRD.md                          # Cross-reference
```

### For Technical/Bug Issues

```
1. docs/architecture.md                 # System context
2. docs/Technology-Stack.md             # Tech details
3. Relevant sprint/FR documentation
```
