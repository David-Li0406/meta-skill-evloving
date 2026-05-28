---
name: dependency-conflict-resolver
description: Diagnoses npm/yarn dependency conflicts, identifies cascading updates, and suggests safe upgrade paths for React/Node.js projects.
scripts:
  - name: analyze-dependencies
    command: node .github/skills/dependency-conflict-resolver/analyze-dependencies.js
    description: Checks package.json for compatibility issues (React ecosystem, version mismatches, outdated packages)
---

# Dependency Conflict Resolver Skill

This skill helps diagnose and resolve npm dependency conflicts for FanHub's React frontend and Node.js backend.

## Common Dependency Conflict Patterns

### 1. ERESOLVE Peer Dependency Errors

**Symptom**:
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE could not resolve
npm ERR! 
npm ERR! While resolving: react-router-dom@6.20.0
npm ERR! Found: react@17.0.2
npm ERR! 
npm ERR! Could not resolve dependency:
npm ERR! peer react@"^18.0.0" from react-router-dom@6.20.0
```

**What This Means**:
- `react-router-dom@6.20.0` **requires** React 18+
- Your project currently has React 17.0.2
- npm can't install both (incompatible)

**Diagnostic Steps**:
1. Identify the requesting package: `react-router-dom@6.20.0`
2. Identify the peer requirement: `react@^18.0.0`
3. Check current version: `react@17.0.2`
4. Determine cascading updates needed

**Resolution**:
```bash
# Check what else depends on React
npm list react

# Update related packages together
npm install react@^18.2.0 react-dom@^18.2.0 @testing-library/react@^13.0.0
```

---

### 2. React Ecosystem Version Mismatches

**The React Ecosystem Rule**: These packages MUST be on the same major version:
- `react`
- `react-dom`
- `react-native` (if used)

**Common Mismatch**:
```json
{
  "react": "^17.0.2",
  "react-dom": "^18.2.0"  // ❌ Different major version!
}
```

**Fix**:
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0"  // ✅ Same major version
}
```

**Why This Matters**: react-dom is tightly coupled to React internals. Version mismatch causes runtime errors.

---

### 3. Cascading Updates

When you update one package, others may need updates too.

**Example**: Upgrading to React 18

**Packages that need updates**:
| Package | React 17 Version | React 18 Version | Why |
|---------|------------------|------------------|-----|
| `react` | 17.0.2 | 18.2.0 | Core |
| `react-dom` | 17.0.2 | 18.2.0 | Must match React |
| `react-router-dom` | 5.3.0 | 6.x+ | v6 requires React 18 |
| `@testing-library/react` | 12.x | 13.x+ | Testing hooks for React 18 |
| `react-scripts` | 4.x | 5.x+ | Create React App tooling |

**Safe Update Order**:
1. Update all at once (avoid intermediate conflicts):
   ```bash
   npm install react@^18.2.0 react-dom@^18.2.0 \
     @testing-library/react@^13.0.0 \
     react-router-dom@^6.20.0 \
     react-scripts@^5.0.1
   ```

2. Check for breaking changes in each package
3. Run tests after update
4. Commit dependency updates separately from features

---

### 4. Lock File Desync

**Symptom**:
```
npm install
# Works fine

git pull
npm install
# Suddenly fails with conflicts
```

**Root Cause**: `package-lock.json` is out of sync with `package.json`

**Diagnostic Questions**:
- Is `package-lock.json` committed?
- Did someone manually edit `package.json` without running `npm install`?
- Are different npm versions being used? (check `npm --version`)

**Fix**:
```bash
# Delete lock file and regenerate
rm package-lock.json
npm install

# Or update specific package
npm update <package-name>
```

---

### 5. Exact Versions vs. Semantic Versioning

**Version Syntax**:
```json
{
  "react": "18.2.0",      // Exact - only 18.2.0
  "react": "^18.2.0",     // Caret - 18.x.x (minor/patch updates)
  "react": "~18.2.0",     // Tilde - 18.2.x (patch updates only)
}
```

**Problem with Exact Versions**:
- No automatic security patches
- Harder to resolve peer dependency ranges
- Lock file defeats the purpose

**FanHub Standard**: Use caret (`^`) for dependencies
```json
{
  "react": "^18.2.0",       // ✅ Allows patch and minor updates
  "react-router-dom": "^6.20.0"  // ✅ Gets security fixes
}
```

**Exception**: Exact versions for tools with breaking changes:
```json
{
  "typescript": "5.3.3"     // Exact - TS has frequent breaking changes
}
```

---

## FanHub-Specific Dependency Rules

### Frontend (React App)

