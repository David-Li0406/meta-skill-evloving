<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Monorepo Ownership Analysis

## Overview

Zero's code ownership scanner automatically detects monorepos and provides per-workspace ownership analysis. This enables accurate ownership tracking in large codebases with multiple projects, packages, or services.

## Supported Monorepo Types

### JavaScript/TypeScript

| Type | Detection File | Workspace Definition |
|------|---------------|---------------------|
| **Turborepo** | `turbo.json` | `package.json` workspaces |
| **Lerna** | `lerna.json` | `packages` array in config |
| **pnpm** | `pnpm-workspace.yaml` | `packages` array in config |
| **npm/Yarn** | `package.json` | `workspaces` field |
| **Nx** | `nx.json` | `project.json` files |

### Other Languages

| Type | Detection File | Workspace Definition |
|------|---------------|---------------------|
| **Cargo (Rust)** | `Cargo.toml` | `[workspace].members` |
| **Go Modules** | `go.work` | `use` directives |
| **Go Multi-module** | Multiple `go.mod` | Each directory with `go.mod` |

## Detection Logic

### Turborepo
```
if exists("turbo.json"):
    workspaces = parse_package_json_workspaces()
    return MonorepoAnalysis(type="turborepo", workspaces=workspaces)
```

### Lerna
```
if exists("lerna.json"):
    config = parse_json("lerna.json")
    workspaces = config.packages || ["packages/*"]
    return MonorepoAnalysis(type="lerna", workspaces=workspaces)
```

### pnpm
```
if exists("pnpm-workspace.yaml"):
    config = parse_yaml("pnpm-workspace.yaml")
    workspaces = config.packages
    return MonorepoAnalysis(type="pnpm", workspaces=workspaces)
```

### Cargo
```
if exists("Cargo.toml") and contains("[workspace]"):
    members = parse_workspace_members()
    return MonorepoAnalysis(type="cargo", workspaces=members)
```

### Go
```
if exists("go.work"):
    uses = parse_go_work_use_directives()
    return MonorepoAnalysis(type="go", workspaces=uses)
elif count(find("go.mod")) > 1:
    modules = find_all_go_mod_directories()
    return MonorepoAnalysis(type="go", workspaces=modules)
```

## Per-Workspace Metrics

For each workspace, Zero calculates:

### Ownership Metrics
- **Top Contributors**: Ranked by enhanced ownership score
- **Bus Factor**: Per-workspace knowledge concentration
- **Languages Used**: Programming languages in workspace

### CODEOWNERS Integration
- **Has Own CODEOWNERS**: Whether workspace has dedicated owners
- **Inherited Owners**: Owners from parent CODEOWNERS rules

## Output Format

```json
{
  "monorepo": {
    "is_monorepo": true,
    "type": "turborepo",
    "config_file": "turbo.json",
    "workspaces": [
      {
        "name": "web-app",
        "path": "apps/web",
        "top_contributors": [...],
        "bus_factor": 3,
        "bus_factor_risk": "healthy",
        "languages_used": ["TypeScript", "CSS"],
        "has_own_codeowners": false
      },
      {
        "name": "api",
        "path": "apps/api",
        "top_contributors": [...],
        "bus_factor": 2,
        "bus_factor_risk": "warning",
        "languages_used": ["TypeScript"],
        "has_own_codeowners": true
      },
      {
        "name": "shared-ui",
        "path": "packages/ui",
        "top_contributors": [...],
        "bus_factor": 1,
        "bus_factor_risk": "critical",
        "languages_used": ["TypeScript", "CSS"],
        "has_own_codeowners": false
      }
    ],
    "cross_workspace_owners": ["alice@example.com", "bob@example.com"]
  }
}
```

## Cross-Workspace Owners

Zero identifies developers who contribute across multiple workspaces:

```
cross_workspace_owners = [
  email for email, workspaces in contributor_workspaces.items()
  if len(workspaces) >= 2
]
```

These individuals are valuable for:
- **Architecture decisions**: Understanding system-wide impact
- **Breaking changes**: Knowing what might break downstream
- **Integration testing**: Experience with workspace interactions
- **Code sharing**: Understanding shared library usage

## Configuration

```json
{
  "monorepo": {
    "enabled": true,
    "auto_detect": true
  }
}
```

- `enabled`: Enable monorepo detection
- `auto_detect`: Automatically detect monorepo type (vs. manual specification)

## Best Practices

### 1. CODEOWNERS Per Workspace
For large monorepos, consider workspace-level CODEOWNERS:

```
# Root CODEOWNERS
* @platform-team

# Workspace-specific (override)
/apps/web/** @web-team
/apps/api/** @api-team
/packages/ui/** @design-system-team
```

### 2. Monitor Workspace Bus Factor
Critical workspaces should have bus factor >= 2:

| Risk Level | Action |
|------------|--------|
| Critical (1) | Immediate knowledge transfer |
| Warning (2) | Plan cross-training |
| Healthy (3+) | Maintain documentation |

### 3. Track Cross-Workspace Contributors
These developers are high-value:
- Include in architectural reviews
- Protect from burnout (they're in demand)
- Encourage documentation of cross-cutting concerns

### 4. Workspace-Level Incident Contacts
Generate contacts per workspace for targeted incident response:

```json
{
  "workspace": "apps/api",
  "primary_contact": "api-lead@example.com",
  "backup_contact": "backend-team@example.com"
}
```

### 5. Detect Workspace Isolation
If no one works across workspaces, consider:
- Whether integration is being tested
- Whether architectural knowledge is siloed
- Whether shared libraries are being maintained

## Common Patterns

### Turborepo with Apps and Packages
```
repo/
├── turbo.json
├── package.json (workspaces: ["apps/*", "packages/*"])
├── apps/
│   ├── web/
│   └── api/
└── packages/
    ├── ui/
    └── utils/
```

### Lerna Legacy
```
repo/
├── lerna.json (packages: ["packages/*"])
├── package.json
└── packages/
    ├── core/
    ├── cli/
    └── shared/
```

### Go Workspace
```
repo/
├── go.work
├── cmd/
│   └── myapp/
│       └── go.mod
├── pkg/
│   └── mylib/
│       └── go.mod
└── internal/
    └── shared/
        └── go.mod
```

### Cargo Workspace
```
repo/
├── Cargo.toml (workspace.members = ["crates/*"])
└── crates/
    ├── core/
    │   └── Cargo.toml
    ├── cli/
    │   └── Cargo.toml
    └── shared/
        └── Cargo.toml
```

## Limitations

1. **Detection Heuristics**: May not detect custom monorepo setups
2. **Nested Workspaces**: Limited support for deeply nested structures
3. **Virtual Workspaces**: Some patterns (like Yarn 2 PnP) need special handling
4. **Private Registries**: Internal package dependencies not tracked

## Integration with Organization Analysis

When analyzing a GitHub organization:
- Monorepo detection runs per-repository
- Cross-repo specialists may overlap with cross-workspace owners
- Domain expertise aggregates workspace-level data
