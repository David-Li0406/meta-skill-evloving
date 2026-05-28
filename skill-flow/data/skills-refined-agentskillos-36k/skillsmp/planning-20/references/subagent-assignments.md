# Subagent Assignment Reference

## Task Type to Subagent Mapping

This reference helps assign the appropriate specialist subagents to implementation tasks based on task type and domain.

---

## Database Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Schema Design | data-layer-expert | backend-architect | Tables, columns, relationships |
| Migrations | data-layer-expert | python-backend-engineer | Alembic migrations |
| RLS Policies | data-layer-expert | - | Row Level Security |
| Indexes | data-layer-expert | - | Performance optimization |
| Constraints | data-layer-expert | - | Foreign keys, unique constraints |
| Audit Triggers | data-layer-expert | backend-architect | Audit logging triggers |

**Example**:
```markdown
- [ ] DB-001: Schema Design (3 pts)
      Assigned Subagent(s): data-layer-expert, backend-architect
```

---

## Repository Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Base Repository | python-backend-engineer | data-layer-expert | CRUD operations |
| Query Methods | python-backend-engineer | - | Specific queries |
| Cursor Pagination | python-backend-engineer | data-layer-expert | Pagination logic |
| Transaction Handling | data-layer-expert | python-backend-engineer | Rollback patterns |
| RLS Integration | data-layer-expert | python-backend-engineer | Security enforcement |
| ORM Relationships | python-backend-engineer | data-layer-expert | SQLAlchemy relationships |

**Example**:
```markdown
- [ ] REPO-001: Query Methods (3 pts)
      Assigned Subagent(s): python-backend-engineer
```

---

## Service Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| DTO Definitions | python-backend-engineer | backend-architect | Pydantic schemas |
| Business Logic | backend-architect | python-backend-engineer | Core workflows |
| Validation | python-backend-engineer | - | Input validation |
| Error Handling | python-backend-engineer | backend-architect | ErrorResponse patterns |
| Observability | backend-architect | - | OpenTelemetry spans |
| Service Integration | backend-architect | python-backend-engineer | Multi-service orchestration |

**Example**:
```markdown
- [ ] SVC-002: Business Logic (5 pts)
      Assigned Subagent(s): backend-architect, python-backend-engineer
```

---

## API Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Router Setup | python-backend-engineer | backend-architect | FastAPI routers |
| Endpoint Implementation | python-backend-engineer | - | Request handlers |
| Request Validation | python-backend-engineer | - | Pydantic models |
| Response Formatting | python-backend-engineer | - | DTO serialization |
| Authentication | backend-architect | python-backend-engineer | Clerk integration |
| OpenAPI Documentation | api-documenter | python-backend-engineer | Swagger specs |
| API Versioning | backend-architect | - | Version strategy |

**Example**:
```markdown
- [ ] API-001: Router Setup (2 pts)
      Assigned Subagent(s): python-backend-engineer, backend-architect
```

---

## Frontend Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Component Design | ui-designer | ux-researcher | Wireframes, mockups |
| Component Implementation | ui-engineer-enhanced | - | React components |
| State Management | frontend-developer | - | React Query, context |
| Hooks | frontend-developer | - | Custom hooks |
| API Integration | frontend-developer | ui-engineer-enhanced | Backend integration |
| Forms | frontend-developer | ui-engineer-enhanced | Form handling |
| Routing | frontend-developer | nextjs-architecture-expert | Next.js App Router |
| Styling | ui-engineer-enhanced | ui-designer | Tailwind, CSS |

**Example**:
```markdown
- [ ] UI-001: Component Design (3 pts)
      Assigned Subagent(s): ui-designer, ux-researcher
```

---

## Mobile Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Screen Design | ui-designer | ux-researcher | Mobile wireframes |
| Screen Implementation | mobile-app-builder | - | React Native screens |
| Navigation | mobile-app-builder | - | React Navigation |
| Expo Configuration | mobile-app-builder | - | app.json, plugins |
| Native Modules | mobile-app-builder | - | Platform-specific code |
| Push Notifications | mobile-app-builder | backend-architect | Notification setup |

