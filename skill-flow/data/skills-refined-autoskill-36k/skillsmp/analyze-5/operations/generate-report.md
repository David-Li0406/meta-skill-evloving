# Generate Analysis Report

Template and guidelines for creating `analysis-report.md`.

## Overview

After completing all analysis steps, generate a comprehensive `analysis-report.md` file in the project root.

---

## Report Template

```markdown
# Initial Analysis Report

**Date:** [Current Date - YYYY-MM-DD]
**Directory:** [Full path from pwd]
**Analyst:** Claude Code (Reverse Engineering Toolkit v1.0.0)

---

## Executive Summary

[2-3 paragraph summary of the application, its purpose, current state, and overall completeness]

Example:
> This is a full-stack Next.js application for managing aquarium fish care ("fishfan"). The backend is fully implemented with 17 AWS Lambda functions, PostgreSQL database, and complete authentication. The frontend is ~60% complete with core functionality implemented but several pages still in placeholder state. Overall project completion is estimated at ~66%.

---

## Application Metadata

- **Name:** [Application Name from package.json or directory]
- **Version:** [Version from manifest]
- **Description:** [From manifest or README]
- **Repository:** [Git remote URL or "Not configured"]
- **License:** [From LICENSE file or package.json]
- **Primary Language:** [Language] [Version if available]

---

## StackShift Configuration

- **Route:** [Greenfield / Brownfield]
- **Implementation Framework:** [GitHub Spec Kit / BMAD Method]
- **Transmission:** [Manual / Cruise Control]
- **Brownfield Mode:** [Standard / Upgrade] _(if Brownfield)_
- **Spec Output Location:** [Current repo / Separate location] _(if Greenfield)_

**What this means:**
- [Brief explanation based on selections]

Example (Spec Kit):
> Using GitHub Spec Kit for brownfield maintenance. Specs will be created in `.specify/` and implementation will use `/speckit.implement` commands.

Example (BMAD):
> Using BMAD Method for enterprise-scale development. Documentation will be created in `docs/` and handed off to BMAD's `*workflow-init` for agent-driven implementation.

---

## Technology Stack

### Primary Language
- [Language] [Version]
  - [Key notes about language usage]

### Frontend Framework
- [Framework] [Version]
  - [Key dependencies and notes]

### Backend Framework
- [Framework] [Version]
  - [Key dependencies and notes]

### Database
- [Database Type] [Version/Service]
  - ORM: [ORM if applicable]
  - Migration System: [Yes/No with details]

### Infrastructure & Deployment
- **Cloud Provider:** [AWS/GCP/Azure/Other]
- **IaC Tool:** [Terraform/CloudFormation/CDK/None]
- **CI/CD:** [GitHub Actions/GitLab CI/CircleCI/None]
- **Hosting:** [Vercel/Netlify/AWS Lambda/EC2/etc.]

### Key Dependencies

| Category | Library | Version | Purpose |
|----------|---------|---------|---------|
| Auth | [Library] | [Version] | [Purpose] |
| API | [Library] | [Version] | [Purpose] |
| UI | [Library] | [Version] | [Purpose] |
| Testing | [Library] | [Version] | [Purpose] |
| Build | [Library] | [Version] | [Purpose] |

---

## Architecture Overview

### Application Type
[Full-Stack Monolith / Microservices / JAMstack / Serverless / etc.]

### Directory Structure

```
[Project Root]/
├── [key-directory-1]/         # [Purpose]
│   ├── [subdirectory]/        # [Purpose]
│   └── ...
├── [key-directory-2]/         # [Purpose]
├── [configuration-files]      # [Purpose]
└── [other-key-files]
```

### Key Components

#### Backend
- **Status:** [Exists / Not Found]
- **Location:** [Directory path]
- **Type:** [REST API / GraphQL / tRPC / Mixed]
- **Endpoints:** [Count] endpoints identified
- **Database Models:** [Count] models
- **Authentication:** [Method - JWT/Session/OAuth/None]
- **Key Features:**
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]

#### Frontend
- **Status:** [Exists / Not Found]
- **Location:** [Directory path]
- **Type:** [SPA / SSR / SSG / Hybrid]
- **Pages:** [Count] pages identified
- **Components:** [Count] reusable components
- **Styling:** [Tailwind/CSS Modules/Styled Components/etc.]
- **State Management:** [Redux/Context/Zustand/None]
- **Key Features:**
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]

#### Database
- **Type:** [PostgreSQL/MySQL/MongoDB/etc.]
- **ORM:** [Prisma/TypeORM/Sequelize/etc.]
- **Schema Location:** [Path to schema files]
- **Models:** [Count] models defined
- **Migrations:** [Count] migrations
- **Seeding:** [Configured / Not Configured]

#### API Architecture
- **Type:** [RESTful / GraphQL / tRPC / Mixed]
- **Endpoints:** [Count] total endpoints
- **Documentation:** [OpenAPI Spec / Inline Comments / None]
- **Versioning:** [v1/v2/etc. or None]
- **Rate Limiting:** [Configured / Not Configured]

#### Infrastructure
- **IaC Tool:** [Terraform/CloudFormation/etc.]
- **Services Used:**
  - [Service 1]: [Purpose]
  - [Service 2]: [Purpose]
  - [Service 3]: [Purpose]
- **Configuration:** [Location of IaC files]
- **Environments:** [dev/staging/prod or single]

---

## Existing Documentation

### README.md
- **Status:** [Yes / No]
- **Quality:** [Good / Basic / Poor]
- **Sections:**
  - [✓] Description
  - [✓] Installation
  - [✗] API Documentation
  - [✓] Development Setup
  - [✗] Testing Guide
  - [✓] Deployment
- **Last Updated:** [Date from git log]
- **Notes:** [Any observations]

### API Documentation
- **Status:** [Yes / Partial / No]
- **Format:** [OpenAPI/Postman/Inline/None]
- **Coverage:** [Percentage or count]
- **Location:** [Path or URL]
- **Notes:** [Any observations]

### Architecture Documentation
- **Status:** [Yes / Partial / No]
- **Files:** [List of architecture docs]
- **Diagrams:** [Yes/No - list types]
- **Notes:** [Any observations]

### Setup/Deployment Documentation
- **Status:** [Yes / Partial / No]
- **Files:** [List files]
- **Coverage:** [What's documented]
- **Notes:** [Any observations]

### Developer Documentation
- **Status:** [Yes / Partial / No]
- **Files:** [CONTRIBUTING.md, etc.]
- **Coverage:** [What's documented]
- **Notes:** [Any observations]

### Testing Documentation
- **Status:** [Yes / Partial / No]
- **Files:** [Test guide files]
- **Coverage:** [What's documented]
- **Notes:** [Any observations]

### Database Documentation
- **Status:** [Yes / Partial / No]
- **Type:** [ER Diagram / Schema Comments / None]
- **Coverage:** [What's documented]
- **Notes:** [Any observations]

### Documentation Tools
- **Configured:** [List tools like TypeDoc, JSDoc, Sphinx, etc.]
- **Output Location:** [Where docs are generated]
- **Notes:** [Any observations]

---

## Completeness Assessment

### Overall Completion: ~[X]%

### Component Breakdown

| Component | Completion | Evidence |
|-----------|------------|----------|
| Backend | ~[X]% | [Brief evidence] |
| Frontend | ~[X]% | [Brief evidence] |
| Database | ~[X]% | [Brief evidence] |
| Tests | ~[X]% | [Brief evidence] |
| Documentation | ~[X]% | [Brief evidence] |
| Infrastructure | ~[X]% | [Brief evidence] |

### Detailed Evidence

#### Backend (~[X]%)
[Detailed evidence with specific examples, file counts, etc.]

Example:
- 17 Lambda functions fully implemented and tested
- All API endpoints functional with proper error handling
- Authentication/authorization complete with JWT
- Database queries optimized
- No placeholder or TODO comments in backend code

#### Frontend (~[X]%)
[Detailed evidence]

Example:
- 8 of 12 planned pages implemented
- Core pages complete: Login, Dashboard, Fish List, Fish Detail
- Placeholder pages: Analytics (TODO), Settings (stub), Admin (not started), Reports (skeleton)
- Components: 23 reusable components, all functional
- Styling: ~80% complete, missing dark mode and mobile polish

#### Tests (~[X]%)
[Detailed evidence]

#### Documentation (~[X]%)
[Detailed evidence]

#### Infrastructure (~[X]%)
[Detailed evidence]

### Placeholder Files & TODOs

**Files with Placeholder Content:**
- [File path]: [Description]
- [File path]: [Description]

**TODO/FIXME Comments:**
- Found [N] TODO comments across codebase
- Top categories:
  1. [Category]: [Count]
  2. [Category]: [Count]
  3. [Category]: [Count]

**Sample TODOs:**
```
[File:Line] - TODO: [Comment]
[File:Line] - FIXME: [Comment]
[File:Line] - TODO: [Comment]
```

### Missing Components

**Not Started:**
- [Component/Feature]: [Description]
- [Component/Feature]: [Description]

**Partially Implemented:**
- [Component/Feature]: [What exists vs what's missing]
- [Component/Feature]: [What exists vs what's missing]

**Needs Improvement:**
- [Component/Feature]: [Current state and what needs work]
- [Component/Feature]: [Current state and what needs work]

---

## Source Code Statistics

- **Total Source Files:** [Count]
- **Lines of Code:** ~[Estimate from cloc or wc]
- **Test Files:** [Count]
- **Test Coverage:** [Percentage if available or "Not measured"]
- **Configuration Files:** [Count]

### File Type Breakdown

| Type | Count | Purpose |
|------|-------|---------|
| TypeScript/JavaScript | [Count] | [Application code/Components/etc.] |
| Tests | [Count] | [Unit/Integration/E2E] |
| Styles | [Count] | [CSS/SCSS/etc.] |
| Configuration | [Count] | [Build/Deploy/Environment] |
| Documentation | [Count] | [Markdown files] |

---

## Technical Debt & Issues

### Identified Issues
1. [Issue 1]: [Description and impact]
2. [Issue 2]: [Description and impact]
3. [Issue 3]: [Description and impact]

### Security Concerns
- [Concern 1]: [Description]
- [Concern 2]: [Description]

### Performance Concerns
- [Concern 1]: [Description]
- [Concern 2]: [Description]

### Code Quality
- Linting: [Configured / Not Configured]
- Type Checking: [Strict / Loose / None]
- Code Formatting: [Prettier/ESLint/None]
- Pre-commit Hooks: [Configured / Not Configured]

---

## Recommended Next Steps

Based on this analysis, the reverse engineering process should focus on:

### Immediate Priorities
1. **[Priority 1]**
   - Why: [Reasoning]
   - Impact: [Expected outcome]

2. **[Priority 2]**
   - Why: [Reasoning]
   - Impact: [Expected outcome]

3. **[Priority 3]**
   - Why: [Reasoning]
   - Impact: [Expected outcome]

### Reverse Engineering Focus Areas

For **Step 2 (Reverse Engineer)**:
- Prioritize extracting documentation for: [List components]
- Pay special attention to: [Areas of concern]
- Can likely skip: [Well-documented areas]

### Estimated Reverse Engineering Effort
- **Step 2 (Reverse Engineer):** ~[X] minutes (based on codebase size)
- **Step 3 (Create Specifications):** ~[X] minutes
- **Step 4 (Gap Analysis):** ~[X] minutes
- **Step 5 (Complete Specification):** ~[X] minutes (interactive)
- **Step 6 (Implement from Spec):** ~[X] hours/days (depends on gaps)

---

## Notes & Observations

[Any additional observations, concerns, or context that doesn't fit above categories]

Examples:
- Monorepo structure detected but not using workspace tools
- Multiple authentication methods suggest migration in progress
- Infrastructure code is more mature than application code
- Build process is complex and could be simplified
- Dependencies are up-to-date (as of [date])

---

## Appendices

### A. Dependency Tree (Top-Level)

```
[Main dependencies with versions]
```

### B. Configuration Files Inventory

```
[List of all configuration files with brief descriptions]
```

### C. Database Schema Summary

```
[List of models/tables with key relationships]
```

---

**Report Generated:** [Timestamp]
**Toolkit Version:** 1.0.0
**Ready for Step 2:** ✅
```

