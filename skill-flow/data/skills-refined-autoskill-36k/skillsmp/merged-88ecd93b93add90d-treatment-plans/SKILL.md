---
name: treatment-plans
description: Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Supports general medical treatment, rehabilitation therapy, mental health care, chronic disease management, perioperative care, and pain management. Includes SMART goal frameworks, evidence-based interventions with minimal text citations, regulatory compliance (HIPAA), and professional formatting. Prioritizes brevity and clinical actionability.
---

# Treatment Plan Writing

## Overview

Treatment plan writing is the systematic documentation of clinical care strategies designed to address patient health conditions through evidence-based interventions, measurable goals, and structured follow-up. This skill provides comprehensive LaTeX templates and validation tools for creating **concise, focused** treatment plans (3-4 pages standard) across all medical specialties with full regulatory compliance.

**Critical Principles:**
1. **CONCISE & ACTIONABLE**: Treatment plans default to 3-4 pages maximum, focusing only on clinically essential information that impacts care decisions.
2. **Patient-Centered**: Plans must be evidence-based, measurable, and compliant with healthcare regulations (HIPAA, documentation standards).
3. **Minimal Citations**: Use brief in-text citations only when needed to support clinical recommendations; avoid extensive bibliographies.

Every treatment plan should include clear goals, specific interventions, defined timelines, monitoring parameters, and expected outcomes that align with patient preferences and current clinical guidelines - all presented as efficiently as possible.

## When to Use This Skill

This skill should be used when:
- Creating individualized treatment plans for patient care.
- Documenting therapeutic interventions for chronic disease management.
- Developing rehabilitation programs (physical therapy, occupational therapy, cardiac rehab).
- Writing mental health and psychiatric treatment plans.
- Planning perioperative and surgical care pathways.
- Establishing pain management protocols.
- Setting patient-centered goals using SMART criteria.
- Coordinating multidisciplinary care across specialties.
- Ensuring regulatory compliance in treatment documentation.
- Generating professional treatment plans for medical records.

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every treatment plan MUST include at least 1 AI-generated figure using the scientific-schematics skill.**

This is not optional. Treatment plans benefit greatly from visual elements. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., treatment pathway flowchart, care coordination diagram, or therapy timeline).
2. For complex plans: include decision algorithm flowchart.
3. For rehabilitation plans: include milestone progression diagram.

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Simply describe your desired diagram in natural language.
- Nano Banana Pro will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting.
- Review and refine through multiple iterations.
- Ensure accessibility (colorblind-friendly, high contrast).
- Save outputs in the figures/ directory.

**When to add schematics:**
- Treatment pathway flowcharts.
- Care coordination diagrams.
- Therapy progression timelines.
- Multidisciplinary team interaction diagrams.
- Medication management flowcharts.
- Rehabilitation protocol visualizations.
- Clinical decision algorithm diagrams.
- Any complex concept that benefits from visualization.

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Document Format and Best Practices

### Document Length Options

Treatment plans come in three format options based on clinical complexity and use case:

#### Option 1: One-Page Treatment Plan (PREFERRED for most cases)

**When to use**: Straightforward clinical scenarios, standard protocols, busy clinical settings.

**Format**: Single page containing all essential treatment information in scannable sections.
- No table of contents needed.
- No extensive narratives.
- Focused on actionable items only.
- Similar to precision oncology reports or treatment recommendation cards.

**Required sections** (all on one page):
1. **Header Box**: Patient info, diagnosis, date, molecular/risk profile if applicable.
2. **Treatment Regimen**: Numbered list of specific interventions.
3. **Supportive Care**: Brief bullet points.
4. **Rationale**: 1-2 sentence justification (optional for standard protocols).
5. **Monitoring**: Key parameters and frequency.
6. **Evidence Level**: Guideline reference or evidence grade (e.g., "Level 1, FDA approved").
7. **Expected Outcome**: Timeline and success metrics.

