# Tigris Snapshots and Forking

This skill helps you implement point-in-time recovery, version control, and isolated bucket copies.

## What It Covers

**Snapshots** capture your entire bucket at a point in time. **Forking** creates instant, isolated copies from snapshots using copy-on-write.

Use cases:

- **Point-in-time recovery** - Restore after accidental deletion or corruption
- **Version control** - Tag meaningful states like releases
- **Reproducibility** - Recreate exact environments for debugging or testing
- **Developer sandboxes** - Test with real production data safely
- **AI agent environments** - Spin up agents with pre-loaded dependencies

## Installation

### Claude Code

```bash
cp -r skills/tigris-snapshots-forking ~/.claude/skills/
```

### claude.ai

Add the `SKILL.md` file to your project knowledge or paste its contents into the conversation.

## Usage

Claude automatically uses this skill for snapshots and forking. Trigger phrases include:

- "Create a snapshot of this bucket"
- "Fork this bucket for testing"
- "Restore from snapshot"
- "Point-in-time recovery"

## Quick Reference

| Operation | Function | Description |
|-----------|----------|-------------|
| Create snapshot | `createSnapshot(name, tag)` | Capture point-in-time bucket state |
| List snapshots | `listSnapshots(name)` | Get all snapshots for a bucket |
| Fork | `createFork(source, target, snapshot)` | Create isolated copy from snapshot |
| Restore | `restoreFromSnapshot(name, snapshot)` | Replace bucket with snapshot state |

## Example

```typescript
import {
  createSnapshot,
  listSnapshots,
  createFork,
  restoreFromSnapshot
} from "@tigrisdata/storage";

// Create a snapshot before deployment
await createSnapshot("production", "v1.0.0");

// Fork for testing
await createFork("production", "dev-test", "v1.0.0");

// List snapshots
const snapshots = await listSnapshots("production");

// Restore if needed
await restoreFromSnapshot("production", "v1.0.0");
```

## Key Concepts

- **Snapshots** are instant and don't copy data - they reference the existing objects
- **Forks** use copy-on-write - only changed objects consume new storage
- **Deletion protection** - Forks can be destroyed without affecting the source bucket
- **Instant operations** - Even for terabytes of data, forks complete in milliseconds

## License

MIT
