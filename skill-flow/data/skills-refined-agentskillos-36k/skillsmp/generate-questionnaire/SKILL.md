---
name: generate-questionnaire
description: Generate comprehensive health log augmentation questionnaires for systematic data collection. Use when user asks "create questionnaire", "generate questionnaire", "health log augmentation", or needs structured data collection forms.
---

# Generate Questionnaire

Generate comprehensive questionnaires to systematically augment existing health log data with additional context, patterns, and details.

## Purpose

This skill provides:
- Structured questionnaires tailored to profile's existing conditions and patterns
- Systematic data collection across 14 major health domains
- Gap analysis to identify missing information
- Actionable follow-up tasks for enriching health records

## Workflow

1. Load profile to get demographics and data source paths
2. Sample recent health log entries (last 100 rows of CSV, recent narrative entries)
3. Identify active conditions, medications, symptoms, and episodes
4. Generate questionnaire sections targeting identified patterns
5. Include follow-up recommendations
6. Save to `.output/{profile}/questionnaires/health-log-augmentation-{date}.md`

## Efficient Data Access

### Current State (Source of Truth)
```bash
# Read current.yaml for active medications, conditions, supplements
cat "{health_log_path}/current.yaml"
```

### Sample Recent Health Timeline Entries
```bash
# Last 100 CSV entries from history.csv to identify recent patterns
tail -100 "{health_log_path}/history.csv"

# Recent narrative entries for context
tail -200 "{health_log_path}/health_log.md" | head -150
```

### Identify Active Conditions
```bash
# From current.yaml (preferred - source of truth)
grep -A 100 "^conditions:" "{health_log_path}/current.yaml"

# From history.csv (for timeline analysis)
grep -E ",(condition|symptom)," "{health_log_path}/history.csv" | tail -50
```

### Identify Current Medications/Supplements
```bash
# From current.yaml (preferred - source of truth)
grep -A 100 "^medications:" "{health_log_path}/current.yaml"
grep -A 100 "^supplements:" "{health_log_path}/current.yaml"

# From history.csv (for timeline analysis)
grep -E ",(medication|supplement)," "{health_log_path}/history.csv" | tail -50
```

## Questionnaire Structure

The questionnaire should include these major sections:

### Core Sections (Always Include)
1. **Chronic Conditions Deep Dive** - Pattern analysis for persistent conditions
2. **Medication & Supplement Responses** - Why discontinued, PRN protocols, sensitivities
3. **Symptom Deep Dives** - Detailed characterization of recurring symptoms
4. **Family History** - First-degree relatives, specific condition screening
5. **Lab Work Correlations** - Patterns, missing tests, frequency
6. **Health Goals & Priorities** - Current focus areas, functional goals

### Conditional Sections (Include If Relevant)
7. **Infectious Disease History** - If URI or infections present in log
8. **Musculoskeletal Issues** - If orthopedic conditions present
9. **Environmental & Lifestyle** - Work, exercise, diet, sleep, stress
10. **Medical Provider Relationships** - Care team, coordination gaps
11. **Genetic Data** - If genetics_23andme_path configured in profile
12. **Exam & Imaging History** - If multiple imaging studies present
13. **Episode-Specific Deep Dives** - For significant episodes requiring more context
14. **Open-Ended Reflections** - Always include for uncaptured patterns

## Section Templates

### Chronic Condition Template
For each chronic condition identified, create a subsection with:
- **Temporal Patterns**: Seasonal, stress-related, activity-related
- **Symptom Correlations**: Associated symptoms, severity scales
- **Triggering Factors**: Foods, medications, activities
- **Family History**: Related conditions in relatives
- **Treatment Response Matrix**: Interventions tried, effectiveness ratings

### Medication/Supplement Template
For discontinued items:
- Start date, stop date, reason for discontinuation, would retry?

For PRN items:
- Specific triggers, typical relief timeline, decision criteria

For sensitivities:
- Dose-response details, time to symptoms, mitigation strategies

### Lab Work Template
- Patterns noticed across markers
- Frequency of testing
- Missing lab data (tests never done but potentially informative)

## Output Format

