# STIX v2 IOCs in THOR

THOR supports STIX v2 JSON indicator files for threat intelligence integration.

## Overview

- File extension: `.json` (plain) or `.jsos` (encrypted)
- Format: STIX v2 JSON bundles
- STIX v1: **Not supported**

## File Placement

```
thor/
└── custom-signatures/
    ├── threat-intel.json
    └── encrypted-intel.jsos
```

## Supported Observables

### File Observables

#### file:name

```json
{
  "type": "indicator",
  "pattern": "[file:name = 'malware.exe']",
  "pattern_type": "stix"
}
```

Operators: `=`, `!=`, `LIKE`, `MATCHES`

#### file:parent_directory_ref.path

```json
{
  "pattern": "[file:parent_directory_ref.path LIKE '%\\Temp\\%']"
}
```

Operators: `=`, `!=`, `LIKE`, `MATCHES`

#### file:hashes

```json
{
  "pattern": "[file:hashes.'SHA-256' = 'aabbcc...']"
}
```

Supported hash types:
- `file:hashes.sha-256` / `file:hashes.sha256`
- `file:hashes.sha-1` / `file:hashes.sha1`
- `file:hashes.md-5` / `file:hashes.md5`

Operators: `=`, `!=`

#### file:size

```json
{
  "pattern": "[file:size > 1000000]"
}
```

Operators: `<`, `<=`, `>`, `>=`, `=`, `!=`

#### file:created / file:modified / file:accessed

```json
{
  "pattern": "[file:modified > '2024-01-01T00:00:00Z']"
}
```

Operators: `<`, `<=`, `>`, `>=`, `=`, `!=`

### Registry Observables

#### win-registry-key:key

```json
{
  "pattern": "[win-registry-key:key LIKE '%\\CurrentVersion\\Run%']"
}
```

Operators: `=`, `!=`, `LIKE`, `MATCHES`

#### win-registry-key:values.name

```json
{
  "pattern": "[win-registry-key:values.name = 'SuspiciousEntry']"
}
```

Operators: `=`, `!=`, `LIKE`, `MATCHES`

#### win-registry-key:values.data

```json
{
  "pattern": "[win-registry-key:values.data MATCHES '.*powershell.*']"
}
```

Operators: `=`, `!=`, `LIKE`, `MATCHES`

#### win-registry-key:values.modified_time

```json
{
  "pattern": "[win-registry-key:values.modified_time > '2024-01-01T00:00:00Z']"
}
```

Operators: `<`, `<=`, `>`, `>=`, `=`, `!=`

## Complete Example

```json
{
  "type": "bundle",
  "id": "bundle--example",
  "objects": [
    {
      "type": "indicator",
      "id": "indicator--hash-example",
      "name": "Malware XYZ Hash",
      "description": "SHA256 hash of known malware",
      "pattern": "[file:hashes.'SHA-256' = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']",
      "pattern_type": "stix",
      "valid_from": "2024-01-01T00:00:00Z"
    },
    {
      "type": "indicator",
      "id": "indicator--filename-example",
      "name": "Suspicious filename pattern",
      "description": "Detects files matching malware naming pattern",
      "pattern": "[file:name MATCHES '^update[0-9]+\\.exe$']",
      "pattern_type": "stix",
      "valid_from": "2024-01-01T00:00:00Z"
    },
    {
      "type": "indicator",
      "id": "indicator--registry-example",
      "name": "Malicious registry persistence",
      "description": "Detects known malware registry key",
      "pattern": "[win-registry-key:key LIKE '%\\CurrentVersion\\Run%' AND win-registry-key:values.name = 'MalwareUpdater']",
      "pattern_type": "stix",
      "valid_from": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## Pattern Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Exact match | `file:name = 'test.exe'` |
| `!=` | Not equal | `file:name != 'legit.exe'` |
| `LIKE` | SQL-style wildcard (`%`) | `file:name LIKE '%update%'` |
| `MATCHES` | Regex match | `file:name MATCHES '^evil.*'` |
| `<`, `<=`, `>`, `>=` | Comparison | `file:size > 1000` |

## Combining Patterns

Use `AND` and `OR` within patterns:

```json
{
  "pattern": "[file:name LIKE '%update%' AND file:size < 100000]"
}
```

## Encryption

```bash
thor-util encrypt --file threat-intel.json
# Creates threat-intel.jsos
```

## Integration with Threat Intel Platforms

Many threat intel platforms export STIX v2:
- MISP (export as STIX 2.x)
- OpenCTI
- Anomali ThreatStream
- Mandiant Advantage

Ensure exports use STIX v2 JSON format (not STIX v1 XML).