**Design principles**:
- Use small boxes/tables for organization (like the clinical treatment recommendation card format).
- Eliminate all non-essential text.
- Use abbreviations familiar to clinicians.
- Dense information layout - maximize information per square inch.
- Think "quick reference card" not "comprehensive documentation".

**Example structure**:
```latex
[Patient ID/Diagnosis Box at top]

TARGET PATIENT POPULATION
  Number of patients, demographics, key features.

PRIMARY TREATMENT REGIMEN
  • Medication 1: dose, frequency, duration.
  • Procedure: specific details.
  • Monitoring: what and when.

SUPPORTIVE CARE
  • Key supportive medications.

RATIONALE
  Brief clinical justification.

MOLECULAR TARGETS / RISK FACTORS
  Relevant biomarkers or risk stratification.

EVIDENCE LEVEL
  Guideline reference, trial data.

MONITORING REQUIREMENTS
  Key labs/vitals, frequency.

EXPECTED CLINICAL BENEFIT
  Primary endpoint, timeline.
```

#### Option 2: Standard 3-4 Page Format

**When to use**: Moderate complexity, need for patient education materials, multidisciplinary coordination.

Uses the Foundation Medicine first-page summary model with 2-3 additional pages of details.

#### Option 3: Extended 5-6 Page Format

**When to use**: Complex comorbidities, research protocols, extensive safety monitoring required.

### First Page Summary (Foundation Medicine Model)

**CRITICAL REQUIREMENT: All treatment plans MUST have a complete executive summary on the first page ONLY, before any table of contents or detailed sections.**

Following the Foundation Medicine model for precision medicine reporting and clinical summary documents, treatment plans begin with a one-page executive summary that provides immediate access to key actionable information. This entire summary must fit on the first page.

**Required First Page Structure (in order):**
1. **Title and Subtitle**
   - Main title: Treatment plan type (e.g., "Comprehensive Treatment Plan").
   - Subtitle: Specific condition or focus (e.g., "Type 2 Diabetes Mellitus - Young Adult Patient").

2. **Report Information Box** (using `\begin{infobox}` or `\begin{patientinfo}`)
   - Report type/document purpose.
   - Date of plan creation.
   - Patient demographics (age, sex, de-identified).
   - Primary diagnosis with ICD-10 code.
   - Report author/clinic (if applicable).
   - Analysis approach or framework used.

3. **Key Findings or Treatment Highlights** (2-4 colored boxes using appropriate box types)
   - **Primary Treatment Goals** (using `\begin{goalbox}`)
     - 2-3 SMART goals in bullet format.
   - **Main Interventions** (using `\begin{keybox}` or `\begin{infobox}`)
     - 2-3 key interventions (pharmacological, non-pharmacological, monitoring).
   - **Critical Decision Points** (using `\begin{warningbox}` if urgent)
     - Important monitoring thresholds or safety considerations.
   - **Timeline Overview** (using `\begin{infobox}`)
     - Brief treatment duration/phases.
     - Key milestone dates.

**Visual Format Requirements:**
- Use `\thispagestyle{empty}` to remove page numbers from first page.
- All content must fit on page 1 (before `\newpage`).
- Use colored boxes (tcolorbox package) with different colors for different information types.
- Boxes should be visually prominent and easy to scan.
- Use concise, bullet-point format.
- Table of contents (if included) starts on page 2.
- Detailed sections start on page 3.

**Example First Page Structure:**
```latex
\maketitle
\thispagestyle{empty}

% Report Information Box
\begin{patientinfo}
  Report Type, Date, Patient Info, Diagnosis, etc.
\end{patientinfo}

% Key Finding #1: Treatment Goals
\begin{goalbox}[Primary Treatment Goals]
  • Goal 1
  • Goal 2
  • Goal 3
\end{goalbox}

% Key Finding #2: Main Interventions
\begin{keybox}[Core Interventions]
  • Intervention 1
  • Intervention 2
  • Intervention 3
\end{keybox}

% Key Finding #3: Critical Monitoring (if applicable)
\begin{warningbox}[Critical Decision Points]
  • Decision point 1
  • Decision point 2
\end{warningbox}

\newpage
\tableofcontents  % TOC on page 2
\newpage  % Detailed content starts page 3
```

