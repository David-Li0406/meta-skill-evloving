---
name: clinical-reports
description: Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports (radiology/pathology/lab), clinical trial reports (ICH-E3, SAE, CSR), and patient documentation (SOAP, H&P, discharge summaries). Full support with templates, regulatory compliance (HIPAA, FDA, ICH-GCP), and validation tools.
---

# Clinical Report Writing

## Overview

Clinical report writing is the process of documenting medical information with precision, accuracy, and compliance with regulatory standards. This skill covers four major categories of clinical reports: case reports for journal publication, diagnostic reports for clinical practice, clinical trial reports for regulatory submission, and patient documentation for medical records. Apply this skill for healthcare documentation, research dissemination, and regulatory compliance.

**Critical Principle: Clinical reports must be accurate, complete, objective, and compliant with applicable regulations (HIPAA, FDA, ICH-GCP).** Patient privacy and data integrity are paramount. All clinical documentation must support evidence-based decision-making and meet professional standards.

## When to Use This Skill

This skill should be used when:
- Writing clinical case reports for journal submission (CARE guidelines)
- Creating diagnostic reports (radiology, pathology, laboratory)
- Documenting clinical trial data and adverse events
- Preparing clinical study reports (CSR) for regulatory submission
- Writing patient progress notes, SOAP notes, and clinical summaries
- Drafting discharge summaries, H&P documents, or consultation notes
- Ensuring HIPAA compliance and proper de-identification
- Validating clinical documentation for completeness and accuracy
- Preparing serious adverse event (SAE) reports
- Creating data safety monitoring board (DSMB) reports

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every clinical report MUST include at least 1 AI-generated figure using the scientific-schematics skill.**

This is not optional. Clinical reports benefit greatly from visual elements. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., patient timeline, diagnostic algorithm, or treatment workflow)
2. For case reports: include clinical progression timeline
3. For trial reports: include CONSORT flow diagram

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Patient case timelines and clinical progression diagrams
- Diagnostic algorithm flowcharts
- Treatment protocol workflows
- Anatomical diagrams for case reports
- Clinical trial participant flow diagrams (CONSORT)
- Adverse event classification trees
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Core Capabilities

### 1. Clinical Case Reports for Journal Publication

Clinical case reports describe unusual clinical presentations, novel diagnoses, or rare complications. They contribute to medical knowledge and are published in peer-reviewed journals.

#### CARE Guidelines Compliance

The CARE (CAse REport) guidelines provide a standardized framework for case report writing. All case reports should follow this checklist:

**Title**
- Include the words "case report" or "case study"
- Indicate the area of focus
- Example: "Unusual Presentation of Acute Myocardial Infarction in a Young Patient: A Case Report"

**Keywords**
- 2-5 keywords for indexing and searchability
- Use MeSH (Medical Subject Headings) terms when possible

**Abstract** (structured or unstructured, 150-250 words)
- Introduction: What is unique or novel about the case?
- Patient concerns: Primary symptoms and key medical history
- Diagnoses: Primary and secondary diagnoses
- Interventions: Key treatments and procedures
- Outcomes: Clinical outcome and follow-up
- Conclusions: Main takeaway or clinical lesson

**Introduction**
- Brief background on the medical condition
- Why this case is novel or important
- Literature review of similar cases (brief)
- What makes this case worth reporting

**Patient Information**
- Demographics (age, sex, race/ethnicity if relevant)
- Medical history, family history, social history
- Relevant comorbidities
- **De-identification**: Remove or alter 18 HIPAA identifiers
- **Patient consent**: Document informed consent for publication

**Clinical Findings**
- Chief complaint and presenting symptoms
- Physical examination findings
- Timeline of symptoms (consider timeline figure or table)
- Relevant clinical observations

**Timeline**
- Chronological summary of key events
- Dates of symptoms, diagnosis, interventions, outcomes
- Can be presented as a table or figure
- Example format:
  - Day 0: Initial presentation with symptoms X, Y, Z
  - Day 2: Diagnostic test A performed, revealed finding B
  - Day 5: Treatment initiated with drug C
  - Day 14: Clinical improvement noted
  - Month 3: Follow-up examination shows complete resolution

**Diagnostic Assessment**
- Diagnostic tests performed (labs, imaging, procedures)
- Results and interpretation
- Differential diagnosis considered
- Rationale for final diagnosis
- Challenges in diagnosis

**Therapeutic Interventions**
- Medications (names, dosages, routes, duration)
- Procedures or surgeries performed
- Non-pharmacological interventions
- Reasoning for treatment choices
- Alternative treatments considered

**Follow-up and Outcomes**
- Clinical outcome (resolution, improvement, unchanged, worsened)
- Follow-up duration and frequency
- Long-term outcomes if available
- Patient-reported outcomes
- Adherence to treatment

