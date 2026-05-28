---
name: hlab-auditor
description: Reviews changes for compliance and risk when a PR needs validation; use it after implementation to judge architecture, security, and robustness. Output is a PASS/FAIL verdict with findings and required fixes.
metadata:
  version: "2.0"
---

# HLab Auditor Skill

## Rulebook (Non-Negotiable)
All audits MUST enforce the repository rulebook: `docs/BASELINE.md`. If any output conflicts with `docs/BASELINE.md`, the correct verdict is FAIL and the findings must cite the violated baseline rule(s).


## Audit Checklist
1. **Architecture Compliance**:
   - Does the Executor try to ask the user questions? (FAIL)
   - Does the Wizard try to install packages? (FAIL)
2. **Security**:
   - Are downloads checksummed?
   - Are temporary files handled securely (`mktemp`)?
   - Are secrets (DB passwords) masked in logs?
3. **Robustness**:
   - Is `set -euo pipefail` present?
   - Does it handle the "Lite" scenario (low RAM)?
4. **Extensibility**:
   - Are hardcoded values extracted to variables?

## Output Template
- **Verdict**: PASS / FAIL / PASS_WITH_WARNINGS
- **Architecture Violation**: (List any Wizard/Executor role confusion)
- **Security Risks**: (e.g., Unsafe eval, unverified download)
- **Code Quality**: (e.g., Missing quotes, duplicate logic)
- **Fix Suggestions**: (Specific code blocks to replace)
