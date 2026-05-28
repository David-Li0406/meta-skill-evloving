#!/bin/bash
# ==============================================================================
# lib/instructions.sh - Instruction Generation for Claude
#
# Generates structured instructions that Claude reads and follows.
# No subprocess calls, no API invocations.
# ==============================================================================

generate_stress_test_instruction() {
    local spec_file="$1"
    local output_dir="${2:-.}"
    local instruction_file="${output_dir}/$(basename "$spec_file" .md).stress-test-instruction.md"
    local spec_content
    spec_content=$(cat "$spec_file")

    cat > "$instruction_file" << 'EOF'
# Stress-Test Instruction

## Your Task

Review this specification for COMPLETENESS. Does it address:

### Coverage Areas to Check

1. **Happy Path Explicitly Described**
   - The primary/successful flow is documented
   - All steps are clear

2. **Error Cases Addressed**
   - What happens if the user provides invalid input?
   - What if a required external service fails?
   - What if the operation times out?

3. **Empty/Null States Handled**
   - What does the interface show when there's no data?
   - How does the system behave on first use?

4. **External Failure Modes**
   - What if the API is down?
   - What if the network is slow?
   - What if the database is unavailable?

5. **Concurrency Considerations**
   - What if two users perform the same action simultaneously?
   - Are there race conditions?
   - How are conflicts resolved?

6. **Limits and Boundaries Specified**
   - Maximum file size?
   - Maximum number of items?
   - Performance targets?

### SPEC CONTENT

```
EOF

    echo "$spec_content" >> "$instruction_file"

    cat >> "$instruction_file" << 'EOF'
```

## Your Output Format

When you've reviewed, output:

```json
{
  "completeness_check": {
    "happy_path": "explicit" | "missing" | "unclear",
    "error_cases": "addressed" | "missing" | "partial",
    "empty_states": "handled" | "missing" | "unclear",
    "external_failures": "addressed" | "missing" | "partial",
    "concurrency": "considered" | "missing" | "unclear",
    "boundaries": "explicit" | "missing" | "partial"
  },
  "gaps": [
    "Gap 1 description",
    "Gap 2 description"
  ],
  "critical_blockers": [
    "Blocker 1: If this isn't addressed, implementation will fail",
    "Blocker 2: ..."
  ],
  "summary": "Overall assessment of spec completeness"
}
```

## When You're Done

After completing this stress-test:
1. Save your output to a JSON file
2. Report back: "Stress-test complete"
3. Next step will be: `./design-ops-v3-refactored.sh validate specs/feature.md`

---
This is STRESS-TEST. You are checking COMPLETENESS, not clarity.
EOF

    echo -e "${GREEN}✅${NC} Instruction generated: $instruction_file"
    echo ""
    echo "Please read the instruction and check spec completeness:"
    echo "  cat $instruction_file"
}

generate_validate_instruction() {
    local spec_file="$1"
    local output_dir="${2:-.}"
    local instruction_file="${output_dir}/$(basename "$spec_file" .md).validate-instruction.md"
    local spec_content
    spec_content=$(cat "$spec_file")

    cat > "$instruction_file" << 'EOF'
# Validation Instruction

## Your Task

Review this specification for CLARITY and PRECISION against the 43 Design Ops Invariants.

### Universal Invariants (1-10)

Check each:

**INV-1: Ambiguity is Invalid**
- Every term must have an operational definition
- No vague words: "properly", "efficiently", "adequate", "reasonable"
- Every requirement must be testable

**INV-2: State Must Be Explicit**
- Are all possible states documented?
- Are state transitions clear?

**INV-3: Emotional Intent Must Compile**
- If the spec says "users should feel confident", what mechanism provides that feeling?
- Emotion = concrete_mechanism (e.g., confident := show_success_rate + undo_option)

**INV-4: No Irreversible Without Recovery**
- Any destructive action (delete, overwrite, reset) must have recovery
- Must specify: undo, backup, confirmation dialog

**INV-5: Execution Must Fail Loudly**
- No silent failures
- All error paths must be explicit
- Users must know when something goes wrong

**INV-6: Scope Must Be Bounded**
- What's IN scope?
- What's OUT of scope?
- What's explicitly NOT happening?

**INV-7: Validation Must Be Executable**
- Every success criterion must be testable
- No "works correctly" or "performs well" without metrics
- E.g., "Loads in < 2 seconds, tested on slow connection"

**INV-8: Cost Boundaries Explicit**
- Performance limits (response time, memory, CPU)
- Storage limits (max file size, max concurrent users)
- All bounds must have units and context

**INV-9: Blast Radius Declared**
- If this feature fails, what else breaks?
- What are the dependencies?
- What's the impact?

**INV-10: Degradation Path Exists**
- What happens if one part fails?
- Can the system continue partially?
- How does the user know?

### SPEC CONTENT

```
EOF

    echo "$spec_content" >> "$instruction_file"

    cat >> "$instruction_file" << 'EOF'
```

## Your Output Format

Check each invariant and report:

```json
{
  "invariant_violations": [
    {
      "invariant_number": 1,
      "invariant_name": "Ambiguity is Invalid",
      "location": "Line 25: 'Process data properly'",
      "issue": "Word 'properly' is vague",
      "fix": "Replace with objective criteria: 'Validate data against schema X, reject if invalid'"
    }
  ],
  "ambiguity_flags": [
    "Term: 'efficiently' (line 40) - add metric",
    "Requirement: 'should work' (line 52) - not testable"
  ],
  "summary": "X violations found, Y warnings",
  "ready_for_prp": true | false
}
```

## When You're Done

After completing validation:
1. Save your output JSON
2. If violations exist, fix them in the spec and re-run validate
3. If violations cleared, report back: "Validation passed"
4. Next step: `./design-ops-v3-refactored.sh generate specs/feature.md`

---
This is VALIDATION. You are checking CLARITY and PRECISION against invariants.
EOF

    echo -e "${GREEN}✅${NC} Instruction generated: $instruction_file"
    echo ""
    echo "Please read the instruction and validate against invariants:"
    echo "  cat $instruction_file"
}

