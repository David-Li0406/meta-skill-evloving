# Confidence Self-Assessment Protocol

**Purpose:** Force rigorous, evidence-based self-assessment to prevent hallucination and false confidence.

**When to use:**

- After completing any implementation work
- Before declaring a task "done"
- When user asks "are you sure this works?"
- Periodically during long tasks to validate progress

---

## Anti-Hallucination Rules

**BEFORE claiming ANY confidence level, you MUST provide concrete evidence.**

**Forbidden confidence claims:**

- ❌ "The tests should pass" → Did you RUN them? Show output.
- ❌ "This is production ready" → Did you validate ALL dimensions? Show proof.
- ❌ "I verified it works" → HOW? What command? What output?
- ❌ "The documentation says..." → Did you READ it via tool? Which URL/file?
- ❌ "This follows best practices" → Which practices? From which validated source?

**Required evidence types:**

- ✅ Tool results (Bash output, Read file content, WebFetch/Ref results)
- ✅ Specific line numbers and file paths
- ✅ Exact commands run and their output
- ✅ URLs/docs fetched and quoted text
- ✅ Test results showing pass/fail

---

## Confidence Matrix Assessment

Complete ALL dimensions. Do NOT skip any. Do NOT assume. ONLY state what you have OBSERVABLE EVIDENCE for.

### 1. Knowledge Source

**Question:** Where did the implementation approach come from?

**Levels:**

- `unfamiliar` = Closed source, unfamiliar system, no validation methods available, guessing
- `pattern_recall` = Recalled pattern from training data, NOT validated against current docs
- `pattern_adapted` = Known working pattern from codebase/example, modified for this use case
- `documented` = Official documentation checked via tool (Ref/Context7/WebFetch) and validated
- `cited` = Specific version documentation with URLs/file paths cited, best practices confirmed

**Your Assessment:**

```text
Level: [choose one above]

Evidence:
- [ ] I used Ref/Context7/Exa to search official documentation (provide query)
- [ ] I read specific documentation URL/file: _______________
- [ ] I quoted relevant sections from line ___ to line ___
- [ ] I cited specific version: _______________
OR
- [ ] I recalled pattern from training without validation
- [ ] I adapted existing code from file: _______________ lines ___-___
OR
- [ ] I have no documented source, this is unfamiliar

What I observed: [describe what you actually did, not what should work]
```

---

### 2. Documentation Status

**Question:** Has the implementation been validated against official documentation and is project documentation updated?

**Levels:**

- `none` = No documentation exists or was not checked
- `internal` = Inline comments/docstrings added to code only
- `validated` = Official API/library docs checked via tool, parameters/APIs confirmed correct
- `complete` = README updated, citations added, mkdocs regenerated (if applicable), inline docs present

**Your Assessment:**

```text
Level: [choose one above]

Evidence:
- [ ] I searched official docs for APIs/functions used: [list them]
- [ ] I verified parameter names match docs in file: _______________
- [ ] I verified function signatures match docs in file: _______________
- [ ] I added inline docstrings to: [list files and functions]
- [ ] I updated README.md with new functionality (show diff or changes made)
- [ ] I regenerated mkdocs site via Bash command: [show command + output]
OR
- [ ] No documentation was checked
- [ ] Documentation exists but I did not validate against it

What I observed: [what docs did you actually read/update?]
```

---

### 3. Testing Coverage

**Question:** What tests exist and have you ACTUALLY RUN THEM to verify they PASS?

**Levels:**

- `none` = No tests exist for this functionality
- `mocked` = Mocked unit tests created, dependencies stubbed/mocked
- `unit` = Real unit tests exist and PASS (no mocks for core logic)
- `integration` = Unit + integration tests exist and PASS (multiple components interact)
- `e2e` = Unit + integration + end-to-end tests in realistic scenarios, all PASS

**Your Assessment:**

