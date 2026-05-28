# Troubleshooting Guide

Common issues and solutions when using appshot_

---

## Project Setup Issues

### "Configuration not found"

**Cause:** No `.appshot/config.json` exists in the project.

**Solution:**
```
appshot_init with force: true
```

### "Input directory not found"

**Cause:** Screenshot folder doesn't exist or is empty.

**Solution:**
1. Create the directory: `screenshots/iphone/`
2. Add PNG/JPG screenshots to the folder
3. Run build again

---

## Caption Issues

### Captions not appearing

**Causes:**
1. No captions set for the screenshots
2. Caption file is empty
3. Wrong language specified

**Solutions:**
```
# Check current captions
appshot_captions with device: "iphone", action: "list"

# Auto-generate from filenames
appshot_captions with device: "iphone", action: "auto"

# Set manually
appshot_captions with device: "iphone", action: "set", filename: "screen.png", caption: "My Caption"
```

### Caption text cut off

**Cause:** Caption too long for the available space.

**Solutions:**
1. Use shorter text (2-3 words ideal)
2. Adjust caption box settings:
```
appshot_config with device: "iphone", captionPosition: "above"
```

### Wrong font displaying

**Cause:** Font not available on system.

**Solution:**
```
# Check font availability
appshot_fonts with action: "validate", font: "SF Pro Display"

# List embedded fonts (always available)
appshot_fonts with action: "embedded"
```

**Embedded fonts:** Inter, Poppins, Montserrat, DM Sans, Roboto, Open Sans, Lato, Work Sans, JetBrains Mono, Fira Code

---

## Frame Issues

### "No matching frame found"

**Cause:** Screenshot dimensions don't match any known device.

**Solutions:**
1. Use standard device resolutions
2. Check screenshot dimensions match config

**Common iPhone resolutions:**
- 1290x2796 (iPhone 15 Pro Max, 16 Plus)
- 1179x2556 (iPhone 15 Pro, 16)
- 1206x2622 (iPhone 16 Pro)

### Frame looks wrong / misaligned

**Cause:** Screenshot orientation doesn't match frame.

**Solution:** Ensure portrait screenshots are taller than wide, landscape wider than tall.

---

## Build Issues

### Build produces blank/black images

**Causes:**
1. Screenshot files are corrupted
2. Sharp module issue

**Solutions:**
```
# Run diagnostics
appshot_doctor
```

### "Failed to load screenshot"

**Cause:** File is not a valid image or is corrupted.

**Solution:**
1. Verify the file opens in an image viewer
2. Re-export from the source
3. Ensure file extension matches actual format

### Build is slow

**Solutions:**
```
# Reduce concurrency on low-memory systems
appshot_build with concurrency: 2

# Build specific devices only
appshot_build with devices: ["iphone"]

# Use preview mode for testing
appshot_build with preview: true
```

---

## Background Issues

### Background image not appearing

**Causes:**
1. Image path incorrect
2. Mode set to gradient instead of image/auto

**Solutions:**
```
# Set background explicitly
appshot_backgrounds with action: "set", image: "./bg.png", fit: "cover"

# Or use auto-detect (looks for background.png in device folders)
appshot_build with autoBackground: true
```

### Background looks stretched/cropped

**Solution:** Change fit mode:
```
appshot_backgrounds with action: "set", image: "./bg.png", fit: "contain"
```

Fit modes:
- `cover` - Fill entire area, may crop (default)
- `contain` - Show entire image, may letterbox
- `fill` - Stretch to fill (may distort)
- `scale-down` - Like contain but never upscale

---

## Validation Issues

### "Resolution mismatch"

**Cause:** Screenshot doesn't match App Store requirements.

**Solution:**
```
# Check required specs
appshot_specs with device: "iphone", required: true

# Use presets for correct sizing
appshot_build with presets: ["iphone-6-9", "ipad-13"]
```

### Missing required sizes

**Required for App Store:**
- iPhone 6.9": 1320x2868 or 1290x2796
- iPad 13": 2064x2752 or 2048x2732

---

## System Issues

### Sharp module errors

**Solution:**
```
# Run doctor to check system
appshot_doctor

# Reinstall if needed (in terminal)
npm rebuild sharp
```

### Permission denied errors

**Cause:** Cannot write to output directory.

**Solution:** Check file permissions on `final/` directory.

---

## Quick Diagnostics

Run the doctor command to check all systems:
```
appshot_doctor
```

This checks:
- Node.js version (requires 18+)
- Sharp module installation
- Font detection capability
- File system permissions
- Frame asset availability
