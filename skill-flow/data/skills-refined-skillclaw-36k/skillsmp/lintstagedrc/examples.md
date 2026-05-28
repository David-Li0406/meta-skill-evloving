# Lint-Staged Configuration Examples

## ⚠️ CRITICAL DEPRECATION WARNING

**Date**: December 2025
**Status**: This example may be outdated

**🚨 HIGH PRIORITY - DO NOT USE WITHOUT VERIFICATION**

Before using this example:
1. ✅ Verify `eslint --fix` flag is still correct for current ESLint version
2. ✅ Verify `prettier --write` flag is still correct for current Prettier version
3. ✅ Check if `stylelint --fix` syntax has changed (if using Stylelint)
4. ✅ Verify glob pattern syntax works with current lint-staged version
5. ✅ Check if `.lintstagedrc.json` format is still recommended
6. ✅ Verify command array execution order hasn't changed

**If lint-staged or tools have breaking changes:**
- Consult lint-staged documentation for current configuration format
- Check ESLint/Prettier/Stylelint CLI documentation for current flags
- Verify file pattern syntax

---

## Example: .lintstagedrc.json (Preferred Format)

**Configuration Date**: December 2025
**Format**: JSON

### Basic Configuration (Vue + TypeScript)

```json
{
  "*.{js,ts,vue}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"]
}
```

### Extended Configuration (with JSX/TSX Support)

```json
{
  "*.{js,jsx,ts,tsx,vue}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"]
}
```

### Extended Configuration (with Stylelint for CSS/SCSS)

**Note**: Only include if project has `stylelint` in `package.json`

```json
{
  "*.{js,jsx,ts,tsx,vue}": ["eslint --fix", "prettier --write"],
  "*.{css,scss}": ["stylelint --fix", "prettier --write"],
  "*.{json,md,yml,yaml}": ["prettier --write"]
}
```

### Full Configuration (All File Types)

```json
{
  "*.{js,jsx,ts,tsx,vue}": ["eslint --fix", "prettier --write"],
  "*.{css,scss,sass,less}": ["stylelint --fix", "prettier --write"],
  "*.{json,md,yml,yaml,html}": ["prettier --write"]
}
```

---

## Configuration Explanations

### File Patterns

**JavaScript/TypeScript/Vue Files**:
- `*.{js,ts,vue}` - Basic Vue 3 + TypeScript project
- `*.{js,jsx,ts,tsx,vue}` - If project uses JSX/TSX (React components or Vue JSX)
- **Why**: These files need ESLint for code quality and Prettier for formatting

**Style Files** (Optional - only if Stylelint configured):
- `*.{css,scss}` - Common style file extensions
- `*.{css,scss,sass,less}` - Extended style file support
- **Why**: Style files need Stylelint for CSS rules and Prettier for formatting

**Configuration Files**:
- `*.{json,md,yml,yaml}` - Common config and doc files
- `*.{json,md,yml,yaml,html}` - Extended with HTML
- **Why**: These files only need Prettier for consistent formatting

### Commands

**ESLint**: `eslint --fix`
- Automatically fixes linting errors where possible
- **Verify**: Check if `--fix` flag is still current
- **Alternative**: `eslint --fix --max-warnings=0` to fail on warnings

**Prettier**: `prettier --write`
- Formats files and writes changes back to disk
- **Verify**: Check if `--write` flag is still current
- **Alternative**: Add `--ignore-unknown` to skip unknown file types

**Stylelint**: `stylelint --fix` (optional)
- Automatically fixes style linting errors where possible
- **Verify**: Check if `--fix` flag is still current
- **Check Project**: Only include if `stylelint` in package.json

### Command Execution Order

**Important**: Commands in arrays run **sequentially** for each matched file:

1. First: `eslint --fix` runs and fixes code issues
2. Then: `prettier --write` runs and formats the fixed code

This order matters because:
- ESLint may modify code structure
- Prettier should format the final modified code
- Both commands modify files in place

---

## Stylelint Integration Decision Tree

**Should you include Stylelint commands?**