```markdown
# Health Log Augmentation Questionnaire
**Profile**: {name}
**Generated**: {YYYY-MM-DD}
**Purpose**: Systematic data collection to enrich existing health log entries

---

## Instructions

This questionnaire is designed to be completed iteratively...

[Instructions for use]

---

## Section 1: [Section Name]

### 1.1 [Subsection]

**[Question Category]:**
- [ ] Question 1
- [ ] Question 2

[Tables, forms, or structured data collection templates]

---

[Repeat for all sections]

---

## Next Steps

After completing relevant sections:

1. **Update health log entries** with new details
2. **Generate targeted analyses** using health-agent skills:
   - Use lab queries (see `analysis-patterns.md`) for markers with clarified patterns
   - Investigate episodes with enriched context
   - Identify cross-temporal correlations using data patterns
   - Run `investigate-root-cause` for conditions with new context
3. **Create provider reports** with augmented data (use `prepare-provider-visit`)
4. **Consider additional testing** based on gaps identified
5. **Set up prospective tracking** for patterns to monitor going forward

---

**Questionnaire Version**: 1.0
**Last Updated**: {YYYY-MM-DD}
**Status**: Initial draft for iterative completion
```

## Output File

- **Directory**: `.output/{profile}/questionnaires/`
- **Filename**: `health-log-augmentation-{YYYY-MM-DD}.md`
- **Create directory if needed**: `mkdir -p .output/{profile}/questionnaires`

## Questionnaire Design Principles

1. **Iterative Completion** - Don't require all-at-once completion
2. **Targeted Questions** - Base questions on actual conditions/patterns in the data
3. **Multiple Formats** - Use checkboxes, tables, scales, and open-ended questions
4. **Actionable Output** - Include specific next steps for using collected information
5. **Gap Analysis** - Explicitly identify missing information that would be valuable
6. **Mark Uncertainty** - Provide convention for uncertain information (e.g., `[UNCERTAIN]`)

## Integration with Other Skills

After questionnaire completion, recommend these follow-up analyses:

- **Data Analysis**: Use enriched data with lab queries and timeline correlation (see `analysis-patterns.md`)
- **Root Cause Investigation**: Better-informed `investigate-root-cause` with detailed patterns
- **Provider Reports**: More comprehensive `prepare-provider-visit` summaries with augmented context
- **Genetics Lookups**: Targeted SNP lookups via `genetics-snp-lookup` based on conditions

## Special Considerations

- **Privacy**: Questionnaires should be saved locally and gitignored
- **Length**: Comprehensive but skippable - users should be able to work through in stages
- **Personalization**: Tailor sections to the individual's actual health patterns, not generic questions
- **Time Efficiency**: Prioritize high-value questions that fill genuine gaps in the data
- **Clinical Relevance**: Focus on information that would aid diagnosis, treatment, or pattern identification

## Example Triggers

User phrases that should invoke this skill:
- "Create a questionnaire for me"
- "Generate health log augmentation questionnaire"
- "I want to add more detail to my health data"
- "Help me systematically fill in gaps in my health records"
- "Questionnaire to enrich my health log"

---

## Gap Analysis Algorithm

### Overview

The gap analysis algorithm systematically identifies missing information that would improve health understanding, diagnosis, and treatment decisions. It scores gaps by clinical value and generates targeted questions.

### Step 1: Data Inventory

First, inventory what data IS present:

```bash
# Count entries by type
echo "=== Data Inventory ==="

# From current.yaml (current state)
echo "Current Medications: $(grep -c '^\s*-\s*name:' <(grep -A 100 '^medications:' "$current_yaml" 2>/dev/null) 2>/dev/null || echo 0)"
echo "Current Supplements: $(grep -c '^\s*-\s*name:' <(grep -A 100 '^supplements:' "$current_yaml" 2>/dev/null) 2>/dev/null || echo 0)"
echo "Current Conditions: $(grep -c '^\s*-\s*name:' <(grep -A 100 '^conditions:' "$current_yaml" 2>/dev/null) 2>/dev/null || echo 0)"

# From history.csv (timeline)
echo "Historical Medications: $(grep -c ',medication,' "$history_csv")"
echo "Historical Supplements: $(grep -c ',supplement,' "$history_csv")"
echo "Historical Symptoms: $(grep -c ',symptom,' "$history_csv")"
echo "Historical Conditions: $(grep -c ',condition,' "$history_csv")"
echo "Labs: $(wc -l < "$labs_csv" | tr -d ' ')"
echo "Exams: $(find "$exams_path" -name "*.summary.md" | wc -l | tr -d ' ')"
echo "Entities: $(grep -oE 'entity_[0-9]+' "$history_csv" | sort -u | wc -l | tr -d ' ')"
```

