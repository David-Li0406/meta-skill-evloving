# Risk-Based Sprint Planning

Organize implementation sprints by risk level to ship safely and efficiently.

## Risk Classification Matrix

| Risk Level | Characteristics | Ship Gate | Examples |
|------------|-----------------|-----------|----------|
| Low | No user-facing changes, isolated scope | Immediately | Type fixes, token audits, docs, lint rules |
| Medium | User-visible but reversible | Unit tests pass | Component rewrites, animations, styling |
| High | Data mutations, auth, payments | E2E tests pass | Checkout flows, auth changes, payment processing |
| Critical | Irreversible operations | Full regression + manual QA | Data migrations, account deletion, refunds |

## Priority Order

When tasks compete for attention:

1. **Bugs** - Broken functionality blocks everything
2. **Breaking Changes** - API/schema changes affecting downstream
3. **Consistency** - UI/UX coherence across flows
4. **Polish** - Animations, micro-interactions, edge states
5. **Performance** - Optimization after correctness

## Sprint Sequencing Strategy

### Phase 1: Foundation (Low Risk)
- Design tokens and CSS variables
- Type definitions and interfaces
- Utility functions
- Static configuration
- Documentation updates

**Gate:** Type check passes

### Phase 2: Core Components (Medium Risk)
- Building block components
- State management setup
- Layout containers
- Navigation structure
- Form components

**Gate:** Unit tests pass + visual review

### Phase 3: Critical Flows (High Risk)
- Authentication flows
- Payment processing
- Data mutations
- User account operations
- Session management

**Gate:** E2E tests pass + security review

### Phase 4: Polish (Low-Medium Risk)
- Animations and transitions
- Loading states
- Error states
- Edge case handling
- Accessibility refinements

**Gate:** Visual regression passes

## Sprint Sizing Guidelines

| Sprint Type | Duration | Max Tasks | Focus |
|-------------|----------|-----------|-------|
| Micro | 1-2 days | 3-5 | Single component/flow |
| Standard | 3-5 days | 8-12 | Feature slice |
| Major | 1-2 weeks | 15-25 | Full feature |

## Scope Creep Prevention

### Expansion Triggers
When PRD grows during implementation:

1. **Minor expansion** (<20% new scope)
   - Add to current sprint if low risk
   - Document additions in PRD changelog

2. **Moderate expansion** (20-50% new scope)
   - Split into follow-up sprint
   - Ship MVP first, iterate second

3. **Major expansion** (>50% new scope)
   - Pause implementation
   - Re-run clarification session
   - Replan sprints from scratch

### Scope Lock Criteria
Lock scope when:
- Core flow is defined
- Dependencies identified
- Risk levels assigned
- Acceptance criteria written

## Dependency Mapping

### Dependency Types
| Type | Description | Handling |
|------|-------------|----------|
| Hard | Blocks task completely | Sequence strictly |
| Soft | Preferred but not blocking | Parallelize with mocks |
| Optional | Nice to have | Defer to polish phase |

### Dependency Resolution Order
1. External APIs/services
2. Database schema
3. Shared components
4. Feature-specific code
5. Tests
6. Documentation

## Sprint Retrospective Triggers

Run retro when:
- Sprint takes >150% estimated time
- Scope expanded mid-sprint
- Critical bug found post-ship
- Team blocked on dependencies
- Tech debt added intentionally

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Big Bang | Everything ships at once | Ship foundation first |
| Perfectionism | Polish before function | Ship MVP, iterate |
| Dependency Ignoring | Parallel work blocks | Map dependencies upfront |
| Scope Creep | Endless expansion | Lock scope, add sprints |
| Test Debt | Ship without coverage | Gate high-risk on E2E |
| Isolation | Build without user input | Demo at each phase |

## Sprint Documentation Template

```markdown
## Sprint: [Name]

### Scope
- [ ] Task 1 (Risk: Low/Medium/High)
- [ ] Task 2 (Risk: Low/Medium/High)

### Dependencies
- Blocked by: [list]
- Blocks: [list]

### Gate Criteria
- [ ] Type check passes
- [ ] Unit tests pass
- [ ] E2E tests pass (if high risk)
- [ ] Visual review complete

### Scope Lock
- Date locked: YYYY-MM-DD
- Additions after lock: [list]
```

## Velocity Tracking

Track per sprint:
- Tasks planned vs completed
- Risk level distribution
- Scope additions count
- Blocking time (hours)
- Rollback count

Use trends to improve estimation and identify systemic issues.