### Concise Documentation

**CRITICAL: Treatment plans MUST prioritize brevity and clinical relevance. Default to 3-4 pages maximum unless clinical complexity absolutely demands more detail.**

Treatment plans should prioritize **clarity and actionability** over exhaustive detail:
- **Focused**: Include only clinically essential information that impacts care decisions.
- **Actionable**: Emphasize what needs to be done, when, and why.
- **Efficient**: Facilitate quick decision-making without sacrificing clinical quality.
- **Target length options**:
  - **1-page format** (preferred for straightforward cases): Quick-reference card with all essential information.
  - **3-4 pages standard**: Standard format with first-page summary + supporting details.
  - **5-6 pages** (rare): Only for highly complex cases with multiple comorbidities or multidisciplinary interventions.

**Streamlining Guidelines:**
- **First Page Summary**: Use individual colored boxes to consolidate key information (goals, interventions, decision points) - this alone can often convey the essential treatment plan.
- **Eliminate Redundancy**: If information is in the first-page summary, don't repeat it verbatim in detailed sections.
- **Patient Education section**: 3-5 key bullet points on critical topics and warning signs only.
- **Risk Mitigation section**: Highlight only critical medication safety concerns and emergency actions (not exhaustive lists).
- **Expected Outcomes section**: 2-3 concise statements on anticipated responses and timelines.
- **Interventions**: Focus on primary interventions; secondary/supportive measures in brief bullet format.
- **Use tables and bullet points** extensively for efficient presentation.
- **Avoid narrative prose** where structured lists suffice.
- **Combine related sections** when appropriate to reduce page count.

### Quality Over Quantity

The goal is professional, clinically complete documentation that respects clinicians' time while ensuring comprehensive patient care. Every section should add value; remove or condense sections that don't directly inform treatment decisions.

### Citations and Evidence Support

**Use minimal, targeted citations to support clinical recommendations:**
- **Text Citations Preferred**: Use brief in-text citations (Author Year) or simple references rather than extensive bibliographies unless specifically requested.
- **When to Cite**:
  - Clinical practice guideline recommendations (e.g., "per ADA 2024 guidelines").
  - Specific medication dosing or protocols (e.g., "ACC/AHA recommendations").
  - Novel or controversial interventions requiring evidence support.
  - Risk stratification tools or validated assessment scales.
- **When NOT to Cite**:
  - Standard-of-care interventions widely accepted in the field.
  - Basic medical facts and routine clinical practices.
  - General patient education content.
- **Citation Format**: 
  - Inline: "Initiate metformin as first-line therapy (ADA Standards of Care 2024)".
  - Minimal: "Treatment follows ACC/AHA heart failure guidelines".
  - Avoid formal numbered references and extensive bibliography sections unless document is for academic/research purposes.
- **Keep it Brief**: A 3-4 page treatment plan should have 0-3 citations maximum, only where essential for clinical credibility or novel recommendations.

## Core Capabilities

### 1. General Medical Treatment Plans

General medical treatment plans address common chronic conditions and acute medical issues requiring structured therapeutic interventions.

#### Standard Components

**Patient Information (De-identified)**
- Demographics (age, sex, relevant medical background).
- Active medical conditions and comorbidities.
- Current medications and allergies.
- Relevant social and family history.
- Functional status and baseline assessments.
- **HIPAA Compliance**: Remove all 18 identifiers per Safe Harbor method.

