---
name: investigate-root-cause
description: High-confidence root cause investigation using 4 parallel agents with different reasoning strategies, mandatory adversarial validation, evidence verification, and blind spot detection. Use when user asks to "investigate root cause of [condition]", "why do I have [condition]", "find the cause of [symptom]", or "what's causing my [condition]".
---

# Ensemble Root Cause Investigation

Maximize diagnostic accuracy through independent reasoning paths, mandatory adversarial validation, evidence verification, and blind spot detection.

## Objective: Maximize Diagnostic Accuracy

Simple consensus can fail if all agents make the same error. This skill incorporates techniques to maximize accuracy:

1. **Independent reasoning paths** - Different starting points reduce correlated errors
2. **Mandatory adversarial validation** - Red team agent actively tries to disprove AND propose alternatives
3. **Cross-agent refinement** - Agents review each other's findings and revise hypotheses
4. **Evidence verification** - Verify cited evidence exists AND interpretations are valid
5. **Interpretation validation** - Check unit consistency, temporal logic, statistical reasonableness
6. **Diagnostic gap penalty** - Reduce confidence when key tests are missing
7. **Epidemiological priors** - Weight by condition prevalence, not just evidence fit
8. **Blind spot detection** - Identify hypotheses ALL agents may have missed
9. **Falsification criteria** - Each hypothesis specifies what would confirm/refute it
10. **Calibrated confidence** - Weight by evidence quality, gap penalty, and priors

## Architecture Overview

```
Phase 0: SelfDecode Configuration Check
    ├─ Read profile YAML
    ├─ Check if selfdecode.enabled is false
    │   ├─ If disabled: Ask user if they want to enable it
    │   │   ├─ If YES: Guide credential setup, test connection
    │   │   └─ If NO: Continue without SelfDecode (note limitation)
    │   └─ If enabled: Test connection immediately
    ├─ Connection test: curl to SelfDecode API with test SNP (rs429358)
    │   ├─ If success: Proceed to Phase 1
    │   └─ If auth error: Prompt user to update credentials, retry
    └─ Loop credential update until success or user declines

Phase 1: Spawn 4 investigators in parallel (single message)
    ├─ Agent 1: Bottom-Up (data-driven, no preconceptions)
    ├─ Agent 2: Top-Down (differential diagnosis, then seek evidence)
    ├─ Agent 3: Genetics-First (genetic etiology prioritized)
    └─ Agent 4: RED TEAM (actively disprove AND propose alternatives) [MANDATORY]

Phase 2: Wait for all agents to complete

Phase 2.5: Cross-Agent Refinement
    ├─ Each agent reviews summaries of other 3 agents
    ├─ Agents can revise hypotheses, adopt insights, note disagreements
    └─ Red Team reviews if critiques were addressed

Phase 3: Evidence Verification Agent
    ├─ Verify all cited evidence exists and supports claims
    └─ Validate interpretations are reasonable (unit consistency, temporal logic, etc.)

Phase 4: Consensus & Blind Spot Agent
    ├─ Merge verified findings
    ├─ Detect hypotheses ALL agents missed
    ├─ Query literature for other known causes
    ├─ Apply diagnostic gap penalty for missing tests
    ├─ Incorporate epidemiological priors
    └─ Produce calibrated final ranking with falsification criteria

Phase 5: Update Health State
    ├─ Add/update condition with hypotheses and confidence
    ├─ Generate prioritized actions from recommended follow-up
    ├─ Update genetics if relevant variants found
    ├─ Create/update goal for condition
    └─ Write updated state file

Phase 6: Return final consensus report path + state update summary
```

## When to Use This Skill

Use ensemble investigation when:
- User asks for "high-confidence investigation"
- User asks for "maximum diagnostic accuracy"
- User explicitly requests "ensemble" or "parallel" investigation
- Standard `investigate-root-cause` results are inconclusive or conflicting
- Condition is complex with multiple possible etiologies
- High stakes require thorough investigation (treatment decisions)

For routine investigations, use standard `investigate-root-cause` which is faster and sufficient for most cases.

**Note**: Phase 0 automatically checks SelfDecode configuration at the start of every investigation. If SelfDecode is disabled, you'll be prompted to enable it for expanded genetic coverage (~20M imputed SNPs vs 631k from 23andMe alone).

---

## Phase 0: SelfDecode Configuration Check

Before spawning investigation agents, verify SelfDecode configuration to maximize genetic coverage.

### Step 0.1: Read Profile and Check SelfDecode Status

```bash
# Read profile YAML to check selfdecode configuration
cat profiles/{profile}.yaml | grep -A 4 "selfdecode:"
```

Check the output:
- `enabled: true` → Proceed to connection test (Step 0.3)
- `enabled: false` or missing → Prompt user (Step 0.2)

### Step 0.2: Prompt User to Enable SelfDecode (If Disabled)

Use the AskUserQuestion tool:

```
AskUserQuestion:
  questions:
    - question: "SelfDecode is currently disabled. Would you like to enable it for expanded genetic coverage? SelfDecode provides ~20M imputed SNPs compared to 631k from 23andMe alone, which can reveal variants not directly genotyped."
      header: "SelfDecode"
      options:
        - label: "Yes, enable SelfDecode"
          description: "I'll guide you through adding your SelfDecode credentials to the profile"
        - label: "No, continue without"
          description: "Investigation will use 23andMe data only (some genetic variants may be unavailable)"
      multiSelect: false
```

**If user selects "Yes, enable SelfDecode"**:

Guide them to update their profile:

```markdown
To enable SelfDecode, you'll need to add credentials to your profile:

1. **Get your profile_id**:
   - Log into SelfDecode → Settings → look for your profile UUID in the URL

2. **Get your JWT token**:
   - In SelfDecode, open browser DevTools (F12) → Network tab
   - Navigate to any page → find a request to api.selfdecode.com
   - Copy the Authorization header value (without "JWT " prefix)

3. **Update your profile** (`profiles/{profile}.yaml`):
   ```yaml
   selfdecode:
     enabled: true
     profile_id: "your-profile-uuid"
     jwt_token: "eyJhbGciOiJSUzI1NiIs..."  # Full token, no "JWT " prefix
   ```

Let me know when you've updated the profile, and I'll test the connection.
```

After user confirms update, proceed to Step 0.3.

**If user selects "No, continue without"**:

Note the limitation and proceed to Phase 1:

```markdown
Continuing without SelfDecode. Note: Some genetic variants may not be available from 23andMe raw data alone. The investigation will proceed with available data.
```

### Step 0.3: Test SelfDecode Connection

Test the connection using a known SNP (rs429358 - APOE variant):

```bash
# Read profile to get credentials
profile_id=$(grep "profile_id:" profiles/{profile}.yaml | awk '{print $2}' | tr -d '"')
jwt_token=$(grep "jwt_token:" profiles/{profile}.yaml | awk '{print $2}' | tr -d '"')

# Test API connection with rs429358
curl -s -X GET "https://api.selfdecode.com/v2/users/${profile_id}/snps/rs429358" \
  -H "Authorization: JWT ${jwt_token}" \
  -H "Content-Type: application/json"
```

**Expected success response** (200 OK with genotype data):
```json
{
  "rsid": "rs429358",
  "genotype": "CT",
  ...
}
```

**If success**: Proceed to Phase 1.

**If authentication error** (401/403): Proceed to Step 0.4.

### Step 0.4: Handle Authentication Errors

If the connection test fails with an authentication error:

```
AskUserQuestion:
  questions:
    - question: "SelfDecode connection failed (authentication error). Your JWT token may have expired. Would you like to update it?"
      header: "Auth Error"
      options:
        - label: "Yes, I'll update the token"
          description: "Get a fresh JWT token from SelfDecode DevTools and update your profile"
        - label: "Skip SelfDecode for now"
          description: "Continue investigation with 23andMe data only"
      multiSelect: false
```

**If user selects "Yes"**:

```markdown
To get a fresh JWT token:

1. Log into SelfDecode in your browser
2. Open DevTools (F12) → Network tab
3. Refresh the page or navigate to any section
4. Find a request to `api.selfdecode.com`
5. Copy the `Authorization` header value (without "JWT " prefix)
6. Update `profiles/{profile}.yaml` with the new token

Let me know when ready, and I'll test again.
```

Return to Step 0.3 to re-test.

**If user selects "Skip"**:

Note the limitation and proceed to Phase 1.

### Step 0.5: Record SelfDecode Status for Investigation

Before proceeding to Phase 1, record the SelfDecode status that agents should use:

| Status | Action for Agents |
|--------|-------------------|
| **Enabled + Connected** | Use two-tier lookup: 23andMe first, then SelfDecode for missing SNPs |
| **Disabled by user choice** | Use 23andMe only; note limitation in reports |
| **Disabled due to auth failure** | Use 23andMe only; note limitation in reports |

Pass this status to all investigation agents in Phase 1 via the Common Preamble:

```markdown
**SelfDecode Status**: {ENABLED|DISABLED}
**Reason**: {User choice / Auth failure / Not configured}
```

---

## Data Snapshot for Consistency

Before spawning agents, capture a snapshot of data file hashes to ensure all agents see the same data state:

```bash
# Create investigation directory
mkdir -p .output/{profile}/investigation-{condition}-{date}

# Capture data file hashes for consistency verification
{
  echo "# Data Snapshot - Investigation started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# All agents should verify these hashes match during analysis"
  echo ""
  echo "labs_hash=$(sha256sum '${labs_path}/all.csv' | awk '{print $1}')"
  echo "current_yaml_hash=$(sha256sum '${health_log_path}/current.yaml' | awk '{print $1}')"
  echo "history_hash=$(sha256sum '${health_log_path}/history.csv' | awk '{print $1}')"
  echo "labs_modified=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' '${labs_path}/all.csv')"
  echo "current_yaml_modified=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' '${health_log_path}/current.yaml')"
  echo "history_modified=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' '${health_log_path}/history.csv')"
} > .output/{profile}/investigation-{condition}-{date}/.data-snapshot
```

