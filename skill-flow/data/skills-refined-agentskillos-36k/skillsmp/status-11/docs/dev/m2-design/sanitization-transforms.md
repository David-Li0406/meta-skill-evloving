# Sanitization Transforms for M2 Branch Validation

## Overview

**Sanitization transforms** are deterministic functions that modify branch content to fix violations or remove problematic elements. Unlike **policy rules** (which reject), sanitization transforms **modify** the proposal to make it acceptable.

**Philosophy**: Apply the smallest change necessary to fix a violation while preserving narrative intent and readability.

---

## Core Transforms

### 1. Profanity Redaction

**Goal**: Replace profane words with asterisks or placeholders.

**Input**:
```
"What the f*** is this? This s*** is unacceptable!"
```

**Output** (asterisk mode):
```
"What the *** is this? This **** is unacceptable!"
```

**Output** (placeholder mode):
```
"What the [expletive] is this? This [vulgarity] is unacceptable!"
```

**Algorithm**:
1. Tokenize text
2. For each token, check if it matches profanity list (case-insensitive, unicode-normalized)
3. Replace matching token with N asterisks (where N = token length) or placeholder
4. Reconstruct text

**Tuning parameters**:
- `mode` (enum): `asterisks` | `placeholder` | `mild_replacement`
  - `asterisks`: Replace with * (default, least immersive)
  - `placeholder`: Replace with `[expletive]` (more readable)
  - `mild_replacement`: Replace with mild synonym (most immersive, but harder to implement)
- `preserve_capitalization` (boolean): If true, maintain original case pattern

**Impact assessment**:
- Risk of unintended sanitization: Low (profanity list is curated)
- Readability after transform: Medium (asterisks are jarring; placeholders are better)
- Narrative coherence: Medium (reader may notice redaction, but plot is unaffected)

**Example transform**:
```json
{
  "rule_id": "profanity_filter",
  "transform_type": "profanity_redaction",
  "original_text": "What the f*** is this? This s*** is unacceptable!",
  "sanitized_text": "What the [expletive] is this? This [vulgarity] is unacceptable!",
  "violations_fixed": 2
}
```

---

### 2. Explicit Content Removal (Sentence-Level)

**Goal**: Remove sentences containing explicit sexual or graphic violent content.

**Input**:
```
He kissed her tenderly. They made passionate love all night, with detailed descriptions of... 
The next morning, he was gone.
```

**Output**:
```
He kissed her tenderly. The next morning, he was gone.
```

**Algorithm**:
1. Sentence-tokenize text using NLTK or similar
2. For each sentence, compute embedding or run keyword check
3. If sentence is flagged as explicit, mark for removal
4. Remove marked sentences
5. Smooth paragraph boundaries (remove double spaces, adjust capitalization)

**Tuning parameters**:
- `granularity` (enum): `sentence` | `paragraph`
  - `sentence`: Remove individual sentences (default, fine-grained)
  - `paragraph`: Remove entire paragraphs (coarser, preserves context)
- `explicit_threshold` (0.0–1.0): Confidence threshold for flagging as explicit

**Impact assessment**:
- Risk of unintended sanitization: Medium (might remove non-explicit sentences if false positive)
- Readability after transform: High (if boundaries are smooth)
- Narrative coherence: Medium (removed sentences might be plot-relevant)

**Example**:
```json
{
  "rule_id": "explicit_content_filter",
  "transform_type": "explicit_content_removal",
  "original_text": "He kissed her. They made love. Morning came.",
  "sanitized_text": "He kissed her. Morning came.",
  "sentences_removed": 1,
  "explanation": "Removed sexually explicit sentence"
}
```

---

### 3. HTML Tag Stripping

**Goal**: Remove disallowed HTML tags and attributes.

**Input**:
```html
He said <script>alert('xss')</script>hello <span onclick="evil()">there</span> <b>friend</b>.
```

**Output**:
```html
He said hello <span>there</span> <b>friend</b>.
```

**Algorithm**:
1. Parse HTML with a safe parser (e.g., BeautifulSoup with whitelist)
2. Define allowed tags (e.g., `<b>`, `<i>`, `<em>`, `<strong>`, safe `<span>`)
3. Iterate over parsed tree
4. Keep allowed tags; strip disallowed tags and all attributes
5. Reconstruct HTML

**Tuning parameters**:
- `allowed_tags` (array): Whitelist of safe tags
- `allowed_attributes` (object): Per-tag allowed attributes (e.g., `span: [class]`)
  - Example: `{"span": ["class"], "a": ["href"]}`
- `strip_or_escape` (enum): `strip` (remove tags) or `escape` (replace with entities)

