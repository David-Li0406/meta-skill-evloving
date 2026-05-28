# Workflow: Analyze Codebase

**Purpose**: Comprehensive codebase analysis and pattern discovery
**Use for**: Feature planning, architecture decisions, refactoring preparation
**Estimated time**: 30-60 minutes
**Output**: Structured research report

## Overview

This workflow provides a systematic approach to analyzing a codebase before feature implementation or architectural changes. It ensures you understand project conventions, existing patterns, technology stack, and integration points.

## Required Tools

- **Read** - Reading documentation and code files
- **Grep** - Searching for patterns and implementations
- **Glob** - Finding files by pattern
- **Bash** - Directory structure analysis (ls commands)
- **WebSearch** - Technology documentation (optional)

## Analysis Process

### Phase 1: Project Structure Analysis

#### 1.1 Read Project Documentation

Read foundational documentation:

```markdown
Priority order:
1. CLAUDE.md (AI agent guidance)
2. README.md (project overview)
3. CONTRIBUTING.md (development guidelines)
4. /docs/architecture/ (system design docs)
5. /docs/architecture/coding-standards.md (if exists)
6. /docs/architecture/file-system.md (if exists)
```

**Document**:
- Project purpose and goals
- Development setup requirements
- Key architectural decisions
- Coding standards and conventions
- Testing requirements

#### 1.2 Analyze Directory Structure

Map the folder organization:

```bash
# Top-level structure
ls -la <project-root>

# Key source directories
ls -d <project-root>/*/

# Source organization (adjust paths as needed)
ls <src-directory>/
ls <src-directory>/*/
```

**Document**:
- How code is organized (by feature, by layer, by module)
- Key directories and their purposes
- Monorepo structure or workspace configurations
- Test directory organization
- Documentation directory structure

#### 1.3 Check Configuration Files

Read configuration files to understand tooling:

```markdown
Configuration files to check:
- package.json / pyproject.toml (dependencies, scripts)
- tsconfig.json / setup.py (build configuration)
- .eslintrc / .ruff.toml (linting rules)
- pytest.ini / jest.config.js (testing framework)
- .env.example (environment variables)
- docker-compose.yml (infrastructure)
```

**Document**:
- Linting rules and formatting standards
- Testing frameworks and patterns
- Build tools and scripts
- Development dependencies
- Production dependencies

### Phase 2: Codebase Pattern Analysis

#### 2.1 Search for Similar Features

Find implementations similar to planned feature:

```markdown
Search strategy:
1. Identify domain terms related to your feature
2. Search by multiple naming conventions
3. Document all matches with file paths
```

**Example Grep patterns**:
```bash
# Search for feature-related terms
Grep: "upload" (case-insensitive)
Grep: "FileService|UploadService" (service patterns)
Grep: "class.*Upload" (class definitions)
```

**Document**:
- Similar feature locations
- How they're implemented
- Patterns used
- Integration points

#### 2.2 Identify Naming Conventions

Analyze naming patterns across codebase:

```markdown
Patterns to identify:
- File naming (kebab-case, PascalCase, snake_case)
- Function/method naming
- Class naming
- Database table/column naming
- API endpoint structure
- Component naming (frontend)
```

**Search techniques**:
- Use Glob for file patterns: `**/*.service.ts`
- Use Grep for class patterns: `class \w+Service`
- Use Grep for function patterns: `function \w+`
- Read multiple files to confirm patterns

**Document**:
- Naming convention for each category
- Examples from codebase
- Exceptions or inconsistencies

#### 2.3 Analyze Architecture Patterns

Identify architectural patterns used:

```markdown
Backend patterns to identify:
- Service layer pattern (business logic)
- Repository pattern (data access)
- Controller/route pattern (API endpoints)
- Middleware pattern (request processing)
- Dependency injection pattern

Frontend patterns to identify:
- Component hierarchy (atoms, molecules, organisms)
- State management (context, stores, reducers)
- Routing pattern
- API client pattern
- Form handling pattern
```

