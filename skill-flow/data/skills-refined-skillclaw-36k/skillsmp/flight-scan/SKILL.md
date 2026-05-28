---
name: flight-scan
description: Scan project and generate flight.json config for domain detection. Use when setting up Flight in a new project or after adding new technologies.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-scan

Scan a project to detect which Flight domains apply and write the config to `.flight/flight.json`.

## Usage

```
/flight-scan
```

## Arguments

- None - Scans current project directory

---

## Process

### 1. List Available Domains

```bash
ls .flight/domains/*.flight
```

### 2. For Each Domain, Check File Patterns

Read each `.flight` file and extract the `file_patterns` section:

```yaml
# Example from typescript.flight
file_patterns:
  - "**/*.ts"
  - "**/*.tsx"
```

For each pattern, check if matching files exist (excluding standard directories):

```bash
find . -name "*.ts" -not -path "*/node_modules/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/.next/*" -not -path "*/.git/*" | head -1
```

If files found → domain is enabled.

### 3. Check package.json for Dependencies

Read `package.json` and check for these dependency mappings:

| package.json dependency | Domain |
|------------------------|--------|
| `twilio` | sms-twilio |
| `@prisma/client`, `prisma` | prisma |
| `@clerk/nextjs`, `@clerk/clerk-react` | clerk |
| `@supabase/supabase-js`, `@supabase/ssr` | supabase |
| `next` | nextjs |
| `react`, `react-dom` | react |
| `vitest`, `jest`, `mocha`, `@testing-library/*` | testing |
| `typescript` | typescript |

### 4. Always Include code-hygiene

The `code-hygiene` domain applies to ALL projects. Always add it to the enabled list.

### 5. Write flight.json

Write the results to `.flight/flight.json`:

```json
{
  "generated": "2026-01-15T12:00:00Z",
  "scan_root": ".",
  "enabled_domains": ["code-hygiene", "typescript", "react"],
  "detection_log": {
    "code-hygiene": "always enabled",
    "typescript": "found *.ts files",
    "react": "package.json: react"
  }
}
```

### 6. Output Summary

Print a summary of detected domains:

```
Flight Scan Complete
====================
Enabled domains: code-hygiene, typescript, react, testing
Written to: .flight/flight.json

Detection log:
  code-hygiene: always enabled
  typescript: found *.ts files
  react: package.json: react
  testing: package.json: vitest
```

---

## Output: flight.json

```json
{
  "generated": "[ISO timestamp]",
  "scan_root": ".",
  "enabled_domains": ["code-hygiene", "..."],
  "detection_log": {
    "[domain]": "[detection reason]"
  }
}
```

---

## Pattern Conversion

Convert glob patterns to find commands:

| Glob Pattern | Find Command |
|--------------|--------------|
| `**/*.ts` | `find . -name "*.ts"` |
| `**/*.tsx` | `find . -name "*.tsx"` |
| `**/sms*.js` | `find . -name "sms*.js"` |

---

## Critical Rules

1. **ALWAYS INCLUDE code-hygiene** - It applies to all code
2. **CHECK BOTH FILE PATTERNS AND DEPENDENCIES** - Some domains detected by files, others by deps
3. **EXCLUDE STANDARD DIRECTORIES** - node_modules, dist, build, .next, .git
4. **PARSE YAML CAREFULLY** - `file_patterns` is an array of glob strings
5. **WRITE VALID JSON** - Use proper escaping and formatting

---

## Example Run

```
$ /flight-scan

Scanning .flight/domains/*.flight...

Checking typescript.flight:
  Pattern: **/*.ts → found 15 files
  Pattern: **/*.tsx → found 8 files
  ✓ typescript enabled

Checking react.flight:
  Pattern: **/*.jsx → found 0 files
  Pattern: **/*.tsx → found 8 files
  ✓ react enabled

Checking package.json dependencies:
  ✓ react found → react domain
  ✓ typescript found → typescript domain
  ✓ vitest found → testing domain

Flight Scan Complete
====================
Enabled domains: code-hygiene, typescript, react, testing
Written to: .flight/flight.json
```

---

## When to Use

| Situation | Use This? |
|-----------|-----------|
| Setting up Flight in new project | Yes |
| Added new technology/framework | Yes |
| Domains not being detected | Yes |
| Starting a task | No → Use `/flight-prime` |
| Validating code | No → Use `/flight-validate` |

---

## Next Step

After scanning:

```
/flight-prime <task>
```
