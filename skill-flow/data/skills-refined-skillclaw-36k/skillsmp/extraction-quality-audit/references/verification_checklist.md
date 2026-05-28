# Verification Checklist

Systematic checklist for quality verification of extraction pipeline outputs.

## Overview

This checklist guides detailed comparison of source documents against extraction outputs. Use Claude's vision capabilities to read source documents and compare against structured extraction results.

**Time per document:** 5-15 minutes depending on complexity

**Tools needed:**
- Claude with vision access
- Source documents (PDFs, images)
- Extraction outputs (markdown, JSON, etc.)
- Results tracking template

## General Verification Workflow

### Step 1: Load Documents

**Source document:**
```
Use Read tool to view source document (PDF, image, etc.)
If multi-page, note page count and content type of each page
```

**Extraction outputs:**
```
Read all extraction files:
- Per-page files (e.g., doc.1.md, doc.2.md, ...)
- Summary file (e.g., doc.summary.md)
- Metadata files (if separate)
```

### Step 2: First Impression

**Quick assessment:**
- Does extraction look complete at first glance?
- Obvious missing content?
- Formatting preserved?
- Any immediate red flags (hallucinations, wrong language, etc.)?

**Document quick notes** before detailed verification.

### Step 3: Systematic Verification

Work through each quality dimension (detailed below).

### Step 4: Score and Document

Use scoring template and document all findings.

### Step 5: Save Results

Save incrementally to verification_results.json.

---

## Quality Dimension 1: Metadata Accuracy

**Purpose:** Verify that structured metadata fields are correctly extracted.

### Checklist

- [ ] **Date:** Exactly matches source (format may differ, but date must be identical)
  - Check: Day, month, year all correct?
  - Watch for: Date format confusion (MM/DD vs DD/MM)
  - Score 0 if wrong, 10 if perfect

- [ ] **Document Title/Name:** Correctly extracted
  - Check: Title exactly as appears in source?
  - Acceptable: Minor case differences (all caps vs. title case)
  - Not acceptable: Different words, missing words

- [ ] **Category/Type:** Appropriate classification
  - Check: Is document correctly categorized?
  - Examples: imaging, ultrasound, endoscopy, other
  - Note if classification is ambiguous

- [ ] **Facility/Institution:** Correctly extracted
  - Check: Exact name match (including accents, abbreviations)
  - Watch for: OCR errors in institution names
  - Note: Sometimes appears in header or footer

- [ ] **Doctor/Provider Name:** Correctly extracted
  - Check: Full name with accents preserved
  - Watch for: Title handling (Dr., Prof., etc.)
  - Multiple doctors: All captured?

- [ ] **Department/Specialty:** Correctly extracted (if applicable)
  - Check: Department name matches source
  - Note if specialty is implied vs. explicit

- [ ] **Other Domain-Specific Fields:** Verify all metadata
  - Medical: Patient age, exam type, equipment used
  - Legal: Case number, parties, jurisdiction
  - Financial: Account numbers, transaction dates
  - Technical: Version numbers, system IDs

### Scoring Rubric

**10 points:** All metadata fields perfect
**9 points:** One minor issue (e.g., missing period in abbreviation)
**8 points:** One field slightly wrong (e.g., partial facility name)
**7 points:** Two fields with minor issues
**5-6 points:** One field significantly wrong or multiple minor issues
**3-4 points:** Multiple fields wrong
**0-2 points:** Critical metadata wrong (date, primary identifier)

### Common Issues

- ❌ Date format confusion (2024-01-15 vs 2024-15-01)
- ❌ Accent loss in facility names (São Paulo → Sao Paulo)
- ❌ Title included in doctor name (Dr. included or excluded inconsistently)
- ❌ Abbreviated vs. full facility names
- ❌ Missing department/specialty information

---

## Quality Dimension 2: Transcription Quality

**Purpose:** Verify that visible text is completely and accurately transcribed.

### 2A: Completeness (Score 0-10)

**Question:** Is all visible text captured?

**Checklist:**
- [ ] **Headers:** All header text included?
- [ ] **Body text:** All paragraphs, sentences captured?
- [ ] **Lists:** All list items included?
- [ ] **Tables:** All table content captured? (structure may vary)
- [ ] **Footers:** Footer text included (contact info, page numbers)?
- [ ] **Marginal notes:** Annotations or side notes captured?
- [ ] **Signatures:** Noted appropriately (e.g., [signature], not transcribed)
- [ ] **Stamps/Seals:** Described or noted if relevant

