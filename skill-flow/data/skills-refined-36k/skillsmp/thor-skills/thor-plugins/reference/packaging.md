# Packaging THOR Plugins

## Basic Structure

A THOR plugin ZIP must contain:

```
plugin.zip
├── plugin.go       # Required: package main with Init()
├── metadata.yml    # Required: plugin metadata
├── *.go            # Optional: additional Go source files
└── vendor/         # Optional: vendored dependencies
```

## metadata.yml

```yaml
name: PluginName              # Required: shown in THOR logs
version: v1.0.0               # Optional: semantic version
description: |                # Optional: plugin description
  Multi-line description
  of the plugin.
author: Your Name             # Optional: author credit
requires_thor: v11.0.0        # Optional: minimum THOR version
link: https://example.com     # Optional: documentation URL
build_tags:                   # Optional: Go build tags
  - windows
```

## Packaging Commands

### Simple Plugin (No Dependencies)

```bash
cd my-plugin/
zip -j my-plugin.zip plugin.go metadata.yml
```

The `-j` flag stores just the files without directory structure.

### Plugin with Multiple Source Files

```bash
zip -j my-plugin.zip *.go metadata.yml
```

### Plugin with Dependencies

```bash
# First, vendor dependencies
go mod tidy
go mod vendor

# Then package everything
zip -r my-plugin.zip *.go metadata.yml vendor/
```

### Plugin with Subdirectories

If your plugin has internal packages:

```bash
zip -r my-plugin.zip *.go metadata.yml vendor/ internal/
```

## Installation

Place the ZIP in THOR's `plugins/` directory:

```bash
# Find or create plugins directory
ls /path/to/thor/plugins/ || mkdir /path/to/thor/plugins/

# Copy plugin
cp my-plugin.zip /path/to/thor/plugins/

# Verify
ls /path/to/thor/plugins/
# my-plugin.zip
```

## Verification

Check plugin loads correctly:

```bash
# Look for plugin initialization messages
./thor-macosx 2>&1 | head -50 | grep -i plugin

# With debug for more detail
./thor-macosx --debug 2>&1 | grep -i "plugin\|PluginName"
```

Expected output:
```
INFO  Plugin loaded: PluginName v1.0.0
INFO  PluginName: My initialization message
```

## CI/CD with GitHub Actions

Example workflow (`.github/workflows/release.yml`):

```yaml
name: Release Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Vendor dependencies
        run: |
          go mod tidy
          go mod vendor

      - name: Package plugin
        run: zip -r plugin.zip *.go metadata.yml vendor/

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: plugin.zip
```

## Troubleshooting

### Plugin Not Loading

1. Check ZIP structure - files must be at root level:
   ```bash
   unzip -l plugin.zip
   # Should show plugin.go, metadata.yml at root, not in subdirectory
   ```

2. Verify `package main` in plugin.go

3. Check THOR version meets `requires_thor`

### Dependency Errors

1. Ensure dependencies are vendored:
   ```bash
   go mod vendor
   ls vendor/
   ```

2. Check for unsupported packages (`unsafe`, `syscall`)

### Version Compatibility

- Use `requires_thor: v11.0.0` to enforce minimum version
- Test with target THOR version before deployment
- yaegi supports latest two Go major versions
