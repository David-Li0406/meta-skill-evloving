---
name: factcheck
description: Adversarial fact-checking and verification of LLM output against uploaded attachments using DeepCitation. Use when you need to verify claims, find contradictions, or perform devil's advocate analysis on AI-generated content.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(node:*, bun:*, npx:*)
---

# Fact-Check Skill

Perform adversarial verification of LLM-generated content against uploaded attachments using DeepCitation.

## When to Use

- Verify claims in an AI response against attachments
- Find potential contradictions or unsupported statements
- Perform devil's advocate analysis
- Generate counter-arguments and check their evidence

## Arguments

- `--output <text|file>` - The LLM output text to fact-check, OR a file path containing the output
- `--sources <files...>` - Source files to verify against (PDF, images, documents)
- `--attachment-id <id>` - (Optional) Use existing DeepCitation attachment ID instead of uploading files

## Prerequisites

1. **DeepCitation API key** in environment (`DEEPCITATION_API_KEY`)

## Workflow

When executing this skill, follow these steps:

### Step 0: Upload Source Files
Read the source files and upload them to DeepCitation:
```typescript
const dc = new DeepCitation({ apiKey: process.env.DEEPCITATION_API_KEY });
const { fileDataParts } = await deepcitation.prepareFiles([
  { file: readFileSync(sourcePath), filename: basename(sourcePath) }
]);
const attachmentId = fileDataParts[0].attachmentId;
```

### Step 1: Extract Claims (You do this)
Analyze the LLM output and identify distinct factual claims:
- QUANTITATIVE claims (numbers, statistics)
- QUALITATIVE claims (descriptions, assessments)
- CAUSAL claims (cause-effect relationships)
- TEMPORAL claims (time-related assertions)

For each claim, note the exact text and extract a key span (1-3 important words).

### Step 2: Verify Claims
For each claim, use DeepCitation to verify against the sources:
```typescript
const result = await deepcitation.verify(attachmentId, {
  "claim-1": { fullPhrase: "exact claim text", keySpan: "key words" }
});
const status = getCitationStatus(result.verifications["claim-1"]);
```

### Step 3: Generate Counter-Arguments (You do this)
For each claim, think adversarially and generate 2-3 counter-arguments:
- Alternative explanations for the same data
- Potential confounding factors
- Missing context that could change interpretation
- What search phrases would find evidence for these counter-arguments?

### Step 4: Search for Counter-Evidence
For each counter-argument search phrase, verify against sources:
```typescript
const counterResult = await deepcitation.verify(attachmentId, {
  "counter-1": { fullPhrase: searchPhrase, keySpan: searchPhrase.split(" ").slice(0,2).join(" ") }
});
```

### Step 5: Calculate Confidence & Report
Score each claim based on verification status and counter-evidence found.

## Output Format

```
=== FACT-CHECK REPORT ===

CLAIM 1: "Revenue grew 45% year-over-year"
├── Verification: VERIFIED (found on page 2, lines 12-14)
├── Counter-Arguments:
│   ├── "Growth could be one-time acquisition effect"
│   │   └── Evidence: NOT FOUND
│   └── "Prior year may have been unusually low"
│       └── Evidence: PARTIAL MATCH (page 5)
└── Confidence: HIGH (85/100)

CLAIM 2: "Market share increased to 35%"
├── Verification: NOT FOUND
├── Counter-Arguments:
│   └── "Market definition may be narrow"
│       └── Evidence: FOUND (page 8, line 42)
└── Confidence: LOW (25/100)

=== SUMMARY ===
Total Claims: 5
Verified: 3 (60%)
Partially Verified: 1 (20%)
Unsupported: 1 (20%)
Counter-Evidence Found: 2 claims
```

## Confidence Scoring

| Factor | Score Impact |
|--------|--------------|
| Claim verified (exact) | +40 |
| Claim partially verified | +20 |
| Claim not found | -20 |
| Counter-evidence found | -15 per instance |
| Counter-evidence not found | +5 per instance |
| Has existing citation | +10 |

**Confidence Levels:**
- **HIGH**: 70-100 points
- **MEDIUM**: 40-69 points
- **LOW**: 0-39 points

## Quick Start

```bash
# Fact-check with source files (most common)
/factcheck --output ./llm-response.txt --sources ./report.pdf ./data.xlsx

# Fact-check inline text with source files
/factcheck --output "The company reported 45% revenue growth..." --sources ./annual-report.pdf

# With existing attachment ID (if already uploaded)
/factcheck --output ./response.txt --attachment-id abc123xyz

# Multiple source files
/factcheck --output ./summary.txt --sources ./doc1.pdf ./doc2.pdf ./chart.png
```

## Integration Details

Uses DeepCitation library exports:
- `DeepCitation.prepareFiles(files)` - Upload source files, returns attachmentIds
- `DeepCitation.verify(attachmentId, citations)` - Verify claims against sources
- `getAllCitationsFromLlmOutput(text)` - Parse existing citations from LLM output
- `getCitationStatus(verification)` - Interpret verification results

For detailed workflow and prompt templates, see [references/WORKFLOW.md](references/WORKFLOW.md).
