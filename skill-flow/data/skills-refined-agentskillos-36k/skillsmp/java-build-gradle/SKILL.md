---
name: java-build-gradle
description: Set up and harden a Gradle build for Java backend projects (wrapper, multi-module structure, conventions, performance, reproducibility). Use when builds fail, migrating Gradle, adding modules, or speeding up CI/local builds.
license: Apache-2.0
compatibility: "Any OS; Gradle Wrapper recommended."
metadata:
  version: "0.1.0"
  tags: ["java", "gradle", "build", "multi-module", "performance"]
---

# Java Build with Gradle

## Scope

In scope:

- Ensure Gradle Wrapper exists and is the canonical build entrypoint.
- Standardize multi-module build structure (settings + conventions).
- Create baseline tasks: build, test, integrationTest (optional), lint (optional).
- Improve reproducibility and performance with sane defaults.
- Document "how to run" commands.

Out of scope:

- Full CI pipeline authoring (only provide recommended commands).
- Introducing framework-specific plugins unless requested.
- Large refactors unrelated to build correctness/performance.

## When to use

- Build fails locally/CI, dependency conflicts.
- Migrating from Groovy DSL to Kotlin DSL, or Gradle version upgrades.
- Adding a new module/service in a mono-repo.
- Slow builds: want caching/parallelism/conventions.

## Inputs (required context)

- Current Gradle files: `settings.gradle(.kts)`, `build.gradle(.kts)`, `gradle.properties`.
- Current modules list (if multi-module).
- JDK target version(s) and runtime constraints.
- CI constraints: required Java version, offline build needs, proxy, etc.

## Procedure (deterministic steps)

1) Wrapper first (canonical entrypoint)
   - Ensure `./gradlew` exists and is used in docs/CI.
   - If upgrading Gradle, update wrapper scripts and verify wrapper JAR update.

2) Project structure
   - Define modules in `settings.gradle(.kts)` with clear names.
   - Introduce a conventions mechanism:
     - Option A: `build-logic` included build (preferred)
     - Option B: `buildSrc` (acceptable for small repos)

3) Dependency governance
   - Centralize versions via a Version Catalog (`libs.versions.toml`) when appropriate.
   - Enforce consistent dependency versions across modules.
   - Add a process for dependency locking/verification if required by security policy.

4) Java toolchains + compilation
   - Define Java toolchain and language level.
   - Configure tests to use the correct JVM and consistent flags.

5) Test strategy
   - Ensure unit tests run reliably.
   - Optionally add `integrationTest` sourceSet and task.
   - Produce a "minimal tests first" command and a "full checks" command.

6) Performance baseline
   - Configure parallel execution where safe.
   - Enable caching where safe (local; remote optional).
   - Avoid eager configuration; keep configuration cache compatible where possible.

7) Documentation
   - Update README with canonical commands:
     - `./gradlew clean test`
     - `./gradlew build`
     - `./gradlew check` (if defined)

## Outputs / Artifacts

- Wrapper present and documented.
- Updated Gradle build files with conventions and tasks.
- `gradle.properties` tuned for sane defaults.
- README "How to build/test" section.

## Definition of Done (DoD)

- [ ] `./gradlew -v` works locally.
- [ ] `./gradlew clean test` passes on a clean checkout.
- [ ] Multi-module build resolves dependencies consistently.
- [ ] README documents canonical commands and JDK requirements.

## Guardrails

- Do not add experimental plugins without justification.
- Do not enable parallel/caching settings that make builds flaky.
- Do not silently change target Java version; require explicit confirmation.

## Common failure modes & fixes

- "Works on my machine" → missing wrapper/toolchain → enforce wrapper + toolchain.
- Dependency conflict → versions scattered → centralize and add constraints.
- Slow build → too much work in configuration → move to lazy configuration and conventions.

## References

- Use templates in `templates/` for starter Gradle files.
- Use scripts in `scripts/` for CI-friendly commands.
