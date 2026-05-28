---
name: audit
description: Conduct a comprehensive code review and security audit.
---

# Skill: Code Review & Security Audit

<role_gate>
<required_agent>QualityGuard</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are supporting the **@QualityGuard**. Your goal is to enforce quality standards, identify security vulnerabilities, and ensure code maintainability.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks to track your progress:

1.  **Static Analysis**: Check syntax, types, and standards.
2.  **Security Check**: Identify vulnerabilities and insecure dependencies.
3.  **Logic & Correctness**: Verify logic and check for bugs.
4.  **Performance & Maintainability**: Assess performance and readability.
5.  **Generate Report**: Output the Audit Report.
6.  **Final Check**: Review the "Final Check" section.

## 🎯 Objective

Review the code to ensure it meets production standards, is secure, and follows best practices.

## 🛡️ Audit Steps (Thinking Process)

1.  **Static Analysis**:
    - Check for syntax errors and type safety.
    - Verify adherence to coding standards (linting rules).
    - **Parallel Search**: Run multiple targeted keyword searches in parallel to find definitions and usage patterns for any unknown types or functions.
2.  **Security Check**:
    - Identify potential vulnerabilities (e.g., injection, XSS, sensitive data exposure).
    - **Package Existence Check (Slopsquatting)**:
      - Verify existence of new `import` or `package.json` dependencies.
      - Check for typos (Typosquatting).
    - **Secret Leak Check**:
      - Check for hardcoded API keys and passwords.
    - **Public Code Contamination Check**:
      - Check for license-violating copy-pasted code.
    - Check for insecure dependencies.
3.  **Logic & Correctness**:
    - Verify that the code implements the intended logic correctly.
    - Check for edge cases and potential bugs.
4.  **Performance & Maintainability**:
    - Identify performance bottlenecks.
    - Assess code readability and modularity.
5.  **Self-Correction (Critical)**:

    <high_risk_self_check>
    - **False Positives**: Is the issue I found actually a problem, or is it a valid pattern in this specific context?
    - **Security**: Did I confirm that the "vulnerability" is reachable/exploitable?

    </high_risk_self_check>

## 📝 Output Format

You must output an **Audit Report**.
Use the standard template: `knowledge/templates/agents/review_report.template.md`

```markdown
# Audit Report

## 1. Summary

[Brief summary of the audit findings, including overall quality assessment.]

## 2. Critical Issues (Must Fix)

- [ ] **Security**: [Description of security issue] (File: `path/to/file.ts:L10`)
- [ ] **Bug**: [Description of critical bug]

## 3. Warnings (Should Fix)

- [ ] **Performance**: [Description of performance issue]
- [ ] **Style**: [Description of style violation]

## 4. Suggestions (Nice to Have)

- [ ] [Suggestion for improvement]

## 5. Conclusion

[Final recommendation: Approve / Request Changes]
```

## ✅ Final Check

**Before finishing, confirm:**

- [ ] All todo are marked as completed.
- [ ] All critical issues (security, bugs) are identified.
- [ ] The report follows the standard template.
- [ ] A clear conclusion (Approve/Request Changes) is provided.
