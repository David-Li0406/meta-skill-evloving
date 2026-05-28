# Getting Started with THOR Plugins

## Prerequisites

- THOR v11 or later
- Go 1.21 or later installed
- A text editor or IDE with Go support

## Quick Start

### 1. Create Plugin Directory

```bash
mkdir my-thor-plugin
cd my-thor-plugin
go mod init my-thor-plugin
```

### 2. Add THOR Plugin Dependency

```bash
go get github.com/NextronSystems/thor-plugin
go get github.com/NextronSystems/jsonlog/thorlog/v3
```

### 3. Create plugin.go

```go
package main

import thor "github.com/NextronSystems/thor-plugin"

func Init(config thor.Configuration, logger thor.Logger, actions thor.RegisterActions) {
    logger.Info("My plugin loaded!")

    // Option 1: Add a YARA rule and hook
    actions.AddYaraRule(thor.TypeMeta, `
rule MyRule: MYRULE {
    meta:
        score = 0
    condition:
        uint16(0) == 0x5A4D  // MZ header
}`)

    actions.AddRuleHook("MYRULE", func(scanner thor.Scanner, obj thor.MatchingObject) {
        scanner.Info("Found PE file!")
    })

    // Option 2: Post-processing hook (fires on findings)
    actions.AddPostProcessingHook(func(logger thor.Logger, obj thor.MatchedObject) {
        logger.Info("Finding detected", "score", obj.Finding.Score)
    })
}
```

### 4. Create metadata.yml

```yaml
name: MyPlugin
version: v1.0.0
description: My first THOR plugin
author: Your Name
requires_thor: v11.0.0
```

### 5. Package the Plugin

```bash
# Simple plugin (no external deps)
zip -j my-plugin.zip plugin.go metadata.yml

# Plugin with dependencies
go mod vendor
zip -r my-plugin.zip plugin.go metadata.yml vendor/
```

### 6. Install and Test

```bash
# Copy to THOR's plugins directory
cp my-plugin.zip /path/to/thor/plugins/

# Run THOR - look for your plugin message
./thor-macosx --debug 2>&1 | grep -i "my plugin"
```

## Plugin Structure

```
my-plugin.zip
├── plugin.go          # Main plugin code (package main, Init function)
├── metadata.yml       # Plugin metadata
├── helper.go          # Optional: additional Go files
└── vendor/            # Optional: vendored dependencies
    └── github.com/
        └── ...
```

## Choosing a Hook Type

### AddRuleHook (YARA/Sigma Triggered)

Use when you want to:
- React to specific file types or content patterns
- Parse custom file formats
- Extract and rescan embedded content

```go
// Triggered when YARA rule with tag "MYTAG" matches
actions.AddRuleHook("MYTAG", func(scanner thor.Scanner, obj thor.MatchingObject) {
    // Access matched file/object
    // Can scan additional data with scanner.ScanFile()
})
```

### AddPostProcessingHook

Use when you want to:
- React to findings (after scoring)
- Upload/collect suspicious samples
- Enrich findings with external data
- Send alerts

```go
// Triggered for each finding
actions.AddPostProcessingHook(func(logger thor.Logger, obj thor.MatchedObject) {
    // Access the finding details
    // obj.Finding contains score, reasons, subject
    // obj.Content provides file content access
})
```

## YARA Rule Types

When adding YARA rules, choose the appropriate type:

| Type | Applied To | Use Case |
|------|------------|----------|
| `TypeMeta` | All files (first 2KB + externals) | Quick file type detection |
| `TypeDefault` | Files selected for deep scan | Content analysis |
| `TypeKeyword` | Non-file elements | String/keyword matching |
| `TypeRegistry` | Registry data only | Registry analysis |
| `TypeLog` | Log files and event logs | Log parsing |
| `TypeProcess` | Process memory | Memory scanning |

## Next Steps

- Read [Plugin API](plugin-api.md) for full interface documentation
- Check [examples/](../examples/) for real-world implementations
- See [Packaging](packaging.md) for deployment options
