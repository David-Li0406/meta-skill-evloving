---
name: intelligence-source-grading
description: Apply formal intelligence tradecraft to business data systems. Separate source reliability from information credibility, handle uncertainty explicitly, and communicate confidence appropriately. Covers the Admiralty Code, confidence frameworks, and signal triangulation.
---

# Intelligence Source Grading

Apply formal intelligence tradecraft to business data systems. Separate source reliability from information credibility, handle uncertainty explicitly, and communicate confidence appropriately.

## Core Principle

Never treat all data as epistemologically equal. A verified government contract and an unverified job posting require different handling in scoring algorithms.

**Always separate three layers:**
1. **Source reliability (A-F)** — historical trustworthiness of the provider
2. **Information credibility (1-6)** — believability of this specific claim
3. **Analytical confidence** — soundness of your final judgment

## Quick Reference: The Admiralty Code

Combine source grade (letter) with credibility grade (number) to form codes like `B2` or `C3`.

### Source Reliability (A-F)

| Grade | Meaning | Business Examples |
|-------|---------|-------------------|
| **A** | Completely Reliable | Government filings, ERP/payment APIs, signed contracts |
| **B** | Usually Reliable | Premium data vendors (D&B, ZoomInfo), reputable news, corporate websites |
| **C** | Fairly Reliable | CRM data (rep-entered), LinkedIn profiles, trade publications |
| **D** | Not Usually Reliable | Job aggregators, unverified reviews, general web scraping |
| **E** | Unreliable | Lead farms, known disinformation, clickbait content |
| **F** | Cannot Be Judged | New sources with no track record (not "bad" — unknown) |

### Information Credibility (1-6)

| Grade | Meaning | Business Application |
|-------|---------|---------------------|
| **1** | Confirmed | Corroborated by 2+ independent sources |
| **2** | Probably True | Logical, consistent with known context, unconfirmed |
| **3** | Possibly True | Plausible but lacks corroboration |
| **4** | Doubtful | Possible but illogical or unsupported |
| **5** | Improbable | Contradicted by other information |
| **6** | Cannot Be Judged | No basis for evaluation |

**Important:** `F` and `6` mean "unknown," not "bad."

## Lead Scoring Weight Matrix

| Code | Interpretation | Weight | Action |
|------|---------------|--------|--------|
| A1 | Confirmed Fact | 1.0 | High-priority alert |
| B1/A2 | High Confidence | 0.9 | Push to CRM |
| B2/C1 | Actionable Intel | 0.75 | Pipeline + verification |
| C3 | Weak Signal | 0.4 | Watchlist only |
| D4/E5 | Noise/Conflict | 0.0 or negative | Suppress |
| F6 | Unknown | 0.0 (neutral) | Sandbox for pattern matching |

## Confidence Framework

Display two separate outputs for each assessment:

### Probability (Likelihood)

| Term | Probability |
|------|-------------|
| Remote Chance | ≤5% |
| Highly Unlikely | 10-20% |
| Unlikely | 25-35% |
| Realistic Possibility | 40-50% |
| Likely / Probable | 55-75% |
| Highly Likely | 80-90% |
| Almost Certain | ≥95% |

### Analytical Confidence (High/Moderate/Low)

**High:** Multiple Grade A/B sources, minimal conflict, stable topic
**Moderate:** Credible sources but limited corroboration or some bias risk
**Low:** Single source, Grade D/E quality, high conflict, or volatile situation

**Critical rule:** Never combine probability and confidence in the same sentence.

✅ "It is *likely* Account X is entering a buying cycle. We have *moderate confidence* based on hiring signals and procurement activity."

❌ "We are highly confident this is likely to happen."

## Signal Triangulation

### Corroboration vs. Repetition

**Corroboration:** Independent collection paths converge on the same fact
**Repetition:** Same claim copied across dependent sources (not confirmation)

Ten news articles citing one press release = 1 signal, not 10.

### The Rule of Threes

Signals corroborated across **three different categories** achieve Grade 1:
- HUMINT: CRM notes, conversations, social media
- TECHINT: DNS, technographics, product usage
- OSINT: Press, news, job boards
- FININT: Filings, funding, procurement

Signals corroborated within one category achieve Grade 2 at best.

### Handling Contradictions

When signals conflict (e.g., "hiring aggressively" + "layoff announcement"), do not average to neutral. Flag as divergence requiring investigation.

Display: "Market Divergence Detected. Manual Review Recommended."

## Implementation Checklist

**Data Model:** Store each signal as an Observation with:
- Source type + instance
- Original URL/reference
- Timestamp + observed_at
- A-F reliability grade
- 1-6 credibility grade
- Independence cluster ID (for deduplication)

**Scoring Engine:**
- Convert grades to weights
- Apply recency decay
- Discount duplicate sources (don't stack linearly)
- Apply conflict penalty
- Output: score, likelihood term, confidence level

**New Source Handling (The "F" Protocol):**
1. Tag as F6 initially
2. Zero-trust weighting (neutral, not negative)
3. Shadow score in background
4. Graduate to C/B after N validated signals
