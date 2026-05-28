---
name: tm-status
description: Show current threat model status including asset counts, threat distribution, control verification status, and compliance coverage. Use when checking threat model status, getting overview of security posture, or reviewing current state.
allowed-tools: Read, Glob
---

# Threat Model Status

## Purpose

Display a comprehensive overview of the current threat model state:

- Asset and component counts
- Threat distribution by severity
- Control verification status
- Gap summary
- Compliance coverage
- Baseline comparison

## Usage

```
/tm-status [--format text|json] [--section <name>]
```

**Arguments**:
- `--format`: Output format (default: text)
- `--section`: Show specific section only (discovery, threats, controls, compliance)

## Status Sections

### Discovery Summary
- Total assets by type
- Total data flows
- Trust boundaries defined
- Attack surface entries

### Threat Summary
- Total threats
- Distribution by severity
- Distribution by STRIDE category
- Unmitigated threats count

### Control Summary
- Total required controls
- Implemented vs partial vs missing
- Verification status
- Recent changes

### Gap Summary
- Total gaps
- Distribution by severity
- Top priority gaps

### Compliance Summary
- Coverage by framework
- Critical compliance gaps

### Baseline Comparison
- Days since last baseline
- Changes since baseline

## Output Format

### Text Output
```
═══════════════════════════════════════════════════════════════
                    THREAT MODEL STATUS
═══════════════════════════════════════════════════════════════

Project: My Application v1.0.0
Framework: STRIDE
Last Updated: 2025-01-20 14:30:00
Baseline: 2025-01-15 (5 days ago)

───────────────────────────────────────────────────────────────
                       DISCOVERY
───────────────────────────────────────────────────────────────

Assets: 14 total
  ├── Data Stores:    3  ████████████░░░░░░░░  21%
  ├── Services:       6  ████████████████████░  43%
  ├── Clients:        3  ████████████░░░░░░░░  21%
  └── Integrations:   2  ████████░░░░░░░░░░░░  14%

Data Flows: 22 total
  └── Crossing trust boundaries: 8 (36%)

Trust Boundaries: 5
  ├── Network:     2
  ├── Privilege:   2
  └── Environment: 1

Attack Surface: 12 entries
  ├── Public:     5  ████████████████░░░░  42%
  ├── Internal:   5  ████████████████░░░░  42%
  └── Restricted: 2  ██████░░░░░░░░░░░░░░  17%

───────────────────────────────────────────────────────────────
                        THREATS
───────────────────────────────────────────────────────────────

Total: 47 threats

By Severity:
  ├── Critical:  5  ██████░░░░░░░░░░░░░░  11%
  ├── High:     12  ████████████░░░░░░░░  26%
  ├── Medium:   18  ██████████████████░░  38%
  └── Low:      12  ████████████░░░░░░░░  26%

By STRIDE Category:
  ├── Spoofing:              8
  ├── Tampering:            10
  ├── Repudiation:           4
  ├── Information Disclosure: 9
  ├── Denial of Service:     7
  └── Elevation of Privilege: 9

Unmitigated Critical Threats: 3
  1. THREAT-001: Credential Stuffing (8.5)
  2. THREAT-002: SQL Injection (8.2)
  3. THREAT-003: JWT Token Theft (8.0)

───────────────────────────────────────────────────────────────
                       CONTROLS
───────────────────────────────────────────────────────────────

Total Required: 29

Implementation Status:
  ├── Implemented: 18  ████████████████████░  62%
  ├── Partial:      7  ████████░░░░░░░░░░░░  24%
  └── Missing:      4  █████░░░░░░░░░░░░░░░  14%

Verification Status:
  ├── Verified:   18  ████████████████████░  62%
  ├── Unverified:  7  ████████░░░░░░░░░░░░  24%
  └── Failed:      4  █████░░░░░░░░░░░░░░░  14%

───────────────────────────────────────────────────────────────
                         GAPS
───────────────────────────────────────────────────────────────

Total: 11 gaps

By Severity:
  ├── Critical: 2  ████░░░░░░░░░░░░░░░░  18%
  ├── High:     4  ████████░░░░░░░░░░░░  36%
  ├── Medium:   3  ██████░░░░░░░░░░░░░░  27%
  └── Low:      2  ████░░░░░░░░░░░░░░░░  18%

Top Priority Gaps:
  1. [CRITICAL] GAP-001: MFA not enforced
  2. [CRITICAL] GAP-002: SQL injection in legacy
  3. [HIGH] GAP-003: Rate limiting missing
  4. [HIGH] GAP-004: Session fixation

───────────────────────────────────────────────────────────────
                      COMPLIANCE
───────────────────────────────────────────────────────────────

OWASP Top 10 2021:
  Overall: 82%
  ├── A01 Access Control:    85%  █████████░░░
  ├── A02 Crypto Failures:  100%  ████████████
  ├── A03 Injection:         70%  ████████░░░░
  ├── A04 Insecure Design:   55%  ██████░░░░░░
  └── ...

SOC2:
  Overall: 88%
  ├── CC6.1 Access:          90%  ███████████░
  ├── CC6.2 Auth:            80%  ██████████░░
  └── ...

───────────────────────────────────────────────────────────────
                     RECOMMENDATIONS
───────────────────────────────────────────────────────────────

Immediate Actions:
  1. [CRITICAL] Implement MFA enforcement
  2. [CRITICAL] Fix SQL injection in legacy module
  3. [HIGH] Add rate limiting to password reset
  4. [HIGH] Fix session fixation vulnerability

───────────────────────────────────────────────────────────────
                      QUICK ACTIONS
───────────────────────────────────────────────────────────────

/tm-threats --focus asset-015    Analyze new assets
/tm-verify --thorough            Deep verification
/tm-report                       Generate full report
/tm-drift --create-baseline      Create new baseline

═══════════════════════════════════════════════════════════════
```

