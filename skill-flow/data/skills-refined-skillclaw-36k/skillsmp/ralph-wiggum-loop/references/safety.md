# Safety Considerations

Running AI agents autonomously requires understanding the risks.

## Blast Radius Model

Think in terms of "what's the worst that can happen?"

| Sandbox Level | Blast Radius | Recovery | Use Case |
|---------------|--------------|----------|----------|
| Fresh VM/container | VM only | Delete VM | Overnight unattended |
| Project directory | Project files | `git reset --hard` | Active development |
| Home directory | User files | Backup restore | NOT RECOMMENDED |
| System paths | Entire system | Reinstall | NEVER |

**Rule:** Blast radius ≤ acceptable loss.

## Built-in Safety

gumloop includes these checks:

### Dangerous Path Rejection

Refuses to run in:
- `~` (home directory root)
- `/` (system root)
- `/etc`, `/usr`, `/var`, `/tmp`
- `/bin`, `/sbin`, `/lib`

### Git Requirement

Won't run outside a git repository. Git enables:
- Instant rollback (`git reset --hard`)
- Change visibility (`git diff`)
- Progress tracking (`git log`)

### Choo-Choo Warning

Warns and requires confirmation for `--choo-choo` in home subdirectories.

## Git as Safety Net

Git is your primary recovery mechanism. Use gumloop's built-in recovery command:

```bash
# Discard all uncommitted changes
gumloop --recover

# Undo last 3 commits
gumloop --recover 3
```

Or use git directly:

```bash
# Undo all uncommitted changes
git reset --hard

# Undo last commit
git reset --hard HEAD~1

# Undo last 5 commits
git reset --hard HEAD~5

# See what changed
git diff HEAD~3

# Restore specific file
git checkout HEAD~1 -- path/to/file
```

## External Sandboxing

For true isolation beyond git (overnight runs, untrusted code):

### E2B (e2b.dev)
Cloud sandboxes for AI agents.
```bash
# Agent runs in isolated container
# Your machine never touched
```

### Docker
```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  ubuntu:22.04 \
  gumloop --choo-choo
```

### Dedicated VM
- Use cloud VM (AWS, GCP, etc.)
- Snapshot before running
- Delete if compromised

### Fly Sprites / Modal
Ephemeral cloud environments. Fresh each run.

## Network Considerations

Autonomous agents with network access can:
- Make API calls (billing implications)
- Download dependencies (supply chain risk)
- Publish packages (if credentials present)

**Mitigations:**
- Use read-only API keys where possible
- Remove npm/pypi publish credentials
- Consider network isolation for sensitive work

## Credential Safety

Before running overnight:

```bash
# Check for exposed credentials
git secrets --scan

# Remove if present
unset AWS_SECRET_ACCESS_KEY
unset OPENAI_API_KEY  # Keep only what agent needs
```

**Best practice:** Agent should only have credentials it needs.

## Monitoring Long Runs

For overnight runs:

```bash
# Watch git log
watch -n 60 'git log --oneline -20'

# Monitor iteration count
# (check terminal output)

# Set iteration limit
gumloop --choo-choo 50  # Stop after 50 iterations max
```

## When Things Go Wrong

### Agent in bad loop

```bash
# Ctrl+C to stop
# Then:
git reset --hard HEAD~N  # Undo N bad commits
```

### Corrupted state

```bash
git reset --hard origin/main  # Reset to remote
# or
git checkout -b fresh-start origin/main
```

### Unexpected files created

```bash
git clean -fd  # Remove untracked files
git reset --hard  # Reset tracked files
```

## Risk Assessment Questions

Before running `--choo-choo`:

1. **What's in this directory?** Only project files, or important data?
2. **Do I have backups?** Git remote? Local backup?
3. **What credentials are accessible?** Remove unnecessary ones.
4. **How long will it run?** Set max iterations.
5. **Can I monitor it?** Even occasionally check in.

## Conservative Defaults

gumloop ships conservative:
- Interactive mode by default (no `--choo-choo`)
- Requires explicit `--choo-choo` flag
- Warns in home subdirectories
- Refuses dangerous paths

You must opt into risk.