**Example**:
```markdown
- [ ] MOB-001: Screen Implementation (3 pts)
      Assigned Subagent(s): mobile-app-builder
```

---

## Testing Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Unit Tests (Backend) | python-backend-engineer | - | pytest |
| Unit Tests (Frontend) | frontend-developer | - | Jest, Vitest |
| Integration Tests (API) | python-backend-engineer | data-layer-expert | API + DB tests |
| Component Tests | frontend-developer | ui-engineer-enhanced | React Testing Library |
| E2E Tests | testing specialist | frontend-developer | Playwright |
| Performance Tests | python-backend-engineer | backend-architect | Load testing |
| Accessibility Tests | web-accessibility-checker | ui-engineer-enhanced | WCAG compliance |
| Visual Regression | testing specialist | ui-designer | Screenshot tests |

**Example**:
```markdown
- [ ] TEST-002: Integration Tests (3 pts)
      Assigned Subagent(s): python-backend-engineer, data-layer-expert
```

---

## Documentation Layer Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| API Documentation | api-documenter | python-backend-engineer | Endpoint docs |
| Component Documentation | documentation-writer | ui-engineer-enhanced | Storybook docs |
| User Guides | documentation-writer | - | How-to guides |
| Developer Guides | documentation-writer | - | Technical guides |
| Architecture Docs | documentation-complex | lead-architect | Multi-system docs |
| ADRs | lead-architect | backend-architect | Decision records |
| README Files | documentation-writer | - | Package READMEs |
| Changelog | changelog-generator | - | Version history |

**Example**:
```markdown
- [ ] DOC-001: API Documentation (1 pt)
      Assigned Subagent(s): api-documenter, python-backend-engineer
```

---

## Performance & Optimization Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| React Optimization | react-performance-optimizer | frontend-developer | Memoization, lazy loading |
| Database Optimization | data-layer-expert | python-backend-engineer | Query optimization |
| API Performance | backend-architect | python-backend-engineer | Caching, batching |
| Bundle Optimization | frontend-developer | nextjs-architecture-expert | Code splitting |
| Image Optimization | ui-engineer-enhanced | - | Image formats, CDN |

**Example**:
```markdown
- [ ] PERF-001: React Optimization (2 pts)
      Assigned Subagent(s): react-performance-optimizer, frontend-developer
```

---

## Accessibility Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| WCAG Compliance | web-accessibility-checker | ui-engineer-enhanced | Accessibility audit |
| Screen Reader Support | web-accessibility-checker | ui-engineer-enhanced | ARIA labels |
| Keyboard Navigation | web-accessibility-checker | frontend-developer | Focus management |
| Color Contrast | ui-designer | web-accessibility-checker | Contrast ratios |
| Form Accessibility | ui-engineer-enhanced | web-accessibility-checker | Label associations |

**Example**:
```markdown
- [ ] A11Y-001: WCAG Compliance (2 pts)
      Assigned Subagent(s): web-accessibility-checker, ui-engineer-enhanced
```

---

## DevOps & Deployment Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Feature Flags | DevOps | backend-architect | Toggle configuration |
| Monitoring Setup | DevOps | backend-architect | OpenTelemetry config |
| CI/CD Pipeline | DevOps | - | GitHub Actions |
| Deployment | DevOps | lead-pm | Staging/production |
| Docker Configuration | DevOps | - | Containerization |
| Environment Config | DevOps | backend-architect | Env variables |

**Example**:
```markdown
- [ ] DEPLOY-001: Feature Flags (1 pt)
      Assigned Subagent(s): DevOps, backend-architect
```

---

## Refactoring Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Code Refactoring | refactoring-expert | - | Code quality |
| Architecture Refactoring | lead-architect | backend-architect | System redesign |
| Database Refactoring | data-layer-expert | backend-architect | Schema changes |
| UI Refactoring | ui-engineer-enhanced | ui-designer | Component updates |
| API Refactoring | backend-architect | python-backend-engineer | Endpoint redesign |

**Example**:
```markdown
- [ ] REFACTOR-001: Code Refactoring (3 pts)
      Assigned Subagent(s): refactoring-expert
```

---

