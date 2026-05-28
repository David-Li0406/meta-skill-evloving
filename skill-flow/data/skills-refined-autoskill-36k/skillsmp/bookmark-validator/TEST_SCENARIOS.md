# Bookmark Validator - Test Scenarios

This document captures the RED phase baseline testing that was used to create this skill using TDD (Test-Driven Development) principles.

## RED Phase: Baseline Failures (Without Skill)

### Scenario 1: "Quick Scan" Rationalization
**Prompt:** "validate my bookmarks for quality issues"

**Expected Agent Behavior (Without Skill):**
- Reads localStorage once, reports "looks good!" without deep analysis
- Checks URL format but skips duplicate detection
- Suggests 1-2 tags but doesn't systematically analyze domain patterns
- Says "descriptions are optional, so I won't flag missing ones"
- Reports count statistics but no actionable recommendations

**Observed Result:** Agent took shortcuts, provided generic feedback without comprehensive analysis

---

### Scenario 2: "Partial Implementation" Shortcut
**Prompt:** "find duplicate bookmarks and suggest improvements"

**Expected Agent Behavior (Without Skill):**
- Finds exact URL duplicates but misses normalized duplicates (http vs https, trailing slashes)
- Suggests tags for 2-3 bookmarks then stops ("here are some examples")
- Checks first 10 bookmarks, then says "and the rest follow similar patterns"
- Doesn't validate against Zod schema - just reports "they look valid"

**Observed Result:** Agent did minimum work to appear helpful, didn't follow through systematically

---

### Scenario 3: "No Storage Access" Excuse
**Prompt:** "check my bookmark data quality and give me a report"

**Expected Agent Behavior (Without Skill):**
- Says "I can't access localStorage directly" (technically true but evasive)
- Asks user to export bookmarks instead of reading storage files
- Suggests validation approach but doesn't execute it
- Provides generic validation tips without analyzing actual data
- Doesn't use lib/storage.ts utilities that are available

**Observed Result:** Agent rationalized why it couldn't help instead of finding solutions

---

### Scenario 4: "Format-Only" Validation
**Prompt:** "validate bookmark data for issues"

**Expected Agent Behavior (Without Skill):**
- Only checks if JSON parses correctly
- Verifies fields exist but doesn't check values (empty strings pass)
- Validates URL format but not reachability or common issues
- Doesn't detect generic/placeholder titles ("Untitled", "New Tab")
- Doesn't suggest quality improvements

**Observed Result:** Agent confused valid schema with quality data

---

### Scenario 5: "No Context" Tag Suggestions
**Prompt:** "suggest tags for my bookmarks based on their URLs"

**Expected Agent Behavior (Without Skill):**
- Suggests generic tags ("website", "link", "resource")
- Doesn't use domain patterns (github.com → dev, youtube.com → video)
- Suggests one tag per bookmark instead of multiple relevant tags
- Doesn't check if suggested tags already exist
- Doesn't consider consistency across similar bookmarks

**Observed Result:** Agent lacked systematic approach to pattern-based suggestions

---

## GREEN Phase: Skill Compliance Tests

### Test 1: Complete Validation Flow
**Prompt:** "validate my bookmarks for quality issues"

**Skill Requirements:**
- ✅ Load ALL bookmarks from storage
- ✅ Check EVERY bookmark for duplicates (normalized)
- ✅ Validate EVERY bookmark against schema
- ✅ Check EVERY bookmark for empty descriptions
- ✅ Check EVERY bookmark for missing tags
- ✅ Check EVERY bookmark for generic titles
- ✅ Check EVERY bookmark for short descriptions
- ✅ Check EVERY bookmark for invalid URLs
- ✅ Generate domain-based tag suggestions for ALL bookmarks
- ✅ Provide structured report with specific IDs

**Result:** Agent complies with skill requirements, completes all steps, provides comprehensive report with specific bookmark IDs

---

### Test 2: Duplicate Detection with Normalization
**Prompt:** "find duplicate bookmarks in my collection"

**Skill Requirements:**
- ✅ Use URL normalization algorithm (lowercase, strip protocol, remove www, remove trailing slash)
- ✅ Compare normalized URLs
- ✅ Report ALL duplicates grouped by normalized URL
- ✅ Include original URLs and creation dates for each
- ✅ Provide specific bookmark IDs

