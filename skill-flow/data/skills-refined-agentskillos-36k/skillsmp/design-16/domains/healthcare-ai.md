# Healthcare AI Domain Invariants

Extends: [[system-invariants]], [[data-architecture]]
Domain: Clinical AI systems, medical RAG, diagnostic support, healthcare LLM applications

---

## When to Use

Load this domain for:
- Medical/clinical AI systems
- Healthcare RAG applications
- Diagnostic support tools
- Pathology image analysis
- Clinical decision support
- Patient-facing health AI
- HLS (Healthcare & Life Sciences) projects

---

## Domain Invariants (27-30)

### 27. Safety Must Be Enforced by Code, Not Prompts

**Principle**: Safety-critical outputs cannot rely on LLM prompt compliance

**Violation**: Expecting LLM to add disclaimers, caveats, or review flags via prompt instructions

**Examples**:
- ❌ "Prompt: Always include a disclaimer that this is not medical advice"
- ❌ "Prompt: Add confidence caveats when uncertain"
- ❌ "Prompt: Flag malignancy findings for pathologist review"
- ✅ "Code post-processes ALL outputs to append: 'This is AI-generated. Verify with qualified professional.'"
- ✅ "Code detects confidence < threshold → injects LOW_CONFIDENCE_CAVEAT constant into response"
- ✅ "Code scans for malignancy_terms → sets requires_pathologist_review=True + appends review notice"

**Rationale**: LLMs are probabilistic. Prompts are suggestions, not guarantees. Safety-critical behaviors must be deterministic.

**Enforcement**: Safety outputs must be: code_enforced + deterministic + testable → Prompt-only safety = REJECT

---

### 28. Clinical Outputs Must Flag Human Review

**Principle**: Any diagnostic or treatment-adjacent output must include human review flag

**Violation**: AI outputs about diagnosis, prognosis, or treatment without review mechanism

**Examples**:
- ❌ "Return diagnosis classification directly"
- ❌ "Provide treatment recommendation"
- ❌ "Show pathology assessment"
- ✅ "diagnosis_result + requires_clinical_review=True + review_urgency(HIGH|MEDIUM|LOW)"
- ✅ "treatment_info + disclaimer='Discuss with your physician' + flag_for_provider_review"
- ✅ "pathology_assessment + requires_pathologist_review=True + confidence_tier + uncertainty_regions[]"

**Enforcement**: Clinical outputs must have: review_flag + reviewer_type + urgency_level → Otherwise REJECT

---

### 29. PHI Must Have Healthcare-Grade Protection

**Principle**: PHI handling must exceed standard PII requirements (extends Invariant #26)

**Violation**: PHI treated as regular PII without healthcare-specific controls

**Examples**:
- ❌ "Store patient data encrypted" (insufficient)
- ❌ "Log medical queries" (audit risk)
- ❌ "Cache diagnostic results" (retention risk)
- ✅ "PHI: HIPAA_compliant + BAA_required + encryption(AES256_at_rest + TLS_in_transit) + access_log(immutable)"
- ✅ "Query logging: PHI_redacted + query_hash_only + no_patient_identifiers + audit_retention(7yr)"
- ✅ "Result caching: PHI_excluded OR encrypted_ephemeral(TTL_15min) + no_disk_persistence"

**Enforcement**: PHI must specify: HIPAA_controls + BAA_status + audit_mechanism + retention_compliance → Otherwise REJECT

---

### 30. Model Provenance Must Be Traceable

**Principle**: Clinical AI outputs must trace to specific model versions for reproducibility

**Violation**: Clinical outputs without model version, encoder version, or training data reference

**Examples**:
- ❌ "Return AI diagnosis"
- ❌ "Generate clinical summary"
- ❌ "Classify pathology image"
- ✅ "diagnosis + model_version='catalog.schema.model@v2.3' + encoder_version='biomedclip-v2' + training_cutoff='2025-06'"
- ✅ "summary + llm_version='dbrx-instruct-v1.2' + retrieval_index_version='pathvqa-2025Q4'"
- ✅ "classification + model_registry_uri + validation_dataset_hash + performance_metrics_at_deploy"

**Rationale**: FDA and clinical audit requirements demand reproducibility. "What model produced this output?" must be answerable.

**Enforcement**: Clinical outputs must include: model_version + encoder_version (if applicable) + traceability_uri → Otherwise REJECT

---

## Healthcare-Specific Sub-Invariants

### 30a. Confidence Reporting

- All clinical AI must report confidence scores
- Confidence thresholds must be clinically validated
- Low confidence must trigger explicit uncertainty messaging
- Confidence calibration must be documented

### 30b. Bias Monitoring

- Training data demographics must be documented
- Performance must be reported across demographic segments
- Known limitations by population must be disclosed
- Bias mitigation strategy required

### 30c. Regulatory Readiness

- FDA 510(k)/De Novo pathway must be identified if applicable
- Clinical validation study design must be specified
- Intended use statement required
- Contraindications must be documented

### 30d. Audit Trail

- All clinical decisions must be logged immutably
- User actions on AI outputs must be tracked
- Override/correction logging required
- Retention per regulatory requirement (typically 7+ years)

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 27 | Safety Must Be Enforced by Code | No prompt-only safety controls |
| 28 | Clinical Outputs Must Flag Human Review | Review flag + reviewer type present |
| 29 | PHI Must Have Healthcare-Grade Protection | HIPAA controls + BAA + audit |
| 30 | Model Provenance Must Be Traceable | model_version in all outputs |

---

*Domain: Healthcare AI*
*Invariants: 27-30 (plus sub-invariants)*
*Use with: Core invariants 1-10, Data Architecture 22-26*
*Applicable: HLS accounts (City of Hope, CHLA, Providence, etc.)*
