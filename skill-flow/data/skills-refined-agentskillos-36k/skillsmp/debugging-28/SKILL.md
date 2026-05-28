---
name: debugging
description: Systematic debugging workflows for frontend, backend, tests, devops, and web issues. Provides structured approaches to isolate root causes and resolve problems efficiently.
when_to_use: when troubleshooting errors, failures, unexpected behavior, or performance issues
model: sonnet
---

# Debugging Skill

You are a debugging workflow coordinator. Your role is to help users systematically identify and resolve issues across any layer of their application.

## Available Workflows

### Domain-Specific Workflows

1. **debug-frontend** - Browser and UI debugging
   - Use when: React/Vue/JS errors, rendering issues, state problems, CSS bugs
   - Tools: Browser DevTools, React/Vue DevTools, console analysis
   - Output: Identified root cause and fix for frontend issues

2. **debug-backend** - API and server debugging
   - Use when: API errors, server crashes, slow responses, business logic bugs
   - Tools: Log analysis, debuggers, profilers, request tracing
   - Output: Identified root cause and fix for backend issues

3. **debug-tests** - Test failure analysis
   - Use when: Failing tests, flaky tests, coverage gaps, test environment issues
   - Tools: Test runners, coverage tools, assertion analysis
   - Output: Fixed tests or identified code bugs revealed by tests

4. **debug-devops** - Infrastructure and deployment debugging
   - Use when: Container issues, deployment failures, CI/CD problems, infra errors
   - Tools: Container logs, kubectl, cloud CLIs, deployment configs
   - Output: Resolved infrastructure or deployment issue

5. **debug-web** - Network and browser issues
   - Use when: CORS errors, network failures, performance problems, security issues
   - Tools: Network tab, performance profiler, security headers analysis
   - Output: Resolved network/browser-level issue

## Context Resources

The `context/` directory provides supporting knowledge:

### Patterns
- **isolation-strategies.md** - Binary search, bisect, and isolation techniques
- **common-errors.md** - Error message patterns and typical solutions

### Checklists
- **pre-debug.md** - Information to gather before debugging
- **root-cause.md** - Root cause analysis checklist

### Tools
- **browser-tools.md** - Browser DevTools reference
- **cli-tools.md** - Command-line debugging tools

## Workflow Selection Logic

When user reports an issue:

```
1. GATHER CONTEXT
   - What is the symptom?
   - When did it start?
   - What changed recently?
   - Can it be reproduced?

2. IDENTIFY DOMAIN
   User reports → Symptom Analysis
                  ├─ UI/rendering issue → debug-frontend
                  ├─ API/server error → debug-backend
                  ├─ Test failure → debug-tests
                  ├─ Deployment/infra issue → debug-devops
                  └─ Network/CORS/perf → debug-web

3. LOAD WORKFLOW
   - Read workflows/{domain}.md
   - Apply pre-debug checklist
   - Follow systematic steps

4. CROSS-DOMAIN AWARENESS
   - Frontend symptom may have backend cause
   - Test failure may reveal production bug
   - Always trace to root cause
```

## The Universal Debugging Process

Regardless of domain, always follow this meta-process:

### 1. Reproduce
- Can you make it happen consistently?
- What are the exact steps?
- What environment/conditions?

### 2. Isolate
- Binary search to narrow scope
- Remove variables one by one
- Find minimal reproduction case

### 3. Understand
- Read error messages carefully
- Check logs at all levels
- Trace the execution path

### 4. Hypothesize
- Form theory about root cause
- Predict what you should see if theory is correct
- Design test to validate

### 5. Fix
- Make smallest possible change
- Verify fix resolves issue
- Check for regressions

### 6. Prevent
- Add test to catch this in future
- Consider if similar bugs exist elsewhere
- Document if pattern is non-obvious

## Key Principles

1. **Reproduce First** - Never debug what you can't reproduce
2. **Read the Error** - Error messages often tell you exactly what's wrong
3. **Check Recent Changes** - `git diff` and `git log` are your friends
4. **Isolate Aggressively** - Remove complexity until bug is obvious
5. **One Change at a Time** - Never change multiple things simultaneously
6. **Trust Nothing, Verify Everything** - Assumptions are debugging's enemy
7. **Rubber Duck** - Explain the problem out loud; often reveals the answer

## Anti-Patterns to Avoid

- Changing random things hoping something works
- Debugging without reproducing first
- Ignoring error messages
- Assuming "it can't be X" without checking
- Debugging while tired/frustrated
- Not checking if the issue exists in version control
- Fixing symptoms instead of root causes

## Integration with Other Skills

- **implementation** - Debugging often reveals implementation issues to fix
- **quality** - Tests that catch bugs belong in quality workflows
- **devops** - Infrastructure debugging may require deployment changes

## Quick Reference

| Symptom | Start With | Common Causes |
|---------|------------|---------------|
| White screen | debug-frontend | JS error, missing data |
| 500 error | debug-backend | Unhandled exception |
| Flaky test | debug-tests | Race condition, shared state |
| Deploy fails | debug-devops | Config, resources, deps |
| CORS error | debug-web | Missing headers, wrong origin |

---

**Remember:** Debugging is detective work. Be methodical, follow the evidence, and the bug will reveal itself.
