# Conventional Commits Rules

Follows the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Commit Message Format

```
<emoji> <type>[scope][!]: <description>

[body]

[footer]
```

### Required Elements

- `<emoji>`: Emoji corresponding to the type
- `<type>`: Commit type (see table below)
- `<description>`: Summary of changes (in Korean)

### Optional Elements

- `[scope]`: Scope of change (e.g., `feat(auth):`, `fix(api):`)
- `[!]`: Breaking Change indicator (e.g., `feat!:`, `feat(auth)!:`)
- `[body]`: Detailed description (bullet point format)
- `[footer]`: Breaking Change explanation, etc.

## Type & Emoji Map

| Type | Emoji | Description | Examples |
|------|-------|-------------|----------|
| `feat` | ✨ | New feature | New component, API endpoint |
| `fix` | 🐛 | Bug fix | Logic error, exception handling |
| `docs` | 📝 | Documentation change | README, comments, JSDoc |
| `style` | 💄 | Code style | Formatting, semicolons, whitespace |
| `refactor` | ♻️ | Refactoring | Code improvement without behavior change |
| `perf` | ⚡ | Performance improvement | Optimization, caching |
| `test` | ✅ | Tests | Add/modify tests |
| `chore` | 🔧 | Config/build | package.json, config files |
| `ci` | 🚀 | CI/CD | GitHub Actions, deployment scripts |
| `build` | 📦 | Build system | Dependency changes, build tools |
| `revert` | ⏪ | Revert | Undo previous commit |

## Branch-Based Type Inference

| Branch Pattern | Inferred Type |
|----------------|---------------|
| `feature/*`, `feat/*` | `feat` |
| `fix/*`, `bugfix/*`, `hotfix/*` | `fix` |
| `docs/*` | `docs` |
| `refactor/*` | `refactor` |
| `test/*` | `test` |
| `chore/*` | `chore` |

## File-Based Type Inference

### File Extensions/Paths

| Changed Files | Inferred Type |
|---------------|---------------|
| `*.md`, `docs/*` | `docs` |
| `*.test.*`, `*.spec.*`, `__tests__/*` | `test` |
| `package.json`, `tsconfig.json`, `.eslintrc` | `chore` |
| `.github/*`, `Dockerfile`, `*.yml` (CI) | `ci` |

### Change Content Keywords

| Diff Content | Inferred Type |
|--------------|---------------|
| `TODO`, `FIXME` removed | `fix` |
| `console.log` removed | `chore` |
| New function/component added | `feat` |
| Import cleanup only | `style` |

## Type Inference Priority

1. **Branch name** (highest priority)
2. **Changed file paths/extensions**
3. **Diff content analysis**
4. **Default**: `feat`

## Breaking Change Notation

### Method 1: Add `!` after type

```
✨ feat!: Change API response structure
```

### Method 2: Add `BREAKING CHANGE:` in footer

```
✨ feat: Change API response structure

- Change response object field names
- Change pagination structure

BREAKING CHANGE: response.data changed to response.items
```

## Scope Usage

Add scope when changes are limited to a specific module/area:

```
✨ feat(auth): Add social login
🐛 fix(api): Fix token refresh error
♻️ refactor(components): Split Button component
```

## Examples

### Basic Format

```
✨ feat: Add user authentication feature

- Implement login/signup forms
- Add JWT token handling logic
```

### With Scope

```
🐛 fix(auth): Fix session expiry handling error

- Adjust token refresh timing
- Improve error handling
```

### Breaking Change

```
✨ feat(api)!: Change response structure

- response.data → response.items
- Add pagination metadata

BREAKING CHANGE: Existing API clients need modification
```

### Branch-Based Inference

Branch `feature/user-auth`:
```
✨ feat: Add user authentication feature
```

Branch `hotfix/login-bug`:
```
🐛 fix: Fix login bug
```

### File-Based Inference

Changed file `README.md`:
```
📝 docs: Update README
```

## Commit Message Writing Rules

### Length Limits

- **Subject (first line)**: Under 72 characters (including emoji + type + scope)
- Body: 72 characters per line recommended

### Tone

- Use **imperative mood** (present tense, start with verb)
- ✅ "Add", "Fix", "Delete", "Improve", "Refactor"
- ❌ "Added", "Fixed", "Deleted"

### Atomic Commits

- **One commit = One logical change**
- Unrelated changes must be split
- Example:
  - ❌ `feat: Add login feature and fix bug` (mixed)
  - ✅ `feat: Add login feature` + `fix: Fix session bug` (split)

## Prohibited

- ❌ Using `hotfix:` type → Use `fix`
- ❌ Using `merge:` type → Use Git auto-generated message
- ❌ Using non-standard types (types not in the table above)
- ❌ Adding `Co-Authored-By` pattern
