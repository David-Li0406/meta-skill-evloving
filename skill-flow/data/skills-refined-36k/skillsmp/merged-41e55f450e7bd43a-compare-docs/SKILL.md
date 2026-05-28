---
name: compare-docs
description: Compare two documents semantically with relationship preservation to identify content and structural differences.
---

# Semantic Document Comparison Command

**Task**: Compare two documents semantically: `{{arg1}}` vs `{{arg2}}`

**Goal**: Determine if documents contain the same semantic content AND preserve relationships (temporal, conditional, cross-document) despite different wording/organization.

**Method**: Enhanced claim extraction + relationship extraction + execution equivalence scoring

**⚠️ CRITICAL: Independent Extraction Required**

This command MUST extract claims from BOTH documents independently. NEVER:
- Pre-populate with "items to verify" or "improvements to check"
- Prime the extractor with knowledge of what changed between documents
- Use targeted confirmation instead of full extraction

Targeted validation (telling extractor what to look for) inflates scores by confirming a checklist rather than independently discovering all claims.

---

## Overview

**Workflow**:
1. **Extract enhanced claims + relationships from Document A IN PARALLEL**
2. **Extract enhanced claims + relationships from Document B IN PARALLEL**
3. Compare claim sets AND relationship graphs (after both complete)
4. Calculate execution equivalence score (claim 40% + relationship 40% + graph 20%)
5. Report: shared/unique claims, preserved/lost relationships, warnings

**⚡ CRITICAL: Steps 1 and 2 MUST run in parallel (single message with two Task calls)**
- Extractions are completely independent (no cross-contamination risk)
- Running sequentially wastes time (~50% slower for no accuracy benefit)
- Step 3 waits for both to complete before comparing

**Key Insight**: Claim preservation ≠ Execution preservation. Documents can have identical claims but different execution behavior if relationships are lost.

**Reproducibility and Determinism**:

This command aims for high reproducibility but cannot guarantee perfect determinism due to LLM semantic judgment.

**Sources of Variance**:
1. **LLM Temperature** (±2-5% score variance if >0)
   - Mitigation: Use `temperature=0` in all Task calls
   - Expected with temp=0: ±0.5-1% residual variance
2. **Model Version** (±1-3% score drift across versions)
   - Mitigation: Pin exact model version (e.g., `"claude-opus-4-5-20251101"`)
3. **Semantic Judgment** (±1-2% for boundary cases)
   - Claim similarity: "essentially the same" vs "slightly different"
   - Relationship matching: "same constraint" vs "subtly modified"
4. **Claim Boundary Detection** (±0.5-1% for complex nested claims)
   - Conjunctions: Split into parts vs preserved as unit
   - Conditionals: Boundary of IF-THEN-ELSE scope

**Expected Reproducibility**:
- **Same session, same documents**: ±0-1% (near-identical, small rounding differences)
- **Different sessions, temp=0, pinned model**: ±1-2% (good reproducibility)
- **Different sessions, temp>0**: ±3-7% (moderate variance)
- **Different model versions**: ±5-10% (significant drift possible)

**Best Practices for Consistency**:
- Always use `temperature=0`
- Pin model version if absolute consistency required across sessions
- Accept ±1-2% variance as inherent to semantic analysis
- Focus on score interpretation range (≥0.95, 0.85-0.94, etc.) not exact decimal

---

## Steps 1 & 2: Extract Claims + Relationships from BOTH Documents (IN PARALLEL)

**⚡ CRITICAL**: Invoke BOTH extraction agents in a single message with two Task tool calls.

**Why Parallel Execution**:
- ✅ **Safe**: Extractions are completely independent (no shared state)
- ✅ **Accurate**: No cross-contamination between Document A and B analysis
- ✅ **Faster**: ~50% time reduction (both extractions run simultaneously)
- ✅ **Required by Step 3**: Comparison waits for both anyway

**Agent Prompt Template** (use for BOTH documents):

