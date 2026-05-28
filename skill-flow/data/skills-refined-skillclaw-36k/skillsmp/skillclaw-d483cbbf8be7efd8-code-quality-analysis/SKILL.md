---
name: code-quality-analysis
description: Use this skill when you need to comprehensively analyze code quality, security, performance, and architecture before committing changes.
---

# Skill body

## Purpose

This skill performs a thorough analysis of the codebase to identify issues and improvement opportunities across various dimensions, including quality, security, performance, and architecture.

## 🔴 Execution Steps

1. **Project Setup Verification**
   ```bash
   # Check package.json scripts
   cat package.json | jq '.scripts'
   ```

2. **Quality Gate Checks**
   - **Linting**
     ```bash
     npm run lint
     ```
   - **Type Checking**
     ```bash
     npx tsc --noEmit
     ```
   - **Build Verification**
     ```bash
     npm run build
     ```
   - **Testing**
     ```bash
     npm test
     ```

3. **Code Analysis**
   - **Quality Analysis**
     ```bash
     # Complexity analysis
     grep -rn "when\|if.*else\|for\|while" src/ --include="*.kt" | wc -l
     # Long method detection
     awk '/^[[:space:]]*(fun|suspend fun)/{start=NR} /^[[:space:]]*\}$/{if(NR-start>30) print FILENAME":"start}' src/**/*.kt
     # Duplicate code patterns
     grep -rn "TODO\|FIXME\|XXX\|HACK" src/ --include="*.kt"
     ```
   - **Security Analysis**
     ```bash
     # SQL Injection vulnerabilities
     grep -rn "sql\|query" src/ --include="*.kt" | grep -v "bind\|parameter"
     # Hardcoded secrets
     grep -rn "password\|secret\|apiKey\|token" src/ --include="*.kt"
     ```
   - **Performance Analysis**
     ```bash
     # N+1 query patterns
     grep -rn "flatMap.*repository\|forEach.*find" src/ --include="*.kt"
     # Blocking calls
     grep -rn "\.block()\|Thread\.sleep\|\.get()" src/ --include="*.kt"
     ```

4. **Reporting Results**
   - Generate a comprehensive report summarizing the results of the quality gate checks and code analysis, including:
     - Status of each check (pass/fail)
     - Identified issues with severity levels (Critical, High, Medium, Low)
     - Recommendations for improvements

## Output Format

### On Success
```markdown
[SEMO] Skill: code-quality-analysis completed

✅ **Quality Gate Passed**

| Step | Status | Duration |
|------|--------|----------|
| Lint | ✅ Pass | 2.3s |
| TypeCheck | ✅ Pass | 4.1s |
| Build | ✅ Pass | 12.5s |
| Test | ✅ Pass (42/42) | 8.2s |

---

💡 **Next Steps**: Shall we commit?
   - "Commit" → proceed with commit workflow
   - "No" → wait for further instructions
```

### On Failure
```markdown
[SEMO] Skill: code-quality-analysis failed

❌ **Lint Failed**

Errors:
src/utils/auth.ts
  42:10  error  'foo' is not defined  no-undef
  55:3   error  Unexpected any type    @typescript-eslint/no-explicit-any

💡 Would you like help fixing the errors?
   - "Fix it" → invoke code writing skill
   - "Ignore and continue" → proceed to next step (not recommended)
```

## 🔴 Post-Action: Commit Prompt

> After passing the quality gate, always confirm whether to commit.

### Automatic Prompt on Completion
```markdown
💡 **Next Steps**: Shall we commit?
   - "Commit" → proceed with commit workflow
   - "No" → wait for further instructions
```