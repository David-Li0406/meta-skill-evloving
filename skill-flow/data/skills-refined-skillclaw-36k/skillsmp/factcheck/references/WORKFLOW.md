# Fact-Check Workflow Reference

Detailed reference for the `/factcheck` skill. Claude Code handles claim extraction and counter-argument generation directly - the helper script only handles DeepCitation API calls.

## Complete Workflow

```
User provides: LLM output + source files
                    ↓
Step 0: Upload source files (helper script)
                    ↓
Step 1: Extract claims (Claude does this)
                    ↓
Step 2: Verify claims (helper script)
                    ↓
Step 3: Generate counter-arguments (Claude does this)
                    ↓
Step 4: Search for counter-evidence (helper script)
                    ↓
Step 5: Calculate confidence & report (Claude does this)
```

## Helper Script Usage

The `scripts/factcheck.ts` helper handles DeepCitation API calls:

```bash
# Upload source files
bun run scripts/factcheck.ts upload ./report.pdf ./data.xlsx

# Output:
# Uploaded files:
#   report.pdf: abc123xyz...
#   data.xlsx: def456uvw...

# Verify claims against a source
bun run scripts/factcheck.ts verify <attachmentId> '{"claim-1": {"fullPhrase": "revenue grew 45%", "keySpan": "45%"}}'
```

## Step 0: Upload Source Files

Run the helper script to upload files:

```bash
bun run scripts/factcheck.ts upload ./report.pdf ./chart.png
```

This returns attachment IDs for each file. Save these for verification steps.

## Step 1: Claim Extraction (Claude does this)

Analyze the LLM output and identify factual claims. For each claim:

1. **Quote the exact text** making the claim
2. **Classify the type**:
   - QUANTITATIVE: numbers, statistics, measurements
   - QUALITATIVE: descriptions, assessments
   - CAUSAL: cause-effect relationships
   - TEMPORAL: time-related assertions
3. **Extract key span**: 1-3 most important words (numbers, proper nouns, key metrics)
4. **Note existing citations** if present (e.g., `[1]`, `[2]`)

### Key Span Selection

Good key spans for verification:
- Numbers and percentages: "45%", "2024", "$1.2B"
- Proper nouns: "Microsoft", "Q3"
- Specific metrics: "revenue", "market share"

Example:
- Claim: "Revenue grew 45% year-over-year in Q3 2024"
- Key span: "45% Q3 2024"

## Step 2: Verify Claims

Use the helper script to verify each claim:

```bash
bun run scripts/factcheck.ts verify abc123xyz '{
  "claim-1": {"fullPhrase": "Revenue grew 45% year-over-year in Q3 2024", "keySpan": "45% Q3"},
  "claim-2": {"fullPhrase": "The company expanded into three new markets", "keySpan": "three new markets"}
}'
```

### Interpreting Results

| Status | Meaning |
|--------|---------|
| `found` | Exact text found in source |
| `found_key_span_only` | Key phrase found |
| `found_on_other_page` | Found but different location |
| `partial_text_found` | Only part matched |
| `not_found` | Text not in source |

## Step 3: Counter-Argument Generation (Claude does this)

For each claim, think adversarially:

**Ask yourself:**
- What alternative explanations exist for this data?
- What confounding factors could affect this?
- What context might be missing?
- What would weaken this claim if true?

**Generate 2-3 counter-arguments with search phrases:**

Example for "Revenue grew 45%":
1. "Growth from one-time acquisition" → search: "acquisition acquired merger"
2. "Prior year was unusually low" → search: "prior year decline challenges"
3. "Currency effects inflated numbers" → search: "currency exchange rate impact"

### Counter-Argument Types

| Type | Description | Search for |
|------|-------------|------------|
| Alternative Cause | Different explanation | acquisition, merger, one-time |
| Confounding Factor | Hidden variable | currency, seasonal, adjustment |
| Missing Context | Omitted information | excluding, discontinued, restated |
| Methodology | Measurement issues | definition, calculated, methodology |
| Temporal | Time-based issues | prior year, seasonal, temporary |

## Step 4: Search for Counter-Evidence

Use the helper script to search for counter-argument evidence:

```bash
bun run scripts/factcheck.ts verify abc123xyz '{
  "counter-1a": {"fullPhrase": "acquisition acquired merger", "keySpan": "acquisition"},
  "counter-1b": {"fullPhrase": "prior year decline challenges", "keySpan": "decline"}
}'
```

If counter-evidence is found, it weakens the original claim.

## Step 5: Confidence Scoring (Claude does this)

Calculate a confidence score for each claim:

**Start with 50 points, then:**

| Factor | Points |
|--------|--------|
| Claim fully verified | +40 |
| Claim partially verified | +20 |
| Claim not found | -20 |
| Counter-evidence found | -15 each |
| Counter-evidence NOT found | +5 each |
| Had existing citation | +10 |

**Clamp final score to 0-100.**

### Confidence Levels

| Score Range | Level | Interpretation |
|-------------|-------|----------------|
| 70-100 | HIGH | Claim is well-supported with minimal contradicting evidence |
| 40-69 | MEDIUM | Claim has some support but also potential weaknesses |
| 0-39 | LOW | Claim lacks support or has significant contradicting evidence |

## Verification Status Mapping

| DeepCitation Status | Category | Description |
|---------------------|----------|-------------|
| `found` | Fully Verified | Exact text found in source |
| `found_key_span_only` | Fully Verified | Key phrase found |
| `found_phrase_missed_value` | Fully Verified | Phrase found, value differs |
| `found_on_other_page` | Partial Match | Found on different page than claimed |
| `found_on_other_line` | Partial Match | Found on different line than claimed |
| `partial_text_found` | Partial Match | Only part of text found |
| `first_word_found` | Partial Match | Only first word matched |
| `not_found` | Not Found | Text not in source document |
| `pending` / `loading` | Pending | Verification in progress |

## Report Generation

### Terminal Output Format

```
=== FACT-CHECK REPORT ===

Source Files:
├── report.pdf (attachmentId: abc123...)
├── data.xlsx (attachmentId: def456...)
└── chart.png (attachmentId: ghi789...)

CLAIM 1: "Revenue grew 45% year-over-year in Q3 2024"
├── Type: QUANTITATIVE | Verifiability: HIGH
├── Verification: VERIFIED
│   └── Found in: report.pdf, page 2, lines 12-14
│   └── Match: "...revenue increased 45% compared to Q3 2023..."
├── Counter-Arguments:
│   ├── "Growth from one-time acquisition"
│   │   └── Evidence: NOT FOUND
│   └── "Low prior year baseline"
│       └── Evidence: PARTIAL MATCH
│       └── Found in: report.pdf, page 5
│       └── Match: "...challenging market conditions in 2023..."
└── Confidence: MEDIUM (55/100)

=== SUMMARY ===
Total Claims: 5
Verified: 3 (60%)
Partially Verified: 1 (20%)
Unsupported: 1 (20%)
Counter-Evidence Found: 2 claims
Overall Confidence: MEDIUM
```

### Status Icons

| Status | Icon | Color |
|--------|------|-------|
| Verified | `✅` | Green |
| Partial Match | `⚠️` | Amber |
| Not Found | `❌` | Red |
| Pending | `⏳` | Gray |
