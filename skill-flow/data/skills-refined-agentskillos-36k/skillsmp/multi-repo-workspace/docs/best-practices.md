# Best Practices

Guidelines for effective use of the Multi-Repo Workspace skill.

---

## Configuration Management

### 1. Keep Configuration Files Updated

**Why**: Outdated configuration leads to incorrect code generation.

**How**:
```bash
# After changing tech stack
vim .claude/config.json
# Update tech_stack array

# After changing conventions
vim .claude/config.json
# Update development.conventions

# Commit changes
git add .claude/
git commit -m "Update Claude configuration"
```

**When to Update**:
- ✅ Adding/removing dependencies
- ✅ Changing frameworks or libraries
- ✅ Updating coding conventions
- ✅ Modifying build commands
- ✅ Changing testing frameworks

### 2. Document Architectural Decisions

**Why**: Helps Claude understand context and make better suggestions.

**How**:
```markdown
# .claude/context.md

## Recent Decisions

### 2026-01-15 - Switched to Zustand for State Management

**Context**: Redux was too verbose for our use case
**Decision**: Migrated to Zustand for simpler state management
**Consequences**: 
- Reduced boilerplate by ~60%
- Easier to test
- Better TypeScript support
```

**What to Document**:
- ✅ Why certain patterns were chosen
- ✅ Trade-offs made
- ✅ Alternatives considered
- ✅ Future migration plans
- ✅ Known limitations

### 3. Version Your Configuration

**Why**: Track changes and rollback if needed.

**How**:
```json
{
  "metadata": {
    "version": "2.1.0",
    "last_updated": "2026-01-20",
    "changelog": "Added OAuth preferences"
  }
}
```

---

## Workspace Organization

### 1. Consistent Directory Structure

**Why**: Makes navigation and analysis easier.

**Recommended Structure**:
```
workspace/
├── .workspace/
│   └── config.json          # Workspace configuration
├── frontend/
│   ├── .claude/
│   │   ├── config.json
│   │   └── context.md
│   └── src/
├── backend/
│   ├── .claude/
│   │   ├── config.json
│   │   └── context.md
│   └── src/
└── shared/
    ├── .claude/
    │   ├── config.json
    │   └── context.md
    └── src/
```

### 2. Clear Repository Naming

**Why**: Easier to reference and understand dependencies.

**Good Names**:
- ✅ `frontend-web`
- ✅ `backend-api`
- ✅ `mobile-ios`
- ✅ `shared-types`
- ✅ `auth-service`

**Avoid**:
- ❌ `app1`
- ❌ `project`
- ❌ `new-repo`
- ❌ `temp`

### 3. Logical Repository Grouping

**Why**: Reflects actual architecture and dependencies.

**Monorepo**:
```
packages/
├── web-app/
├── mobile-app/
├── shared-ui/
└── api-client/
```

**Microservices**:
```
services/
├── auth-service/
├── user-service/
├── product-service/
└── api-gateway/
```

---

## Dependency Management

### 1. Explicit Internal Dependencies

**Why**: Claude can track and coordinate changes.

**How**:
```json
{
  "dependencies": {
    "internal": [
      "@workspace/shared-types",
      "@workspace/api-client"
    ]
  }
}
```

### 2. Mark Critical External Dependencies

**Why**: Claude knows which dependencies are essential.

**How**:
```json
{
  "dependencies": {
    "external_critical": [
      "react",
      "express",
      "typescript"
    ]
  }
}
```

### 3. Document Dependency Versions

**Why**: Avoid version conflicts.

**How**:
```markdown
# .claude/context.md

## Dependencies

### Critical Versions
- React: 18.2.0 (must match across all repos)
- TypeScript: 5.0.0 (workspace-wide standard)
- Node.js: 18.x (LTS)
```

---

## Code Generation Preferences

### 1. Set Clear Preferences

**Why**: Consistent code style across the repository.

**How**:
```json
{
  "claude_preferences": {
    "code_generation": {
      "style": "functional",
      "testing": "vitest",
      "documentation": "tsdoc",
      "error_handling": "try-catch"
    }
  }
}
```

### 2. Repository-Specific Conventions

**Why**: Different repos may have different needs.

**Example**:

**Frontend**:
```json
{
  "claude_preferences": {
    "code_generation": {
      "style": "functional",
      "prefer_composition": true,
      "use_hooks": true
    }
  }
}
```

**Backend**:
```json
{
  "claude_preferences": {
    "code_generation": {
      "style": "class-based",
      "use_dependency_injection": true,
      "prefer_async_await": true
    }
  }
}
```

### 3. Review Focus Areas

**Why**: Claude prioritizes what matters most.

**How**:
```json
{
  "claude_preferences": {
    "review_focus": [
      "security",
      "performance",
      "accessibility",
      "maintainability"
    ]
  }
}
```

---

## Workflow Best Practices

### 1. Initialize Once, Focus Often

**Pattern**:
```
# Once per session
@workspace init my-project

# Then focus as needed
@workspace focus frontend
# Work on frontend...

@workspace focus backend
# Work on backend...
```

