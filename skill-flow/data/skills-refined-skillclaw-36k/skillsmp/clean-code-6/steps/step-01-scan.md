---
name: step-01-scan
description: Initialize and scan codebase for technologies and issues
prev_step: null
next_step: steps/step-02-apply.md
---

# Step 1: SCAN

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER modify files in this step - scan only
- ✅ ALWAYS parse flags before anything else
- 📋 YOU ARE A SCANNER, not a fixer
- 💬 FOCUS on detection and analysis only
- 🚫 FORBIDDEN to apply any changes

## EXECUTION PROTOCOLS:

- 🎯 Parse flags first, then analyze
- 💾 Save results if `{save_mode}` = true
- 📖 Complete scan before moving to step-02
- 🚫 FORBIDDEN to load step-02 until scan complete

## CONTEXT BOUNDARIES:

- This is the first step - no previous context
- Flags parsed from user input
- Results passed to step-02 via memory

## YOUR TASK:

Parse flags, detect technologies, and find anti-patterns in the codebase.

---

## EXECUTION SEQUENCE:

### 1. Parse Flags

```yaml
defaults:
  auto_mode: false # -a
  economy_mode: false # -e
  save_mode: false # -s
  force_react: false # --react
  force_nextjs: false # --nextjs
  force_zustand: false # --zustand
  force_query: false # --query
  force_backend: false # --backend
  force_test: false # --test
  force_expo: false # --expo
  force_forms: false # --forms
  force_css: false # --css
  force_ux: false # --ux
  force_security: false # --security
  skip_a11y: false # --no-a11y
```

Parse input: flags → state variables, remainder → `{task_description}`
Generate `{task_id}` (kebab-case from description)

### 2. Check Resume (-r)

**If `-r {id}` provided:**
→ Find `.claude/output/clean-code/{id}*/`
→ Restore state from `00-context.md`
→ Load appropriate step
→ **STOP**

### 3. Create Output (if save_mode)

```bash
mkdir -p .claude/output/clean-code/{task_id}
```

### 4. Scan Codebase

**If `{economy_mode}` = true:**
→ Direct tools only (Read, Grep, Glob)

**If `{economy_mode}` = false:**
→ Launch 3 agents in parallel (single message):

| Agent | Type             | Task                                       |
| ----- | ---------------- | ------------------------------------------ |
| 1     | explore-codebase | Detect technologies from package.json      |
| 2     | explore-codebase | Find anti-patterns in `{task_description}` |
| 3     | explore-codebase | Find good patterns to preserve             |

### 5. Technology Detection Rules

**Read `package.json` and detect technologies using these exact matches:**

| Technology     | Detection (dependencies/devDependencies)  | Sets Flag        |
| -------------- | ----------------------------------------- | ---------------- |
| React          | `react`                                   | `force_react`    |
| Next.js        | `next`                                    | `force_nextjs`   |
| Expo           | `expo`                                    | `force_expo`     |
| Zustand        | `zustand`                                 | `force_zustand`  |
| TanStack Query | `@tanstack/react-query`                   | `force_query`    |
| TanStack Form  | `@tanstack/react-form`                    | `force_forms`    |
| Prisma         | `@prisma/client` OR `prisma`              | `force_backend`  |
| Vitest         | `vitest`                                  | `force_test`     |
| Playwright     | `@playwright/test`                        | `force_test`     |
| Maestro        | `maestro` (check also `.maestro/` folder) | `force_test`     |
| Tailwind       | `tailwindcss`                             | `force_css`      |
| Better Auth    | `better-auth`                             | `force_security` |

**Additional file-based detection:**

| Technology | File/Folder Detection         | Sets Flag       |
| ---------- | ----------------------------- | --------------- |
| Prisma     | `prisma/schema.prisma` exists | `force_backend` |
| Expo       | `app.json` with `expo` key    | `force_expo`    |
| Maestro    | `.maestro/` folder exists     | `force_test`    |

### 6. Summarize Findings

```markdown
## Detected Technologies

| Category  | Found      |
| --------- | ---------- |
| Framework | Next.js 15 |
| State     | Zustand    |

| ...

## Issues Found

| File:Line   | Issue              | Priority |
| ----------- | ------------------ | -------- |
| Auth.tsx:45 | useEffect fetching | 🔴       |

| ...
```

### 7. Confirm

**If `{auto_mode}` = true:**
→ Proceed to step-02

**If `{auto_mode}` = false:**
→ Use AskUserQuestion to confirm

---

## SUCCESS METRICS:

✅ Flags parsed correctly
✅ Technologies detected
✅ Issues cataloged with file:line
✅ Good patterns identified

## FAILURE MODES:

❌ Modifying files during scan
❌ Skipping package.json analysis
❌ Not using parallel agents (when economy_mode = false)

## SCAN PROTOCOLS:

- Always read package.json first
- Report issues with file:line format
- Distinguish "missing" from "incorrectly used"

---

## NEXT STEP:

After scan complete, load `./step-02-apply.md`

<critical>
SCAN ONLY - don't fix anything!
</critical>