**Discussion**
- Strengths and novelty of the case
- How this case compares to existing literature
- Limitations of the case report
- Potential mechanisms or explanations
- Clinical implications and lessons learned
- Unanswered questions or areas for future research

**Patient Perspective** (optional but encouraged)
- Patient's experience and viewpoint
- Impact on quality of life
- Patient-reported outcomes
- Quote from patient if appropriate

**Informed Consent**
- Statement documenting patient consent for publication
- If patient deceased or unable to consent, describe proxy consent
- For pediatric cases, parental/guardian consent
- Example: "Written informed consent was obtained from the patient for publication of this case report and accompanying images. A copy of the written consent is available for review by the Editor-in-Chief of this journal."

For detailed CARE guidelines, refer to `references/case_report_guidelines.md`.

#### Journal-Specific Requirements

Different journals have specific formatting requirements:
- Word count limits (typically 1500-3000 words)
- Number of figures/tables allowed
- Reference style (AMA, Vancouver, APA)
- Structured vs. unstructured abstract
- Supplementary materials policies

Check journal instructions for authors before submission.

#### De-identification and Privacy

**18 HIPAA Identifiers to Remove or Alter:**
1. Names
2. Geographic subdivisions smaller than state
3. Dates (except year)
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying characteristic

**Best Practices:**
- Use "the patient" instead of names
- Report age ranges (e.g., "a woman in her 60s") or exact age if relevant
- Use approximate dates or time intervals (e.g., "3 months prior")
- Remove institution names unless necessary
- Blur or crop identifying features in images
- Obtain explicit consent for any potentially identifying information

### 2. Clinical Diagnostic Reports

Diagnostic reports communicate findings from imaging studies, pathological examinations, and laboratory tests. They must be clear, accurate, and actionable.

#### Radiology Reports

Radiology reports follow a standardized structure to ensure clarity and completeness.

**Standard Structure:**

**1. Patient Demographics**
- Patient name (or ID in research contexts)
- Date of birth or age
- Medical record number
- Examination date and time

**2. Clinical Indication**
- Reason for examination
- Relevant clinical history
- Specific clinical question to be answered
- Example: "Rule out pulmonary embolism in patient with acute dyspnea"

**3. Technique**
- Imaging modality (X-ray, CT, MRI, ultrasound, PET, etc.)
- Anatomical region examined
- Contrast administration (type, route, volume)
- Protocol or sequence used
- Technical quality and limitations
- Example: "Contrast-enhanced CT of the chest, abdomen, and pelvis was performed using 100 mL of intravenous iodinated contrast. Oral contrast was not administered."

**4. Comparison**
- Prior imaging studies available for comparison
- Dates of prior studies
- Stability or change from prior imaging
- Example: "Comparison: CT chest from [date]"

**5. Findings**
- Systematic description of imaging findings
- Organ-by-organ or region-by-region approach
- Positive findings first, then pertinent negatives
- Measurements of lesions or abnormalities
- Use of standardized terminology (ACR lexicon, RadLex)
- Example:
  - Lungs: Bilateral ground-glass opacities, predominant in the lower lobes. No consolidation or pleural effusion.
  - Mediastinum: No lymphadenopathy. Heart size normal.
  - Abdomen: Liver, spleen, pancreas unremarkable. No free fluid.

**6. Impression/Conclusion**
- Concise summary of key findings
- Answers to the clinical question
- Differential diagnosis if applicable
- Recommendations for follow-up or additional studies
- Level of suspicion or diagnostic certainty
- Example:
  - "1. Bilateral ground-glass opacities consistent with viral pneumonia or atypical infection. COVID-19 cannot be excluded. Clinical correlation recommended.
  - 2. No evidence of pulmonary embolism.
  - 3. Recommend follow-up imaging in 4-6 weeks to assess resolution."

**Structured Reporting:**

Many radiology departments use structured reporting templates for common examinations:
- Lung nodule reporting (Lung-RADS)
- Breast imaging (BI-RADS)
- Liver imaging (LI-RADS)
- Prostate imaging (PI-RADS)
- CT colonography (C-RADS)

Structured reports improve consistency, reduce ambiguity, and facilitate data extraction.

For radiology reporting standards, see `references/diagnostic_reports_standards.md`.

#### Pathology Reports

Pathology reports document microscopic findings from tissue specimens and provide diagnostic conclusions.

**Surgical Pathology Report Structure:**

**1. Patient Information**
- Patient name and identifiers
- Date of birth, age, sex
- Ordering physician
- Medical record number
- Specimen received date

**2. Specimen Information**
- Specimen type (biopsy, excision, resection)
- Anatomical site
- Laterality if applicable
- Number of specimens/blocks/slides
- Example: "Skin, left forearm, excisional biopsy"