**Current Stack**:
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "@testing-library/react": "^13.4.0",
  "react-scripts": "^5.0.1"
}
```

**Key Constraints**:
- React 18+ (using concurrent features)
- React Router v6 (new route syntax)
- Testing Library v13+ (React 18 support)

**When Upgrading**:
1. Check React compatibility first
2. Update react + react-dom together
3. Update testing-library if major React change
4. Check react-router compatibility
5. Update react-scripts last (if needed)

---

### Backend (Node.js API)

**Current Stack**:
```json
{
  "express": "^4.18.2",
  "pg": "^8.11.0",
  "jest": "^29.5.0"
}
```

**Key Constraints**:
- Node 18+ LTS
- PostgreSQL 14+ (pg driver compatibility)
- Express 4.x (stable, well-tested)

**When Upgrading**:
1. Check Node version compatibility (`.nvmrc`)
2. Check database driver compatibility
3. Run integration tests (database connections)

---

## Diagnostic Workflow

When `npm install` fails:

1. **Read the error message for package names**
   ```
   While resolving: [PACKAGE A]
   Found: [PACKAGE B]
   peer [VERSION REQUIREMENT] from [PACKAGE A]
   ```

2. **Identify the conflict type**:
   - Peer dependency? (one package requires specific version of another)
   - Version mismatch? (react vs react-dom on different majors)
   - Missing dependency? (package.json missing required peer)

3. **Check current versions**:
   ```bash
   npm list [package-name]
   ```

4. **Find compatible versions**:
   - Check package's GitHub/npm page for requirements
   - Look for "Peer Dependencies" section
   - Check CHANGELOG for breaking changes

5. **Plan update order**:
   - Core packages first (react, react-dom)
   - Dependent packages second (react-router, testing-library)
   - Build tools last (react-scripts)

6. **Execute and test**:
   ```bash
   npm install [packages]
   npm test
   ```

---

## Using the Diagnostic Script

Run before major updates:

```bash
node .github/skills/dependency-conflict-resolver/analyze-dependencies.js frontend/package.json
```

**Output Example**:
```json
{
  "file": "frontend/package.json",
  "totalDependencies": 42,
  "issues": [
    {
      "severity": "error",
      "package": "react-router-dom",
      "message": "react-router-dom@6 requires React 18+, but found React 17",
      "fix": "Upgrade react and react-dom to ^18.0.0, or downgrade react-router-dom to ^5.3.0",
      "category": "peer-dependency"
    },
    {
      "severity": "warning",
      "package": "react, typescript",
      "message": "2 packages use exact versions (no ^ or ~)",
      "fix": "Consider using ^ for minor version updates: \"^1.2.3\" allows 1.x.x updates",
      "category": "versioning-strategy"
    }
  ],
  "summary": "Found 2 potential issue(s)"
}
```

**Interpretation**:
- `severity: error` — Will cause install failure
- `severity: warning` — May cause issues or is non-optimal
- `category` — Type of issue (helps with resolution)

---

## Safe Upgrade Strategies

### Strategy 1: Check Breaking Changes First

Before updating:
```bash
# View package's changelog
npm view [package-name] repository.url
# Visit repo → CHANGELOG.md

# Or check directly on npm
npm view [package-name] version
npm view [package-name]@latest version
```

**Key breaking changes to check**:
- React 18: New rendering model, automatic batching
- React Router v6: New route syntax, no Switch component
- Testing Library v13: New render behavior for React 18

---

### Strategy 2: Update package.json All at Once

**Don't do this** (causes intermediate conflicts):
```bash
npm install react@^18.0.0    # Install
npm install react-dom@^18.0.0  # Conflict with existing lock
npm install @testing-library/react@^13.0.0  # More conflicts
```

**Do this** (resolve all at once):
```bash
npm install react@^18.0.0 react-dom@^18.0.0 @testing-library/react@^13.0.0
```

---

### Strategy 3: Verify Resolution

After updating:
```bash
# Check what was installed
npm list [package-name]

# Run tests
npm test

# Check for security issues
npm audit
```

---

### Strategy 4: Commit Separately

```bash
# Separate commits for dependency updates
git add package.json package-lock.json
git commit -m "chore: upgrade React 17 → 18 and related packages

- react: 17.0.2 → 18.2.0
- react-dom: 17.0.2 → 18.2.0
- @testing-library/react: 12.1.5 → 13.4.0

Breaking changes reviewed in React 18 migration guide."

# Then commit feature work
```

**Why**: Makes it easy to revert dependency changes if something breaks.

---

## Quick Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `ERESOLVE peer react@18` | Package needs newer React | Upgrade React + ecosystem together |
| React/React-DOM mismatch | Different major versions | Sync both to same major version |
| Lock file conflicts | Desync with package.json | Delete package-lock.json, reinstall |
| "Couldn't find package" | Typo or unpublished version | Check npm registry for correct version |
| Install works, app breaks | Breaking changes in update | Read CHANGELOGs, update code |

---

## When to Use This Skill

Ask Copilot with this skill when:
- `npm install` fails with ERESOLVE
- Need to update a major package version
- Unsure what cascading updates are needed
- Want to check compatibility before updating
- Teaching someone about dependency management

**Example prompts**:
- *"I'm getting ERESOLVE error for react-router-dom. What do I need to update?"*
- *"Run the dependency analyzer on frontend/package.json"*
- *"I want to upgrade React to 18. What other packages need updates?"*
- *"How do I resolve this peer dependency conflict?"*
