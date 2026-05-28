---
name: Design
description: Design Ops v2.2 gold standard. Transform intent → validated specs → executable PRPs through 11-step invariant-enforced pipeline with multi-agent architecture. USE WHEN design, spec, PRP, validate, requirements, init project, review implementation.
version: "2.2"
---

# Design Ops v2.2 Skill

**PRODUCTION GOLD STANDARD FOR AI-ASSISTED SYSTEM DESIGN**

Design Ops v2.2 transforms human intent into validated specifications and AI-executable PRPs through a rigorous 11-step invariant-enforced pipeline. This is the definitive workflow—do not deviate.

## Multi-Agent Architecture

The pipeline executes 5 specialized agents in coordinated sequence:

```
                         Spec (human intent)
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
        │spec-analyst │  │  validator  │  │  CONVENTIONS│
        │             │  │             │  │    check    │
        │• Complete   │  │• Invariants │  │             │
        │• Complexity │  │• Domain     │  │• Style      │
        │• Think level│  │• Confidence │  │• Patterns   │
        └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
               │                │                │
               └────────────────┼────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   prp-generator     │ ← Templates + Patterns
                    │                     │
                    │ • Structure PRP     │
                    │ • Validation cmds   │
                    │ • Thinking level    │
                    │ • Pattern links     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     reviewer        │ ← Quality gate
                    │                     │
                    │ • Required sections │
                    │ • No placeholders   │
                    │ • Executable cmds   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              APPROVED              NEEDS WORK
                    │                     │
                    ▼                     └─► Iterate
            ┌─────────────────────┐
            │   ralph-check       │ ← PRP compliance
            │                     │
            │ • Schema fields     │
            │ • Routes match      │
            │ • Success criteria  │
            └──────────┬──────────┘
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
         COMPLIANT           VIOLATIONS
            │                     │
            ▼                     └─► Fix steps
        Implementation (run)
                    │
                    ▼
            ┌─────────────────────┐
            │   retrospective     │ ← Learning loop
            │                     │
            │ • Extract learnings │
            │ • Propose invariants│
            │ • System improve    │
            └─────────────────────┘
```

---

## Why v2.2 is Production Gold Standard

**Invariant enforcement as hard gates**: 43 invariants (11 universal + 32 domain-specific) catch design issues at spec-time, not production. The system rejects bad specs; it doesn't attempt fixes.

**11-step non-negotiable pipeline**: Each step is sequential for a reason. Specs generate structure. Stress-test finds incompleteness. Validate finds ambiguity. All must pass before PRP generation.

**Confidence-gated implementation**: Quantitative risk assessment (1-10 scale) prevents overconfident decisions. A 6/10 spec gets built WITH EXPLICIT RISK ACKNOWLEDGMENT.

**Multi-agent parallel analysis**: Spec-analyst, validator, CONVENTIONS-checker, PRP-generator, and reviewer agents run in coordinated sequence, each with specific expertise.

**Automatic CONVENTIONS enforcement**: Extracts codebase patterns and ensures implementations match project style, not just functional requirements.

**Learning loops built in**: Retrospectives after implementation extract learnings, propose new invariants, continuously improve the system.

---

## The Workflow

Use this exact sequence. Skip nothing.

```
INTENT (user story, journey, or problem statement)
  ↓
0. /design spec {journey}                           Create spec from journey
  ↓
SPECIFICATION
  ↓
1. /design stress-test {spec}                       Check COMPLETENESS
  ↓ (MUST PASS)
2. /design validate {spec}                          Check CLARITY
  ↓ (MUST PASS)
VALIDATED SPEC
  ↓
3. /design prp {spec}                               Compile to PRP
4. /design check {prp}                              Verify PRP quality
  ↓ (MUST PASS)
EXECUTABLE PRP
  ↓
5. /design implement {prp}                          Generate tests (TDD)
6. /design test-validate {tests}                    Validate test syntax
7. /design test-cohesion {tests}                    Verify test interactions
8. /design ralph-check {prp}                        Verify PRP compliance
  ↓ (MUST PASS)
TEST SUITE + READY-TO-IMPLEMENT PRP
  ↓
9. /design run {prp}                                AI implements to spec
  ↓
IMPLEMENTATION
  ↓
10. Retrospective                                   Extract learnings
  ↓
LEARNINGS → System improvements
```

---

## Agent Usage

This skill is used by design systems engineers and implementation teams. You will follow the 11-step pipeline exactly.

## Command Reference

### Command Workflow

**MUST FOLLOW THIS ORDER** - each step catches different problems:

```
┌─────────────────────────────────────────────────────────────────┐
│  0. /design spec           "Generate spec FROM journey"         │
│     └─► Creates: specs/{name}-spec.md from journey + personas   │
│                                                                 │
│  1. /design stress-test    "Is the spec COMPLETE?"              │
│     └─► Checks: invariant violations, coverage gaps, blockers   │
│                                                                 │
│  2. /design validate       "Is the spec CLEAR?"                 │
│     └─► Checks: ambiguity, vague terms, implicit assumptions    │
│                                                                 │
│  3. /design prp            "Compile to PRP" (alias: generate)   │
│     └─► Extracts: confidence, thinking level, verbatim content  │
│     └─► **NEW: Runs dependency-trace (INV-L010, INV-L011)**     │
│                                                                 │
│  4. /design check          "Is the PRP READY?"                  │
│     └─► Verifies: extraction completeness, source comparison    │
│     └─► (Runs automatically after prp)                          │
│                                                                 │
│  5. /design dependency-trace "Are all deps covered?"            │
│     └─► Verifies: TODO→deliverable, table→CREATE (INV-L010/11) │
│     └─► BLOCKS if any gaps found                                │
│                                                                 │
│  6. HUMAN REVIEWS          ← YOU approve before implementation  │
│                                                                 │
│  7. /design implement      "Generate tests (TDD mode)"          │
│     └─► Creates: test_NN.py, gate_N.py, conftest.py            │
│     └─► NO step files - tests are the contract (INV-L007)       │
│                                                                 │
│  8. /design test-validate  "Are tests valid & complete?"        │
│     └─► Verifies: syntax, SC coverage, integration (INV-L008)   │
│                                                                 │
│  9. /design test-cohesion  "Do tests work together?"            │
│     └─► Verifies: no duplicates, fixtures, imports (INV-L009)   │
│                                                                 │
│ 10. /design ralph-check    "Do tests match PRP?"                │
│     └─► Verifies: schema fields, routes, success criteria       │
│                                                                 │
│ 11. /design run            "AI writes code to pass tests"       │
│     └─► AI coding agent implements, tests verify, iterate       │
└─────────────────────────────────────────────────────────────────┘
```

**Don't skip steps.** Spec generates structure. Stress-test catches completeness. Validate catches clarity. All must pass before PRP generation.

---

### /design init {project-name}

Bootstrap a new project with complete Design Ops structure.

**Usage:**
```
/design init my-new-feature
/design init house-build --domain physical-construction
/design init api-service --domain integration
```

**Execution:**

1. **Create folder structure:**
```
{project-name}/
├── docs/
│   └── design/
│       ├── research/           # Market research, user interviews
│       ├── personas/           # User persona definitions
│       ├── journeys/           # User journey maps
│       ├── specs/              # Feature specifications
│       ├── PRPs/               # Compiled Product Requirements Prompts
│       └── deltas/             # Post-execution learnings
├── CONVENTIONS.md              # Codebase conventions (if code exists)
└── README.md                   # Project overview
```

2. **Initialize templates:**
   - Copy spec template to `docs/design/specs/spec-template.md`
   - Copy PRP template to `docs/design/PRPs/prp-template.md`
   - Initialize empty `CONVENTIONS.md` if codebase exists

3. **Configure domain (if specified):**
   - Create `.designops` config file with domain reference
   - Note which domain invariants will apply

**Output:**
```
Created Design Ops structure for: {project-name}
├── docs/design/ (6 subdirectories)
├── CONVENTIONS.md (initialized)
└── .designops (config)

Domain: {domain | universal}
Invariants: Universal (1-10) + {domain-specific if applicable}

Next steps:
1. Add research to docs/design/research/
2. Define personas in docs/design/personas/
3. Create journeys in docs/design/journeys/
4. Run: /design spec docs/design/journeys/your-journey.md
```

---

### /design spec {journey-file} [--output path]

Generate a specification from a user journey document. Extracts pain points, goals, and steps into functional requirements.

**Usage:**
```
/design spec docs/design/journeys/pathologist-search-journey.md
/design spec journeys/checkout-flow.md --output specs/checkout-spec.md
```

**What It Does:**

1. **Parses journey document:**
   - Extracts journey steps (the WHAT)
   - Identifies pain points (the PROBLEMS)
   - Captures goals (the OUTCOMES)
   - Notes persona references

2. **Generates structured spec:**
   - Problem statement from pain points
   - Functional requirements from steps
   - Success criteria from goals
   - Non-functional requirements inferred

3. **Prepares manifest for traceability:**
   - Links spec back to source journey
   - Tracks journey hash for change detection

**Execution:**
```bash
./enforcement/design-ops-v3.sh spec-prepare "{journey-file}"
# Reads manifest at output_dir/.manifest.json
# Then generates spec using template
```

**Output:**
```
━━━ SPEC-PREPARE COMPLETE ━━━
Journey:     journeys/pathologist-search-journey.md
Output:      specs/pathologist-search-spec.md

Extracted:
  Steps:        14
  Pain points:  8
  Goals:        5
  Personas:     1 (Dr. Sarah Chen)

Generated spec sections:
  - Problem Statement (from pain points)
  - Scope (bounded by journey steps)
  - Functional Requirements (14 FRs)
  - Success Criteria (5 measurable criteria)
  - Failure Modes (from pain points)

Next: /design stress-test specs/pathologist-search-spec.md
```

---

### /design stress-test {spec-file} [--requirements file] [--journeys file]

Check spec COMPLETENESS against domain invariants. **Run this BEFORE validate.**

**Usage:**
```
/design stress-test docs/design/specs/feature-spec.md
/design stress-test specs/api-spec.md --requirements requirements.md
/design stress-test specs/checkout.md --journeys user-journeys.md
```

