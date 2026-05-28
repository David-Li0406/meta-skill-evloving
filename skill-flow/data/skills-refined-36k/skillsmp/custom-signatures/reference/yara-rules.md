# YARA Rules in THOR

THOR supports custom YARA rules with extensions to the standard YARA syntax.

## File Placement

```
thor/
└── custom-signatures/
    └── yara/
        ├── my-generic-rules.yar      # Generic rules
        ├── my-registry-rules.yar     # Registry-specific (tag in name)
        ├── my-log-rules.yar          # Log-specific (tag in name)
        └── my-meta-rules.yar         # Meta rules (tag in name)
```

## Rule Types

### Generic YARA Rules

No special tag in filename. Applied to:
- Files (up to max file size limit)
- Process memory
- DeepDive data chunks

```yara
rule MyGenericRule {
    meta:
        description = "Detects malware X"
        score = 80
    strings:
        $s1 = "malicious_string"
    condition:
        $s1
}
```

### Specific YARA Rules

Tag in filename determines where rules are applied:

| Tag | Applied To | Example Filename |
|-----|------------|------------------|
| `registry` | Registry keys/values | `apt-registry.yar` |
| `log` | Log files, eventlogs | `suspicious-log.yar` |
| `process` or `memory` | Process memory only | `inmem-process.yar` |
| `keyword` | All string checks | `evil-keyword.yar` |
| `meta` | All files (first 2KB + externals) | `quick-meta.yar` |

## THOR-Specific Meta Attributes

### score

Sets the score added when rule matches. Default: 75.

```yara
meta:
    score = 80
```

### type

Restrict rule to file objects or memory only:

```yara
meta:
    type = "file"    // File objects only
    type = "memory"  // Process memory only
```

### limit

Restrict rule to specific module:

```yara
meta:
    limit = "Mutex"       // Only in Mutex module
    limit = "ServiceCheck" // Only in ServiceCheck
```

### nodeepdive

Exclude rule from DeepDive scanning:

```yara
meta:
    nodeepdive = 1
```

### falsepositive

Rule reduces score instead of adding:

```yara
rule FP_KnownGood {
    meta:
        falsepositive = 1
        score = 50  // Will subtract 50 from total score
    strings:
        $s1 = "known_good_string"
    condition:
        $s1
}
```

## External Variables

Available in generic and meta rules:

```yara
rule DetectSuspiciousLocation {
    meta:
        description = "EXE in temp with specific name"
        score = 70
    strings:
        $s1 = "MZ"
    condition:
        $s1 and
        filename matches /update\.exe/i and
        filepath matches /\\[Tt]emp\\/
}
```

| Variable | Type | Description |
|----------|------|-------------|
| `filename` | string | File name only |
| `filepath` | string | Path without filename |
| `extension` | string | Extension with dot, lowercase |
| `filetype` | string | Magic header type (EXE, ZIP, etc.) |
| `filesize` | int | File size in bytes (YARA built-in) |
| `owner` | string | File owner |
| `group` | string | File group (Linux only) |
| `filemode` | int | POSIX-style file mode |
| `timezone` | string | System timezone |
| `language` | string | System language |
| `osversion` | int | Windows build number (0 on non-Windows) |
| `unpack_parent` | string | Immediate container (e.g., "ZIP") |
| `unpack_source` | string | Full unpack chain (e.g., "EMAIL>ZIP") |

## Registry Rules

Registry data is formatted as:
```
KEYPATH;KEY;VALUE\n
```

Example rule:

```yara
rule Registry_Persistence {
    meta:
        description = "Suspicious Run key"
    strings:
        $s1 = "\\CurrentVersion\\Run;SuspiciousEntry"
    condition:
        $s1
}
```

**Note:** Registry base names (HKLM, HKCU, etc.) are NOT included in the scanned string.

Value formatting:
- REG_BINARY: Hex encoded, uppercase
- REG_MULTI_SZ: Separated by `\0`
- REG_DWORD: Decimal (e.g., `32` for 0x20)

## Log Rules

- Text logs: Each line passed to rules
- Event logs: Serialized as `Key1: Value1  Key2: Value2  ...`

```yara
rule Suspicious_EventLog {
    meta:
        description = "Suspicious PowerShell execution"
    strings:
        $s1 = "CommandLine: powershell" nocase
        $s2 = "-enc" nocase
    condition:
        all of them
}
```

## Meta Rules with DEEPSCAN

Meta rules with DEEPSCAN tag trigger full file scan:

```yara
rule TriggerDeepScan : DEEPSCAN {
    meta:
        description = "Trigger deep scan on suspicious archive"
        score = 0
    condition:
        filetype == "RAR" and filesize > 10MB
}
```

## Bulk Scanning Caveat

Registry and log rules use bulk scanning for performance. False positive strings in one entry can affect matching of another entry in the same bulk.

**Problem:**
```yara
rule FakeEntry {
    strings:
        $s1 = "SuspiciousKey;Value;"
        $fp = "Windows\\System32"
    condition:
        $s1 and not $fp
}
```

The `$fp` might match a different entry in the bulk, preventing detection.

**Solution:** Make FP strings specific to the detection:
```yara
rule FakeEntry {
    strings:
        $s1 = "SuspiciousKey;Value;"
        $fp = /SuspiciousKey;Value;[^\n]{0,40}Windows\\System32/
    condition:
        $s1 and not $fp
}
```

## Performance Guidelines

1. Avoid unbounded regex quantifiers (`.*`, `.+`, `\w+`)
2. Use `fullword` modifier when possible
3. Prefer literal strings over regex
4. Test rules with `yara` binary before deploying
5. Use `score = 0` for detection-only rules (triggers only)

Reference: https://gist.github.com/Neo23x0/e3d4e316d7441d9143c7

## Encryption

```bash
thor-util encrypt --file my-rules.yar
# Creates my-rules.yas
```
