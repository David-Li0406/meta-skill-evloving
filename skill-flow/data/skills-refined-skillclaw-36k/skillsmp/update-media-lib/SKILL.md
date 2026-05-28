---
name: update-media-lib
description: Update third-party media libraries (libvpx, libdav1d, libaom, libopus, libcubeb, etc.) in the Firefox media/ directory. Use when updating codecs, decoders, or vendored media packages.
---

# Update Media Libraries

## Overview

This skill helps update vendored third-party media libraries in Firefox. Each library has its own update process documented in its README and moz.yaml files.

## Supported Libraries

### Fully Automated (mach vendor)

| Library | Path | Source Location | Update Method |
|---------|------|-----------------|---------------|
| libvpx | media/libvpx | media/libvpx/libvpx/ | Two-step with patches |
| libaom | media/libaom | third_party/aom/ | Two-step with patches |
| libsoundtouch | media/libsoundtouch | media/libsoundtouch/ | Two-step with patches |
| libspeex_resampler | media/libspeex_resampler | media/libspeex_resampler/ | Two-step with patches |
| highway | media/highway | third_party/highway/ | Two-step with patches |
| libcubeb | media/libcubeb | media/libcubeb/ | Two-step with patches |
| libpng | media/libpng | media/libpng/ | Two-step with patches |
| libogg | media/libogg | media/libogg/ | Two-step with patches |
| libyuv | media/libyuv | media/libyuv/libyuv/ | Two-step with patches |
| libdav1d | media/libdav1d | third_party/dav1d/ | Simple vendor |
| libvorbis | media/libvorbis | media/libvorbis/ | Simple vendor (file renames) |
| libwebp | media/libwebp | media/libwebp/ | Simple vendor |
| libjxl | media/libjxl | third_party/jpeg-xl/ | Simple vendor |
| libnestegg | media/libnestegg | media/libnestegg/ | Simple vendor |
| libopus | media/libopus | media/libopus/ | Script-based (update.sh) |
| mp4parse-rust | media/mp4parse-rust | third_party/rust/mp4parse* | Rust crate (Cargo.toml) |
| libjpeg | media/libjpeg | media/libjpeg/ | Script-based (update-libjpeg.sh) |

### Manual Update Required (Cannot Auto-Update)

| Library | Path | Reason | Update Method |
|---------|------|--------|---------------|
| ffvpx | media/ffvpx | Requires platform-specific config regeneration | Manual rsync + config generation |
| libmkv | media/libmkv | No vendoring section, upstream abandoned | Cannot update |

## Process

1. **Identify the library** - Confirm which library needs updating
2. **Check limitations** - Verify the library can be auto-updated (see table above)
3. **Read the README** - Check `media/<lib>/README_MOZILLA` or `README.md` for library-specific instructions
4. **Check moz.yaml** - Review `media/<lib>/moz.yaml` for current version and upstream URL
5. **Ask about commit preference** - For two-step libraries, ask user if they want one combined commit or two separate commits
6. **Ask for Bugzilla number** - Optionally ask user for a bug number to include in commit messages
7. **Run the update command** - Execute the appropriate vendor command
8. **Apply patches if needed** - Some libraries require a second step for patches
9. **Build and test** - Verify the update works

## Update Patterns

### Two-step with patches

Libraries with local patches use a two-step process:

```bash
# Step 1: Update the source (without patches)
./mach vendor media/<lib>/moz.yaml --patch-mode=none

# Step 2: Apply local patches
./mach vendor media/<lib>/moz.yaml --patch-mode=only --ignore-modified
```

**Two-step libraries:** libvpx, libaom, libsoundtouch, libspeex_resampler, highway, libcubeb, libpng, libogg, libyuv

**IMPORTANT - Commit Workflow:**
For two-step libraries, ALWAYS ask the user whether they want:
1. **Two separate commits** (recommended by upstream README):
   - First commit: "Update <library> to <version>" (after step 1)
   - Second commit: "Apply local patches to <library>" (after step 2)
2. **Single combined commit**:
   - One commit after both steps: "Update <library> to <version> and apply local patches"

**IMPORTANT - Bugzilla Bug Number:**
ALWAYS ask the user if they have a Bugzilla bug number for this update. This should be asked alongside the commit preference question using AskUserQuestion.

If user provides a bug number, format commit messages as:
- `Bug XXXXXX - Update <library> to <version>`
- `Bug XXXXXX - Apply local patches to <library>`

If no bug number is provided, use the standard format without the "Bug XXXXXX - " prefix.

Use AskUserQuestion to get both the commit preference and optional bug number before proceeding.

### Simple vendor

Libraries without patches or with auto-applied patches:

```bash
# Update to latest
./mach vendor media/<lib>/moz.yaml

# Or update to specific version/commit
./mach vendor media/<lib>/moz.yaml -r <tag-or-commit>

# Or update from a fork
./mach vendor media/<lib>/moz.yaml --repo <repository-url> -r <commit>
```

**Simple vendor libraries:** libdav1d, libvorbis, libwebp, libjxl, libnestegg

**Commit format for simple vendor:**
Ask for optional Bugzilla bug number. If provided:
- `Bug XXXXXX - Update <library> to <version>`

