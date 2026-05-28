# Windows Live Scan Examples

## Basic Endpoint Scan

```bash
thor64.exe -e C:\thor-reports
```

Scans default locations, outputs to specified directory.

## Quick Triage Scan

```bash
thor64.exe --quick -e C:\thor-reports
```

~20% runtime for ~80% coverage. Good for initial triage.

## Scan Specific Path

```bash
thor64.exe -p C:\Users\suspicious_user -e C:\thor-reports
```

## Scan with JSON Output for SIEM

```bash
thor64.exe --jsonfile report.json -s 10.0.0.4:514:SYSLOGJSON -e C:\thor-reports
```

## Conservative Production Scan

```bash
thor64.exe --soft --cpulimit 70 --lowprio -e C:\thor-reports
```

Minimizes system impact on production servers.

## Recent Activity Only (Last 7 Days)

```bash
thor64.exe --lookback 7 --global-lookback -e C:\thor-reports
```

## Targeted Threat Hunt

```bash
thor64.exe --init-selector Cobalt -p C:\ -e C:\thor-reports
```

Only loads Cobalt Strike-related signatures.

## All Drives Scan

```bash
thor64.exe --allhds -e C:\thor-reports
```

Scans all local hard drives. Use `--alldrives` for network drives too (requires forensic license, very slow).

## Reduce False Positives

```bash
thor64.exe --init-filter AutoIt,Nirsoft -e C:\thor-reports
```

## With Custom Scan ID

```bash
thor64.exe -i INCIDENT-2024-001 -e C:\thor-reports
```

## Debug Mode (Troubleshooting)

```bash
thor64.exe --debug -a Filescan -p C:\temp --printall
```

Single module with verbose output for testing.