This snapshot allows detection if data changed during the investigation. Include the snapshot path in the Common Preamble so agents can verify data consistency.

## Phase 1: Spawn 4 Investigation Agents

**CRITICAL**: Spawn ALL agents in a SINGLE MESSAGE for parallel execution. Do NOT spawn sequentially.

### Agent Spawning Instructions

Spawn four Task agents in one message:

```
Task tool call 1:
- subagent_type: "general-purpose"
- description: "Bottom-up investigate {condition}"
- prompt: [Agent 1 Bottom-Up Prompt Template]
- run_in_background: true

Task tool call 2:
- subagent_type: "general-purpose"
- description: "Top-down investigate {condition}"
- prompt: [Agent 2 Top-Down Prompt Template]
- run_in_background: true

Task tool call 3:
- subagent_type: "general-purpose"
- description: "Genetics-first investigate {condition}"
- prompt: [Agent 3 Genetics-First Prompt Template]
- run_in_background: true

Task tool call 4:
- subagent_type: "general-purpose"
- description: "Red team attack {condition}"
- prompt: [Agent 4 Red Team Prompt Template]
- run_in_background: true
```

### Why Different Reasoning Strategies?

| Agent | Reasoning Strategy | Why It Improves Accuracy |
|-------|-------------------|--------------------------|
| **Bottom-Up** | Start with raw data, let patterns emerge, form hypotheses from observations | Avoids anchoring bias; finds unexpected connections |
| **Top-Down** | Start with differential diagnosis list, then seek/refute evidence for each | Ensures common causes aren't missed; systematic coverage |
| **Genetics-First** | Comprehensive genetic analysis before other evidence; genetic etiology prioritized | Catches hereditary conditions that explain chronic patterns |
| **RED TEAM** | Given preliminary hypotheses, actively try to DISPROVE them | Catches confirmation bias; finds fatal contradictions |

---

## Agent Prompt Templates

### Common Preamble (Include in All Agent Prompts)

```markdown
**Profile Data Sources**:
- Labs: {labs_path}/all.csv
- Current State: {health_log_path}/current.yaml (source of truth for active medications/conditions)
- Health Timeline: {health_log_path}/history.csv
- Entity Registry: {health_log_path}/entities.json
- Health Log Narrative: {health_log_path}/health_log.md
- Medical Exams: {exams_path}/*/*.summary.md
- Genetics (optional): {genetics_23andme_path}

**IMPORTANT - Evidence Citation Format**:

You MUST cite all evidence in this structured format for verification:

## Evidence Citations

| # | Claim | Source | Location | Exact Quote/Value | Interpretation |
|---|-------|--------|----------|-------------------|----------------|
| 1 | "Patient has elevated bilirubin" | all.csv | 2025-03-15 | "bilirubin,2.8,mg/dL" | Supports Hypothesis A |
| 2 | "Reticulocytes consistently elevated" | all.csv | 2024-01 to 2025-12 | "Range: 2.1-3.8%" | Supports Hypothesis B |

This format enables the verification agent to check each claim.

**Data Access Patterns**:
Use efficient extraction commands from CLAUDE.md "Common Analysis Patterns":
- Current state: Read `{health_log_path}/current.yaml` directly for medications, conditions
- Labs: `grep -iE "(marker1|marker2)" "{labs_path}/all.csv" | sort -t',' -k1`
- Timeline: `grep -i "{term}" "{health_log_path}/history.csv" | head -50`
- Entity: `grep ",{entity_id}," "{health_log_path}/history.csv"`
- Genetics: `grep -E "^(rs123|rs456)" "{genetics_23andme_path}"`

**Genetics Lookup Strategy** (use 23andMe by default, SelfDecode for gaps):
1. First: Query 23andMe via `grep -E "^rs..." "{genetics_23andme_path}"` - directly genotyped, most reliable
2. If SNP not found AND SelfDecode configured in profile: Query `genetics-selfdecode-lookup` for imputed data
3. Always: Use SNPedia (via `genetics-snp-lookup`) for interpretation context

**Skills Available**:
- `genetics-snp-lookup` - Read `.claude/skills/health-agent/genetics-snp-lookup/SKILL.md` first (primary genetics source)
- `genetics-selfdecode-lookup` - Read `.claude/skills/health-agent/genetics-selfdecode-lookup/SKILL.md` (for SNPs missing from 23andMe, if SelfDecode configured)
- `scientific-literature-search` - Read `.claude/skills/health-agent/scientific-literature-search/SKILL.md` first

**Output Location**:
Save report to: `.output/{profile}/investigation-{condition}-{date}/agent-{strategy}.md`

Create directory first: `mkdir -p .output/{profile}/investigation-{condition}-{date}`
Use Write tool (NOT bash heredocs) to create report file.
```

---

### Agent 1: Bottom-Up (Data-Driven) Prompt Template

```markdown
Investigate the root cause of {condition} using a BOTTOM-UP data-driven approach.

{Common Preamble}

---

## YOUR STRATEGY: Bottom-Up Investigation

**DO NOT** start with hypotheses. Start with raw data exploration:

### Step 1: Extract ALL Abnormal Findings (No Filtering)

Search ALL data sources without preconceptions:

1. **All abnormal labs** (last 2 years):
   ```bash
   awk -F',' 'NR==1 || ($5 > $7 || $5 < $6)' "{labs_path}/all.csv" | head -100
   ```

2. **All health timeline events related to {condition}**:
   ```bash
   grep -i "{condition}" "{health_log_path}/history.csv" | head -50
   ```

3. **All symptoms and conditions**:
   ```bash
   # Current conditions from current.yaml (source of truth)
   grep -A 100 "^conditions:" "{health_log_path}/current.yaml"

   # Historical symptom/condition events from history.csv
   grep -E ",symptom,|,condition," "{health_log_path}/history.csv" | tail -100
   ```

4. **All medications and supplements**:
   ```bash
   # Current from current.yaml (source of truth)
   grep -A 100 "^medications:" "{health_log_path}/current.yaml"
   grep -A 100 "^supplements:" "{health_log_path}/current.yaml"

   # Historical events from history.csv
   grep -E ",medication,|,supplement," "{health_log_path}/history.csv" | tail -100
   ```

5. **Medical exam findings**:
   ```bash
   find "{exams_path}" -name "*.summary.md" | xargs grep -l "{relevant_terms}"
   ```

### Step 2: Look for Patterns and Correlations

Analyze the raw data for:
- Temporal clustering (events that occur together)
- Dose-response relationships (stronger X → stronger Y)
- Consistent patterns across time
- Unexpected associations

Let hypotheses EMERGE from data patterns. Do NOT impose expected diagnoses.

### Step 3: Generate Hypotheses from Patterns

Only AFTER finding patterns, propose 3-5 explanations:
- Base each hypothesis on observed data patterns
- Note which specific data points support each hypothesis
- Rank by how strongly data patterns support them

### Step 4: Test Hypotheses Against Data

For each hypothesis:
- Search for contradicting evidence
- Identify confounding factors
- Assess temporal sequence
- Query scientific literature for mechanisms

### Step 5: Genetics Analysis (If Configured)

If genetics data is available:
- Read `.claude/skills/health-agent/genetics-snp-lookup/SKILL.md`
- Query condition-relevant genes
- Include both positive AND negative genetic findings

### Step 6: Literature Validation

For each proposed mechanism:
- Read `.claude/skills/health-agent/scientific-literature-search/SKILL.md`
- Query PubMed/Semantic Scholar for biological pathways
- Include PMIDs in your mechanism descriptions

---

## Output Format

```markdown
---
agent: bottom-up
condition: {condition}
generated: {YYYY-MM-DD}
profile: {profile}
---

# Bottom-Up Investigation: {Condition}

## Strategy
Data-driven approach: Extract all abnormal findings, identify patterns, let hypotheses emerge.

## Raw Data Findings

### Abnormal Lab Values
[Table of all abnormal labs found]

### Timeline Events
[Table of relevant events]

### Patterns Identified
1. **Pattern A**: [Description with data citations]
2. **Pattern B**: [Description with data citations]

## Evidence Citations
[Required structured citation table - see format above]

## Hypotheses (Emerged from Data)

### Hypothesis 1: {Name}
**Data Pattern Supporting This**: [Description]
**Mechanism**: [Biological pathway with literature citations]
**Likelihood**: HIGH/MODERATE/LOW ({XX}%)

### Hypothesis 2: {Name}
[Same structure]

### Hypothesis 3: {Name}
[Same structure]

## Contradictions Found
[List any evidence that contradicts proposed hypotheses]

## Genetic Findings
[If genetics configured, include all checked SNPs with results]

## Falsification Criteria (REQUIRED)

For EACH hypothesis, specify what would confirm or refute it:

### Hypothesis 1: {Name}

**Would be CONFIRMED if**:
- [ ] {Specific test result}
- [ ] {Specific finding}

**Would be REFUTED if**:
- [ ] {Specific contradicting evidence}
- [ ] {Specific test result}

**Recommended tests to discriminate** (ordered by cost/invasiveness):
1. {Test 1}
2. {Test 2}

### Hypothesis 2: {Name}
[Same structure]

## Confidence Assessment
- Primary Hypothesis: {name} - {likelihood}
- Confidence Basis: [What data patterns support this confidence]
- Key Uncertainties: [What would need to change your mind]
```

**AVOID**: Anchoring on obvious diagnoses. The goal is to find what the data shows, not confirm what you expect.
```

---

### Agent 2: Top-Down (Differential Diagnosis) Prompt Template

