---
name: uv-mcp
description: UV command automation and project lifecycle management patterns powered by the uv-mcp server
license: MIT
compatibility: opencode
metadata:
  related_python_guidelines: For general Python development standards
  related_python_cli: For CLI scaffolding patterns
  related_mcp_servers: For MCP integration best practices
---

# UV MCP

## What I Do

Describe how to steer the uv-mcp server so natural language requests become precise `uv` workflows. This skill focuses on diagnosing environments, managing dependencies, controlling Python runtimes, and building artifacts with uv while keeping the workspace healthy.

## Core Workflows

### Environment Health & Setup

| Intent | Tool | What Happens |
| --- | --- | --- |
| Diagnose failures or missing environments | `diagnose_environment` | Confirms `pyproject.toml`, virtualenv presence, lock sync status, and reports remediation steps. |
| Repair broken setups | `repair_environment` | Creates `.venv`, installs Python, and syncs dependencies automatically. |
| Verify/install uv itself | `check_uv_installation`, `install_uv` | Checks uv availability and returns platform-specific install steps when missing. |

```text
> "Diagnose the environment"
# Use output to confirm pyproject + venv state
> "Repair the environment"
# Follow-up diagnostics ensure issues are resolved
```

### Dependency Management

| Scenario | Tool | Notes |
| --- | --- | --- |
| Add/remove libraries | `add_dependency`, `remove_dependency` | Supports `--dev`, optional dependency groups, and updates both config + env. |
| Keep env aligned with `uv.lock` | `sync_environment` | Syncs or upgrades locked versions; run after lockfile updates. |
| Inspect or refresh packages | `check_outdated_packages`, `show_package_info` | Surfaces available upgrades and in-depth metadata for any package. |

### Project Inspection

- `list_dependencies`: Lists installed packages; request `tree` mode for transitive view.
- `analyze_dependency_tree`: Visualizes dependency graph depth to spot heavy branches before refactors.

### Runtime Management

| Action | Tool | Guidance |
| --- | --- | --- |
| List installed interpreters | `list_python_versions` | Shows versions uv already manages. |
| Install new interpreter | `install_python_version` | Downloads and activates the requested Python release. |
| Pin project runtime | `pin_python_version` | Updates `.python-version` to keep CI/CD aligned. |

### Project Lifecycle

- `init_project`: Scaffold a fresh uv-enabled project, ideal for greenfield work.
- `export_requirements`: Emit `requirements.txt` for platforms that expect pip-compatible manifests.

### Build & Distribution (uv ≥ 0.6.4)

| Need | Tool | Tips |
| --- | --- | --- |
| Create wheels/sdists | `build_project` | Choose wheel-only or sdist-only, customize output dir, capture artifact paths. |
| Refresh lockfile without installing | `lock_project` | Useful after manual `pyproject.toml` edits or before committing dependency changes. |
| Clear uv cache | `clear_cache` | Fixes checksum mismatches or frees disk space; target entire cache or a single package. |

### Diagnostic Workflow Template

1. `diagnose_environment`
2. Review reported issues.
3. `repair_environment`
4. `diagnose_environment` again.
5. If still broken: `clear_cache` → `lock_project` → `sync_environment`.

## Error Handling & Troubleshooting

- uv-mcp returns structured errors (`error`, `error_code`, `suggestion`). Echo them in summaries so humans know the auto-remediation path.
- Common scenarios:
  - **UV not installed** → run `install_uv`.
  - **Missing packages** → `sync_environment`.
  - **Version conflicts** → `clear_cache` then `lock_project` and `sync_environment`.
  - **Corrupted artifacts** → `clear_cache` for that package and re-sync.

## When to Use Me

- Onboarding or repairing uv-based projects without manual shell work.
- Automating dependency chores (install, remove, upgrade) through MCP.
- Managing Python runtimes inside CI/CD or multi-OS fleets.
- Preparing releases: lockfiles, builds, `requirements.txt` exports.

## Best Practices

1. **Diagnose before repair**: Always capture the initial state so changes are auditable.
2. **Sync after mutations**: Any `add_dependency` / `lock_project` call should be followed by `sync_environment` to keep `.venv` aligned.
3. **Pin intentionally**: Use `pin_python_version` once a runtime is validated by CI.
4. **Cache hygiene**: Run `clear_cache` when checksum or corruption errors show up, then re-sync immediately.
5. **Capture artifacts**: After `build_project`, record the returned artifact list (wheel + sdist paths) in release notes.

## Integration Patterns

- **With `python-guidelines`**: Apply linting/testing standards after uv-mcp modifies dependencies.
- **With `python-cli`**: Use `init_project` + dependency adds to scaffold CLIs rapidly.
- **With `mcp-servers`**: Document uv-mcp availability in `.vscode/mcp.json` and keep tool lists lean.

Use this skill whenever the uv-mcp server is the fastest path to maintaining healthy uv environments without leaving the IDE context.