**Search strategies**:
- Find service files: Glob `**/*service*`
- Find repository files: Glob `**/*repository*`
- Find controllers: Glob `**/*controller*`
- Read representative files to understand patterns

**Document**:
- Architecture layers identified
- How layers communicate
- Design patterns in use
- File organization within patterns

### Phase 3: Technology Stack Documentation

#### 3.1 Backend Stack

Identify backend technologies:

```markdown
Framework:
- Read package.json/pyproject.toml for framework
- Examples: FastAPI, Express, Django, NestJS

ORM/Database:
- Check for SQLAlchemy, Prisma, TypeORM, Sequelize
- Identify database type (PostgreSQL, MySQL, MongoDB)

Authentication:
- Search for auth patterns: Grep "authenticate|authorization"
- Identify JWT, session, OAuth patterns

API Style:
- REST, GraphQL, tRPC
- API versioning approach
```

**Document in table format**:
| Layer | Technology | Version | Usage Pattern |
|-------|------------|---------|---------------|
| Framework | e.g., FastAPI | 0.100.0 | Async endpoints |
| ORM | e.g., SQLAlchemy | 2.0 | Declarative models |

#### 3.2 Frontend Stack

Identify frontend technologies:

```markdown
Framework:
- React, Vue, Svelte, Angular
- Check package.json for version

State Management:
- Redux, Zustand, Pinia, Context API
- Find store/state files

Component Library:
- Material-UI, Radix, Shadcn, Ant Design
- Search for imports

Styling:
- Tailwind, CSS Modules, Styled Components
- Check for config files
```

**Document in table format**:
| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | e.g., Vue 3 | Composition API |
| State | e.g., Pinia | Store modules |

#### 3.3 DevOps/Infrastructure

Identify deployment and CI/CD:

```markdown
CI/CD:
- Check .github/workflows/
- Check .gitlab-ci.yml
- Check .circleci/config.yml

Containerization:
- Dockerfile
- docker-compose.yml
- Kubernetes configs

Deployment:
- Vercel, Netlify, AWS, GCP
- Check package.json scripts
```

**Document**:
- CI/CD platform and configuration
- Container strategy
- Deployment targets
- Environment configurations

### Phase 4: Related Feature Analysis

#### 4.1 Find All Related Code

When analyzing features related to planned work:

```markdown
Search strategy:
1. Identify domain-specific terms
2. Search across all file types
3. Track imports to find dependencies
4. Map call graph for key functions
```

**Example workflow**:
```bash
# Find all references to domain term
Grep: "UserProfile" (output_mode: files_with_matches)

# Read key files
Read: src/models/user-profile.ts
Read: src/services/user-profile-service.ts
Read: src/api/routes/user-profile.ts

# Find imports of UserProfile
Grep: "import.*UserProfile" (output_mode: content)
```

**Document**:
- All related files with purposes
- Key functions and their responsibilities
- Data models and schemas
- API endpoints

#### 4.2 Document Extension Opportunities

Analyze whether to extend existing code or create new:

```markdown
Questions to answer:
- Can existing code be extended?
- Would extension violate Single Responsibility Principle?
- What are risks of modification vs. new code?
- Are there extension points designed in?
```

**Document in table format**:
| Existing Code | Extend? | Rationale |
|---------------|---------|-----------|
| UserService | No | SRP violation - handles too much already |
| AuthMiddleware | Yes | Designed with plugin pattern |

#### 4.3 Identify Integration Points

Map where new code will connect:

```markdown
Integration points to identify:
- Existing services to call
- Shared utilities to use
- Database tables to relate to
- API endpoints to integrate with
- Frontend components to extend
- State stores to connect with
```

**Document**:
- Service integrations needed
- Shared utilities available
- Database relationships required
- API integration points

## Output Format

Generate research report using template from `context/documentation-standards.md`:

