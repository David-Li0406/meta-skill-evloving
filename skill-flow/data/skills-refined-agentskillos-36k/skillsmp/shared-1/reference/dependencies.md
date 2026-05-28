# PRISM Dependencies Reference

This document describes the dependencies, integrations, and file structure used by PRISM skills.

## Dependency Structure

PRISM uses a modular dependency system where each skill can reference:

1. **Tasks** - Executable workflows (`.prism/tasks/`)
2. **Templates** - Document structures (`.prism/templates/`)
3. **Checklists** - Quality gates (`.prism/checklists/`)
4. **Data** - Reference information (`.prism/data/`)
5. **Integrations** - External systems (Jira, etc.)

## File Resolution

Dependencies follow this pattern:
```
.prism/{type}/{name}
```

**Examples:**
- `create-doc.md` → `.prism/tasks/create-doc.md`
- `architect-checklist.md` → `.prism/checklists/architect-checklist.md`
- `architecture-tmpl.yaml` → `.prism/templates/architecture-tmpl.yaml`
- `technical-preferences.md` → `.prism/data/technical-preferences.md`

## Architect Dependencies

### Tasks
- `create-deep-research-prompt.md` - Deep technical research
- `create-doc.md` - Document generation engine
- `document-project.md` - Project documentation workflow
- `execute-checklist.md` - Checklist validation

### Templates
- `architecture-tmpl.yaml` - Backend architecture template
- `brownfield-architecture-tmpl.yaml` - Legacy system assessment template
- `front-end-architecture-tmpl.yaml` - Frontend architecture template
- `fullstack-architecture-tmpl.yaml` - Complete system architecture template

### Checklists
- `architect-checklist.md` - Architecture quality gates

### Data
- `technical-preferences.md` - Team technology preferences and patterns

## Product Owner Dependencies

### Tasks
- `correct-course.md` - Requirement change management
- `execute-checklist.md` - Checklist validation
- `shard-doc.md` - Document sharding workflow
- `validate-next-story.md` - Story validation workflow
- `brownfield-create-story.md` - Brownfield story creation

### Templates
- `story-tmpl.yaml` - User story template

### Checklists
- `change-checklist.md` - Change management checklist
- `po-master-checklist.md` - Product owner master checklist

## Developer Dependencies

### Tasks
- `apply-qa-fixes.md` - QA feedback application workflow
- `execute-checklist.md` - Checklist validation
- `validate-next-story.md` - Story validation (pre-development)

### Checklists
- `story-dod-checklist.md` - Story Definition of Done checklist

### Configuration
**Dev Load Always Files** (from `core-config.yaml`):
- Files automatically loaded during developer activation
- Contains project-specific patterns and standards
- Keeps developer context lean and focused

**Story File Sections** (Developer can update):
- Tasks/Subtasks checkboxes
- Dev Agent Record (all subsections)
- Agent Model Used
- Debug Log References
- Completion Notes List
- File List
- Change Log
- Status (only to "Ready for Review")

## QA/Test Architect Dependencies

### Tasks
- `nfr-assess.md` - Non-functional requirements validation
- `qa-gate.md` - Quality gate decision management
- `review-story.md` - Comprehensive story review
- `risk-profile.md` - Risk assessment workflow
- `test-design.md` - Test strategy design
- `trace-requirements.md` - Requirements traceability mapping

### Templates
- `qa-gate-tmpl.yaml` - Quality gate template
- `story-tmpl.yaml` - Story template (for reading)

### Data
- `technical-preferences.md` - Team preferences
- `test-levels-framework.md` - Unit/Integration/E2E decision framework
- `test-priorities-matrix.md` - P0/P1/P2/P3 priority system

### Output Locations
**Assessment Documents:**
```
docs/qa/assessments/
├── {epic}.{story}-risk-{YYYYMMDD}.md
├── {epic}.{story}-test-design-{YYYYMMDD}.md
├── {epic}.{story}-trace-{YYYYMMDD}.md
└── {epic}.{story}-nfr-{YYYYMMDD}.md
```

**Gate Decisions:**
```
docs/qa/gates/
└── {epic}.{story}-{slug}.yml
```

**Story File Sections** (QA can update):
- QA Results section ONLY
- Cannot modify: Status, Story, Acceptance Criteria, Tasks, Dev Notes, Testing, Dev Agent Record, Change Log

## Scrum Master Dependencies

### Tasks
- `brownfield-create-epic.md` - Epic creation for brownfield projects

## Jira Integration

### Configuration
Jira integration is configured in `.prism/core-config.yaml`:

```yaml
integrations:
  jira:
    enabled: true
    baseUrl: "https://your-company.atlassian.net"
    # Additional config...
```

### Usage Pattern

**1. Fetch Issue Context:**
```
*jira PROJ-123
```

**2. Use in Workflows:**
- Architect: Fetch epic for architecture planning
- PO: Fetch epic/story for refinement
- Dev: Fetch story for implementation context
- QA: Fetch story for test planning

**3. Automatic Linking:**
- Created artifacts reference source Jira key
- Traceability maintained throughout workflow

### Integration Points

**Available in:**
- ✅ Architect skill
- ✅ Product Owner skill
- ✅ Developer skill
- ✅ QA skill
- ✅ Scrum Master skill

**Command:**
```
*jira {issueKey}
```

**Output:**
- Issue summary and description
- Acceptance criteria (if available)
- Comments and discussion
- Current status and assignee
- Labels and components

## PRISM Configuration

### Core Config File

**Location:** `.prism/core-config.yaml`

**Purpose:** Central configuration for all PRISM skills