If no bug number:
- `Update <library> to <version>`

### Script-based (libopus)

libopus uses a custom update script integrated with mach vendor:

```bash
./mach vendor media/libopus/moz.yaml
```

The update.sh script is automatically invoked during vendoring.

### Script-based (libjpeg)

libjpeg uses a custom update script that requires cloning the upstream repository first.

**Known issue with patch step:**
The script runs `patch -p0` from `media/libjpeg/`, but the patch file (`mozilla.diff`) contains paths like `a/media/libjpeg/jmorecfg.h`. With `-p0`, patch looks for `a/media/libjpeg/jmorecfg.h` relative to current directory, which doesn't exist. This is documented in MOZCHANGES: *"fix up any rejects from applying the Mozilla specific patches"*.

**Workaround:** After the script fails at the patch step, apply manually with `-p1` from Firefox root (strips the `a/` prefix).

**Update process:**

1. Clone libjpeg-turbo to a temporary directory:
   ```bash
   git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git /tmp/libjpeg-turbo
   ```

2. Run the update script (patch step will fail - this is expected per MOZCHANGES):
   ```bash
   ./media/update-libjpeg.sh /tmp/libjpeg-turbo [tag]
   # Example: ./media/update-libjpeg.sh /tmp/libjpeg-turbo 2.1.5.1
   ```

3. When prompted about patch failure, skip (press Enter or 'y')

4. Apply the patch manually from the Firefox root directory:
   ```bash
   patch -p1 -i media/libjpeg/mozilla.diff
   ```

5. Clean up temporary clone:
   ```bash
   rm -rf /tmp/libjpeg-turbo
   ```

**Version compatibility:**
- Versions 2.x: Compatible with current file structure
- Versions 3.x: Reorganized source structure (files in `src/` subdirectory) - may require additional work

**Commit format:**
Ask for optional Bugzilla bug number. If provided:
- `Bug XXXXXX - Update libjpeg-turbo to <version>`

If no bug number:
- `Update libjpeg-turbo to <version>`

### Rust crate (mp4parse-rust)

mp4parse-rust is a Rust crate hosted at https://github.com/mozilla/mp4parse-rust and vendored into `/third_party/rust/`.

**Update process:**

1. Find the current revision in `/toolkit/library/rust/shared/Cargo.toml`:
   ```toml
   mp4parse_capi = { git = "https://github.com/mozilla/mp4parse-rust", rev = "<current-rev>", ... }
   ```

2. Get the new revision (commit hash or tag) from upstream repository

3. Update the `rev` attribute in Cargo.toml to the new revision

4. Run the vendor command:
   ```bash
   ./mach vendor rust
   # Use --force if needed (mp4parse's lib.rs is quite large)
   ./mach vendor rust --force
   ```

5. Verify expected changes in `/third_party/rust/mp4parse*`

**Commit format:**
Ask for optional Bugzilla bug number. If provided:
- `Bug XXXXXX - Update mp4parse-rust to <revision>`

If no bug number:
- `Update mp4parse-rust to <revision>`

## Limitations and Known Issues

### libaom
- **Issue:** `generate_sources_mozbuild.sh` requires `python3-venv` system package
- **Solution:** Install `python3-venv` before updating: `apt install python3-venv`

### libdav1d
- **Issue:** May require manual moz.build updates for new/removed files
- **Post-update:** Check `moz.build` and `asm/moz.build` for file changes
- **Note:** Assembly files with `%if ARCH_X86_64` may need conditional handling

### libmkv
- **Issue:** Cannot be auto-updated - no vendoring section in moz.yaml
- **Reason:** Upstream (Chromium libvpx) is abandoned
- **Status:** Maintenance only, manual patches required

### ffvpx
- **Issue:** Cannot use mach vendor
- **Update method:** Manual rsync from FFmpeg source
- **Requires:** Platform-specific config regeneration for each target (Unix32, Unix64, Darwin, Windows, Android)
- **See:** `media/ffvpx/README_MOZILLA` for detailed instructions

## Key Files

For each library:
- `media/<lib>/moz.yaml` - Version info, upstream URL, vendoring configuration, patches list
- `media/<lib>/README_MOZILLA` or `README.md` - Detailed update instructions
- `media/<lib>/*.patch` - Local patches to apply

Some libraries store source in `third_party/`:
- `third_party/dav1d/` - dav1d source
- `third_party/aom/` - AOM source
- `third_party/highway/` - highway source
- `third_party/jpeg-xl/` - libjxl source

## Post-Update Steps

1. **Build**: `./mach build`
2. **Lint**: `./mach lint`
3. **Format**: `./mach format`
4. **Test**: `./mach test --auto`

## Troubleshooting

- **Build failures after update**: Check for new source files not added to moz.build
- **Patch failures**: Patches may need updating for new upstream changes
- **Assembly errors on win32**: Move x86_64-only .asm files to conditional blocks
- **nasm version errors**: May need to update minimum nasm version in toolchain
- **python3-venv missing**: Install with `apt install python3-venv` (for libaom)
- **Uncommitted changes error**: Use `--ignore-modified` flag for step 2, or commit between steps
