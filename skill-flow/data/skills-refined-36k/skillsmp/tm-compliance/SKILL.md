---
name: tm-compliance
description: Map threats and controls to compliance frameworks like OWASP Top 10, SOC2, PCI-DSS, HIPAA, GDPR. Generates compliance reports with coverage percentages and gaps. Use when checking compliance status, mapping to security frameworks, or generating audit documentation.
allowed-tools: Read, Write, Glob
---

# Compliance Mapping

## Purpose

Map your threat model to compliance frameworks to:

- Calculate compliance coverage percentages
- Identify compliance gaps
- Generate audit-ready documentation
- Track requirements across multiple frameworks

## Usage

```
/tm-compliance [--framework <name>] [--policy <path>] [--gaps-only]
```

**Arguments**:
- `--framework`: Framework(s) to map: owasp, soc2, pci-dss, hipaa, gdpr, custom
- `--policy`: Path to custom policy document
- `--gaps-only`: Only show gaps/non-compliance

## Supported Frameworks

### OWASP Top 10 2021
| ID | Name |
|----|------|
| A01 | Broken Access Control |
| A02 | Cryptographic Failures |
| A03 | Injection |
| A04 | Insecure Design |
| A05 | Security Misconfiguration |
| A06 | Vulnerable and Outdated Components |
| A07 | Identification and Authentication Failures |
| A08 | Software and Data Integrity Failures |
| A09 | Security Logging and Monitoring Failures |
| A10 | Server-Side Request Forgery (SSRF) |

### SOC2 Trust Services Criteria
| Category | Description |
|----------|-------------|
| CC6.1 | Logical and Physical Access Controls |
| CC6.2 | System Access Authentication |
| CC6.3 | Access Restriction and Privileges |
| CC6.6 | System Boundaries |
| CC6.7 | Transmission Integrity |
| CC6.8 | Data Integrity |
| CC7.1 | Configuration Management |
| CC7.2 | Change Management |

### PCI-DSS v4.0
| Requirement | Description |
|-------------|-------------|
| 1 | Install and maintain network security controls |
| 2 | Apply secure configurations |
| 3 | Protect stored account data |
| 4 | Protect cardholder data during transmission |
| 5 | Protect from malicious software |
| 6 | Develop and maintain secure systems |
| 7 | Restrict access by business need |
| 8 | Identify users and authenticate access |
| 9 | Restrict physical access |
| 10 | Log and monitor access |
| 11 | Test security regularly |
| 12 | Support information security with policies |

## Mapping Process

### For Each Framework Requirement

1. **Identify related threats**
   - Match requirement to STRIDE categories
   - Find threats in those categories

2. **Identify related controls**
   - Find controls that mitigate related threats
   - Check control implementation status

3. **Assess compliance status**
   - `compliant`: All related controls implemented
   - `partial`: Some controls implemented
   - `non-compliant`: No controls or all missing

4. **Document evidence**
   - Link to verified controls
   - Note gaps

## Output Files

### compliance.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "frameworks": [
    {
      "name": "OWASP Top 10 2021",
      "version": "2021",
      "overall_compliance": 82,
      "mappings": [
        {
          "requirement_id": "A01:2021",
          "requirement_name": "Broken Access Control",
          "description": "Restrictions on authenticated users not properly enforced",
          "stride_categories": ["elevation-of-privilege", "information-disclosure"],
          "related_threats": ["threat-010", "threat-011"],
          "related_controls": ["control-020", "control-021"],
          "status": "partial",
          "coverage": 85,
          "gaps": ["gap-005"],
          "evidence": [
            "RBAC implemented in src/middleware/authorize.ts",
            "Missing: Object-level authorization"
          ]
        }
      ]
    }
  ]
}
```

### compliance-report.md (Visual Report)
```markdown
# Compliance Report

**Generated**: [Date]
**Frameworks**: OWASP Top 10 2021, SOC2

## Executive Summary

```
COMPLIANCE OVERVIEW
═══════════════════════════════════════════════════════════

OWASP Top 10 2021
─────────────────────────────────────────────────────────
A01 Broken Access Control:     ████████░░ 85%   (1 gap)
A02 Cryptographic Failures:    ██████████ 100%
A03 Injection:                 ███████░░░ 70%   (3 gaps)
A04 Insecure Design:           ██████░░░░ 55%   (5 gaps)
A05 Security Misconfiguration: █████████░ 95%   (1 gap)
A06 Vulnerable Components:     █████████░ 90%   (1 gap)
A07 Auth Failures:             ████████░░ 75%   (4 gaps)
A08 Data Integrity Failures:   ████████░░ 85%   (2 gaps)
A09 Logging Failures:          ████████░░ 80%   (2 gaps)
A10 SSRF:                      ██████████ 100%
─────────────────────────────────────────────────────────
OVERALL:                       ████████░░ 82%

SOC2 Trust Services
─────────────────────────────────────────────────────────
CC6.1 Logical Access:          █████████░ 90%   (1 gap)
CC6.2 Authentication:          ████████░░ 80%   (2 gaps)
CC6.3 Access Restriction:      █████████░ 95%   (1 gap)
─────────────────────────────────────────────────────────
OVERALL:                       █████████░ 88%
```

