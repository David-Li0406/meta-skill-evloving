# Role Routing Guide

Roles are defined in `conductor.json`. Route tasks to the appropriate role based on task characteristics.

**Config location** (project-local takes precedence):
1. `./.conductor-kit/conductor.json`
2. `~/.conductor-kit/conductor.json`

## Role Matrix

| Role | Use For | Strengths |
|------|---------|-----------|
| `sage` | Deep analysis, architecture, security, algorithms | Extended thinking, trade-off analysis |
| `scout` | Web search, API reference, best practices research | Fast retrieval, broad knowledge |
| `pathfinder` | Codebase navigation, file discovery, pattern finding | Quick scanning, parallel search |
| `pixelator` | Web UI/UX, React/Vue/CSS, responsive design | Visual reasoning, frontend patterns |
| `author` | README, docs, comments, changelogs | Clear writing, formatting |
| `vision` | Screenshot analysis, image review, visual debugging | Image understanding |

**Note:** The `cli` and `model` for each role are configured in `conductor.json`, not hardcoded here.

## Task -> Role Mapping

### Use `sage` when:
- Architecture decisions with trade-offs
- Root cause analysis for complex bugs
- Security vulnerability assessment
- Algorithm design / complexity analysis
- Refactoring strategy for legacy code
- Migration planning with risk assessment
- Any task requiring step-by-step reasoning

### Use `scout` when:
- Looking up framework/library docs
- Finding best practices or patterns
- Researching external dependencies
- Checking API specifications

### Use `pathfinder` when:
- Initial codebase discovery
- Finding relevant files for a task
- Understanding project structure
- Locating similar implementations

### Use `pixelator` when:
- Web UI component design (React/Vue/Svelte)
- CSS/Tailwind styling decisions
- Responsive layout and accessibility
- Frontend architecture (not mobile/desktop native)

### Use `author` when:
- Writing/updating documentation
- Generating changelogs
- Creating code comments
- README improvements

### Use `vision` when:
- Analyzing screenshots or mockups
- Visual regression review
- Image-based debugging
- UI comparison tasks

## Combining Roles

For complex tasks, combine roles in sequence:

1. **Discovery phase**: `pathfinder` -> find relevant files
2. **Analysis phase**: `sage` -> deep reasoning on findings
3. **Review phase**: `scout` -> verify against docs/best practices

Example (security audit):
```
pathfinder -> find auth-related files
sage -> analyze vulnerabilities + propose fixes
scout -> verify against OWASP guidelines
```
