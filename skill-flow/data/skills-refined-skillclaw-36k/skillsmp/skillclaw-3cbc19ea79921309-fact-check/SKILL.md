---
name: fact-check
description: Use this skill to systematically verify claims in generated content against reliable sources, ensuring accuracy and reducing the risk of hallucinations.
---

# Fact-Check Skill

This skill provides a structured approach to verify claims made in generated content, aiming to identify and correct hallucinations, confabulations, and unsupported assertions.

## Why Separate Passes Matter

**The Fundamental Problem:** LLMs generate plausible-sounding content by predicting what should come next. This same mechanism produces hallucinations—confident statements that feel true but aren't. An LLM in generation mode cannot reliably catch its own hallucinations because:

1. **Attention is on generation**, not verification.
2. **Coherence pressure** makes false claims feel correct in context.
3. **Same weights** that produced the error will confirm it.
4. **No external grounding** to contradict the confabulation.

**The Solution:** Verification must be a separate cognitive pass with:
- Fresh attention focused solely on each claim.
- Explicit source checking (not memory/training data).
- An adversarial stance toward the content.
- External grounding where possible.

## Diagnostic States

### F1: No Verification Pass
**Symptoms:** Content generated and delivered without any fact-checking.  
**Risk:** Hallucinations pass through undetected.  
**Intervention:** Run a verification pass before delivery. Extract claims and check each against sources.

### F2: Self-Verification (Invalid)
**Symptoms:** Same pass asked to "check your facts" while generating.  
**Risk:** False confidence—errors confirmed by the same process that created them.  
**Intervention:** Complete generation first, then run a separate verification pass with explicit source requirements.

### F3: Memory-Based Verification (Unreliable)
**Symptoms:** Claims checked against "what I know" without external sources.  
**Risk:** Hallucinations verified by hallucinated knowledge.  
**Intervention:** Require explicit source citation for each verified claim. If no source is available, mark as unverified.

### F4: Selective Verification
**Symptoms:** Only some claims checked; others assumed correct.  
**Risk:** Unchecked claims may contain errors.  
**Intervention:** Systematic extraction of ALL verifiable claims. Check each, or explicitly mark unchecked items.

### F5: Verification Complete
**Symptoms:** All claims extracted, each checked against sources, confirming their validity.  
**Risk:** None, as all claims are verified.  
**Intervention:** Ensure that all claims are documented with their sources for transparency.

By following these guidelines, you can effectively reduce the risk of misinformation in generated content.