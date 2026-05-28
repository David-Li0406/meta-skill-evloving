# Prettier Configuration Examples

## ⚠️ CRITICAL DEPRECATION WARNING

**Date**: December 2025
**Status**: This example may be outdated

**🚨 HIGH PRIORITY - DO NOT USE WITHOUT VERIFICATION**

Before using this example:
1. ✅ Verify `singleQuote` option is still valid and accepts boolean
2. ✅ Verify `semi` option is still valid and accepts boolean
3. ✅ Verify `trailingComma` option is still valid and accepts "es5"/"all"/"none"
4. ✅ Check if Prettier has deprecated or renamed any options
5. ✅ Verify `.prettierrc` format is still recommended
6. ✅ Check if new recommended options have been added

**If Prettier has breaking changes:**
- Consult Prettier documentation for current configuration options
- Check migration guides for deprecated options
- Verify option value types and allowed values

---

## Example: .prettierrc (Preferred Format)

**Configuration Date**: December 2025
**Prettier Version**: 3.x
**Format**: JSON (no file extension)

### Minimal Configuration (Recommended)

```json
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5"
}
```

### Extended Configuration (with Common Options)

```json
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "endOfLine": "lf"
}
```

### Full Configuration (with All Common Options)

```json
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "endOfLine": "lf",
  "useTabs": false,
  "arrowParens": "always",
  "bracketSpacing": true,
  "bracketSameLine": false,
  "proseWrap": "preserve"
}
```

---

## Configuration Option Explanations

### Essential Options (Minimal Config)

**`singleQuote: true`**
- Uses single quotes instead of double quotes for strings
- **Why**: Common JavaScript convention, cleaner appearance
- **Default**: `false` (double quotes)
- **Values**: `true` | `false`

**`semi: true`**
- Requires semicolons at the end of statements
- **Why**: Explicit statement termination, prevents ASI issues
- **Default**: `true`
- **Values**: `true` | `false`

**`trailingComma: "es5"`**
- Adds trailing commas where valid in ES5 (objects, arrays)
- **Why**: Cleaner git diffs, easier to add/remove items
- **Default**: `"all"` (in Prettier 3.x - verify current default)
- **Values**: `"none"` | `"es5"` | `"all"`

### Common Additional Options

**`printWidth: 100`**
- Maximum line length before wrapping
- **Why**: Balance between readability and screen space
- **Default**: `80`
- **Recommended**: `80` | `100` | `120`

**`tabWidth: 2`**
- Number of spaces per indentation level
- **Why**: Standard JavaScript convention
- **Default**: `2`
- **Values**: Any positive integer

**`endOfLine: "lf"`**
- Line ending style
- **Why**: Consistent across OS, Git-friendly
- **Default**: `"lf"`
- **Values**: `"lf"` | `"crlf"` | `"cr"` | `"auto"`

**`arrowParens: "always"`**
- Include parentheses around arrow function parameters
- **Why**: Consistency, easier to add parameters later
- **Default**: `"always"`
- **Values**: `"always"` | `"avoid"`

---

## Configuration Selection Guide

### Use Minimal Configuration:
- You want Prettier's defaults for most options
- Small to medium projects
- Team prefers convention over configuration
- **Recommended**: Start here and add options only if needed

### Use Extended Configuration:
- Need to customize line length (printWidth)
- Want explicit line ending control
- Team has specific formatting preferences
- **Use when**: Minimal config doesn't meet team needs

### Use Full Configuration:
- Large team with strict formatting standards
- Need explicit control over all formatting
- Documenting all decisions for new team members
- **Use when**: Need maximum clarity and control

---

## Option Value Guide

### `trailingComma` Values:

**`"none"`** - No trailing commas
```javascript
const obj = {
  a: 1,
  b: 2
};
```

**`"es5"`** - Trailing commas where valid in ES5 (objects, arrays)
```javascript
const obj = {
  a: 1,
  b: 2,  // ✓ Trailing comma
};

function foo(
  a,
  b,  // ✗ No trailing comma (not valid in ES5)
) {}
```

**`"all"`** - Trailing commas wherever possible (ES2017+)
```javascript
const obj = {
  a: 1,
  b: 2,  // ✓ Trailing comma
};

function foo(
  a,
  b,  // ✓ Trailing comma (valid in ES2017+)
) {}
```

### `endOfLine` Values:

