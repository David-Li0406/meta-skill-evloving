# Report Template

Write to `./reports/{yyyyMMdd}-{branch-name}.md`. Use `!` prefix for warnings (e.g., `!Breaking:`, `!FAILED`).

```markdown
# Package Update Report: {branch-name}

## Summary

| Metric          | Value            |
| --------------- | ---------------- |
| Verification    | PASSED / !FAILED |
| Vulnerabilities | {count} / None   |
| Major           | {count}          |
| Minor           | {count}          |
| Patch           | {count}          |

## Notable Changes

### {package-name} ({old-version} -> {new-version}) [major/minor]

**Changes:**

- !Breaking: {description}
- New: {description}
- Fix: {description}

**Project Impact:** Affected / Not affected

- {affected-files-or-features}

**Reference:** [CHANGELOG]({url})

## Other Updates

| Package | Change             | Type  | Notes |
| ------- | ------------------ | ----- | ----- |
| {name}  | {x.x.x} -> {y.y.y} | patch | -     |

## Security Audit

No vulnerabilities found. / {count} vulnerabilities found:

| Severity | Package | Advisory               |
| -------- | ------- | ---------------------- |
| {level}  | {name}  | [{id}]({advisory-url}) |

## Verification Results

### {script-name}

\`\`\`
{output-summary}
\`\`\`

## Conclusion

- **Breaking Changes:** No action required / !Action required: {details}
- **Vulnerabilities:** None / !{count} found: {details}
- **Recommendation:** Ready to merge / !Needs attention: {details}
```