**Allowed tags (default)**:
- Text formatting: `<b>`, `<i>`, `<em>`, `<strong>`, `<u>`, `<s>`
- Grouping: `<div>`, `<span>`, `<p>` (with `class` attribute only)
- Lists: `<ul>`, `<ol>`, `<li>`
- Line breaks: `<br>`

**Disallowed tags (default)**:
- Scripts: `<script>`, `<style>`, `<link>`
- Iframes: `<iframe>`, `<object>`, `<embed>`
- Event handlers: Any tag with `on*` attributes

**Impact assessment**:
- Risk of unintended sanitization: Low (whitelist is strict)
- Readability after transform: High (safe tags are preserved)
- Narrative coherence: High (formatting is preserved; no content removed)

---

### 4. Whitespace Normalization

**Goal**: Remove excessive whitespace and control characters.

**Input**:
```
Line 1



Line 2	with	tabs   and  extra  spaces
```

**Output**:
```
Line 1

Line 2 with tabs and extra spaces
```

**Algorithm**:
1. Replace all control characters (except \n, \r, \t) with spaces
2. Replace multiple tabs with single space
3. Replace multiple spaces with single space
4. Replace multiple newlines (3+) with double newline
5. Strip leading/trailing whitespace

**Tuning parameters**:
- `collapse_newlines` (boolean): If true, reduce 3+ newlines to 2
- `collapse_spaces` (boolean): If true, reduce 3+ spaces to 1
- `allow_tabs` (boolean): If true, preserve tabs; otherwise convert to spaces

**Impact assessment**:
- Risk of unintended sanitization: Very low (whitespace-only change)
- Readability after transform: High (normalizes formatting)
- Narrative coherence: None (no content change)

---

### 5. Character Encoding Normalization

**Goal**: Ensure valid UTF-8 encoding and normalize unicode.

**Input**:
```
"café" (using decomposed unicode, NFD form)
```

**Output**:
```
"café" (using composed unicode, NFC form)
```

**Algorithm**:
1. Detect encoding (assume UTF-8)
2. If invalid UTF-8 sequences, replace with replacement character (U+FFFD) or remove
3. Normalize unicode to NFC (Canonical Decomposition, Canonical Composition)
4. Reject if normalization fails (indicates corrupted input)

**Tuning parameters**:
- `normalization_form` (enum): `NFC` | `NFKC`
- `invalid_byte_handling` (enum): `replace` | `remove`

**Impact assessment**:
- Risk of unintended sanitization: Very low (encoding-only change)
- Readability after transform: None (normalized encoding is invisible)
- Narrative coherence: None (no content change)

---

### 6. Content Truncation (Length Limit)

**Goal**: If branch exceeds token limit, truncate to fit within limit while preserving narrative sense.

**Input** (600 tokens):
```
Long narrative text ... [continues for 600 tokens total] ...
```

**Output** (trimmed to 500 tokens):
```
Long narrative text ... [truncated at sentence boundary before 500th token] ...
```

**Algorithm**:
1. Tokenize text
2. If token count > limit, find last complete sentence before limit
3. Truncate at sentence boundary
4. Optionally append "[continued...]" or "[...]"

**Tuning parameters**:
- `max_tokens` (int): Hard limit
- `truncate_at_boundary` (enum): `sentence` | `paragraph` | `token`
- `append_marker` (boolean): If true, add "[...]" to indicate truncation

**Impact assessment**:
- Risk of unintended sanitization: Medium (might lose plot-relevant content)
- Readability after transform: High (if truncated at sentence boundary)
- Narrative coherence: Medium (ending may feel abrupt)

**Example**:
```json
{
  "rule_id": "length_limit_check",
  "transform_type": "content_truncation",
  "original_token_count": 650,
  "target_token_count": 500,
  "sanitized_token_count": 495,
  "truncation_point": "sentence boundary",
  "message": "Truncated to 495 tokens at last complete sentence"
}
```

---

### 7. Inconsistency Flagging (Non-Transform)

**Goal**: Flag contradictions with LORE but allow manual override (not auto-sanitized).

**Note**: This is **not a transform**—it's a **flag** that allows human review.

**Input**:
```
The compass was forged in 1920 by a master craftsman.
```

**LORE contradiction**:
```
compass_origin: "Lost expedition of 1847"
compass_creation_date: 1847
```

**Flag** (not sanitized):
```json
{
  "rule_id": "lore_consistency_check",
  "result": "warning",
  "severity": "high",
  "message": "Branch asserts compass was created in 1920, but LORE says 1847. Allow with manual review.",
  "recommendation": "manual_review"
}
```

---

## Transform Application Strategy

### When to Apply