### Step 2: Gap Detection Rules

For each domain, apply these detection rules:

#### Medications Gap Detection

| Gap Type | Detection Rule | Priority |
|----------|---------------|----------|
| Missing discontinuation reason | Medication appears, then stops without "reason" in details | HIGH |
| Missing start date | Medication mentioned without clear start date | MEDIUM |
| Missing dosage | Medication name present but no dose information | MEDIUM |
| Missing response assessment | Medication taken >3 months with no efficacy notes | MEDIUM |
| Missing side effect documentation | Medication present but no side effect entries | LOW |

```bash
# Find medications without discontinuation reason (from history.csv)
grep ',medication,' "$history_csv" | \
  grep -iE 'stopped|discontinued|ended' | \
  grep -viE 'reason|because|due to|side effect' | \
  awk -F',' '{print $1, $2, $3, $5}'
```

#### Symptoms Gap Detection

| Gap Type | Detection Rule | Priority |
|----------|---------------|----------|
| Uncharacterized severity | Symptom mentioned without severity scale | HIGH |
| Missing duration | Symptom without start/end dates | HIGH |
| No triggering factors | Recurrent symptom (>3 occurrences) without triggers documented | HIGH |
| No resolution documented | Symptom started but no resolution entry | MEDIUM |
| Missing temporal pattern | >5 symptom entries without pattern analysis | MEDIUM |

```bash
# Find recurring symptoms without pattern info (from history.csv)
grep ',symptom,' "$history_csv" | \
  awk -F',' '{print $3}' | \
  sort | uniq -c | sort -rn | \
  awk '$1 > 3 {print $0}'
# These recurring symptoms need pattern questions
```

#### Conditions Gap Detection

| Gap Type | Detection Rule | Priority |
|----------|---------------|----------|
| No family history for heritable condition | Condition known to be genetic, no family data | CRITICAL |
| Missing diagnostic confirmation | Condition listed as "suspected" >6 months | HIGH |
| No treatment response tracking | Condition present >6 months, no efficacy data | HIGH |
| Missing onset circumstances | Condition without onset details | MEDIUM |

#### Labs Gap Detection

| Gap Type | Detection Rule | Priority |
|----------|---------------|----------|
| Missing baseline for new medication | Medication started, no pre-treatment labs | HIGH |
| Abnormal value not repeated | Out-of-range lab >6 months old, not rechecked | HIGH |
| Missing confirmatory test | Single abnormal value, no follow-up | MEDIUM |
| Incomplete workup | Condition suggests tests not yet done | HIGH |

```bash
# Find abnormal labs not repeated (from all.csv)
awk -F',' 'NR>1 && ($5<$7 || $5>$8) {print $1, $4}' "$labs_csv" | \
  sort -t' ' -k2 | \
  uniq -f1 -c | \
  awk '$1 == 1 {print "Single abnormal:", $2, $3}'
```

### Step 3: Gap Scoring

Each identified gap receives a score based on:

```
Gap Score = Clinical_Value × Fillability × Urgency
```

#### Clinical Value (1-5)

| Score | Meaning | Example |
|-------|---------|---------|
| 5 | Critical for diagnosis/treatment | Family history for heritable condition |
| 4 | Significantly improves understanding | Medication side effect details |
| 3 | Useful for pattern recognition | Symptom triggers |
| 2 | Provides helpful context | Lifestyle factors |
| 1 | Nice to have | Historical details |

#### Fillability (1-3)

| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Patient can easily answer | "Do you have family history of X?" |
| 2 | Requires some recall/research | "When exactly did symptom start?" |
| 1 | May require records/testing | "What was your HbA1c 5 years ago?" |

#### Urgency (1-3)

| Score | Meaning | Example |
|-------|---------|---------|
| 3 | Needed for upcoming decision | Info needed before specialist visit |
| 2 | Would improve current management | Optimization opportunity |
| 1 | Can wait for routine collection | Long-term tracking |

**Prioritization Formula**:
```
Priority Score = Clinical_Value × Fillability × Urgency
Max score = 5 × 3 × 3 = 45
```

