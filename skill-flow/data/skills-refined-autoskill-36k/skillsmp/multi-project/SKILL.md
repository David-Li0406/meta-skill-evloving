---
name: multi-project
description: Manage multiple AOCyber projects with shared infrastructure - start, stop, and monitor all projects
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: [status|start|stop|configure]
---

# Multi-Project Management

Manage multiple devflow projects that share infrastructure (Traefik, network, certificates).

## Usage

- `/devflow-multi-project status` - Show status of all registered projects
- `/devflow-multi-project start` - Start all registered projects
- `/devflow-multi-project start aocodex` - Start specific project
- `/devflow-multi-project stop` - Stop all projects (keep infrastructure)
- `/devflow-multi-project stop aosentry` - Stop specific project
- `/devflow-multi-project configure /path/to/project` - Add project to shared infrastructure

## Command

$ARGUMENTS (defaults to "status" if not specified)

## Commands

### status

Show unified status of all registered projects and shared infrastructure.

```bash
devflow infra status --json
```

For each registered project, check its status:

```bash
# For each project path from registry
cd <project_path> && docker compose ps --format json
```

Output format:
```
MULTI-PROJECT STATUS
====================

SHARED INFRASTRUCTURE
---------------------
Network:      devflow-proxy [OK]
Traefik:      running (http://localhost:8088)
Certificates: valid

REGISTERED PROJECTS
-------------------
┌───────────┬─────────────────────────┬────────────────────────┬──────────┬──────────┐
│ Project   │ Path                    │ Domains                │ Services │ Status   │
├───────────┼─────────────────────────┼────────────────────────┼──────────┼──────────┤
│ aocodex   │ ~/projects/aocodex      │ aocodex.localhost      │ 4/4      │ running  │
│ aosentry  │ ~/projects/aosentry     │ aosentry.localhost     │ 3/3      │ running  │
│ devflow   │ ~/projects/devflow      │ -                      │ 0/0      │ stopped  │
└───────────┴─────────────────────────┴────────────────────────┴──────────┴──────────┘

QUICK ACTIONS
-------------
• Start all:     /devflow-multi-project start
• Stop all:      /devflow-multi-project stop
• Add project:   /devflow-multi-project configure /path/to/project
```

### start [project]

Start project services. If no project specified, start all registered projects.

**Start all projects:**

```bash
# Ensure infrastructure is running first
devflow infra status --json
# If not running:
devflow infra up
```

For each registered project (in registration order):

```bash
cd <project_path> && docker compose up -d
```

Report startup status for each project.

**Start specific project:**

```bash
cd <project_path> && docker compose up -d
```

### stop [project]

Stop project services. Infrastructure remains running.

**Stop all projects:**

For each registered project:

```bash
cd <project_path> && docker compose stop
```

**Stop specific project:**

```bash
cd <project_path> && docker compose stop
```

Note: To stop infrastructure too, use `devflow infra down`.

### configure <path>

Add a new project to the shared infrastructure.

```bash
# Verify infrastructure is running
devflow infra status --json

# If not running, start it
devflow infra up
```

Configure the project:

```bash
devflow infra configure <path> --dry-run
```

Show what will be changed and ask for confirmation. If approved:

```bash
devflow infra configure <path>
```

Update /etc/hosts if needed:

```bash
devflow infra hosts list --json
# If missing entries:
echo "Run with sudo to update hosts: sudo devflow infra hosts add"
```

## Project Discovery

The project registry is stored in `~/.devflow/projects.json`. Projects are added when:
1. Running `devflow infra configure <path>`
2. Projects track: name, path, domains, compose files, backup location

## Multi-Project Startup Order

Currently, projects start in registration order. Future enhancement could support dependency-based ordering.

If a project depends on another (e.g., AOCodex needs AOSentry's API), manually specify order:

```
/devflow-multi-project start aosentry
/devflow-multi-project start aocodex
```

## Common Workflows

### Morning Startup
```
/devflow-multi-project start
```
Starts infrastructure (if needed) and all registered projects.

### End of Day
```
/devflow-multi-project stop
devflow infra down
```
Stops all projects and infrastructure.

### Add New Project
```
/devflow-multi-project configure ~/projects/new-project
/devflow-multi-project start new-project
```

### Check Everything
```
/devflow-multi-project status
```

## Error Handling

- **Project path not found**: Verify the path exists and contains a docker-compose.yml
- **Infrastructure not running**: Auto-start with `devflow infra up`
- **Compose file not found**: Check project has docker-compose.yml or specify with `--compose`
- **Network conflict**: Project may need to be re-configured after compose changes