```markdown
Investigate the root cause of {condition} using a TOP-DOWN differential diagnosis approach.

{Common Preamble}

---

## YOUR STRATEGY: Top-Down Differential Diagnosis

Start with systematic differential diagnosis, then seek evidence:

### Step 1: Generate Differential Diagnosis List

Query scientific literature for known causes:
- Read `.claude/skills/health-agent/scientific-literature-search/SKILL.md`
- Search: "differential diagnosis of {condition}"
- Search: "causes of {condition}"
- List the top 10 known causes of this condition

### Step 2: For EACH Cause, Systematically Search Evidence

For each cause in your differential:

1. **Search for SUPPORTING evidence**:
   - Labs that would confirm this cause
   - Timeline events consistent with this cause
   - Exam findings that support this cause
   - Genetic variants associated with this cause

2. **Search for REFUTING evidence**:
   - Labs that should be abnormal but aren't
   - Timeline inconsistencies
   - Exam findings that contradict this cause
   - Genetic protection factors

3. **Calculate evidence balance**:
   - Supporting evidence count and quality
   - Refuting evidence count and quality
   - Likelihood = Support / (Support + Refutation)

### Step 3: Genetics Analysis (If Configured)

For each differential diagnosis:
- Read `.claude/skills/health-agent/genetics-snp-lookup/SKILL.md`
- Query genes associated with that cause
- Include both positive AND negative findings

### Step 4: Rank by Differential Diagnosis Probability

Combine:
- Base rate (how common is this cause?)
- Evidence support (what data confirms it?)
- Evidence refutation (what data contradicts it?)

Final Likelihood = Base Rate × Evidence Support × (1 - Evidence Refutation)

---

## Output Format

```markdown
---
agent: top-down
condition: {condition}
generated: {YYYY-MM-DD}
profile: {profile}
---

# Top-Down Differential Diagnosis: {Condition}

## Strategy
Systematic differential diagnosis: List known causes, then seek/refute evidence for each.

## Differential Diagnosis List (from Literature)

1. {Cause 1} - Base rate: {X}%
2. {Cause 2} - Base rate: {X}%
3. {Cause 3} - Base rate: {X}%
...
10. {Cause 10} - Base rate: {X}%

**Literature Source**: [PMID citations for differential diagnosis]

## Evidence Citations
[Required structured citation table - see format above]

## Systematic Evidence Review

### 1. {Cause 1}

**Supporting Evidence**:
- ✅ [Evidence with citation]
- ✅ [Evidence with citation]

**Refuting Evidence**:
- ❌ [Evidence with citation]

**Genetic Findings**:
- [SNP results if relevant]

**Likelihood**: {XX}% (Base rate × Support × (1 - Refutation))

---

### 2. {Cause 2}
[Same structure]

---

[Continue for all differential diagnoses]

## Final Ranking

| Rank | Cause | Base Rate | Support | Refutation | Final Likelihood |
|------|-------|-----------|---------|------------|------------------|
| 1 | {Name} | X% | Y% | Z% | {Final}% |
| 2 | {Name} | X% | Y% | Z% | {Final}% |

## Causes Ruled Out
[List causes with strong refuting evidence]

## Falsification Criteria (REQUIRED)

For each top-ranked diagnosis, specify what would confirm or refute it:

### Diagnosis 1: {Name}

**Would be CONFIRMED if**:
- [ ] {Specific test result (gold standard if available)}
- [ ] {Specific clinical finding}

**Would be REFUTED if**:
- [ ] {Specific contradicting evidence}
- [ ] {Alternative diagnosis confirmed}

**Key discriminating tests**:
| Test | Expected if This Diagnosis | Expected if Alternative |
|------|---------------------------|------------------------|
| {Test 1} | {Result} | {Result} |
| {Test 2} | {Result} | {Result} |

### Diagnosis 2: {Name}
[Same structure]

## Confidence Assessment
- Primary Diagnosis: {name} - {likelihood}%
- Confidence Basis: [Systematic evidence review supports this]
- Diagnostic Gaps: [What tests would increase confidence]
```

**GOAL**: Ensure common causes aren't missed. Systematic coverage over insight.
```

---

### Agent 3: Genetics-First Prompt Template

```markdown
Investigate the root cause of {condition} using a GENETICS-FIRST approach.

{Common Preamble}

---

## YOUR STRATEGY: Genetics-First Investigation

Prioritize genetic etiology before other explanations:

### Step 1: Identify ALL Genes Associated with {Condition}

1. Read `.claude/skills/health-agent/genetics-snp-lookup/SKILL.md`
2. Check if SelfDecode is configured in profile (optional expanded coverage)
3. Query SNPedia for condition-associated genes:
   - Search: "{condition}" to find relevant genes
   - Search: specific gene names known to cause {condition}
4. Create comprehensive list of genes to check

### Step 2: Check EVERY Relevant Gene (Two-Tier Lookup)

**Use 23andMe as primary source (directly genotyped = most reliable):**

For each identified gene:
1. First: Query 23andMe raw data via `grep -E "^rs..." "{genetics_23andme_path}"`
2. Document genotype and interpretation
3. Note any pathogenic or risk variants
4. Note protective variants

**For SNPs NOT found in 23andMe** (and SelfDecode configured):
1. Read `.claude/skills/health-agent/genetics-selfdecode-lookup/SKILL.md`
2. Query SelfDecode API for imputed genotypes
3. Note these are IMPUTED (less reliable than directly genotyped)
4. Mark imputed SNPs clearly in output: "rs123456 (imputed via SelfDecode)"

**Do NOT skip genes or assume SNPs aren't available without checking BOTH sources.**

### Step 3: Genetic Etiology Assessment

If positive genetic findings:
- Make genetics your PRIMARY hypothesis
- Assess penetrance (does genotype always cause phenotype?)
- Check if genetic findings explain observed phenotype
- Look for gene-environment interactions

If negative genetic findings:
- Document which genes were checked and ruled out
- Note limitations of 23andMe coverage
- Proceed to environmental/acquired causes

### Step 4: Secondary Evidence Gathering

Only AFTER genetic analysis, consider:
- Lab trends that support/refute genetic hypothesis
- Timeline events consistent with genetic etiology
- Environmental factors that might modify genetic risk

### Step 5: Pharmacogenomics Consideration

Check if {condition} is related to medication response:
- Query CYP2D6, CYP2C19, CYP2C9, VKORC1, SLCO1B1
- Check if current medications might be causing or worsening {condition}

---

## Output Format

```markdown
---
agent: genetics-first
condition: {condition}
generated: {YYYY-MM-DD}
profile: {profile}
---

# Genetics-First Investigation: {Condition}

## Strategy
Comprehensive genetic analysis before other explanations. Genetic etiology prioritized.

## Genetic Analysis (COMPREHENSIVE)

### Genes Associated with {Condition}

| Gene | SNPs Checked | Genotypes | Interpretation |
|------|--------------|-----------|----------------|
| {Gene1} | rs123, rs456 | AA, CT | {Interpretation} |
| {Gene2} | rs789 | GG | {Interpretation} |

### Positive Genetic Findings

**{Gene/Variant}**:
- Genotype: {X}
- Clinical Significance: {Description}
- Penetrance: {X}%
- Supports {condition} etiology: YES/NO

### Negative Genetic Findings (Ruled Out)

| Gene | SNPs Checked | Result | Condition Ruled Out |
|------|--------------|--------|---------------------|
| {Gene1} | rs123 | Normal | {Associated condition} |

### Genes NOT Available in 23andMe

[List any relevant genes not covered by 23andMe genotyping]

### Imputed SNPs (from SelfDecode)

| Gene | SNP | Genotype | Confidence Note |
|------|-----|----------|-----------------|
| {Gene1} | rs789 | GG | Imputed (SelfDecode) - verify with clinical testing |

**Note**: Imputed genotypes are statistical predictions based on surrounding markers. For clinical decisions, confirm with direct genotyping.

### Pharmacogenomics Findings

[If medication-related, include CYP enzyme status]

## Evidence Citations
[Required structured citation table - see format above]

## Hypotheses (Genetics-Prioritized)

### Hypothesis 1: {Genetic Cause}
**Genetic Evidence**: [Specific variants found]
**Supporting Lab/Clinical Evidence**: [Additional support]
**Likelihood**: HIGH/MODERATE/LOW ({XX}%)

### Hypothesis 2: {Acquired/Environmental Cause}
**Why Genetics Didn't Explain**: [What was checked and negative]
**Alternative Explanation**: [Description]
**Likelihood**: {XX}%

## Genetic Recommendations

If genetic testing gaps exist:
- Recommend clinical genetic testing for {genes}
- Note: 23andMe covers ~631k SNPs, may miss rare variants

## Falsification Criteria (REQUIRED)

For each hypothesis, specify genetic and clinical confirmation/refutation:

### Hypothesis 1: {Genetic Cause}

**Would be CONFIRMED if**:
- [ ] Clinical sequencing confirms pathogenic variant in {gene}
- [ ] Functional test (e.g., enzyme assay) shows deficiency
- [ ] Family segregation analysis supports inheritance

**Would be REFUTED if**:
- [ ] Clinical sequencing shows no pathogenic variants
- [ ] Functional test normal
- [ ] Family history negative after detailed inquiry

**Recommended genetic follow-up**:
1. {Clinical gene panel for condition}
2. {Specific functional test}
3. If based on imputed data: Direct genotyping to confirm imputed variants

### Hypothesis 2: {Acquired Cause}

**Would be CONFIRMED if**:
- [ ] {Specific test identifying acquired cause}
- [ ] {Temporal relationship established}

**Would be REFUTED if**:
- [ ] Genetic cause confirmed instead
- [ ] {Specific exclusion test}

## Confidence Assessment
- Primary Hypothesis: {name} - {likelihood}%
- Genetic Confidence: [Based on coverage and findings]
- 23andMe Limitations: [What variants might be missed]
```

**RATIONALE**: Genetic causes explain chronic, persistent patterns better than environmental factors. If there's a genetic explanation, it should be top-ranked.
```

---

### Agent 4: RED TEAM (Adversarial Validation) Prompt Template

