---
name: sdist-unix-socket-handling
description: Guide to understanding and handling UNIX socket files in source distributions, including prevention strategies and troubleshooting socket-related build issues
---

# UNIX Socket Handling in Sdist

Understand how Hatchling's sdist builder handles UNIX socket files - special files representing network endpoints for inter-process communication. Since these files cannot be stored in tar archives, Hatchling gracefully skips them during the build process.

## What Are UNIX Sockets?

UNIX sockets have these characteristics:

- **Special Files:** Not regular files or directories
- **IPC Endpoints:** Used for inter-process communication
- **Runtime Created:** Typically created when processes start
- **Temporary:** Usually deleted when processes stop

Examples of UNIX sockets:

```bash
# Docker daemon socket
/var/run/docker.sock

# PostgreSQL socket
/var/run/postgresql/.s.PGSQL.5432

# Custom application socket
/tmp/myapp.sock

# Session socket
/run/user/1000/systemd/private
```

## Why Sockets Can't Be Archived

UNIX sockets have characteristics that make them unsuitable for tar archives:

1. **System Resources:** Represent active system resources, not files
2. **Dynamic:** Created at runtime with transient data
3. **Not Replicable:** Cannot be recreated from stored state
4. **Process-Specific:** Tied to specific process instances
5. **Tar Limitation:** The tar format has no standard way to represent sockets

## Hatchling's Socket Handling

### Graceful Ignoring

When Hatchling encounters UNIX socket files during sdist creation:

```text
Processing files for sdist...
Skipping UNIX socket: /tmp/myapp.sock
Skipping UNIX socket: /var/run/socket.sock
...
SDist created successfully
```

The behavior:

1. **Detection:** Hatchling identifies socket files by examining file type
2. **Skipping:** Sockets are silently skipped (not included in archive)
3. **Continuation:** Build continues successfully
4. **Logging:** May log a message depending on verbosity settings

### Why This Works

UNIX sockets should **never** be:

- **Committed to version control:** Sockets are runtime artifacts
- **Included in distributions:** They can't be restored
- **Packaged in releases:** They belong on target systems only

Therefore, skipping them is the correct behavior.

## Preventing Sockets in Your Repository

### Best Practice: .gitignore

Ensure UNIX sockets are never committed:

```gitignore
# UNIX sockets
*.sock
*.socket
/run/
/var/run/

# Python server sockets
.gunicorn.sock
celery.sock

# Application specific
server.sock
app.socket
```

### Common Socket Locations

```gitignore
# Development server sockets
*.sock

# Database sockets
*.pgsql
*.mysql

# Message queue sockets
*.amqp
*.redis

# Custom application sockets
celery.sock
gunicorn.sock
django.sock
```

## How to Check for Sockets in Your Repository

### List All Sockets

```bash
# Find socket files (type 's')
find . -type s

# In git
git ls-files --others --exclude-standard | grep -E '\.(sock|socket)$'
```

### Verify Sockets Aren't Tracked

```bash
# Check if git ignores socket files
git check-ignore *.sock

# Check repository status
git status

# Sockets should not appear in status
```

## When Sockets Appear in Source Directory

If sockets exist in your source directory (development environment):

### Scenario 1: Development Socket (Normal)

You're running a development server that creates sockets:

```text
my-project/
├── src/
├── run/
│   └── myapp.sock       ← Created by development server
├── pyproject.toml
└── .gitignore
```

**Solution:**

1. Add to `.gitignore`:

   ```gitignore
   run/
   *.sock
   ```

2. Create sockets in ignored directories:

   ```bash
   mkdir -p run
   # Server creates socket in run/ directory
   # Which is ignored by VCS
   ```

3. Hatchling will automatically skip sockets during build

### Scenario 2: Accidental Socket Creation

A process creates sockets unexpectedly:

```bash
# Clean up sockets before building
find . -type s -delete

# Or remove specific directory
rm -rf /tmp/myapp.sock
```

### Scenario 3: Socket in Package Source

If sockets appear in your package source (unusual):

```text
src/
└── mypackage/
    └── some.sock        ← Should not be here
```

**Solution:** Remove from repository, add to `.gitignore`, and never commit.

```bash
git rm src/mypackage/some.sock
echo "*.sock" >> .gitignore
git add .gitignore
git commit -m "Remove socket files and ignore them"
```

## Building with Sockets Present

### Full Build Example

```bash
# Create test socket (for demonstration)
touch /tmp/test.sock

# Build ignores the socket
hatch build -t sdist

# Check archive - no socket present
tar -tzf dist/my-package-1.0.0.tar.gz | grep -i socket

# No output - socket correctly excluded
```

### Verification

```bash
# Extract sdist
tar -xzf dist/my-package-1.0.0.tar.gz

# List all files
find my-package-1.0.0 -type s

# No sockets found - confirms they were excluded
```

## Troubleshooting

### Socket Files Appearing in Sdist (Rare)

If socket files somehow appear in the sdist:

1. **Check Hatchling version:**

   ```bash
   pip show hatchling | grep Version
   # Should be >= 1.2.0 for reliable socket handling
   ```

2. **Update if needed:**

   ```bash
   pip install --upgrade hatchling
   ```

3. **Clean and rebuild:**
   ```bash
   rm -rf dist build
   # Remove any socket files
   find . -type s -delete
   # Rebuild
   hatch build -t sdist
   ```

### Socket Paths in Error Messages

If you see socket errors during build:

```text
Warning: Encountered UNIX socket at /path/to/socket
```

This is **normal and expected**. The warning indicates:

1. A socket was found
2. It was correctly identified as a socket
3. It was safely skipped

No action needed - the build succeeded.

### Sockets Breaking Installation from Sdist

If installing from sdist fails with socket-related errors:

1. **Extract and verify:**

   ```bash
   tar -tzf dist/my-package-1.0.0.tar.gz | grep -i socket
   # Should return no results
   ```

2. **Check if sockets are in your VCS:**

   ```bash
   git ls-files | grep socket
   # Should return no results
   ```

3. **Check file types:**
   ```bash
   file $(git ls-files | head -10)
   # All should be regular files, not sockets
   ```

## Development Best Practices

### Project Structure

Organize directories to keep sockets separate:

```text
my-project/
├── src/
│   └── mypackage/
├── tests/
├── .gitignore
├── pyproject.toml
├── run/                 # Sockets and runtime files
│   └── .gitkeep
└── tmp/                 # Temporary files
    └── .gitkeep
```

Contents of `.gitignore`:

```gitignore
# Runtime directories
run/
tmp/
var/

# Socket files (defensive)
*.sock
*.socket
```

Contents of `.gitkeep` (empty file to track directory):

```text
# .gitkeep keeps empty directories in git
# Without it, git doesn't track empty directories
```

### Development vs. Distribution

**Development environment** may have sockets:

```bash
# Developer runs this
python -m mypackage.server

# Creates: run/myapp.sock
# Git ignores this
# No impact on distribution
```

**Distribution** never has sockets:

```bash
# User installs from PyPI
pip install mypackage

# No sockets - they're not in the sdist
# Sockets are created when user runs the application
```

## See Also

- [UNIX Domain Sockets](https://en.wikipedia.org/wiki/Unix_domain_socket)
- [Python Unix Sockets Documentation](https://docs.python.org/3/library/socket.html#socket.AF_UNIX)
- [Tar Format Limitations](https://www.gnu.org/software/tar/manual/)
- [.gitignore Documentation](https://git-scm.com/docs/gitignore)
