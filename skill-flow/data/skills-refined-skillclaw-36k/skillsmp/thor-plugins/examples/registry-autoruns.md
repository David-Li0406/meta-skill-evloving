# Registry Autoruns Logger Plugin

Demonstrates registry scanning with YARA rules targeting registry data.

## Use Case

Log all autorun entries found in the Windows registry during a scan:
- Track persistence mechanisms
- Feed to SIEM for baseline comparison
- Alert on new/unknown autoruns

## Implementation

```go
package main

import (
    "path/filepath"

    "github.com/NextronSystems/jsonlog/thorlog/v3"
    "github.com/NextronSystems/thor-plugin"
)

func Init(config thor.Configuration, logger thor.Logger, actions thor.RegisterActions) {
    // YARA rule targeting registry data
    actions.AddYaraRule(thor.TypeRegistry, `
rule RunKey: RUNKEY {
    meta:
        score = 0
    strings:
        $s1 = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" nocase
    condition:
        1 of them
}`)

    actions.AddRuleHook("RUNKEY", func(scanner thor.Scanner, object thor.MatchingObject) {
        // Cast to registry value
        registryValue, isRegistryValue := object.Object.(*thorlog.RegistryValue)
        if !isRegistryValue {
            return
        }

        // Extract value name from key path
        valueName := filepath.Base(registryValue.Key)

        // Log the autorun entry
        logger.Info("Found autorun entry",
            "value", valueName,
            "command", registryValue.ParsedValue,
            "key", registryValue.Key,
        )
    })
}
```

## Key Techniques

### Registry-Specific YARA Rules

```go
actions.AddYaraRule(thor.TypeRegistry, `...`)
```

`TypeRegistry` rules only run against registry data, not files. This improves performance and reduces false positives.

### RegistryValue Object

```go
registryValue, isRegistryValue := object.Object.(*thorlog.RegistryValue)

// Available fields:
registryValue.Key          // Full registry key path
registryValue.ParsedValue  // Value data (parsed/decoded)
registryValue.Type         // REG_SZ, REG_DWORD, etc.
```

### Common Registry Persistence Locations

Extend the YARA rule to cover more persistence keys:

```yara
rule PersistenceKeys: PERSISTENCE {
    meta:
        score = 0
    strings:
        $run = "\\CurrentVersion\\Run" nocase
        $runonce = "\\CurrentVersion\\RunOnce" nocase
        $services = "\\Services\\" nocase
        $winlogon = "\\Winlogon\\" nocase
        $shell = "\\Explorer\\Shell" nocase
    condition:
        any of them
}
```

### Structured Data Scanning

If you extract structured data from registry, use `ScanStructuredData`:

```go
scanner.ScanStructuredData([]thor.KeyValuePair{
    {Key: "command", Value: registryValue.ParsedValue},
    {Key: "path", Value: extractedPath},
})
```

## Extending: Custom Alerting

Add severity-based alerting:

```go
func checkAutorun(scanner thor.Scanner, reg *thorlog.RegistryValue) {
    cmd := strings.ToLower(reg.ParsedValue)

    // Check for suspicious patterns
    suspicious := false
    if strings.Contains(cmd, "powershell") && strings.Contains(cmd, "-enc") {
        suspicious = true
    }
    if strings.Contains(cmd, "cmd.exe") && strings.Contains(cmd, "/c") {
        suspicious = true
    }

    if suspicious {
        scanner.AddReason(thorlog.Reason{
            Score:   60,
            Message: "Suspicious autorun command pattern",
        })
    }
}
```

## metadata.yml

```yaml
name: RegistryAutorunsLogger
version: v1.0.0
description: Log registry autorun entries during scans
author: Your Name
requires_thor: v11.0.0
```

## Packaging

```bash
zip -j registry-autoruns.zip plugin.go metadata.yml
```
