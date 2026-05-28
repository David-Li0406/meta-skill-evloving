# Workflow: Create PRD from Feature Request

**Input**: Feature description or request from user

## Process

### 1. Analyze Request

- Extract feature name, scope, goals
- Identify related systems and components
- Determine priority and complexity

### 2. Structure PRD

- Use template: `../templates/prd-template.md`
- Follow MP architecture patterns
- Include frontmatter with proper metadata
- Organize into standard PRD sections

### 3. Add Implementation Context

- Break into phased approach
- Identify architectural layers involved
- Note dependencies and risks
- Define success criteria and acceptance tests

### 4. Determine Location

- Category: `docs/project_plans/PRDs/[category]/`
- Categories: `harden-polish`, `features`, `enhancements`, `refactors`
- Naming: `[feature-name]-v1.md` (kebab-case)

### 5. Generate File

- Write PRD to determined location
- Include YAML frontmatter with metadata
- Link to related docs (ADRs, guides, etc.)
- Add to project tracking if needed

## Output

- PRD file at: `docs/project_plans/PRDs/[category]/[feature-name]-v1.md`
- Follows template structure
- Ready for implementation planning

## Example

**Input**:
```
"Add real-time collaboration features to prompt editing"
```

**Output Location**: `docs/project_plans/PRDs/features/realtime-collaboration-v1.md`

**Generated Sections**:
1. Executive Summary - Real-time collaborative editing
2. Context & Background - Current single-user editing limitations
3. Problem Statement - Users can't collaborate on prompts
4. Goals & Success Metrics - Multiple concurrent editors, conflict resolution
5. Requirements - WebSocket connections, operational transforms, presence indicators
6. Implementation Phases - Phase 1: Backend infrastructure, Phase 2: Frontend integration

[Return to Planning Skill](../SKILL.md)
