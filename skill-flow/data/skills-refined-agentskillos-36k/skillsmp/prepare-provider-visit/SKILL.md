---
name: prepare-provider-visit
description: "Intelligently orchestrate provider visit documentation by gathering relevant health data and generating coherent provider-appropriate narratives. Use when user asks to 'prepare for doctor visit', 'generate provider summary', 'create medical summary', or needs documentation for healthcare appointments."
---

# Prepare Provider Visit

Generate comprehensive, coherent provider documentation by intelligently selecting and presenting relevant health data based on visit type and context.

## When to Use This Skill

Trigger when user asks:
- "Prepare a summary for my doctor"
- "Generate documentation for my appointment"
- "Create a provider visit summary"
- "I have a doctor's appointment, what should I bring?"
- "Summarize my health for my specialist"

## Workflow

### Step 1: Gather Context (Minimal Questions)

Ask the user for essential context:

1. **Visit type**: Annual physical / Specialist consult / Follow-up / Urgent care
2. **Specific concerns** (optional): Any particular issues to highlight?
3. **For follow-ups only**: Date of last visit (to determine "since last visit" timeframe)

Use the AskUserQuestion tool with clear options for visit type.

### Step 2: Determine Content Strategy (Smart Defaults)

Based on visit type, automatically determine what to include:

**Annual Physical**:
- Time period: Last 12 months
- Include: Current medications, recent health events, abnormal labs, active conditions
- Include genetics: Only if `genetics_23andme_path` is configured AND relevant findings exist
- Tone: Comprehensive overview

**Specialist Consult**:
- Time period: Last 6 months (focus on specialty-relevant recent changes)
- Include: Medications (specialty-relevant), recent events (related to specialty), targeted labs
- Include genetics: Only if relevant to specialty (e.g., cardiology → APOE, Factor V)
- Tone: Focused on specialist's domain

**Follow-up Visit**:
- Time period: Since last visit date (user provides)
- Include: Changes since last visit, monitored markers, new events, medication adjustments
- Include genetics: Only if new interpretation or relevant to follow-up reason
- Tone: Delta-focused (what changed)

**Urgent Care**:
- Time period: Last 3-6 months (recent context only)
- Include: Chief complaint details, recent relevant events, pertinent labs
- Include genetics: Rarely (only if directly relevant to acute issue)
- Tone: Focused on presenting problem

### Step 3: Gather Data

For each content area, gather data naturally (NOT by invoking deleted skills):

**Current Medications & Supplements**:
```bash
# Preferred: Get from current.yaml (source of truth)
grep -A 100 "^medications:" "{health_log_path}/current.yaml" | grep -B 100 -m 1 "^[a-z]" | head -n -1
grep -A 100 "^supplements:" "{health_log_path}/current.yaml" | grep -B 100 -m 1 "^[a-z]" | head -n -1

# Alternative: Extract from history.csv for timeline
grep -E ",medication,|,supplement," "{health_log_path}/history.csv" | \
  awk -F',' '{print $1","$2","$3","$4","$5","$6}' | \
  tail -50  # Recent 50 entries
```

When using current.yaml, the status is already determined (items listed are active).
For history.csv analysis, apply status determination logic from `.claude/skills/health-agent/references/status-keywords.md`.

**Recent Health Events**:
```bash
# Events in timeframe from history.csv
awk -F',' -v start="YYYY-MM-DD" 'NR==1 || $1 >= start' "{health_log_path}/history.csv"
```

Group by Type column and EntityID for coherent presentation.

**Abnormal Labs**:
```bash
# Out-of-range labs in timeframe
awk -F',' -v start="YYYY-MM-DD" 'NR==1 || ($1 >= start && ($5 > $7 || $5 < $6))' "{labs_path}/all.csv"
```

Use lab_specs.json (via helpers in `.claude/skills/health-agent/references/lab-specs-helpers.sh`) for canonical names if available.

