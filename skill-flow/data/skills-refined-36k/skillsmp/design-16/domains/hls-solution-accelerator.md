# HLS Solution Accelerator Domain Invariants

Extends: [[system-invariants]], [[healthcare-ai]]
Domain: Healthcare & Life Sciences demos, solution accelerators, SA enablement tools

---

## When to Use

Load this domain for:
- HLS customer demos (City of Hope, CHLA, Providence, etc.)
- Solution accelerators for healthcare
- SA enablement and POC tools
- Technical demos for clinical buyers
- Databricks HLS field engineering projects
- Pathology, genomics, clinical AI demos

---

## Research Sources

This domain synthesizes best practices from:

- **[Great Demo! by Peter Cohan](https://www.amazon.com/Great-Demo-Stunning-Software-Demonstrations/dp/059534559X)** — "Do the Last Thing First" methodology
- **[Databricks Solution Accelerators](https://www.databricks.com/solutions/accelerators)** — Enterprise patterns and medallion architecture
- **[JAMIA Recommendations for AI-CDS](https://academic.oup.com/jamia/article/31/11/2730/7776823)** — Clinical decision support best practices
- **[Databricks HLS Platform](https://www.databricks.com/solutions/industries/healthcare-and-life-sciences)** — Industry-specific patterns

---

## Domain Invariants (31-38)

### 31. Demo Must Show End Result First

**Principle**: Lead with the "Wow!" — show the valuable outcome before explaining how

**Source**: Peter Cohan's "Do the Last Thing First" — executives leave early, show best stuff first

**Violation**: Long setup, architecture slides, or build-up before showing value

**Examples**:
- ❌ "Let me walk you through the architecture first..."
- ❌ "Here's how we ingest data, then transform, then..."
- ❌ "First, let's look at the medallion layers"
- ✅ "Here's a pathology image. Ask any question. [shows answer with citations in 3 seconds]"
- ✅ "This is your patient readmission prediction — 87% confidence, here's why. Now let me show you how."
- ✅ "End result first: compliance score, issues found, remediation steps. Architecture comes after."

**Enforcement**: Demo scripts must start with: outcome_demo (30 sec) → discovery questions → deep dive. No architecture-first → REJECT

---

### 32. Solution Must Be Fork-Ready

**Principle**: Customer must be able to clone and run in their workspace within 30 minutes

**Source**: [Databricks Solution Accelerator patterns](https://github.com/databricks-industry-solutions) — "clone via Repos, Run-All"

**Violation**: Hard-coded paths, missing dependencies, undocumented setup

**Examples**:
- ❌ "Works on my workspace"
- ❌ "You'll need to manually configure these 12 settings"
- ❌ Absolute paths: `/Users/samuel.selvan/projects/...`
- ✅ "RUNME notebook: creates catalog, schema, and tables automatically"
- ✅ "Clone repo → attach cluster → Run All → working demo in 15 minutes"
- ✅ "Config in `config/dev.yml` — change 3 variables for your workspace"

**Enforcement**: Must include: RUNME.py + setup_time < 30min + config externalized + no hardcoded paths → REJECT

---

### 33. Data Must Be Substitutable

**Principle**: Demo works with sample data AND customer's own data with minimal changes

**Source**: Solution accelerator pattern — "can be extended with customer data"

**Violation**: Tightly coupled to specific dataset with no abstraction

**Examples**:
- ❌ "Only works with PathVQA dataset"
- ❌ "Schema must match exactly"
- ❌ "Requires our proprietary data format"
- ✅ "Works with PathVQA (included) OR bring your own images (BYOD guide in docs)"
- ✅ "Data contract: {image_path, diagnosis, tissue, qa_pairs} — map your schema to this"
- ✅ "Sample data for demo → customer data for POC → production data for deployment"

**Enforcement**: Must specify: sample_data_included + customer_data_guide + schema_mapping_docs → REJECT

---

### 34. Platform Capabilities Must Be Visible

**Principle**: Demo should naturally showcase Databricks differentiators

**Source**: SA enablement — demos should answer "why Databricks?"

**Violation**: Generic demo that could run on any platform

**Examples**:
- ❌ Generic Python script with no Databricks integration
- ❌ "This would work the same on AWS/GCP/Azure native"
- ❌ No Unity Catalog, no Model Serving, no Vector Search
- ✅ "Embeddings stored in Unity Catalog → lineage tracked → governed access"
- ✅ "Model Serving endpoint → scales to zero → pay per token"
- ✅ "Vector Search → managed index → automatic sync from Delta"
- ✅ "MLflow experiment tracking → compare retrieval strategies → pick winner"

**Platform Features to Showcase**:
| Feature | How to Showcase |
|---------|-----------------|
| Unity Catalog | Data lineage, governed access, tagging |
| Model Serving | Endpoint deployment, scaling, cost |
| Vector Search | Managed index, Delta sync |
| MLflow | Experiment tracking, model registry |
| Delta Lake | Time travel, ACID, schema evolution |
| Workflows | Orchestration, scheduling |

**Enforcement**: Demo must showcase ≥3 Databricks differentiators with explicit callout → REJECT

---

### 35. Discovery Must Precede Deep Dive

**Principle**: Ask questions before showing how it works

**Source**: Peter Cohan — "Insufficient discovery is the single largest reason demos fail"

**Violation**: Launching into technical details without understanding customer context

**Examples**:
- ❌ "Let me show you all the features..."
- ❌ 45-minute monologue through every capability
- ❌ "Here's our architecture diagram [30 slides]"
- ✅ "Before I dive in — what's your current approach to pathology image search?"
- ✅ "What does 'good enough' retrieval accuracy look like for your use case?"
- ✅ "Who would use this day-to-day? Pathologists? Researchers? Both?"
- ✅ "What's your timeline for a POC? Are there compliance gates?"

**Discovery Questions for HLS**:
1. Current state: "How do you handle X today?"
2. Pain: "What's broken or frustrating about that?"
3. Impact: "What does this cost you (time, money, risk)?"
4. Success: "What would 'good' look like?"
5. Timeline: "When do you need this by?"
6. Stakeholders: "Who else needs to see this?"

**Enforcement**: Demo script must include: discovery_questions (≥3) before deep_dive section → REJECT

---

### 36. Compliance Readiness Must Be Demonstrable

**Principle**: Show governance/compliance during demo, not as afterthought

**Source**: [JAMIA recommendations](https://academic.oup.com/jamia/article/31/11/2730/7776823) — "make system enterprise-level by involving security, legal"

**Violation**: "We can add compliance later" or no compliance story

**Examples**:
- ❌ "Security is handled separately"
- ❌ "We'll figure out HIPAA compliance in production"
- ❌ No audit trail, no access controls, no data governance
- ✅ "Tab 4 shows live compliance status — NIST/HITRUST aligned"
- ✅ "Unity Catalog tags PHI columns → access controlled → audit logged"
- ✅ "Every AI output includes model version for FDA traceability"
- ✅ "Human-in-the-loop: malignancy findings require pathologist sign-off"

**Compliance Features to Demo**:
| Requirement | How to Show |
|-------------|-------------|
| PHI Protection | UC tags, encryption, access controls |
| Audit Trail | System tables, query history |
| Model Governance | Registry, versioning, lineage |
| Human Oversight | Review flags, escalation paths |
| Regulatory Alignment | NIST/HITRUST/FDA mapping |

**Enforcement**: Demo must include live compliance check OR governance walkthrough → REJECT

---

### 37. Setup Must Be Self-Documenting

**Principle**: Customer can set up without SA hand-holding

**Source**: Solution accelerator pattern — README + RUNME + inline comments

**Violation**: Requires live support to get running

**Examples**:
- ❌ "Call me when you get stuck"
- ❌ "I'll send you the missing config file"
- ❌ No README, no comments, no error messages
- ✅ "README: Prerequisites → Quick Start → Configuration → Troubleshooting"
- ✅ "RUNME.py: checks prerequisites, creates resources, validates setup"
- ✅ "Error: 'DATABRICKS_TOKEN not set' → See README section 2.1"
- ✅ "Setup wizard: prompts for catalog name, validates permissions, creates schema"

**Required Documentation**:
| Doc | Purpose |
|-----|---------|
| README.md | Overview, prerequisites, quick start |
| RUNME.py | Automated setup with validation |
| config/README.md | All configuration options explained |
| TROUBLESHOOTING.md | Common errors and fixes |
| docs/ARCHITECTURE.md | System design for technical buyers |

**Enforcement**: Must include: README + RUNME + config_docs + troubleshooting → REJECT

---

### 38. Value Must Be Quantifiable

**Principle**: Demo should connect to business metrics the buyer cares about

**Source**: Great Demo! — "calculate deltas (build a business case)"

**Violation**: Pure technical demo with no business value articulation

**Examples**:
- ❌ "Look how fast this is!"
- ❌ "Our architecture is really clean"
- ❌ Technical metrics only (latency, accuracy) without business translation
- ✅ "92% retrieval accuracy → pathologists find relevant cases 3x faster"
- ✅ "Automated compliance check → saves 40 hours/quarter of manual review"
- ✅ "Real-time malignancy flagging → reduces diagnostic delay from days to minutes"
- ✅ "Cost calculator: $X/query at your volume = $Y/month vs current $Z"

**Value Metrics for HLS**:
| Technical | Business Translation |
|-----------|---------------------|
| Retrieval accuracy | Faster case finding, fewer missed diagnoses |
| Response latency | Clinician time saved per query |
| Compliance automation | Audit prep hours reduced |
| Model accuracy | Diagnostic confidence, fewer re-reads |

**Enforcement**: Demo must include ≥2 business value statements with quantification → REJECT

---

## HLS-Specific Sub-Invariants

### 38a. Clinical Workflow Alignment

- Demo must show integration point with clinical workflow
- "Where does this fit in the pathologist's day?"
- Not just standalone tool — connected to existing systems

### 38b. Stakeholder Mapping

- Know your audience: Pathologist vs CIO vs CISO vs CFO
- Different demo paths for different stakeholders
- Technical depth adjustable based on audience

### 38c. Competitive Differentiation

- Be ready for "How is this different from X?"
- Know competitor limitations (Snowflake, AWS, Google)
- Lead with differentiation, not feature parity

### 38d. POC Transition Path

- Clear path from demo → POC → production
- "Here's what a 2-week POC would look like"
- Success criteria defined upfront

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 31 | Demo Must Show End Result First | Outcome in first 30 seconds |
| 32 | Solution Must Be Fork-Ready | Clone → Run → Working in 30 min |
| 33 | Data Must Be Substitutable | Sample data + BYOD guide |
| 34 | Platform Capabilities Must Be Visible | ≥3 Databricks features called out |
| 35 | Discovery Must Precede Deep Dive | ≥3 discovery questions before features |
| 36 | Compliance Readiness Must Be Demonstrable | Live compliance check in demo |
| 37 | Setup Must Be Self-Documenting | README + RUNME + troubleshooting |
| 38 | Value Must Be Quantifiable | ≥2 business metrics with numbers |

---

## Demo Flow Template

Based on Great Demo! + HLS best practices:

```
1. OPENING (30 sec)
   - "Here's what you'll be able to do" [show end result]
   - Generate "Wow!" moment

2. DISCOVERY (5-10 min)
   - Current state questions
   - Pain points
   - Success criteria
   - Stakeholders and timeline

3. CONTEXT BRIDGE (1 min)
   - "Based on what you told me, let me show you..."
   - Connect their pain to your solution

4. CAPABILITY DEEP DIVE (15-20 min)
   - Features that address their specific pain
   - Platform differentiators (UC, Model Serving, VS)
   - Compliance/governance story

5. VALUE SUMMARY (5 min)
   - Business metrics recap
   - "This means X hours saved, Y% improvement"
   - ROI/cost calculator if available

6. NEXT STEPS (5 min)
   - POC proposal
   - Success criteria
   - Timeline and stakeholders
```

---

*Domain: HLS Solution Accelerator*
*Invariants: 31-38 (plus sub-invariants)*
*Use with: Core invariants 1-10, Healthcare AI 27-30*
*Applicable: Databricks SA work with healthcare providers*

---

## Sources

- [Great Demo! by Peter Cohan](https://www.amazon.com/Great-Demo-Stunning-Software-Demonstrations/dp/059534559X)
- [Databricks Solution Accelerators](https://www.databricks.com/solutions/accelerators)
- [Databricks HLS Industry Solutions](https://github.com/databricks-industry-solutions)
- [JAMIA AI-CDS Recommendations](https://academic.oup.com/jamia/article/31/11/2730/7776823)
- [Databricks HLS Platform](https://www.databricks.com/solutions/industries/healthcare-and-life-sciences)
