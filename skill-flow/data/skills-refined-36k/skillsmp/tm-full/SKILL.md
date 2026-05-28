---
name: tm-full
description: Run the complete threat modeling workflow from initialization through reporting. Orchestrates all other skills in sequence. Use when performing full threat model analysis, running complete security assessment, or generating comprehensive threat documentation.
allowed-tools: Read, Write, Glob, Grep, Bash(mkdir:*), Bash(ls:*)
---

# Full Threat Modeling Workflow

## Purpose

Orchestrate the complete threat modeling workflow in a single command:

1. **Initialize** - Discover assets and architecture
2. **Analyze** - Identify and assess threats
3. **Verify** - Check control implementations
4. **Comply** - Map to frameworks
5. **Report** - Generate comprehensive documentation

## Usage

```
/tm-full [--docs <path>] [--framework stride|pasta] [--compliance <list>] [--output <path>] [--report-level executive|standard|detailed]
```

**Arguments**:
- `--docs`: Path to architecture documentation (default: ./docs)
- `--framework`: Threat framework (default: stride)
- `--compliance`: Compliance frameworks, comma-separated (default: owasp)
- `--output`: Output directory (default: .threatmodel)
- `--report-level`: Report detail level (default: standard)

## Workflow Steps

```
┌─────────────────────────────────────────────────────────────┐
│                    FULL WORKFLOW                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [1/5] INITIALIZATION                                       │
│  ─────────────────────                                      │
│  • Read architecture documentation                          │
│  • Extract assets and classify                              │
│  • Map data flows                                           │
│  • Identify trust boundaries                                │
│  • Catalog attack surface                                   │
│  • Generate architecture diagrams                           │
│                                                             │
│  Output: assets.json, dataflows.json, trust-boundaries.json │
│          attack-surface.json, diagrams/*.mmd                │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [2/5] THREAT ANALYSIS                                      │
│  ─────────────────────                                      │
│  • Apply STRIDE to each component                           │
│  • Enumerate threats per attack surface                     │
│  • Build attack trees for critical threats                  │
│  • Assess likelihood and impact                             │
│  • Calculate risk scores                                    │
│  • Create risk register                                     │
│                                                             │
│  Output: threats.json, attack-trees.json, risk-register.json│
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [3/5] CONTROL VERIFICATION                                 │
│  ─────────────────────────                                  │
│  • Identify required controls                               │
│  • Search codebase for implementations                      │
│  • Verify configurations                                    │
│  • Collect evidence                                         │
│  • Document gaps                                            │
│                                                             │
│  Output: controls.json, gaps.json, verification.json        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [4/5] COMPLIANCE MAPPING                                   │
│  ───────────────────────                                    │
│  • Map threats to framework requirements                    │
│  • Map controls to requirements                             │
│  • Calculate coverage percentages                           │
│  • Identify compliance gaps                                 │
│                                                             │
│  Output: compliance.json, compliance-report.md              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [5/5] REPORT GENERATION                                    │
│  ───────────────────────                                    │
│  • Aggregate all findings                                   │
│  • Prioritize risks                                         │
│  • Generate countermeasures                                 │
│  • Create executive summary                                 │
│  • Compile detailed report                                  │
│  • Create baseline snapshot                                 │
│                                                             │
│  Output: risk-report.md, executive-summary.md,              │
│          baseline/snapshot-{date}.json                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Progress Display

```
═══════════════════════════════════════════════════════════════
            THREAT MODELING - FULL WORKFLOW
═══════════════════════════════════════════════════════════════

Project: My Application
Documentation: ./docs/architecture
Framework: STRIDE
Compliance: OWASP, SOC2

───────────────────────────────────────────────────────────────

[1/5] Initializing...
      ├── Scanning documentation...
      ├── Extracting assets... found 14
      ├── Mapping data flows... found 22
      ├── Identifying trust boundaries... found 5
      ├── Cataloging attack surface... found 12 entries
      └── Generating diagrams... done
      ✓ Initialization complete

[2/5] Analyzing threats...
      ├── Applying STRIDE framework...
      ├── Processing 14 assets...
      ├── Analyzing 8 trust boundary crossings...
      ├── Building attack trees for critical threats...
      └── Creating risk register...
      ✓ Threat analysis complete (47 threats identified)

[3/5] Verifying controls...
      ├── Identifying required controls... 29 needed
      ├── Searching codebase...
      ├── Verifying implementations...
      └── Documenting gaps...
      ✓ Verification complete (18 verified, 7 partial, 4 missing)

[4/5] Mapping compliance...
      ├── Mapping to OWASP Top 10...
      ├── Mapping to SOC2...
      └── Calculating coverage...
      ✓ Compliance mapping complete (OWASP: 82%, SOC2: 88%)

