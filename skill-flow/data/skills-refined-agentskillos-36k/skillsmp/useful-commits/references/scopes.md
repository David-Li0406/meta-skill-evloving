# Scope Usage Guidelines

## Purpose

Scopes provide additional context about which part of the codebase changed. Use them to improve commit message clarity when the change is localized to a specific area.

## When to Use Scopes

### Use Scopes When:

**1. Change is localized to a clear component**
```
feat(auth): add password reset functionality
fix(ui): correct button alignment on mobile
refactor(api): simplify error handling middleware
```

**2. Codebase has well-defined modules**
```
feat(billing): implement subscription management
fix(analytics): correct event tracking timestamps
test(parser): add edge case coverage
```

**3. Multiple teams work on different areas**
```
feat(mobile): add offline sync capability
feat(web): add offline sync capability
```
Scopes distinguish which platform was modified

### Omit Scopes When:

**1. Change affects entire codebase**
```
chore: update dependencies
build: upgrade to Node 18
style: apply new formatting rules
```

**2. Scope is unclear or debatable**
```
refactor: consolidate validation logic
```
Better than `refactor(utils): consolidate validation logic` if logic spans multiple areas

**3. Change is trivial**
```
docs: fix typo in README
ci: update workflow timeout
```

**4. Only one meaningful scope exists**
For small projects with no clear component boundaries, scopes add noise

## Consistency Rules

### Rule 1: Establish Scope Names Early

Once a scope name is chosen, use it consistently throughout the project.

**Good consistency:**
```
feat(auth): add login endpoint
fix(auth): correct token expiry calculation
refactor(auth): extract validation to middleware
test(auth): add integration tests
```

**Bad inconsistency:**
```
feat(auth): add login endpoint
fix(authentication): correct token expiry
refactor(authorization): extract validation
test(auths): add integration tests
```

### Rule 2: Use Singular, Not Plural

Scopes should be singular nouns unless the plural is the established term.

**Prefer:**
```
fix(component): ...
feat(service): ...
refactor(util): ...
```

**Avoid:**
```
fix(components): ...
feat(services): ...
refactor(utils): ...
```

**Exception:** When plural is the accepted term
```
docs(faqs): update frequently asked questions
feat(plugins): add plugin loader
```

### Rule 3: Lowercase Only

Scopes must be lowercase, even for acronyms.

**Correct:**
```
feat(api): add REST endpoints
fix(ui): correct layout
refactor(db): optimize queries
perf(grpc): reduce serialization overhead
```

**Incorrect:**
```
feat(API): add REST endpoints        ❌
fix(UI): correct layout              ❌
refactor(DB): optimize queries       ❌
perf(gRPC): reduce overhead          ❌
```

### Rule 4: No File Extensions or Paths

Use concept names, not file or directory names.

**Good (concept-focused):**
```
fix(auth): prevent token leakage
feat(parser): support JSON parsing
refactor(config): simplify initialization
```

**Bad (file/path-focused):**
```
fix(auth-service.ts): prevent token leakage           ❌
feat(src/parsers/json.go): support JSON parsing       ❌
refactor(config/loader.js): simplify initialization   ❌
```

## Scope Granularity

### Too Broad
```
feat(backend): add user management         ❌
```
"backend" is too generic—use specific component like "users" or "admin"

### Right Level
```
feat(users): add user management           ✅
feat(admin): add user management           ✅
```

### Too Narrow
```
feat(user-profile-avatar-component): add upload   ❌
```
Just use "profile" or "avatar"

```
feat(profile): add avatar upload           ✅
feat(avatar): add upload functionality     ✅
```

## Multiple Scopes

Use comma-separated scopes when a change affects multiple distinct areas.

### When to Use Multiple Scopes

**Legitimate multi-scope changes:**
```
refactor(core,api): consolidate error handling

Move shared error types from api package to core package. Update
api code to use core error types. This eliminates duplication and
enables other packages to use standard error types.
```

```
feat(ui,mobile): implement dark mode

Add dark mode support to both web UI and mobile app. Share color
definitions in design tokens package to ensure consistency across
platforms.
```

### Keep It Limited

**Maximum 2-3 scopes**. If more are needed, the commit likely does too much.

**Too many scopes indicates poor commit separation:**
```
refactor(auth,api,ui,db,cache,logging): update user system   ❌
```
Split into multiple commits

### Order Matters

List scopes by importance or in the order they appear in the project structure.

**Alphabetical:**
```
feat(api,ui): add user preferences
```

**By importance:**
```
feat(core,plugins): add plugin API
```
Core is more fundamental, so it comes first

## Scope Naming Patterns

### Component-Based
When project is organized by UI components:
```
feat(header): add logo
fix(footer): correct link colors
refactor(sidebar): simplify navigation
```

### Layer-Based
When project has architectural layers:
```
feat(api): add REST endpoint
fix(db): correct migration script
refactor(service): simplify business logic
test(repository): add integration tests
```

### Feature-Based
When project is organized by features:
```
feat(auth): add OAuth support
fix(billing): correct invoice calculation
refactor(notifications): consolidate email logic
```

