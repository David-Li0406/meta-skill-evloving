# Output and Reporting

## Default Outputs

THOR produces by default:
- **Real-time**: Text log (.txt), optional Syslog
- **End-of-scan**: HTML report, CSV file

## Output Directory (`-e`)

Write all outputs to specified directory:
```bash
thor64.exe -e /path/to/output/
```

## Text Log

```bash
--nolog              # Disable text log
--logfile <name>     # Custom filename
```

Format: SYSLOG-compatible, written in real-time.

## HTML Report

```bash
--nohtml             # Disable HTML report
--htmlfile <name>    # Custom filename
```

## CSV Output

Legacy format with 3 columns: hash, path, score. Filescan findings only.
Archive contents shown as: `archive.zip|file-with-finding.js`

```bash
--csvstats           # Single-line stats summary
```

## JSON Output

```bash
--jsonfile <name>    # Enable JSON output with custom filename
--jsonv2             # Use JSON v2 format (easier to parse)
--cmdjson            # Print JSON to console (Splunk integration)
```

Default filename: `:hostname:_thor_:time:.json`

## Key/Value Output

```bash
--keyval             # Write key/value format to log
--cmdkeyval          # Print key/value to console
```

## Syslog Output (`-s` / `--syslog`)

Flexible target definition:
```bash
--syslog <target>:<port>:<format>:<protocol>
```

**Formats**: DEFAULT, CEF, JSON, SYSLOGJSON, SYSLOGKV

**Protocols**: UDP (default), TCP, TCPTLS

Examples:
```bash
# UDP syslog (default)
-s 10.0.0.4:514

# TCP with TLS
-s 10.0.0.4:6514:DEFAULT:TCPTLS

# CEF format for ArcSight
-s 10.0.0.4:514:CEF

# JSON format
-s 10.0.0.4:514:JSON
```

Multiple targets: use `-s` multiple times.

Local syslog: `--local-syslog` (logs to local0 facility).

## Audit Trail (`--audit-trail`)

Comprehensive JSON logging of ALL scanned elements (not just findings) plus relationships.

```bash
--audit-trail <hostname>_audittrail.json.gz
```

Output: Gzipped newline-delimited JSON.

Schema includes:
- `id`: Unique element identifier
- `object`: The scanned element
- `timestamps`: All timestamps within element
- `reasons`: Matching signatures with scores
- `references`: Links to related elements (parent archives, extracted files)

Use cases:
- Visualizing scan scope
- Grouping suspicious items
- Finding lateral connections
- THOR Lens input (v11 only)

**Note**: Audit trail with full schema requires THOR v11.

## Timestamps

```bash
--utc                # Use UTC time
--rfc3339            # RFC 3339 format: 2017-02-31T23:59:60Z
```

Default: ANSI C format `Mon Jan 2 15:04:05 2006`

## Scan ID (`-i` / `--scanid`)

```bash
-i SCAN001           # Custom scan ID
--scanid-prefix IR   # Prefix (replaces default "S")
```

Auto-generated format: `S-<random>`. Helps correlate logs from multiple scans.

## Filename Placeholders

- `:hostname:` – System hostname
- `:time:` – Scan timestamp

Example: `--jsonfile :hostname:_:time:.json`

## Encrypted Output

```bash
--encrypt            # Encrypt all output files
--pubkey <file>      # Custom RSA public key (PEM format)
```

Supports 1024, 2048, or 4096 bit keys. Default key decryptable via `thor-util decrypt`.

## Output Summary Table

| Flag | Purpose |
|------|---------|
| `-e PATH` | Output directory |
| `-l FILE` | Custom text log path |
| `--htmlfile FILE` | Custom HTML report path |
| `--jsonfile FILE` | Enable JSON output |
| `--nohtml` | Disable HTML report |
| `--nolog` | Disable text log |
| `-s SERVER` | Send to syslog |
| `--audit-trail FILE` | Enable audit trail |
| `--encrypt` | Encrypt outputs |
