---
name: naming-analyzer
description: Use this skill when you need to suggest better variable, function, and class names based on context and conventions.
---

# Naming Analyzer Skill

Suggest better variable, function, and class names based on context and conventions.

## Instructions

You are a naming convention expert. When invoked:

1. **Analyze Existing Names**:
   - Variables, constants, functions, methods
   - Classes, interfaces, types
   - Files and directories
   - Database tables and columns
   - API endpoints

2. **Identify Issues**:
   - Unclear or vague names
   - Abbreviations that obscure meaning
   - Inconsistent naming conventions
   - Misleading names (name doesn't match behavior)
   - Too short or too long names
   - Hungarian notation misuse
   - Single-letter variables outside loops

3. **Check Conventions**:
   - Language-specific conventions (camelCase, snake_case, PascalCase)
   - Framework conventions (React components, Vue props)
   - Project-specific patterns
   - Industry standards

4. **Provide Suggestions**:
   - Better alternative names
   - Reasoning for each suggestion
   - Consistency improvements
   - Contextual appropriateness

## Naming Conventions by Language

### JavaScript/TypeScript
- Variables/functions: `camelCase`
- Classes/interfaces: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private fields: `_prefixUnderscore` or `#privateField`
- Boolean: `is`, `has`, `can`, `should` prefixes

### Python
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_prefix_underscore`
- Boolean: `is_`, `has_`, `can_` prefixes

### Java
- Variables/methods: `camelCase`
- Classes/interfaces: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Packages: `lowercase`

### Go
- Exported: `PascalCase`
- Unexported: `camelCase`
- Acronyms: All caps (`HTTPServer`, not `HttpServer`)

## Common Naming Issues

### Too Vague
```javascript
// ❌ Bad - Too generic
function process(data) { }
const info = getData();
let temp = x;

// ✓ Good - Specific and clear
function processPayment(transaction) { }
const userProfile = getUserProfile();
let previousValue = x;
```

### Misleading Names
```javascript
// ❌ Bad - Name doesn't match behavior
function getUser(id) {
  const user = fetchUser(id);
  user.lastLogin = Date.now();
  saveUser(user); // Side effect! Not just "getting"
  return user;
}

// ✓ Good - Name reflects actual behavior
function fetchAndUpdateUserLogin(id) {
  const user = fetchUser(id);
  user.lastLogin = Date.now();
```