**Key Sections:**
```yaml
project:
  name: "Your Project"
  type: "brownfield" | "greenfield"

paths:
  stories: "docs/stories"
  architecture: "docs/architecture"
  qa:
    qaLocation: "docs/qa"
    assessments: "docs/qa/assessments"
    gates: "docs/qa/gates"

dev:
  devStoryLocation: "docs/stories"
  devLoadAlwaysFiles:
    - "docs/architecture/technical-standards.md"
    - "docs/architecture/project-conventions.md"

integrations:
  jira:
    enabled: true
    baseUrl: "https://your-company.atlassian.net"
```

### Story File Structure

**Location:** `{devStoryLocation}/{epic}.{story}.{slug}.md`

**Example:** `docs/stories/1.3.user-authentication.md`

**Required Sections:**
- Story ID and Title
- Story (user need and business value)
- Acceptance Criteria
- Tasks/Subtasks with checkboxes
- Dev Notes
- Testing approach
- Dev Agent Record (for developer updates)
- QA Results (for QA updates)
- PSP Estimation Tracking
- File List
- Change Log
- Status

### Template Structure

**Location:** `.prism/templates/{template-name}.yaml`

**Format:**
```yaml
metadata:
  id: template-id
  title: Template Title
  version: 1.0.0

workflow:
  elicit: true | false
  confirm_sections: true | false

sections:
  - id: section-1
    title: Section Title
    prompt: |
      Instructions for generating this section
    elicit:
      - question: "What is...?"
        placeholder: "Example answer"
```

## Workflow Dependencies

### Story Creation Workflow

```
1. PO creates story using story-tmpl.yaml
2. Story validation using validate-next-story.md
3. QA risk assessment using risk-profile.md
4. QA test design using test-design.md
5. Dev implements using develop-story command
6. QA traces coverage using trace-requirements.md
7. QA reviews using review-story.md
8. QA gates using qa-gate.md
```

### Architecture Workflow

```
1. Architect creates doc using create-doc.md + architecture template
2. Validation using execute-checklist.md + architect-checklist.md
3. Sharding using shard-doc.md
4. Stories created from sharded content
```

### Brownfield Workflow

```
1. Architect documents project using document-project.md
2. PM creates brownfield PRD
3. Architect creates brownfield architecture using brownfield-architecture-tmpl.yaml
4. PO creates stories using brownfield-create-story.md
5. QA risk profiles using risk-profile.md (CRITICAL)
6. Development proceeds with enhanced QA validation
```

## Data Files

### Technical Preferences

**Location:** `.prism/data/technical-preferences.md`

**Purpose:** Team-specific technology choices and patterns

**Used By:** All skills to bias recommendations

**Example Content:**
```markdown
# Technical Preferences

## Backend
- Language: Python 3.11+
- Framework: FastAPI
- Database: PostgreSQL 15+
- ORM: SQLAlchemy 2.0

## Frontend
- Framework: React 18+ with TypeScript
- State: Redux Toolkit
- Routing: React Router v6

## Testing
- Unit: pytest
- E2E: Playwright
- Coverage: >80% for new code
```

### Test Frameworks

**test-levels-framework.md:**
- Unit test criteria and scenarios
- Integration test criteria
- E2E test criteria
- Selection guidance

**test-priorities-matrix.md:**
- P0: Critical (>90% unit, >80% integration, all E2E)
- P1: High (happy path + key errors)
- P2: Medium (happy path + basic errors)
- P3: Low (smoke tests)

## Dependency Loading

### Progressive Loading

**Principle:** Load dependencies only when needed, not during activation

**Activation:**
1. Read skill SKILL.md
2. Adopt persona
3. Load core-config.yaml
4. Greet and display help
5. HALT and await commands

**Execution:**
1. User requests command
2. Load required dependencies
3. Execute workflow
4. Return results

### Dev Agent Special Rules

**CRITICAL:**
- Story has ALL info needed
- NEVER load PRD/architecture unless explicitly directed
- Only load devLoadAlwaysFiles during activation
- Keep context minimal and focused

## External Dependencies

### Version Control
- Git required for all PRISM workflows
- Branch strategies defined per project

### Node.js (Optional)
- Optional for CLI tools
- Required for flattener utilities

### IDEs
- Claude Code (recommended)
- VS Code with Claude extension
- Cursor
- Any IDE with Claude support

### AI Models
- Claude 3.5 Sonnet (recommended for all skills)
- Claude 3 Opus (alternative)
- Other models may work but not optimized

## Best Practices

**Dependency Management:**
- ✅ Keep dependencies minimal and focused
- ✅ Load progressively (on-demand)
- ✅ Reference by clear file paths
- ✅ Maintain separation of concerns

**File Organization:**
- ✅ Tasks in `.prism/tasks/`
- ✅ Templates in `.prism/templates/`
- ✅ Checklists in `.prism/checklists/`
- ✅ Data in `.prism/data/`

**Configuration:**
- ✅ Central config in `core-config.yaml`
- ✅ Project-specific settings
- ✅ Integration credentials secure

**Anti-Patterns:**
- ❌ Loading all dependencies during activation
- ❌ Mixing task types in single file
- ❌ Hardcoding paths instead of using config
- ❌ Dev agents loading excessive context

## Troubleshooting

**Dependency Not Found:**
- Check file path matches pattern: `.prism/{type}/{name}`
- Verify file exists in correct directory
- Check core-config.yaml paths configuration

**Integration Failures:**
- Verify Jira configuration in core-config.yaml
- Check credentials and permissions
- Test connection with `*jira {test-key}`

**Task Execution Errors:**
- Ensure all required dependencies loaded
- Check task file format (markdown with YAML frontmatter)
- Verify user has permissions for file operations

---

**Last Updated**: 2025-10-22
