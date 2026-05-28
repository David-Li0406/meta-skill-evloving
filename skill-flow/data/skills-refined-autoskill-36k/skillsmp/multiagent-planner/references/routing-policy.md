# Routing Policy

Detailed decision trees for routing tasks to specialist subagents.

## Task Type Classification

### Primary Keywords

| Task Type | Strong Indicators | Weak Indicators |
|-----------|-------------------|-----------------|
| Bug | fix, broken, error, crash, failing, flaky, regression, doesn't work | issue, problem, wrong |
| Feature | add, implement, create, new, build, enable, support | want, need, should |
| Refactor | refactor, cleanup, reorganize, simplify, consolidate, extract | improve, optimize |
| Test | test, coverage, spec, verify, assert | check, ensure |
| Review | review, audit, analyze, check | look at, examine |

### Context Signals

Beyond keywords, consider:
- **Stack traces present** → Bug
- **"How does X work"** → Review/Explore
- **Performance concerns** → Could be Bug, Refactor, or Feature
- **Multiple files mentioned** → Consider Architect
- **Unknown library/framework** → Consider Searcher

## Decision Trees

### Bug Task Routing

```
Is there a failing test or error?
├─ Yes → Bug Finder
│   └─ Does fix require structural changes?
│       ├─ Yes → Also use Refactorer
│       └─ No → Continue to Test Planner
└─ No → Is it flaky/intermittent?
    ├─ Yes → Bug Finder (timing/state hypothesis)
    └─ No → Might be Feature or Review instead
```

### Feature Task Routing

```
Is this a large feature?
├─ Yes (cross-module, new abstraction, public API)
│   └─ Use Architect before Test Planner
└─ No (contained, clear scope)
    └─ Skip Architect, go to Test Planner

Does it touch auth, payments, or security boundaries?
├─ Yes → Consider Advisory Panel for risk assessment
└─ No → Standard flow
```

### Refactor Task Routing

```
Does refactor change interfaces/contracts?
├─ Yes → Use Architect to assess impact
└─ No → Refactorer alone is sufficient

Is there existing test coverage?
├─ Yes → Refactorer can proceed
└─ No → Test Planner first (characterization tests)
```

### Review Task Routing

```
Is this a design/architecture review?
├─ Yes → Use Architect before Reviewer
└─ No → Reviewer alone is sufficient

Is this security-sensitive?
├─ Yes → Reviewer with security focus
└─ No → Standard review
```

## Risk Flag Detection

Automatically trigger extra scrutiny when detecting:

| Risk Flag | Detection | Action |
|-----------|-----------|--------|
| Auth | "auth", "login", "session", "token", "password" | Security-focused review |
| Payments | "payment", "billing", "charge", "subscription" | Advisory Panel |
| Migrations | "migration", "schema", "database change" | Architect + rollback plan |
| Concurrency | "async", "parallel", "race", "lock", "thread" | Bug Finder for race conditions |
| Security | "security", "vulnerability", "injection", "xss" | Security audit |
| Performance | "slow", "timeout", "memory", "cpu" | Performance profiling |
| Public API | "api", "endpoint", "external", "breaking change" | Architect for compatibility |

## Agent Selection Heuristics

### When to Use Architect

Use Architect (opus model) when:
- Change spans 3+ modules
- Introduces new abstraction or pattern
- Modifies public/external interfaces
- Touches core domain model
- Has backwards compatibility concerns

Skip Architect when:
- Change is localized (1-2 files)
- Following existing patterns
- Internal refactoring only
- Test-only changes

### When to Use Searcher

Use Searcher (with Perplexity MCP) when:
- Unknown framework/library behavior
- Version-specific API questions
- Best practice uncertainty
- External standard compliance

Skip Searcher when:
- Codebase has clear patterns to follow
- Question is about internal code
- Documentation is in repo

### When to Use Advisory Panel

Use Advisory Panel when:
- High-stakes decisions (security, data, money)
- Multiple valid approaches with tradeoffs
- Team is uncertain about direction
- Reversibility is low

Skip Advisory Panel when:
- Clear precedent exists
- Low-risk changes
- Time-sensitive fixes