[5/5] Generating reports...
      ├── Aggregating findings...
      ├── Prioritizing risks...
      ├── Generating countermeasures...
      ├── Creating executive summary...
      ├── Compiling detailed report...
      └── Creating baseline snapshot...
      ✓ Reports generated

───────────────────────────────────────────────────────────────
                         SUMMARY
───────────────────────────────────────────────────────────────

Discovery:
  • 14 assets discovered
  • 22 data flows mapped
  • 5 trust boundaries identified
  • 12 attack surface entries cataloged

Threats:
  • 47 threats identified
  • 5 critical, 12 high, 18 medium, 12 low
  • 3 unmitigated critical threats

Controls:
  • 29 controls required
  • 62% fully implemented
  • 11 gaps identified (2 critical)

Compliance:
  • OWASP Top 10: 82%
  • SOC2: 88%

───────────────────────────────────────────────────────────────
                    CRITICAL FINDINGS
───────────────────────────────────────────────────────────────

1. [CRITICAL] Credential Stuffing Attack
   Risk: 8.5 | Target: Auth API | Gap: Rate limiting insufficient

2. [CRITICAL] SQL Injection in Legacy Module
   Risk: 8.2 | Target: Reports API | Gap: Queries not parameterized

3. [CRITICAL] JWT Token Theft via XSS
   Risk: 8.0 | Target: Session | Gap: HttpOnly not set

───────────────────────────────────────────────────────────────
                       FILES CREATED
───────────────────────────────────────────────────────────────

.threatmodel/
├── config.yaml
├── state/
│   ├── assets.json
│   ├── dataflows.json
│   ├── trust-boundaries.json
│   ├── attack-surface.json
│   ├── threats.json
│   ├── controls.json
│   ├── gaps.json
│   ├── risk-register.json
│   └── compliance.json
├── diagrams/
│   ├── architecture.mmd
│   ├── dataflow.mmd
│   └── trust-boundaries.mmd
├── reports/
│   ├── risk-report.md
│   ├── executive-summary.md
│   └── compliance-report.md
└── baseline/
    └── snapshot-20250120.json

───────────────────────────────────────────────────────────────
                      NEXT STEPS
───────────────────────────────────────────────────────────────

1. Review risk report: .threatmodel/reports/risk-report.md
2. Address critical findings immediately
3. Share executive summary with stakeholders
4. Create Jira tickets for gaps
5. Schedule follow-up assessment

═══════════════════════════════════════════════════════════════
                  THREAT MODEL COMPLETE
═══════════════════════════════════════════════════════════════
```

## Error Handling

### Documentation Not Found
```
[1/5] Initializing...
      └── ERROR: No documentation found at ./docs

Please specify documentation path:
  /tm-full --docs /path/to/architecture/docs

Or create documentation first.
```

### Partial Failure
```
[3/5] Verifying controls...
      └── WARNING: Could not access codebase at ./src

Continuing with available information...
Control verification skipped.

To include verification:
  /tm-verify --thorough

Continuing to next step...
```

## Instructions for Claude

When executing this skill:

1. **Parse arguments**:
   - Extract --docs, --framework, --compliance, --output, --report-level
   - Use defaults for missing values

2. **Execute Step 1 - Initialize**:
   - Follow /tm-init process
   - Display progress
   - Report findings

3. **Execute Step 2 - Threat Analysis**:
   - Follow /tm-threats process
   - Use specified framework
   - Include abuse cases
   - Display progress

4. **Execute Step 3 - Verification**:
   - Follow /tm-verify process
   - Use thorough mode
   - Collect evidence
   - Display progress

5. **Execute Step 4 - Compliance**:
   - Follow /tm-compliance process
   - Map to specified frameworks
   - Display progress

6. **Execute Step 5 - Reporting**:
   - Follow /tm-report process
   - Use specified detail level
   - Create baseline
   - Display progress

7. **Handle errors gracefully**:
   - Continue if possible
   - Report what couldn't be completed
   - Suggest remediation

8. **Display final summary**:
   - Key statistics
   - Critical findings
   - Files created
   - Next steps

## Timing Guidance

The full workflow processes multiple phases. Between phases:
- Display clear progress indicators
- Show intermediate results
- Allow for interruption if needed

## Reference

This skill orchestrates:
- [/tm-init](../tm-init/SKILL.md)
- [/tm-threats](../tm-threats/SKILL.md)
- [/tm-verify](../tm-verify/SKILL.md)
- [/tm-compliance](../tm-compliance/SKILL.md)
- [/tm-report](../tm-report/SKILL.md)
