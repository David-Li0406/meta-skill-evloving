# Module: Project Plan Assembly

## Output artifact

Use `templates/sprint-plan.template.md` as the skeleton.

## Merge strategy

Define:
- Main integration branch name
- Feature branch naming (must include backlog ID)
- Whether you need integration branches (int/phase1-core, etc.)
- Hierarchical merge order when clusters exist

### Branch naming convention

```
feature/<ID>-<slug>     # Feature branches (matches CLAUDE.md)
fix/<ID>-<slug>         # Bug fixes
int/phase<N>-<name>     # Integration branches (if needed)
claude/<ID>-<slug>      # AI-assisted development
```

### Merge order patterns

**Simple (no conflicts)**:
```
feature/101-types → develop
feature/102-api → develop
feature/103-ui → develop
```

**Phased (with integration)**:
```
Phase 1:
  feature/101-types → int/phase1-core
  feature/102-api → int/phase1-core
  int/phase1-core → develop

Phase 2:
  feature/103-ui → develop (depends on phase 1)
```

## Engineer coordination

Define:
- Which tasks can run in parallel (Phase 1)
- Which tasks depend on Phase 1 (Phase 2+)
- Explicit "integration merge" tasks at the end of each phase

## Coordination checklist

For each phase:
- [ ] All tasks have clear owners
- [ ] Dependencies are explicit
- [ ] Integration checkpoint is scheduled
- [ ] CI gates are defined
- [ ] Rollback plan exists

## Output structure

See `templates/sprint-plan.template.md` for the full template.