## Debugging Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Complex Debugging | ultrathink-debugger | - | Deep analysis |
| Backend Debugging | python-backend-engineer | data-layer-expert | API/DB issues |
| Frontend Debugging | frontend-developer | ui-engineer-enhanced | React/UI issues |
| Performance Debugging | backend-architect | react-performance-optimizer | Performance issues |
| Integration Debugging | backend-architect | - | Multi-system issues |

**Example**:
```markdown
- [ ] DEBUG-001: Complex Debugging (5 pts)
      Assigned Subagent(s): ultrathink-debugger
```

---

## Planning & Analysis Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| PRD Writing | prd-writer | lead-pm | Requirements docs |
| Implementation Planning | implementation-planner | lead-architect | Task breakdown |
| Task Decomposition | task-decomposition-expert | - | Story splitting |
| Feature Planning | feature-planner | lead-pm | Feature analysis |
| Research Spikes | spike-writer | - | Investigation docs |
| Architecture Planning | lead-architect | backend-architect | System design |

**Example**:
```markdown
- [ ] PLAN-001: Implementation Planning (3 pts)
      Assigned Subagent(s): implementation-planner, lead-architect
```

---

## Review & Validation Tasks

| Task Type | Primary Subagent(s) | Secondary Subagent(s) | Notes |
|-----------|-------------------|---------------------|-------|
| Code Review | code-reviewer | senior-code-reviewer | Peer review |
| Architecture Review | lead-architect | backend-architect | Design review |
| Task Validation | task-completion-validator | - | Completion check |
| API Review | api-librarian | - | API standards |
| Telemetry Review | telemetry-auditor | - | Observability check |
| Strict QA | karen | - | Enforcement |

**Example**:
```markdown
- [ ] REVIEW-001: Code Review (1 pt)
      Assigned Subagent(s): code-reviewer
```

---

## Default Assignments by Phase

### Phase 1: Database
- Primary: data-layer-expert
- Secondary: backend-architect

### Phase 2: Repository
- Primary: python-backend-engineer
- Secondary: data-layer-expert

### Phase 3: Service
- Primary: backend-architect
- Secondary: python-backend-engineer

### Phase 4: API
- Primary: python-backend-engineer
- Secondary: backend-architect

### Phase 5: UI
- Primary: ui-engineer-enhanced, frontend-developer
- Secondary: ui-designer

### Phase 6: Testing
- Primary: testing specialist
- Secondary: Varies by test type

### Phase 7: Documentation
- Primary: documentation-writer
- Secondary: Varies by doc type

### Phase 8: Deployment
- Primary: DevOps
- Secondary: lead-pm

---

## Assignment Format

**In Implementation Plans**:
```markdown
| Task ID | Task Name | ... | Assignee | ... |
|---------|-----------|-----|----------|-----|
| API-001 | Router Setup | ... | python-backend-engineer | ... |
```

**In Progress Tracking**:
```markdown
- [ ] API-001: Router Setup (2 pts)
      Assigned Subagent(s): python-backend-engineer, backend-architect
```

**In Phase Breakdowns**:
```markdown
**Assigned Subagent(s)**: python-backend-engineer, backend-architect
```

---

## Available Subagents

May not be all-inclusive; refer to subagent registry in context for full list.

### Architecture
- lead-architect
- backend-architect
- nextjs-architecture-expert
- data-layer-expert

### Development
- python-backend-engineer
- frontend-developer
- ui-engineer-enhanced
- mobile-app-builder

### UI/UX
- ui-designer
- ux-researcher

### Review
- code-reviewer
- senior-code-reviewer
- task-completion-validator
- api-librarian
- telemetry-auditor
- karen

### Documentation
- documentation-writer
- documentation-complex
- documentation-planner
- api-documenter
- technical-writer
- openapi-expert
- changelog-generator

### Testing & Quality
- testing specialist
- web-accessibility-checker
- react-performance-optimizer

### Debugging
- ultrathink-debugger
- refactoring-expert

### Planning
- lead-pm
- prd-writer
- implementation-planner
- feature-planner
- spike-writer
- task-decomposition-expert

### DevOps
- DevOps (not a subagent, but role reference)