**Diagnosis and Assessment Summary**
- Primary diagnosis with ICD-10 code.
- Secondary diagnoses and comorbidities.
- Severity classification and staging.
- Functional limitations and quality of life impact.
- Risk stratification (e.g., cardiovascular risk, fall risk).
- Prognostic indicators.

**Treatment Goals (SMART Format)**

Short-term goals (1-3 months):
- **Specific**: Clearly defined outcome (e.g., "Reduce HbA1c to <7%").
- **Measurable**: Quantifiable metrics (e.g., "Decrease systolic BP by 10 mmHg").
- **Achievable**: Realistic given patient capabilities.
- **Relevant**: Aligned with patient priorities and values.
- **Time-bound**: Specific timeframe (e.g., "within 8 weeks").

Long-term goals (6-12 months):
- Disease control or remission targets.
- Functional improvement objectives.
- Quality of life enhancement.
- Prevention of complications.
- Maintenance of independence.

**Interventions**

_Pharmacological_:
- Medications with specific dosages, routes, frequencies.
- Titration schedules and target doses.
- Drug-drug interaction considerations.
- Monitoring for adverse effects.
- Medication reconciliation.

_Non-pharmacological_:
- Lifestyle modifications (diet, exercise, smoking cessation).
- Behavioral interventions.
- Patient education and self-management.
- Monitoring and self-tracking (glucose, blood pressure, weight).
- Assistive devices or adaptive equipment.

_Procedural_:
- Planned procedures or interventions.
- Referrals to specialists.
- Diagnostic testing schedule.
- Preventive care (vaccinations, screenings).

**Timeline and Schedule**
- Treatment phases with specific timeframes.
- Appointment frequency (weekly, monthly, quarterly).
- Milestone assessments and goal evaluations.
- Medication adjustments schedule.
- Expected duration of treatment.

**Monitoring Parameters**
- Clinical outcomes to track (vital signs, lab values, symptoms).
- Assessment tools and scales (e.g., PHQ-9, pain scales).
- Frequency of monitoring.
- Thresholds for intervention or escalation.
- Patient-reported outcomes.

**Expected Outcomes**
- Primary outcome measures.
- Success criteria and benchmarks.
- Expected timeline for improvement.
- Criteria for treatment modification.
- Long-term prognosis.

**Follow-up Plan**
- Scheduled appointments and reassessments.
- Communication plan (phone calls, secure messaging).
- Emergency contact procedures.
- Criteria for urgent evaluation.
- Transition or discharge planning.

**Patient Education**
- Understanding of condition and treatment rationale.
- Self-management skills training.
- Medication administration and adherence.
- Warning signs and when to seek help.
- Resources and support services.

**Risk Mitigation**
- Potential adverse effects and management.
- Drug interactions and contraindications.
- Fall prevention, infection prevention.
- Emergency action plans.
- Safety monitoring.

#### Common Applications

- Diabetes mellitus management.
- Hypertension control.
- Heart failure treatment.
- COPD management.
- Asthma care plans.
- Hyperlipidemia treatment.
- Osteoarthritis management.
- Chronic kidney disease.

### 2. Rehabilitation Treatment Plans

Rehabilitation plans focus on restoring function, improving mobility, and enhancing quality of life through structured therapeutic programs.

#### Core Components

**Functional Assessment**
- Baseline functional status (ADLs, IADLs).
- Range of motion, strength, balance, endurance.
- Gait analysis and mobility assessment.
- Standardized measures (FIM, Barthel Index, Berg Balance Scale).
- Environmental assessment (home safety, accessibility).

**Rehabilitation Goals**

_Impairment-level goals_:
- Improve shoulder flexion to 140 degrees.
- Increase quadriceps strength by 2/5 MMT grades.
- Enhance balance (Berg Score >45/56).

_Activity-level goals_:
- Independent ambulation 150 feet with assistive device.
- Climb 12 stairs with handrail supervision.
- Transfer bed-to-chair independently.

_Participation-level goals_:
- Return to work with modifications.
- Resume recreational activities.