**What It Checks:**

1. **Domain Detection:**
   - Parses `Domain:` header from spec
   - Resolves applicable invariants (universal + domain-specific)
   - Reports total invariant count

2. **Deterministic Coverage Checks:**
   - Happy path explicitly described
   - Error/failure cases addressed
   - Empty/null states handled
   - External failure modes (timeout, offline, API down)
   - Concurrency considerations
   - Limits/boundaries specified

3. **LLM Invariant Analysis:**
   - Invariant #1 (Ambiguity): Terms without operational definitions
   - Invariant #4 (No Irreversible Without Recovery): Destructive actions without undo
   - Invariant #5 (Fail Loudly): Silent failures
   - Invariant #7 (Validation Executable): Untestable success criteria
   - Invariant #10 (Degradation Path): Missing fallback strategies

**Execution:**
```bash
./enforcement/design-ops-v3.sh stress-test "{spec-file}" [--requirements "{file}"] [--journeys "{file}"] [--quick]
```

**Output:**
```
━━━ Domain Detection ━━━
  Domains detected: 2 (including universal)
  Total invariants: 20
    → Universal: system-invariants.md (1-11)
    → Domain (consumer product): consumer-product.md (11-15)

━━━ Deterministic Coverage Checks ━━━
  ✓ Happy path mentioned
  ✓ Error cases mentioned
  ✗ External failure modes not addressed

━━━ LLM Deep Analysis ━━━
Invariant Violations:
  ✗ Invariant #4: Delete operation has no confirmation dialog
  ✗ Invariant #7: "Works correctly" is not testable

Missing Coverage:
  ? Offline mode behavior not specified
  ? Rate limiting not addressed

Critical Blockers:
  1. What happens when AIMS API is unavailable?
  2. Max file size for imports not specified

───────────────────────────────────────────────────────────────
  Status: REVIEW REQUIRED
  → Address invariant violations before proceeding to validate
───────────────────────────────────────────────────────────────
```

**Pipeline State:**

Findings are saved to `~/.design-ops-state/{spec-name}.state.json` for use by subsequent commands.

**Next step:** `/design validate {spec-file}`

---

### /design validate {spec-file} [--domain domain-file]

Validate a specification against system invariants before PRP compilation.

**Usage:**
```
/design validate docs/design/specs/feature-spec.md
/design validate specs/mobile-app.md --domain consumer-product
/design validate specs/house-foundation.md --domain physical-construction --domain remote-management
```

**Execution:**

1. **Run validator.sh:**
```bash
./enforcement/validator.sh "{spec-file}" [--domain "{domain-file}"]
```

2. **Parse output for:**
   - Violations (blocking - must fix)
   - Warnings (non-blocking - should address)

3. **Report results with actionable fixes**

**Output (Pass):**
```
Validating: specs/my-feature.md

Checking Universal Invariants...
  [1] Ambiguity is Invalid........... PASS
  [2] State Must Be Explicit......... PASS
  [3] Emotional Intent Must Compile.. PASS
  [4] No Irreversible Without Recovery PASS
  [5] Execution Must Fail Loudly..... PASS
  [6] Scope Must Be Bounded.......... PASS
  [7] Validation Must Be Executable.. PASS
  [8] Cost Boundaries Explicit....... PASS
  [9] Blast Radius Declared.......... PASS
  [10] Degradation Path Exists....... PASS

Violations: 0
Warnings: 0

PASS - Spec ready for PRP compilation
Run: /design prp specs/my-feature.md
```

**Output (Fail):**
```
Validating: specs/my-feature.md

Checking Universal Invariants...
  [1] Ambiguity is Invalid........... FAIL

VIOLATION: Invariant #1 (Ambiguity is Invalid)
  Line 23: "Process data properly"
  Fix: Replace 'properly' with objective criteria: metric + threshold + measurement

VIOLATION: Invariant #3 (Emotional Intent Must Compile)
  Line 45: "Users should feel confident"
  Fix: Use format: emotion := concrete_mechanism (e.g., confident := show_success_rate + undo_option)

Violations: 2
Warnings: 0

REJECTED - Fix violations before proceeding
```

---

### /design prp {spec-file} [--output path] (alias: generate)

Generate a Product Requirements Prompt from a validated specification.

**Usage:**
```
/design prp specs/feature-spec.md
/design prp specs/api-spec.md --output PRPs/api-prp.md
/design prp specs/mobile-app.md --template user-feature
```

**Note:** The shell script uses `generate` as the command name:
```bash
./enforcement/design-ops-v3.sh generate specs/feature.md
```

**Template options:**
- `base` - Generic PRP template (auto-detected by default)
- `api-integration` - Technical API/integration projects
- `user-feature` - Consumer-facing features
- `data-migration` - Database/data infrastructure projects

**Execution:**

1. **Validate spec first:**
```bash
./enforcement/validator.sh "{spec-file}" [--domain "{domain}"]
# Abort if violations found
```

2. **Gather context:**
   - Read spec content
   - Detect project type
   - Load CONVENTIONS.md if exists
   - Identify domain-specific requirements
   - Extract timeline hints
   - Extract key requirements

3. **Generate PRP:**
```bash
./enforcement/spec-to-prp.sh "{spec-file}" [--template type] [--output path]
```

4. **Run quality check:**
```bash
./enforcement/prp-checker.sh "{output-file}"
```

5. **Report confidence and next steps**

**Output:**
```
Spec-to-PRP Generation
======================

Reading spec: specs/my-feature.md
Validating... PASSED (0 violations, 2 warnings)

Extracting project information...
  Project: My Feature Name
  Type: user-feature (auto-detected)
  Timeline hint: 2 weeks

Loading template: user-feature
Substituting variables...
  - PRP_ID: PRP-2026-01-19-042
  - Project name: My Feature Name
  - Validation date: 2026-01-19
  - Remaining placeholders: 24

Running quality check...
  Required sections: PASS
  Quality score: 72/100

OUTPUT: PRPs/my-feature-prp.md

Placeholders to fill:
  Line 32: [FILL_THIS_IN] - Problem statement
  Line 48: [FILL_THIS_IN] - Primary metric
  Line 65: [FILL_THIS_IN] - Phase 1 owner
  ... and 21 more

Next steps:
1. Open PRPs/my-feature-prp.md
2. Fill all [FILL_THIS_IN] placeholders
3. Run: /design check PRPs/my-feature-prp.md
4. Begin execution with validation gates
```

---

### /design check {prp-file}

Verify PRP quality and extraction completeness. **Runs automatically after generate.**

**Usage:**
```
/design check PRPs/feature-prp.md
/design check PRPs/api-prp.md --quick
```

**What It Checks:**

1. **Domain Detection** (from PRP content)

2. **Source Spec Comparison:**
   - Extracts `source_spec:` path from PRP meta block
   - If source spec accessible, compares key content:
     - Database schema (CREATE TABLE statements)
     - API endpoints (GET/POST/PUT/DELETE routes)
     - ASCII wireframes (box-drawing characters)
     - Error messages

3. **Structural Checks:**
   - Required sections present (overview, success criteria, timeline, risk, validation)
   - No unfilled placeholders ([FILL], [TODO], [TBD])
   - No LLM reasoning artifacts ("let me", "I'll", "here's my")

4. **LLM Readiness Assessment:**
   - Confidence score sanity check
   - Extraction completeness (NOT_SPECIFIED_IN_SPEC flags)
   - Thinking level appropriateness
   - Appendix content verification
   - Implementation blockers

**Execution:**
```bash
./enforcement/design-ops-v3.sh check "{prp-file}" [--quick]
```

**Output:**
```
━━━ Spec-to-PRP Comparison ━━━
  ✓ Database schema content preserved
  ✓ API endpoints preserved
  ✗ Source has ASCII wireframes but PRP may be missing them

━━━ Deterministic Checks ━━━
  ✓ overview section found
  ✓ success criteria section found
  ✗ Found 2 unfilled placeholders

━━━ LLM Advisory Assessment ━━━
Summary: PRP is mostly implementation-ready with minor gaps

Blockers (must resolve):
  ✗ Section 4.2 references "degradation strategy" but none defined

Confidence Assessment:
  Stated 7.2/10 seems accurate given documented edge cases

───────────────────────────────────────────────────────────────
  Status: ITEMS TO REVIEW
  → Fix placeholders, then proceed to implementation
───────────────────────────────────────────────────────────────
```

**Next step:** Human review, then `/design implement`

---

### /design review {spec-file} {implementation-path}

Review an implementation against its source specification for compliance.

**Usage:**
```
/design review specs/feature-spec.md ./src/feature/
/design review specs/api-spec.md ./api/ --check-conventions
```

**Execution:**

1. **Load spec requirements:**
   - Parse spec file for requirements (bullet points, acceptance criteria)
   - Extract validation criteria
   - Load CONVENTIONS.md if present

2. **Analyze implementation:**
   - Scan implementation path for relevant files
   - Check for test coverage
   - Look for validation commands
   - Check convention compliance

3. **Cross-reference:**
   - Map requirements to implementation
   - Identify gaps
   - Check edge case handling

4. **Run validation commands (if defined):**
   - Execute test suites
   - Check linting
   - Run type checks

5. **Generate compliance report**

**Output:**
```
Implementation Review
=====================

Spec: specs/feature-spec.md
Implementation: ./src/feature/

Requirements Coverage
---------------------
[ ] Requirement 1: User can submit form
    Status: IMPLEMENTED
    Files: src/feature/form.tsx, src/feature/submit.ts
    Tests: tests/feature/form.test.ts

[ ] Requirement 2: Form validates email format
    Status: IMPLEMENTED
    Files: src/feature/validation.ts
    Tests: tests/feature/validation.test.ts

[ ] Requirement 3: Error messages display inline
    Status: PARTIAL
    Files: src/feature/errors.tsx
    Missing: No test coverage for error display

[!] Requirement 4: Rate limit submissions
    Status: NOT IMPLEMENTED
    Note: No rate limiting found in codebase

Convention Compliance
--------------------
[x] TypeScript strict mode enabled
[x] ESLint rules passing
[x] Test coverage >= 80%
[ ] Component naming conventions - 2 violations
    - SubmitBtn.tsx should be SubmitButton.tsx
    - errorMsg.tsx should be ErrorMessage.tsx

Validation Commands
------------------
npm test: PASS (45/45)
npm run lint: PASS
npm run typecheck: PASS

SUMMARY
-------
Requirements: 3/4 implemented (75%)
Conventions: 3/4 passing (75%)
Tests: PASS

Status: NEEDS ATTENTION
- Complete rate limiting implementation
- Fix naming convention violations
- Add error display tests
```