| Total Score | Priority Level | Action |
|-------------|----------------|--------|
| 30-45 | CRITICAL | Include in top 5 questions |
| 15-29 | HIGH | Include in questionnaire |
| 8-14 | MEDIUM | Include if space permits |
| 1-7 | LOW | Optional section |

### Step 4: Domain Prioritization

When generating the questionnaire, order domains by aggregate gap score:

```python
# Pseudocode for domain prioritization
domain_scores = {}
for gap in identified_gaps:
    domain = gap.domain  # e.g., "medications", "symptoms"
    score = gap.clinical_value * gap.fillability * gap.urgency
    domain_scores[domain] = domain_scores.get(domain, 0) + score

# Sort domains by total score
prioritized_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
```

**Default Domain Priority** (when scores are equal):

1. **Family History** - Often most impactful, frequently missing
2. **Medications** - Critical for safety and treatment decisions
3. **Symptoms** - Essential for diagnosis
4. **Conditions** - Core health understanding
5. **Labs** - Objective data gaps
6. **Lifestyle** - Context and modifiable factors
7. **Provider Relationships** - Care coordination
8. **Goals** - Patient-centered care

### Step 5: Question Generation

For each high-priority gap, generate targeted questions:

#### Question Templates by Gap Type

**Missing Family History**:
```markdown
### Family History: {Condition}

Your health log indicates {condition}. Family history is important for understanding your risk.

**First-degree relatives (parents, siblings, children):**
- [ ] Mother: {condition}? Age at diagnosis? Current status?
- [ ] Father: {condition}? Age at diagnosis? Current status?
- [ ] Siblings: Any with {condition}? Details:
- [ ] Children: Any with {condition}? Details:

**Second-degree relatives (grandparents, aunts/uncles):**
- [ ] Any known cases of {condition}?
```

**Missing Medication Details**:
```markdown
### Medication: {Name}

You've been taking {medication}. Please fill in any missing details:

| Question | Your Answer |
|----------|-------------|
| Exact dose | |
| Frequency | |
| Date started | |
| Why prescribed | |
| How well does it work? (1-5) | |
| Any side effects? | |
| Have you ever missed doses? How often? | |
```

**Missing Symptom Characterization**:
```markdown
### Symptom: {Symptom Name}

This symptom has appeared {count} times in your records. Help us understand the pattern:

**Severity Scale** (use for each occurrence):
1 = Barely noticeable
2 = Mild, doesn't affect activities
3 = Moderate, somewhat limits activities
4 = Severe, significantly limits activities
5 = Extreme, incapacitating

**Pattern Questions**:
- Time of day most common: [ ] Morning [ ] Afternoon [ ] Evening [ ] Night [ ] No pattern
- Duration typically: [ ] Minutes [ ] Hours [ ] Days [ ] Constant
- What makes it better?:
- What makes it worse?:
- Associated symptoms:

**Occurrence Log** (fill in for recent episodes):
| Date | Severity (1-5) | Trigger (if known) | What helped |
|------|----------------|-------------------|-------------|
| | | | |
```

---

## Example Questionnaire Output

Below is an example of a generated questionnaire based on gap analysis:

