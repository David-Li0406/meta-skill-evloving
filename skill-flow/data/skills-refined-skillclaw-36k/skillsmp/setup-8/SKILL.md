---
name: setup
description: Initialize and set up local development environment with devflow infrastructure
allowed-tools: Bash, Read, Write
disable-model-invocation: true
argument-hint: [--full|--minimal]
---

# Local Development Setup

Set up a complete local development environment for a devflow-managed project.

## Usage

- `/devflow-setup` - Standard setup (infrastructure + project)
- `/devflow-setup --full` - Full setup including database migrations
- `/devflow-setup --minimal` - Project only, skip shared infrastructure

## Prerequisites Check

First, verify the environment:

```bash
devflow doctor
```

If any tools are missing, inform the user what needs to be installed before proceeding.

## Setup Steps

### Step 1: Verify Configuration

Check that `devflow.yml` exists in the current directory:

```bash
devflow config validate
```

If missing, ask the user which preset to use (aocodex, aosentry, or custom).

### Step 2: Start Shared Infrastructure (unless --minimal)

```bash
devflow infra status --json
```

If infrastructure is not running:

```bash
devflow infra up
```

### Step 3: Configure Project for Shared Infrastructure

Check if project is already configured:

```bash
devflow infra status --json
```

If not registered, configure it:

```bash
devflow infra configure . --dry-run
```

Show the user what changes will be made. If they approve:

```bash
devflow infra configure .
```

### Step 4: Set Up Hosts Entries

```bash
devflow infra hosts list --json
```

If domains are missing, inform user they need to run with sudo:

```bash
sudo devflow infra hosts add
```

### Step 5: Start Project Services

```bash
devflow dev start
```

### Step 6: Apply Local Migrations (if --full)

```bash
devflow db status --env local --json
```

If migrations are pending:

```bash
devflow db migrate --env local
```

### Step 7: Verify Setup

Run a final status check:

```bash
devflow infra status
devflow db status --env local
```

## Output

Provide a summary showing:
- Infrastructure status (Traefik dashboard URL)
- Project domains configured
- Services running
- Database migration state
- Any manual steps remaining (like hosts file if sudo wasn't available)

## Error Handling

- If Docker is not running, instruct user to start Docker Desktop or daemon
- If mkcert CA is not installed, provide installation instructions
- If ports are in use, identify conflicting processes
- If compose file has issues, show specific validation errors