**Active Conditions**:
```bash
# Preferred: Get from current.yaml (source of truth)
grep -A 100 "^conditions:" "{health_log_path}/current.yaml" | grep -B 100 -m 1 "^[a-z]" | head -n -1

# Alternative: Extract from history.csv for timeline
grep ",condition," "{health_log_path}/history.csv" | \
  awk -F',' '{print $1","$2","$3","$4","$5","$6}'
```

When using current.yaml, items are definitively active. For history.csv, apply status keywords to determine active vs resolved.

**Genetics** (ONLY if `genetics_23andme_path` is configured):

For specialist visits or when relevant, use `genetics-snp-lookup` skill to check:
- Pharmacogenomics (if new medications discussed)
- Relevant health risks (e.g., cardiology → APOE, Factor V)

**Do NOT include comprehensive genetics reports** unless specifically relevant to visit purpose.

### Step 4: Generate Coherent Narrative

**CRITICAL**: Generate a NARRATIVE, not concatenated sections.

Use this structure:

```markdown
---
document_type: provider_visit_summary
visit_type: {annual|specialist|follow_up|urgent}
generated: {YYYY-MM-DD}
profile: {profile_name}
timeframe: {description of time period covered}
---

# Provider Visit Summary
**Patient**: {profile_name}
**Visit Type**: {visit_type}
**Generated**: {YYYY-MM-DD}
**Timeframe**: {description}

## Visit Context

{2-3 sentences describing reason for visit, any specific concerns, and overall health status}

## Current Medications & Supplements

{Narrative intro: "Currently taking the following medications:"}

| Medication/Supplement | Dosage/Frequency | Started | Status |
|----------------------|------------------|---------|--------|
| ... | ... | ... | Active |

{Brief commentary on recent changes, if any}

## Recent Health Events

{Narrative intro describing event categories and any patterns}

**[Category Name]** ({count} events):
- {Date}: {Event} - {Brief detail}
- {Date}: {Event} - {Brief detail}

{Narrative synthesis: "Notable patterns include..." or "No concerning patterns identified"}

## Laboratory Results

{Narrative intro describing lab monitoring and any trends}

**Abnormal Values**:

| Date | Test | Value | Reference Range | Status |
|------|------|-------|-----------------|--------|
| ... | ... | ... | ... | High/Low |

{Brief interpretation: "HbA1c trending upward, may warrant discussion of medication adjustment"}

## Active Medical Conditions

{If none: "No active chronic conditions documented in health log."}
{If present: Bulleted list with onset dates and current status}

- **{Condition}** (since {date}): {Brief status note}

{FOR SPECIALIST/RELEVANT VISITS ONLY}
## Relevant Genetic Findings

{ONLY include if genetics configured AND directly relevant to visit}

{Brief narrative on findings relevant to visit purpose}

## Summary & Considerations

{2-4 bullet points synthesizing key discussion points for provider:}
- {Synthesis point 1}
- {Synthesis point 2}
- {Potential discussion topic}

---
*This summary was generated by health-agent to support clinical decision-making. All data is patient-reported or extracted from personal health records. Please verify critical information.*
```

### Step 5: Save Output

Save the generated document to:
```
.output/{profile}/provider-visit-{visit_type}-{YYYY-MM-DD}.md
```

Use the `Write` tool (NOT Bash heredocs - they fail in sandbox mode).

Before writing, ensure directory exists:
```bash
mkdir -p .output/{profile}
```

### Step 6: Confirm Completion

Tell the user:
```
Provider visit summary generated and saved to:
.output/{profile}/provider-visit-{visit_type}-{YYYY-MM-DD}.md

The summary includes:
- {List of sections included}
- Covers timeframe: {timeframe description}

You can review, edit, or print this document for your appointment.
```

## Key Principles

1. **Smart Defaults**: Visit type determines everything - don't over-question the user
2. **Coherent Narrative**: Write connected prose, not isolated sections
3. **Provider-Appropriate Tone**: Professional medical documentation style
4. **Selective Genetics**: Only include if configured AND relevant - avoid overwhelming providers
5. **Data Citations**: Include dates and source references for verifiability
6. **Actionable Synthesis**: End with discussion points, not just data dumps

