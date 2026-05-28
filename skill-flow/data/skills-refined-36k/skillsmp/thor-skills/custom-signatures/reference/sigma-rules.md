# Sigma Rules in THOR

Sigma is a generic rule format for log detection. THOR applies Sigma rules to Windows Eventlogs and text log files.

## Overview

- File extension: `.yml` (plain) or `.yms` (encrypted)
- Applied to: Windows Eventlogs, log files (`.log`)
- Default levels shown: `high` and `critical`
- With `--intense`: Also shows `medium` level

## Activation

```bash
# Sigma enabled by default since THOR 10.7
./thor-macosx -p /path

# Explicitly enable (older versions)
./thor-macosx --sigma -p /path

# Include medium-level rules
./thor-macosx --intense -p /path
```

## File Placement

```
thor/
└── custom-signatures/
    ├── my-sigma-rule.yml
    └── my-encrypted-sigma.yms
```

## Sigma Rule Structure

```yaml
title: Suspicious PowerShell Download
status: experimental
description: Detects PowerShell downloading files
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        CommandLine|contains|all:
            - 'powershell'
            - 'downloadstring'
    condition: selection
level: high
```

## Log Sources Supported

### Windows Eventlogs

```yaml
logsource:
    product: windows
    service: security
```

Common services:
- `security` - Security.evtx
- `system` - System.evtx
- `application` - Application.evtx
- `powershell` - PowerShell logs
- `sysmon` - Sysmon logs

### Text Log Files

THOR scans `.log` files with Sigma rules during Filescan module.

## Rule Levels and Scoring

| Sigma Level | THOR Behavior |
|-------------|---------------|
| `critical` | Always shown |
| `high` | Always shown |
| `medium` | Only with `--intense` |
| `low` | Only with `--intense` |
| `informational` | Not shown by default |

## Custom Sigma Rules

### Example: Detect Specific Scheduled Task

```yaml
title: Malicious Scheduled Task
status: stable
description: Detects creation of known malicious scheduled task
author: Your Name
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4698
        TaskName|contains:
            - 'EvilTask'
            - 'Updater32'
    condition: selection
level: high
tags:
    - attack.persistence
    - attack.t1053
```

### Example: Linux Auth Log

```yaml
title: SSH Brute Force
status: experimental
description: Detects multiple failed SSH logins
logsource:
    product: linux
    service: auth
detection:
    selection:
        - 'Failed password'
        - 'authentication failure'
    condition: selection
level: medium
```

## Scanning Commands

### Windows Eventlog Scan

```bash
# Scan only eventlogs
thor64.exe -a Eventlog --sigma

# Scan specific evtx files
thor64.exe -a Eventlog -p C:\path\to\evtx\files --sigma
```

### Linux Log Scan

```bash
# Scan /var/log
./thor-linux-64 -a Filesystem -p /var/log --sigma
```

## Sigma Resources

- Official repo: https://github.com/SigmaHQ/sigma
- Rule converter: https://github.com/SigmaHQ/sigma/tree/master/tools
- THOR ships with SigmaHQ public rules + Nextron rules

## Encryption

```bash
thor-util encrypt --file my-sigma-rule.yml
# Creates my-sigma-rule.yms
```
