---
name: tm-threats
description: Analyze threats against discovered assets using STRIDE or PASTA framework. Generates threat catalog, attack trees, abuse cases, and risk register. Use when analyzing threats, identifying attack vectors, assessing security risks, or expanding threat catalog.
allowed-tools: Read, Write, Glob, Grep
---

# Threat Analysis

## Purpose

Systematically identify and analyze threats against your system using established threat modeling frameworks. This skill:

- Applies STRIDE methodology to each component
- Generates comprehensive threat catalog
- Builds attack trees for critical threats
- Identifies abuse cases from legitimate functionality
- Creates prioritized risk register

## Usage

```
/tm-threats [--framework stride|pasta] [--focus <asset-id>] [--depth quick|standard|deep] [--include-abuse]
```

**Arguments**:
- `--framework`: Threat framework (default: stride)
- `--focus`: Analyze specific asset only
- `--depth`: Analysis depth
- `--include-abuse`: Generate abuse cases from sequences

## Prerequisites

Requires initialized threat model. Run `/tm-init` first if `.threatmodel/` doesn't exist.

## STRIDE Analysis Process

### For Each Asset

Apply STRIDE categories based on asset type:

| Asset Type | S | T | R | I | D | E |
|------------|---|---|---|---|---|---|
| External Entity | ✓ | | ✓ | | | |
| Process/Service | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Store | | ✓ | ✓ | ✓ | ✓ | |
| Data Flow | | ✓ | | ✓ | ✓ | |

### For Each Trust Boundary Crossing

Analyze threats for data flows crossing trust boundaries:

1. **Spoofing**: Can the source be impersonated?
2. **Tampering**: Can the data be modified in transit?
3. **Repudiation**: Can the action be denied?
4. **Information Disclosure**: Can the data be intercepted?
5. **Denial of Service**: Can the flow be disrupted?
6. **Elevation of Privilege**: Can privileges be escalated?

### For Each Attack Surface Entry

Analyze exposed entry points:

1. What authentication is required?
2. What authorization is enforced?
3. What input validation exists?
4. What rate limiting is applied?
5. What data is exposed?

## Risk Scoring

### Likelihood Scale (1-5)
| Score | Level | Description |
|-------|-------|-------------|
| 1 | Rare | Requires significant resources, unlikely to occur |
| 2 | Unlikely | Difficult but possible with moderate resources |
| 3 | Possible | Achievable with common tools and moderate skill |
| 4 | Likely | Easy to exploit with readily available tools |
| 5 | Almost Certain | Trivial to exploit, may already be happening |

### Impact Scale (1-5)
| Score | Level | Description |
|-------|-------|-------------|
| 1 | Negligible | Minor inconvenience, no data loss |
| 2 | Minor | Limited data exposure, quick recovery |
| 3 | Moderate | Significant data exposure, business disruption |
| 4 | Major | Large scale data breach, major business impact |
| 5 | Severe | Complete system compromise, existential threat |

### Risk Score = Likelihood × Impact

| Risk Score | Level |
|------------|-------|
| 1-4 | Low |
| 5-9 | Medium |
| 10-15 | High |
| 16-25 | Critical |

## Output Files

