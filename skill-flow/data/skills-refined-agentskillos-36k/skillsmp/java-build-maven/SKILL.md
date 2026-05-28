---
name: java-build-maven
description: Standardize a Maven build for Java backend projects (parent POM, plugin management, profiles, enforcer rules, reproducible builds). Use when builds fail, adding modules, or pinning plugin versions.
license: Apache-2.0
compatibility: "Any OS; Maven Wrapper recommended."
metadata:
  version: "0.1.0"
  tags: ["java", "maven", "build", "multi-module", "enforcer"]
---

# Java Build with Maven

## Scope

In scope:

- Create/standardize parent POM and multi-module structure.
- Pin plugin versions via `pluginManagement`.
- Centralize dependency versions via `dependencyManagement` (BOMs allowed).
- Add Maven Enforcer rules for Java/Maven versions and dependency convergence.
- Define profiles for environments (dev/test/prod) if needed.
- Document reproducible build steps.

Out of scope:

- CI pipeline authoring (only provide commands).
- Framework-specific starters unless requested.
- Rewriting code unrelated to build.

## When to use

- Build fails or behaves inconsistently across machines.
- Adding modules; migrating to multi-module reactor.
- Needing strict plugin/dependency version control.
- Security reviews requiring pinned build toolchain behavior.

## Inputs

- Current `pom.xml`(s), module list, publishing requirements.
- Target Java version(s) and runtime constraints.
- Existing profiles and settings (private repos, proxies).

## Procedure

1) Wrapper + baseline
   - Ensure Maven Wrapper exists (`./mvnw`) and is the canonical entrypoint.
   - Ensure `.mvn/` config exists for consistent JVM flags if needed.

2) Reactor structure (multi-module)
   - Create a root `pom.xml` packaging `pom`.
   - Define `<modules>` list.
   - Move shared configuration to parent.

3) Dependency governance
   - Use `<dependencyManagement>` to pin versions.
   - Use BOMs where appropriate.
   - Ensure no module declares arbitrary versions when managed.

4) Plugin governance
   - Pin plugin versions in `<pluginManagement>`.
   - Ensure surefire/failsafe versions are pinned.
   - Keep compiler plugin aligned with target Java version.

5) Enforcer hardening
   - Add Enforcer with rules:
     - RequireMavenVersion
     - RequireJavaVersion
     - DependencyConvergence (or equivalent)
   - Fail fast with actionable messages.

6) Profiles (optional)
   - Use profiles for environment-specific settings only.
   - Avoid profiles that change core dependency graphs unexpectedly.

7) Documentation
   - Update README with canonical commands:
     - `./mvnw -q test`
     - `./mvnw -q -DskipTests package`
     - `./mvnw -q -P<profile> verify` (if profiles exist)

## Outputs

- Parent POM + module POMs standardized.
- Enforcer rules added.
- Reproducible build steps documented.

## DoD

- [ ] Clean checkout builds with `./mvnw -q test`.
- [ ] Modules are listed and build in reactor order.
- [ ] Dependencies and plugins are pinned/governed.
- [ ] Enforcer catches wrong Java/Maven versions early.

## Guardrails

- Do not introduce too many profiles; keep them minimal.
- Do not allow unmanaged dependency versions without explicit reason.
- Do not weaken enforcer rules to “make it pass” without root-cause analysis.

## Failure modes & fixes

- "Different results across machines" → missing wrapper/pinned plugins → add wrapper + pluginManagement.
- "Dependency diamond conflicts" → no convergence checks → add enforcer + dependencyManagement.
- "CI uses wrong Java" → missing RequireJavaVersion → enforce and document.

## References

- See `templates/` for parent/module POM examples and `.mvn/` config.
- See `references/` for profile and plugin governance playbooks.
