# Elara Package Dependency Graph

This document maps the cross-repository npm/Python package dependencies for the Elara ecosystem.

## Repositories

| Repo | Packages | Language |
|------|----------|----------|
| east | @elaraai/east | TypeScript |
| east-node | @elaraai/east-node-std, east-node-io, east-node-cli | TypeScript |
| east-py | east-py, east-py-std, east-py-io, east-py-cli, east-py-datascience | Python |
| east-ui | @elaraai/east-ui, east-ui-components, east-ui-showcase, east-ui-extension | TypeScript |
| e3 | @elaraai/e3, e3-types, e3-core, e3-cli, e3-api-client, e3-api-server | TypeScript |

## Cross-Repository Dependencies

### @elaraai/east (root)
No external @elaraai dependencies.

### east-node packages
| Package | Depends On |
|---------|------------|
| @elaraai/east-node-std | @elaraai/east |
| @elaraai/east-node-io | @elaraai/east, @elaraai/east-node-std |
| @elaraai/east-node-cli | @elaraai/east |

### east-py packages (Python)
| Package | Depends On |
|---------|------------|
| east-py | (none - root) |
| east-py-std | east-py |
| east-py-io | east-py, east-py-std |
| east-py-cli | east-py |
| east-py-datascience | east-py |

### east-ui packages
| Package | Depends On |
|---------|------------|
| @elaraai/east-ui | @elaraai/east |
| @elaraai/east-ui-components | @elaraai/east, @elaraai/east-ui |
| @elaraai/east-ui-showcase | @elaraai/east, @elaraai/east-ui, @elaraai/east-ui-components |
| @elaraai/east-ui-extension | @elaraai/e3-api-server |

### e3 packages
| Package | Depends On |
|---------|------------|
| @elaraai/e3-types | @elaraai/east |
| @elaraai/e3 | @elaraai/east, @elaraai/e3-types |
| @elaraai/e3-core | @elaraai/east, @elaraai/e3, @elaraai/e3-types |
| @elaraai/e3-cli | @elaraai/east, @elaraai/e3, @elaraai/e3-core, @elaraai/e3-types |
| @elaraai/e3-api-client | @elaraai/east, @elaraai/east-node-std, @elaraai/e3-types |
| @elaraai/e3-api-server | @elaraai/east, @elaraai/e3-core, @elaraai/e3-types |

## Dependency Graph (Cross-Repo Only)

```
@elaraai/east (root)
├── east-node repo
│   ├── east-node-std → east
│   ├── east-node-io → east, east-node-std
│   └── east-node-cli → east
│
├── east-ui repo
│   ├── east-ui → east
│   ├── east-ui-components → east, east-ui
│   ├── east-ui-showcase → east, east-ui, east-ui-components
│   └── east-ui-extension → e3-api-server (!)
│
└── e3 repo
    ├── e3-types → east
    ├── e3 → east, e3-types
    ├── e3-core → east, e3, e3-types
    ├── e3-cli → east, e3, e3-core, e3-types
    ├── e3-api-client → east, east-node-std, e3-types
    └── e3-api-server → east, e3-core, e3-types
```

## Publish Order

Based on dependencies, the correct publish order when @elaraai/east is updated:

```
Level 0: @elaraai/east
         ↓
Level 1: east-node (east-node-std, east-node-io, east-node-cli)
         east-py (east-py, east-py-std, east-py-io, east-py-cli, east-py-datascience)
         ↓
Level 2: e3 (e3-types, e3, e3-core, e3-cli, e3-api-client, e3-api-server)
         east-ui (east-ui, east-ui-components, east-ui-showcase)
         ↓
Level 3: east-ui-extension (depends on e3-api-server)
```

## Circular Dependency Warning

`east-ui-extension` depends on `@elaraai/e3-api-server`, which creates a dependency:
- east → e3 → east-ui-extension

This means east-ui-extension cannot be updated until e3 is updated.

## Publish Cascade (Implemented)

Each repo triggers only its direct dependents, creating a cascade:

```
east publishes
  ├── waits for npm propagation (nick-invision/retry@v3)
  └── triggers: east-node, east-py
                    │
                    ▼
east-node publishes
  ├── waits for npm propagation
  └── triggers: e3
                    │
                    ▼
e3 publishes
  ├── waits for npm propagation
  └── triggers: east-ui
                    │
                    ▼
east-ui publishes (end of cascade)
```

### Workflow Files

| Repo | Workflow | Triggers |
|------|----------|----------|
| east | `.github/workflows/publish.yml` | east-node, east-py |
| east-node | `.github/workflows/publish.yml` | e3 |
| e3 | `.github/workflows/publish.yml` | east-ui |
| east-ui | `.github/workflows/publish.yml` | (none) |
| east-py | `.github/workflows/publish.yml` | (none) |

### npm Propagation Wait

All publish workflows use `nick-invision/retry@v3` to wait for npm propagation:

```yaml
- name: Wait for npm propagation
  uses: nick-invision/retry@v3
  with:
    timeout_minutes: 5
    max_attempts: 20
    retry_wait_seconds: 15
    command: npm view "@elaraai/package@version" version
```

## Skill Documentation Publishing

After a publish cascade completes, skill documentation can be synced to east-plugin:

```
Source Repos                          east-plugin
─────────────                         ───────────
east/SKILL.md                    →    skills/east/
east/reference/*                      skills/east/references/

east-node/packages/east-node-std/ →   skills/east-node-std/
east-node/packages/east-node-io/  →   skills/east-node-io/

east-py/packages/east-py-datascience/ → skills/east-py-datascience/

east-ui/SKILL.md                 →    skills/east-ui/
east-ui/reference/*                   skills/east-ui/references/

e3/SKILL.md                      →    skills/e3/
e3/reference/*                        skills/e3/references/
```

### Workflow

| Repo | Workflow | Trigger |
|------|----------|---------|
| east-plugin | `.github/workflows/update-skills.yml` | Manual (workflow_dispatch) |

Run manually after publish cascade completes to sync all skill docs.