Apply sanitization **only** if:
1. Violation is clear and unambiguous (e.g., profanity, disallowed HTML)
2. Transform does not alter narrative meaning (e.g., whitespace normalization)
3. Content violation is not critical (e.g., not a plot-critical sentence)

### When NOT to Apply

**Reject instead of sanitize** if:
1. Violation would leave nonsensical result (e.g., removing all dialogue)
2. Violation suggests author intent mismatch (e.g., LORE contradiction)
3. Violation indicates misunderstanding of story context (likely hallucination)

---

## Sanitization Pipeline Flow

```
Branch Proposal
    ↓
[1] Structural Checks (ink syntax, encoding)
    ↓ FAIL → Auto-Reject
    ↓ PASS
[2] Safety Checks (profanity, explicit content, hate speech)
    ↓ CRITICAL FAIL → Auto-Reject
    ↓ SANITIZABLE VIOLATION → Apply Transform
    ↓ PASS
[3] Coherence Checks (LORE, character, theme, pacing)
    ↓ HIGH FAIL → Flag for Manual Review
    ↓ PASS
[4] Path Validation (return path reachability)
    ↓ FAIL → Flag for Director Evaluation
    ↓ PASS
[5] Format Checks (length, HTML)
    ↓ SANITIZABLE VIOLATION → Apply Transform
    ↓ PASS
    ↓
Sanitized Proposal + Validation Report
    ↓
Director Evaluation
    ↓
Runtime Integration Decision
```

---

## Determinism Guarantee

**Critical requirement**: Sanitization must be deterministic.

```
sanitize(proposal, ruleset_v1.2) == sanitize(proposal, ruleset_v1.2)
```

**Implementation guidelines**:
- Use deterministic regex and parsing (no random sampling)
- Version all lists (profanity, LORE, character profiles)
- Document randomness: if any randomness is used (e.g., random replacement word), seed it explicitly

---

## Testing Sanitization Transforms

### Test Cases

For each transform, test:

1. **Happy path**: Sanitization fixes violation without breaking narrative
   ```
   Input: "He said what the f*** is this?"
   Output: "He said what the [expletive] is this?"
   Assertion: Output is grammatical, meaning preserved
   ```

2. **Edge case**: Multiple violations in same sentence
   ```
   Input: "What the f*** is this s***?"
   Output: "What the [expletive] is this [vulgarity]?"
   Assertion: Both violations fixed
   ```

3. **Over-sanitization**: Risk of breaking narrative
   ```
   Input: "Character's only line: 'Go f*** yourself.'"
   Output: "Character's only line: 'Go [expletive] yourself.'"
   Assertion: Character voice still comes through, but redaction noticed
   ```

4. **No false positives**: Non-violating content unchanged
   ```
   Input: "The café was lovely."
   Output: "The café was lovely."
   Assertion: Output == Input
   ```

---

## Example: Full Sanitization Report

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440101",
  "proposal_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "rejected_with_sanitization",
  "rules": [
    {
      "rule_id": "profanity_filter",
      "result": "sanitized",
      "severity": "critical",
      "message": "Found 2 profane words; sanitized with placeholders",
      "violations": [
        {
          "offset": 8,
          "text": "f***",
          "explanation": "Matches profanity list"
        }
      ],
      "sanitization_applied": {
        "original_text": "He said what the f*** is this s***?",
        "sanitized_text": "He said what the [expletive] is this [vulgarity]?",
        "transform_type": "profanity_redaction"
      }
    }
  ],
  "overall_risk_score": 0.75,
  "recommendation": "manual_review",
  "sanitized_proposal": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "content": {
      "text": "He said what the [expletive] is this [vulgarity]?",
      "length_tokens": 18
    }
  },
  "metadata": {
    "validation_time_ms": 145,
    "ruleset_version": "v1.2.0"
  }
}
```

---

## Monitoring & Iteration

### Metrics

- **Sanitization rate**: % of proposals requiring sanitization
- **Over-sanitization rate**: % of sanitized proposals that are still unreadable
- **Playtest feedback**: Do players notice redactions? Do they find sanitized branches immersive?

### Tuning Loop

1. **Phase 1**: Baseline sanitization with default params (profanity redaction, HTML stripping)
2. **Week 2 feedback**: Identify which transforms are too aggressive or too lenient
3. **Phase 2**: Refine transforms based on playtest feedback
4. **Post-launch**: Monitor player perception and adjust

---

## Future Enhancements

1. **Smart truncation**: Truncate at plot-critical sentence boundaries, not just token count
2. **Mild replacement**: Replace profanity with contextual mild equivalents (e.g., "frick" instead of asterisks)
3. **Semantic coherence**: Use embeddings to ensure sanitized text maintains meaning
4. **Multi-language support**: Extend to non-English profanity and content detection