---

## Narrative Generation Strategy

### The Problem: Section Concatenation

**Bad approach** (avoid this):
```
## Medications
Patient takes lisinopril 10mg.

## Labs
HbA1c was 6.8% on 2026-01-15.

## Events
Patient had a cold in December.
```

This reads like a form, not a document. It doesn't help the provider understand the patient's health story.

### The Solution: Connected Narrative

**Good approach** (do this):
```
## Visit Context
Mr. Smith is a 52-year-old male presenting for routine follow-up of his well-controlled
hypertension. Since his last visit, he reports good medication adherence with stable
blood pressure readings at home, though he experienced a brief upper respiratory
infection in December that resolved without complications.

## Current Medications
He continues on lisinopril 10mg daily, which he tolerates well with no reported side
effects. No medication changes have been made since his last visit.

## Laboratory Results
Recent labs from January 15th show an HbA1c of 6.8%, which represents a slight increase
from his previous value of 6.5%. While still within the prediabetic range, this upward
trend may warrant discussion of lifestyle modifications.
```

### Narrative Building Blocks

#### Opening Sentences by Visit Type

**Annual Physical**:
- "{Name} is a {age}-year-old {gender} presenting for routine annual examination."
- "This summary covers the past 12 months of health activity for {Name}."
- "{Name} returns for their annual physical with [no major concerns / several items to discuss]."

**Specialist Consult**:
- "{Name} is referred to {specialty} for evaluation of {chief complaint}."
- "This summary is prepared for {Name}'s first visit with {specialty} regarding {condition}."
- "{Name} seeks specialist consultation for {symptom/condition} that has been present for {duration}."

**Follow-up Visit**:
- "{Name} returns for follow-up of {condition(s)} since their visit on {last visit date}."
- "This visit follows up on {condition} discussed on {date}. Since then, {brief status update}."
- "{Name} is here for {X}-month follow-up of {condition}."

**Urgent Care**:
- "{Name} presents with acute onset of {chief complaint} beginning {timeframe}."
- "{Name} seeks urgent evaluation for {symptom} that started {when}."
- "This summary supports urgent evaluation of {chief complaint} in the context of {relevant history}."

#### Transition Phrases Between Sections

| From → To | Transition Options |
|-----------|-------------------|
| Context → Medications | "Currently, {patient} is taking...", "Their medication regimen includes...", "Active medications at this time:" |
| Medications → Labs | "Recent laboratory studies show...", "Labs obtained on {date} reveal...", "Supporting this assessment, recent labs indicate..." |
| Labs → Events | "Over the past {timeframe}, the patient experienced...", "Health events during this period include...", "Notable occurrences since last visit:" |
| Events → Conditions | "These events occur in the context of...", "Underlying conditions that may be relevant:", "The patient's active problem list includes:" |
| Conditions → Genetics | "Relevant genetic findings include...", "Genetic testing has revealed...", "From a pharmacogenomic perspective:" |
| Any → Summary | "In summary,", "Key discussion points for this visit:", "The following topics warrant discussion:" |

#### Connective Words for Flow

**Addition**: additionally, furthermore, moreover, also, in addition
**Contrast**: however, nevertheless, although, despite, while
**Cause/Effect**: consequently, therefore, as a result, thus, leading to
**Temporal**: subsequently, since then, following this, meanwhile, recently
**Emphasis**: notably, importantly, significantly, particularly, especially
**Clarification**: specifically, in particular, that is, namely, for instance

### Tone Guidelines by Visit Type

| Visit Type | Tone | Word Choice | Detail Level |
|------------|------|-------------|--------------|
| **Annual** | Comprehensive, measured | Neutral medical terminology | High - cover all systems |
| **Specialist** | Focused, technical | Domain-specific terms welcome | High for relevant area, low elsewhere |
| **Follow-up** | Comparative, progress-oriented | Change-focused language ("improved", "stable", "worsening") | Medium - emphasize deltas |
| **Urgent** | Concise, action-oriented | Direct, avoid hedging | Minimal - only pertinent info |