**Scoring:**
- **10:** 100% of text captured
- **9:** 1-2% missing (insignificant footer text)
- **8:** 3-5% missing (minor paragraph omitted)
- **7:** 6-10% missing
- **5-6:** 11-20% missing
- **3-4:** 21-50% missing
- **0-2:** >50% missing

**Common issues:**
- ❌ Footer contact information omitted
- ❌ Marginal notes or annotations missed
- ❌ Second column of two-column layout missed
- ❌ Content on image-heavy pages omitted
- ❌ Faint or low-contrast text not captured

### 2B: Accuracy (Score 0-10)

**Question:** Does transcribed text match source exactly?

**Checklist:**
- [ ] **Word accuracy:** Words spelled correctly?
- [ ] **Number accuracy:** Numbers exactly match (critical!)?
- [ ] **Punctuation:** Periods, commas preserved?
- [ ] **Capitalization:** Case generally preserved?
- [ ] **Special characters:** Accents, symbols correct?
- [ ] **Abbreviations:** Preserved as-is or expanded appropriately?
- [ ] **Line breaks:** Preserved where semantically important?
- [ ] **Hyphenation:** End-of-line hyphens handled correctly?

**Scoring:**
- **10:** Zero transcription errors
- **9:** 1-2 minor errors (capitalization, punctuation)
- **8:** 3-5 minor errors or 1 word error
- **7:** Several word errors or number error (non-critical)
- **5-6:** Multiple word errors
- **3-4:** Frequent errors, some comprehension affected
- **0-2:** Pervasive errors, severely affects meaning

**Critical errors** (automatic score ≤5):
- ❌ Numbers wrong (measurements, dates, values)
- ❌ Medical/legal/financial terms wrong
- ❌ Negation errors (adding/removing "not", "no")
- ❌ Hallucinated content not in source

**Acceptable variations:**
- ✓ Capitalization differences if non-semantic (TITLE vs Title)
- ✓ Spacing variations (ManopH vs Mano pH)
- ✓ Expanded abbreviations if clear (Dr. → Doctor)

### 2C: Layout Preservation (Score 0-10)

**Question:** Is document structure and formatting preserved?

**Checklist:**
- [ ] **Paragraphs:** Paragraph breaks preserved?
- [ ] **Sections:** Section headings identified?
- [ ] **Lists:** Bulleted/numbered lists formatted as lists?
- [ ] **Tables:** Table content organized (markdown table or structured)?
- [ ] **Spacing:** Significant spacing preserved (e.g., between sections)?
- [ ] **Emphasis:** Bold, italic, underline noted if semantic?
- [ ] **Columns:** Multi-column layouts handled?
- [ ] **Headers/Footers:** Identified as such?

**Scoring:**
- **10:** Perfect layout preservation
- **9:** Minor spacing variations
- **8:** One structural element slightly off (list as paragraph)
- **7:** Multiple minor layout issues
- **5-6:** Significant layout loss (table as flat text)
- **3-4:** Most structure lost
- **0-2:** All formatting lost, unreadable

**Common issues:**
- ❌ Tables converted to flat text without structure
- ❌ Multi-column content merged incorrectly
- ❌ List items run together in paragraph
- ❌ Section breaks not preserved
- ❌ Header/footer mixed into body text

### 2D: Overall Transcription Score

**Calculate:** Average of Completeness, Accuracy, Layout scores

**Example:**
- Completeness: 10/10
- Accuracy: 9/10
- Layout: 9/10
- **Overall: 9.3/10**

---

## Quality Dimension 3: Domain-Specific Terminology

**Purpose:** Verify accuracy of specialized terminology.

### General Checklist

- [ ] **Technical terms:** Domain vocabulary correct?
- [ ] **Measurements:** Values with units preserved (15 mm, 10 Hz, $1,000)?
- [ ] **Special characters:** Accents, subscripts, superscripts?
- [ ] **Abbreviations:** Handled correctly?
- [ ] **Proper nouns:** Names, locations, brands correct?
- [ ] **Formulas:** Mathematical or chemical formulas accurate?

### Rating Scale

**Excellent (★★★★★):**
- Zero terminology errors
- All accents/special characters preserved
- Measurements with units correct
- Abbreviations appropriate

**Good (★★★★):**
- 1-2 minor terminology issues
- Accents mostly preserved (1 missing)
- Measurements correct

**Fair (★★★):**
- Several terminology errors
- Some accent loss
- One measurement error (non-critical)

**Poor (★★):**
- Frequent terminology errors
- Systematic accent loss
- Multiple measurement errors
- Affects comprehension

