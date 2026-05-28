# Methodologies Folder

## Overview

Contains 45 HR and recruiting methodologies organized into talent acquisition, employer branding, interviewing, onboarding, retention, and compliance. Each methodology follows a consistent structure: Metadata, Problem, Framework, Templates, Examples, Implementation Checklist, Common Mistakes, Metrics, and Related Methodologies.

## Structure

```
methodologies/
├── CLAUDE.md                    # This file
├── *.md                         # Core methodologies (4 files)
├── talent-acquisition/          # Recruiting methodologies (12 files)
├── interviewing/                # Interview & selection (10 files)
├── onboarding/                  # Onboarding processes (8 files)
├── retention/                   # Retention strategies (4 files)
└── compliance/                  # HR compliance (3 files)
```

## Subfolders

| Folder | Description | Files |
|--------|-------------|-------|
| [talent-acquisition/](talent-acquisition/) | Recruiting funnel, sourcing, ATS, AI tools, job descriptions | 12 |
| [interviewing/](interviewing/) | STAR method, structured interviews, scorecards, assessments | 10 |
| [onboarding/](onboarding/) | 30-60-90 plans, preboarding, buddy programs, orientation | 8 |
| [retention/](retention/) | Stay interviews, exit analysis, retention strategies | 4 |
| [compliance/](compliance/) | Hiring compliance, DEI practices, process audit | 3 |

## Root Level Files (Employer Branding)

| File | ID | Description |
|------|----|-------------|
| employee-value-proposition.md | employee-value-proposition | Define and communicate EVP |
| employer-brand-audit.md | employer-brand-audit | Assess current employer brand |
| careers-page-optimization.md | careers-page-optimization | High-converting careers page |
| glassdoor-management.md | glassdoor-management | Review monitoring and response |
| employee-testimonials.md | employee-testimonials | Authentic employer brand content |
| employer-brand-content-calendar.md | employer-brand-content-calendar | Consistent content publishing |
| dei-employer-branding.md | dei-employer-branding | Attract diverse candidates |
| talent-community-building.md | talent-community-building | Nurture future candidates |

## Talent Acquisition Methodologies

| File | ID | Description |
|------|----|-------------|
| recruitment-funnel-optimization.md | recruitment-funnel-optimization | Optimize funnel conversion |
| multi-channel-sourcing.md | multi-channel-sourcing | Diversify sourcing channels |
| skills-based-hiring.md | skills-based-hiring | Focus on skills over degrees |
| job-description-writing.md | job-description-writing | Compelling job descriptions |
| candidate-persona-development.md | candidate-persona-development | Target candidate profiles |
| passive-candidate-outreach.md | passive-candidate-outreach | Engage passive candidates |
| internal-mobility-program.md | internal-mobility-program | Internal career opportunities |
| talent-pipeline-building.md | talent-pipeline-building | Proactive talent sourcing |
| recruitment-metrics-dashboard.md | recruitment-metrics-dashboard | Track recruiting KPIs |
| ats-optimization.md | ats-optimization | Applicant tracking optimization |
| ai-recruiting-tools.md | ai-recruiting-tools | AI for sourcing and screening |
| recruitment-marketing.md | recruitment-marketing | Promote employer brand |

## Interviewing Methodologies

| File | ID | Description |
|------|----|-------------|
| structured-interview-design.md | structured-interview-design | Consistent interview process |
| star-interview-method.md | star-interview-method | Behavioral interviewing |
| behavioral-interview-questions.md | behavioral-interview-questions | Question bank by competency |
| interview-scorecard.md | interview-scorecard | Objective evaluation |
| technical-assessment-design.md | technical-assessment-design | Skills verification |
| culture-fit-assessment.md | culture-fit-assessment | Values alignment |
| reference-check-framework.md | reference-check-framework | Effective reference checks |
| interviewer-training.md | interviewer-training | Train interview team |
| hiring-committee-debrief.md | hiring-committee-debrief | Evidence-based decisions |
| offer-management.md | offer-management | Close candidates |

## Onboarding Methodologies

| File | ID | Description |
|------|----|-------------|
| 30-60-90-day-plan.md | 30-60-90-day-plan | Structured new hire ramp |
| preboarding-process.md | preboarding-process | Pre-start engagement |
| day-one-orientation.md | day-one-orientation | Great first day |
| buddy-program.md | buddy-program | Peer support system |
| onboarding-checklist.md | onboarding-checklist | Nothing falls through cracks |
| manager-onboarding-guide.md | manager-onboarding-guide | Manager responsibilities |
| onboarding-feedback-loop.md | onboarding-feedback-loop | Continuous improvement |
| remote-onboarding.md | remote-onboarding | Virtual onboarding |

## Retention Methodologies

| File | ID | Description |
|------|----|-------------|
| employee-retention-strategies.md | employee-retention-strategies | Reduce turnover |
| stay-interview-framework.md | stay-interview-framework | Proactive retention |
| exit-interview-analysis.md | exit-interview-analysis | Learn from departures |
| talent-review-process.md | talent-review-process | Talent visibility |

## Compliance Methodologies

| File | ID | Description |
|------|----|-------------|
| hiring-compliance-checklist.md | hiring-compliance-checklist | Legal requirements |
| dei-hiring-practices.md | dei-hiring-practices | Inclusive hiring |
| recruitment-process-audit.md | recruitment-process-audit | Process improvement |

## Methodology Structure

Each methodology file follows this structure:

```markdown
# methodology-name

## Metadata
| Field | Value |
|-------|-------|
| ID | methodology-name |
| Name | Methodology Name |
| Category | Category |
| Difficulty | Beginner/Intermediate/Advanced |
| Agent | faion-*-agent |
| Related | methodology-1, methodology-2 |

## Problem
[What problem this solves]

## Framework
[Step-by-step approach]

## Templates
[Ready-to-use templates]

## Examples
[Real-world examples]

## Implementation Checklist
[Action items]

## Common Mistakes
[What to avoid]

## Metrics
[How to measure success]

## Related Methodologies
[Links to related methodology files]
```

## Agent Assignments

| Agent | Methodologies |
|-------|---------------|
| faion-recruiter-agent | talent-acquisition/*, interviewing/*, retention/*, compliance/* |
| faion-employer-brand-agent | employee-value-proposition, employer-brand-*, careers-page-*, testimonials |
| faion-onboarding-agent | onboarding/* |

## ID Conventions

| Category | Pattern | Examples |
|----------|---------|----------|
| Talent Acquisition | recruitment-*, sourcing-*, job-* | recruitment-funnel-optimization |
| Employer Branding | employer-*, evp-*, careers-* | employee-value-proposition |
| Interviewing | interview-*, star-*, assessment-* | star-interview-method |
| Onboarding | onboarding-*, *-day-plan | 30-60-90-day-plan |
| Retention | retention-*, *-interview | stay-interview-framework |
| Compliance | compliance-*, dei-* | hiring-compliance-checklist |

---

*45 Methodologies | 6 Categories | 3 Agents*
*Based on: SHRM BASK, AIHR, Gartner HR Research*
