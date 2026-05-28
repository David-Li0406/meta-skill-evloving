---
name: java-dependency-audit
description: Audit Java dependencies for vulnerabilities, licenses, duplicates, and version conflicts; produce an upgrade plan with pinned versions and risk notes. Use during security review, CVE response, or upgrade sprints.
license: Apache-2.0
compatibility: "Any OS; supports Gradle or Maven projects."
metadata:
  version: "0.1.0"
  tags: ["java", "security", "dependencies", "sca", "sbom", "cve"]
---

# Java Dependency Audit

## Scope

In scope:

- Dependency inventory (direct + transitive).
- Vulnerability scanning and report generation.
- Version conflicts/duplicates analysis.
- License metadata collection (best-effort; depends on tool support).
- Produce an actionable upgrade plan:
  - what to upgrade
  - why (CVE/severity/exposure)
  - risk notes and test requirements
  - pinned versions strategy

Out of scope:

- Patching upstream libraries.
- Organization-wide policy decisions (only propose options).
- Major feature refactors unrelated to dependency remediation.

## When to use

- Security review before release.
- CVE response and emergency patching.
- Scheduled upgrade sprint.
- Suspected dependency conflict or "jar hell".

## Inputs

- Build files: `build.gradle(.kts)` or `pom.xml`.
- Dependency repositories constraints (private repo? proxy? air-gapped?).
- Runtime environment constraints (Java version, platform).
- Release risk tolerance (hotfix vs normal release).

## Procedure

1) Inventory
   - Produce dependency graph (direct + transitive).
   - Generate an SBOM (CycloneDX recommended) when possible.

2) Vulnerability scan
   - Run SCA scanning (OWASP Dependency-Check recommended).
   - Capture output in a versioned location (e.g., `reports/security/`).

3) Conflict & duplication analysis
   - Identify dependency convergence issues (multiple versions of same artifact).
   - Identify shaded/relocated dependencies if relevant.

4) Triage (critical step)
   - Prioritize by severity + exploitability + exposure:
     - Is the vulnerable code reachable?
     - Is it in runtime path or test-only?
   - Mark false positives with justification.

5) Upgrade plan
   - Propose minimal safe upgrades first.
   - Prefer upgrading via BOM or centrally managed constraints.
   - Note breaking changes risk and required regression tests.

6) Implementation (small batches)
   - Upgrade highest-risk items first.
   - After each batch:
     - run minimal tests
     - then run full checks
   - Update lockfiles/verification metadata if used.

7) Output documentation
   - Produce `upgrade-plan.md` with:
     - summary
     - prioritized items
     - changes made
     - remaining risks
     - follow-ups

## Outputs / Artifacts

- SBOM file(s) (JSON/XML) if supported by build tool.
- Vulnerability scan report(s).
- `upgrade-plan.md` and pinned versions changes.
- Notes on false positives and mitigations.

## DoD

- [ ] Vulnerability report generated and stored.
- [ ] SBOM generated (preferred) or dependency graph captured.
- [ ] Upgrade plan produced with priorities and risks.
- [ ] Upgraded dependencies verified by tests.
- [ ] Remaining risks are documented (not silently ignored).

## Guardrails

- Do not blindly bump everything. Prioritize minimal safe changes.
- Do not “suppress” findings without justification and tracking.
- Do not remove transitive deps by exclusions unless you confirm runtime behavior.
- Require explicit confirmation before major-version upgrades in critical libraries.

## Common failure modes & fixes

- False positives from CPE matching → add justification + consider alternative identification.
- Massive breaking changes → split upgrades into batches and add regression tests.
- Conflicts after upgrades → centralize constraints or use dependency convergence checks.

## References

- Use scripts in `scripts/` to run scanners and generate SBOM.
- Use templates in `templates/` to write upgrade plans and triage notes.
