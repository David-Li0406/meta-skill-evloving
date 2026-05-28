# Scoring and Priorities

## Score Levels

THOR uses an additive scoring system. Multiple indicators on the same element accumulate.

| Level | Score Range | Meaning |
|-------|-------------|---------|
| Notice | 40-59 | Low confidence, worth investigating |
| Warning | 60-80 | Medium confidence, likely suspicious |
| Alert | 81+ | High confidence, likely malicious |

Default thresholds can be adjusted:
```bash
--notice 40 --warning 60 --alert 81
```

v11 adds an Info level (default score 30) for lower-priority findings:
```bash
--info 30
```

## Triage Priority

1. **Alerts first** – High-confidence malicious findings
2. **Warnings second** – Medium-confidence suspicious activity
3. **High-signal Notices** – YARA matches, known-bad hashes
4. **Low-signal Notices** – Anomaly scores, generic patterns

## Key Output Fields

| Field | Description |
|-------|-------------|
| `TARGET` | File path or element that matched |
| `SCORE` | Total accumulated score |
| `NAME` | Rule or signature name |
| `DESCRIPTION` | What the detection means |
| `MATCHING_STRINGS` | Content that triggered the match |
| `TAGS` | MITRE ATT&CK or classification tags |
| `CHUNK_OFFSET` | Byte offset (memory/dump scans) |
| `MODULE` | Which THOR module generated the finding |
| `REASON_1`, `REASON_2`, etc. | Individual scoring reasons |

## Score Accumulation

Scores accumulate from multiple indicators:
- Base YARA match: typically 70-100
- Suspicious filename: +20-40
- Suspicious location: +10-30
- Suspicious timestamp: +35 (epoch match)
- Known-bad hash: +100

Example: A file might score 125 from:
- YARA match: 75
- Suspicious path: 30
- Epoch timeframe: 20

## Detection Types

### YARA Matches
Pattern-based file content detection. Highest signal.

Key fields: `NAME`, `MATCHING_STRINGS`, `TAGS`

#### Looking Up YARA Rules in Valhalla

When you see a YARA match, you can look up the rule in Nextron's Valhalla rule database:

**URL pattern:**
```
https://valhalla.nextron-systems.com/info/rule/<RULE_NAME>
```

**Example**: For a match named `HKTL_Mimikatz_MemoryModule`:
```
https://valhalla.nextron-systems.com/info/rule/HKTL_Mimikatz_MemoryModule
```

**What Valhalla shows:**
- Rule description and purpose
- Detection quality (experimental, emerging, stable)
- MITRE ATT&CK mapping
- Related samples and references
- False positive guidance
- When the rule was added/modified

This is invaluable for assessing whether a detection is:
- A known false positive pattern
- A high-confidence threat indicator
- An experimental rule needing verification

### Sigma Matches
Log/event-based detection rules. Applied to Eventlog, log files.

Default minimum level: high (production), medium (lab mode).

Key fields: `SIGMA_RULE`, `SIGMA_LEVEL`, `SIGMA_TAGS`

### IOC Matches
Known indicators: hashes, IPs, domains, filenames.

Key fields: `MATCH_TYPE`, `MATCH_VALUE`, `IOC_SOURCE`

### Anomaly Detection
Behavioral scoring for suspicious characteristics.

Examples:
- Executable in unexpected location
- Hidden file with execution permissions
- Timestomping indicators
- Unsigned executable in system folder

### Tesseract Anomalies (v11)
ML-based outlier detection for "unusual" files.

Key fields: `TESSERACT_SCORE`, `TESSERACT_REASON`

## Grouping Findings

When analyzing results, group by:

1. **By target file/path** – See all indicators for one element
2. **By detection type** – YARA vs Sigma vs IOC
3. **By module** – Filescan vs Eventlog vs ProcessCheck
4. **By signature family** – APT groups, malware families
5. **By MITRE ATT&CK tag** – Technique-based grouping

## Recommended Analysis Workflow

### Step 1: Sort by Score

Start with highest-scoring events and work down to score 80:

```
Alerts (81+) → Warnings (60-80) → then switch to module-based
```

### Step 2: Analyze by Module

After processing high scores, switch to module-based analysis:

1. Select a module (e.g., FileScan)
2. Choose characteristic columns (e.g., FILE, MAIN_REASON)
3. Process remaining findings for that module
4. Repeat for next module

### Key Insight: Quantity vs Relevance

**High detection count = Lower relevance** (opposite of firewall logs)

| Count | Interpretation |
|-------|---------------|
| 1-5 endpoints | Likely significant, investigate |
| 5-30 endpoints | Could be targeted or FP, verify |
| 100+ endpoints | Almost certainly FP |

Exception: Confirmed widespread campaigns

## Score Adjustment

Use `--allreasons` to see all contributing factors:
```bash
thor64.exe --allreasons -p /path
```

Epoch scoring boost for attacker activity timeframe:
```bash
--epoch 2024-01-15 --epochscore 35
```

Files modified around the specified date get +35 score boost.
