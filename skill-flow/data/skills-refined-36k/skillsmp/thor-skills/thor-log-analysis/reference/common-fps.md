# Common False Positives

## Software Categories Prone to FPs

### Admin/IT Tools
- **Nirsoft utilities** – Password recovery, system info tools
- **SysInternals** – PsExec, Process Monitor, Autoruns
- **Remote access** – TeamViewer, AnyDesk, RustDesk
- **Network tools** – Nmap, Wireshark components

### Development Tools
- **AutoIt/AutoHotkey** – Compiled scripts trigger packers signatures
- **Python** – PyInstaller executables, pip packages
- **Node.js** – npm packages with suspicious patterns
- **Go binaries** – Large static binaries trigger anomalies

### Security Tools
- **Penetration testing** – Metasploit, Cobalt Strike (legitimate use)
- **Vulnerability scanners** – Nessus agents, Qualys
- **EDR agents** – Some agents contain detection signatures

### System Components
- **Windows Defender** – Signature files may match
- **Backup software** – Contains system tools
- **Forensic tools** – EnCase, FTK components

## Common FP Patterns

### Generic Packers
```
SUSPICIOUS_Packed_Binary
HKTL_Packed_Executable
```
Triggered by: UPX, custom packers, some installers

**Verify**: Check file origin, digital signature, VirusTotal

### Webshell Signatures
```
WEBSHELL_Generic_PHP
SUSPICIOUS_ASPX_Pattern
```
Triggered by: CMS plugins, legitimate admin panels, development files

**Verify**: Check file location, modification date, content review

### Mimikatz-Related
```
HKTL_Mimikatz_Memory
SUSP_Mimikatz_Strings
```
Triggered by: Security tools containing detection strings, documentation

**Verify**: Full file context, is it actual mimikatz or reference?

### Credential Dumping
```
HKTL_Credential_Dump
SUSP_SAM_Access
```
Triggered by: Backup utilities, forensic tools, password managers

**Verify**: Process context, user account, business justification

## Suppressing Known FPs

### Using `false_positive_filters.cfg`

Location: `./config/false_positive_filters.cfg`

Format:
```
# Comment explaining why this is filtered
<SIGNATURE_NAME>;<PATH_REGEX>
```

Example:
```
# IT admin tools - approved by security team
HKTL_Nirsoft_WebBrowserPassView;C:\\IT\\Tools\\.*
SUSP_AutoIt_Compiled;C:\\Automation\\Scripts\\.*
```

### Using `--init-filter`

Runtime suppression:
```bash
thor64.exe --init-filter AutoIt,Nirsoft -p C:\
```

### Using Trusted Hashes

Create `trusted-hashes.txt` in `./custom-signatures/`:
```
<sha256>;<comment>
a1b2c3d4...;Approved IT tool - JIRA-1234
```

## Investigation Workflow for FPs

1. **Check file metadata**
   - Digital signature valid?
   - Expected location?
   - Expected modification time?

2. **Check VirusTotal**
   - Hash lookup
   - Community score
   - Detection ratio

3. **Check business context**
   - Is this software approved?
   - Who installed it and when?
   - Is the user role appropriate?

4. **Document decision**
   - If FP: Add to filters with justification
   - If suspicious: Escalate for investigation

## High-Confidence vs Low-Confidence Rules

### Usually Reliable (Low FP Rate)
- APT-specific YARA rules
- Known malware hashes
- Specific webshell variants
- Memory-only Cobalt Strike beacons

### Requires Context (Higher FP Rate)
- Generic packer detection
- Obfuscation indicators
- Suspicious strings in scripts
- Anomaly-based detections
- Tesseract outliers

## Quick FP Assessment Questions

1. Is the file digitally signed by a trusted vendor?
2. Is it in an expected location for that software?
3. Does the user's role justify having this tool?
4. Does VirusTotal show low/zero detections?
5. Has this file been in place for a long time unchanged?

If YES to most: Likely FP, add to filters.
If NO to most: Treat as suspicious, investigate further.

## Module-Specific False Positives

### FileScan FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| Filename regex IOC match | Legitimate file matching generic pattern |
| YARA match on THOR reports | Cleartext signatures left from previous scans |
| Dual-use tools | Admin tools like `nmap.exe`, `ncat.exe` in approved locations |
| Recycled files | Legitimate tools in Recycle Bin with wrong names (e.g., `$IR4HB6A.exe`) |
| File size anomaly | Very old legitimate files triggering size checks |
| Signature anomaly | Old/rare versions of legitimate programs (common with `javaw.exe`) |

### SHIMCache / AmCache FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| Strange execution location | Legitimate software using unusual paths |
| THOR's own path | Admins running THOR from suspicious locations (e.g., `C:\Temp\`) |
| Suspicious filename pattern | Software with numeric names (`1.exe`) that's actually legitimate |

### LogScan FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| Web scan attempts | Vulnerability scanners probing for files (HTTP 404s) |
| RoboCopy logs | Backup logs listing hack tools being copied as part of backup |

### ProcessCheck FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| Strange process location | Legitimate software with unusual install paths |
| Parent/child anomaly | Old Windows versions (XP, 2003) with different process hierarchy |
| GeoIP connection | System in region X connecting to servers in region X |
| Process memory YARA match | AV processes, VMware tools, SearchIndexer containing signatures |

### Registry FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| System file in backup path | Values referencing backups (e.g., `\\backupserv\sysbackup\Windows\system32`) |
| Keyboard layout preload | Regional keyboard settings normal for system location |
| Hex pattern `4d5a` | Registry value starting with `4d5a` by coincidence |

### Autoruns FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| New element | Recently installed legitimate software |
| Strange autorun location | Legitimate software using unusual persistence |

### ServiceCheck FPs

| Pattern | Typical FP Cause |
|---------|------------------|
| Suspicious service path | Legitimate software installed in user folders |
| Filename IOC match | Service name matching regex pattern |
| Admin-created service | Services registered manually by admins (e.g., `C:\srvany.exe`) |
