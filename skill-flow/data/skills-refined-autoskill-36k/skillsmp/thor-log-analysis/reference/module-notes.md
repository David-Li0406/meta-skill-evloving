# Module Notes

THOR has 30+ modules, each scanning different system aspects. Understanding which module produced a finding helps contextualize it.

**Message Enrichment**: Some modules may produce FileScan-like events due to "Message Enrichment" - when a module includes full file paths, THOR enriches the message with file metadata.

## File System Modules

### Filescan

Most common source of findings. Scans files on disk. Rich in attributes.

**Sample fields**:
- `FILE`: Full file path
- `MD5`, `SHA1`, `SHA256`: File hashes
- `SIZE`: File size in bytes
- `TYPE`: Detected file type (may differ from extension)
- `FIRSTBYTES`: First 20 bytes (hex) + ASCII interpretation
- `COMPANY`, `DESC`: PE header metadata
- `OWNER`: File owner account
- `CREATED`, `MODIFIED`, `ACCESSED`: Timestamps
- `REASON_1`, `REASON_2`: Individual scoring reasons

**Characteristic analysis columns**: FILE, MAIN_REASON, SCORE

**Follow-up**: Check file metadata, VirusTotal lookup, submit to sandbox, review with hex editor.

### ArchiveScan
Scans inside archives (ZIP, RAR, 7z, etc.).

Target format: `archive.zip|internal/path/file.js`

Note: Findings inside archives need extraction for deeper analysis.

### MFT (Master File Table)
Windows NTFS metadata analysis. Finds deleted files, timestomping.

Key indicators:
- `MFT_RECORD`: Record number
- `SI_*` vs `FN_*`: $STANDARD_INFORMATION vs $FILE_NAME timestamps

Timestomping: SI timestamps manipulated, FN timestamps original.

## Memory/Process Modules

### ProcessCheck

Running process analysis. Evaluates process characteristics, parent/child relations, priorities, locations, network connections, and process memory with YARA.

**Sample fields**:
- `PID`: Process ID
- `PPID`: Parent process ID
- `PARENT`: Parent process path
- `NAME`: Process name
- `OWNER`: Process owner account
- `COMMAND`: Full command line
- `PATH`: Executable path
- `CREATED`: Process creation time
- `MD5`: Hash of executable
- `CONNECTION_COUNT`, `LISTEN_PORTS`: Network info
- `RULE`: YARA rule name (for memory matches)
- `STRINGS`: Matched strings (for YARA matches)

**Types of detections**:
1. Process location anomalies (started from suspicious path)
2. Parent/child relationship anomalies
3. Process priority anomalies
4. Network connection anomalies (suspicious GeoIP)
5. YARA matches on process memory

