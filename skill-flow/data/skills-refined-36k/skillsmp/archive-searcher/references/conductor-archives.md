# Conductor Archival Standards
> **Reference for managing and searching archived mission tracks.**

## 1. Archival Structure
In the Conductor system, tracks are promoted from `active` to `archived` to keep the working set small while preserving context.

### Standard Paths:
- `conductor/tracks/`: Active development.
- `conductor/archive/tracks/`: Historical tracks.
- `conductor/archive/specs/`: Legacy product definitions.

## 2. Searching Metadata
Archived tracks always contain a `metadata.json` file. 

### Key Fields for Forensics:
- `track_id`: Unique identifier.
- `status`: Should be `completed`, `abandoned`, or `merged`.
- `created_at` / `archived_at`: The temporal window of the mission.
- `tags`: Keywords for broad search.

### Search Pattern:
```bash
# Find archived tracks tagged with 'security'
grep -l ""tags":.*"security"" conductor/archive/tracks/*/metadata.json
```

## 3. Reconstructing a Mission Timeline
To understand the evolution of a feature, you must link archived tracks.

1. Find the current track.
2. Check `parent_track_id`.
3. Locate the parent in `conductor/archive/`.
4. Repeat until the root mission is found.

## 4. Best Practices
- **Never delete metadata**: Even if the code is gone, the metadata explains *why*.
- **Sync with Git Tags**: When archiving a major track, create a corresponding Git tag `track/<id>/archived`.

---
*Updated: January 22, 2026 - 15:18*
