# Voice Extraction Edge Cases

## Handling Difficult Voice Extraction Scenarios

### Edge Case 1: Inconsistent Voice Across Channels

**Scenario:** Website copy is formal, but social media is casual.

**How to Handle:**
1. Document both voices with sources
2. Don't average them—note the inconsistency
3. Ask: "Is this intentional (channel-appropriate) or accidental (brand drift)?"

**Output Format:**
```json
{
  "voice_inconsistency": {
    "channel_a": {
      "source": "Website",
      "formality_score": 7,
      "evidence": "[quote]"
    },
    "channel_b": {
      "source": "Instagram",
      "formality_score": 3,
      "evidence": "[quote]"
    },
    "resolution_needed": "Clarify: Should all channels match, or is channel-specific voice intentional?"
  }
}
```

---

### Edge Case 2: Stated Voice ≠ Actual Voice

**Scenario:** Client says they want to sound "bold and edgy" but all their content is conservative and safe.

**How to Handle:**
1. Document both the stated preference AND the actual voice
2. Flag the gap explicitly
3. Don't assume which is "correct"

**Output Format:**
```json
{
  "voice_gap": {
    "stated_preference": "Bold, edgy, disruptive",
    "source": "Intake form Q12",
    "actual_voice": {
      "directness_score": 4,
      "evidence": "[conservative quote]"
    },
    "resolution_question": "Should new content match current voice or shift toward stated preference? If shifting, how aggressively?"
  }
}
```

---

### Edge Case 3: Multiple Authors, Multiple Voices

**Scenario:** Blog posts vary wildly because different team members write them.

**How to Handle:**
1. Analyze samples from each identifiable author
2. Find the common elements (if any)
3. Note the variation range
4. Recommend: standardize or embrace variety?

**Output Format:**
```json
{
  "voice_variation": {
    "samples_analyzed": 10,
    "distinct_voices_detected": 3,
    "common_elements": ["Always uses 'we'", "Avoids jargon"],
    "variable_elements": ["Formality ranges 3-8", "Humor ranges 1-6"],
    "recommendation": "Define acceptable range or standardize to primary voice"
  }
}
```

---

### Edge Case 4: No Content Exists Yet

**Scenario:** New brand, no existing copy to analyze.

**How to Handle:**
1. Document that no samples exist
2. Extract voice preferences from questionnaire
3. Analyze competitor voices for positioning
4. Mark everything as PREFERENCE, not DEMONSTRATED

**Output Format:**
```json
{
  "voice_source": "stated_preference_only",
  "confidence": "LOW",
  "note": "No existing content to analyze. Voice profile based on stated preferences and competitor positioning.",
  "validation_needed": "Create 3-5 sample pieces and validate voice before scaling"
}
```

---

### Edge Case 5: B2B with Technical + Marketing Content

**Scenario:** Documentation is technical, marketing is benefit-focused. Both are "the brand."

**How to Handle:**
1. Create separate voice profiles for each context
2. Identify the shared elements (the "brand core")
3. Define when each applies

**Output Format:**
```json
{
  "voice_contexts": {
    "marketing": {
      "when": "Ads, landing pages, social",
      "profile": { "formality": 5, "technical": 3 }
    },
    "technical": {
      "when": "Docs, API reference, support",
      "profile": { "formality": 7, "technical": 9 }
    },
    "shared_core": {
      "always": ["Clear", "Helpful", "No jargon without definition"]
    }
  }
}
```

---

### Edge Case 6: Founder Voice vs. Brand Voice

**Scenario:** Founder has a distinct personal voice. Should the brand match?

**How to Handle:**
1. Analyze founder's writing separately
2. Determine if founder IS the brand (personal brand) or represents it (company brand)
3. Document the relationship

**Questions to Ask:**
- Does the founder write customer-facing content?
- Is the founder's personality central to the brand story?
- Will the brand need to scale beyond the founder?

---

### Edge Case 7: Voice for Sensitive Topics

**Scenario:** Brand normally playful, but needs to address serious topics (crisis, health, money).

**How to Handle:**
1. Define the "baseline" voice
2. Define "serious mode" modifications
3. Specify triggers for each mode

**Output Format:**
```json
{
  "voice_modes": {
    "baseline": {
      "humor": 6,
      "enthusiasm": 7,
      "when": "Default for all content"
    },
    "serious": {
      "humor": 1,
      "enthusiasm": 4,
      "warmth": 8,
      "when": "Health topics, money discussions, crisis communications",
      "modifications": "Drop humor entirely, increase empathy, maintain warmth"
    }
  }
}
```

---

### Edge Case 8: Minimal Content to Analyze

**Scenario:** Only have 2-3 short pieces (e.g., a brief About page and a few social posts).

**How to Handle:**
1. Analyze what exists with appropriate skepticism
2. Note sample size limitations
3. Provide provisional scores with wide ranges
4. Recommend minimum content for confident analysis

**Output Format:**
```json
{
  "sample_limitation": {
    "samples_analyzed": 3,
    "total_words": 450,
    "confidence": "LOW",
    "scores_are": "provisional_ranges",
    "formality": "5-7 (insufficient data to narrow)",
    "recommendation": "Analyze 5+ pieces totaling 2000+ words for confident profile"
  }
}
```

---

## General Principle

When in doubt:
1. **Document, don't decide** — Note the ambiguity
2. **Ask, don't assume** — Add to clarification questions
3. **Range, don't pinpoint** — Give a range when evidence is thin
4. **Source everything** — Even uncertainty needs documentation