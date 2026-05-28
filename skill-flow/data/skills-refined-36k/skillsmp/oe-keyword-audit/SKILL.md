---
name: oe-keyword-audit
description: Find and replace dangerous keyword-based detection with LLM signals. Use when debugging detection interference or before touching routing/detection code. Produces a prioritized migration plan.
---

# oe-keyword-audit

> **PURPOSE:** Identify keyword/regex patterns that override LLM semantic understanding.
> These patterns caused BUG-036 through BUG-042 (7 consecutive bugs).

## The Dangerous Patterns

### Priority 1: BLOCKING (Must fix before PR)

```python
# Pattern: Raw question mark gates Q&A
if "?" in text:           # Blocks detours phrased as questions
if has_question_mark:     # Same issue

# Pattern: Substring keyword matching
if "tour" in text.lower():        # Matches "detour", email addresses
if keyword in message:            # No word boundary

# Pattern: Keyword list without LLM check
if any(kw in text for kw in KEYWORDS):  # Overrides LLM intent
```

### Priority 2: WARNING (Should migrate)

```python
# Pattern: Regex without LLM fallback
if re.search(r"change|modify|update", text):  # Misses paraphrasing

# Pattern: Pre-filter signal used directly
if pre_filter_result.has_question_signal:  # Should check LLM first
```

## Audit Command

Run this grep to find candidates:

```bash
# Find raw question mark checks
rg 'if.*"\?".*in|has_question_mark' --type py -g '!tests/*'

# Find substring keyword matching
rg 'if.*in text|in message|\.lower\(\)' --type py -g '!tests/*' | grep -v unified

# Find keyword list patterns
rg 'any\(.*for.*in.*KEYWORD|for kw in' --type py -g '!tests/*'
```

## Safe Migration Template

**Before (Dangerous):**
```python
def handle_message(text, unified_detection):
    if "?" in text:
        return handle_qna(text)
    # ... rest of logic
```

**After (LLM-first):**
```python
def handle_message(text, unified_detection):
    # LLM signal takes priority
    if unified_detection and unified_detection.is_question:
        return handle_qna(text)
    # Keyword fallback ONLY if LLM unavailable
    elif unified_detection is None and "?" in text:
        return handle_qna(text)
    # ... rest of logic
```

## Files to Audit (Priority Order)

1. `detection/unified.py` - Signal merging logic (BUG-042 home)
2. `detection/pre_filter.py` - Pre-filter signals (BUG-039)
3. `detection/qna/general_qna.py` - Q&A detection (BUG-038)
4. `workflows/steps/step*_handler.py` - Step guards (BUG-041)
5. `detection/response/matchers.py` - Acceptance patterns (BUG-040)
6. `workflows/change_propagation.py` - Change detection
7. `workflows/runtime/router.py` - Site visit intercept (BUG-021)

## Test After Migration

For each migrated pattern, test these combinations:
- [ ] Pure Q&A: "What rooms are available?"
- [ ] Confirmation as question: "Can you confirm this?"
- [ ] Change as question: "Can we change the date to May 20?"
- [ ] Hybrid: "Room B looks perfect. What about parking?"

## Output Format

```markdown
## Keyword Audit: [File Name]

### Dangerous Patterns Found
| Line | Pattern | Risk | Suggested Fix |
|------|---------|------|---------------|
| 145 | `if "?" in text` | Blocks detours | Use `unified.is_question` |

### Migration Status
- [ ] Pattern migrated
- [ ] Unit test added
- [ ] E2E verified with real APIs
```