```markdown
Perform RED TEAM adversarial validation for hypotheses about {condition}.

{Common Preamble}

---

## YOUR STRATEGY: Red Team / Devil's Advocate

Your job is to DISPROVE the likely hypotheses AND PROPOSE ALTERNATIVES for the same evidence.

### Step 1: Identify Likely Hypotheses

Based on {condition}, the most commonly proposed hypotheses are typically:
- {Common hypothesis 1 for this condition}
- {Common hypothesis 2 for this condition}
- {Common hypothesis 3 for this condition}

Your goal: Try to DESTROY each one AND propose what ELSE could explain the evidence.

### Step 2: For Each Hypothesis, Attack Systematically

For each plausible hypothesis:

1. **Search for CONTRADICTING evidence**:
   - Labs that should be abnormal but are normal
   - Labs that should be normal but are abnormal
   - Timeline events that don't fit the hypothesis
   - Exam findings that contradict

2. **Find TEMPORAL violations**:
   - Did the proposed effect appear BEFORE the proposed cause?
   - Is the time course inconsistent with the mechanism?

3. **PROPOSE ALTERNATIVE EXPLANATIONS** (NEW - REQUIRED):
   For EACH piece of evidence supporting a hypothesis:
   - List at least 2 ALTERNATIVE explanations for that evidence
   - Rate which explanation is more likely given ALL data
   - If you DESTROY a hypothesis, propose what diagnosis fits better

4. **Check for CHERRY-PICKING**:
   - Did proponents of this hypothesis ignore contradictory data?
   - Are they only citing supportive evidence?

5. **Assess MECHANISM plausibility**:
   - Is the proposed biological pathway well-established?
   - Are there missing intermediate steps?

### Step 3: Rate Hypothesis Survival

For each hypothesis tested:
- **SURVIVED**: No fatal flaws found. Hypothesis is strengthened.
- **WEAKENED**: Minor contradictions found. Hypothesis still possible but less likely.
- **DESTROYED**: Fatal contradiction found. **MUST specify alternative diagnosis**.

### Step 4: Identify What Would Change Your Mind

For each hypothesis that survived:
- What evidence would definitively disprove it?
- What tests could discriminate between competing hypotheses?

### Step 5: Propose Counter-Hypotheses (NEW - REQUIRED)

Based on your adversarial analysis:
1. List 1-3 alternative hypotheses that better explain the evidence
2. For each alternative, explain why it fits the contradictions you found
3. Rate your confidence in each alternative

---

## Output Format

```markdown
---
agent: red-team
condition: {condition}
generated: {YYYY-MM-DD}
profile: {profile}
---

# Red Team Attack Report: {Condition}

## Strategy
Adversarial validation: Actively try to DISPROVE likely hypotheses AND propose alternatives. A hypothesis that survives Red Team scrutiny is more likely correct.

## Hypotheses Under Attack

### Attack 1: {Hypothesis Name}

**Hypothesis Statement**: {Description}

**Contradictions Found**:
| # | Contradiction | Source | Impact |
|---|---------------|--------|--------|
| 1 | {Evidence that contradicts} | {Source:date} | FATAL/MINOR |
| 2 | {Evidence that contradicts} | {Source:date} | FATAL/MINOR |

**Temporal Violations**:
- {Any cause-effect timing issues}

**Alternative Explanations for Same Evidence** (REQUIRED):
| Evidence | Original Interpretation | Alternative 1 | Alternative 2 | Most Likely |
|----------|------------------------|---------------|---------------|-------------|
| {Evidence 1} | {Supports Hyp A} | {Could mean X} | {Could mean Y} | {Winner} |
| {Evidence 2} | {Supports Hyp A} | {Could mean X} | {Could mean Y} | {Winner} |

**Cherry-Picking Assessment**:
- {Did proponents ignore this contradictory evidence?}

**SURVIVAL RATING**: SURVIVED / WEAKENED / DESTROYED

**If DESTROYED - Replacement Diagnosis**: {What diagnosis fits better and why}

**Attack Summary**: {Why this hypothesis survived or was destroyed}

---

### Attack 2: {Hypothesis Name}
[Same structure]

---

### Attack 3: {Hypothesis Name}
[Same structure]

## Evidence Citations
[Required structured citation table - see format above]

## Counter-Hypotheses Proposed (REQUIRED)

Based on adversarial analysis, these alternative diagnoses may better explain the evidence:

### Counter-Hypothesis 1: {Name}
**Why Proposed**: {What contradictions/evidence led to this alternative}
**Supporting Evidence**: {Evidence that fits this better than original hypotheses}
**Confidence**: {X}%

### Counter-Hypothesis 2: {Name}
[Same structure]

## Discriminating Tests

To distinguish between surviving hypotheses AND counter-hypotheses:

| Test | Expected if Hypothesis A True | Expected if Counter-Hypothesis True |
|------|------------------------------|-------------------------------------|
| {Test 1} | {Result A} | {Result B} |
| {Test 2} | {Result A} | {Result B} |

## Red Team Conclusion

**Hypotheses That Survived**:
1. {Name} - Survival confidence: {X}%
2. {Name} - Survival confidence: {X}%

**Hypotheses Destroyed**:
1. {Name} - Fatal flaw: {Description} - **Replaced by**: {Counter-hypothesis}

**Counter-Hypotheses Worth Investigating**:
1. {Name} - Confidence: {X}%

**Strongest Hypothesis Post-Attack**: {Name}

**Confidence**: {X}% (based on survival of adversarial testing)
```

**SUCCESS CRITERIA**: A hypothesis that survives Red Team scrutiny is more likely correct. You WANT to find fatal flaws AND propose alternatives. If you can't find flaws, that strengthens the hypothesis. If you destroy a hypothesis, you MUST suggest what fits better.
```

---

## Phase 2: Wait for Agent Completion

After spawning all 4 agents, wait for completion:

```bash
# Check if all output files exist
ls -la .output/{profile}/investigation-{condition}-{date}/
# Expected: agent-bottomup.md, agent-topdown.md, agent-genetics.md, agent-redteam.md
```

If any agent fails or times out (>15 minutes):
- Note the failure in the consensus report
- Proceed with available agent outputs
- Reduce confidence in final assessment

---

## Phase 2.5: Cross-Agent Refinement (NEW)

After all 4 agents complete, spawn a refinement round where each agent reviews others' findings.

### Why Cross-Agent Refinement?

Without refinement:
- Agents work in isolation and can't learn from each other's insights
- Red Team critiques may go unaddressed
- Novel findings from one agent aren't considered by others
- Correlated errors persist across all agents

With refinement:
- Agents can revise hypotheses based on new evidence from others
- Red Team critiques get explicitly addressed
- Cross-pollination of insights improves coverage
- Reduces correlated errors by forcing reconsideration

### Refinement Agent Spawning

Spawn 4 refinement agents in parallel (single message):

```
Task tool call 1:
- subagent_type: "general-purpose"
- description: "Refine bottom-up findings for {condition}"
- prompt: [Refinement Prompt Template - Bottom-Up]
- run_in_background: true

Task tool call 2:
- subagent_type: "general-purpose"
- description: "Refine top-down findings for {condition}"
- prompt: [Refinement Prompt Template - Top-Down]
- run_in_background: true

Task tool call 3:
- subagent_type: "general-purpose"
- description: "Refine genetics-first findings for {condition}"
- prompt: [Refinement Prompt Template - Genetics-First]
- run_in_background: true

Task tool call 4:
- subagent_type: "general-purpose"
- description: "Red team review critiques for {condition}"
- prompt: [Refinement Prompt Template - Red Team Review]
- run_in_background: true
```

### Refinement Prompt Template (For Bottom-Up, Top-Down, Genetics-First)

```markdown
Review findings from other agents investigating {condition} and refine your analysis.

**Your Original Report**: .output/{profile}/investigation-{condition}-{date}/agent-{your-strategy}.md

**Other Agent Reports to Review**:
- .output/{profile}/investigation-{condition}-{date}/agent-bottomup.md (if not you)
- .output/{profile}/investigation-{condition}-{date}/agent-topdown.md (if not you)
- .output/{profile}/investigation-{condition}-{date}/agent-genetics.md (if not you)
- .output/{profile}/investigation-{condition}-{date}/agent-redteam.md

---

## YOUR TASK: Cross-Agent Refinement

### Step 1: Review Other Agents' Hypotheses

For each hypothesis from other agents:
- Did they find evidence you missed?
- Do they propose causes you didn't consider?
- Is their confidence higher or lower than yours for the same hypothesis?

### Step 2: Review Red Team Critiques

For each Red Team critique relevant to your hypotheses:
- Was the critique valid?
- Can you address it with additional evidence?
- Should you revise your confidence based on it?

### Step 3: Decide on Revisions

For EACH of your original hypotheses, choose one:
- **MAINTAIN**: No change based on new information
- **REVISE UP**: Increase confidence due to corroborating evidence from others
- **REVISE DOWN**: Decrease confidence due to valid critiques or contradictions
- **ADOPT**: Add a hypothesis from another agent you hadn't considered
- **ABANDON**: Remove a hypothesis based on fatal critique

### Step 4: Address Critiques Explicitly

For each Red Team critique of your hypotheses:
- Quote the critique
- Provide your response (refutation, acknowledgment, or revision)

---

## Output Format

Save to: `.output/{profile}/investigation-{condition}-{date}/refined-{your-strategy}.md`

```markdown
---
phase: refinement
agent: {your-strategy}
condition: {condition}
generated: {YYYY-MM-DD}
---

# Refined Analysis: {Condition}

## Changes Summary

| Hypothesis | Original Confidence | Revised Confidence | Change Type | Reason |
|------------|--------------------|--------------------|-------------|--------|
| {Hyp 1} | 80% | 85% | REVISE UP | Corroborated by genetics-first agent |
| {Hyp 2} | 60% | 40% | REVISE DOWN | Red Team found valid temporal violation |
| {Hyp 3} | N/A | 45% | ADOPT | From top-down agent, overlooked initially |

## Insights Adopted from Other Agents

### From Bottom-Up Agent
- {Insight 1}: {How it changed your analysis}

### From Top-Down Agent
- {Insight 1}: {How it changed your analysis}

### From Genetics-First Agent
- {Insight 1}: {How it changed your analysis}

## Red Team Critiques Addressed

### Critique 1: "{Quote from Red Team}"
**Response**: {Your refutation, acknowledgment, or how you revised}

### Critique 2: "{Quote from Red Team}"
**Response**: {Your refutation, acknowledgment, or how you revised}