**Agent Prompt**:
```
**SEMANTIC CLAIM AND RELATIONSHIP EXTRACTION**

**Document**: {{arg1}}

**Your Task**: Extract all semantic claims AND relationships from this document.

---

## Part 1: Claim Extraction

**What is a "claim"?**
- A requirement, instruction, rule, constraint, fact, or procedure
- A discrete unit of meaning that can be verified as present/absent
- Examples: "must do X before Y", "prohibited to use Z", "setting W defaults to V"

**Claim Types**:

1. **Simple Claims** (requirement, instruction, constraint, fact, configuration)
2. **Conjunctions**: ALL of {X, Y, Z} must be true
   - Markers: "ALL of the following", "both X AND Y", "requires all"
3. **Conditionals**: IF condition THEN consequence_true ELSE consequence_false
   - Markers: "IF...THEN...ELSE", "when X, do Y", "depends on"
4. **Consequences**: Actions that result from conditions/events
   - Markers: "results in", "causes", "leads to", "enforcement"
5. **Negations with Scope**: Prohibition with explicit scope
   - Markers: "NEVER", "prohibited", "CANNOT", "forbidden"

**Extraction Rules**:

1. **Granularity**: Atomic claims (cannot split without losing meaning)
2. **Completeness**: Extract ALL claims, including implicit ones if unambiguous
3. **Context**: Include minimal context for understanding
4. **Exclusions**: Skip pure examples, meta-commentary, table-of-contents

**Normalization Rules** (apply to all claim types):

1. **Tense**: Present tense ("create" not "created")
2. **Voice**: Imperative/declarative ("verify changes" not "you should verify")
3. **Synonyms**: Normalize common variations:
   - "must/required/mandatory" → "must"
   - "prohibited/forbidden/never" → "prohibited"
   - "create/establish/generate" → "create"
   - "remove/delete/cleanup" → "remove"
   - "verify/validate/check/confirm" → "verify"
4. **Negation**: Standardize ("must not X" → "prohibited to X")
5. **Quantifiers**: Normalize ("≥80%", "<100")
6. **Filler**: Remove filler words

---

## Part 2: Relationship Extraction

**Relationship Types to Extract**:

1. **Temporal Dependencies (Step A → Step B)**
   - Markers: "before", "after", "then", "Step N must occur after Step M", "depends on completing"
2. **Prerequisite Relationships (Condition → Action)**
   - Markers: "prerequisite", "required before", "must be satisfied before"
3. **Hierarchical Conjunctions (ALL of X must be true)**
   - Markers: "ALL", "both...AND...", "requires all", nested lists
4. **Conditional Relationships (IF-THEN-ELSE)**
   - Markers: "IF...THEN...ELSE", "when X, do Y", "depends on"
5. **Exclusion Constraints (A and B CANNOT co-occur)**
   - Markers: "CANNOT run concurrently", "NEVER together", "mutually exclusive"
6. **Escalation Relationships (State A → State B under trigger)**
   - Markers: "escalate to", "redirect to", "upgrade severity"
7. **Cross-Document References (Doc A → Doc B Section X)**
   - Markers: "see Section X.Y", "defined in Document Z", "refer to"

---

## Output Format (JSON)

```json
{
  "claims": [
    {
      "id": "claim_1",
      "type": "simple|conjunction|conditional|consequence|negation",
      "text": "normalized claim text",
      "location": "line numbers or section",
      "confidence": "high|medium|low",

      // For conjunctions
      "sub_claims": ["claim_2", "claim_3"],
      "all_required": true,

      // For conditionals
      "condition": "condition text",
      "true_consequence": "claim_4",
      "false_consequence": "claim_5",

      // For consequences
      "triggered_by": "event or condition",
      "impact": "severity description",

      // For negations
      "prohibition": "what is prohibited",
      "scope": "when prohibition applies",
      "violation_consequence": "what happens if violated"
    }
  ],
  "relationships": [
    {
      "id": "rel_1",
      "type": "temporal|prerequisite|conditional|exclusion|escalation|cross_document",
      "from_claim": "claim_1",
      "to_claim": "claim_2",
      "constraint": "must occur after|required before|IF-THEN|CANNOT co-occur",
      "strict": true,
      "evidence": "line numbers and quote",
      "violation_consequence": "what happens if relationship violated"
    }
  ],
  "dependency_graph": {
    "nodes": ["claim_1", "claim_2", "claim_3"],
    "edges": [
      ["claim_1", "claim_2"],
      ["claim_2", "claim_3"]
    ],
    "topology": "linear_chain|tree|dag|cyclic",
    "critical_path": ["claim_1", "claim_2", "claim_3"]
  },
  "metadata": {
    "total_claims": 10,
    "total_relationships": 5,
    "relationship_types": {
      "temporal": 3,
      "conditional": 1,
      "exclusion": 1
    }
  }
}
```

**CRITICAL**: Extract ALL relationships, not just claims. Relationships are as important as claims for execution equivalence.
```

**Execute PARALLEL extraction (single message with TWO Task calls)**:

