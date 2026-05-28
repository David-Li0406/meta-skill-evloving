# Defender Quarantine Extractor Plugin

Automatically decrypts Windows Defender quarantine files and scans the original malware payload.

## Use Case

When Defender quarantines a file, it encrypts and stores it in:
```
C:\ProgramData\Microsoft\Windows Defender\Quarantine\
```

This plugin:
1. Detects quarantine files by magic header (`0x0B AD 00`)
2. Decrypts the RC4-encrypted blob using Defender's known key
3. Extracts the original malware payload
4. Feeds it back to THOR for full scanning

## Implementation

```go
package main

import (
    "crypto/rc4"
    "encoding/binary"
    "fmt"
    "io"
    "strings"

    thorlog "github.com/NextronSystems/jsonlog/thorlog/v3"
    thor "github.com/NextronSystems/thor-plugin"
)

func Init(_ thor.Configuration, logger thor.Logger, actions thor.RegisterActions) {
    // YARA rule to detect Defender quarantine files
    const yaraRule = `
rule defender_quarantine : DEEPSCAN defender_quarantine
{
    meta:
        description = "Windows Defender quarantine file"
        score = 0
    condition:
        uint16(0) == 0xAD0B and uint8(2) == 0x00
}`

    actions.AddYaraRule(thor.TypeMeta, yaraRule)
    actions.AddRuleHook("defender_quarantine", extractAndRescan)
    logger.Info("Defender quarantine plugin initialised")
}

func extractAndRescan(scanner thor.Scanner, obj thor.MatchingObject) {
    // Verify path is actually Defender quarantine
    if f, ok := obj.Object.(*thorlog.File); ok {
        pathNorm := strings.ToLower(strings.ReplaceAll(f.Path, "\\", "/"))
        if !strings.Contains(pathNorm, "programdata/microsoft/windows defender/quarantine") {
            return
        }
    } else {
        return
    }

    scanner.Debug("Decrypting Defender quarantine blob")

    data, err := readAll(obj.Content)
    if err != nil {
        scanner.Error("failed to read blob", "err", err)
        return
    }

    payload, err := decodePayload(data)
    if err != nil {
        scanner.Debug("quarantine decode failed", "err", err)
        return
    }

    // Scan the extracted payload
    scanner.ScanFile("defender_quarantine_payload.bin", payload, "DEFENDER_QUARANTINE")
}

func readAll(r thor.ObjectReader) ([]byte, error) {
    size := r.Size()
    if size <= 0 || size > 1<<30 {
        return nil, fmt.Errorf("invalid size: %d", size)
    }
    buf := make([]byte, size)
    r.Seek(0, io.SeekStart)
    io.ReadFull(r, buf)
    return buf, nil
}

func decodePayload(enc []byte) ([]byte, error) {
    if len(enc) < 12 || enc[0] != 0x0B || enc[1] != 0xAD || enc[2] != 0x00 {
        return nil, fmt.Errorf("invalid quarantine header")
    }

    // RC4 decrypt with Defender's static key
    cipher, _ := rc4.NewCipher(mseKey)
    cipher.XORKeyStream(enc, enc)

    // Parse header: 0x28 bytes + metadata length at offset 8
    headerLen := 0x28 + int(binary.LittleEndian.Uint32(enc[8:12]))
    if headerLen <= 0 || headerLen > len(enc) {
        return nil, fmt.Errorf("corrupt header length")
    }

    return enc[headerLen:], nil
}

// mseKey: 256-byte RC4 key from mpengine.dll
var mseKey = []byte{
    0x1E, 0x87, 0x78, 0x1B, 0x8D, 0xBA, 0xA8, 0x44, /* ... full key ... */
}
```

## Key Techniques

### Path Filtering

The YARA rule matches any file with the quarantine header. The hook then filters by path:

```go
pathNorm := strings.ToLower(strings.ReplaceAll(f.Path, "\\", "/"))
if !strings.Contains(pathNorm, "programdata/microsoft/windows defender/quarantine") {
    return
}
```

This prevents false positives on files that happen to start with the same bytes.

### Rescanning Extracted Content

```go
scanner.ScanFile("defender_quarantine_payload.bin", payload, "DEFENDER_QUARANTINE")
```

- First arg: virtual filename for the extracted content
- Second arg: raw bytes to scan
- Third arg: unpack method (appears in YARA `unpack_source` external)

### Score = 0

```yara
meta:
    score = 0
```

The YARA rule itself doesn't indicate maliciousness - it's just for triggering the hook. The extracted payload will be scored based on its own matches.

## metadata.yml

```yaml
name: DefenderQuarantineExtractor
version: v0.1.0
description: Extracts original payloads from Windows Defender quarantine files
author: Florian Roth
requires_thor: v11.0.0
```

## Packaging

```bash
zip -j defender-quarantine.zip defender_quarantine.go metadata.yml
```

No vendoring needed - only uses Go standard library.