## Unresolved Disagreements

| Topic | Your View | Other Agent's View | Why Unresolved |
|-------|-----------|-------------------|----------------|
| {Topic} | {Your position} | {Their position} | {Why you still disagree} |

## Revised Hypothesis Ranking

1. **{Hypothesis Name}**: {Revised confidence}% ({direction} from original)
2. **{Hypothesis Name}**: {Revised confidence}%
3. **{Hypothesis Name}**: {Revised confidence}%

## Key Evidence Integrated

[Include any new evidence citations from other agents that you now consider relevant]
```
```

### Red Team Review Prompt Template

```markdown
Review whether other agents addressed your critiques for {condition} investigation.

**Your Original Report**: .output/{profile}/investigation-{condition}-{date}/agent-redteam.md

**Other Agent Reports**:
- .output/{profile}/investigation-{condition}-{date}/agent-bottomup.md
- .output/{profile}/investigation-{condition}-{date}/agent-topdown.md
- .output/{profile}/investigation-{condition}-{date}/agent-genetics.md

---

## YOUR TASK: Verify Critiques Were Addressed

### Step 1: Inventory Your Critiques

List each contradiction, temporal violation, and alternative explanation you identified.

### Step 2: Check if Other Agents Could Address Them

For each critique:
- Did any agent have evidence that addresses this?
- Was the critique actually valid given all evidence?
- Should you revise your attack based on new information?

### Step 3: Update Survival Ratings

Based on full information from all agents:
- Did any DESTROYED hypothesis deserve resurrection?
- Did any SURVIVED hypothesis deserve downgrade?

### Step 4: Revise Counter-Hypotheses

Based on evidence from all agents:
- Are your counter-hypotheses still viable?
- Should you add new counter-hypotheses based on others' findings?

---

## Output Format

Save to: `.output/{profile}/investigation-{condition}-{date}/refined-redteam.md`

```markdown
---
phase: refinement
agent: red-team
condition: {condition}
generated: {YYYY-MM-DD}
---

# Red Team Refinement Review

## Critique Resolution Status

| Critique | Target Hypothesis | Addressed By | Resolution |
|----------|------------------|--------------|------------|
| {Critique 1} | {Hypothesis} | {Agent or none} | RESOLVED/UNRESOLVED/INVALID |
| {Critique 2} | {Hypothesis} | {Agent or none} | RESOLVED/UNRESOLVED/INVALID |

## Revised Survival Ratings

| Hypothesis | Original Rating | Revised Rating | Reason for Change |
|------------|-----------------|----------------|-------------------|
| {Hyp 1} | WEAKENED | SURVIVED | Critique was addressed with evidence from genetics agent |
| {Hyp 2} | SURVIVED | WEAKENED | Found additional contradiction in top-down report |

## Counter-Hypotheses Update

| Counter-Hypothesis | Original Confidence | Revised Confidence | Reason |
|--------------------|--------------------|--------------------|--------|
| {Counter 1} | 30% | 45% | New supporting evidence from bottom-up agent |
| {Counter 2} | 25% | 10% | Genetics ruled out key mechanism |

## Unresolved Critiques

These critiques remain unaddressed and should factor into consensus:

1. **{Critique}**: {Why it remains important}
2. **{Critique}**: {Why it remains important}

## Final Red Team Assessment

**Strongest Hypothesis Post-Refinement**: {Name} ({confidence}%)
**Most Viable Counter-Hypothesis**: {Name} ({confidence}%)
```
```

### Wait for Refinement Completion

After spawning refinement agents:

```bash
# Check if all refined output files exist
ls -la .output/{profile}/investigation-{condition}-{date}/
# Expected additions: refined-bottomup.md, refined-topdown.md, refined-genetics.md, refined-redteam.md
```

Proceed to Phase 3 when all refinement reports complete.

---

## Phase 3: Evidence Verification Agent

Spawn verification agent AFTER Phase 2 completes:

```
Task tool with:
- subagent_type: "general-purpose"
- description: "Verify evidence citations for {condition}"
- prompt: [Evidence Verification Prompt Template]
```

### Evidence Verification Prompt Template

```markdown
Verify evidence citations AND interpretations from the ensemble investigation of {condition}.

**Input Files (include refined versions)**:
- .output/{profile}/investigation-{condition}-{date}/agent-bottomup.md
- .output/{profile}/investigation-{condition}-{date}/agent-topdown.md
- .output/{profile}/investigation-{condition}-{date}/agent-genetics.md
- .output/{profile}/investigation-{condition}-{date}/agent-redteam.md
- .output/{profile}/investigation-{condition}-{date}/refined-bottomup.md
- .output/{profile}/investigation-{condition}-{date}/refined-topdown.md
- .output/{profile}/investigation-{condition}-{date}/refined-genetics.md
- .output/{profile}/investigation-{condition}-{date}/refined-redteam.md

**Profile Data Sources**:
- Labs: {labs_path}/all.csv
- Current State: {health_log_path}/current.yaml
- Health Timeline: {health_log_path}/history.csv
- Genetics: {genetics_23andme_path}

**Reference Documentation**:
- Read `.claude/skills/health-agent/references/interpretation-validation.md` for validation rules

---

## YOUR TASK: Verify Evidence AND Interpretations

### Step 1: Extract All Evidence Citations

Read each agent report (original + refined) and extract the "Evidence Citations" table.

### Step 2: Verify Each Citation Exists

For each citation:

1. **Check file exists**:
   ```bash
   test -f "{source_file}" && echo "EXISTS" || echo "MISSING"
   ```

2. **Check claimed value matches actual data**:
   ```bash
   # For labs
   grep -i "{claimed_marker}" "{labs_path}/all.csv" | grep "{claimed_date}"

   # For timeline
   grep -i "{claimed_event}" "{health_log_path}/history.csv" | grep "{claimed_date}"

   # For current state (medications, conditions)
   grep -i "{claimed_item}" "{health_log_path}/current.yaml"

   # For genetics
   grep "^{rsid}" "{genetics_23andme_path}"
   ```

### Step 3: Interpretation Validation (NEW - CRITICAL)

For each interpretation claim, validate using rules from `interpretation-validation.md`:

#### 3a. Unit Consistency Check
- Extract all citations of the same marker across agents
- Verify units are consistent or conversions are correct
- Flag any unit mismatches

#### 3b. Reference Range Accuracy
- For each "abnormal/elevated/low" claim, verify against actual reference range
- Check if margin is significant (borderline vs truly abnormal)
- Flag overclaims (e.g., "significantly elevated" for borderline values)

#### 3c. Pattern Validity
- For "trend" claims: Verify ≥3 data points AND direction is consistent
- For "consistent" claims: Verify ≥75% of data points fit the pattern
- For "correlation" claims: Verify ≥5 paired observations
- Flag patterns based on insufficient data

#### 3d. Temporal Logic
- Verify causes precede effects in all causal claims
- Check time gaps are plausible for claimed mechanisms
- Flag any temporal violations

#### 3e. Statistical Reasonableness
- Verify confidence claims match evidence quantity
- Flag overclaiming from small samples
- Check if statistical language is appropriate

#### 3f. Causal Overclaiming
- Distinguish correlation vs causation in agent claims
- Verify causal language matches evidence strength
- Flag "causes" claims that should be "associated with"

### Step 4: Cherry-Picking Detection

For each hypothesis:
- Search for CONTRADICTORY evidence the agent may have ignored
- Flag hypotheses with unaddressed contradictions

Example:
```bash
# If agent claims "all bilirubin values elevated"
# Check for any normal bilirubin values
grep -i "bilirubin" "{labs_path}/all.csv" | awk -F',' '$5 <= $7 && $5 >= $6'
```

### Step 5: Completeness Check

For each agent, assess:
- What % of relevant data sources did they query?
- Did they check labs? Timeline? Genetics? Exams?
- Flag agents that skipped major data sources

---

## Output Format

Save to: `.output/{profile}/investigation-{condition}-{date}/evidence-verification.md`

```markdown
---
phase: evidence-verification
condition: {condition}
generated: {YYYY-MM-DD}
---

# Evidence Verification Report

## Citation Verification Results

### Agent: Bottom-Up

| # | Claim | Verified | Actual Value | Status |
|---|-------|----------|--------------|--------|
| 1 | "Bilirubin 2.8" | YES | 2.8 mg/dL | ✓ Verified |
| 2 | "Reticulocytes 3.5%" | NO | 2.1% | ⚠️ Misquoted |
| 3 | "Episode in March" | YES | 2025-03-15 | ✓ Verified |

**Verified**: X/Y citations (Z%)
**Flagged**: [List any misquotes or errors]

---

### Agent: Top-Down

[Same structure]

---

### Agent: Genetics-First

[Same structure]

---

### Agent: Red-Team

[Same structure]

---

## Interpretation Validation Results (NEW)

### Unit Consistency
| Marker | Agent 1 Unit | Agent 2 Unit | Conversion Valid | Status |
|--------|-------------|--------------|------------------|--------|
| {Marker} | {Unit 1} | {Unit 2} | YES/NO | ✓/⚠️/❌ |

**Issues Found**: {List any unit inconsistencies}

### Reference Range Accuracy
| Claim | Cited Value | Actual Range | True Status | Verdict |
|-------|-------------|--------------|-------------|---------|
| "Elevated bilirubin" | 1.3 mg/dL | 0.1-1.2 | Borderline high | ⚠️ Overclaim |
| "Normal ferritin" | 12 ng/mL | 15-150 | Actually low | ❌ Error |

**Overclaims Detected**: {Count}
**Errors Detected**: {Count}

### Pattern Validity
| Pattern Claim | Data Points | Minimum Required | Fit % | Verdict |
|---------------|-------------|------------------|-------|---------|
| "Trending upward" | 4 | 3 | 75% | ✓ Valid |
| "Consistently elevated" | 3 | 4 | 67% | ⚠️ Insufficient |

**Invalid Pattern Claims**: {List}

