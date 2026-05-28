# Accuracy Checker - Expanded Reference

The Accuracy Checker prevents factual errors that damage credibility. A single wrong date or misquote can undermine an entire piece.

## Core Principle

Every verifiable claim must trace back to a source in the compiled sources file. If it can't be verified, it gets cut or softened.

---

## What Gets Checked

### Hard Facts (Zero Tolerance)

| Category | Examples | Verification |
|----------|----------|--------------|
| **Dates** | Birth/death years, publication years, founding dates | Cross-reference 2+ sources |
| **Names** | Full names, titles, institutional affiliations | Exact spelling from primary source |
| **Numbers** | Statistics, percentages, counts | Original source citation |
| **Locations** | Cities, schools, institutions | Primary source confirmation |
| **Titles** | Book titles, job titles, degree titles | Verbatim from source |

### Quotes (Verbatim or Don't Use)

| Check | Action |
|-------|--------|
| Direct quote | Must match source exactly, including punctuation |
| Paraphrase | Must preserve original meaning |
| Context | Quote must represent source's actual position |
| Attribution | Correct person, correct source |

### Timeline Integrity

Events must occur in the correct order. Common errors:

- "After X happened, he did Y" (verify X actually preceded Y)
- "In the 1970s, she..." (verify the decade is correct)
- Career progressions (did they really do A before B?)

---

## Verification Protocol

### Step 1: Flag All Verifiable Claims

Read through the draft and highlight every:
- Date or year
- Number or statistic
- Direct quote
- Named person
- Named institution or place
- Causal claim ("X led to Y")
- Historical sequence

### Step 2: Check Against Sources

For each flagged item:

1. Find the claim in compiled sources
2. Verify exact match
3. If no source exists: mark as UNVERIFIED

### Step 3: Handle Unverified Claims

Options for unverified claims:

| Option | When to Use | Example |
|--------|-------------|---------|
| **Cut it** | Claim is decorative | "He was known as the most..." |
| **Soften it** | Claim is useful but unverified | "reported to have" → "said to have" |
| **Source it** | Claim is essential | Do additional research |
| **Generalize it** | Specifics are wrong | "in 1952" → "in the early 1950s" |

---

## Common Accuracy Pitfalls

### 1. AI Hallucinations

AI confidently invents details that sound plausible:

- Specific ages at life events
- Exact years for vague periods
- Publication details for books
- Degree specifics and universities

**Fix:** Verify every specific. AI-generated content is especially prone to confident fabrication.

### 2. Secondary Source Drift

Information gets distorted when passed through sources:

- Wikipedia cites a blog that cites an interview → check original interview
- "According to sources" → which sources specifically?

**Fix:** Trace claims to primary sources when possible.

### 3. Compound Errors

One wrong fact can cascade:

- Wrong birth year → wrong age at career milestone
- Wrong school name → wrong city → wrong context

**Fix:** Catch errors early; don't propagate them.

### 4. Quote Frankenstein

Combining pieces of different quotes:

- "He said 'X' and also mentioned that 'Y'" (were these said together?)
- Ellipsis abuse hiding contradictory middle sections

**Fix:** Only cut from quotes if meaning is preserved.

---

## Before/After Examples

### Example 1: Vague Claim Made Specific

**Flagged:** "Gatto was in his fifties when he resigned"

**Source says:** "Resigned in 1991" but birth year isn't confirmed

**Fix:** "After nearly 30 years in the classroom, Gatto resigned in 1991"

---

### Example 2: Unverifiable Detail Cut

**Flagged:** "His 400-page investigation detailed..."

**Source says:** Mentions the essay exists, no page count

**Fix:** "His sprawling investigation detailed..."

---

### Example 3: Quote Context Preserved

**Flagged:** "Schools are designed to produce employees, not thinkers"

**Source says:** This was said about a specific type of schooling, not all schools

**Fix:** "The Prussian model, he argued, was 'designed to produce employees, not thinkers'"

---

## Verdict Criteria

### PASS Requirements

- [ ] All dates verified against sources
- [ ] All names spelled correctly
- [ ] All quotes verbatim from source
- [ ] All statistics have citations
- [ ] Timeline events in correct order
- [ ] No claims that can't be traced to sources

### FAIL Triggers

- Any verifiably wrong fact
- Any misquote
- Any unverified specific claim presented as fact
- Any timeline error

### Verdict Format

```
ACCURACY CHECKER VERDICT: [PASS/FAIL]

[If FAIL:]
ISSUES FOUND:
1. Line [X]: "[claim]" - [problem] - Fix: [solution]
2. Line [X]: "[claim]" - [problem] - Fix: [solution]

[If PASS:]
All claims verified against compiled sources.
```

---

## Quick Reference: Red Flags

Phrases that often signal unverified claims:

- "was known as" / "was considered"
- Specific ages: "at age 30"
- Round numbers: "over 100,000 students"
- Superlatives: "the first," "the most," "the only"
- Causal claims: "which led to," "resulting in"

When you see these, verify extra carefully.
