# ZIP Parser Plugin

Demonstrates parsing archive formats and recursively scanning extracted content.

## Use Case

THOR has built-in archive handling, but this example shows how to:
- Trigger on specific file types using YARA
- Parse file formats in plugin code
- Recursively scan extracted files

## Implementation

```go
package main

import (
    "archive/zip"
    "io"

    "github.com/NextronSystems/jsonlog/thorlog/v3"
    "github.com/NextronSystems/thor-plugin"
)

func Init(config thor.Configuration, logger thor.Logger, actions thor.RegisterActions) {
    // Trigger on ZIP files using THOR's filetype external
    actions.AddYaraRule(thor.TypeMeta, `
rule DetectZipFiles: ZIPFILE {
    meta:
        score = 0
    condition: filetype == "ZIP"
}`)

    actions.AddRuleHook("ZIPFILE", func(scanner thor.Scanner, object thor.MatchingObject) {
        file, isFile := object.Object.(*thorlog.File)
        if !isFile {
            return
        }

        scanner.Debug("Scanning ZIP file", "path", file.Path)

        // Use Go's archive/zip with ObjectReader
        zipReader, err := zip.NewReader(object.Content, object.Content.Size())
        if err != nil {
            scanner.Error("Could not parse zip file", "path", file.Path, "error", err)
            return
        }

        // Scan each file in the archive
        for _, f := range zipReader.File {
            scanZipEntry(config, scanner, f)
        }
    })

    logger.Info("ZipParser plugin loaded!")
}

func scanZipEntry(config thor.Configuration, scanner thor.Scanner, file *zip.File) {
    // Open the file within the ZIP
    reader, err := file.Open()
    if err != nil {
        scanner.Error("Could not open file in zip", "file", file.Name, "error", err)
        return
    }
    defer reader.Close()

    // Respect THOR's max file size setting
    if file.UncompressedSize64 > config.MaxFileSize {
        scanner.Error("File too large", "file", file.Name, "size", file.UncompressedSize64)
        return
    }

    // Read file content
    data, err := io.ReadAll(reader)
    if err != nil {
        scanner.Error("Could not read file", "file", file.Name, "error", err)
        return
    }

    // Scan the extracted file
    // Note: If data is another ZIP, this hook will fire again (recursive)
    scanner.ScanFile(file.Name, data, "ZIP")
}
```

## Key Techniques

### Using THOR Externals in YARA

```yara
condition: filetype == "ZIP"
```

THOR provides external variables to YARA rules:
- `filetype` - detected file type (e.g., "ZIP", "EXE", "PDF")
- `filename` - base filename
- `filepath` - full path
- `extension` - file extension
- `filesize` - file size

### Respecting Configuration

```go
if file.UncompressedSize64 > config.MaxFileSize {
    scanner.Error("File too large", ...)
    return
}
```

Always check `config.MaxFileSize` before loading large files into memory.

### Recursive Scanning

```go
scanner.ScanFile(file.Name, data, "ZIP")
```

When `ScanFile` encounters another ZIP, the same hook fires again. THOR handles recursion depth limits automatically.

## metadata.yml

```yaml
name: ZipParser
version: v1.0.0
description: Example plugin demonstrating archive parsing
author: Nextron Systems
requires_thor: v11.0.0
```

## Packaging

```bash
zip -j zipparser.zip plugin.go metadata.yml
```

Uses only Go standard library - no vendoring needed.
