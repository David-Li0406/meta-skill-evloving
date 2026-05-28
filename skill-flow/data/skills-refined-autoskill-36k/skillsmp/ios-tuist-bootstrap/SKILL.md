---
name: ios-tuist-bootstrap
description: Bootstrap a new iOS project using Tuist with mise-managed tooling, pre-commit hooks, SwiftLint/SwiftFormat build scripts, Periphery, buildServer.json generation, and custom Tuist stencils. Use when creating a fresh iOS app or standardizing a new repo to this setup.
---

# iOS Tuist Bootstrap

## Overview

Create a Tuist-generated iOS app with Swift 6.2 concurrency defaults, lint/format automation, pre-commit self-healing hooks, Periphery checks, and a build server config for Swift LSP.

## Workflow

### 1) Collect inputs

Gather:
- Project/app name (used for targets, scheme, and workspace).
- Bundle ID.
- Organization name.
- iOS deployment target.
- Whether SwiftUI or UIKit.

### 2) Initialize the Tuist project

Preferred: use the bootstrap script so `tuist init` always runs.

```bash
uv run python <skill-root>/scripts/bootstrap_tuist_project.py \
  --dest . \
  --repo-name "my-app" \
  --project-name "MyApp" \
  --scheme "MyApp"
```

This runs `mise x tuist@latest -- tuist init` (or `tuist init` if mise is missing), applies the template files (overwriting template-owned files like `.gitignore`), and patches `Project.swift` to add:
- Swift 6.2 + concurrency settings
- SwiftLint/SwiftFormat build scripts
- `fileHeaderTemplate` + `resourceSynthesizers`

If `--repo-name` is provided, the script creates that folder under `--dest` and flattens Tuist’s generated subdirectory so the repo root stays kebab-case.
If Tuist creates a subdirectory (common), the script detects it and applies the template there.

### 3) Apply the project template files (standalone)

If you already ran `tuist init`, copy the template files (mise, pre-commit, stencils, scripts, lint config) using the bundled Python script:

```bash
uv run python <skill-root>/scripts/apply_template.py \
  --dest . \
  --project-name "MyApp" \
  --scheme "MyApp"
```

Notes:
- The script replaces `{{PROJECT_NAME}}`, `{{SCHEME_NAME}}`, and `{{WORKSPACE_NAME}}`.
- Use `--force` to overwrite existing files.
- Template sources live under `assets/template/`.

### 4) Update `Project.swift`

Set Swift 6.2, strict concurrency, default main-actor isolation, and approachable concurrency.
Also add SwiftLint/SwiftFormat build scripts and enable the custom Files stencil.

Reference: `references/project-settings.md`.

Key settings to apply:
- Swift language version: **6.2**
- Strict Concurrency Checking: **Complete**
- Default Actor Isolation: **MainActor**
- Approachable Concurrency: **Yes**

Also set:
- `fileHeaderTemplate: .string("// TODO: Remove this comment")`
- `resourceSynthesizers: .default + [.files(extensions: ["json"])]`
- Build scripts: `Script/swift-format-changed.sh` and `Script/swiftlint.sh`

### 5) Hook up the Files.stencil

Ensure `Tuist/ResourceSynthesizers/Files.stencil` exists in the repo and that `resourceSynthesizers` includes `.files(...)` so Tuist uses the custom stencil (avoids Xcode header boilerplate in generated files).

### 6) Install tooling + hooks

```bash
mise install
mise run pre-commit-install
```

Because this is a static skill, update tool versions right after bootstrapping:

```bash
mise run bump-tools
```

### 7) Generate and verify

```bash
tuist install
tuist generate
Script/build_server_gen.sh
```

Optional:
- `Script/find-unused-code.sh` to run Periphery.
- `mise run pre-commit-run` to lint everything.

## Resources

- `scripts/bootstrap_tuist_project.py`: Runs `tuist init` then applies template files.
- `scripts/apply_template.py`: Copies template files into a repo and replaces placeholders.
- `assets/template/`: Mise config, pre-commit config, SwiftLint/SwiftFormat settings, Periphery config, scripts, and stencils.
- `references/project-settings.md`: Swift 6.2 and build script snippets for `Project.swift`.
