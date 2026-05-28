# Filename IOC Examples

## Basic Filename Detection

Filename: `suspicious-filenames.txt`

```text
# Suspicious executables in temp folders
\\[Tt]emp\\.*\.exe;60

# Common malware names
\\mimikatz\.exe;100
\\pwdump.*\.exe;90
\\procdump\.exe;70
```

## Path-Based Detection with Whitelist

Filename: `svchost-filename-iocs.txt`

```text
# Detect svchost.exe outside normal locations
# Column 1: Detection regex
# Column 2: Score
# Column 3: False positive regex (whitelist)

\\svchost\.exe;75;(?i)(System32|SysWOW64|winsxs|servicing)\\
```

## PsExec Detection

Filename: `psexec-filename-iocs.txt`

```text
# PsExec anywhere is suspicious
\\PsExec\.exe;60

# But legitimate in SysInternals folder
\\SysInternals\\PsExec\.exe;-60

# Alternative: Combined format
\\PsExec64\.exe;60;\\SysInternals\\
```

## Webshell Locations

Filename: `webshell-filename-iocs.txt`

```text
# ASP/ASPX in unusual locations
(?i)\\inetpub\\.*\\[a-z0-9]{8}\.aspx;80
(?i)\\wwwroot\\.*cmd\.aspx;100
(?i)\\wwwroot\\.*shell\.asp;100

# PHP webshells
(?i)/var/www/.*c99\.php;100
(?i)/var/www/.*r57\.php;100
(?i)/var/www/html/.*\.php\.suspected;90
```

## Reducing False Positives

Filename: `reduce-fps-filename.txt`

```text
# Noisy directories - reduce score
\\AppData\\Local\\Temp\\;-20
\\Windows\\Installer\\;-30
\\ProgramData\\Package Cache\\;-25

# Known good vendor paths
\\Vendor\\KnownGoodTool\\;-50
```

## Case-Insensitive Detection

Filename: `case-insensitive-filename.txt`

```text
# Use (?i) for case-insensitive regex
(?i)\\payload\.exe;80
(?i)\\malware\d+\.dll;90

# Without (?i), regex is case-sensitive
\\PAYLOAD\.exe;80
```

## Multi-Condition Rules

Filename: `complex-filename-iocs.txt`

```text
# Executable in user profile with suspicious name
(?i)\\Users\\[^\\]+\\.*update.*\.exe;50;(?i)(Microsoft|Adobe|Google)\\

# DLL side-loading indicators
(?i)\\Users\\.*\\version\.dll;70
(?i)\\ProgramData\\.*\\dbghelp\.dll;60;(?i)Windows\\
```

## Timestamp-Based Anomalies

For timestamp-based detection, use YARA rules with external variables instead:

```yara
rule RecentExeInSystem32 {
    meta:
        description = "Recently modified EXE in System32"
        score = 50
    condition:
        extension == ".exe" and
        filepath matches /\\Windows\\System32$/ and
        filesize < 1MB
}
```

## Usage

```bash
# Place in custom-signatures folder
cp suspicious-filenames.txt /path/to/thor/custom-signatures/

# Verify loading
./thor-macosx 2>&1 | grep -i "filename"
```
