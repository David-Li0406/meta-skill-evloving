# Quality Assurance

Testing, code review, security audits, and quality improvements.

## Mental Model

QA is about finding problems before users do. You're adversarial - try to break things.

```
Codebase: Existing code with potential issues
         ↓
Scan: Automated tools, code review, pattern analysis
         ↓
Test: Write tests, run tests, manual testing
         ↓
Review: Code quality, optimization opportunities
         ↓
Report: What was found, severity, recommendations
```

## Key Principles

### Multiple Angles
Use different approaches to find different types of problems.
- Static analysis catches pattern issues
- Unit tests catch logic errors
- Integration tests catch interaction problems
- Manual testing catches UX issues
- Security review catches vulnerabilities

### Adversarial Mindset
Think like an attacker or confused user.
- "How would I exploit this?"
- "What would confuse a user?"
- "What happens if this fails?"
- "What if I provide unexpected input?"

### Prioritize by Impact
Not all issues are equal.
- Critical security bugs > performance issues > code style
- User-facing bugs > internal bugs
- Frequent issues > rare edge cases
- Focus energy on what matters most

### Browser Verification for UI
Any UI work needs visual and interactive verification.
- Test actual user flows
- Check visual appearance
- Verify error states
- Test on different screen sizes if relevant

## Agent Browser CLI Usage

Browser verification is essential for QA.

**Testing user flows:**
```bash
agent-browser open http://localhost:3000
agent-browser snapshot -i

# Test login flow
agent-browser fill "[name='email']" "test@example.com"
agent-browser fill "[name='password']" "password123"
agent-browser click "[type='submit']"
agent-browser screenshot after-login.png

# Test error states
agent-browser fill "[name='email']" "invalid-email"
agent-browser click "[type='submit']"
agent-browser screenshot error-state.png
```

**Visual verification:**
```bash
# Check different pages/states
agent-browser navigate http://localhost:3000/dashboard
agent-browser screenshot dashboard.png
agent-browser navigate http://localhost:3000/settings
agent-browser screenshot settings.png
```

## What to Extract from Users

- What areas should be focused on (security, performance, correctness)
- Known problem areas or concerns
- Risk tolerance (how thorough should we be?)
- What tests already exist
- Success criteria (all tests pass? security audit clean?)
- Timeline and priorities
- Access to test environments

## QA Approaches by Focus

| Focus | Key Activities |
|-------|----------------|
| Security | Input validation, auth flows, dependency vulnerabilities, OWASP top 10 |
| Performance | Profiling, load testing, bundle analysis, render optimization |
| Correctness | Unit tests, integration tests, edge cases, regression tests |
| Code quality | Patterns, readability, maintainability, documentation |
| Accessibility | Screen readers, keyboard navigation, color contrast |

## Red Flags

You're doing it wrong if:
- Only testing happy paths
- Ignoring UI/UX issues because "code works"
- Not prioritizing findings
- Testing without clear criteria for "done"
- Skipping browser verification for UI
- Not documenting what was tested

## Story Structure for QA

Typical QA PRD structure:
1. Setup - establish testing approach and scope
2. Automated analysis - run tools, analyze results
3. Manual review - code review, pattern analysis
4. Test writing - new tests for gaps identified
5. Browser verification - UI and interaction testing
6. Report - document findings, severity, recommendations
