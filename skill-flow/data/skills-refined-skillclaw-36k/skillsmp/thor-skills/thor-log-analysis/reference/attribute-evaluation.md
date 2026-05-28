# Attribute Evaluation

Guidance for evaluating specific attributes in THOR findings. Use these questions to assess whether a finding is suspicious or benign.

## File Path Evaluation

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| FILE | In temporary directory? (`C:\Temp`, `AppData\Local\Temp`) | **Bad** | Medium |
| FILE | Contains local language elements? (`Datensicherung`, `Zeiterfassung`) | Good | Medium |
| FILE | Detected on 100+ systems? | Good (FP) | High |
| FILE | Known on Google as goodware? | Good | Medium |
| FILE | Google results show malware/hack tool? | **Bad** | Medium |
| FILE | Google returns no results for path? | **Bad** | Low |
| FILE | In backup or home folder on server? (`G:\Backup2007\`) | Good | Medium |
| FILE | In `%AppData%` folder? | **Bad** | Low |
| FILE | In folder that shouldn't contain executables? (`C:\Windows\Fonts`, `C:\PerfLogs`) | **Bad** | Medium |
| FILE | Looks like admin tool? (`robocopy-migration.exe`) | Good | Low |
| FILE | On mounted/shared network drive? (`\\tsclient\C$`) | **Bad** | Medium |
| FILE | Looks like custom internal software? (`Arbeitszeitnachweis`) | Good | Medium |
| FILE | Directly in folder typically empty? (`C:\ProgramData\1.exe`) | **Bad** | Medium |
| FILE | Modified by user to bypass filters? (`ChromePortable.txt`) | Good | Low |

## Hash Evaluation

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| MD5/SHA1/SHA256 | VT shows unknown? | Neutral | - |
| MD5/SHA1/SHA256 | VT shows > 2 matches (suspicious)? | **Bad** | High |
| MD5/SHA1/SHA256 | VT shows > 10 matches (malicious)? | **Bad** | High |
| MD5/SHA1/SHA256 | VT shows names with `.vir` extension or hash names? | **Bad** | Low |
| MD5/SHA1/SHA256 | VT first submission > 7 years ago? | Good | Low |
| MD5/SHA1/SHA256 | VT has negative votes/comments? | **Bad** | Medium |
| MD5/SHA1/SHA256 | AV names contain `Hack`, `Scan`, `Dump`, `Password`, `Webshell`? | **Bad** | High |
| MD5/SHA1/SHA256 | In Microsoft software catalogue? | Good | High |
| MD5/SHA1/SHA256 | VT shows "probably harmless"? | Good | High |
| MD5/SHA1/SHA256 | Valid signature from trusted vendor? | Good | Medium |
| MD5/SHA1/SHA256 | Listed file names are all legitimate? | Good | Low |
| MD5/SHA1/SHA256 | Listed file names are hash values? | **Bad** | Low |
| MD5/SHA1/SHA256 | PE compilation timestamp > 10 years old? | Good | Low |

## FileScan-Specific Attributes

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| SIZE | 0 bytes? (AV cleaned) | Good | High |
| FIRSTBYTES | Contains native language words? (`@ECHO OFF ECHO "Übertragung`) | Good | High |
| FIRSTBYTES | Contains executables/CLI tools? (`@echo off net user`) | **Bad** | Medium |
| OWNER | Typical user account? (`DOM\user123`) | Good | Low |
| OWNER | `BUILTIN\Administrators`? | Neutral | - |
| OWNER | Contains IIS or service name? (`IIS_USRS`, `tomcat`) | **Bad** | Medium |
| TYPE | Matches extension? | If No → **Bad** | Low |
| TYPE | EXE but extension looks benign? (`.txt`, `.pdf`) | **Bad** | Medium |
| COMPANY | Matches expected value? (`cmd.exe` should say `Microsoft`) | If No → **Bad** | Medium |
| DESC | Matches expected value? | If No → **Bad** | Low |
| CREATED/MODIFIED | Very far in the past? | Good | Low |
| CREATED/MODIFIED | On a Sunday? | **Bad** | Medium |

## FileScan REASON Evaluation

| Pattern | Question | If Yes → | Weight |
|---------|----------|----------|--------|
| REASON_1 | Only a filename pattern match? | Good (prone to FP) | Low |
| REASON_2 | User changed extension to avoid filters? (`Chrome-Portable.exe.txt`) | Good | Medium |
| ... | In backup folder from old Windows? (`F:\WinNT35\`) | Good | Medium |
| ... | Suspicious unsigned `javaw.exe` in software folder? | Good | Medium |
| ... | Rule starts with `VUL_` (vulnerability)? | Good | Medium |
| ... | Hack tool in typical location? (`/usr/bin/ncat`) | Good | Medium |

## SHIMCache / AmCache Attributes

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| ELEMENT | See File Path Evaluation above | | |
| MD5/SHA1/SHA256 | Hash field empty? (file no longer on disk) | Neutral | - |
| DATE/FIRST_RUN | Very recent timestamp? | **Bad** | Low |

## ProcessCheck Attributes

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| PATH | In typical attacker/temp location? | **Bad** | Medium |
| COMMAND | Contains suspicious parameters? | **Bad** | Medium |
| PARENT | Unusual parent process? | **Bad** | Medium |
| OWNER | Running as SYSTEM but shouldn't be? | **Bad** | Medium |
| CONNECTION | To suspicious GeoIP region? | **Bad** | Medium |
| CONNECTION | To region same as system location? | Good | Low |
| RULE | Memory-only detection? | **Bad** | High |

## ServiceCheck Attributes

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| IMAGE_PATH | In typical attacker location? | **Bad** | High |
| IMAGE_PATH | In user `%AppData%` folder? | **Bad** | Medium |
| SERVICE_NAME | Random/GUID-like name? | **Bad** | Medium |
| USER | Running as LocalSystem for no reason? | **Bad** | Low |
| START_TYPE | Auto start but service unknown? | **Bad** | Low |

## Autoruns Attributes

| Attribute | Question | If Yes → | Weight |
|-----------|----------|----------|--------|
| LOCATION | Standard Run key? | Neutral | - |
| LOCATION | Unusual persistence location? | **Bad** | Medium |
| IMAGE_PATH | Points to temp folder? | **Bad** | High |
| ENABLED | Disabled entry? | Good | Low |
| PUBLISHER | Unknown or empty? | **Bad** | Low |

## Using This Reference

1. Look at the MODULE in your THOR finding
2. Find the relevant section above
3. Work through applicable questions
4. Weight the answers
5. Make a determination: FP or investigate further

**Remember**: A single "Bad" indicator doesn't necessarily mean malicious. Look at the overall picture and combine multiple indicators.
