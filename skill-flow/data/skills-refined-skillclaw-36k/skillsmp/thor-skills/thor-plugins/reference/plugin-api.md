# THOR Plugin API Reference

## Entry Point

Every plugin must define:

```go
package main

import thor "github.com/NextronSystems/thor-plugin"

func Init(config thor.Configuration, logger thor.Logger, actions thor.RegisterActions)
```

This function is called once when THOR starts and the plugin is loaded.

## Configuration

```go
type Configuration struct {
    MaxFileSize uint64  // Maximum file size THOR will scan
}
```

Use to respect THOR's configured limits when processing files.

## Logger

Available throughout plugin lifecycle:

```go
type Logger interface {
    Info(text string, kv ...any)   // Informational messages
    Debug(text string, kv ...any)  // Debug messages (--debug flag)
    Error(text string, kv ...any)  // Error messages
}
```

Key-value pairs are passed as alternating key, value arguments:

```go
logger.Info("Processing file", "path", "/tmp/test.exe", "size", 1024)
// Output: Processing file path=/tmp/test.exe size=1024
```

## RegisterActions

Available only during `Init()`:

```go
type RegisterActions interface {
    AddYaraRule(ruletype YaraRuleType, rule string)
    AddRuleHook(tag string, callback RuleMatchedCallback)
    AddPostProcessingHook(callback PostProcessingCallback)
}
```

### AddYaraRule

Adds a YARA rule to THOR's ruleset:

```go
actions.AddYaraRule(thor.TypeMeta, `
rule DetectPE: PETAG {
    meta:
        score = 0
    condition:
        uint16(0) == 0x5A4D
}`)
```

**Important:** Set `score = 0` for detection-only rules that don't indicate maliciousness.

### YaraRuleType

```go
const (
    TypeMeta     // All files, first 2KB + THOR externals
    TypeKeyword  // Non-file elements
    TypeDefault  // Files selected for deep scan
    TypeRegistry // Registry data only
    TypeLog      // Log files and event logs
    TypeProcess  // Process memory
)
```

### AddRuleHook

Registers callback for when a rule with specified tag matches:

```go
actions.AddRuleHook("PETAG", func(scanner thor.Scanner, obj thor.MatchingObject) {
    // Called when rule with tag PETAG matches
})
```

### AddPostProcessingHook

Registers callback for each finding:

```go
actions.AddPostProcessingHook(func(logger thor.Logger, obj thor.MatchedObject) {
    // Called for each finding after scoring
})
```

## Scanner Interface

Available within `RuleMatchedCallback`:

```go
type Scanner interface {
    ScanString(data string)
    ScanFile(name string, data []byte, unpackMethod string)
    ScanStructuredData(data []KeyValuePair)
    AddReason(reason thorlog.Reason)
    Logger  // Embeds Info, Debug, Error methods
}
```

### ScanString

Scan a string with filename IOCs, keyword YARA, and Sigma:

```go
scanner.ScanString(extractedText)
```

### ScanFile

Scan extracted file content as if found on filesystem:

```go
scanner.ScanFile("extracted.exe", fileBytes, "MYFORMAT")
// unpackMethod appears in unpack_source YARA external
```

### ScanStructuredData

Scan key-value pairs:

```go
scanner.ScanStructuredData([]thor.KeyValuePair{
    {Key: "command", Value: "/bin/sh -c evil"},
    {Key: "path", Value: "/tmp/suspicious"},
})
```

### AddReason

Add a reason to the current finding:

```go
scanner.AddReason(thorlog.Reason{
    Score:   50,
    Message: "Suspicious pattern detected",
})
```

## MatchingObject

Passed to `RuleMatchedCallback`:

```go
type MatchingObject struct {
    Object  jsonlog.Object  // Full object description
    Content ObjectReader    // File/process content access
}
```

### Accessing Object Details

```go
// Check if it's a file
if file, ok := obj.Object.(*thorlog.File); ok {
    scanner.Info("File matched", "path", file.Path, "size", file.Size)
}

// Check if it's a registry value
if reg, ok := obj.Object.(*thorlog.RegistryValue); ok {
    scanner.Info("Registry matched", "key", reg.Key)
}
```

### ObjectReader

```go
type ObjectReader interface {
    io.ReaderAt
    io.ReadSeeker
    Size() int64
}
```

Read file content:

```go
data := make([]byte, obj.Content.Size())
obj.Content.Seek(0, io.SeekStart)
io.ReadFull(obj.Content, data)
```

## MatchedObject

Passed to `PostProcessingCallback`:

```go
type MatchedObject struct {
    Finding *thorlog.Finding
    Content ObjectReader
}
```

Access finding details:

```go
func postProcess(logger thor.Logger, obj thor.MatchedObject) {
    logger.Info("Finding",
        "score", obj.Finding.Score,
        "module", obj.Finding.Module,
    )

    if file, ok := obj.Finding.Subject.(*thorlog.File); ok {
        logger.Info("File finding", "sha256", file.Hashes.Sha256)
    }
}
```

## Common Object Types

From `github.com/NextronSystems/jsonlog/thorlog/v3`:

- `*thorlog.File` - File with Path, Size, Hashes, MagicHeader, etc.
- `*thorlog.RegistryValue` - Registry entry with Key, ParsedValue
- `*thorlog.Process` - Process with PID, Name, CommandLine
- `*thorlog.LogEntry` - Log line with Source, Message
- `*thorlog.Finding` - Complete finding with Score, Reasons, Subject

## Limitations

Plugins run in yaegi interpreter with restrictions:

- No `unsafe` package
- No `syscall` package
- No CGO
- External dependencies must be vendored
- Supported Go versions: latest two major releases