```
Check package.json for "stylelint" dependency:
├─ Found in dependencies/devDependencies?
│  ├─ YES → Include stylelint commands for *.{css,scss}
│  └─ NO  → Skip stylelint, only ESLint + Prettier
└─ Project has .stylelintrc or stylelint.config.*?
   ├─ YES → Include stylelint commands
   └─ NO  → Skip stylelint
```

**Example Detection Logic**:
```bash
# Check if Stylelint is installed
if grep -q '"stylelint"' package.json; then
  echo "✓ Stylelint found - include style file patterns"
else
  echo "✗ Stylelint not found - skip style file patterns"
fi
```

---

## Pattern Selection Guide

**Use Basic Pattern** (`*.{js,ts,vue}`):
- Pure Vue 3 project without React/JSX
- No style preprocessing (using plain CSS)
- Minimal configuration needed

**Use Extended Pattern** (`*.{js,jsx,ts,tsx,vue}`):
- Project uses JSX/TSX syntax
- Vue components with JSX render functions
- Mixed React and Vue components

**Use Stylelint Pattern** (`*.{css,scss}`):
- Project has Stylelint configured
- Using SCSS/Sass preprocessing
- Enforcing CSS code quality standards

**Use Full Pattern** (All extensions):
- Large project with multiple file types
- Comprehensive linting and formatting
- Team wants strict quality controls

---

## How to Verify Current Standards

**Check lint-staged Version**:
```bash
npm view lint-staged version
npm list lint-staged
```

**Check Tool CLI Flags**:
```bash
# ESLint
npx eslint --help | grep -A5 "fix"

# Prettier
npx prettier --help | grep -A5 "write"

# Stylelint (if installed)
npx stylelint --help | grep -A5 "fix"
```

**Test Configuration**:
```bash
# Test lint-staged without committing
npx lint-staged --verbose

# Test on specific file
echo "test" > test.js
git add test.js
npx lint-staged
git reset test.js
rm test.js
```

**Validate JSON Syntax**:
```bash
# Using jq (if installed)
jq empty .lintstagedrc.json && echo "Valid JSON" || echo "Invalid JSON"

# Using Node.js
node -e "require('./.lintstagedrc.json')" && echo "Valid JSON" || echo "Invalid JSON"
```

---

## Alternative Formats (If JSON Deprecated)

### .lintstagedrc.js (JavaScript with Logic)

```javascript
module.exports = {
  '*.{js,jsx,ts,tsx,vue}': ['eslint --fix', 'prettier --write'],
  '*.{css,scss}': ['stylelint --fix', 'prettier --write'],
  '*.{json,md,yml,yaml}': ['prettier --write'],
};
```

### package.json Field

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,vue}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml,yaml}": ["prettier --write"]
  }
}
```

---

## Common Issues and Solutions

**Issue**: Commands not running on staged files
- **Solution**: Verify files are actually staged with `git status`
- **Check**: Ensure patterns match your file extensions

**Issue**: ESLint errors block commit
- **Solution**: Fix errors or add `--max-warnings=-1` to allow warnings
- **Alternative**: Configure `.eslintrc` to reduce rule severity

**Issue**: Prettier reformats files after ESLint
- **Solution**: This is expected - always run Prettier after ESLint
- **Verify**: Check ESLint and Prettier configs are compatible

**Issue**: Stylelint command fails
- **Solution**: Verify Stylelint is installed: `npm list stylelint`
- **Check**: Ensure `.stylelintrc` configuration exists

---

## Important Reminders

1. **Always Research First**: Verify CLI flags haven't changed
2. **Check Tool Versions**: Ensure ESLint/Prettier/Stylelint versions are compatible
3. **Test Before Commit**: Run `npx lint-staged --verbose` to test
4. **Order Matters**: Run fixers (ESLint) before formatters (Prettier)
5. **Stylelint Optional**: Only include if project uses it
6. **Pattern Specificity**: Use specific patterns to avoid unnecessary processing
7. **JSON Preferred**: Simplest format, no build step required