### Temporal Logic
| Causal Claim | Cause Date | Effect Date | Time Gap | Verdict |
|--------------|------------|-------------|----------|---------|
| "Supplement fixed deficiency" | 2025-01 | 2025-04 | 3 months | ✓ Plausible |
| "Stress caused headache" | 2025-03-15 | 2025-03-10 | -5 days | ❌ Effect before cause |

**Temporal Violations**: {Count}

### Statistical Reasonableness
| Claim | Data Size | Appropriate | Verdict |
|-------|-----------|-------------|---------|
| "85% confidence" | 2 data points | NO | ❌ Overconfident |
| "Moderate confidence" | 8 data points | YES | ✓ Reasonable |

**Overclaimed Confidence**: {List}

### Causal Overclaiming
| Original Claim | Should Be | Severity |
|----------------|-----------|----------|
| "X causes Y" | "X associated with Y" | Moderate |
| "Definitely due to" | "Likely contributes to" | Minor |

**Causal Overclaims**: {Count}

---

## Cherry-Picking Detection

### Hypothesis: {Name}

**Unaddressed Contradictions Found**:
| Evidence | Source | Impact on Hypothesis |
|----------|--------|---------------------|
| {Contradictory finding} | {Source} | WEAKENS/FATAL |

---

## Completeness Scores

| Agent | Labs | Timeline | Genetics | Exams | Overall |
|-------|------|----------|----------|-------|---------|
| Bottom-Up | ✓ | ✓ | ✓ | ✗ | 75% |
| Top-Down | ✓ | ✓ | ✗ | ✓ | 75% |
| Genetics | ✓ | ✗ | ✓ | ✗ | 50% |
| Red-Team | ✓ | ✓ | ✓ | ✓ | 100% |

---

## Verification Summary

**Citation Verification**:
- Total Citations: X
- Verified: Y (Z%)
- Flagged: W citations

**Interpretation Validation**:
- Total Interpretations: X
- Valid: Y (Z%)
- Overclaims: W
- Errors: V

**Overall Quality Score**: {X}% (citations verified × interpretations valid)

**High-Confidence Findings**: [Citations verified AND interpretations valid]
**Questionable Findings**: [Citations or interpretations with issues]
**Errors Requiring Correction**: [Factual errors that must be addressed in consensus]
```
```

---

## Phase 4: Consensus & Blind Spot Agent

Spawn consensus agent AFTER Phase 3 completes:

```
Task tool with:
- subagent_type: "general-purpose"
- description: "Generate consensus for {condition}"
- prompt: [Consensus & Blind Spot Prompt Template]
```

### Consensus & Blind Spot Prompt Template

```markdown
Generate calibrated consensus from ensemble investigation of {condition}.

**Input Files (include refined versions)**:
- .output/{profile}/investigation-{condition}-{date}/agent-bottomup.md
- .output/{profile}/investigation-{condition}-{date}/agent-topdown.md
- .output/{profile}/investigation-{condition}-{date}/agent-genetics.md
- .output/{profile}/investigation-{condition}-{date}/agent-redteam.md
- .output/{profile}/investigation-{condition}-{date}/refined-bottomup.md
- .output/{profile}/investigation-{condition}-{date}/refined-topdown.md
- .output/{profile}/investigation-{condition}-{date}/refined-genetics.md
- .output/{profile}/investigation-{condition}-{date}/refined-redteam.md
- .output/{profile}/investigation-{condition}-{date}/evidence-verification.md

**Reference Documentation**:
- Read `.claude/skills/health-agent/references/confidence-calibration.md` for calibration formulas
- Read `.claude/skills/health-agent/scientific-literature-search/SKILL.md` for blind spot detection

---

## YOUR TASK: Generate Calibrated Consensus

### Step 1: Hypothesis Inventory

List ALL unique hypotheses across all agent reports (use refined versions):

| Hypothesis | Bottom-Up | Top-Down | Genetics | Red-Team | Counter-Hyp |
|------------|-----------|----------|----------|----------|-------------|
| {Name 1} | ✓ 80% | ✓ 75% | ✗ | SURVIVED | No |
| {Name 2} | ✗ | ✓ 40% | ✓ 90% | WEAKENED | No |
| {Name 3} | ✗ | ✗ | ✗ | N/A | Yes (RT proposed) |

Include counter-hypotheses from Red Team in the inventory.

### Step 2: Verified Agreement Scoring

Only count VERIFIED evidence (from evidence-verification.md):

```
Raw Agreement Score = (Agents proposing hypothesis) / 4

Verified Score = Raw Agreement × (Verified citations / Total citations)
```

Example:
- Hypothesis X: 3/4 agents proposed (75% agreement)
- But only 60% of citations verified
- Verified Score = 0.75 × 0.60 = 0.45 (45%)

### Step 3: Contradiction Weighting

Adjust scores based on Red Team results (use refined ratings):

```
Contradiction Survival Factor:
- SURVIVED Red Team (no fatal flaws): × 1.0
- WEAKENED by Red Team (minor contradictions): × 0.8
- DESTROYED by Red Team (fatal contradiction): × 0.1
```

### Step 4: Diagnostic Gap Penalty (NEW - CRITICAL)

Reduce confidence when key diagnostic tests are unavailable. Reference: `confidence-calibration.md`

**Step 4a: Identify Missing Tests**

For each hypothesis, list diagnostic tests that could confirm/refute it but are unavailable:

| Hypothesis | Missing Test | Test Type | P(would change dx) |
|------------|--------------|-----------|-------------------|
| {Hyp 1} | EMA binding test | Gold standard | 30% |
| {Hyp 1} | Direct Coombs | Confirmatory | 40% |

**Step 4b: Calculate Gap Penalty**

```
Individual Penalty = P(test would change diagnosis) × 0.10
Total Gap Penalty = min(Σ Individual Penalties, 0.30)  # Capped at 30%

Gap-Adjusted Confidence = Raw Confidence × (1 - Gap Penalty)
```

Example:
- Raw confidence: 78%
- Missing EMA: 3%, Missing Coombs: 4%, Missing bone marrow: 1.5%
- Total gap penalty: 8.5%
- Gap-adjusted: 78% × (1 - 0.085) = 71.4%

### Step 5: Epidemiological Priors (NEW)

Adjust for condition prevalence. Reference: `confidence-calibration.md`

**Step 5a: Obtain Priors**

Query literature for prevalence of each hypothesis:
1. Search: "epidemiology {condition}" or "prevalence {condition}"
2. Adjust for patient demographics (age, gender, ancestry)

**Step 5b: Apply Bayesian Adjustment**

```
Posterior = (Likelihood × Prior) / Σ(Likelihood_i × Prior_i)

Where:
- Likelihood = Evidence support score (0-1)
- Prior = Population prevalence
```

| Hypothesis | Evidence Likelihood | Raw Prior | Demo-Adjusted Prior |
|------------|--------------------|-----------|--------------------|
| {Hyp 1} | 0.75 | 1:2000 | 1:2000 |
| {Hyp 2} | 0.70 | 1:100000 | 1:100000 |

**When to skip priors**:
- Evidence is overwhelming (likelihood >0.95)
- Patient has known risk factors changing their prior
- Rare disease specialist referral (selection bias)

### Step 6: Blind Spot Detection (CRITICAL)

Query literature for known causes of {condition} NOT proposed by any agent:

1. Read `.claude/skills/health-agent/scientific-literature-search/SKILL.md`
2. Search: "causes of {condition}" or "differential diagnosis {condition}"
3. Compare literature causes against proposed hypotheses
4. For EACH known cause NOT investigated:
   - Flag as blind spot
   - Generate brief assessment (could this apply?)
   - Note if worth investigating

### Step 7: Full Calibrated Confidence Calculation

Reference: `confidence-calibration.md`

```
Calibrated Confidence =
    Raw_Confidence
    × (1 - Gap_Penalty)
    × Evidence_Quality
    × Red_Team_Survival
    × Prior_Adjustment  # If applicable

Evidence Quality Weights:
- Genetics confirmation: 1.0
- Gold standard test: 0.95
- Lab pattern (multiple markers): 0.8
- Single lab value: 0.6
- Timeline correlation only: 0.5
- Inference/speculation: 0.3

Contradiction Survival:
- Survived RED TEAM with no fatal flaws: 1.0
- Minor contradictions addressed: 0.9
- Unaddressed contradictions: 0.5
- Fatal contradiction found: 0.1
```

### Step 8: Generate Final Ranking with Falsification Criteria

Order hypotheses by calibrated confidence. For EACH hypothesis, include:

1. **What would CONFIRM this hypothesis**:
   - Specific test results
   - Specific findings

2. **What would REFUTE this hypothesis**:
   - Specific contradicting evidence
   - Specific test results

3. **Recommended next steps** (ordered by cost/invasiveness)

---

## Output Format

Save to: `.output/{profile}/investigation-{condition}-{date}/consensus-final.md`

```markdown
---
document_type: ensemble_consensus
condition: {condition}
generated: {YYYY-MM-DD}
profile: {profile}
agents: 4
phases: 7
refinement: true
state_updated: true
---

# Ensemble Root Cause Investigation: {Condition}

## Executive Summary

**Primary Hypothesis**: {Name}
**Calibrated Confidence**: {XX}% (±Y%)
**Agreement**: X/4 agents
**Red Team Status**: SURVIVED / WEAKENED
**Gap Penalty Applied**: {X}% (for missing tests)

{2-3 sentence summary of investigation findings}

---

## Methodology

This investigation used 4 parallel agents with different reasoning strategies:
1. **Bottom-Up**: Data-driven pattern discovery
2. **Top-Down**: Systematic differential diagnosis
3. **Genetics-First**: Genetic etiology prioritization
4. **Red Team**: Adversarial hypothesis testing with alternative proposals

Enhanced with:
- **Cross-Agent Refinement**: Agents reviewed each other's findings and revised
- **Interpretation Validation**: Verified not just citations but interpretation validity
- **Diagnostic Gap Penalty**: Confidence reduced for missing confirmatory tests
- **Epidemiological Priors**: Adjusted for condition prevalence
- **Falsification Criteria**: Each hypothesis specifies confirmation/refutation conditions