### JSON Output
```json
{
  "project": {
    "name": "My Application",
    "version": "1.0.0",
    "framework": "STRIDE",
    "last_updated": "2025-01-20T14:30:00Z"
  },
  "discovery": {
    "assets": {
      "total": 14,
      "by_type": {
        "data-store": 3,
        "service": 6,
        "client": 3,
        "integration": 2
      }
    },
    "dataflows": {
      "total": 22,
      "crossing_boundaries": 8
    },
    "trust_boundaries": 5,
    "attack_surface": {
      "total": 12,
      "by_exposure": {
        "public": 5,
        "internal": 5,
        "restricted": 2
      }
    }
  },
  "threats": {
    "total": 47,
    "by_severity": {
      "critical": 5,
      "high": 12,
      "medium": 18,
      "low": 12
    },
    "by_category": {
      "spoofing": 8,
      "tampering": 10,
      "repudiation": 4,
      "information-disclosure": 9,
      "denial-of-service": 7,
      "elevation-of-privilege": 9
    },
    "unmitigated_critical": 3
  },
  "controls": {
    "total": 29,
    "by_status": {
      "implemented": 18,
      "partial": 7,
      "missing": 4
    },
    "verification": {
      "verified": 18,
      "unverified": 7,
      "failed": 4
    }
  },
  "gaps": {
    "total": 11,
    "by_severity": {
      "critical": 2,
      "high": 4,
      "medium": 3,
      "low": 2
    }
  },
  "compliance": {
    "owasp": {
      "overall": 82,
      "gaps": 5
    },
    "soc2": {
      "overall": 88,
      "gaps": 3
    }
  },
  "baseline": {
    "date": "2025-01-15",
    "days_ago": 5,
    "changes_since": {
      "assets_added": 2,
      "threats_added": 5,
      "controls_changed": 2
    }
  }
}
```

## Instructions for Claude

When executing this skill:

1. **Check for threat model**:
   - Look for `.threatmodel/` directory
   - If not found, report and suggest `/tm-init`

2. **Load all state files**:
   - Read assets.json, dataflows.json, etc.
   - Read config.yaml for project info
   - Check for baseline files

3. **Calculate statistics**:
   - Count items in each category
   - Calculate percentages
   - Identify top items

4. **Format output**:
   - Use box drawing characters for text
   - Include progress bars for percentages
   - Highlight critical items

5. **Provide recommendations**:
   - Based on current state
   - Suggest next actions

6. **Display status**:
   ```
   [Display formatted status output as shown above]
   ```

## Edge Cases

### No Threat Model
```
═══════════════════════════════════════════════════════════════
                    THREAT MODEL STATUS
═══════════════════════════════════════════════════════════════

No threat model found in current directory.

───────────────────────────────────────────────────────────────
                     GETTING STARTED
───────────────────────────────────────────────────────────────

OPTION 1: Run everything at once (recommended)

  /tm-full --docs ./path/to/docs

OPTION 2: Run step by step

  1. /tm-init --docs ./path/to/docs    Initialize & discover assets
  2. /tm-threats                        Analyze threats (STRIDE)
  3. /tm-verify                         Check controls in code
  4. /tm-compliance --framework owasp   Map to compliance frameworks
  5. /tm-report                         Generate reports

───────────────────────────────────────────────────────────────
                     WHAT IS --docs?
───────────────────────────────────────────────────────────────

Point --docs to a folder containing your architecture documentation:

  - README.md with system overview
  - Architecture diagrams or descriptions
  - API specifications (OpenAPI, GraphQL schemas)
  - Infrastructure-as-code (Terraform, CloudFormation)
  - Database schemas
  - Any markdown files describing your system

Examples:
  /tm-init --docs ./docs
  /tm-init --docs ./architecture
  /tm-init --docs ./design

The toolkit will read these files to understand your system
and automatically discover assets, data flows, and trust boundaries.

═══════════════════════════════════════════════════════════════
```

### Partial State
```
═══════════════════════════════════════════════════════════════
                    THREAT MODEL STATUS
═══════════════════════════════════════════════════════════════

Warning: Incomplete threat model

───────────────────────────────────────────────────────────────
                        COMPLETED
───────────────────────────────────────────────────────────────
  ✓ assets.json: 14 assets
  ✓ dataflows.json: 22 flows

───────────────────────────────────────────────────────────────
                      NOT YET RUN
───────────────────────────────────────────────────────────────
  ✗ threats.json     → Run /tm-threats
  ✗ controls.json    → Run /tm-verify
  ✗ compliance.json  → Run /tm-compliance

───────────────────────────────────────────────────────────────
                       NEXT STEP
───────────────────────────────────────────────────────────────

Run the next phase:
  /tm-threats

Or run everything remaining:
  /tm-full --continue

═══════════════════════════════════════════════════════════════
```