```markdown
# Health Log Augmentation Questionnaire
**Profile**: Jane Doe
**Generated**: 2026-01-23
**Purpose**: Systematic data collection to enrich existing health log entries

---

## Instructions

This questionnaire targets specific gaps identified in your health records. You don't
need to complete everything at once—work through sections as you have time. For each
question, answer as completely as you can; if uncertain, mark with [UNCERTAIN].

**Priority indicators**:
- 🔴 CRITICAL: Important for upcoming care decisions
- 🟡 HIGH: Significantly improves health understanding
- 🟢 MEDIUM: Helpful context

---

## Section 1: Family History 🔴 CRITICAL

*Gap detected: Your records show elevated bilirubin and suspected Gilbert syndrome,
but no family history is documented. Gilbert syndrome is genetic.*

### 1.1 Gilbert Syndrome / Jaundice

Do any blood relatives have:
- [ ] Gilbert syndrome (diagnosed)
- [ ] History of jaundice (yellowing of eyes/skin)
- [ ] Unexplained elevated bilirubin

**If yes, please specify:**

| Relative | Condition | Age at Diagnosis | Notes |
|----------|-----------|------------------|-------|
| | | | |

### 1.2 Anemia / Blood Disorders

Have any blood relatives been diagnosed with:
- [ ] Hereditary spherocytosis
- [ ] Sickle cell disease or trait
- [ ] Thalassemia
- [ ] G6PD deficiency
- [ ] Other hemolytic anemia
- [ ] Iron deficiency requiring treatment
- [ ] Needed their spleen removed

**If yes, please specify relationship and details:**

---

## Section 2: Medication Responses 🟡 HIGH

*Gap detected: Several medications were discontinued without documented reasons.*

### 2.1 Discontinued Medications

Please provide details for each medication you stopped:

**Omeprazole** (appears stopped around 2025-06)
- Why did you stop? [ ] Side effects [ ] Not effective [ ] No longer needed [ ] Cost [ ] Other
- If side effects, what were they?:
- Would you take it again if needed? [ ] Yes [ ] No [ ] Maybe

**Vitamin D 2000 IU** (appears stopped around 2025-09)
- Why did you stop?:
- Current vitamin D status: [ ] Taking different form [ ] Not taking any [ ] Unknown

### 2.2 Current Medication Efficacy

For medications you're currently taking, rate effectiveness:

| Medication | Works Well (1-5) | Any Side Effects? | Would Recommend? |
|------------|------------------|-------------------|------------------|
| Lisinopril 10mg | | | |
| Metformin 500mg | | | |

---

## Section 3: Symptom Deep Dive 🟡 HIGH

*Gap detected: "Fatigue" appears 8 times without characterization.*

### 3.1 Fatigue Pattern Analysis

Your records show fatigue mentioned on: 2025-03-15, 2025-04-02, 2025-05-18,
2025-06-30, 2025-08-12, 2025-09-25, 2025-11-08, 2026-01-05

**Severity by episode** (use scale 1-5):
| Date | Severity | Duration | Possible Trigger |
|------|----------|----------|------------------|
| 2025-03-15 | | | |
| 2025-04-02 | | | |
| [continue...] | | | |

**Pattern Questions**:
- Worse at specific times? [ ] Morning [ ] Afternoon [ ] Evening [ ] Variable
- Related to sleep quality? [ ] Yes [ ] No [ ] Uncertain
- Related to meals? [ ] Yes [ ] No [ ] Uncertain
- Related to stress? [ ] Yes [ ] No [ ] Uncertain
- Relieved by rest? [ ] Yes [ ] No [ ] Partially

**Associated symptoms when fatigued**:
- [ ] Brain fog / difficulty concentrating
- [ ] Muscle weakness
- [ ] Headache
- [ ] Dizziness
- [ ] Other:

---

## Section 4: Lab Correlations 🟢 MEDIUM

*Gap detected: Abnormal values without follow-up context.*

### 4.1 Elevated Bilirubin

Your bilirubin has been elevated on multiple tests. Please document:

- Do you notice yellowing of eyes when bilirubin is high? [ ] Yes [ ] No [ ] Never checked
- Does it correlate with: [ ] Fasting [ ] Stress [ ] Illness [ ] Exercise [ ] Unknown
- Have you ever been told you have Gilbert syndrome? [ ] Yes [ ] No [ ] Suspected

### 4.2 Missing Tests

Based on your conditions, these tests might be informative but aren't in your records:

| Test | Would you be willing to get this? | Notes |
|------|-----------------------------------|-------|
| Reticulocyte count | [ ] Yes [ ] No [ ] Already done | |
| Haptoglobin | [ ] Yes [ ] No [ ] Already done | |
| LDH | [ ] Yes [ ] No [ ] Already done | |
| Direct Coombs | [ ] Yes [ ] No [ ] Already done | |

---

## Section 5: Open-Ended 🟢 MEDIUM

### 5.1 Anything Else?

Is there anything about your health that:
- You've been meaning to document but haven't?
- You think is important but doesn't fit standard categories?
- You've noticed as a pattern but aren't sure is significant?

**Space for notes:**




---

## Next Steps

After completing relevant sections:

1. **Update health log entries** with new details using health-log-parser
2. **Run targeted analyses** with enriched data
3. **Consider investigate-root-cause** for conditions with new family history
4. **Prepare provider visit** using `prepare-provider-visit` with augmented data
5. **Schedule recommended tests** identified in Section 4.2

---

**Questionnaire Version**: 1.0
**Generated**: 2026-01-23
**Priority Gaps Identified**: 12
**Estimated Completion Time**: 20-30 minutes
```