### threats.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "framework": "STRIDE",
  "threats": [
    {
      "id": "threat-001",
      "title": "Credential Stuffing Attack",
      "category": "spoofing",
      "framework": "STRIDE",
      "description": "Attacker uses leaked credentials to gain unauthorized access",
      "target": {
        "asset_id": "asset-002",
        "attack_surface_id": "as-001",
        "entry_point": "/api/auth/login"
      },
      "threat_actor": "external-attacker",
      "prerequisites": ["Leaked credential database", "Knowledge of login endpoint"],
      "impact": {
        "confidentiality": "high",
        "integrity": "medium",
        "availability": "low"
      },
      "likelihood": "likely",
      "risk_score": 16,
      "risk_level": "critical",
      "mitre_attack": ["T1110.004"],
      "cwe": ["CWE-307", "CWE-521"],
      "countermeasures": ["control-001", "control-002"]
    }
  ]
}
```

### attack-trees.json
```json
{
  "version": "1.0",
  "trees": [
    {
      "id": "at-001",
      "threat_id": "threat-001",
      "goal": "Gain unauthorized access to user accounts",
      "root": {
        "description": "Compromise user account",
        "type": "or",
        "children": [
          {
            "description": "Credential stuffing",
            "type": "and",
            "children": [
              {"description": "Obtain leaked credentials", "type": "leaf", "difficulty": "low"},
              {"description": "Bypass rate limiting", "type": "leaf", "difficulty": "medium"}
            ]
          },
          {"description": "Phishing attack", "type": "leaf", "difficulty": "medium"}
        ]
      }
    }
  ]
}
```

### risk-register.json
```json
{
  "version": "1.0",
  "generated": "ISO-8601",
  "entries": [
    {
      "id": "risk-001",
      "threat_id": "threat-001",
      "title": "Credential Stuffing Attack",
      "category": "authentication",
      "likelihood": {"score": 4, "rationale": "Common attack, tools readily available"},
      "impact": {"score": 4, "rationale": "Account takeover leads to data breach"},
      "inherent_risk_score": 16,
      "inherent_risk_level": "critical",
      "treatment": "mitigate",
      "treatment_plan": "Implement MFA and improve rate limiting",
      "owner": "security-team",
      "status": "open"
    }
  ]
}
```

## Common Threat Patterns

### Authentication Threats (Spoofing)
- Credential stuffing
- Brute force attacks
- Session hijacking
- Token theft
- Password spraying

### Data Integrity Threats (Tampering)
- SQL injection
- Parameter tampering
- Man-in-the-middle
- File upload attacks
- Configuration tampering

### Audit Threats (Repudiation)
- Missing audit logs
- Log tampering
- Insufficient logging

### Confidentiality Threats (Information Disclosure)
- Data leaks in errors
- Directory traversal
- Insecure direct object references
- Excessive data exposure

### Availability Threats (Denial of Service)
- Resource exhaustion
- Algorithmic complexity
- DDoS attacks

### Authorization Threats (Elevation of Privilege)
- Broken access control
- Privilege escalation
- IDOR vulnerabilities

## Instructions for Claude

When executing this skill:

1. **Load existing threat model state**:
   - Read `.threatmodel/state/assets.json`
   - Read `.threatmodel/state/dataflows.json`
   - Read `.threatmodel/state/trust-boundaries.json`
   - Read `.threatmodel/state/attack-surface.json`

2. **Apply STRIDE systematically**:
   - For each asset, consider applicable STRIDE categories
   - For each trust boundary crossing, analyze all categories
   - For each attack surface entry, identify threats

3. **Generate threat entries**:
   - Create unique IDs (threat-001, threat-002, etc.)
   - Write clear descriptions
   - Identify prerequisites
   - Assess impact (CIA triad)
   - Estimate likelihood
   - Calculate risk score
   - Map to MITRE ATT&CK and CWE where applicable

4. **Build attack trees for critical threats**:
   - Create tree for threats with risk_score >= 12
   - Show attack paths as AND/OR trees

5. **Generate abuse cases** (if --include-abuse):
   - Review sequence diagrams
   - Identify how legitimate flows could be misused

6. **Create risk register**:
   - Prioritize by risk score
   - Group by category
   - Assign treatment strategy

7. **Write visual threat report** (`.threatmodel/reports/threat-report.md`):
   ```markdown
   # Threat Analysis Report

   **Generated**: [Date]
   **Framework**: STRIDE

   ## Summary

   ```
   THREAT ANALYSIS
   ═══════════════════════════════════════════════════════════

   Assets Analyzed: 14
   Attack Surfaces Analyzed: 12

   THREATS BY SEVERITY
   ─────────────────────────────────────────────────────────
   CRITICAL │██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  5  (11%)
       HIGH │████████████████████████░░░░░░░░░░░░░░░░│ 12  (26%)
     MEDIUM │████████████████████████████████████░░░░│ 18  (38%)
        LOW │████████████████████████░░░░░░░░░░░░░░░░│ 12  (26%)

   THREATS BY STRIDE CATEGORY
   ─────────────────────────────────────────────────────────
   Spoofing              │████████████████░░░░░░░░░░░░░░░░│  8
   Tampering             │████████████████████░░░░░░░░░░░░│ 10
   Repudiation           │████████░░░░░░░░░░░░░░░░░░░░░░░░│  4
   Information Disclosure│██████████████████░░░░░░░░░░░░░░│  9
   Denial of Service     │██████████████░░░░░░░░░░░░░░░░░░│  7
   Elevation of Privilege│██████████████████░░░░░░░░░░░░░░│  9
   ```

   ## Critical Threats

   ### THREAT-001: Credential Stuffing Attack

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ RISK SCORE: 8.5/10 (CRITICAL)                           │
   ├─────────────────────────────────────────────────────────┤
   │ Category: Spoofing                                      │
   │ Target:   POST /api/auth/login                          │
   │                                                         │
   │ ATTACK VECTOR:                                          │
   │   Automated login attempts with leaked credentials      │
   │                                                         │
   │ IMPACT:                                                 │
   │   Confidentiality: HIGH                                 │
   │   Integrity: MEDIUM                                     │
   │   Availability: LOW                                     │
   │                                                         │
   │ MITRE ATT&CK: T1110.001                                 │
   │ CWE: CWE-307                                            │
   │                                                         │
   │ REQUIRED COUNTERMEASURES:                               │
   │   • Rate limiting on auth endpoints                     │
   │   • Account lockout after failed attempts               │
   │   • MFA enforcement                                     │
   └─────────────────────────────────────────────────────────┘
   ```

   [Additional threats...]
   ```

8. **Console summary** (also display to user):
   ```
   Threat Analysis Complete
   ========================

   Framework: STRIDE
   Assets Analyzed: X
   Attack Surfaces Analyzed: Y

   Threats Identified:
     Critical: N
     High: N
     Medium: N
     Low: N

   Top Critical Threats:
     1. [THREAT-001] Title (Risk: 16)
     2. [THREAT-002] Title (Risk: 15)

   Attack Trees Generated: N
   Abuse Cases Documented: N

   Files Updated:
     .threatmodel/state/threats.json
     .threatmodel/state/attack-trees.json
     .threatmodel/state/risk-register.json
     .threatmodel/reports/threat-report.md

   Next Steps:
     Run /tm-verify to check control implementations
   ```

## Reference Files

- [STRIDE Framework](../../shared/frameworks/stride.md)
- [OWASP Top 10](../../shared/frameworks/owasp-top10-2021.md)
