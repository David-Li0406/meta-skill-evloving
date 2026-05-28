# Xcode Cleanup Locations Reference

## Quick Reference Table

| Target | Location | Safe to Auto-Delete | Notes |
|--------|----------|---------------------|-------|
| Derived Data | `~/Library/Developer/Xcode/DerivedData` | Only orphaned | Check worktrees first |
| iOS Device Support | `~/Library/Developer/Xcode/iOS DeviceSupport` | No | From PHYSICAL devices |
| watchOS Device Support | `~/Library/Developer/Xcode/watchOS DeviceSupport` | No | From PHYSICAL devices |
| tvOS Device Support | `~/Library/Developer/Xcode/tvOS DeviceSupport` | No | From PHYSICAL devices |
| Simulator Runtimes | via `xcrun simctl runtime list` | No | Downloaded OS images |
| Simulator Devices | via `xcrun simctl list devices` | No | Simulator instances |
| Archives | `~/Library/Developer/Xcode/Archives` | No | Release builds |
| Xcode Caches | `~/Library/Caches/com.apple.dt.Xcode` | Yes | Auto-regenerated |
| Simulator Caches | `~/Library/Developer/CoreSimulator/Caches` | Yes | Auto-regenerated |
| SwiftUI Previews | `~/Library/Developer/Xcode/UserData/Previews` | Yes | Can grow to 80GB |
| Module Cache | `~/Library/Developer/Xcode/DerivedData/ModuleCache.noindex` | Yes | Auto-regenerated |

---

## IMPORTANT: Device Support vs Simulators

These are **completely different things** that are often confused:

### Device Support = PHYSICAL DEVICES

**What it is:** Debug symbols downloaded when you connect a **physical iPhone, iPad, or Apple Watch** to your Mac.

**Location:** `~/Library/Developer/Xcode/iOS DeviceSupport/`

**How it gets there:** Automatically downloaded when you plug in a device. You don't manually install these.

**Naming:** Named after the device model and iOS version, e.g., `iPhone16,1 26.2 (23C55)`

**Purpose:** Used to symbolicate crash logs from that physical device.

**If deleted:** Re-downloads automatically next time you connect that device (takes several minutes).

### Simulator Runtimes = DOWNLOADED OS IMAGES

**What it is:** The iOS/visionOS versions you **explicitly downloaded** through Xcode to run in Simulator.

**Location:** Managed by `xcrun simctl runtime list`

**How it gets there:** You download these through Xcode > Settings > Platforms, or they come bundled with Xcode.

**Naming:** Listed as `iOS 26.0 (23A343)` etc.

**Purpose:** The actual OS that runs inside the Simulator.

**If deleted:** Must re-download through Xcode (can be several GB, slow).

### Simulator Devices = SIMULATOR INSTANCES

**What it is:** The actual simulator instances (iPhone 16 Pro, iPad Pro, etc.) and their app data.

**Location:** `~/Library/Developer/CoreSimulator/Devices/`

**How it gets there:** Created automatically or manually through Xcode/simctl.

**Purpose:** Each "device" is a separate instance with its own apps, data, settings.

**If deleted:** Recreated automatically, but loses any installed apps/data.

---

## Detailed Descriptions

### Derived Data
**Location:** `~/Library/Developer/Xcode/DerivedData`

Contains intermediate build products, indexes, and logs for each project. Each project gets a folder with a random suffix (e.g., `MyApp-abcdefghijk`).

**Structure:**
- `ProjectName-hash/` - Per-project build artifacts
- `ModuleCache.noindex/` - Shared module cache
- `CompilationCache.noindex/` - Compilation cache

**Cleanup notes:**
- Safe to delete if project no longer exists (orphaned)
- Check for git worktrees before deleting
- Xcode rebuilds as needed

### Device Support (Physical Devices)
**Locations:**
- `~/Library/Developer/Xcode/iOS DeviceSupport`
- `~/Library/Developer/Xcode/watchOS DeviceSupport`
- `~/Library/Developer/Xcode/tvOS DeviceSupport`

Contains debug symbols downloaded when you connect physical devices. Each device/OS combination is 2-5GB.

**Cleanup notes:**
- These are from PHYSICAL devices you've plugged in
- Needed for crash log symbolication from those devices
- Re-downloads automatically when you reconnect the device
- Xcode 12+ auto-prunes files unused for 180 days
- Safe to delete old versions for devices you no longer own

### Simulator Runtimes
**Managed by:** `xcrun simctl runtime list`

Contains the actual iOS/visionOS runtime images for simulators. Each is 5-10GB.

**Useful commands:**
```bash
# List installed runtimes with total size
xcrun simctl runtime list

# Delete unavailable runtimes
xcrun simctl runtime delete unavailable

# Delete specific runtime by identifier
xcrun simctl runtime delete <identifier>
```

**Cleanup notes:**
- Multiple versions of same OS (e.g., 5 versions of iOS 26.0) are often beta builds
- Keep the release version, delete old betas
- Deleting a runtime removes ALL simulators using it

### Simulator Devices
**Location:** `~/Library/Developer/CoreSimulator/Devices`

Contains the actual simulator instances and their user data.

**Useful commands:**
```bash
# List all simulators
xcrun simctl list devices

# Delete unavailable simulators
xcrun simctl delete unavailable

# Delete specific simulator by name or UUID
xcrun simctl delete "iPhone 14 Pro"
xcrun simctl delete <UUID>

# Erase all simulator content (keeps simulators)
xcrun simctl erase all
```

### Archives
**Location:** `~/Library/Developer/Xcode/Archives`

Contains .xcarchive bundles for each app archive you've created (usually for App Store submissions).

**Structure:** Organized by date: `2024-01-15/MyApp 1-15-24, 2.30 PM.xcarchive`

**Cleanup notes:**
- These are your release builds
- Keep recent archives for debugging production crashes
- Safe to delete old archives you no longer need

### Caches (Safe to Delete)

**Xcode Caches:** `~/Library/Caches/com.apple.dt.Xcode`
- General Xcode caches, auto-regenerated

**Simulator Caches:** `~/Library/Developer/CoreSimulator/Caches`
- Simulator-specific caches, auto-regenerated

**SwiftUI Previews:** `~/Library/Developer/Xcode/UserData/Previews`
- Preview cache for SwiftUI canvas
- Can grow to 80GB over time
- Safe to delete, regenerated on demand

**Module Cache:** `~/Library/Developer/Xcode/DerivedData/ModuleCache.noindex`
- Shared module compilation cache
- Safe to delete, rebuilt as needed

---

## Worktree Detection Logic

To determine if a Derived Data folder is safe to delete:

1. Extract `WorkspacePath` from `info.plist`:
   ```bash
   /usr/libexec/PlistBuddy -c "Print :WorkspacePath" "$derived_data_folder/info.plist"
   ```

2. Get the project directory (parent of .xcodeproj):
   ```bash
   project_dir=$(dirname "$workspace_path")
   ```

3. Check if it's part of a git worktree:
   ```bash
   git_root=$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null)
   worktrees=$(git -C "$git_root" worktree list | awk '{print $1}')
   ```

4. Safe to delete if:
   - Path doesn't exist (orphaned)
   - Path exists but is NOT in the worktree list AND user confirms