### Domain-Specific Guides

**See domain-specific guides for detailed verification:**
- **Medical:** `medical_terminology_guide.md`
- **Legal:** Create `legal_terminology_guide.md`
- **Financial:** Create `financial_terminology_guide.md`
- **Scientific:** Create `scientific_terminology_guide.md`
- **Technical:** Create `technical_terminology_guide.md`

### Common Issues Across Domains

- ❌ Accent loss (crítico → critico)
- ❌ Units separated from numbers (15mm → 15 mm acceptable, 15 → wrong)
- ❌ Abbreviations expanded incorrectly
- ❌ Technical jargon misspelled
- ❌ Proper nouns with spelling errors

---

## Quality Dimension 4: Summary Quality

**Purpose:** Verify that summaries accurately capture key information.

### Checklist

- [ ] **Completeness:** All key findings included?
  - Critical findings: All present?
  - Supporting details: Included appropriately?
  - Context: Sufficient background?

- [ ] **Accuracy:** No hallucinations or errors?
  - Information matches source?
  - No added details not in source?
  - No contradictions?

- [ ] **Appropriate Detail Level:**
  - Not too brief (missing important info)?
  - Not too verbose (excessive detail)?
  - Balanced summary?

- [ ] **Structure:**
  - Logical organization?
  - Clear narrative flow?
  - Sections/headings if appropriate?

- [ ] **Language:**
  - Clear, professional language?
  - Appropriate technical vocabulary?
  - Correct grammar?

- [ ] **De-identification** (if applicable):
  - Patient/client names removed?
  - Dates preserved (clinically/legally relevant)?
  - Facility/provider names removed if required?

### Scoring Rubric

**10 points:** Perfect summary
- All key information included
- Zero errors or hallucinations
- Appropriate detail level
- Well-structured and clear

**9 points:** Excellent summary
- One negligible omission
- Otherwise perfect

**8 points:** Very good summary
- One minor omission or slight verbosity
- No errors

**7 points:** Good summary
- Missing one moderately important detail
- Or slightly too brief/verbose

**5-6 points:** Fair summary
- Missing multiple important details
- Or one factual error (non-critical)

**3-4 points:** Poor summary
- Missing critical information
- Or factual errors

**0-2 points:** Failing summary
- Hallucinations (information not in source)
- Critical errors
- Incomprehensible

### Common Issues

- ❌ Hallucinated details not in source
- ❌ Missing critical findings
- ❌ Too brief, lacks necessary context
- ❌ Too verbose, buries key findings
- ❌ Wrong interpretation of findings
- ❌ Patient names not removed (de-identification failure)

---

## Quality Dimension 5: Multi-Page Coherence

**Purpose:** Verify consistency across multi-page documents.

**Note:** Only applicable to documents with multiple pages.

### Checklist

- [ ] **Metadata Consistency:**
  - Date identical across all pages?
  - Doctor name identical?
  - Facility name identical?
  - Other metadata consistent?

- [ ] **Page Numbering:**
  - Pages correctly numbered (1, 2, 3, ...)?
  - No gaps or duplicates?
  - Matches actual page count?

- [ ] **Content Continuity:**
  - No duplicate paragraphs across pages?
  - Content flows logically?
  - Cross-page references preserved?

- [ ] **Summary Integration:**
  - Summary integrates findings from all pages?
  - Page-specific information included?
  - No content from one page dominates unfairly?

### Scoring Rubric

**10 points:** Perfect coherence
- All metadata identical across pages
- Page numbering perfect
- No duplicate content
- Summary integrates all pages

**9 points:** One negligible inconsistency

**8 points:** One minor inconsistency (case difference in name)

**7 points:** Two minor inconsistencies

**5-6 points:** Multiple inconsistencies or one significant issue

**3-4 points:** Major coherence problems

**0-2 points:** Severe fragmentation, pages appear unrelated

### Common Issues

- ❌ Metadata varies across pages (different dates, doctor names)
- ❌ Page numbering wrong (1, 1, 2, ... or 1, 3, 4, ...)
- ❌ Duplicate paragraphs on multiple pages
- ❌ Summary only reflects first page, ignores others
- ❌ Pages appear to be from different documents

---

## Special Case: Low Confidence Investigation

**For documents tagged LOW_CONF:** Investigate root cause of low confidence.

### Investigation Steps

1. **Identify trigger:** Why is confidence low?
   - Image-heavy pages?
   - Handwritten content?
   - Complex layout?
   - Poor scan quality?
   - Very long document?