generate_prp_instruction() {
    local spec_file="$1"
    local prp_id="$2"
    local domain="$3"
    local output_dir="${4:-.}"
    local instruction_file="${output_dir}/$(basename "$spec_file" .md).generate-instruction.md"
    local spec_content
    spec_content=$(cat "$spec_file")

    cat > "$instruction_file" << 'EOF'
# PRP Generation Instruction (Structured Extraction)

## Your Task

Transform this VALIDATED SPEC into a Product Requirements Prompt (PRP) using STRUCTURED EXTRACTION.

**CRITICAL:** Extract from the spec, do NOT invent. The PRP is a compilation of the spec, not creative interpretation.

### Extraction Rules (MUST FOLLOW)

| From Spec | To PRP | Rule |
|-----------|--------|------|
| Problem statement | PRP Section 1 | Copy **VERBATIM** |
| Success criteria | PRP Section 2 | Copy **VERBATIM** as table |
| Scope boundaries | PRP Section 3 | Extract **VERBATIM** |
| Functional requirements | PRP Section 4 | List each FR, source from spec |
| Failure modes | PRP Section 5 | Extract error cases **VERBATIM** |
| Acceptance criteria | PRP Section 6 | Copy **VERBATIM** |
| Validation commands | PRP Section 7 | Extract **VERBATIM** if specified |
| Domain invariants applicable | PRP Meta | List by domain, e.g., "consumer-product #11-15" |

### PRP Metadata

Extract and populate:
- **prp_id**: PRP-YYYY-MM-DD-NNN (use: EOF
    echo "$prp_id"
    cat >> "$instruction_file" << 'EOF')
- **domain**: EOF
    echo "$domain"
    cat >> "$instruction_file" << 'EOF'
- **confidence_score**: Estimate 1-10 based on:
  - Spec completeness: Are all sections filled?
  - Clarity: Are requirements unambiguous?
  - Unknowns: What external dependencies exist?
- **thinking_level**: Normal | Think | Think Hard | Ultrathink
  - Use Ultrathink if confidence < 5 or 3+ unknowns
  - Use Think Hard if confidence < 7 or 2+ unknowns
  - Use Think if confidence < 9
  - Use Normal otherwise

### SPEC CONTENT

```
EOF

    echo "$spec_content" >> "$instruction_file"

    cat >> "$instruction_file" << 'EOF'
```

### PRP Output Format

Structure as markdown with these sections:

```markdown
# PRP-YYYY-MM-DD-NNN

## Meta
- ID: PRP-YYYY-MM-DD-NNN
- Domain: consumer-product + integration
- Confidence: 7.5/10 (Moderate)
- Thinking Level: Think Hard
- Invariants: Universal (1-10) + Domain (11-15)

## Section 1: Problem Statement
[Copy from spec - VERBATIM]

## Section 2: Success Criteria
| Criterion | Source | Notes |
|-----------|--------|-------|
| SC-1.1: ... | Spec line 25 | |

## Section 3: Scope
[Extract VERBATIM from spec]

## Section 4: Functional Requirements
1. FR-1: [From spec step/requirement]
2. FR-2: [From spec step/requirement]

## Section 5: Failure Modes & Recovery
- [Extract from spec error cases]

## Section 6: Acceptance Criteria
- [Copy VERBATIM from spec success criteria]

## Section 7: Validation Commands
- [Extract VERBATIM if specified, otherwise note "To be defined"]

## Section 8: Appendices
- Wireframes: [reference if in spec]
- Database Schema: [extract if in spec]
- API Endpoints: [extract if in spec]
```

## When You're Done

1. Generate the PRP following extraction rules above
2. Save as: PRPs/{spec-basename}-prp.md
3. Report back: "PRP generated: PRPs/{name}-prp.md"
4. Next step: `./design-ops-v3-refactored.sh check PRPs/{name}-prp.md`

---
This is PRP GENERATION. You are EXTRACTING from spec, not generating new content.
EOF

    echo -e "${GREEN}✅${NC} Instruction generated: $instruction_file"
    echo ""
    echo "Please read the instruction and generate PRP using structured extraction:"
    echo "  cat $instruction_file"
}

