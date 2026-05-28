---
name: agent-ops-dependencies
description: Use this skill when managing project dependencies, including adding, updating, or auditing them for security and compatibility.
---

# Dependencies Workflow

## Purpose

Safely manage project dependencies including adding new packages, updating existing ones, and handling security advisories.

## When to Use

- Adding a new dependency to the project
- Updating dependencies (routine or security)
- Auditing dependencies for vulnerabilities
- Investigating dependency conflicts
- Removing unused dependencies

## Preconditions

- `.agent/constitution.md` exists with package manager info
- Understand the project's dependency management approach

## Dependency Operations

### Adding a New Dependency

**Procedure**:

1. **Justify the addition**:
   - What problem does it solve?
   - Is there an existing alternative in the project?
   - What is the package's maintenance status?
   - What is the license? (compatible with project?)

2. **Evaluate the package**:
   - Check download stats / popularity
   - Check last update date
   - Check open issues / security history
   - Check transitive dependencies (avoid bloat)

3. **Add with pinned version**:
   ```bash
   # npm
   npm install package-name@version --save-exact
   
   # pip
   pip install package-name==version
   
   # cargo
   cargo add package-name@version
   ```

4. **Update lock file**: Ensure lock file is committed.

5. **Run validation**: Execute the full test suite after adding.

6. **Document**: Note in CHANGELOG if user-facing.

### Updating Dependencies

**Routine Updates**:

1. Check for available updates.
2. Review changelogs for breaking changes.
3. Update one package at a time (easier to debug).
4. Run full test suite after each update.
5. Commit with a clear message.

**Security Updates** (Priority):

1. Identify severity (critical/high/medium/low).
2. For critical/high: update immediately.
3. For medium/low: batch with routine updates.
4. Test thoroughly (security patches can break things).
5. Document in CHANGELOG.

### Removing Dependencies

1. Identify why it's being removed.
2. Find all usages in the codebase.
3. Remove usages first.
4. Remove from package manifest.
5. Update lock file.
6. Run full test suite.
7. Document removal reason.