**3. Clinical History**
- Relevant clinical information
- Indication for biopsy
- Prior diagnoses
- Example: "History of melanoma. New pigmented lesion, rule out recurrence."

**4. Gross Description**
- Macroscopic appearance of specimen
- Size, weight, color, consistency
- Orientation markers if present
- Sectioning and sampling approach
- Example: "The specimen consists of an ellipse of skin measuring 2.5 x 1.0 x 0.5 cm. A pigmented lesion measuring 0.6 cm in diameter is present on the surface. The specimen is serially sectioned and entirely submitted in cassettes A1-A3."

**5. Microscopic Description**
- Histological findings
- Cellular characteristics
- Architectural patterns
- Presence of malignancy
- Margins if applicable
- Special stains or immunohistochemistry results

**6. Diagnosis**
- Primary diagnosis
- Grade and stage if applicable (cancer)
- Margin status
- Lymph node status if applicable
- Synoptic reporting for cancers (CAP protocols)
- Example:
  - "MALIGNANT MELANOMA, SUPERFICIAL SPREADING TYPE
  - Breslow thickness: 1.2 mm
  - Clark level: IV
  - Mitotic rate: 3/mm²
  - Ulceration: Absent
  - Margins: Negative (closest margin 0.4 cm)
  - Lymphovascular invasion: Not identified"

**7. Comment** (if needed)
- Additional context or interpretation
- Differential diagnosis
- Recommendations for additional studies
- Clinical correlation suggestions

**Synoptic Reporting:**

The College of American Pathologists (CAP) provides synoptic reporting templates for cancer specimens. These checklists ensure all relevant diagnostic elements are documented.

Key elements for cancer reporting:
- Tumor site
- Tumor size
- Histologic type
- Histologic grade
- Extent of invasion
- Lymph-vascular invasion
- Perineural invasion
- Margins
- Lymph nodes (number examined, number positive)
- Pathologic stage (TNM classification)
- Ancillary studies (molecular markers, biomarkers)

#### Laboratory Reports

Laboratory reports communicate test results for clinical specimens (blood, urine, tissue, etc.).

**Standard Components:**

**1. Patient and Specimen Information**
- Patient identifiers
- Specimen type (blood, serum, urine, CSF, etc.)
- Collection date and time
- Received date and time
- Ordering provider

**2. Test Name and Method**
- Full test name
- Methodology (immunoassay, spectrophotometry, PCR, etc.)
- Laboratory accession number

**3. Results**
- Quantitative or qualitative result
- Units of measurement
- Reference range (normal values)
- Flags for abnormal values (H = high, L = low)
- Critical values highlighted
- Example:
  - Hemoglobin: 8.5 g/dL (L) [Reference: 12.0-16.0 g/dL]
  - White Blood Cell Count: 15.2 x10³/μL (H) [Reference: 4.5-11.0 x10³/μL]

**4. Interpretation** (when applicable)
- Clinical significance of results
- Suggested follow-up or additional testing
- Correlation with diagnosis
- Drug levels and therapeutic ranges

**5. Quality Control Information**
- Specimen adequacy
- Specimen quality issues (hemolyzed, lipemic, clotted)
- Delays in processing
- Technical limitations

**Critical Value Reporting:**
- Life-threatening results require immediate notification
- Examples: glucose <40 or >500 mg/dL, potassium <2.5 or >6.5 mEq/L
- Document notification time and recipient

For laboratory standards and terminology, see `references/diagnostic_reports_standards.md`.

### 3. Clinical Trial Reports

Clinical trial reports document the conduct, results, and safety of clinical research studies. These reports are essential for regulatory submissions and scientific publication.

#### Serious Adverse Event (SAE) Reports

SAE reports document unexpected serious adverse reactions during clinical trials. Regulatory requirements mandate timely reporting to IRBs, sponsors, and regulatory agencies.

**Definition of Serious Adverse Event:**
An adverse event is serious if it:
- Results in death
- Is life-threatening
- Requires inpatient hospitalization or prolongation of existing hospitalization
- Results in persistent or significant disability/incapacity
- Is a congenital anomaly/birth defect
- Requires intervention to prevent permanent impairment or damage

**SAE Report Components:**

**1. Study Information**
- Protocol number and title
- Study phase
- Sponsor name
- Principal investigator
- IND/IDE number (if applicable)
- Clinical trial registry number (NCT number)

**2. Patient Information (De-identified)**
- Subject ID or randomization number
- Age, sex, race/ethnicity
- Study arm or treatment group
- Date of informed consent
- Date of first study intervention

**3. Event Information**
- Event description (narrative)
- Date of onset
- Date of resolution (or ongoing)
- Severity (mild, moderate, severe)
- Seriousness criteria met
- Outcome (re