---

### /design orchestrate {spec-file} [--domain domain] [--phase phase]

Run the multi-agent orchestration pipeline for complete spec-to-PRP workflow.

**Usage:**
```
/design orchestrate specs/feature-spec.md --domain api
/design orchestrate specs/migration-spec.md --phase analysis
/design orchestrate specs/api-spec.md --domain integration --output ./output
```

**Phases:**
- `analysis` - Run spec-analyst and validator in parallel
- `generate` - Generate PRP from analysis results
- `review` - Review existing PRP for quality
- `retrospective` - Create retrospective from completed PRP
- `full` - Run complete pipeline (default)

**Execution:**
```bash
./tools/multi-agent-orchestrator.sh --spec "{spec-file}" --domain "{domain}" [--phase "{phase}"]
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║      MULTI-AGENT DESIGN OPS ORCHESTRATOR                      ║
╚═══════════════════════════════════════════════════════════════╝

Phase: full
Domain: api
Output: ./output

━━━ Phase 1: Analysis ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:45] Starting parallel analysis...
[10:23:47] ✓ spec-analyst completed
[10:23:48] ✓ validator completed

Analysis results: Completeness=85%, Thinking=Think
Validation results: Confidence=78%, Violations=0

━━━ Phase 2: Generation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:50] ✓ prp-generator completed

━━━ Phase 3: Review ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:52] ✓ reviewer completed

╔═══════════════════════════════════════════════════════════════╗
║                      ORCHESTRATION COMPLETE                   ║
╚═══════════════════════════════════════════════════════════════╝

Generated Files:
  - analysis.json
  - validation.json
  - prp-feature.md
  - review.json

Status: PRP APPROVED - Ready for implementation
```

---

### /design watch {spec-file} [--domain domain] [--interval seconds]

Monitor spec file for changes with real-time validation feedback.

**Usage:**
```
/design watch specs/feature-spec.md --domain api
/design watch specs/api-spec.md --interval 5
```

**Execution:**
```bash
./tools/watch-mode.sh --spec "{spec-file}" --domain "{domain}" [--interval "{seconds}"]
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║                    WATCH MODE - LIVE VALIDATION               ║
╚═══════════════════════════════════════════════════════════════╝

Watching: specs/feature-spec.md
Domain:   api
Interval: 2s

Press Ctrl+C to stop

[10:25:32] Confidence: 78% ─ | Major: 1 Warnings: 2 (updated)
[10:25:34] Watching... (no changes)
[10:25:38] Confidence: 82% ↑ | Warnings: 1 (updated)
✓ Confidence improved by 4%
```

---

### /design dashboard [--results-dir dir]

Display real-time validation dashboard showing all spec health status.

**Usage:**
```
/design dashboard
/design dashboard --refresh 10
```

**Execution:**
```bash
./tools/validation-dashboard.sh [--results-dir "{dir}"] [--refresh "{seconds}"]
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║           DESIGN OPS VALIDATION DASHBOARD                     ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║ SYSTEM HEALTH                                                 ║
╠═══════════════════════════════════════════════════════════════╣
║ Status: HEALTHY                                               ║
║ Specs Monitored: 5                                            ║
║ Average Confidence: 76%                                       ║
║                                                               ║
║   ████████████████░░░░░░░░                                    ║
║   ■ Healthy: 4  ■ Warning: 1  ■ Critical: 0                   ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║ SPEC VALIDATION STATUS                                        ║
╠═══════════════════════════════════════════════════════════════╣
║   SPEC                   CONFIDENCE           CRIT  MAJOR     ║
║   ──────────────────────────────────────────────────────────  ║
║   ● api-spec             ████████████████░░░░  82%    0     0 ║
║   ● user-feature         ████████████████░░░░  78%    0     1 ║
║   ● migration            ████████████░░░░░░░░  65%    0     2 ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### /design continuous start|stop|status [--spec files]

Manage background continuous validation service.

**Usage:**
```
/design continuous start --spec specs/api.md --spec specs/db.md --domain api
/design continuous status
/design continuous stop
```

**Execution:**
```bash
./tools/continuous-validator.sh start --spec "{file1}" --spec "{file2}" --domain "{domain}"
./tools/continuous-validator.sh status
./tools/continuous-validator.sh stop
```

---

### /design retrospective {prp-file} --outcome "{summary}"

Generate retrospective and extract learnings after implementation.

**Usage:**
```
/design retrospective PRPs/feature-prp.md --outcome "Successfully deployed, minor issues with error handling"
```

**Execution:**
```bash
./agents/retrospective.sh "{prp-file}" --outcome "{summary}" --domain "{domain}"
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║  RETROSPECTIVE - Learning Extraction & System Improvement     ║
╚═══════════════════════════════════════════════════════════════╝

PRP:     PRPs/feature-prp.md
Domain:  api
Outcome: Successfully deployed, minor issues with error handling

[1/4] Analyzing implementation...
  Completion: 45/48 tasks (94%)

[2/4] Generating retrospective...

[3/4] Identifying invariant proposals...
  Generated 2 invariant proposals

[4/4] Generating output files...
  Created: retrospective-feature.md
  Created: invariant-proposals.json

Generated Files:
  Retrospective: retrospective-feature.md
  Proposals:     invariant-proposals.json

Summary:
  Project:       Feature Implementation
  Completion:    94%
  Proposals:     2

Next steps:
  1. Review and complete the retrospective answers
  2. Finalize invariant proposals
  3. Run: ./tools/spec-delta-to-invariant.sh retrospective-feature.md
```

---

### /design freshness [quick|full]

Run the Design Ops freshness check to ensure methodology stays current with agentic engineering best practices.

**Usage:**
```
/design freshness quick   # Check known sources only (5-10 min)
/design freshness full    # Full landscape research (15-30 min)
/design freshness         # Defaults to quick
```

**What It Does:**

1. **Scans Current State** - Inventories all Design Ops files
2. **Checks Source Health** - Validates registry sources are still active
3. **Researches Landscape** - Discovers new developments since last scan
4. **Validates Findings** - Scores against Anthropic-anchored criteria
5. **Analyzes Impact** - Compares findings to current Design Ops
6. **Generates Actions** - Creates prioritized update plan

**Execution (Claude Code does this inline):**

**Step 1: Gather Context**
```
Read and summarize current Design Ops state:
- templates/ (what PRP templates exist)
- tools/ (what automation exists)
- examples/ (what patterns are documented)
- docs/ (what guidance exists)
- invariants/ (what domains are covered)
```

**Step 2: Research Landscape**
```
Research agentic engineering developments from [LAST_SCAN_DATE] to today.

REQUIRED SOURCES (always check):
- Anthropic official: docs.anthropic.com, anthropic.com/research
- Anthropic Cookbook: github.com/anthropics/anthropic-cookbook
- Claude Code docs: Current best practices
- MCP updates: modelcontextprotocol.io

DISCOVERY FOCUS:
- New methodologies with >1000 GitHub stars OR enterprise adoption
- Patterns validated by Anthropic or recognized experts
- Tools/approaches compatible with invariant-based validation

CONTEXT: Design Ops uses invariant-based validation, multi-agent orchestration,
confidence scoring, and PRP-based implementation planning. Assess compatibility.