**Reference**: [Windows System Processes Overview](https://nasbench.medium.com/windows-system-processes-an-overview-for-blue-teams-42fa7a617920)

**Follow-up**: Memory dump, process tree analysis, handle review, network connection analysis.

### Mutex / Handles
Named synchronization objects. Malware often creates unique mutexes.

Key indicators:
- `MUTEX_NAME` / `HANDLE_NAME`
- Associated process

### Pipes
Named pipe analysis. Used for IPC, C2 communication.

Key indicators:
- `PIPE_NAME`
- Connected processes

## Registry Modules

### RegistryChecks

Windows Registry analysis. Matches can be caused by filename IOCs, keywords, or YARA signatures.

**Sample fields**:
- `KEY`: Full registry key path
- `NAME`: YARA rule or IOC name
- `DESCRIPTION`: Rule description
- `REF`: Reference URL
- `MATCHED_STRINGS`: Content that matched

**Common persistence locations**:
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- Services references
- Scheduled Tasks references
- Keyboard Layout\Preload (language detection)

### SHIMCache

Application compatibility cache (AppCompatCache). Contains valuable execution evidence.

**What it shows**: Full path to executed binaries with timestamps (last execution or creation time, depending on Windows version).

**Sample fields**:
- `ELEMENT`: Executed file path
- `DATE`: Timestamp (interpretation varies by Windows version)
- `TYPE`: system/user
- `HIVEFILE`: Source hive file
- `MD5`, `SHA1`, `SHA256`: Hashes (only if file still exists on disk)

**Key insight**: If hash fields are empty (`-`), the file was executed but is no longer on disk.

**Message enrichment**: If the file is still present, THOR calculates hashes and includes them.

**Reference**: [Count Upon Security - SHIMCache Artifacts](https://countuponsecurity.com/2016/05/18/digital-forensics-shimcache-artifacts/)

### AmCache

Similar to SHIMCache but includes SHA1 hash for executed programs.

**Sample fields**:
- `ELEMENT`: Executed file path
- `SHA1`: Hash from AmCache (not recalculated)
- `SIZE`, `DESC`, `PRODUCT`, `COMPANY`: File metadata
- `FIRST_RUN`: First execution timestamp
- `CREATED`: File creation timestamp

**Advantage over SHIMCache**: Contains SHA1 hash even if file is deleted.

**Reference**: [Swift Forensics - AmCache.hve](http://www.swiftforensics.com/2013/12/amcachehve-in-windows-8-goldmine-for.html)

## Log Modules

### Eventlog
Windows Event Log analysis with Sigma rules.

Key indicators:
- `EVENT_ID`: Windows Event ID
- `CHANNEL`: Log channel (Security, System, etc.)
- `SIGMA_RULE`: Triggered Sigma rule

Common high-value Event IDs:
- 4624/4625: Logon success/failure
- 4688: Process creation
- 7045: Service installation
- 1102: Audit log cleared

### LogScan

Generic log file analysis. Processes `*.log` files line by line.

**What it scans**: Each log line is checked with filename IOCs, keyword IOCs, and "keyword" and "log" type YARA rules.

**Sample fields**:
- `FILE`: Path to the log file
- `LINE`: Line number in the log file
- `ELEMENT`: The matched content
- `PATTERN`: IOC pattern that matched

**Parses**: Apache logs, IIS logs, application logs, any ASCII text log file.

**Note**: THOR performs checks to avoid scanning files that aren't actually ASCII logs despite having `.log` extension.

## Network Modules

### DNSCache
DNS resolver cache analysis.

Key indicators:
- `DNS_NAME`: Queried domain
- `DNS_TYPE`: Record type
- `DNS_DATA`: Resolution result

### NetworkShares
SMB/network share enumeration.

### NetworkSessions
Active network sessions.

### Firewall
Windows Firewall rule analysis.

## Persistence Modules

### Autoruns

Auto-start extensibility points (ASEPs). Uses SysInternals Autorunsc.exe under the hood.

**Sample fields**:
- `LOCATION`: Registry key or file path
- `ENTRY`: Entry name
- `ENABLED`: enabled/disabled
- `CATEGORY`: Drivers, Services, Logon, etc.
- `PROFILE`: System-wide or per-user
- `DESC`, `PUBLISHER`: Software metadata
- `IMAGE_PATH`: Path to executable
- `LAUNCH_STRING`: Command that runs
- `MD5`, `SHA256`: File hashes

**Note**: SHA1 hash from Autorunsc.exe is unreliable and suppressed.

**Covers**: Run keys, services, scheduled tasks, browser extensions, drivers, etc.

**Reference**: [Microsoft Sysinternals Autoruns](https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns)

### ServiceCheck

Windows service analysis. Detects suspicious service entries via anomaly checks, blacklisted keywords, and file path anomalies.

**Sample fields**:
- `KEY`: Service registry key
- `SERVICE_NAME`: Display name
- `IMAGE_PATH`: Path to service binary
- `SHA1`: File hash
- `START_TYPE`: Auto, Manual, OnDemand, etc.
- `USER`: Account service runs as
- `MODIFIED`: Last modification timestamp

**Detection types**:
1. Service binary in typical attacker location
2. YARA rule match in service configuration
3. Blacklisted service names
4. File path anomalies

### ScheduledTasks
Task Scheduler analysis.

Key indicators:
- `TASK_NAME`
- `TASK_ACTION`: What runs
- `TASK_TRIGGER`: When it runs

### WMIStartup
WMI persistence (event subscriptions).

### AtJobs
Legacy AT scheduler jobs.

### Cron (Linux)
Cron job analysis.

## User Modules

### Users
Local user account enumeration.

### UserDir
User profile directory analysis.

### LoggedIn
Currently logged-in users.

### LSASessions
LSA session information.

## Integrity Modules

### Rootkit
Rootkit detection techniques.

### Integritycheck (Linux)
Package manager integrity verification.

### Timestomp
Timestamp manipulation detection.

## Module Selection

Run specific modules only:
```bash
thor64.exe -a Filescan -a ProcessCheck -a Eventlog
```

Disable specific modules:
```bash
thor64.exe --noprocs --noreg --noeventlog
```

## Module Availability by Mode

| Module | Default | Quick | Soft | Intense |
|--------|---------|-------|------|---------|
| Filescan | Yes | Yes | Yes | Yes |
| ProcessCheck | Yes | Yes | No | Yes |
| Eventlog | Yes | No | Yes | Yes |
| MFT | No | No | No | Yes |
| RegistryChecks | Yes | Yes | Yes | Yes |
| Mutex | Yes | Yes | No | Yes |

See THOR documentation for complete matrix.
