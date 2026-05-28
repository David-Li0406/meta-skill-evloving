---
name: isda
description: Irreducible Semantic Density Analysis - analyzes text compressibility by decomposing into five strata (structure, retrievable, derived, curatorial, novel). Use when asked to analyze text density, measure originality, check if something could be shorter, or assess semantic compression.
allowed-tools: Read, Glob, Grep
---

# Irreducible Semantic Density Analysis (ISDA)

Perform structured analysis estimating the compressibility of written content. Answer the question: *"How much of this text is genuinely necessary to convey its core intellectual contribution?"*

## Core Concept

ISDA measures **semantic Kolmogorov complexity**: the minimal description length required to reconstruct the *meaning* and *argumentative force* of a text, not its literal characters.

The core question: **Could this have been a tweet? A paragraph? Or does it genuinely require its current length?**

## The Five Strata

Decompose any text into these five strata:

| Stratum | Name | Description | Compressibility |
|---------|------|-------------|-----------------|
| S₁ | Structural Skeleton | Document architecture, templates, formatting | High |
| S₂ | Retrievable Knowledge | Facts, quotes, definitions from reference sources | Near-total (pointers) |
| S₃ | Derived Inferences | Standard analytical moves any practitioner would make | High |
| S₄ | Curatorial Decisions | Selection, arrangement, emphasis choices | Moderate |
| S₅ | Generative Novelty | Irreducible original content - the reason the text exists | Low/None |

## Analysis Protocol

### Step 1: Measure Raw Length
Count total bytes/characters of the text.

### Step 2: Create Stratum Ledger

```
| Stratum | Description | Raw Bytes | Compressed Estimate |
|---------|-------------|-----------|---------------------|
| S₁      |             |           |                     |
| S₂      |             |           |                     |
| S₃      |             |           |                     |
| S₄      |             |           |                     |
| S₅      |             |           |                     |
| TOTAL   |             |           |                     |
```

### Step 3-7: Encode Each Stratum

**S₁ (Structure):** Describe architecture in minimal notation
- Example: "5-part essay [Intro→Review→Methods→Results→Discussion]" ≈ 60 bytes

**S₂ (Retrievable):** Replace with minimal pointers
- `Smith.2019.p42` (14 bytes), `Gen.2.9` (7 bytes), `OED.sublime.n.2` (15 bytes)

**S₃ (Derived):** Encode as [method] + [input] → [output]
- `statistical_test(data, t-test) → significance` (40 bytes)

**S₄ (Curatorial):** Enumerate decisions with choice-space bits
- "Select 5 examples from 50" → log₂(C(50,5)) ≈ 22 bits
- "Order 6 sections non-obviously" → log₂(6!) ≈ 9.5 bits

**S₅ (Novel):** Extract verbatim - this is the irreducible core

### Step 8: Compute Metrics

**Semantic Compression Ratio (SCR):**
```
SCR = Raw_Bytes / (S₁ + S₂_compressed + S₃_compressed + S₄ + S₅)
```

**Novelty Density (ND):**
```
ND = S₅ / Raw_Bytes
```

**Retrievability Index (RI):**
```
RI = (S₂_raw + S₃_raw) / Raw_Bytes
```

**Could-Be-A-Tweet Test (CBAT):**
```
S₅ < 280 chars → YES | S₅ ≥ 280 chars → NO
```

## Interpretation Guide

### SCR (Semantic Compression Ratio)
| Value | Meaning |
|-------|---------|
| < 2 | Extremely dense, minimal elaboration |
| 2-5 | Well-developed, efficient |
| 5-10 | Expansive, could be condensed |
| 10-20 | Verbose, core buried in padding |
| > 20 | Severely bloated |

### ND (Novelty Density)
| Value | Meaning |
|-------|---------|
| > 0.20 | Highly original, groundbreaking |
| 0.10-0.20 | Strong original contribution |
| 0.05-0.10 | Solid synthesis with insights |
| 0.02-0.05 | Primarily synthesis/review |
| < 0.02 | Essentially derivative |

### RI (Retrievability Index)
| Value | Meaning |
|-------|---------|
| > 0.80 | Encyclopedic, review-like |
| 0.50-0.80 | Balanced sources + authorial contribution |
| 0.20-0.50 | Source-light, more argumentation |
| < 0.20 | Minimally sourced |

### CBAT
- **YES**: Core insight is compact; length serves elaboration
- **NO**: Argument inherently complex; compression loses essential content

## Output Template

Present analysis in this format:

```
## ISDA Analysis: [Title]

**Genre:** [type]
**Raw Length:** X bytes

### Stratum Breakdown

| Stratum | Content Summary | Raw | Compressed |
|---------|----------------|-----|------------|
| S₁ | [structure description] | X | X |
| S₂ | [X retrievable items] | X | X |
| S₃ | [X inferences] | X | X |
| S₄ | [X curatorial decisions] | X | X bits |
| S₅ | [novel elements] | X | X |

### Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| SCR | X | [assessment] |
| ND | X% | [assessment] |
| RI | X% | [assessment] |
| CBAT | YES/NO | [assessment] |

### Compression Potential

| Target | Content |
|--------|---------|
| Tweet (280c) | [thesis only] |
| Paragraph (500-800c) | [thesis + key insight + support] |
| Abstract (1500-2000c) | [above + example + conclusion] |

### Key Findings

[2-3 sentences on what the analysis reveals about this text]
```

## Genre Expectations

Different genres have different expected profiles:
- **Literature review**: High RI, low ND (appropriate)
- **Original research**: Moderate RI, higher ND (expected)
- **Opinion/essay**: Low RI, variable ND
- **Technical docs**: High RI, near-zero ND (appropriate)

## Caveats

1. S₄/S₅ boundary is somewhat subjective
2. Domain expertise improves accuracy
3. Rhetorical value not captured
4. What's "retrievable" depends on assumed knowledge base
