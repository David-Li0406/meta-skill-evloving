# Linting and Formatting

Runs project linters and formatters on changed files, fixing auto-fixable issues.

## Detect Project Tooling

Check for configuration files:
```bash
ls -la | grep -E "(eslint|prettier|biome|stylelint)"
cat package.json | grep -E "(lint|format|prettier|eslint)"
```

## Language-Specific Tools

### JavaScript/TypeScript

**ESLint** (`.eslintrc*`, `eslint.config.*`):
```bash
npx eslint --fix <files>
```

**Prettier** (`.prettierrc*`, `prettier.config.*`):
```bash
npx prettier --write <files>
```

**Biome** (`biome.json`):
```bash
npx biome check --apply <files>
```

Order: ESLint first, then Prettier

### Python

**Ruff** (`ruff.toml`, `pyproject.toml`):
```bash
ruff check --fix <files>
ruff format <files>
```

**Black** (`pyproject.toml`):
```bash
black <files>
```

**isort**:
```bash
isort <files>
```

Order: isort, then black/ruff

### Go

```bash
gofmt -w <files>
goimports -w <files>
golangci-lint run --fix <files>  # if .golangci.yml exists
```

### CSS/SCSS

**Stylelint** (`.stylelintrc*`):
```bash
npx stylelint --fix <files>
```

## What Gets Fixed

**Auto-fixable:**
- Indentation and spacing
- Quote style
- Semicolons
- Trailing commas
- Import order
- Line length (via wrapping)
- Bracket spacing
- Object shorthand

**NOT auto-fixable (requires manual intervention):**
- Complex type errors
- Naming convention violations
- Logic-related warnings

## Guidelines

- Only fix changed files, not entire codebase
- Use project config, don't override with personal preferences
- Consider committing format fixes separately from logic changes