```text
Level: [choose one above]

Evidence - You MUST run tests and show output:
- [ ] I created test file: _______________
- [ ] I RAN tests via Bash: [exact command]
- [ ] Test output shows: ___ passed, ___ failed
- [ ] All tests PASSED (not "should pass" - ACTUALLY PASSED)
- [ ] Tests cover realistic usage scenarios: [describe scenarios]
- [ ] I used Read tool to verify test file content at lines ___-___
OR
- [ ] Tests exist but I have NOT run them
- [ ] Tests exist but FAILED: [show failure output]
- [ ] No tests exist yet

Test execution evidence:
[Paste actual Bash output from test run, or state "NOT RUN"]

What I observed: [what actually happened when tests ran?]
```

---

### 4. Static Analysis

**Question:** Have you run linting, formatting, type checking tools and do they pass WITHOUT warnings?

**Levels:**

- `not_run` = Linting/formatting/type checking not performed
- `warnings` = Ran but produced warnings or errors
- `clean` = ALL static analysis passes without warnings or errors

**Your Assessment:**

```text
Level: [choose one above]

Evidence - You MUST actually run these tools:
- [ ] I ran linting via: [exact command]
- [ ] Output: [paste output or state "no issues found"]
- [ ] I ran formatting via: [exact command]
- [ ] Output: [paste output or state "no changes needed"]
- [ ] I ran type checking via: [exact command]
- [ ] Output: [paste output or state "no errors"]
- [ ] Exit codes: linting=___, formatting=___, type checking=___
OR
- [ ] Static analysis tools NOT run
- [ ] Static analysis produced warnings: [show them]

Static analysis execution evidence:
[Paste actual Bash output, or state "NOT RUN"]

What I observed: [what actually happened when tools ran?]
```

---

### 5. CI/CD Validation

**Question:** Has the CI/CD pipeline been executed and did ALL steps complete successfully?

**Levels:**

- `not_run` = CI/CD pipeline not executed
- `local` = Tested locally with simulation tool (e.g., gitlab-ci-local, act)
- `partial` = Some pipeline steps completed, some skipped or failed
- `full` = Full pipeline executed, all steps passed, all artifacts created

**Your Assessment:**

```text
Level: [choose one above]

Evidence - You MUST show pipeline execution:
- [ ] I ran CI/CD locally via: [exact command]
- [ ] Pipeline output saved to: [file path]
- [ ] All stages completed: [list stages and status]
- [ ] All artifacts created: [list artifacts and paths]
- [ ] Exit code: ___
OR
- [ ] CI/CD pipeline NOT executed
- [ ] Pipeline failed at stage: _______________ [show error]

Pipeline execution evidence:
[Paste relevant Bash output, or state "NOT RUN"]

What I observed: [what actually happened when pipeline ran?]
```

---

## Overall Confidence Summary

Based on the evidence above, answer these questions:

### Reality Check Questions

**Answer HONESTLY:**

1. **Can a user run this code RIGHT NOW without modifications?**

   - [ ] Yes, I verified via execution
   - [ ] No, it needs: **\*\***\_\_\_**\*\***
   - [ ] I don't know, I didn't test execution

2. **If this fails in production, do I have evidence of WHY it should work?**

   - [ ] Yes, I have test results, docs, validation
   - [ ] No, I'm relying on "it should work"
   - [ ] Partially, I have some evidence

3. **Did I actually USE the tools (Bash/Read/Ref) to gather evidence, or am I assuming?**

   - [ ] I used tools and cited results above
   - [ ] I made assumptions without tool verification

4. **What would break if I'm wrong?**

   - [Describe realistic failure modes]

5. **What is the WEAKEST dimension in my assessment?**
   - [Identify which dimension has least evidence]

---

## Final Confidence Statement

**Based on observable evidence only:**

```text
I am [not confident / somewhat confident / confident / highly confident] in this implementation.

Strongest evidence:
- [What you KNOW works based on actual verification]

Weakest evidence:
- [What you have NOT verified or only assumed]

Recommended next steps before declaring "done":
- [ ] [List specific verification actions needed]
- [ ] [List documentation gaps to fill]
- [ ] [List tests to run or create]

User should be aware:
- [Any caveats, assumptions, or unverified aspects]
```
