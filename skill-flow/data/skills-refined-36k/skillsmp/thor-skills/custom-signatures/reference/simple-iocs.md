# Simple IOCs

Simple IOC files are CSV-style text files with `.txt` extension. The filename must contain a tag (with word boundaries) to indicate the IOC type.

## Hash IOCs

Files with `hash` or `hashes` in filename.

### Format

```
HASH;COMMENT
HASH;SCORE;COMMENT
```

- Columns separated by semicolon
- Supports MD5, SHA1, SHA256, and Imphash (since THOR 10.7.6)
- Case-insensitive matching
- Default score: 100

### Examples

```text
# custom-hashes-iocs.txt

# Basic hash with comment
0c2674c3a97c53082187d930efb645c2;DEEP PANDA Sakula Malware

# Hash with custom score
f05b1ee9e2f6ab704b8919d5071becbce6f9d0f9d0ba32a460c41d5272134abe;50;Vulnerable driver

# SHA1
da39a3ee5e6b4b0d3255bfef95601890afd80709;Empty file hash

# Imphash (since 10.7.6)
d0583e7f5e56a9621b4fe9e4d65ab347;Cobalt Strike imphash
```

## Filename IOCs

Files with `filename` or `filenames` in filename.

### Format

```
REGEX;SCORE
REGEX;SCORE;FP_REGEX
```

- Column 1: Regex pattern for path/filename
- Column 2: Score (positive adds, negative subtracts)
- Column 3: Optional false positive regex (only evaluated if column 1 matched)

### Case Sensitivity

- Simple strings (no regex chars): case-insensitive
- Regex patterns: case-sensitive by default
- Use `(?i)` anywhere in pattern for case-insensitive regex

### Examples

```text
# custom-filename-iocs.txt

# Simple filename match (case-insensitive)
\\nc\.exe;60

# Score reduction for known location
\\SysInternals\\PsExec\.exe;-60

# Combined: detect + whitelist in one line
\\PsExec\.exe;60;\\SysInternals\\

# Detect svchost.exe outside normal paths
([C-Zc-z]:\\|\\\\).{1,40}\\svchost\.exe;65;(?i)(System32|SysWOW64|winsxs)\\

# Reduce score for noisy directory
\\directory_with_false_positives\\;-30
```

## C2 IOCs

Files with `c2` or `domains` in filename.

### Format

```
INDICATOR;SCORE
```

- Domain names, FQDNs, single IPs, CIDR ranges
- Default score: 100
- Comments start with `#`

### Examples

```text
# case44-c2-domains.txt

# Comment applies to following IOCs
# APT Campaign C2 Infrastructure
mastermind.eu
googleaccountservices.com
89.22.123.12

# Custom score
someotherdomain.biz;80

# CIDR range
192.168.100.0/24;70
```

## Keyword IOCs

Files with `keyword` or `keywords` in filename.

### Format

One string per line. Case-sensitive matching.

### Examples

```text
# incident-keywords.txt

# Evil strings from our case
sekurlsa::logonpasswords
failed to create Service 'GAMEOVER'
kiwi.eo.oe
Invoke-Mimikatz
```

## Mutex/Event Handle IOCs

Files with `handles` in filename.

### Format

```
PATTERN;COMMENT
```

- String or regex pattern
- Scope prefixes: `Global\\`, `BaseNamedObjects\\` (optional)
- Case-sensitive
- Simple strings match as "equals", regex as "contains"

### Examples

```text
# operation-handles.txt

Global\\mymaliciousmutex;Operation Fallout RAT Mutex
Global\\WMI_CONNECTION_RECV;Flame Event
Dwm-[a-f0-9]{4}-ApiPort-[a-f0-9]{4};Chinese campaign malware
```

## Named Pipe IOCs

Files with `pipes` or `pipe` in filename.

### Format

```
PATTERN;COMMENT
PATTERN;SCORE;COMMENT
```

- Regex pattern (without `\\.\pipe\` prefix)
- Case-insensitive
- Default score: 100

### Examples

```text
# incident-named-pipes.txt

# Comment for context
MyMaliciousNamedPipe;Known RAT pipe
MyInteresting[a-z]+Pipe;50;Suspicious pattern
```

## Trusted Hash IOCs

Files with `trusted-hash`, `trusted-hashes`, `falsepositive-hash`, or `falsepositive-hashes` in filename.

Used to whitelist known-good hashes and reduce false positives.

### Examples

```text
# my-trusted-hashes.txt

# Known good files in our environment
a1b2c3d4e5f6...;Internal tool hash
```

## Module Coverage

Different IOC types are applied in different modules:

| IOC Type | Modules |
|----------|---------|
| Hash | Filescan, ProcessCheck |
| Filename | Filescan |
| C2 | ProcessConnections, (optionally process memory) |
| Keyword | Many modules (see THOR docs) |
| Handles | ProcessCheck |
| Pipes | NamedPipes |

## Encryption

To protect sensitive IOCs on potentially compromised systems:

```bash
thor-util encrypt --file my-c2-domains.txt
# Creates my-c2-domains.dat (encrypted)
```

Encrypted files use different extensions:
- `.txt` → `.dat`
- `.yar` → `.yas`
- `.yml` → `.yms`
- `.json` → `.jsos`
