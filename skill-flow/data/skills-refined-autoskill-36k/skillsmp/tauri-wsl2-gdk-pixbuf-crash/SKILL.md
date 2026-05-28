---
name: tauri-wsl2-gdk-pixbuf-crash
description: |
  Fix for Tauri v2 app crashing on startup in WSL2 with gdk-pixbuf panic: "data.len() must
  fit the width, height, and row_stride". Use when: (1) Tauri app panics immediately on
  launch in WSL2/Linux, (2) error occurs in gdk-pixbuf crate at pixbuf.rs, (3) crash happens
  before window renders, (4) app works on Windows/macOS but fails on Linux/WSL2. The fix is
  to use an empty icon array in tauri.conf.json to bypass icon loading issues with GTK.
author: Claude Code
version: 1.0.0
date: 2025-01-23
---

# Tauri WSL2 gdk-pixbuf Crash Fix

## Problem
Tauri v2 desktop application crashes immediately on startup when running in WSL2 (Windows
Subsystem for Linux) with WSLg. The panic occurs in the gdk-pixbuf crate before the window
can render.

## Context / Trigger Conditions

**Error message:**
```
thread 'main' panicked at /home/user/.cargo/registry/src/.../gdk-pixbuf-0.18.5/src/pixbuf.rs:44:13:
data.len() must fit the width, height, and row_stride
```

**When this occurs:**
- Running Tauri v2 app on WSL2 with WSLg (GUI support)
- App compiles successfully but crashes on `Running` step
- Icons are configured in `tauri.conf.json` under `bundle.icon`
- DISPLAY and WAYLAND_DISPLAY environment variables are set
- Crash happens even with valid PNG files (32x32, 128x128, etc.)

**NOT this issue if:**
- App fails during compilation
- Error mentions missing libraries (install GTK dependencies instead)
- App runs but window doesn't appear (display server issue)

## Solution

### Quick Fix
Set an empty icon array in `tauri.conf.json`:

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": []
  }
}
```

### Why This Works
The gdk-pixbuf library in GTK has issues loading certain icon formats or dimensions in the
WSL2/WSLg environment. By providing an empty icon array, Tauri skips the problematic icon
loading during window initialization. The app will use a default system icon instead.

### Alternative: Ensure Icons are Proper RGBA
If you need custom icons, ensure they are:
1. True color RGBA (not indexed/palette)
2. Created with proper color depth: `convert -size 32x32 xc:'#3b82f6' -type TrueColorAlpha -define png:color-type=6 icon.png`
3. Standard dimensions (32x32, 128x128, 256x256)

Even with proper icons, the empty array workaround may still be needed on WSL2.

## Verification

After applying the fix:
1. Run `npm run tauri:dev` or `cargo tauri dev`
2. App should compile and show `Running /path/to/app`
3. Window should appear without panic
4. Check with `ps aux | grep your-app-name` to confirm process is running

## Example

**Before (crashes):**
```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/icon.png"
    ]
  }
}
```

**After (works):**
```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": []
  }
}
```

## Notes

- This is a WSL2/Linux-specific issue; the same app typically works fine on Windows and macOS
- The fix only affects the development/bundle icons, not runtime functionality
- For production Linux builds, you may need to test on actual Linux to see if the issue persists
- The empty icon array results in a generic/default window icon
- This issue is related to how GTK's gdk-pixbuf handles icon data in the WSLg compositor environment
- Future Tauri or GTK updates may resolve this; check if the issue persists after updates

## Related Issues

- Tauri apps on WSL2 may also require proper DISPLAY/WAYLAND_DISPLAY setup
- If app runs but window doesn't appear, check `echo $DISPLAY` and `/mnt/wslg/` exists
- For "cannot open display" errors, ensure WSLg is installed and running