2. **Assess justification:** Is low confidence appropriate?
   - If image-heavy: Expected (uncertainty about visual content)
   - If handwritten: Expected (interpretation ambiguity)
   - If poor scan: Expected (OCR uncertainty)
   - If none of above: Investigate further

3. **Evaluate quality despite low confidence:**
   - Is extraction still accurate?
   - Are uncertainties handled appropriately?
   - Would a human struggle too?

4. **Document findings:**
   - Root cause identified?
   - Low confidence justified?
   - Extraction quality acceptable?
   - Is this a false positive (low conf, high quality)?

### Common Root Causes

**Legitimate (justified low confidence):**
- ✓ Endoscopy images (6+ photos with minimal text)
- ✓ Handwritten prescriptions (illegible handwriting)
- ✓ Faded/low-quality scans (hard to read)
- ✓ Mixed content types (text + charts + images)
- ✓ Very complex multi-page documents (45+ pages)

**Investigate further (potentially unjustified):**
- ⚠️ Standard typed text flagged as low confidence
- ⚠️ High-quality modern document flagged low
- ⚠️ Simple 1-page document flagged low

---

## Special Case: Complex Documents

**For documents tagged COMPLEX (10+ pages):** Additional checks.

### Checklist

- [ ] **Sampling pages:** Verify beginning, middle, end pages
  - First page: Title, metadata correct?
  - Middle pages: Content consistent?
  - Last page: Conclusions, signatures captured?

- [ ] **Page count:** Matches source exactly?

- [ ] **Content types:** Different content types handled?
  - Text pages: Transcribed well?
  - Image pages: Noted appropriately?
  - Chart/graph pages: Described or noted?
  - Table pages: Structure preserved?

- [ ] **Cross-references:** Page references preserved?
  - "See page 5" → noted correctly?

- [ ] **Summary comprehensiveness:** Integrates entire document?

### Scoring

Use standard rubrics above, but pay special attention to:
- Metadata consistency (most critical for complex docs)
- Summary integration (must cover all pages)
- Page numbering accuracy

---

## Results Documentation Template

Use this template for each verified document:

```json
{
  "doc_stem": "document_name",
  "profile": "profile_name",
  "page_count": 3,
  "min_confidence": 0.85,
  "category": "imaging",
  "tags": ["MULTI_PAGE", "CAT_IMAGING"],
  "sample_reason": "MULTI_PAGE (3-9 pages)",

  "verification": {
    "metadata_accuracy": {
      "score": 10,
      "issues": []
    },
    "transcription_quality": {
      "completeness_score": 10,
      "accuracy_score": 9,
      "layout_preservation_score": 9,
      "overall_score": 9.3,
      "issues": ["Minor spacing variation in one paragraph"]
    },
    "domain_terminology": {
      "rating": "Excellent",
      "issues": []
    },
    "summary_quality": {
      "score": 10,
      "issues": []
    },
    "multi_page_coherence": {
      "score": 10,
      "issues": []
    },
    "overall_assessment": "Excellent",
    "notable_issues": [],
    "recommendations": [],
    "verified_date": "2026-01-21"
  }
}
```

---

## Tips for Efficient Verification

**1. Batch similar documents:**
- Verify all endoscopy reports together
- Verify all prescriptions together
- Reduces context switching

**2. Use keyboard shortcuts:**
- Quickly navigate between source and extraction files
- Use split-screen viewing

**3. Take breaks:**
- Verification is mentally intensive
- Break every 5-7 documents
- Maintain quality of assessment

**4. Document as you go:**
- Don't wait until end to record findings
- Note issues immediately
- Save incrementally

**5. Spot-check vs. exhaustive:**
- For very long documents, spot-check representative pages
- Focus on high-risk areas (headers, numbers, technical terms)

**6. Trust your judgment:**
- If something looks wrong, investigate
- Note uncertainties
- Flag for re-review if needed

---

## Troubleshooting

**Issue:** Source document not readable
- Try adjusting zoom/contrast
- Request higher resolution version
- Document issue, skip document if necessary

**Issue:** Extraction format unclear
- Consult extraction pipeline documentation
- Ask about format conventions
- Document format questions

**Issue:** Unable to assess domain terminology
- Consult domain expert
- Use domain-specific guide
- Mark as "requires expert review"

**Issue:** Verification taking too long
- Focus on most critical dimensions first
- Use spot-checking for very long documents
- Set time limit per document (15 min max)

---

## Version History

- **v1.0** (2026-01-21): Initial checklist based on medical-exams-parser quality investigation