```bash
# ⚡ INVOKE BOTH AGENTS IN PARALLEL (single message, 2 Task tool calls)
# This is a SINGLE assistant message containing TWO Task invocations

Task(
  subagent_type="general-purpose",
  model="opus",  # For reproducibility, consider pinning: "claude-opus-4-5-20251101"
  temperature=0,   # Deterministic sampling for consistency
  description="Extract claims from Document A",
  prompt="[Full extraction prompt above]

  Document: {{arg1}}

  Extract all claims and relationships.
  Return COMPLETE JSON (not summary)."
)

Task(
  subagent_type="general-purpose",
  model="opus",  # For reproducibility, consider pinning: "claude-opus-4-5-20251101"
  temperature=0,   # Deterministic sampling for consistency
  description="Extract claims from Document B",
  prompt="[Full extraction prompt above]

  Document: {{arg2}}

  Extract all claims and relationships.
  Return COMPLETE JSON (not summary)."
)

# Wait for BOTH agents to complete, then save results

# Save Document A extraction
cat > /tmp/compare-doc-a-extraction.json << 'EOF'
{agent JSON response with ALL claims and relationships from Document A}
EOF

# Save Document B extraction
cat > /tmp/compare-doc-b-extraction.json << 'EOF'
{agent JSON response with ALL claims and relationships from Document B}
EOF

echo "✅ Saved Document A extraction: $(wc -l < /tmp/compare-doc-a-extraction.json) lines"
echo "✅ Saved Document B extraction: $(wc -l < /tmp/compare-doc-b-extraction.json) lines"
```

**❌ WRONG: Sequential Execution**
```bash
# DON'T do this - wastes time
Task(doc A) → wait → save
Task(doc B) → wait → save  # Unnecessarily sequential
```

**✅ CORRECT: Parallel Execution**
```bash
# Single message with both Task calls
Task(doc A)
Task(doc B)
# Both run simultaneously, then save both results
```

---

## Step 3: Compare Claims AND Relationships

**Invoke comparison agent** with enhanced comparison logic:

**Agent Prompt**:
```
**SEMANTIC COMPARISON WITH RELATIONSHIP ANALYSIS**

**Document A Data**: {{DOC_A_DATA}}

**Document B Data**: {{DOC_B_DATA}}

**Your Task**: Compare claims AND relationships to determine execution equivalence.

---

## Part 1: Claim Comparison

**Comparison Rules**:

1. **Exact Match**: Identical normalized text → shared
2. **Semantic Equivalence**: Different wording, identical meaning → shared
3. **Type Mismatch**: Same concept but different structure (e.g., conjunction split into separate claims) → flag as structural change
4. **Unique**: Claims appearing in only one document

**Enhanced Claim Comparison**:

- **Conjunctions**: Two conjunctions equivalent ONLY if same sub-claims AND all_required matches
- **Conditionals**: Equivalent ONLY if same condition AND same true/false consequences
- **Consequences**: Match on trigger AND impact
- **Negations**: Match on prohibition AND scope

---

## Part 2: Relationship Comparison

**Relationship Matching Rules**:

1. **Exact Match**: Same type, same from/to claims, same constraint → preserved
2. **Missing Relationship**: Exists in A but not in B → lost
3. **New Relationship**: Exists in B but not in A → added
4. **Modified Relationship**: Same claims but different constraint → changed

**Relationship Preservation Scoring**:

```python
def calculate_relationship_preservation(a_rels, b_rels, shared_claims):
    # Only count relationships where both endpoints are shared claims
    a_valid = [r for r in a_rels if r.from in shared_claims and r.to in shared_claims]
    b_valid = [r for r in b_rels if r.from in shared_claims and r.to in shared_claims]

    preserved = count_matching_relationships(a_valid, b_valid)
    lost = len(a_valid) - preserved
    added = len(b_valid) - preserved

    if len(a_valid) == 0:
        return 1.0  # No relationships to preserve

    return preserved / len(a_valid)
```

---

## Part 3: Dependency Graph Comparison

**Graph Comparison**:

1. **Topology**: Compare graph structure (linear_chain vs tree vs dag)
2. **Connectivity**: Compare edge preservation (same connections?)
3. **Critical Path**: Compare critical paths (same ordering?)

**Graph Structure Score**:

```python
def calculate_graph_score(a_graph, b_graph, shared_claims):
    # Subgraph of shared claims
    a_sub = subgraph(a_graph, shared_claims)
    b_sub = subgraph(b_graph, shared_claims)

    # Compare connectivity
    connectivity = edge_preservation(a_sub, b_sub)

    # Compare topology
    topology = 1.0 if a_sub.topology == b_sub.topology else 0.5

    # Compare critical path
    critical_path = path_similarity(a_sub.critical_path, b_sub.critical_path)

    return (connectivity * 0.5) + (topology * 0.25) + (critical_path * 0.25)
```

---

## Part 4: Execution Equivalence Scoring

**Scoring Formula**:

```python
def calculate_execution_equivalence(claim_comp, rel_comp, graph_comp):
    weights = {
        "claim_preservation": 0.4,
        "relationship_preservation": 0.4,
        "graph_structure": 0.2
    }

    scores = {
        "claim_preservation": claim_comp["semantic_equivalence"],
        "relationship_preservation": rel_comp["overall_preservation"],
        "graph_structure": graph_comp["structure_score"]
    }

    base_score = sum(weights[k] * scores[k] for k in