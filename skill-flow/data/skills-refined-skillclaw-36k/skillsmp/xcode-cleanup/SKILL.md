---
name: xcode-cleanup
description: Clean up Xcode disk space by removing derived data, old simulators, device support files, caches, and archives. Use when the user mentions running low on disk space, Xcode consuming too much storage, cleaning up after development, removing orphaned build artifacts, or freeing up space on Mac. Includes git worktree protection for derived data and confirmation prompts for simulators and devices.
---

# Xcode Cleanup

Reclaim disk space consumed by Xcode build artifacts, caches, simulators, and device support files.

## Important: Device Support vs Simulators

These are **completely different things**:

- **Device Support** = Debug symbols from **PHYSICAL devices** you've plugged into your Mac. Downloaded automatically when you connect an iPhone/iPad/Watch. Used for crash log symbolication.

- **Simulator Runtimes** = iOS/visionOS images you **explicitly downloaded** through Xcode to run in Simulator. These are 5-10GB each.

- **Simulator Devices** = The actual simulator instances (iPhone 16 Pro, etc.) and their app data.

See `references/cleanup-locations.md` for detailed explanations.

## Workflow

Follow these steps in order:

### 1. Show Initial Disk Stats

Run `scripts/disk-stats.sh` to display:
- Current free disk space
- Breakdown of all Xcode-related storage by category

Present results to user before proceeding.

### 2. Analyze Derived Data

Run `scripts/analyze-derived-data.sh` to check each DerivedData folder for:
- **ACTIVE WORKTREE** - Project is part of an active git worktree (protected)
- **PATH EXISTS** - Project path exists but not a worktree (ask before deleting)
- **ORPHANED** - Project path no longer exists (safe to delete)

### 3. Safe Cleanup (no confirmation needed)

Run `scripts/safe-cleanup.sh` to automatically clean:
- Xcode Caches
- Simulator Caches
- SwiftUI Previews
- Module Cache
- Orphaned Derived Data (detected via worktree analysis)

### 4. Confirmable Items (REQUIRES USER APPROVAL)

Run `scripts/list-confirmable.sh` to display all confirmable items with clear explanations, then use AskUserQuestion with multiSelect to let the user choose specific items.

**For Device Support (PHYSICAL devices):**

Create separate questions for iOS/watchOS/tvOS. List ALL versions with sizes. Make clear these are from physical devices:

```
Question: "Which iOS Device Support versions do you want to remove? (These are from physical iPhones/iPads you've connected)"
Header: "iOS Devices"
Options (multiSelect: true):
- "iPad16,3 26.2 (23C55) - 5.4G"
- "iPhone16,1 26.2 (23C55) - 5.3G"
- "iPhone13,1 17.7.1 (21H216) - 3.7G"
- etc. (include ALL versions found by the script)
```

**For Simulator Runtimes (downloaded OS images):**

List each runtime with its build number. Highlight duplicate versions (beta builds):

```
Question: "Which Simulator Runtimes do you want to remove? (These are OS images you downloaded for Simulator)"
Header: "Sim Runtimes"
Options (multiSelect: true):
- "iOS 26.0 (23A5297i) - beta"
- "iOS 26.0 (23A343) - release"
- "iOS 18.6 (22G86)"
- etc.
```

**For Archives:**

List each date with size:

```
Question: "Which Archives do you want to remove? (These are your App Store/distribution builds)"
Header: "Archives"
Options (multiSelect: true):
- "2025-09-12 - 550M"
- "2025-11-05 - 284M"
- etc.
```

After user selects items, run `scripts/remove-selected.sh` with the selections:

```bash
scripts/remove-selected.sh \
  --ios-device-support "iPhone16,1 26.1 (23B85)" "iPad16,3 26.1 (23B85)" \
  --ios-runtime "6EB69496-B03A-476A-A1BF-5B9C329FA732" \
  --visionos-runtime "07E155BF-35E2-498F-A87C-420327BD9B06" \
  --archives "2025-09-12" "2025-11-05"
```

Use `--dry-run` flag to preview without removing.

### 5. Show Results

Run `scripts/disk-stats.sh` again and calculate space recovered.

## Confirmation Requirements

| Target | Auto-Delete | Confirmation | Notes |
|--------|-------------|--------------|-------|
| Xcode Caches | Yes | No | Auto-regenerated |
| Simulator Caches | Yes | No | Auto-regenerated |
| SwiftUI Previews | Yes | No | Can be huge (80GB) |
| Module Cache | Yes | No | Auto-regenerated |
| Orphaned Derived Data | Yes | No | Project no longer exists |
| Active Derived Data | No | Yes | Has active worktree |
| Device Support | No | Yes | From PHYSICAL devices |
| Simulator Runtimes | No | Yes | Large downloads (5-10GB) |
| Simulator Devices | No | Yes | Loses installed apps |
| Archives | No | Yes | Release builds |

## Worktree Protection

The skill protects Derived Data folders associated with active git worktrees:

1. Extract workspace path from `info.plist`
2. Find git root with `git rev-parse --show-toplevel`
3. Check `git worktree list` for active worktrees
4. Only auto-delete if path doesn't exist (orphaned)

This prevents accidental deletion of build artifacts for feature branches in worktrees.
