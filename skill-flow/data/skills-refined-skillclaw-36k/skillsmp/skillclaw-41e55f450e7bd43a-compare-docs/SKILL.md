---
name: compare-docs
description: Use this skill when you need to compare two documents semantically to identify content and structural differences while preserving relationships.
---

# Semantic Document Comparison Command

**Task**: Compare two documents semantically: `{{arg1}}` vs `{{arg2}}`

**Goal**: Determine if documents contain the same semantic content AND preserve relationships (temporal, conditional, cross-document) despite different wording/organization.

**Method**: Enhanced claim extraction + relationship extraction + execution equivalence scoring.

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
   - Mitigation: Use `temperature=0` in all Task calls.
2. **Model Version** (±1-3% score drift across versions)
   - Mitigation: Pin exact model version (e.g., `"claude-opus-4-5-20251101"`).
3. **Semantic Judgment** (±1-2% for boundary cases).