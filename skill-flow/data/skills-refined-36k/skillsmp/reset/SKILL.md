---
name: reset
description: Safely reset development environment with confirmation and data preservation options
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: [--soft|--hard|--nuclear]
---

# Environment Reset

Safely reset the local development environment with varying levels of destruction.

## Usage

- `/devflow-reset` - Interactive mode, ask what to reset
- `/devflow-reset --soft` - Stop services, keep data
- `/devflow-reset --hard` - Remove containers, keep volumes
- `/devflow-reset --nuclear` - Remove everything including volumes (DATA LOSS)

## Reset Levels

### Soft Reset (--soft)
- Stops all running services
- Keeps containers, volumes, and data intact
- Fastest way to free resources
- Safe, no data loss

### Hard Reset (--hard)
- Stops and removes all containers
- Keeps volumes (database data preserved)
- Removes orphaned containers
- Rebuilds will use fresh containers

### Nuclear Reset (--nuclear)
- Removes containers AND volumes
- **DESTROYS ALL DATABASE DATA**
- Removes networks
- Complete clean slate
- Requires explicit confirmation

## Arguments

$ARGUMENTS

## Reset Workflow

### Step 1: Show Current State

Before any destructive action, show what exists:

```bash
docker compose ps
docker volume ls --filter name=<project>
```

Display:
- Running services
- Stopped containers
- Volumes and their sizes
- Networks

### Step 2: Confirm Reset Level

If no argument provided, ask user:

```
What level of reset do you want?

1. Soft  - Stop services (keep everything)
2. Hard  - Remove containers (keep data)
3. Nuclear - Remove EVERYTHING (data loss!)

Choose [1/2/3]:
```

### Step 3: Execute Reset

**Soft Reset:**
```bash
devflow dev stop
# or
docker compose stop
```

**Hard Reset:**
```bash
docker compose down --remove-orphans
```

**Nuclear Reset:**

First, require explicit confirmation:
```
WARNING: This will DELETE ALL DATA including:
- Database contents
- Redis cache
- Uploaded files
- Any other persisted data

Type 'DELETE ALL DATA' to confirm:
```

If confirmed:
```bash
docker compose down --volumes --remove-orphans

# Also clean up devflow infrastructure if requested
devflow infra down --volumes --network
```

### Step 4: Clean Up Orphans

Remove any dangling resources:

```bash
# Remove unused networks
docker network prune -f

# Remove dangling volumes (only in nuclear mode)
docker volume prune -f

# Remove dangling images (optional, save space)
docker image prune -f
```

### Step 5: Verify Clean State

```bash
docker compose ps
docker volume ls --filter name=<project>
```

Show what remains.

### Step 6: Next Steps

After reset, show what to do next:

**After Soft Reset:**
```
Services stopped. To restart:
  devflow dev start
```

**After Hard Reset:**
```
Containers removed. To rebuild and start:
  devflow dev start

Your data is preserved in volumes.
```

**After Nuclear Reset:**
```
Environment completely reset. To set up from scratch:
  devflow infra up
  devflow dev start
  devflow db migrate --env local

Note: You will need to re-seed any test data.
```

## Safety Checks

Before nuclear reset, check for:

1. **Uncommitted migrations**: Warn if there are local migration files not in git
2. **Unique data**: Check if volumes contain data that can't be recreated
3. **Running processes**: Ensure no active connections to databases

```bash
# Check for uncommitted files
git status --porcelain migrations/

# Check volume sizes (large = more data to lose)
docker system df -v
```

## Recovery Options

If user accidentally runs nuclear reset:

1. **Database**: If using Supabase, data may be recoverable from cloud
2. **Migrations**: Should be in git, re-run `devflow db migrate`
3. **Seed data**: Re-run seed scripts if available
4. **Uploads**: Lost unless backed up externally

## Common Use Cases

| Scenario | Recommended Reset |
|----------|------------------|
| Free up memory/CPU | Soft |
| Fix weird container state | Hard |
| Compose file changed significantly | Hard |
| Database schema totally broken | Nuclear |
| Starting fresh on a project | Nuclear |
| Switching branches with incompatible migrations | Nuclear |

## Partial Reset

For resetting specific components:

**Reset single service:**
```bash
docker compose rm -sf <service>
docker compose up -d <service>
```

**Reset database only:**
```bash
docker compose rm -sf postgres
docker volume rm <project>_postgres_data
docker compose up -d postgres
devflow db migrate --env local
```

**Reset Redis cache:**
```bash
docker compose exec redis redis-cli FLUSHALL
```