- **`"lf"`**: Unix/macOS line endings (`\n`) - **Recommended**
- **`"crlf"`**: Windows line endings (`\r\n`)
- **`"cr"`**: Old Mac line endings (`\r`) - Rare
- **`"auto"`**: Maintain existing line endings - **Not recommended** (inconsistent)

---

## How to Verify Current Standards

**Check Prettier Version**:
```bash
npm view prettier version
npx prettier --version
```

**Check Available Options**:
```bash
# List all options with defaults
npx prettier --help

# Check specific option
npx prettier --help | grep -A3 "single-quote"
```

**Test Configuration**:
```bash
# Format a file and see output
echo 'const x = { a: 1, b: 2 }' | npx prettier --parser babel

# Check what Prettier would change
npx prettier --check "src/**/*.{js,ts,vue}"

# Format all files
npx prettier --write "src/**/*.{js,ts,vue}"
```

**Validate Configuration File**:
```bash
# Using jq (if installed)
jq empty .prettierrc && echo "Valid JSON" || echo "Invalid JSON"

# Using Node.js
node -e "JSON.parse(require('fs').readFileSync('.prettierrc', 'utf8'))" && echo "Valid" || echo "Invalid"

# Using Prettier itself
npx prettier --check .prettierrc
```

**Check Configuration Resolution**:
```bash
# See what config Prettier resolves for a file
npx prettier --find-config-path src/App.vue

# Show resolved configuration
npx prettier --config-precedence file-override src/App.vue
```

---

## Alternative Formats

### .prettierrc.json (Explicit JSON)

```json
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5"
}
```

### .prettierrc.js (JavaScript with Logic)

```javascript
module.exports = {
  singleQuote: true,
  semi: true,
  trailingComma: 'es5',
  // Can include dynamic logic
  printWidth: process.env.CI ? 80 : 100,
};
```

### package.json Field

```json
{
  "prettier": {
    "singleQuote": true,
    "semi": true,
    "trailingComma": "es5"
  }
}
```

---

## Integration with Other Tools

### ESLint Integration

When using with `eslint-plugin-prettier`:

**.prettierrc**:
```json
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5"
}
```

**eslint.config.cjs** should include:
```javascript
{
  rules: {
    'prettier/prettier': ['error', { endOfLine: 'auto' }],
  }
}
```

### Editor Integration

Most editors auto-detect `.prettierrc`:
- **VS Code**: Install "Prettier - Code formatter" extension
- **WebStorm**: Built-in Prettier support
- **Vim**: Use prettier/vim-prettier plugin

---

## Common Issues and Solutions

**Issue**: Prettier and ESLint conflicts
- **Solution**: Use `eslint-config-prettier` to disable conflicting ESLint rules
- **Verify**: Both tools should format the same way

**Issue**: Different formatting on different machines
- **Solution**: Ensure same Prettier version in package.json
- **Check**: Run `npm list prettier` on all machines

**Issue**: Git shows formatting changes after commit
- **Solution**: Set up lint-staged to format before commit
- **Configure**: `.lintstagedrc.json` with `prettier --write`

**Issue**: Line endings mixed (CRLF and LF)
- **Solution**: Set `endOfLine: "lf"` and use `.gitattributes`
- **Add**: `* text=auto eol=lf` to `.gitattributes`

**Issue**: Configuration not being applied
- **Solution**: Check if `.prettierrc` has valid JSON syntax
- **Debug**: Run `npx prettier --find-config-path .`

---

## Prettier Version Compatibility

**Prettier 3.x** (Current - December 2025):
- Default `trailingComma` changed from `"es5"` to `"all"`
- Dropped support for Node.js < 14
- Improved TypeScript and Vue formatting

**Prettier 2.x** (Legacy):
- Default `trailingComma` was `"es5"`
- Different formatting for some edge cases

**Migration from 2.x to 3.x**:
- Review changed defaults
- Test formatting on entire codebase
- Commit formatted changes separately

---

## Important Reminders

1. **Always Research First**: Verify options haven't changed in current Prettier version
2. **Minimal is Better**: Only configure options you need to change from defaults
3. **Test Configuration**: Run Prettier on sample files before committing config
4. **Version Lock**: Pin Prettier version in package.json to avoid unexpected changes
5. **Team Alignment**: Ensure all team members use same Prettier version
6. **Editor Integration**: Configure editors to format on save for consistency
7. **Git Integration**: Use lint-staged to format files before commit
8. **JSON Syntax**: Ensure .prettierrc is valid JSON (no trailing commas in config file itself!)
