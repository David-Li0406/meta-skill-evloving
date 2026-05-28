---
name: audit-codebase
description: Use this skill to run a comprehensive single-session audit on the codebase, covering aspects such as code quality, performance, security, refactoring, and documentation.
---

# Single-Session Codebase Audit

## Pre-Audit Validation

**Step 1: Check Thresholds**

Run `npm run review:check` and report results. If no thresholds are triggered:

- Display: "⚠️ No review thresholds triggered. Proceed anyway? (This is a lightweight single-session audit)"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# Test count
npm test 2>&1 | grep -E "Tests:|passing|failed" | head -5

# Lint status
npm run lint 2>&1 | tail -10

# Dependency vulnerabilities
npm audit --json 2>/dev/null | node -e '
try {
  const d = JSON.parse(require("fs").readFileSync(0,"utf8"));
  console.log(JSON.stringify(d.metadata?.vulnerabilities ?? d.vulnerabilities ?? {}, null, 2));
} catch (e) {
  console.log("{\"error\": \"Invalid JSON from npm audit\"}");
}
'

# Documentation lint
npm run docs:check 2>&1 | tail -30

# Check for broken links
grep -rn "\[.*\](.*\.md)" docs/ --include="*.md" 2>/dev/null | head -20
```

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `code`, `performance`, `refactoring`, `security`, `documentation`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_AUDIT_PLAN_TEMPLATE.md` and verify:

- [ ] Stack versions match package.json
- [ ] Test count baseline is accurate
- [ ] Documentation inventory is current
- [ ] Security-sensitive file list is current

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas:**

1. **Code Quality**: Check for unused imports, dead code, and adherence to best practices.
2. **Performance**: Analyze bundle sizes, rendering performance, and data fetching strategies.
3. **Security**: Review authentication, authorization, and input validation practices.
4. **Refactoring**: Identify god objects, code duplication, and cognitive complexity issues.
5. **Documentation**: Ensure all documentation is up-to-date, links are valid, and content is coherent.

**For each category:**

1. Search relevant files using Grep/Glob.
2. Identify specific issues with file:line references.
3. Classify severity: S0 (Critical - blocks work) | S1 (Major - causes confusion) | S2 (Minor) | S3 (Trivial).
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major).
5. **Assign confidence level** based on findings.

This skill provides a holistic approach to auditing a codebase, ensuring that all critical aspects are covered in a single session.