```markdown
# Project Research Report: {Feature Name}

**Date**: {YYYY-MM-DD}
**Researcher**: {agent-name}
**Feature Context**: {what you're researching for}

## Executive Summary

{2-3 sentences summarizing key findings and recommendations}

## Project Structure

### Directory Organization
{How project is organized}

### Key Directories for This Feature
- `{path}` - {purpose}

## Coding Standards

### Naming Conventions
- **Files**: {pattern with examples}
- **Functions**: {pattern with examples}
- **Classes**: {pattern with examples}
- **Database**: {pattern with examples}
- **API Endpoints**: {pattern with examples}

### Code Style
- **Linting**: {tool and key rules}
- **Formatting**: {tool and configuration}
- **Documentation**: {standard with examples}

### Testing Standards
- **Framework**: {tool}
- **Coverage**: {requirements if any}
- **Organization**: {pattern}

## Technology Stack

### Backend
| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | | |
| ORM | | |
| Database | | |
| Auth | | |

### Frontend
| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | | |
| State | | |
| Styling | | |
| Components | | |

## Related Existing Features

### Similar Implementations Found

#### {Feature Name}
- **Location**: `{path}`
- **Pattern**: {description}
- **Relevance**: {why this matters}

### Extension vs. New Code Analysis

| Existing Code | Extend? | Rationale |
|---------------|---------|-----------|
| | | |

## Integration Points

### Services to Integrate With
- `{ServiceName}` at `{path}` - {integration needed}

### Shared Utilities Available
- `{utilityName}` at `{path}` - {what it provides}

### Database Relationships
- `{existing_table}` - {how to relate}

## Recommendations

### Do's
1. {Specific recommendation based on findings}
2. {Follow pattern X found in Y}

### Don'ts
1. {Anti-pattern to avoid}
2. {Inconsistency to not propagate}

### Files Likely to Create/Modify

**New Files**:
- `{path}` - {purpose}

**Modified Files**:
- `{path}` - {what changes}

## Open Questions

1. {Question needing team clarification}
2. {Technical decision to discuss}

## References

- Project Documentation: `{paths}`
- Similar Features: `{paths}`
- Related Issues/PRs: `{links if applicable}`
```

## Success Criteria

Analysis is complete when:
- [ ] All project documentation read and summarized
- [ ] Directory structure mapped and documented
- [ ] Naming conventions identified with examples
- [ ] Architecture patterns documented
- [ ] Technology stack fully cataloged
- [ ] Similar features found and analyzed
- [ ] Integration points clearly identified
- [ ] Extension vs. new code decisions documented
- [ ] Recommendations are specific and actionable
- [ ] Research report is comprehensive and well-organized

## Tips & Best Practices

### Do's
1. **Be thorough** - Don't assume, verify by reading code
2. **Document evidence** - Always cite file paths
3. **Focus on relevance** - Prioritize findings for your feature
4. **Note inconsistencies** - If patterns vary, document both
5. **Use context files** - Refer to analysis-patterns.md and search-strategies.md

### Don'ts
1. **Don't skip documentation reading** - May contain critical context
2. **Don't assume single pattern** - Codebases often have multiple conventions
3. **Don't analyze everything** - Focus on areas relevant to your work
4. **Don't delay writing** - Document as you discover, not at end
5. **Don't ignore tooling** - Linters and configs reveal standards

### Time Management
- **Quick analysis** (15 min): Phases 1-2 only
- **Standard analysis** (30-45 min): Phases 1-3
- **Deep analysis** (60+ min): All phases with thorough Phase 4

### Progressive Refinement
1. Start with broad overview
2. Narrow to relevant areas
3. Deep dive on integration points
4. Document throughout

## Related Workflows

- Use **map-filesystem** first if project structure is unfamiliar
- Use **find-patterns** for focused pattern discovery
- Use **understand-feature** for deeper dive on specific features
- Use **trace-dependencies** if integration points are complex

## Related Context Files

- `../context/analysis-patterns.md` - Analysis methodologies
- `../context/search-strategies.md` - Effective search techniques
- `../context/documentation-standards.md` - Report templates and standards