---

## Diagnostic Gap Assessment (NEW)

### Missing Tests That Could Change Diagnosis

| Missing Test | Test Type | Relevant Hypotheses | P(would change dx) | Penalty |
|--------------|-----------|---------------------|-------------------|---------|
| {Test 1} | Gold standard | {Hyp A, B} | 30% | 3% |
| {Test 2} | Confirmatory | {Hyp A} | 20% | 2% |
| {Test 3} | Rule-out | {Hyp C} | 40% | 4% |

**Total Gap Penalty**: {X}% (capped at 30%)

**Interpretation**: Confidence is reduced by {X}% because these tests, if available, could confirm or refute the hypotheses. This is a limitation, not a flaw in the investigation.

---

## Epidemiological Prior Analysis (NEW)

### Condition Prevalence Comparison

| Hypothesis | Evidence Likelihood | Population Prevalence | Demo-Adjusted | Bayesian Posterior |
|------------|--------------------|-----------------------|---------------|-------------------|
| {Hyp 1} | 0.75 | 1:2000 (0.05%) | Same | 85% |
| {Hyp 2} | 0.70 | 1:100000 (0.001%) | Same | 3% |
| {Hyp 3} | 0.50 | 1:20 (5%) | Same | 12% |

**Prior Sources**: [PMID citations for epidemiology data]

**Adjustment Applied**: {YES with explanation / NO with reason (e.g., evidence overwhelming)}

---

## Hypothesis Ranking (Fully Calibrated)

### Rank 1: {Hypothesis Name}

**Calibrated Confidence**: {XX}% (±Y%)

| Metric | Value |
|--------|-------|
| Agent Agreement | X/4 (refined) |
| Verified Citations | Y% |
| Interpretation Validity | Z% |
| Evidence Quality | {HIGH/MODERATE/LOW} |
| Red Team Status | SURVIVED/WEAKENED |
| Gap Penalty | -{X}% |
| Prior Adjustment | {×Y or N/A} |
| Blind Spot Risk | LOW |

**Full Calculation**:
```
Raw Confidence: {X}%
× (1 - Gap Penalty {Y}%): {Z}%
× Evidence Quality: {W}%
× Red Team Survival: {V}%
× Prior Adjustment: {U}
= Calibrated: {XX}%
Uncertainty: ±{Y}%
```

**Supporting Evidence** (verified + interpretation validated):
1. ✅ {Evidence 1 with citation}
2. ✅ {Evidence 2 with citation}

**Contradictions** (addressed in refinement):
1. ⚠️ {Contradiction 1 - explanation from refined report}

**Mechanism** (literature-supported):
{Biological pathway with PMID citations}

#### Falsification Criteria (NEW)

**This hypothesis would be CONFIRMED if**:
- [ ] {Specific test result (e.g., "EMA binding test positive")}
- [ ] {Specific finding (e.g., "Bone marrow shows specific morphology")}
- [ ] {Specific genetic test (e.g., "Clinical sequencing finds pathogenic variant")}

**This hypothesis would be REFUTED if**:
- [ ] {Specific contradicting evidence (e.g., "Direct Coombs test positive")}
- [ ] {Specific test result (e.g., "Normal osmotic fragility")}
- [ ] {Specific finding (e.g., "No family history after detailed inquiry")}

**Recommended Next Steps** (ordered by cost/invasiveness):
1. {Low cost/invasive}: {Test and expected result}
2. {Moderate}: {Test and expected result}
3. {Higher}: {Test and expected result if still unresolved}

---

### Rank 2: {Hypothesis Name}

[Same structure including falsification criteria]

---

### Rank 3: {Hypothesis Name}

[Same structure including falsification criteria]

---

## Counter-Hypotheses from Red Team

Red Team proposed these alternatives that deserve consideration:

### Counter-Hypothesis: {Name}

**Origin**: Proposed by Red Team when destroying/weakening {original hypothesis}
**Red Team Confidence**: {X}%
**Evidence Supporting**: {List}
**Why Not Ranked Higher**: {Explanation}
**Worth Investigating**: YES/NO

---

## Blind Spots Detected

### {Known Cause Not Investigated}

**Why Flagged**: Listed in literature as cause of {condition}, but no agent investigated.

**Quick Assessment**: {Could this apply to this patient? Brief analysis.}

**Recommendation**: {Investigate further / Unlikely / Ruled out by existing evidence}

---

## Cross-Agent Refinement Impact

### How Refinement Changed Results

| Hypothesis | Pre-Refinement | Post-Refinement | Change |
|------------|----------------|-----------------|--------|
| {Hyp 1} | 75% | 80% | +5% (corroborated) |
| {Hyp 2} | 60% | 45% | -15% (critique addressed) |

### Red Team Critiques Resolution

| Critique | Status | Resolution |
|----------|--------|------------|
| {Critique 1} | RESOLVED | {How addressed} |
| {Critique 2} | UNRESOLVED | {Still factors into confidence} |

---

## Unresolved Conflicts

Where agents disagreed after refinement:

| Topic | Bottom-Up | Top-Down | Genetics | Red-Team |
|-------|-----------|----------|----------|----------|
| {Issue 1} | {View} | {View} | {View} | {View} |

**Resolution Path**: {How to resolve this disagreement}

---

## Evidence Quality Assessment

| Evidence Type | Count | Weight | Contribution |
|---------------|-------|--------|--------------|
| Genetics confirmation | X | 1.0 | {XX}% |
| Lab pattern | Y | 0.8 | {YY}% |
| Timeline correlation | Z | 0.5 | {ZZ}% |

**Interpretation Validation**:
- Valid interpretations: {X}%
- Overclaims corrected: {Y}
- Errors identified: {Z}

---

## Recommended Follow-Up

### High Priority (Would Resolve Diagnosis)
1. {Test 1}: Would {confirm/refute} primary hypothesis
   - If positive: Confirms {hypothesis}
   - If negative: Refutes {hypothesis}, investigate {alternative}

2. {Test 2}: Would resolve diagnostic gap
   - Addresses missing test penalty of {X}%

### Moderate Priority (Additional Confirmation)
3. {Test 3}: Additional supporting evidence

### Blind Spot Investigation
4. {Test 4}: Would rule out {blind spot condition}

---

## Limitations

- Agent agreement ≠ correctness (all agents can make same error)
- Cross-agent refinement helps but doesn't eliminate correlated errors
- Gap penalty estimates are approximate
- Epidemiological priors may not reflect patient-specific risk factors
- 23andMe genetics limited to ~631k SNPs
- Timeline data depends on user's recording accuracy
- Literature search limited to PubMed/Semantic Scholar

---

## Medical Disclaimer

This ensemble investigation is a data-driven analysis using multiple reasoning strategies, cross-agent refinement, and calibrated confidence calculations. **This is not medical advice**.

- Calibrated confidence reflects data support and uncertainty, not diagnostic certainty
- Gap-adjusted confidence acknowledges missing diagnostic tests
- Multiple mechanisms may coexist
- Blind spots may still exist despite detection efforts
- Falsification criteria are for informational purposes
- Always consult healthcare provider for clinical decisions and diagnostic testing

---

*Ensemble investigation completed using 4 parallel agents + refinement + verification + consensus + state update*
*Phases: 7 (spawn → refine → verify → consensus → blind spots → state update → report)*
*Generated: {YYYY-MM-DD}*
*Profile: {profile}*
*Health state updated: .state/{profile}/health-state.yaml*
```
```

---

## Phase 5: Update Health State

After consensus is complete, update `.state/{profile}/health-state.yaml` to persist the investigation findings.

### Step 5.1: Check if State File Exists

```bash
test -f ".state/{profile}/health-state.yaml" && echo "EXISTS" || echo "MISSING"
```

If missing, create directory and initialize:
```bash
mkdir -p .state/{profile}
```

Then create from template `.state/_template/health-state.yaml` or existing data.

### Step 5.2: Add/Update Condition

From the consensus report, extract and add/update the condition entry:

```yaml
conditions:
  - name: "{condition}"  # From investigation target
    status: active  # active (symptomatic) or monitoring (stable/mild)
    confidence: {calibrated_confidence}  # From consensus
    primary_hypothesis: "{top_hypothesis_name}"
    hypotheses:  # Ranked list from consensus
      - name: "{hypothesis_1}"
        confidence: {confidence_1}
      - name: "{hypothesis_2}"
        confidence: {confidence_2}
    diagnostic_gaps:  # From gap assessment
      - "{missing_test_1}"
      - "{missing_test_2}"
    investigation_ref: "investigation-{condition}-{date}"
```

### Step 5.3: Generate Actions from Recommended Follow-up

Convert the "Recommended Follow-up" section into prioritized actions:

**Priority Assignment**:
| Criteria | Priority |
|----------|----------|
| Would resolve diagnosis (high confidence impact) | high |
| Addresses diagnostic gap | high |
| Additional confirmation | medium |
| Blind spot investigation | medium |
| Optional/supplementary | low |

**Dependency Detection**:
- If test requires provider appointment → create appointment action first, set dependency
- If test requires prior test results → set dependency on prior test

**Due Date Assignment**:
- Urgent/time-sensitive: 2 weeks
- High priority: 1 month
- Medium priority: 2-3 months
- Low priority: No specific due date

```yaml
actions:
  - id: {next_available_id}
    action: "{test_or_action_from_followup}"
    priority: high  # Based on criteria above
    why: "{from_consensus_explanation}"
    status: recommended
    due: "YYYY-MM-DD"
    depends_on: []  # Or list of action ids
```

### Step 5.4: Update Genetics if Relevant Variants Found

If the investigation found relevant genetic variants:

```yaml
genetics:
  data_source: "23andme"  # or "selfdecode" or "both"
  key_findings:
    - gene: "{gene_name}"
      rsid: "{rs_number}"  # If specific SNP
      genotype: "{genotype}"
      significance: "{clinical_significance}"
```

### Step 5.5: Create/Update Goal

If no existing goal for this condition:

```yaml
goals:
  - goal: "Identify root cause of {condition}"
    target_date: "YYYY-MM-DD"  # 6 months from now
    progress: {estimated_progress}%
    success_criteria: "Diagnosis confidence > 70%"
```

Progress estimation:
- Initial investigation: 30%
- One confirmatory test completed: 50%
- Multiple tests completed: 70%
- Diagnosis established: 100%

### Step 5.6: Update last_updated Timestamp

```yaml
last_updated: "{today's date YYYY-MM-DD}"
```

### Step 5.7: Write Updated State File (Atomic)

Use atomic write pattern to prevent corruption:

```bash
STATE_FILE=".state/{profile}/health-state.yaml"
BACKUP_FILE=".state/{profile}/health-state.yaml.bak"
TEMP_FILE=".state/{profile}/health-state.yaml.tmp"

# 1. Backup existing state
if [ -f "$STATE_FILE" ]; then
    cp "$STATE_FILE" "$BACKUP_FILE"
fi
```

Then use the Write tool to write to the temp file path, validate YAML, and move:

```bash
# 2. Validate new state (basic YAML check)
if python3 -c "import yaml; yaml.safe_load(open('$TEMP_FILE'))" 2>/dev/null; then
    mv "$TEMP_FILE" "$STATE_FILE"
else
    echo "ERROR: Invalid YAML - state not updated"
    rm -f "$TEMP_FILE"
    # Original state preserved
fi
```

**IMPORTANT**: If the state write fails, the investigation results are still available in `consensus-final.md`. The user can manually apply findings or re-run Phase 5.

**Example state update after hemolysis investigation**:

```yaml
conditions:
  - name: "Chronic Compensated Hemolysis"
    status: active
    confidence: 0.54
    primary_hypothesis: "Hereditary Spherocytosis"
    hypotheses:
      - name: "Hereditary Spherocytosis"
        confidence: 0.54
      - name: "Idiopathic"
        confidence: 0.25
      - name: "Congenital Dyserythropoietic Anemia"
        confidence: 0.15
    diagnostic_gaps:
      - "EMA binding test"
      - "Direct Coombs test"
      - "Genetic panel (ANK1/SPTB)"
    investigation_ref: "investigation-chronic-hemolysis-2026-01-22"

actions:
  - id: 1
    action: "Schedule hematology follow-up"
    priority: high
    why: "Required to order EMA test and discuss investigation findings"
    status: recommended
    due: "2026-02-15"
    depends_on: []
  - id: 2
    action: "Request EMA binding test"
    priority: high
    why: "Would confirm/exclude hereditary spherocytosis (primary hypothesis)"
    status: recommended
    due: "2026-03-01"
    depends_on: [1]
  - id: 3
    action: "Request Direct Coombs test"
    priority: high
    why: "Would rule out autoimmune hemolysis"
    status: recommended
    due: "2026-03-01"
    depends_on: [1]

goals:
  - goal: "Identify root cause of hemolysis"
    target_date: "2026-07-22"
    progress: 30%
    success_criteria: "Diagnosis confidence > 70%"
```

---

## Phase 6: Return Final Report Path

After consensus report is generated and state updated:

1. Verify all output files exist:
```bash
ls -la .output/{profile}/investigation-{condition}-{date}/
```

Expected files:
- `agent-bottomup.md` (Phase 1)
- `agent-topdown.md` (Phase 1)
- `agent-genetics.md` (Phase 1)
- `agent-redteam.md` (Phase 1)
- `refined-bottomup.md` (Phase 2.5)
- `refined-topdown.md` (Phase 2.5)
- `refined-genetics.md` (Phase 2.5)
- `refined-redteam.md` (Phase 2.5)
- `evidence-verification.md` (Phase 3)
- `consensus-final.md` (Phase 4)

2. Verify state file was updated:
```bash
head -20 .state/{profile}/health-state.yaml
```

3. Return summary to user:

```markdown
## Ensemble Investigation Complete

**Condition**: {condition}
**Output Directory**: `.output/{profile}/investigation-{condition}-{date}/`

**Files Generated**:
- 4 agent investigation reports (Phase 1)
- 4 refined reports after cross-agent review (Phase 2.5)
- Evidence & interpretation verification report (Phase 3)
- Final consensus report with calibrated confidence (Phase 4)

**Primary Hypothesis**: {Name}
**Calibrated Confidence**: {XX}% (±Y%)
**Gap Penalty Applied**: -{Z}% (for {N} missing tests)

### Key Falsification Criteria
**Would confirm**: {top 2 confirmation criteria}
**Would refute**: {top 2 refutation criteria}

### Health State Updated
- Condition added/updated with {N} hypotheses
- {N} actions generated (prioritized)
- Goal created: "Identify root cause of {condition}"

**Read full consensus**: `.output/{profile}/investigation-{condition}-{date}/consensus-final.md`
**View pending actions**: `.state/{profile}/health-state.yaml`
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **Agent timeout (>15 min)** | Proceed with available agents; note gap in consensus |
| **Agent fails** | Log error; reduce consensus confidence |
| **Refinement agent fails** | Use original (unrefined) report; note limitation |
| **No genetics data** | Genetics-first agent adapts; notes limitation |
| **All agents agree on wrong hypothesis** | Blind spot detection queries literature for alternatives |
| **Verification finds >30% citation errors** | Flag low-quality investigation; recommend re-run |
| **Interpretation validation finds >20% errors** | Flag interpretation issues; adjust confidence accordingly |
| **No clear consensus** | Report uncertainty; list discriminating tests needed |
| **Red Team proposes no alternatives** | Flag incomplete Red Team analysis; reduce adversarial confidence weight |
| **Gap penalty exceeds 30%** | Cap at 30%; note severe diagnostic limitations |
| **Epidemiological priors unavailable** | Skip prior adjustment; note limitation in report |
| **State file doesn't exist** | Create from template; initialize with investigation findings |
| **State file write fails** | Report error; investigation results still in consensus-final.md |

---

## Example Invocation

**User**: "Run an ensemble investigation on my chronic hemolysis"

**Assistant Process**:

1. Load profile and extract data source paths

2. **Phase 1**: Spawn 4 agents in parallel (single message with 4 Task calls):
   - Bottom-Up: Start with all abnormal labs, find hemolysis patterns
   - Top-Down: Differential diagnosis of hemolysis (hereditary vs acquired)
   - Genetics-First: Check spherocytosis genes, G6PD, pyruvate kinase, etc.
   - Red Team: Try to disprove hemolysis hypotheses AND propose alternatives

3. **Phase 2**: Wait for all agents to complete (background)

4. **Phase 2.5 (NEW)**: Spawn 4 refinement agents in parallel:
   - Each agent reviews others' findings
   - Agents revise hypotheses based on new evidence
   - Red Team verifies if critiques were addressed
   - Results in refined-*.md files

5. **Phase 3**: Spawn Evidence Verification Agent:
   - Check all lab value citations
   - Verify genetic findings
   - **Validate interpretations** (unit consistency, temporal logic, pattern validity)
   - Detect cherry-picking

6. **Phase 4**: Spawn Consensus Agent:
   - Merge verified findings (use refined versions)
   - **Apply diagnostic gap penalty** for missing tests
   - **Incorporate epidemiological priors**
   - Calculate fully calibrated confidence
   - Check blind spots (query literature for other hemolysis causes)
   - **Add falsification criteria** for each hypothesis
   - Generate final ranking

7. **Phase 5**: Update Health State:
   - Add condition "Chronic Compensated Hemolysis" with hypotheses
   - Generate 3 prioritized actions from follow-up recommendations
   - Create goal "Identify root cause of hemolysis" (30% progress)
   - Write updated state file

8. **Phase 6**: Return:
   ```
   ## Ensemble Investigation Complete

   **Primary Hypothesis**: Hereditary Spherocytosis
   **Calibrated Confidence**: 54% (±10%)
   **Gap Penalty Applied**: -10.5% (missing EMA, Coombs, bone marrow)

   ### Key Falsification Criteria
   **Would confirm**: Positive EMA binding test, clinical gene panel confirms ANK1/SPTB
   **Would refute**: Positive direct Coombs (autoimmune), normal osmotic fragility

   ### Health State Updated
   - Condition added with 3 hypotheses
   - 3 actions generated (2 high priority, 1 medium)
   - Goal created: "Identify root cause of hemolysis"

   - 4/4 agents proposed (refined)
   - Survived Red Team (critiques addressed in refinement)
   - Genetics support found (23andMe variant)
   - Interpretation validation: 95% valid
   - Red Team counter-hypothesis: Congenital Dyserythropoietic Anemia (15% confidence)

   **Output**: .output/{profile}/investigation-chronic-hemolysis-2026-01-22/consensus-final.md
   **Actions**: .state/{profile}/health-state.yaml
   ```

---

## Comparison: Standard vs Ensemble Investigation

| Aspect | Standard | Ensemble |
|--------|----------|----------|
| **Agents** | 1 | 4 parallel + 4 refinement + 2 sequential |
| **Reasoning paths** | Single | 4 independent strategies |
| **Cross-agent learning** | No | Yes (Phase 2.5 refinement) |
| **Adversarial testing** | Optional | Mandatory + alternatives required |
| **Evidence verification** | No | Yes |
| **Interpretation validation** | No | Yes (unit, temporal, statistical checks) |
| **Blind spot detection** | No | Yes |
| **Diagnostic gap penalty** | No | Yes (reduces overconfidence) |
| **Epidemiological priors** | No | Yes (Bayesian adjustment) |
| **Falsification criteria** | No | Yes (per hypothesis) |
| **Confidence calibration** | Subjective | Fully calculated from metrics |
| **Counter-hypotheses** | No | Yes (from Red Team) |
| **Health state update** | No | Yes (Phase 5 - persists findings) |
| **Action generation** | No | Yes (prioritized next steps) |
| **Execution time** | ~5-10 min | ~20-30 min |
| **Use case** | Routine investigation | High-stakes, complex cases |

Use standard `investigate-root-cause` for routine cases. Use ensemble for complex cases requiring maximum diagnostic accuracy and calibrated confidence.