### Tone Examples

**Annual Physical Tone**:
> "Blood pressure has remained well-controlled throughout the year, with home readings averaging 125/78. Lipid panel from June showed LDL of 118 mg/dL, within target range for his cardiovascular risk profile. Weight has been stable at 185 lbs."

**Specialist Consult Tone**:
> "Referred for evaluation of persistent microcytic anemia (Hgb 11.2 g/dL, MCV 72 fL) despite 3 months of oral iron supplementation. Iron studies show ferritin 15 ng/mL with TIBC elevated at 450 μg/dL, suggesting ongoing iron deficiency. GI workup has not yet been performed."

**Follow-up Tone**:
> "Since starting metformin 500mg BID on October 15th, HbA1c has decreased from 7.2% to 6.8% - a 0.4% improvement over 3 months. Patient reports mild GI side effects initially that have since resolved. Fasting glucose logs show improved morning values (avg 118 mg/dL vs prior 145 mg/dL)."

**Urgent Care Tone**:
> "72-year-old female with atrial fibrillation on warfarin presenting with 2 days of melena and lightheadedness. Last INR 3.8 (above target range). No recent NSAID use. Hemoglobin today 9.2 g/dL, down from baseline 12.5 g/dL."

### Example Generated Output Structure

Below is a complete example of a well-structured provider visit summary:

```markdown
---
document_type: provider_visit_summary
visit_type: follow_up
generated: 2026-01-23
profile: john_smith
timeframe: Since last visit (2025-10-15)
---

# Provider Visit Summary
**Patient**: John Smith
**Visit Type**: Follow-up
**Generated**: January 23, 2026
**Timeframe**: October 15, 2025 - Present (3 months)

## Visit Context

Mr. Smith is a 54-year-old male returning for 3-month follow-up of newly diagnosed
type 2 diabetes and hypertension. Since initiating therapy in October, he reports
good adherence to both medications and has made dietary modifications as recommended.
His primary concerns today are occasional morning headaches and questions about
exercise intensity.

## Current Medications

His current regimen includes metformin 500mg twice daily for glycemic control and
lisinopril 10mg daily for blood pressure management. He tolerates both medications
well, though he notes mild gastrointestinal discomfort with metformin that improved
after taking it with meals. He has discontinued his previous as-needed ibuprofen use
per prior guidance and now uses acetaminophen occasionally for headaches.

| Medication | Dose | Frequency | Started | Status |
|------------|------|-----------|---------|--------|
| Metformin | 500mg | BID with meals | 2025-10-15 | Active |
| Lisinopril | 10mg | Daily | 2025-10-15 | Active |
| Acetaminophen | 500mg | PRN | Long-standing | Active (PRN) |

## Recent Health Events

Over the past three months, Mr. Smith has had no acute illnesses or emergency visits.
He reports the following health-related events:

**Symptoms (2 events)**:
- 2025-12-01: Morning headaches, mild intensity, approximately 3x/week
- 2026-01-10: Occasional dizziness when standing quickly

**Lifestyle changes (3 events)**:
- 2025-10-20: Started walking program (30 min, 4x/week)
- 2025-11-15: Reduced carbohydrate intake per dietitian recommendations
- 2026-01-05: Joined gym, began light resistance training

The morning headaches may correlate with the timing of his blood pressure medication;
further discussion regarding timing optimization may be beneficial.

## Laboratory Results

Labs obtained on January 15, 2026, show encouraging progress:

| Test | Value | Reference | Status | Trend |
|------|-------|-----------|--------|-------|
| HbA1c | 6.8% | <5.7% (normal) | Elevated | ↓ Improved (was 7.2%) |
| Fasting Glucose | 118 mg/dL | 70-99 | Elevated | ↓ Improved (was 145) |
| Creatinine | 1.0 mg/dL | 0.7-1.3 | Normal | Stable |
| Potassium | 4.2 mEq/L | 3.5-5.0 | Normal | Stable |

His HbA1c has decreased by 0.4% over three months on metformin monotherapy, suggesting
good response to current therapy. Renal function remains stable on lisinopril, with
no electrolyte abnormalities. Lipid panel was not repeated at this visit; last values
from October showed LDL 142 mg/dL (above target for diabetic patient).

## Active Medical Conditions

- **Type 2 Diabetes Mellitus** (diagnosed 2025-10): Currently on metformin, responding well
- **Essential Hypertension** (diagnosed 2025-10): On lisinopril, home BP readings 128-135/78-84
- **Obesity** (BMI 32.1): Weight stable at 218 lbs; actively working on lifestyle changes

## Summary & Considerations

Key discussion points for this visit:

1. **Glycemic control improving**: HbA1c down 0.4% on metformin alone. Consider continuing
   current regimen with repeat HbA1c in 3 months. Discuss target goal (<7% vs <6.5%).

2. **Morning headaches**: Evaluate relationship to BP medication timing. Consider checking
   morning blood pressure before medication dose. Rule out sleep apnea given obesity.

3. **Orthostatic symptoms**: Occasional dizziness on standing - check orthostatic vitals
   today. May warrant lisinopril dose adjustment if significant drop.

4. **Lipid management**: LDL 142 mg/dL untreated. Per guidelines, diabetic patients benefit
   from statin therapy. Discuss initiation of moderate-intensity statin.

5. **Exercise clearance**: Patient asking about increasing exercise intensity. Cardiac risk
   assessment may be appropriate given new diabetes diagnosis and desire for vigorous exercise.

---
*This summary was generated by health-agent to support clinical decision-making.
All data is patient-reported or extracted from personal health records.
Please verify critical information.*
```