generate_implement_instruction() {
    local prp_file="$1"
    local output_dir="${2:-.}"
    local instruction_file="${output_dir}/$(basename "$prp_file" .md).implement-instruction.md"
    local prp_content
    prp_content=$(cat "$prp_file")

    cat > "$instruction_file" << 'EOF'
# Ralph Step Generation Instruction (Structured Extraction)

## Your Task

Generate Ralph steps from this PRP using STRUCTURED EXTRACTION.

**CRITICAL:** Extract from PRP, do NOT invent. Each step is a verbatim copy of a PRP deliverable.

### Extraction Mapping (MUST FOLLOW)

| PRP Section | Ralph Output | Extraction Rule |
|-------------|--------------|-----------------|
| Meta: prp_id | All step headers | Include as "# PRP: ..." |
| Meta: confidence_score | All step headers | Include as "# Confidence: X.X/10" |
| Meta: thinking_level | All step headers | Include as "# Thinking Level: ..." |
| Phase N deliverables | step-NN.sh | **VERBATIM** - one step per deliverable |
| Success criteria table | test-NN.sh | **VERBATIM** as test assertions |
| Validation commands | test-NN.sh | **COPY EXACTLY** |
| Domain invariants | Step + test headers | Reference by number, e.g. "Invariants: #1, #7, #11" |

### Step Header Template (REQUIRED FORMAT)

```bash
#!/bin/bash
# ==============================================================================
# Step NN: [Deliverable title from PRP - VERBATIM]
# ==============================================================================
# PRP: [prp_id]
# PRP Phase: [Phase N - title]
# PRP Deliverable: [F0.1 - description]
#
# Invariants Applied:
#   - #1 (Ambiguity): [how this step addresses it]
#   - #7 (Validation): [how this step ensures it]
#   - #11 (Accessibility): [how this step ensures it]
#
# Thinking Level: [Normal|Think|Think Hard|Ultrathink]
# High-Attention Sections: [list if Think Hard or Ultrathink]
#
# Confidence: [X.X/10] ([High|Medium|Low])
# Confidence Notes: [why this score]
# ==============================================================================

# === OBJECTIVE (from PRP deliverable - VERBATIM) ===
# [Deliverable description copied exactly from PRP]

# === ACCEPTANCE CRITERIA (from PRP success criteria - VERBATIM) ===
# SC-1.1: [exact criterion text]
# SC-1.2: [exact criterion text]

# === IMPLEMENTATION ===
# [Your implementation here]
```

### Test Header Template (REQUIRED FORMAT)

```bash
#!/bin/bash
# ==============================================================================
# Test NN: [Same title as step]
# ==============================================================================
# PRP: [prp_id]
# PRP Phase: [Phase N]
# Success Criteria Tested: SC-1.1, SC-1.2, SC-1.3
# Invariants Verified: #1, #7, #11
# ==============================================================================

# === PRP SUCCESS CRITERIA (VERBATIM from PRP) ===
# SC-1.1: [exact text from PRP]
# SC-1.2: [exact text from PRP]
# === END VERBATIM ===

# === IMPLEMENTATION ===
# [Test code here]
```

### PRP CONTENT

```
EOF

    echo "$prp_content" >> "$instruction_file"

    cat >> "$instruction_file" << 'EOF'
```

## Step-by-Step Process

1. **Extract PRP Metadata**
   - prp_id, domain, confidence_score, thinking_level

2. **For Each Phase in PRP**
   - Create gate-N.sh (aggregates phase)
   - For each deliverable (F0.1, F1.2, etc.)
     - Create step-NN.sh (extract title, copy objective)
     - Create test-NN.sh (copy success criteria VERBATIM)

3. **Include Domain Invariants**
   - From PRP meta, determine domain invariants
   - Reference in headers: "Invariants: #1, #7, #11"

4. **Maintain Traceability**
   - Every step must link back to PRP
   - Success criteria must be copied VERBATIM, not paraphrased

## File Output Structure

```
ralph-steps/
├── step-01.sh         (First deliverable)
├── test-01.sh         (Test for deliverable 1)
├── step-02.sh         (Second deliverable)
├── test-02.sh         (Test for deliverable 2)
├── gate-1.sh          (Gate for Phase 1)
├── gate-2.sh          (Gate for Phase 2)
├── conftest.sh        (Shared test utilities)
└── PRP-COVERAGE.md    (Traceability matrix)
```

## When You're Done

1. Generate all ralph-steps following extraction rules
2. Save to: ralph-steps/ directory
3. Report back: "Ralph steps generated: {step_count} steps, {test_count} tests, {gate_count} gates"
4. Verify: Each step is EXTRACTED VERBATIM from PRP, not invented

---
This is RALPH GENERATION. You are EXTRACTING from PRP, maintaining traceability, not inventing.
EOF

    echo -e "${GREEN}✅${NC} Instruction generated: $instruction_file"
    echo ""
    echo "Please read the instruction and generate Ralph steps using structured extraction:"
    echo "  cat $instruction_file"
}