## OWASP Top 10 2021

### A01:2021 - Broken Access Control

```
┌─────────────────────────────────────────────────────────┐
│ STATUS: ⚠ Partial (85%)                                 │
├─────────────────────────────────────────────────────────┤
│ RELATED THREATS:                                        │
│   • THREAT-010: IDOR in user profile                    │
│   • THREAT-011: Missing function-level access control   │
│                                                         │
│ CONTROLS:                                               │
│   ✓ RBAC implementation                                 │
│   ⚠ Object-level authorization (partial)               │
│                                                         │
│ GAPS:                                                   │
│   • GAP-005: Missing object-level checks                │
│                                                         │
│ EVIDENCE:                                               │
│   src/middleware/authorize.ts:15-89                     │
└─────────────────────────────────────────────────────────┘
```

### A02:2021 - Cryptographic Failures

```
┌─────────────────────────────────────────────────────────┐
│ STATUS: ✓ Compliant (100%)                              │
├─────────────────────────────────────────────────────────┤
│ CONTROLS:                                               │
│   ✓ TLS 1.3 enforced                                    │
│   ✓ AES-256 encryption at rest                          │
│   ✓ Bcrypt password hashing                             │
│                                                         │
│ EVIDENCE:                                               │
│   src/config/tls.ts:5                                   │
│   src/db/encryption.ts:12                               │
└─────────────────────────────────────────────────────────┘
```

[Additional requirements...]
```

## STRIDE to Framework Mapping

### OWASP Top 10
| STRIDE Category | OWASP Requirements |
|-----------------|-------------------|
| Spoofing | A07 |
| Tampering | A03, A08 |
| Repudiation | A09 |
| Information Disclosure | A01, A02 |
| Denial of Service | A05 |
| Elevation of Privilege | A01, A04 |

### SOC2
| STRIDE Category | SOC2 Criteria |
|-----------------|---------------|
| Spoofing | CC6.1, CC6.2 |
| Tampering | CC6.7, CC6.8 |
| Repudiation | CC7.2 |
| Information Disclosure | CC6.1, CC6.3 |
| Denial of Service | CC6.6 |
| Elevation of Privilege | CC6.3 |

## Instructions for Claude

When executing this skill:

1. **Load threat model state**:
   - Read `.threatmodel/state/threats.json`
   - Read `.threatmodel/state/controls.json`
   - Read `.threatmodel/state/gaps.json`

2. **Load framework definitions**:
   - Reference built-in framework mappings
   - Load custom policies if specified

3. **For each framework**:
   - Map requirements to STRIDE categories
   - Find related threats
   - Find related controls
   - Assess coverage

4. **Calculate compliance**:
   - Per-requirement status
   - Per-framework percentage
   - Overall score

5. **Generate reports with visuals IN THE FILES**:
   - JSON for programmatic use
   - Markdown with ASCII progress bars, status boxes, and visual indicators
   - The compliance-report.md MUST include:
     - Visual progress bars: `████████░░ 85%`
     - Status indicators: `✓`, `⚠`, `✗`
     - Visual box frames for each requirement
   - These visuals go in the written file, not just console output

6. **Console summary** (also display to user):
   ```
   Compliance Mapping Complete
   ===========================

   Frameworks Analyzed: 2

   OWASP Top 10 2021:
     A01 Broken Access Control:     ████████░░ 85%  (1 gap)
     A02 Cryptographic Failures:    ██████████ 100%
     A03 Injection:                 ███████░░░ 70%  (3 gaps)
     ...
     Overall: 82%

   SOC2 Trust Services:
     CC6.1 Logical Access:          █████████░ 90%  (1 gap)
     CC6.2 Authentication:          ████████░░ 80%  (2 gaps)
     ...
     Overall: 88%

   Total Gaps: 11
     High Priority: 4
     Medium Priority: 5
     Low Priority: 2

   Files Created:
     .threatmodel/state/compliance.json
     .threatmodel/reports/compliance-report.md

   Next Steps:
     Run /tm-report to generate full risk report
   ```

## Reference Files

- [OWASP Top 10 2021](../../shared/frameworks/owasp-top10-2021.md)
- [STRIDE Framework](../../shared/frameworks/stride.md)