### Platform-Based
For multi-platform projects:
```
feat(web): add offline mode
feat(mobile): add offline mode
feat(desktop): add offline mode
```

### Language-Based
For polyglot projects:
```
fix(python): correct import paths
fix(javascript): correct import paths
```

## Scope Discovery Process

### For New Projects

1. **Start without scopes** for first 10-20 commits
2. **Identify patterns** in commit locations
3. **Define scope names** based on natural groupings
4. **Document scopes** in CONTRIBUTING.md or similar
5. **Apply consistently** going forward

### For Existing Projects

1. **Review git history** to see existing scopes
2. **Follow established patterns** even if imperfect
3. **Propose changes** via team discussion
4. **Document** agreed-upon scopes

### Keep a Scope Glossary

Maintain a list of established scopes in documentation:

```markdown
## Commit Scopes

- `api` - REST API endpoints and middleware
- `auth` - Authentication and authorization
- `cli` - Command-line interface
- `core` - Core business logic
- `db` - Database schemas and migrations
- `docs` - Documentation
- `ui` - User interface components
- `utils` - Shared utilities
```

## Common Scope Anti-Patterns

### Anti-Pattern 1: Inventing New Scopes

❌ **Bad:**
```
feat(authentication): add login          # First commit uses "authentication"
fix(auth): correct token validation      # Second commit uses "auth"
refactor(authorization): simplify        # Third commit uses "authorization"
```

✅ **Good:**
Pick one and stick to it:
```
feat(auth): add login
fix(auth): correct token validation
refactor(auth): simplify permission checks
```

### Anti-Pattern 2: Mixing Granularities

❌ **Bad:**
```
feat(api): add user endpoints            # Broad scope
fix(user-profile-settings): correct bug  # Overly specific scope
```

✅ **Good:**
Use consistent granularity:
```
feat(api): add user endpoints
fix(api): correct user profile bug
```

Or:
```
feat(users): add management endpoints
fix(users): correct profile bug
```

### Anti-Pattern 3: Scope Drift

❌ **Bad:**
```
feat(auth): add login                    # Week 1
fix(authentication): correct token       # Week 2
refactor(auth-service): simplify         # Week 3
```

✅ **Good:**
Maintain consistency over time:
```
feat(auth): add login
fix(auth): correct token validation
refactor(auth): simplify token handling
```

### Anti-Pattern 4: Capitalizing Scopes

❌ **Bad:**
```
feat(API): add endpoint
fix(UI): correct layout
refactor(DB): optimize queries
```

✅ **Good:**
Always lowercase:
```
feat(api): add endpoint
fix(ui): correct layout
refactor(db): optimize queries
```

## Edge Cases

### Monorepos

For monorepos, scope can indicate the package:

```
feat(web-app): add dashboard
feat(mobile-app): add dashboard
feat(shared-components): add button component
```

Or combine package + component:
```
feat(web-app/auth): add login
feat(mobile-app/auth): add login
```

Choose one pattern and document it

### Microservices

Each service can have its own scopes, or service name can be the scope:

**Service as scope:**
```
feat(user-service): add profile endpoint
fix(billing-service): correct invoice calculation
```

**Component within service:**
```
feat(api): add profile endpoint          # In user-service repo
fix(calculator): correct invoice total   # In billing-service repo
```

### Libraries/SDKs

Scope can indicate the module:

```
feat(http): add retry logic
fix(logger): correct timestamp format
refactor(cache): simplify eviction
```

## Character Budget

Remember: scopes count toward the 70-character subject limit.

**Without scope:**
```
feat: implement comprehensive user authentication system with OAuth
     ^-- 67 characters (3 remaining)
```

**With scope:**
```
feat(auth): implement comprehensive user authentication system
            ^-- 63 characters (7 remaining)
```

**Scope impact:**
```
feat(authentication): ...  # Uses 17 chars
feat(auth): ...            # Uses 7 chars (10 chars saved)
```

Choose concise scope names to preserve room for meaningful descriptions.

## Team Guidelines

### Establish Conventions

In team settings, document scope conventions:

**CONTRIBUTING.md example:**
```markdown
## Commit Scopes

Use these standardized scopes:

- `api` - REST API (not "rest-api", "api-server", "backend-api")
- `ui` - User interface (not "frontend", "client", "webapp")
- `db` - Database (not "database", "storage", "persistence")
- `auth` - Authentication (not "authentication", "login", "security")

Omit scopes for changes affecting the entire codebase (build, dependencies, config).
```

### Code Review Scope Checks

During code review, verify:
- [ ] Scope matches established conventions
- [ ] Scope is lowercase
- [ ] Scope is consistent with similar commits
- [ ] Scope fits within 70-character subject limit
- [ ] Multiple scopes are justified
- [ ] Scope is omitted when appropriate

## Summary

Effective scope usage requires:
1. **Consistency**: Use the same names throughout the project
2. **Clarity**: Choose concept-level names, not file names
3. **Conciseness**: Keep scopes short (3-10 characters ideal)
4. **Discipline**: Follow established patterns, even when imperfect
5. **Documentation**: Maintain a scope glossary for teams

When in doubt, prefer consistency over perfection. An imperfect scope used consistently is better than perfect scopes applied inconsistently.
