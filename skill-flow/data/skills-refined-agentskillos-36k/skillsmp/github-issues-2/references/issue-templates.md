# GitHub Issue Templates for LucidData

Complete markdown templates for creating consistent GitHub issues.

## Bug Report Template

```markdown
## Bug Description
[Clear, concise description]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Browser: [Chrome/Firefox/Safari + version]
- OS: [Windows/macOS/Linux + version]
- Node.js: [version]
- Next.js: [version]

## Screenshots/Logs
[Attach or paste here]

## Encryption Context (if applicable)
- Encryption key ID: [v1/v2]
- Data size: [approximate]
- Error from crypto lib: [if any]

## Audit Log Context (if applicable)
- Event type: [DATA_CREATED/DATA_UPDATED/etc.]
- Audit log ID: [if known]
- Hash chain position: [if relevant]

## Additional Context
[Any other relevant information]

⚠️ **Security Note**: Do not include encryption keys, passwords, or real user data
```

## Feature Request Template

```markdown
## Feature Description
[One-sentence summary]

## User Story
As a [user type],
I want to [action],
So that [benefit].

## Problem Statement
[What problem does this solve?]

## Proposed Solution
[Detailed description of how it should work]

## Privacy Impact Assessment
- **Data collected**: [None / Minimal / Sensitive]
- **Consent required**: [Yes/No]
- **Encryption needed**: [Yes/No - describe]
- **Audit events**: [What to log]
- **Data retention**: [How long to keep data]

## User Interface
[Mockups, wireframes, or description]

## Technical Considerations
- **Database changes**: [New tables, fields]
- **API endpoints**: [New routes needed]
- **Dependencies**: [New packages]

## Alternatives Considered
[Other approaches]

## Priority Justification
[Why is this important now?]
```

## Security Vulnerability Template

```markdown
⚠️ **SECURITY ISSUE - Handle with care**

## Vulnerability Type
[Select one: XSS, CSRF, SQL Injection, Authentication Bypass, Information Disclosure, etc.]

## Severity Assessment
- **Severity**: [Critical / High / Medium / Low]
- **CVSS Score**: [If calculated]
- **Attack Complexity**: [Low / Medium / High]
- **Privileges Required**: [None / Low / High]

## Affected Component
[Vault API / Consent Management / Auth System / etc.]

## Vulnerability Description
[Detailed technical description]

## Attack Scenario
[How could this be exploited?]

## Proof of Concept
**Steps to reproduce**:
1. [Step 1]
2. [Step 2]
3. [Observe vulnerability]

**Note**: Do not include actual exploit code for critical vulnerabilities

## Impact Analysis
- **Confidentiality**: [None / Low / Medium / High]
- **Integrity**: [None / Low / Medium / High]
- **Availability**: [None / Low / Medium / High]
- **Data at risk**: [User PII / Encryption keys / Sessions / etc.]

## Affected Versions
- **Introduced in**: [version]
- **Fixed in**: [version, if known]

## Recommended Fix
[Detailed remediation steps]

## Mitigation (Temporary)
[Workarounds until patch is available]

## Disclosure Timeline
- Discovery date: [YYYY-MM-DD]
- Vendor notification: [YYYY-MM-DD]
- Public disclosure: [Coordinate with maintainers]

⚠️ **DO NOT publicly disclose until patch is released**
```

## Test Failure Template

```markdown
## Test Information
- **File**: `path/to/test.test.ts`
- **Test name**: "should ..."
- **Framework**: [Vitest / Playwright]
- **Test type**: [Unit / Integration / E2E]

## Failure Output
```
[Paste error message and stack trace]
```

## Expected Result
[What the test should check]

## Actual Result
[What the test is finding]

## Reproducibility
- [x] Fails consistently
- [ ] Fails intermittently (flaky)
- [ ] Fails only in CI/CD
- [ ] Fails only locally

## Recent Changes
[Commits or PRs that may have caused this]

## Investigation Notes
[Any debugging already done]

## Suggested Fix
[If known]
```

## Documentation Update Template

```markdown
## Documentation Type
[README / API Docs / Code Comments / Setup Guide]

## Current State
[What's missing or incorrect]

## Proposed Changes
[What should be added or updated]

## Affected Files
- `README.md`
- `docs/setup.md`
- etc.

## Audience
[Developers / End Users / Admins]

## Priority
[How urgent is this documentation?]
```

---

**Usage**: Copy template, fill in placeholders, create issue with appropriate labels.