---

## Filling Out the Template

### Executive Summary Guidelines

Write a 2-3 paragraph summary answering:
1. What is this application? (Purpose, domain, users)
2. What's the tech stack? (Key technologies)
3. What's the current state? (Completion %, what's done, what's missing)
4. What's next? (Main recommendation)

### Evidence Requirements

For every percentage estimate, provide concrete evidence:
- File counts
- Feature lists
- Specific examples
- Code samples (for TODOs)
- Dates (for documentation)

### Prioritization Logic

Recommend next steps based on:
1. **Critical gaps** - Security, data integrity, deployment blockers
2. **High-value gaps** - User-facing features, core functionality
3. **Quality gaps** - Tests, documentation, error handling
4. **Nice-to-haves** - Polish, optimizations, extras

---

## Report Validation Checklist

Before finalizing the report, verify:

- [ ] All sections filled out (no [TODO] markers left)
- [ ] Percentages are evidence-based, not guesses
- [ ] File paths are accurate and up-to-date
- [ ] Tech stack versions are correct
- [ ] Missing components are clearly identified
- [ ] Recommendations are actionable
- [ ] Executive summary is clear and concise
- [ ] Report is saved to project root as `analysis-report.md`

---

## Sample Output Location

The report should be saved to:
```
/path/to/project-root/analysis-report.md
```

This ensures it's:
- Easy to find
- Version controlled (add to git)
- Referenced by subsequent steps

---

## Next Steps After Report

Once the report is generated and reviewed:

1. **Review with user** - Present key findings
2. **Confirm accuracy** - Ask if the analysis matches their understanding
3. **Adjust estimates** - Update based on user feedback
4. **Proceed to Step 2** - Use the reverse-engineer skill to generate comprehensive documentation

The analysis report serves as the foundation for the entire reverse engineering process.
