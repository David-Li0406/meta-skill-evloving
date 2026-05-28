# Policy Ruleset for M2 Branch Validation

## Overview

This document defines the **automated policy rules** that the validation pipeline applies to all AI-generated branch proposals. These rules ensure that proposals are:
- Safe (no profanity, hate speech, explicit content)
- On-theme (consistent with story's tone and narrative intent)
- Coherent (logically connected to prior context)
- Playable (valid syntax, acceptable length)

**Philosophy**: Start conservative; loosen iteratively based on playtest feedback.

---

## Rule Categories

## Ruleset Configuration & Overrides

The validation pipeline is **configurable** at runtime. The default ruleset is merged with any overrides provided via:

1. **Browser runtime overrides**
   - `window.PolicyRuleset`
   - `window.DirectorConfig.policyRuleset`
   - `window.DirectorConfig.validationRuleset`

2. **Validator options**
   - `validateProposal(proposal, { ruleset })`
   - `quickValidate(proposal, { ruleset })`
   - `validateProposal(proposal, { rulesetPath })` (Node-only JSON file path)

Overrides are merged on top of the default ruleset (deep merge). Only the provided keys are overridden, so you can change a single rule without redefining the entire ruleset. The resulting ruleset version is included in the validation report metadata.

Example (browser override):

```js
window.PolicyRuleset = {
  version: 'v1.0.1-test',
  rules: {
    profanity_filter: { action: 'reject' }
  }
};
```

Example (per-call override):

```js
ProposalValidator.validateProposal(proposal, {
  ruleset: {
    rules: {
      length_limit_check: { maxLength: 1600, warnLength: 1200 }
    }
  }
});
```

### 1. Content Safety (Critical)

These rules check for harmful, explicit, or offensive content. **Violations trigger auto-rejection.**

#### Rule: `profanity_filter`
**Severity**: Critical
**Type**: Policy check

**Description**: Detects profanity, slurs, and offensive language.

**Implementation**:
- Curated profanity list (configurable per story/region)
- Case-insensitive matching with unicode normalization
- Checks both full words and masked variants (e.g., "f***")

**Action on violation**: Auto-reject with detailed violation report.

**Tuning parameters**:
- `profanity_list` (array): List of prohibited terms
- `allow_mild_expletives` (boolean): If false, rejects all expletives; if true, allows mild ones (story-dependent)

**Example violation**:
```json
{
  "offset": 42,
  "text": "[profanity]",
  "explanation": "Matches prohibited slur in profanity_list"
}
```

---

#### Rule: `explicit_content_filter`
**Severity**: Critical
**Type**: Policy check

**Description**: Detects explicit sexual, violent, or graphic content.

**Implementation**:
- Pattern matching for common explicit phrases and descriptions
- Semantic scoring: embedding-based detection of sexually explicit content
- Violence level assessment (mild action scene vs. gratuitous gore)

**Action on violation**: Auto-reject or mark for manual review (configurable).

**Tuning parameters**:
- `violence_threshold` (0.0–1.0): How much violence is acceptable (0 = none; 1 = unrestricted)
- `explicit_phrases` (array): Patterns to detect explicit content
- `gore_limit` (boolean): If true, rejects descriptions of graphic injury

**Example**:
```json
{
  "rule_id": "explicit_content_filter",
  "result": "failed",
  "severity": "critical",
  "message": "Branch contains graphic sexual content (confidence: 0.92)",
  "violations": [
    {
      "offset": 120,
      "text": "[explicit phrase]",
      "explanation": "Semantic similarity to explicit content (embedding distance 0.15)"
    }
  ]
}
```

---

#### Rule: `hate_speech_detector`
**Severity**: Critical
**Type**: Policy check

**Description**: Detects hate speech, slurs, and discriminatory language.

**Implementation**:
- Curated hate speech list (maintained by trust & safety team)
- Context-aware analysis (e.g., quoting a slur vs. using it authoritatively)
- Language-specific patterns (e.g., dogwhistles)

**Action on violation**: Auto-reject immediately.

**Tuning parameters**:
- `hate_speech_list` (array): Prohibited terms and patterns
- `context_window` (int): Characters around match to evaluate context

---

### 2. Narrative Consistency (High)

These rules check logical and thematic coherence with the story context.

#### Rule: `lore_consistency_check`
**Severity**: High
**Type**: Content validation

**Description**: Verifies that branch content does not contradict established LORE (character facts, world rules, plot events).

**Implementation**:
- Semantic embedding comparison: compare branch text against known LORE facts
- Fact extraction: identify assertions in branch (e.g., "the guard is a spy") and check against LORE
- Contradiction detection: flag if branch asserts something contradictory

**Action on violation**: Flag as warning or high-risk; allow manual override.

**Tuning parameters**:
- `lore_facts` (array): Curated list of immutable story facts (e.g., "the compass was lost in 1847")
- `embedding_threshold` (0.0–1.0): How similar extracted facts must be to LORE to count as a match
- `enforce_strictly` (boolean): If false, allows minor contradictions; if true, rejects any inconsistency

**Example violation**:
```json
{
  "rule_id": "lore_consistency_check",
  "result": "warning",
  "severity": "high",
  "message": "Branch claims compass was created in 1920, but LORE states it was lost in 1847. Contradiction detected.",
  "violations": [
    {
      "offset": 35,
      "text": "created in 1920",
      "explanation": "Contradicts LORE: compass_origin_date = 1847"
    }
  ]
}
```

---

#### Rule: `character_voice_consistency`
**Severity**: High
**Type**: Content validation

**Description**: Checks that character voice, dialogue, and mannerisms match established character definitions.

**Implementation**:
- Compare branch dialogue against character voice samples (if available)
- Semantic distance: embeddings of character speech patterns
- OOC (out-of-character) detection: flag if character does something inconsistent with personality

**Action on violation**: Flag as warning; allow if confidence is low.

**Tuning parameters**:
- `character_profiles` (object): Profiles for each character (voice, dialect, favorite phrases, personality traits)
- `voice_distance_threshold` (0.0–1.0): Maximum embedding distance to accept
- `ooc_tolerance` (0.0–1.0): How much deviation from character is allowed (0 = strict; 1 = very permissive)

---

#### Rule: `theme_consistency_check`
**Severity**: High
**Type**: Content validation

**Description**: Verifies that branch tone, mood, and themes align with the story's established themes.

**Implementation**:
- Semantic analysis: extract theme embeddings from story and branch
- Mood matching: assess tone (dark, hopeful, mysterious) against narrative pacing hint
- Theme keywords: check for presence of expected themes

**Action on violation**: Flag as warning; allow unless severity is high.

**Tuning parameters**:
- `story_themes` (array): Key themes (e.g., "redemption", "betrayal", "discovery")
- `tone_mismatch_threshold` (0.0–1.0): How far branch tone can deviate from story tone
- `required_themes` (array, optional): Themes that **must** be present (e.g., "redemption" is a required theme for this story)

---

#### Rule: `narrative_pacing_check`
**Severity**: Medium
**Type**: Content validation

**Description**: Assesses whether branch length and intensity match the narrative phase (exposition vs. climax).

**Implementation**:
- Length check: climactic branches should be shorter, more intense; exposition branches can be longer
- Intensity analysis: keyword-based or embedding-based intensity scoring
- Pacing consistency: compare to recent branches in same story phase

**Action on violation**: Flag as warning; allow unless branch is severely misaligned.

**Tuning parameters**:
- `phase_length_targets` (object): Target lengths for each phase
  - `exposition`: 100–250 tokens
  - `slow_buildup`: 80–200 tokens
  - `climactic`: 40–120 tokens
  - `resolution`: 100–200 tokens
- `max_intensity` (0.0–1.0): Maximum intensity allowed in resolution phase (resolution should be calm, not chaotic)

---

### 3. Structural Validation (High)

These rules check technical validity of the proposal.

#### Rule: `ink_syntax_validation`
**Severity**: High
**Type**: Structural check

**Description**: If branch_type is `ink_fragment` or `ink_knot`, validate that the Ink syntax is correct.

**Implementation**:
- Parse with InkJS parser
- Check for unmatched brackets, invalid knot names, malformed choice syntax
- Validate that referenced knots/stitches exist (if context includes story JSON)

**Fragment Validation**: For `ink_fragment` type (inline content without knot headers), wrap content in a test knot before parsing:

```javascript
function validateInkSyntax(content, branchType) {
    let contentToValidate = content;
    
    // Wrap fragments in a test knot for parsing
    if (branchType === 'ink_fragment') {
        contentToValidate = `=== _validation_wrapper ===\n${content}\n-> END`;
    }
    
    try {
        const compiler = new inkjs.Compiler(contentToValidate);
        const story = compiler.Compile();
        return { result: 'pass' };
    } catch (parseError) {
        return { result: 'fail', message: parseError.message };
    }
}
```

**Knot/Stitch Reference Validation**: When validating return paths or divert targets:

```javascript
function validateDivertTarget(targetPath, compiledStory) {
    const [knot, stitch] = targetPath.split('.');
    
    // Check knot exists
    const allKnots = Object.keys(compiledStory.mainContentContainer.namedContent);
    if (!allKnots.includes(knot)) {
        return { result: 'fail', message: `Knot '${knot}' not found in story` };
    }
    
    // Check stitch exists (if specified)
    if (stitch) {
        const knotContent = compiledStory.KnotContainerWithName(knot);
        const stitches = Object.keys(knotContent.namedContent || {});
        if (!stitches.includes(stitch)) {
            return { result: 'fail', message: `Stitch '${stitch}' not found in knot '${knot}'` };
        }
    }
    
    return { result: 'pass' };
}
```

**Action on violation**: Auto-reject if critical syntax error; flag as warning if minor.

**Example**:
```json
{
  "rule_id": "ink_syntax_validation",
  "result": "failed",
  "severity": "high",
  "message": "Invalid Ink syntax: unmatched brace at character 42",
  "violations": [
    {
      "offset": 42,
      "text": "{ missing closing }",
      "explanation": "Syntax error: expected '}' but found end of string"
    }
  ]
}
```

---

#### Rule: `length_limit_check`
**Severity**: Medium
**Type**: Structural check

**Description**: Enforces maximum branch length (configurable, default 500 tokens).

**Implementation**:
- Token count using same tokenizer as AI Writer (e.g., GPT-4 tokenizer)
- Configurable per branch type and narrative phase

**Action on violation**: Auto-reject if over hard limit; flag as warning if near limit.

**Tuning parameters**:
- `max_length_tokens` (int): Hard limit (default 500)
- `warn_threshold_tokens` (int): Warning threshold (default 400)

---

#### Rule: `encoding_validation`
**Severity**: Medium
**Type**: Sanitization

**Description**: Ensures branch text uses valid UTF-8 encoding and normalizes whitespace.

**Implementation**:
- Check for invalid UTF-8 sequences
- Normalize unicode (NFC)
- Remove control characters except newlines and tabs
- Collapse excessive whitespace (3+ newlines → 2)

**Action on violation**: Sanitize automatically (replace invalid sequences, normalize).

---

### 4. Format & Encoding (Medium)

#### Rule: `html_sanitization`
**Severity**: Medium
**Type**: Sanitization

**Description**: Strips or escapes HTML/script tags to prevent injection attacks.

**Implementation**:
- Allow safe tags only (e.g., `<i>`, `<b>`, `<span>` with safe classes)
- Strip `<script>`, `<iframe>`, event handlers
- Escape special characters (`&`, `<`, `>`)

**Action on violation**: Sanitize automatically (strip disallowed tags).

**Tuning parameters**:
- `allowed_tags` (array): Whitelist of permitted HTML tags (e.g., `["i", "b", "em", "strong"]`)
- `strip_or_escape` (enum): "strip" (remove tags) or "escape" (replace with entities)

**Example**:
```json
{
  "rule_id": "html_sanitization",
  "result": "sanitized",
  "sanitization_applied": {
    "original_text": "He said <script>alert('XSS')</script>hello",
    "sanitized_text": "He said hello",
    "transform_type": "removal"
  }
}
```

---

### 5. Return Path Validation (High)

#### Rule: `return_path_reachability_check`
**Severity**: High
**Type**: Structural validation

**Description**: Verifies that the specified `return_path` knot exists in the story and is reachable.

**Implementation**:
- Parse story script to extract all knot names
- Check that `return_path` is in the set of valid knots
- Optionally, check that return path is reachable from current scene (control flow analysis)

**Action on violation**: Flag as high-risk; allow if return path is plausible even if not found (hints Director to infer one).

---

#### Rule: `return_path_narrative_coherence`
**Severity**: High
**Type**: Content validation

**Description**: Assesses whether return path makes narrative sense (e.g., "return to middle of a dialogue" might not work).

**Implementation**:
- Semantic analysis: does branch content lead naturally to return path?
- Check return path type (is it a choice point, a scene boundary, an internal monologue?)
- Prefer returning to choice points over mid-scene returns

**Action on violation**: Flag as warning; allow if Director can validate at runtime.

---

## Sanitization Transforms

If a rule triggers a violation but the violation is **sanitizable**, the pipeline applies a transform:

### Transform: `profanity_redaction`
Replaces profanity with asterisks or a placeholder.

Example:
- Input: `"What the f*** is this?"`
- Output: `"What the **** is this?"` or `"What the [expletive] is this?"`

---

### Transform: `explicit_content_removal`
Removes sentences or paragraphs containing explicit content.

Example:
- Input: `"He kissed her tenderly. They made passionate love all night. The next morning, he was gone."`
- Output: `"He kissed her tenderly. The next morning, he was gone."`

---

### Transform: `html_tag_stripping`
Removes disallowed HTML tags.

Example:
- Input: `"He said <script>alert('xss')</script>hello <b>there</b>."`
- Output: `"He said hello <b>there</b>."`

---

### Transform: `whitespace_normalization`
Collapses excessive newlines and tabs.

Example:
- Input: `"Line 1\n\n\n\n\nLine 2"`
- Output: `"Line 1\n\nLine 2"`

---

## Rule Severity Levels

| Severity | Action | Example |
|----------|--------|---------|
| **Critical** | Auto-reject immediately | Profanity, hate speech, explicit content |
| **High** | Flag as high-risk; allow with Director override | LORE contradiction, character voice mismatch |
| **Medium** | Flag as warning; allow by default | Length near limit, theme mismatch |
| **Low** | Log only; no action | Stylistic inconsistency, minor formatting |

---

## Rule Execution Order

1. **Structural checks** (fail fast if syntax is broken)
   - `ink_syntax_validation`
   - `encoding_validation`
2. **Safety checks** (critical-severity first)
   - `profanity_filter`
   - `explicit_content_filter`
   - `hate_speech_detector`
3. **Coherence checks** (high-severity)
   - `lore_consistency_check`
   - `character_voice_consistency`
   - `theme_consistency_check`
   - `narrative_pacing_check`
4. **Path validation**
   - `return_path_reachability_check`
   - `return_path_narrative_coherence`
5. **Length and format** (medium-severity)
   - `length_limit_check`
   - `html_sanitization`

**Rationale**: Fail fast on syntax; then filter for safety; then check coherence. Apply sanitizations after all rule checks.

---

## Configuration Example

```yaml
# policy-config.yaml
profanity_filter:
  enabled: true
  severity: critical
  profanity_list: "curated_profanity_list_v2.txt"
  allow_mild_expletives: false

explicit_content_filter:
  enabled: true
  severity: critical
  violence_threshold: 0.3  # low violence tolerance
  gore_limit: true

lore_consistency_check:
  enabled: true
  severity: high
  enforce_strictly: false  # allow minor contradictions
  embedding_threshold: 0.75

character_voice_consistency:
  enabled: true
  severity: high
  ooc_tolerance: 0.3

theme_consistency_check:
  enabled: true
  severity: high
  tone_mismatch_threshold: 0.4

length_limit_check:
  enabled: true
  severity: medium
  max_length_tokens: 500
  warn_threshold_tokens: 400

# ... more rules
```

---

## Monitoring and Tuning

### Metrics to Track

1. **Rule violation rates**: Which rules trigger most often?
2. **False positive rate**: How many sanitized proposals are still approved?
3. **Playtest feedback**: Do players find sanitized branches coherent and satisfying?
4. **Director override rate**: How often does Director override validation decisions?

### Iterative Tuning

- **Week 1 (Phase 1)**: Run validation on 100 candidate branches; collect statistics.
- **Week 2**: Review top violations; identify rules that are too strict or too loose.
- **Week 3**: Adjust thresholds and add/remove rules based on feedback.
- **Weeks 4+**: Continue monitoring in Phase 2 with internal playtesters.

---

## Future Enhancements

1. **Story-specific policies**: Different rules per story (e.g., noir stories tolerate more violence).
2. **Dynamic profanity lists**: Update from upstream trust & safety team.
3. **Semantic-based coherence**: Use embeddings to detect branches that are "off-vibe" even if they pass syntactic checks.
4. **User feedback integration**: Track which branches players found confusing and use that to retrain/refine rules.