### 2. Analyze Before Major Changes

**Pattern**:
```
# Before starting work
@workspace analyze

# Review inconsistencies and recommendations
# Then proceed with changes
```

### 3. Use Tasks for Multi-Repo Changes

**Pattern**:
```
# Instead of manual coordination
@workspace task "Add user authentication"

# Claude coordinates changes across repos
```

### 4. Regular Workspace Health Checks

**Pattern**:
```
# Weekly or after major changes
@workspace analyze

# Review:
# - Dependency versions
# - Configuration status
# - Inconsistencies
# - Technical debt
```

---

## Team Collaboration

### 1. Shared Configuration Standards

**Why**: Team consistency.

**How**:
- Document configuration standards in team wiki
- Use templates for new repositories
- Review configuration in PRs
- Automate validation with scripts

### 2. Configuration Review in PRs

**Why**: Catch configuration drift early.

**Checklist**:
```markdown
## Configuration Review
- [ ] .claude/config.json updated if tech stack changed
- [ ] .claude/context.md updated if architecture changed
- [ ] Dependencies list updated
- [ ] Conventions still accurate
```

### 3. Onboarding Documentation

**Why**: New team members can quickly understand workspace.

**Include**:
- Workspace structure overview
- How to use @workspace commands
- Repository relationships
- Common workflows
- Configuration guidelines

---

## Performance Optimization

### 1. Minimal Configuration

**Why**: Faster analysis and less context overhead.

**Do**:
```json
{
  "repository": {
    "name": "frontend",
    "type": "frontend",
    "tech_stack": ["react", "typescript"]
  }
}
```

**Don't**:
```json
{
  "repository": {
    "name": "frontend",
    "type": "frontend",
    "tech_stack": ["react", "typescript"],
    "every_single_dependency": ["..."],
    "every_dev_dependency": ["..."],
    "every_file_in_repo": ["..."]
  }
}
```

### 2. Focus Before Detailed Work

**Why**: Loads only relevant context.

**Pattern**:
```
# Load specific context
@workspace focus frontend

# Then work on details
"Add a new component with form validation"
```

### 3. Incremental Analysis

**Why**: Faster feedback.

**Pattern**:
```
# Analyze specific repo
@workspace focus backend
@workspace analyze

# Instead of always analyzing everything
```

---

## Security Considerations

### 1. No Secrets in Configuration

**Never**:
```json
{
  "api_keys": "sk-...",
  "database_password": "secret123"
}
```

**Instead**:
```json
{
  "environment": {
    "required_vars": ["API_KEY", "DATABASE_URL"]
  }
}
```

### 2. Document Security Patterns

**How**:
```markdown
# .claude/context.md

## Security Considerations

- All API keys in environment variables
- Use helmet.js for HTTP headers
- Implement rate limiting
- Sanitize all user inputs
- Follow OWASP Top 10 guidelines
```

### 3. Review Focus on Security

**How**:
```json
{
  "claude_preferences": {
    "review_focus": ["security"]
  }
}
```

---

## Maintenance

### 1. Regular Configuration Audits

**Frequency**: Monthly or quarterly

**Checklist**:
- [ ] All repos have configuration
- [ ] Tech stacks are current
- [ ] Dependencies are accurate
- [ ] Conventions are followed
- [ ] Context docs are updated

### 2. Deprecation Notices

**How**:
```markdown
# .claude/context.md

## Deprecations

### Deprecated: Class Components (2025-12-01)
- Migrate to functional components
- Use hooks instead of lifecycle methods
- Target completion: 2026-03-01
```

### 3. Migration Tracking

**How**:
```markdown
# .claude/context.md

## Active Migrations

### Redux → Zustand
- Status: 60% complete
- Remaining: User module, Settings module
- Target: 2026-02-15
```

---

## Common Pitfalls

### ❌ Outdated Configuration

**Problem**: Claude generates code using old patterns.

**Solution**: Update configuration after changes.

### ❌ Missing Context Documentation

**Problem**: Claude doesn't understand architectural decisions.

**Solution**: Document important decisions in context.md.

### ❌ Inconsistent Conventions

**Problem**: Different code styles across repos.

**Solution**: Standardize conventions in workspace config.

### ❌ Unclear Dependencies

**Problem**: Claude doesn't coordinate changes properly.

**Solution**: Explicitly list internal dependencies.

### ❌ Overloaded Configuration

**Problem**: Too much detail slows down analysis.

**Solution**: Keep configuration minimal and focused.

---

## Success Metrics

Track these to measure effectiveness:

- ✅ Time saved on cross-repo changes
- ✅ Consistency of generated code
- ✅ Reduction in integration bugs
- ✅ Team onboarding time
- ✅ Configuration coverage (% of repos configured)

---

## Next Steps

- 📖 Review [Commands Reference](./commands.md)
- 📖 Check [Setup Guide](./setup-guide.md)
- 🔍 Explore [Examples](../examples/)
- 🚀 Start using the skill!
