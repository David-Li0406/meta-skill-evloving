---
name: java-repo-bootstrap
description: Standardize repository layout, module boundaries, naming conventions, and baseline docs for Java backend projects. Use when starting a new project, restructuring an existing repo, or migrating to a mono-repo.
license: Apache-2.0
compatibility: "Any OS; Git required; Java projects (framework-agnostic)."
metadata:
  version: "0.1.0"
  tags: ["java", "backend", "repo-layout", "architecture", "docs"]
---

# Java Repo Bootstrap

## Scope

In scope:

- Propose and apply a repository layout (mono-repo or multi-module).
- Define module boundaries and dependency direction (allowed imports, ownership).
- Standardize naming conventions (modules, packages, docs).
- Add baseline documentation: README, CONTRIBUTING, ADR template, architecture notes.
- Add minimal CI entrypoints (scripts/commands) but do NOT implement a full CI system.

Out of scope:

- Framework-specific scaffolding (Spring/Quarkus/Micronaut) beyond optional examples.
- Deep refactors across many packages without a phased plan.
- Changing external API contracts unless explicitly requested.

## When to use

- Starting a new Java backend codebase.
- Refactoring repo structure (messy src/, unclear modules).
- Converting to mono-repo or multi-module.
- Onboarding a new team and needing consistent conventions.

## Inputs (required context)

- Current repo tree (top-level files + modules).
- Build tool status: Gradle/Maven/Other (or unknown).
- Existing CI constraints (if any): required commands, existing pipelines.
- Public API surfaces (if any): REST endpoints, libraries, shared modules.

## Procedure (plan-first, small diffs)

1) Discovery
   - Enumerate current top-level layout and key modules.
   - Identify build entrypoints (gradlew/mvnw, build files).
   - Identify public surfaces (API modules, docs, published artifacts).

2) Choose a target layout (justify with trade-offs)
   - Option A: Single service repo (single module).
   - Option B: Multi-module repo (domain/application/infra or feature modules).
   - Option C: Mono-repo with multiple services + shared libraries.
   Provide a file impact map and a migration strategy if restructuring.

3) Define module boundaries + dependency rules
   - Define allowed dependency direction (e.g., domain <- application <- infra).
   - Define shared modules policy (who can depend on what).
   - Define package naming conventions and "no cycles" guardrails.

4) Apply structure using git-safe moves
   - Use `git mv` for moves.
   - Update imports and build configs incrementally.
   - Ensure each commit builds.

5) Add baseline docs (templates allowed)
   - README: purpose, how to build/test/run, local dev, troubleshooting.
   - CONTRIBUTING: branch strategy, code style, tests required, commit guidelines.
   - ADR: add template + index.
   - Architecture notes: a minimal C4-style overview (context/container).

6) Verify (Definition of Done)
   - Repo tree matches target layout.
   - Build commands are documented and reproducible.
   - Minimal docs exist and are discoverable.

## Outputs / Artifacts

- Updated folder layout + module boundaries documented.
- `README.md`, `CONTRIBUTING.md`, `docs/architecture/`, `docs/adr/` (or similar).
- A short "Repo Conventions" section with:
  - module naming
  - package naming
  - dependency rules
  - how to run build/tests

## Definition of Done (DoD)

- [ ] Repo builds locally using a documented command.
- [ ] Tests run using a documented command (even if minimal).
- [ ] Docs added: README + ADR template + architecture overview.
- [ ] No broken imports; compilation succeeds.
- [ ] Module dependencies are acyclic (or explicitly justified).

## Guardrails (What NOT to do)

- Do not perform a big-bang rewrite. Use phased migration.
- Do not rename public APIs without an explicit migration plan.
- Do not move files without `git mv` unless unavoidable.
- Do not invent architecture rules that contradict existing constraints.

## Common failure modes & fixes

- Symptom: "Everything depends on everything"
  - Cause: missing dependency direction
  - Fix: introduce domain/core module and enforce one-way dependencies.
- Symptom: "CI breaks after moves"
  - Cause: scripts/paths hardcoded
  - Fix: update build entrypoints + document canonical commands.
- Symptom: "Endless bikeshedding on layout"
  - Fix: pick a default layout and codify in docs; revisit via ADR later.

## References

- See `templates/` for README/ADR/Contributing stubs.
- See `references/` for deeper layout and module-boundary guidelines.
