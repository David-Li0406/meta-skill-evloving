# Analysis Tools

External tools and resources for verifying THOR findings.

## Hash Analysis

### VirusTotal

**URL**: https://www.virustotal.com/gui/

**Use for**: File hashes (MD5, SHA1, SHA256), domains, IPs, file names

**URL patterns**:
```
https://www.virustotal.com/gui/file/<HASH>
https://www.virustotal.com/gui/domain/<DOMAIN>
https://www.virustotal.com/gui/ip-address/<IP>
```

**File name search via Google**:
```
inurl:virustotal.com <filename>
```

**Key indicators to check**:
- Detection ratio (e.g., 0/70, 5/70, 45/70)
- Community score and comments
- "First submission" date (old = more trustworthy if clean)
- "Probably harmless" bar (strong FP indicator)
- Microsoft software catalogue membership
- Additional file names in "Details" tab
- File names containing `.vir` or hash values = suspicious

### Valhalla (YARA Rules)

**URL pattern**:
```
https://valhalla.nextron-systems.com/info/rule/<RULE_NAME>
```

**Use for**: Looking up YARA rule details when THOR reports a match

**Shows**:
- Rule description and purpose
- Detection quality (experimental, emerging, stable)
- MITRE ATT&CK mapping
- False positive guidance
- Related samples

### Munin (Batch Hash Lookup)

**URL**: https://github.com/Neo23x0/munin

**Use for**: Batch processing hash lists from THOR CSVs

```bash
# Combine all THOR CSV outputs
cat *.csv >> all-hashes.csv

# Run munin for batch VT lookups
python munin.py -i config.ini -f all-hashes.csv
```

## Sandbox Analysis

### Hybrid Analysis

**URL**: https://hybrid-analysis.com/

**Use for**: Sample upload, behavior analysis, keyword search

### any.run

**URL**: https://any.run/

**Use for**: Interactive sandbox analysis, see malware execution in real-time

### Joe Sandbox

**URL**: https://www.joesandbox.com/

**Use for**: Deep malware analysis, comprehensive reports

## Static Analysis

### PEStudio

**URL**: https://www.winitor.com/

**Use for**: Initial static assessment of PE files (Windows executables)

**Key features**:
- Imports/exports analysis
- Strings extraction
- Anomaly detection
- VirusTotal integration

### DIE (Detect It Easy)

**Use for**: Identifying packers, compilers, and protectors

### strings / FLOSS

**Use for**: Extracting readable strings from binaries

```bash
strings suspicious.exe | less
floss suspicious.exe  # Also extracts obfuscated strings
```

## Threat Intelligence

### APT Custom Search

**URL**: https://cse.google.com/cse?cx=003248445720253387346:turlh5vi4xc

**Use for**: Searching APT-related sites for indicators

### MISP / OpenCTI

**Use for**: Threat intelligence platforms with IOC sharing

### AlienVault OTX

**URL**: https://otx.alienvault.com/

**Use for**: Free threat intelligence, pulse subscriptions

## Quick Lookup Workflow

### For Hash Findings

1. Copy hash from THOR output
2. Search on VirusTotal
3. Check detection ratio
4. If unknown, consider sandbox submission
5. Check "Community" tab for analyst notes

### For YARA Matches

1. Copy rule name from THOR output
2. Look up on Valhalla
3. Check rule quality and FP guidance
4. Review matched strings in THOR output
5. Correlate with file metadata

### For Domain/IP Findings

1. Search on VirusTotal
2. Check passive DNS history
3. Look for related malware samples
4. Check WHOIS history
5. Search threat intel platforms

## Assessment Checklist

| Check | Good Sign | Bad Sign |
|-------|-----------|----------|
| VT detection ratio | 0/70 | 10+/70 |
| VT first submission | > 7 years ago | Recent or unknown |
| VT community score | Positive votes | Negative votes |
| Microsoft catalogue | Present | Absent |
| Digital signature | Valid, trusted | Invalid or missing |
| Sandbox behavior | Benign | Malicious indicators |
| Compilation timestamp | Old | Very recent or in future |