For each finding provide:
- Source URL
- Validation evidence (who endorses, adoption metrics)
- Key innovation (what's new)
- Relevance to Design Ops (1-10)
- Recommended action (adopt/watch/ignore)
```

**Step 3: Validate Against Framework**
```
For each discovered source, score against:
1. Anthropic Alignment (0-3): Is it endorsed/compatible with Anthropic guidance?
2. Traction (0-3): GitHub stars >1000? Enterprise adoption? Case studies?
3. Design Ops Fit (0-3): Compatible with invariants, PRPs, confidence scoring?
4. Freshness (0-1): Updated in last 6 months?

Total score /10. Only sources scoring ≥6 get recommended.
```

**Step 4: Generate Impact Analysis**
```
Compare findings against current Design Ops:

VALIDATED (Design Ops already does this):
- [List what's confirmed as best practice]

NEEDS UPDATE (Design Ops should change):
- [List specific files and changes needed]

DEPRECATED (Design Ops should remove/update):
- [List anything now outdated]

NEW ADDITIONS (Design Ops should add):
- [List new patterns/tools to incorporate]
```

**Step 5: Create Action Plan**
```
Write to docs/freshness/actions/YYYY-MM-actions.md:

## Quick Wins (< 1 hour)
- [ ] Action 1: File, change, reason

## Short-term (1 day)
- [ ] Action 2: File, change, reason

## Medium-term (1 week)
- [ ] Action 3: File, change, reason

## Watch List (revisit next month)
- Source X: Why watching, trigger for action
```

**Step 6: Update Dashboard**
```
Write to docs/freshness/dashboard.md:
- Last scan date
- Health score (0-100)
- Sources monitored
- Pending actions count
- Design Ops version alignment
```

**Output Files:**
```
docs/freshness/
├── discoveries/YYYY-MM-raw.md       # Raw research findings
├── validated/YYYY-MM-validated.md   # Scored and filtered
├── impact/YYYY-MM-impact.md         # Gap analysis
├── actions/YYYY-MM-actions.md       # Prioritized todo list
├── reports/YYYY-MM-summary.md       # Executive summary
└── dashboard.md                     # Current state (always updated)
```

**Automated Monthly Reminder:**
Install with `./tools/freshness/install.sh` to get MacOS notification on 1st of each month.

---

### /design report {project-name}

Generate a comprehensive project status report.

**Usage:**
```
/design report my-project
/design report house-build --include-deltas
```

**Execution:**

1. **Scan project structure:**
   - Find all specs in `docs/design/specs/`
   - Find all PRPs in `docs/design/PRPs/`
   - Find all deltas in `docs/design/deltas/`

2. **For each spec:**
   - Run validation status
   - Check if PRP exists
   - Check implementation status if path defined

3. **Aggregate metrics:**
   - Specs validated vs total
   - PRPs generated
   - Invariant violation trends
   - Phase completion status

4. **Generate report**

**Output:**
```
Design Ops Project Report
=========================

Project: my-project
Report Date: 2026-01-19

Specifications
--------------
| Spec | Validated | PRP | Status |
|------|-----------|-----|--------|
| feature-a.md | PASS | YES | In Progress |
| feature-b.md | PASS | YES | Complete |
| feature-c.md | FAIL (2) | NO | Blocked |

Invariant Summary
-----------------
Total validations: 15
Passed: 12 (80%)
Failed: 3 (20%)

Most common violations:
1. Invariant #1 (Ambiguity): 5 occurrences
2. Invariant #7 (Validation): 3 occurrences

PRPs Generated: 8
PRPs with unfilled placeholders: 3

Spec Deltas
-----------
| Date | Delta | New Invariant |
|------|-------|---------------|
| 2026-01-15 | API timeout handling | #44 |
| 2026-01-10 | Payment idempotency | #45 |

Recommendations
---------------
1. Address ambiguity in feature-c.md (2 violations)
2. Fill placeholders in 3 PRPs before execution
3. Review Invariant #44 applicability to active specs
```

---

## Implementation: Ralph Methodology

The Ralph Methodology provides atomic, test-verified implementation of PRPs. See [ralph-methodology.md](docs/ralph-methodology.md) for full documentation.

### /design implement {prp-file} [--output dir] [--phase N]

Generate Ralph steps from an approved PRP using **structured extraction** (not freeform generation).

**Usage:**
```
/design implement PRPs/phase1-foundation-prp.md
/design implement PRPs/feature-prp.md --output ./app/ralph-steps
/design implement PRPs/large-prp.md --phase 2  # Generate only phase 2
```

**Script Execution:**
```bash
# Uses the implement command in design-ops-v3.sh
./enforcement/design-ops-v3.sh implement "{prp-file}" [--output dir] [--phase N]

# This loads the prompt template from:
# $TEMPLATES_DIR/implement-prompt.md
```

**Prompt Template Location:** `~/.claude/plugins/design-ops/templates/implement-prompt.md`

The prompt template ensures consistent, deterministic output across all invocations.

**CRITICAL: Extraction, Not Generation**

The implement command must EXTRACT from PRP, not invent. This prevents drift between PRP and implementation.

**Extraction Mapping (MUST FOLLOW):**

| PRP Section | → | Ralph Output | Extraction Rule |
|-------------|---|--------------|-----------------|
| Meta: confidence_score | → | Step headers | Include score + derivation |
| Meta: thinking_level | → | Step headers | Flag high-attention sections |
| Timeline phases | → | Gate boundaries | One gate per phase |
| Phase deliverables | → | step-NN.sh objectives | **VERBATIM** - one step per deliverable |
| Success criteria table | → | test-NN.sh assertions | **VERBATIM** as test checks |
| Appendix: Validation commands | → | test-NN.sh commands | **COPY EXACTLY** |
| Appendix: Database schema | → | step-NN.sh SQL | **VERBATIM** - must match |
| Appendix: UI wireframes | → | step-NN.sh JSX structure | Preserve layout |
| Appendix: Error messages | → | step-NN.sh error handling | **COPY text exactly** |
| Appendix: API endpoints | → | step-NN.sh routes | **VERBATIM** paths + methods |
| Domain invariants | → | Step + test headers | Reference by number |

**Execution:**

1. **Parse PRP metadata:**
   ```
   Extract from PRP Meta section:
   - prp_id: PRP-2026-01-21-001
   - confidence_score: 7.2/10
   - thinking_level: Think Hard
   - domain: Consumer Product + Integration
   - invariants: Universal (1-11) + Domain-specific
   ```

2. **Extract phase structure:**
   ```
   For each PRP phase (Phase 1, 2, 3...):
   - List all deliverables (F0.1, F1.2, F2.4...)
   - List success criteria (SC-1.1, SC-1.2...)
   - Note performance targets
   - Note validation commands
   ```

3. **Generate step scripts with headers:**

   **REQUIRED STEP HEADER FORMAT:**
   ```bash
   #!/bin/bash
   # ==============================================================================
   # Step NN: [Deliverable title from PRP - VERBATIM]
   # ==============================================================================
   # PRP: [prp_id]
   # PRP Phase: [Phase N.M - Phase title]
   # PRP Deliverable: [F0.1 - Deliverable description]
   #
   # Invariants Applied:
   #   - #1 (Ambiguity): [specific application]
   #   - #7 (Validation): [specific application]
   #   - #11 (Accessibility): [specific application]
   #
   # Thinking Level: [Normal|Think|Think Hard|Ultrathink]
   # High-Attention Sections: [list if Think Hard or Ultrathink]
   #
   # Confidence: [X.X/10] ([High|Medium|Low])
   # Confidence Notes: [why this score, derived from PRP section]
   # ==============================================================================

   # === OBJECTIVE (from PRP deliverable - VERBATIM) ===
   # [Copy deliverable description exactly from PRP]

   # === ACCEPTANCE CRITERIA (from PRP success criteria - VERBATIM) ===
   # SC-N.1: [criterion text]
   # SC-N.2: [criterion text]

   # === IMPLEMENTATION ===
   ```

4. **Generate test scripts with PRP traceability:**

   **REQUIRED TEST FORMAT:**
   ```bash
   #!/bin/bash
   # ==============================================================================
   # Test NN: [Same title as step]
   # ==============================================================================
   # PRP: [prp_id]
   # PRP Phase: [Phase N.M]
   # Success Criteria Tested: SC-N.1, SC-N.2, SC-N.3
   # Invariants Verified: #7, #11
   # ==============================================================================

   source "$(dirname "$0")/test-utils.sh"

   # === PRP SUCCESS CRITERIA (VERBATIM from PRP Section 2) ===
   # SC-N.1: [exact text from PRP]
   # SC-N.2: [exact text from PRP]
   # === END PRP CRITERIA ===

   # === FILE EXISTENCE CHECKS ===
   check_file "src/app/styles/page.tsx"
   check_file "src/components/styles/style-list.tsx"

   # === CONTENT CHECKS (derived from success criteria) ===
   check "grep -q 'Style Library' src/app/styles/page.tsx" "SC-N.1: Styles heading"
   check "grep -q 'No styles yet' src/app/styles/page.tsx" "SC-N.2: Empty state"

   # === PRP VALIDATION COMMANDS (VERBATIM from PRP Appendix) ===
   # Copied from PRP Section 8 - Validation Commands
   check "npm run build" "Build passes"
   check "npx tsc --noEmit" "TypeScript strict mode"
   # === END VERBATIM ===

   # === INVARIANT #11: Accessibility Audit ===
   if command -v axe &> /dev/null; then
     check "axe http://localhost:3000/styles --exit" "Accessibility audit"
   else
     echo "  [SKIP] axe-cli not installed"
   fi

   # === PLAYWRIGHT VERIFICATION ===
   cat << 'PLAYWRIGHT_VERIFY'
   {
     "route": "/styles",
     "prp_phase": "1.3",
     "prp_criteria": ["SC-1.3.1", "SC-1.3.2"],
     "invariants": [11],
     "checks": [
       {
         "type": "heading",
         "level": 1,
         "text": "Style Library",
         "prp_ref": "SC-1.3.1",
         "comment": "Copied from PRP Success Criteria table"
       },
       {
         "type": "text",
         "text": "No styles yet",
         "prp_ref": "SC-1.3.2",
         "comment": "Empty state from PRP UI wireframe"
       },
       {
         "type": "a11y",
         "standard": "wcag21aa",
         "fail_on": ["critical", "serious"],
         "invariant_ref": 11,
         "comment": "Invariant #11 requires automated accessibility audit"
       }
     ]
   }
   PLAYWRIGHT_VERIFY

   report_results
   ```

5. **Generate gate scripts with phase aggregation:**

   **REQUIRED GATE FORMAT:**
   ```bash
   #!/bin/bash
   # ==============================================================================
   # Gate N: [Phase title from PRP]
   # ==============================================================================
   # PRP: [prp_id]
   # PRP Phase: [Phase N - title]
   # Steps Covered: step-01.sh through step-NN.sh
   # Success Criteria Aggregated: SC-N.1 through SC-N.M
   # Invariants Verified: #1, #7, #11
   # Performance Targets: [from PRP]
   # ==============================================================================

   echo "═══════════════════════════════════════════════════════════"
   echo "  GATE N: [Phase title]"
   echo "═══════════════════════════════════════════════════════════"

   FAIL=0

   # === RUN ALL PHASE TESTS ===
   for test in test-01.sh test-02.sh ... test-NN.sh; do
     echo "Running $test..."
     ./$test || FAIL=$((FAIL + 1))
   done

   # === PHASE SUCCESS CRITERIA (from PRP Section 2) ===
   echo ""
   echo "Checking phase success criteria..."

   # SC-N.1: [exact text from PRP]
   check_criterion "npm run build" "SC-N.1: Build successful"

   # SC-N.2: [exact text from PRP]
   check_criterion "npx tsc --noEmit" "SC-N.2: TypeScript passes"

   # SC-N.3: [exact text from PRP]
   check_criterion "test -f src/app/styles/page.tsx" "SC-N.3: Style page exists"

   # === PERFORMANCE TARGETS (from PRP) ===
   echo ""
   echo "Checking performance targets..."

   # PRP Target: Build <30s
   BUILD_START=$(date +%s)
   npm run build > /dev/null 2>&1
   BUILD_END=$(date +%s)
   BUILD_TIME=$((BUILD_END - BUILD_START))

   if [ $BUILD_TIME -lt 30 ]; then
     echo "  ✓ Build time: ${BUILD_TIME}s (target: <30s)"
   else
     echo "  ✗ Build time: ${BUILD_TIME}s (target: <30s)"
     FAIL=$((FAIL + 1))
   fi

   # === INVARIANT #11: Full Accessibility Audit ===
   echo ""
   echo "Running accessibility audit (Invariant #11)..."
   if command -v axe &> /dev/null; then
     axe http://localhost:3000 --exit || FAIL=$((FAIL + 1))
   fi

   # === GATE RESULT ===
   echo ""
   echo "═══════════════════════════════════════════════════════════"
   if [ $FAIL -eq 0 ]; then
     echo "  GATE N: PASSED"
     echo "  Proceed to Phase N+1"
   else
     echo "  GATE N: FAILED ($FAIL issues)"
     echo "  Fix issues before proceeding"
     exit 1
   fi
   echo "═══════════════════════════════════════════════════════════"
   ```

6. **Generate PRP-COVERAGE.md with full traceability:**

   ```markdown
   # PRP Coverage Matrix

   **PRP:** [prp_id]
   **Generated:** [date]
   **Confidence:** [X.X/10]
   **Thinking Level:** [level]

   ## Deliverable → Step Mapping

   | PRP Deliverable | Step | Test | Gate | Success Criteria |
   |-----------------|------|------|------|------------------|
   | F0.1 Sidebar nav | step-01.sh | test-01.sh | gate-1 | SC-0.1.1, SC-0.1.2 |
   | F0.2 Routes | step-02.sh | test-02.sh | gate-1 | SC-0.2.1 |
   | F1.1 Season DB | step-04.sh | test-04.sh | gate-2 | SC-1.1.1, SC-1.1.2 |

   ## Success Criteria → Test Mapping

   | Criterion | Test | Check | Status |
   |-----------|------|-------|--------|
   | SC-0.1.1: Sidebar shows LIBRARY section | test-01.sh | grep 'LIBRARY' | ○ |
   | SC-0.1.2: Sidebar shows SEASON section | test-01.sh | grep 'SEASON' | ○ |

   ## Invariant Coverage

   | Invariant | Applied In | Verification |
   |-----------|------------|--------------|
   | #1 Ambiguity | All steps | PRP criteria verbatim |
   | #7 Validation | All tests | Executable checks |
   | #11 Accessibility | All UI tests | axe-core audit |

   ## Schema Traceability

   | PRP Schema (Appendix B) | Step | Verification |
   |-------------------------|------|--------------|
   | seasons.code (TEXT UNIQUE) | step-04.sh | test-04.sh grep |
   | buyers.company_name | step-10.sh | test-10.sh grep |
   ```

**Output:**
```
Generated Ralph implementation:
├── ralph.sh                    # Runner script
├── ralph-results.json          # Progress tracker
└── ralph-steps/
    ├── step-01.sh ... step-NN.sh  (with invariant headers)
    ├── test-01.sh ... test-NN.sh  (with PRP verbatim sections)
    ├── gate-1.sh ... gate-N.sh    (with phase aggregation)
    └── PRP-COVERAGE.md            (full traceability)

Total: NN steps, N gates
Coverage: 100% of PRP deliverables
Invariants: All referenced in headers
PRP Criteria: All mapped to tests

Next: ./ralph.sh 1  (run step 1)
```

**Quality Checks Before Output:**

Before generating output, verify:
1. ☐ Every PRP deliverable has exactly one step
2. ☐ Every success criterion appears in a test with `prp_ref`
3. ☐ Validation commands copied VERBATIM from PRP
4. ☐ Schema field names match PRP Appendix B exactly
5. ☐ Invariant numbers in all step/test headers
6. ☐ Thinking level propagated to steps
7. ☐ PLAYWRIGHT_VERIFY has prp_criteria references
8. ☐ Gates aggregate all phase success criteria
9. ☐ Performance targets from PRP in gates
10. ☐ PRP-COVERAGE.md has complete traceability

---

### /design dependency-trace {prp-file} --journey {journey-file}

Validate that all implicit dependencies have explicit deliverables. **Required before `/design implement` (INV-L010, INV-L011).**

**Purpose:** Catch gaps like "table referenced but never created" or "TODO item with no deliverable."

**Usage:**
```
/design dependency-trace ./prps/PRP-F-010.md --journey ./journeys/J-010.md
```

**What It Checks:**

1. **TODO/⏳ Items (INV-L010):**
   - Extract all `⏳|TODO|TBD|PENDING` from journey
   - Verify each has a `F*.N` deliverable in PRP

2. **Table Lineage (INV-L011):**
   - Find all `INSERT INTO|UPDATE|DELETE FROM` statements
   - Verify each table has a `CREATE TABLE` somewhere

3. **External Services:**
   - Find all endpoint/index/model references
   - Verify each has a creation/deployment deliverable

**Output:**
```
═══════════════════════════════════════════════════════════════
  DEPENDENCY TRACE - PRP-F-010
═══════════════════════════════════════════════════════════════

━━━ TODO/⏳ Items ━━━
  ✓ Vector Search index → F5.2
  ✓ Model Serving endpoint → F1.2
  ✗ pending_stakeholders table → MISSING

━━━ Table Lineage ━━━
  ✓ signals → CREATE in PRP-F-002
  ✓ graph_nodes → CREATE in PRP-F-003
  ✗ processing_logs → NO CREATE FOUND

───────────────────────────────────────────────────────────────
  STATUS: ❌ BLOCKED - 2 gaps
───────────────────────────────────────────────────────────────
```

**Blocking:** If ANY gaps found, do not proceed to `/design implement`.

---

### /design test-validate {tests-dir}

Validate generated test files before execution. **Required in TDD mode (INV-L007, INV-L008).**

Since tests are the sole contract in TDD mode, they must be validated for:
1. **Syntax correctness** - Tests compile without errors
2. **SC coverage completeness** - Every Success Criterion has a test
3. **Integration readiness** - Tests can run together as a suite

**Usage:**
```
/design test-validate ./ralph-tests-feature
/design test-validate ./ralph-tests-feature --strict
```

**What It Checks:**

1. **Syntax Validation:**
```bash
python -m py_compile test_*.py
```

2. **SC Coverage Mapping:**
```python
# Extract SC-* references from test docstrings
# Verify every SC in PRP has corresponding test
```

3. **Test Collection (pytest dry run):**
```bash
pytest --collect-only ./ralph-tests-feature
```

4. **Integration Check:**
```bash
# Verify conftest.py exists
# Verify shared fixtures work
# Verify no import conflicts
```

**Execution (inline by LLM):**

1. Read all test_*.py files in directory
2. Parse docstrings for SC-* references
3. Compare to PRP Success Criteria table
4. Report gaps and issues

**Output:**
```
═══════════════════════════════════════════════════════════════
  TEST VALIDATION (TDD Mode)
═══════════════════════════════════════════════════════════════

━━━ Syntax Check ━━━
  ✓ test_01_forecast.py - valid
  ✓ test_02_daily_ops.py - valid
  ✗ test_03_newsletter.py - SyntaxError line 45

━━━ SC Coverage ━━━
  PRP Success Criteria: 15
  Tests covering SC-*: 14
  
  MISSING:
    ✗ SC-3.2: "Response time < 2s" - no test found

━━━ Integration Check ━━━
  ✓ conftest.py exists
  ✓ pytest --collect-only: 47 tests collected
  ✓ No import conflicts

───────────────────────────────────────────────────────────────
  Status: 1 SYNTAX ERROR, 1 MISSING SC
  → Fix before proceeding to /design run
───────────────────────────────────────────────────────────────
```

**Next step:** Fix issues, then `/design test-cohesion`

---

### /design test-cohesion {tests-dir}

Validate that all tests work together as a cohesive suite. **Required after test-validate (INV-L009).**

**Purpose:** Catch suite-wide issues that individual test validation misses.

**Usage:**
```
/design test-cohesion ./ralph-tests-J-010
```

**What It Checks:**

1. **Duplicate Function Names:**
   - No two tests can have the same function name
   - Duplicates cause pytest to skip tests silently

2. **Fixture Availability:**
   - All fixtures used by tests must be defined in conftest.py
   - Missing fixtures cause collection failures

3. **Import Collisions:**
   - No conflicting imports across test files
   - Aliases must be consistent

4. **State Isolation:**
   - Warn on module-level mutable state
   - Warn on `global` keyword usage

5. **Integration Test Exists (INV-L009):**
   - Must have test_*integration*.py
   - Integration test must cover full workflow

**Execution (inline by LLM):**

1. Collect all test_*.py files
2. Parse with ast module
3. Extract function names, fixtures, imports
4. Run pytest --collect-only
5. Report issues

**Output:**
```
═══════════════════════════════════════════════════════════════
  TEST COHESION CHECK - ralph-tests-J-010
═══════════════════════════════════════════════════════════════

━━━ Test Count ━━━
  Files: 19
  Test functions: 87
  Integration test: ✓ test_16_integration.py

━━━ Duplicate Names ━━━
  ✓ No duplicates found

━━━ Fixture Analysis ━━━
  Fixtures defined: 5 (conftest.py)
  Fixtures used: 8
  ✓ All fixtures available

━━━ Import Analysis ━━━
  ✓ No collisions

━━━ State Isolation ━━━
  ⚠️ test_05.py uses module-level variable (line 15)

━━━ Suite Collection ━━━
  $ pytest --collect-only
  87 tests collected
  ✓ All tests collectable

───────────────────────────────────────────────────────────────
  STATUS: ✓ COHESIVE (1 warning)
───────────────────────────────────────────────────────────────
```

**Blocking:** If duplicates, missing fixtures, or no integration test → BLOCK.

**Next step:** `/design ralph-check`

---

### /design ralph-check {prp-file} --tests {tests-dir}

Validate generated tests against the PRP contract before execution.

**The PRP is the source of truth.** This command ensures all generated tests verify the exact field names, routes, and validation rules defined in the PRP.

**Usage:**
```
/design ralph-check ./PRPs/phase1-prp.md --steps ./ralph-steps-v3
/design ralph-check ./PRPs/auth-prp.md --steps ./ralph-steps --quick
```

**What It Checks:**

1. **Schema Compliance:**
   - Field names match PRP definitions (e.g., `aims_code` not `fabric_id`)
   - Data types align with PRP specifications
   - Constraint definitions are consistent

2. **Route Coverage:**
   - All routes defined in PRP exist in steps
   - No orphan routes in implementation

3. **Success Criteria:**
   - Steps address each success criterion in PRP
   - Measurable targets are testable

4. **Validation Rules:**
   - Business rules from PRP are implemented
   - Format validations match PRP specifications

**Execution:**

Invoke the shell script:
```bash
./enforcement/design-ops-v3.sh ralph-check "{prp-file}" --steps "{steps-dir}" [--quick]
```

**Output:**
```
═══════════════════════════════════════════════════════════════
  RALPH PRP COMPLIANCE CHECK (v3.3.0)
═══════════════════════════════════════════════════════════════

━━━ Deterministic Checks ━━━
Extracting PRP schema definitions...
  ✓ Fabrics schema found: fabric_name,aims_code,fabric_type,status

Issues (implementation doesn't match PRP):
  ✗ Steps use 'fabric_id' but PRP defines 'aims_code'
  ✗ Steps use 'description' but PRP defines 'fabric_name'

───────────────────────────────────────────────────────────────
  Status: COMPLIANCE ISSUES
  → Fix field names, routes, or validations to match PRP.
───────────────────────────────────────────────────────────────
```

**Why This Matters:**

The schema mismatches we experienced (fabric_id vs aims_code) happened because Ralph steps were generated without validating against the PRP. This check catches those issues **before** execution, not after painful debugging.

**Run this check:**
- After `/design implement` generates Ralph steps
- Before `/design run` executes any steps
- Whenever the PRP is updated

---

### /design run [--dangerous] [--max-regen N]

**EXECUTABLE PROCEDURE - FOLLOW THESE STEPS EXACTLY**

**TDD MODE (INV-L007):** In TDD mode, there are no step scripts. The AI coding agent writes implementation code to pass tests.

---

## STEP 1: LOCATE AND LOAD STATE

```
ACTION: Find ralph-tests directory and load state
```

1.1. Look for `ralph-tests-*/` in current directory (TDD mode) or `ralph-steps/` (legacy mode)
1.2. Read `ralph-state.json`
1.3. If not found: ERROR "No ralph-state.json. Run /design implement first."
1.4. Extract: `current_step`, `total_steps`, `mode`, `dev_server.port`, `dev_server.command`
1.5. Parse arguments:
    - `--dangerous` → set mode to "dangerous"
    - `--max-regen N` → set max_regenerations (default 3)

---

## STEP 2: EXECUTE THE LOOP (TDD MODE)

```
FOR step_num FROM current_step TO total_steps:
```

### 2.1 RUN TEST (EXPECT FAILURE)

```bash
pytest ralph-tests-*/test_{step_num:02d}_*.py -v
```

- If exit code == 0 (unexpected pass): Log warning, continue to 2.5
- If exit code != 0 (expected): Continue to 2.2

### 2.2 AI IMPLEMENTS CODE TO PASS TEST

Read the test file docstring for implementation instructions:
- Target file path
- Required components (endpoints, classes, functions)
- Schema requirements from PRP

**AI coding agent writes implementation code to pass the test.**

### 2.3 RUN TEST (EXPECT PASS)

```bash
pytest ralph-tests-*/test_{step_num:02d}_*.py -v
```

- Capture FULL OUTPUT (stdout + stderr)
- If exit code != 0: Go to **STEP 3: HANDLE FAILURE**
- If exit code == 0: Continue to 2.4

### 2.4 VALIDATE IMPLEMENTATION

Verify the created file:
- File exists at target path
- Contains required components from test docstring
- No syntax errors

Continue to 2.5

### 2.3 PARSE PLAYWRIGHT_VERIFY

Search test output for JSON between `PLAYWRIGHT_VERIFY` markers:

```
Extract: route, checks[]
```

- If no PLAYWRIGHT_VERIFY found: Skip to 2.5
- If found: Continue to 2.4

### 2.4 PLAYWRIGHT MCP VERIFICATION

**2.4.1 Ensure dev server running:**

```bash
Bash: curl -s http://localhost:{port} --max-time 2
```

If fails:
```bash
Bash: lsof -ti:{port} | xargs kill -9 2>/dev/null; {dev_command} &
     (run_in_background=true)
```
Wait 5 seconds, retry health check.

**2.4.2 Navigate:**

```
mcp__playwright__browser_navigate({ url: "http://localhost:{port}{route}" })
```

**2.4.3 Snapshot:**

```
mcp__playwright__browser_snapshot({})
```

**2.4.4 Verify each check:**

| Check Type | How to Verify |
|------------|---------------|
| `heading` | Find `heading` with matching `level` containing `text` |
| `button` | Find `button` containing `text` |
| `text` | Find `text` anywhere in snapshot |
| `link` | Find `link` containing `text` |
| `section` | Find section/region with `label` |
| `navigation` | Find `navigation` landmark |

**2.4.5 If ANY check fails:**

Record failure:
```json
{
  "step": {step_num},
  "check_type": "{type}",
  "expected": "{expected_text}",
  "actual": "Not found in snapshot",
  "snapshot_excerpt": "{relevant_part_of_snapshot}"
}
```

Go to **STEP 3: HANDLE FAILURE**

### 2.5 UPDATE STATE (SUCCESS)

Update `ralph-state.json`:
```json
{
  "steps": {
    "{step_num}": { "status": "passed", "attempts": {attempts} }
  },
  "current_step": {step_num + 1}
}
```

### 2.6 CHECK FOR GATE

If `ralph-steps/gate-{N}.sh` exists for completed phase:

```bash
Bash: ./ralph-steps/gate-{N}.sh
```

- **Default mode**: Ask user "Gate {N} passed. Continue? [Y/n]"
- **Dangerous mode**: Auto-continue

### 2.7 CONTINUE LOOP

Go to next step_num

---

## STEP 3: HANDLE FAILURE

**3.0 Determine failure type:**

| Failed Script | Failure Type | Retry Strategy |
|---------------|--------------|----------------|
| `step-N.sh` | Environment/setup | Often NOT fixable by code edit. Check: missing dependency? permission? If syntax error in step script itself, fix it. Otherwise STOP. |
| `test-N.sh` | Code verification | FIXABLE. The source code that step created is wrong. Fix with Edit/Write. |
| Playwright check | UI rendering | FIXABLE. The component isn't rendering correctly. Fix the source code. |

**3.1 Record attempt:**

```json
{
  "steps": {
    "{step_num}": {
      "status": "failed",
      "attempts": {attempts},
      "error": "{error_message}",
      "failure_type": "step|test|playwright"
    }
  }
}
```

**3.2 If STEP script failed:**

1. Read error message
2. If dependency/permission issue: STOP, output "Environment issue: {error}. Fix manually."
3. If syntax error in step script itself: Fix with Edit, retry
4. If unclear: STOP, wait for human

**3.3 If TEST script failed (attempts < 3):**

1. Read the step script header to understand INTENT
2. Read the error message from test output
3. Identify what source code needs fixing (not the test - test is the contract)
4. Use **Edit** or **Write** to fix the SOURCE CODE that step created
5. Increment attempts
6. Go back to 2.2 (re-run test, not step)

**3.4 If PLAYWRIGHT check failed (attempts < 3):**

1. Read the snapshot to see what's actually rendered
2. Compare to expected check
3. Fix the SOURCE CODE (component/page) to render correctly
4. Increment attempts
5. Go back to 2.4 (re-run playwright verification)

**3.5 If attempts >= 3:**

- **Default mode**:
  - STOP execution
  - Output: "Step {step_num} failed 3 times. Fix manually and run `/design run {step_num}`"

- **Dangerous mode**:
  - If regenerations < max_regenerations:
    - Record learning: what failed, why, what was tried
    - Read PRP file for the deliverable this step implements
    - Regenerate `step-N.sh` with context: "Previous attempts failed because {errors}. Generate differently."
    - NOTE: Do NOT regenerate `test-N.sh` - it's the PRP contract
    - Increment regenerations
    - Reset attempts to 0
    - Go back to 2.1
  - Else:
    - STOP: "Max regenerations ({max_regenerations}) reached"

---

## STEP 4: COMPLETION

When all steps pass:

1. Output summary:
```
═══════════════════════════════════════════════════════════
  RALPH EXECUTION COMPLETE
═══════════════════════════════════════════════════════════
Steps: {total_steps}/{total_steps} passed
Gates: {gates_passed}/{total_gates} passed
Learnings: {learnings_count} captured

Dev server running at http://localhost:{port}
```

2. Update state: `"status": "complete"`

---

## QUICK REFERENCE

| Situation | Action |
|-----------|--------|
| Step script fails | Read error, fix with Edit, retry |
| Test script fails | Read error, fix source code, retry |
| Playwright check fails | Read snapshot, fix UI code, retry |
| 3 failures (default) | Stop, wait for human |
| 3 failures (dangerous) | Regenerate from PRP |
| Gate reached (default) | Ask approval |
| Gate reached (dangerous) | Auto-continue |

---

### Devcontainer Integration

**Setup (one-time, human):**
```bash
# Enter devcontainer
devcontainer exec --workspace-folder . bash

# Login to Claude
claude login
```

**Runner script (`ralph-runner.sh`):**
```bash
#!/bin/bash
# Ralph runner for devcontainers - executes in dangerous mode

PRP_PATH="${1:-./docs/plans/*.prp.md}"
MAX_REGEN="${2:-3}"

echo "Starting Ralph v2 in dangerous mode..."
claude --dangerously-skip-permissions \
  -p "/design run --dangerous --max-regen $MAX_REGEN"
```

---

### Two-Tier Learning System

| Level | Scope | Storage | Example |
|-------|-------|---------|---------|
| **Local** | This project | `ralph-state.json`, `LEARNINGS.md` | "Providence has non-standard YAML" |
| **Invariant** | All future PRPs | `learned-invariants.md` | "Always use python3 not python" |

**Promotion flow:**
```
Local learning captured
       │
       ▼
Human reviews (default) / auto-flag (dangerous)
       │
       ▼
If systemic → promote to invariant
       │
       ▼
Future /design implement references invariant
```

---

### Learning Review & Promotion

**Default mode:** Human reviews learnings after execution:

```
/design learnings review
```

Output:
```
╔═══════════════════════════════════════════════════════════════╗
║  LEARNING REVIEW                                              ║
╚═══════════════════════════════════════════════════════════════╝

Found 3 learning(s) to review:

[L4-1] Step 4 (Phase 1 - Data Loaders)
    python: command not found - use python3 in bash scripts

[L7-1] Step 7 (Phase 3 - Meeting Prep)
    grep interprets --pattern as flag - use grep -- "$pattern"

[L9-1] Step 9 (Phase 4 - Integration)
    YAML parse errors in Obsidian files - need defensive parsing

Options: [A]ccept  [R]eject  [P]romote to invariant
```

**Dangerous mode:** Auto-accepts local learnings, flags potential invariants for later review.

**Promote to invariant:**
```
/design learnings promote L4-1
```

Creates entry in `learned-invariants.md`:
```markdown
### INV-001

**Source:** SA Assistant / Step 4 (Phase 1)
**Date:** 2026-01-23

**Rule:** Always use python3 not python in shell scripts

**Context:** macOS bash doesn't have python in PATH by default

**Prevention:** In test-utils.sh and gate scripts, use python3 -c not python -c
```

**Output (success):**
```
═══════════════════════════════════════════════════════
  STEP 5: Create design system CSS
═══════════════════════════════════════════════════════

Executing step-05.sh...
✓ Step executed

Running test-05.sh...
✓ All checks passed (12/12)

Playwright verification /...
  ✓ heading[1]: "SA DASHBOARD"
  ✓ section: "KEY METRICS"
✓ Playwright: 2/2 checks passed

✓ Step 5 PASSED → Proceeding to Step 6
```

**Output (failure with fix):**
```
═══════════════════════════════════════════════════════
  STEP 5 - ATTEMPT 2/3
═══════════════════════════════════════════════════════

Previous error: TypeError: calculate_health is not defined
Analysis: Missing import in health_calculator.py
Fix: Adding import statement...

Re-running test-05.sh...
✓ All checks passed

✓ Step 5 PASSED (fixed on retry)
Learning captured: "health_calculator needs explicit imports"
```

---

### /design verify {route} [--checks "check1,check2"]

Run Playwright MCP verification for a specific route.

**Usage:**
```
/design verify /styles
/design verify /fabrics/import --checks "heading:Import Fabrics,button:Upload"
/design verify /login --screenshot
```

**Execution:**

The agent executes actual Playwright MCP tools:

1. **Start dev server if needed:**
   ```bash
   curl -s http://localhost:3000 > /dev/null 2>&1 || (cd {app-dir} && npm run dev &)
   ```

2. **Navigate to route:**
   ```javascript
   mcp__playwright__browser_navigate({ url: "http://localhost:3000{route}" })
   ```

3. **Capture snapshot:**
   ```javascript
   mcp__playwright__browser_snapshot({})
   ```

4. **Parse and verify:**
   - Extract text content from snapshot
   - Check for expected elements
   - Verify accessibility tree
   - Report findings

**Verification Types:**

| Type | Example | What it checks |
|------|---------|----------------|
| `heading` | `heading:Style Library` | H1-H6 with exact text |
| `button` | `button:Import` | Button with text/label |
| `link` | `link:View Details` | Link with text |
| `text` | `text:No styles yet` | Any text content |
| `input` | `input:Search` | Input with label/placeholder |
| `form` | `form:Login` | Form with accessible name |
| `table` | `table:Styles` | Table with caption/label |
| `a11y` | `a11y:no-violations` | Accessibility audit |

**Output:**
```
═══════════════════════════════════════════════════════
  PLAYWRIGHT VERIFICATION: /styles
═══════════════════════════════════════════════════════

Navigation: http://localhost:3000/styles
Status: Page loaded successfully

Checks:
  ✓ heading: "Style Library" found
  ✓ button: "Import Styles" found (admin only)
  ✓ text: "No styles yet" found (empty state)
  ✓ a11y: No critical violations

Summary: 4/4 checks passed

Snapshot saved: /tmp/verify-styles-2026-01-20.md
═══════════════════════════════════════════════════════
```

**Screenshot Mode:**

With `--screenshot`, also captures visual screenshot:
```javascript
mcp__playwright__browser_take_screenshot({ filename: "verify-{route}.png" })
```

---

### /design gate [gate-number]

Run a validation gate checkpoint.

**Usage:**
```
/design gate 1        # Run gate 1
/design gate          # Run next pending gate
```

**Execution:**

1. **Aggregate checks from PRP phase:**
   - Build verification
   - TypeScript strict mode
   - Phase-specific file checks
   - Performance targets
   - Accessibility audit

2. **Report results:**
   - Pass/fail for each criterion
   - Overall gate status
   - Next steps

**Output:**
```
═══════════════════════════════════════════════════════
  GATE 1: Foundation Setup
═══════════════════════════════════════════════════════

[PASS] Build successful (exit code 0)
[PASS] TypeScript passes (0 errors)
[PASS] All 6 auth files present
[PASS] Database schema with RLS
[PASS] Dashboard with role-based sidebar

═══════════════════════════════════════════════════════
  GATE 1 RESULTS: 5/5 PASSED
═══════════════════════════════════════════════════════

STATUS: GATE PASSED
Proceed to Phase 2: Authentication & Permissions
```

---

### /design status

Show current Ralph implementation progress.

**Usage:**
```
/design status
```

**Output:**
```
Ralph Implementation Status
===========================

PRP: PRPs/phase1-foundation-prp.md
Progress: 12/25 steps (48%)

Completed Steps:
  ✓ 1-8: Foundation Setup
  ✓ 9-12: Authentication

Current Step: 13 (Dashboard layout)
Status: Failed (attempt 2/3)
Last Error: Component not found

Gates:
  ✓ Gate 1: Foundation (passed)
  ○ Gate 2: Auth & Permissions (pending)
  ○ Gate 3: Style Management (pending)
  ○ Gate 4: Fabric Management (pending)

Next action: Fix step 13, then run: /design run 13
```

---

## Workflow Integration

### Complete Design Ops Flywheel

```
         ┌───────────────────────────────────────────────┐
         │                                               │
         ▼                                               │
    [Research]                                           │
         │                                               │
         ▼                                               │
    [Personas & Journeys]                                │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│   Write Spec        │                                  │
│   (Human intent)    │                                  │
└─────────────────────┘                                  │
         │                                               │
         ▼                                               │
┌─────────────────────┐     FAIL                         │
│ /design validate    │ ────────────────┐                │
│                     │                 │                │
└─────────────────────┘                 │                │
         │                              │                │
         │ PASS                         ▼                │
         │                    ┌─────────────────┐        │
         │                    │   Fix Spec      │        │
         │                    │   (address      │        │
         │                    │   violations)   │        │
         │                    └─────────────────┘        │
         │                              │                │
         │                              │                │
         │◄─────────────────────────────┘                │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│   /design prp       │                                  │
│   (compile to PRP)  │                                  │
└─────────────────────┘                                  │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│   Fill Placeholders │                                  │
│   (human review)    │                                  │
└─────────────────────┘                                  │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│ /design implement   │                                  │
│ (generate Ralph)    │                                  │
└─────────────────────┘                                  │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│   /design run       │◄──────────┐                      │
│   (atomic steps)    │           │                      │
└─────────────────────┘           │                      │
         │                        │ retry                │
         ▼                        │ (with error context) │
┌─────────────────────┐           │                      │
│   Test + Verify     │───FAIL────┘                      │
│   (Playwright MCP)  │                                  │
└─────────────────────┘                                  │
         │ PASS                                          │
         ▼                                               │
┌─────────────────────┐                                  │
│   /design gate      │                                  │
│   (checkpoint)      │                                  │
└─────────────────────┘                                  │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│ /design review      │                                  │
│ (compliance check)  │                                  │
└─────────────────────┘                                  │
         │                                               │
         │ Gap found?                                    │
         │                                               │
         ▼                                               │
┌─────────────────────┐                                  │
│   Spec Delta        │ ─────────────────────────────────┘
│   (new invariant)   │
└─────────────────────┘
```

---

## Error Handling

### Validation Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Spec file not found` | Invalid path | Check file path, use absolute path |
| `Invariants file not found` | Missing system-invariants.md | Ensure DesignOps structure exists |
| `Domain file not found` | Invalid domain reference | Check domain file path |
| `VIOLATION: Invariant #N` | Spec violates invariant | Follow fix suggestion in output |

### PRP Generation Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Spec has N violations` | Validation failed | Run `/design validate` and fix issues |
| `Template not found` | Invalid template name | Use: base, api-integration, user-feature, data-migration |
| `Cannot detect project type` | Ambiguous spec | Specify `--template` explicitly |

### Review Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Implementation path not found` | Invalid directory | Check path exists |
| `No spec requirements found` | Malformed spec | Ensure spec has bullet points or criteria |
| `CONVENTIONS.md not found` | No conventions defined | Create CONVENTIONS.md or use `--skip-conventions` |

---

## Dependencies

### Path Resolution

**IMPORTANT**: All paths are relative to this skill file's location (`design.md`).

When executing commands, resolve the DesignOps root directory as:
- The directory containing this `design.md` file
- Or use `$DESIGNOPS_ROOT` environment variable if set

```
{DESIGNOPS_ROOT}/           ← Directory containing this skill file
├── design.md               ← This skill file
├── enforcement/            ← Shell scripts
├── templates/              ← PRP templates
├── domains/                ← Domain invariant files
└── system-invariants.md    ← Core invariants
```

### Required Scripts

**Located at `{DESIGNOPS_ROOT}/enforcement/`:**

| Script | Purpose | Commands Implemented |
|--------|---------|---------------------|
| `design-ops-v3.sh` | **Main pipeline script** | stress-test, validate, generate, check, ralph-check |

**Note:** The following are archived/legacy (functionality now in design-ops-v3.sh):
- `validator.sh` → use `design-ops-v3.sh validate`
- `spec-to-prp.sh` → use `design-ops-v3.sh generate`
- `prp-checker.sh` → use `design-ops-v3.sh check`
- `confidence-calculator.sh` → called internally by generate

**Located at `{DESIGNOPS_ROOT}/agents/`:**

| Script | Purpose | Direct Use |
|--------|---------|------------|
| `spec-analyst.sh` | Analyze spec completeness | `./spec-analyst.sh <spec> --domain <domain>` |
| `validator.sh` | Domain invariant validation | `./validator.sh <spec> --domain <domain>` |
| `prp-generator.sh` | Generate PRP from analysis | `./prp-generator.sh <spec> --analysis <file> --validation <file>` |
| `reviewer.sh` | Review PRP quality | `./reviewer.sh <prp>` |
| `retrospective.sh` | Extract learnings | `./retrospective.sh <prp> --outcome "<summary>"` |

**Located at `{DESIGNOPS_ROOT}/tools/`:**

| Script | Purpose | Direct Use |
|--------|---------|------------|
| `multi-agent-orchestrator.sh` | Full pipeline coordination | `./multi-agent-orchestrator.sh --spec <file> --domain <domain>` |
| `watch-mode.sh` | Real-time spec monitoring | `./watch-mode.sh --spec <file> --domain <domain>` |
| `continuous-validator.sh` | Background validation service | `./continuous-validator.sh start|stop|status` |
| `validation-dashboard.sh` | Terminal dashboard | `./validation-dashboard.sh` |
| `spec-delta-to-invariant.sh` | Extract invariants from retrospectives | `./spec-delta-to-invariant.sh <retro>` |

### Required Files

| File | Location | Purpose |
|------|----------|---------|
| `system-invariants.md` | `{DESIGNOPS_ROOT}/` | Core invariant definitions |
| `prp-base.md` | `{DESIGNOPS_ROOT}/templates/` | Base PRP template |
| `thinking-level-rubric.md` | `{DESIGNOPS_ROOT}/templates/` | Thinking level quick reference |
| `validation-commands-library.md` | `{DESIGNOPS_ROOT}/templates/` | Reusable validation commands |
| `retrospective-template.md` | `{DESIGNOPS_ROOT}/templates/` | Post-implementation retro template |
| Domain files | `{DESIGNOPS_ROOT}/domains/` | Domain-specific invariants |

### Pattern Examples

| Pattern | Location | Use Case |
|---------|----------|----------|
| `api-client.md` | `{DESIGNOPS_ROOT}/examples/` | API integration, HTTP clients, retries |
| `error-handling.md` | `{DESIGNOPS_ROOT}/examples/` | Error hierarchy, Result types, circuit breakers |
| `database-patterns.md` | `{DESIGNOPS_ROOT}/examples/` | Repository pattern, transactions, pooling |
| `config-loading.md` | `{DESIGNOPS_ROOT}/examples/` | Env vars, validation, secrets |
| `test-fixtures.md` | `{DESIGNOPS_ROOT}/examples/` | Factories, mocks, test isolation |

### Documentation

| Doc | Location | Purpose |
|-----|----------|---------|
| `multi-agent-architecture.md` | `{DESIGNOPS_ROOT}/docs/` | Agent coordination design |
| `thinking-levels.md` | `{DESIGNOPS_ROOT}/docs/` | When to use Think/Think Hard/Ultrathink |

### Configuration

| File | Location | Purpose |
|------|----------|---------|
| `watch-config.yaml` | `{DESIGNOPS_ROOT}/config/` | Watch mode and agent configuration |

### Available Domains

| Domain | File | Use When |
|--------|------|----------|
| Consumer Product | `consumer-product.md` | Mobile apps, web apps, user-facing features |
| Physical Construction | `physical-construction.md` | Buildings, infrastructure, materials |
| Data Architecture | `data-architecture.md` | Pipelines, warehouses, analytics |
| Integration | `integration.md` | APIs, webhooks, third-party services |
| Remote Management | `remote-management.md` | Projects managed from distance |
| Skill Gap Transcendence | `skill-gap-transcendence.md` | New tech, learning-intensive projects |

---

## Configuration

### Project Configuration (.designops)

```yaml
# .designops - Project-level Design Ops configuration
project: my-project
domain: consumer-product
additional_domains:
  - integration

paths:
  specs: docs/design/specs
  prps: docs/design/PRPs
  deltas: docs/design/deltas
  conventions: CONVENTIONS.md

validation:
  strict: true  # Treat warnings as errors

templates:
  default: user-feature
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` | Model for all LLM calls |
| `PIPELINE_STATE_DIR` | `~/.design-ops-state` | Directory for inter-command state files |
| `DESIGN_OPS_BASE` | `~/.claude/plugins/design-ops` | Root directory for invariants, domains, templates |
| `DESIGNOPS_STRICT` | `0` | Set to `1` to treat warnings as errors |

**Example: Use a different model:**
```bash
CLAUDE_MODEL=claude-opus-4-20250514 ./enforcement/design-ops-v3.sh generate spec.md
```

**Example: Custom state directory:**
```bash
PIPELINE_STATE_DIR=/tmp/design-ops ./enforcement/design-ops-v3.sh stress-test spec.md
```

---

### Pipeline State

Commands share findings via JSON state files for continuity:

**Location:** `~/.design-ops-state/{spec-basename}.state.json`

**How it works:**
```
stress-test  →  Saves: invariant_violations, missing_coverage, critical_blockers
     ↓
validate     →  Saves: ambiguity_flags, implicit_assumptions
     ↓
generate     →  Reads previous findings (influences confidence calculation)
     ↓
check        →  Reads all previous findings for context
```

**State file structure:**
```json
{
  "stress-test": {
    "timestamp": "2026-01-21T10:30:00Z",
    "findings": {
      "invariant_violations": ["#4: delete without undo"],
      "critical_blockers": ["Max file size not specified"]
    }
  },
  "validate": {
    "timestamp": "2026-01-21T10:35:00Z",
    "findings": {
      "ambiguity_flags": ["'handle errors properly' - what is properly?"]
    }
  }
}
```

**Clear state for a spec:**
```bash
rm ~/.design-ops-state/my-spec.state.json
```

**Clear all state:**
```bash
rm -rf ~/.design-ops-state/
```

---

## Examples

### Example 1: New Feature Project

```
User: "/design init checkout-optimization"

→ Creates folder structure
→ Initializes templates
→ Provides next steps

User: "Here's my spec for the checkout flow..."
[Creates spec in docs/design/specs/checkout-v2.md]

User: "/design validate docs/design/specs/checkout-v2.md --domain consumer-product"

→ Checks universal invariants (1-10)
→ Checks consumer product invariants (11-15)
→ Reports 1 warning about loading states

User: "/design prp docs/design/specs/checkout-v2.md"

→ Validates (PASS with warning)
→ Auto-detects user-feature template
→ Generates PRP with 18 placeholders
→ Quality score: 78/100
```

### Example 2: House Construction

```
User: "/design init kuberan-house --domain physical-construction"

→ Creates structure with construction-specific templates
→ Notes domain invariants 16-21 will apply

User: "/design validate specs/foundation.md --domain physical-construction --domain remote-management"

→ Checks universal + construction + remote management invariants
→ FAIL: Invariant #17 (Vendor Capabilities) - contractor without verification
→ FAIL: Invariant #31 (Independent Inspection) - no third-party verification

User: [Fixes spec]

User: "/design validate specs/foundation.md --domain physical-construction --domain remote-management"

→ PASS (2 warnings about climate consideration)
```

### Example 3: API Integration Review

```
User: "/design review specs/stripe-integration.md ./src/payments/"

→ Loads spec requirements
→ Scans implementation
→ Runs test suite
→ Checks rate limiting, idempotency, error handling
→ Reports: 4/5 requirements implemented
→ Missing: circuit breaker implementation
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.2 | 2026-01-22 | Added `/design spec` for journey-to-spec generation, unified workflow |
| 2.1 | 2026-01-20 | Ralph Methodology for atomic implementation (implement, run, gate, status commands) |
| 2.0 | 2026-01-19 | Multi-agent architecture, continuous validation, examples library, thinking levels |
| 1.0 | 2026-01-19 | Initial release with validate, prp, review, report commands |

---

## Quick Reference

| Command | Purpose | Key Output |
|---------|---------|------------|
| `/design init {name}` | Bootstrap project | Folder structure + templates |
| `/design spec {journey}` | Generate spec from journey | Structured spec with FRs |
| `/design stress-test {spec}` | Check completeness | Invariant violations, gaps |
| `/design validate {spec}` | Check clarity | PASS/FAIL + fix suggestions |
| `/design prp {spec}` | Generate PRP (alias: generate) | Compiled PRP + quality score |
| `/design check {prp}` | Verify PRP ready | Extraction completeness |
| `/design implement {prp}` | Generate Ralph steps | Atomic steps + tests + gates |
| `/design ralph-check {prp}` | Verify steps match PRP | Schema/route compliance |
| `/design run [step]` | Execute with retry | Step result + progress |
| `/design gate [n]` | Phase checkpoint | Gate pass/fail |
| `/design verify {route}` | Playwright verification | UI element checks |
| `/design status` | Implementation progress | Steps + gates status |
| `/design learnings review` | Review captured learnings | Accept/Reject/Promote |
| `/design review {spec} {impl}` | Check compliance | Coverage report |
| `/design report {project}` | Status overview | Metrics + recommendations |
| `/design orchestrate {spec}` | Full pipeline | Analysis → PRP → Review |
| `/design watch {spec}` | Live monitoring | Real-time confidence |
| `/design dashboard` | System health | All specs status |
| `/design continuous start` | Background service | Continuous validation |
| `/design retrospective {prp}` | Extract learnings | Retro + invariant proposals |
| `/design freshness` | Methodology check | Update recommendations |

---

*Skill version: 2.2*
*Last updated: 2026-01-22*
*Enforcement tools: validator.sh v1.1, spec-to-prp.sh v1.1, prp-checker.sh v1.0*
*Multi-agent system: spec-analyst, validator, prp-generator, reviewer, retrospective*
*Continuous validation: watch-mode, continuous-validator, validation-dashboard*
*Implementation: Ralph Methodology v1.0*