## Efficient Data Access

All data files are large (>256KB). Use filtered extraction commands (shown above) rather than direct reads.

If `{labs_path}/lab_specs.json` exists, use helper functions for canonical marker names:
```bash
source .claude/skills/health-agent/references/lab-specs-helpers.sh
canonical_name=$(get_canonical_name "{labs_path}/lab_specs.json" "HbA1c")
pattern=$(build_grep_pattern "{labs_path}/lab_specs.json" "HbA1c")
```

## Error Handling

- If genetics_23andme_path not configured: Skip genetics section entirely
- If no abnormal labs in timeframe: Note "All recent labs within reference ranges"
- If no recent events: Note "No significant health events documented in timeframe"
- If data source missing: Note in output which sources were unavailable

## Example User Interaction

**User**: "I have my annual physical next week, can you prepare a summary?"

**Assistant**:
1. Uses AskUserQuestion: "What date range should I cover? (Last 12 months / Last 6 months / Custom)"
2. Gathers all relevant data sources
3. Applies status determination to medications/conditions
4. Checks for abnormal labs
5. Reviews recent health events and groups by category
6. IF genetics configured: Checks for relevant findings
7. Generates coherent narrative document
8. Saves to `.output/{profile}/provider-visit-annual-2026-01-21.md`
9. Confirms completion with summary of included sections

**What NOT to do**:
- ❌ Don't invoke deleted skills like `report-medication-list` (they don't exist)
- ❌ Don't generate separate section files then concatenate (not coherent)
- ❌ Don't include genetics by default (only when relevant)
- ❌ Don't ask excessive questions (smart defaults based on visit type)
- ❌ Don't use Bash heredocs for file writing (use Write tool)

## Integration with Other Skills

- **genetics-snp-lookup**: Call directly when genetics relevant to visit
- **scientific-literature-search**: Generally NOT needed for provider summaries (use for investigations only)
- **investigate-root-cause**: If user mentions specific health concern, suggest running investigation separately before visit

Provider visit summaries are for DATA PRESENTATION, not hypothesis generation.