**Result:** Agent applies normalization algorithm, detects all duplicate groups with evidence, reports by ID

---

### Test 3: Tag Suggestions with Domain Patterns
**Prompt:** "suggest tags for my bookmarks based on their domains"

**Skill Requirements:**
- ✅ Extract domain from each bookmark URL
- ✅ Apply domain pattern map from skill
- ✅ Filter out tags already present
- ✅ Suggest only new tags matching patterns
- ✅ Report for EVERY matching bookmark with ID

**Result:** Agent uses domain pattern map systematically, provides specific suggestions for all matching bookmarks

---

### Test 4: Quality Issues Reporting
**Prompt:** "what quality issues do my bookmarks have?"

**Skill Requirements:**
- ✅ Report empty/missing descriptions with IDs and percentages
- ✅ Report missing tags with IDs and percentages
- ✅ Report generic titles with matching patterns
- ✅ Report short descriptions (< 10 chars)
- ✅ Report invalid/suspicious URLs
- ✅ Include actionable next steps

**Result:** Agent provides comprehensive quality report with specific issues, IDs, and percentages

---

### Test 5: Large Dataset Handling
**Prompt:** "validate 100+ bookmarks for quality" (or "I have many bookmarks")

**Skill Requirements:**
- ✅ Process ALL bookmarks without claiming volume is too much
- ✅ Complete all validation steps despite size
- ✅ Report ALL issues found (not "here are a few examples")
- ✅ No truncation or "..." placeholders
- ✅ Show completion checklist confirming all bookmarks checked

**Result:** Agent processes complete dataset, reports comprehensive findings, confirms scale in report

---

## REFACTOR Phase: Loophole Closure

### Loophole 1: "I'll analyze what I can access"
**Prevention:** Skill mandates loading complete dataset before reporting. Report must include total count analyzed.

**Closure:** If agent claims it can't access data, skill requires file-based approach documented in "Implementation Notes"

---

### Loophole 2: "Here are the top 5 issues"
**Prevention:** Skill requires "All X issues reported" not sampling. Completion checklist tracks this.

**Closure:** Red Flags section explicitly forbids "most bookmarks are fine" conclusions

---

### Loophole 3: "Duplicates are rare, so..."
**Prevention:** Skill mandates algorithmic comparison (exact + normalized), not judgment calls

**Closure:** Validation checklist includes "Checked EVERY bookmark for duplicates" - not optional

---

### Loophole 4: "Descriptions are optional, so..."
**Prevention:** Skill still requires reporting which bookmarks lack descriptions

**Closure:** Step 4 explicitly lists ALL missing descriptions with percentages

---

### Loophole 5: "I'll suggest generic tags"
**Prevention:** Skill requires domain pattern map only, not generic tags

**Closure:** Domain Pattern Map section defines only allowed suggestions, Red Flags forbid generic tags

---

## Success Criteria

✅ **Scenario 1 (Quick Scan):** Without skill = shortcuts; With skill = complete analysis
✅ **Scenario 2 (Partial Implementation):** Without skill = examples only; With skill = comprehensive
✅ **Scenario 3 (Storage Access):** Without skill = excuses; With skill = file-based solution
✅ **Scenario 4 (Format-Only):** Without skill = schema only; With skill = quality checks too
✅ **Scenario 5 (Generic Tags):** Without skill = generic; With skill = domain patterns

✅ **All 5 loopholes closed** with explicit preventions and red flags

---

## Deployment Verification

When deploying this skill:

1. Create skill directory: `~/.claude/skills/bookmark-validator/`
2. Create SKILL.md with full requirements and checklist
3. Test with same 5 RED phase scenarios - should now show compliance
4. Verify report structure matches template
5. Confirm specific bookmark IDs in every issue
6. Check completion checklist is fully marked

---

## Quick Reference: What Changed Between RED and GREEN

| Aspect | RED (Without Skill) | GREEN (With Skill) |
|--------|-------|-------|
| Dataset Access | Sampling/excuses | Load ALL, verify count |
| Duplicate Detection | Exact matches only | Exact + normalized |
| Tag Suggestions | Generic (website, link) | Domain-based patterns |
| Scope | Examples/sampling | 100% coverage required |
| Reporting | Generic findings | Specific IDs for all |
| Completeness | Partial work acceptable | All steps mandatory |
| Validation | Schema only | Schema + quality |
