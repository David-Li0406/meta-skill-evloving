---
name: QA Gatekeeper - Testing & CI/CD Pipeline
description: Quality assurance workflow for PR reviews, CI pipeline monitoring, and production verification
version: 1.2.0
triggers:
  - PR created for bug fix or feature
  - Need to review code changes
  - Monitor GitHub Actions pipeline
  - Verify deployment to production
  - Close verified issues
  - CI tests failing
  - Need to diagnose test failures
  - Visual regression approval needed
  - Accessibility false positive verification
---

## Context

The QA Gatekeeper is responsible for maintaining quality standards across the blog. This includes:
- Code review of Pull Requests
- Monitoring CI/CD pipeline (GitHub Actions)
- Testing deployments on production
- Verifying bug fixes and features
- Ensuring all changes follow skill guidelines
- Providing bug template when users report issues

**When user asks to log a bug, ALWAYS provide the bug template first** (see .github/ISSUE_TEMPLATE/bug_report.yml):
```
Required: Priority (P0-P3), Component, Bug Description
Optional: Steps to Reproduce, Reference/Screenshots, Affected URL
```

**GitHub Actions URL**: https://github.com/oviney/blog/actions
**Production URL**: https://www.viney.ca
**Jekyll Build Time**: ~30-60 seconds
**Deployment Time**: ~2 minutes after merge

## S0. Diagnose CI Failures (FIRST STEP)

**When CI tests are failing, ALWAYS investigate before making changes.**

#### 0a. Check PR Status
```bash
# View PR with CI status
gh pr view 35 --repo oviney/blog --json statusCheckRollup

# Or check specific workflow run
gh run list --repo oviney/blog --branch bugfix/GH-33-blog-layout --limit 5
```

**Identify which tests failed:**
- ✅ Jekyll Build (test)
- ❌ Quality Tests (test) - **This is the failure**

#### 0b. Get CI Logs
```bash
# Find the failing run ID
gh run list --repo oviney/blog --workflow "Quality Tests" --limit 5

# View full logs
gh run view <run-id> --log --repo oviney/blog

# Or open in browser
gh run view <run-id> --web --repo oviney/blog
```

#### 0c. Identify Root Cause

**Quality Tests workflow includes:**
1. **Pa11y (Accessibility)** - WCAG 2.1 AA compliance
   - Look for: "color contrast", "aria-label", "heading hierarchy"
   - Error format: `Error: This element has insufficient contrast`
   
2. **Lighthouse (Performance)** - Core Web Vitals
   - Look for: performance scores, FCP, LCP, CLS
   - Error format: `Performance score: 85 (target: 90)`
   
3. **BackstopJS (Visual Regression)** - Screenshot diffs
   - Look for: "Mismatch errors found", "visual regression"
   - Error format: `Test 'homepage' failed with 5.2% mismatch`

**Example log analysis:**
```
Run npm run test:a11y
  pa11y-ci

  ✖ http://localhost:4000/blog/
    • Error: This element has insufficient contrast at its given color...
      ├── selector: .topic-card-excerpt
      ├── expected: 4.5:1
      ├── actual: 3.8:1
      
  9 errors found
```

#### 0d. Document Findings

**Before making any fixes, comment on PR or issue:**
```markdown
🔍 **CI Failure Diagnosis**

**Failed Test:** Pa11y (Accessibility)
**Error Count:** 9 violations
**Root Cause:** Color contrast ratio on `.topic-card-excerpt` is 3.8:1 (need 4.5:1)

**Affected Selectors:**
- `.topic-card-excerpt` (9 instances)
- Color: #4d4d4d on #ffffff background

**Fix Required:** Darken text color to achieve 4.5:1 minimum contrast ratio
**Recommended Color:** #595959 (provides 7:1 ratio)
```

**CRITICAL:** Never guess at fixes. Always pull logs first.

#### 0e. Distinguish Expected vs Unexpected Failures

**Not all CI failures are bugs.** Some failures are EXPECTED:

**Expected Failures (OK to proceed):**
1. **Visual Regression on Design Changes**
   - Scenario: PR intentionally changes layout/styling
   - BackstopJS will fail (screenshots don't match)
   - Action: Review artifacts, approve if design matches requirements

2. **Accessibility False Positives**
   - Scenario: Pa11y reports contrast violations but colors are actually compliant
   - Possible causes: CI rendering differences, Pa11y bugs, dynamic content
   - Action: Verify with external tools (see External Verification below)

**Unexpected Failures (Block merge):**
1. **Syntax/Build Errors** - Code doesn't compile
2. **Genuine Accessibility Issues** - Contrast ratios below WCAG standards
3. **Performance Regressions** - Scores drop significantly
4. **Broken Functionality** - Features stop working

**External Verification Process for Accessibility:**

When Pa11y fails but you suspect a false positive:

```bash
# Step 1: Identify the failing selector and colors from CI logs
# Example: .topic-card-excerpt with color #4a4a4a on #ffffff

# Step 2: Find the SCSS variable
grep -r "#4a4a4a" _sass/
# Output: _sass/economist-theme.scss:$text-secondary: #4a4a4a;

# Step 3: Verify the compiled CSS
bundle exec jekyll build
grep "topic-card-excerpt" _site/assets/css/style.css | grep color
# Confirm the color is correctly compiled

# Step 4: Check contrast ratio externally
```

**Use WebAIM Contrast Checker:**
1. Visit: https://webaim.org/resources/contrastchecker/
2. Enter foreground color: `#4a4a4a`
3. Enter background color: `#ffffff`
4. Verify ratio meets WCAG standards:
   - **WCAG AA (normal text)**: 4.5:1 minimum
   - **WCAG AAA (normal text)**: 7:1 minimum
5. Screenshot the results for documentation

**Document findings in PR comment:**
```markdown
## ⚠️ Pa11y False Positive Confirmed

**Verification Method:** WebAIM Contrast Checker
**URL:** https://webaim.org/resources/contrastchecker/?fcolor=4a4a4a&bcolor=ffffff

**Results:**
- Foreground: #4a4a4a (text-secondary)
- Background: #ffffff
- Contrast Ratio: **9.5:1**
- WCAG AA: ✅ Pass (4.5:1 required)
- WCAG AAA: ✅ Pass (7:1 required)

**Conclusion:** Colors exceed AAA standards. Pa11y failure is a CI environment issue, not an actual accessibility problem.

**Recommendation:** Proceed with merge after visual regression approval.
```

**When to override CI failures:**
- ✅ Visual regression + design intentionally changed + reviewed by Creative Director
- ✅ Pa11y failure + external verification proves compliance + documented in PR
- ❌ Build failures (never override)
- ❌ Genuine accessibility issues (must fix)

### Step-by-Step Instructions

### 1. PR Review Process

When a PR is created (e.g., PR #35), QA Gatekeeper should:

#### 1a. Review PR Description
```bash
# View PR details
gh pr view 35 --repo oviney/blog
```

**Check:**
- [ ] References issue number (e.g., "Closes #33")
- [ ] Lists all changes made
- [ ] Includes testing checklist
- [ ] Has before/after screenshots (if visual)
- [ ] Meets acceptance criteria from issue

#### 1b. Code Review Checklist
- [ ] **Follows SKILL.md**: Check relevant skill file was followed
  - Creative Director: `docs/skills/economist-theme/SKILL.md`
  - Jekyll Dev: `docs/skills/jekyll-development/SKILL.md`
  - Git Ops: `docs/skills/git-operations/SKILL.md`
- [ ] **No hardcoded values**: Uses SCSS variables, not magic numbers
- [ ] **Proper commit format**: `fix(GH-XX): description\n\nCloses #XX`
- [ ] **Tests included**: If applicable
- [ ] **Security**: No exposed credentials, safe dependencies
- [ ] **Responsive**: Changes work at 320px, 768px, 1024px

#### 1c. Local Testing
```bash
# Fetch PR branch
gh pr checkout 35

# Or manually:
git fetch origin
git checkout bugfix/GH-33-blog-layout

# Test build
bundle exec jekyll build

# Visual testing
bundle exec jekyll serve --config _config_dev.yml --livereload
# Open http://localhost:4000
```

**Test at breakpoints:**
- 320px (mobile)
- 768px (tablet)
- 1024px (desktop)
- 1920px (large desktop)

**Check for regressions:**
- Other pages still work
- Navigation intact
- No console errors
- Images load properly
- Fonts render correctly

#### 1d. Provide Review Feedback

**If approved:**
```markdown
✅ **LGTM** (Looks Good To Me)

**Verified:**
- [x] Fix resolves issue #33
- [x] No visual regressions
- [x] Jekyll build passes
- [x] Tested at 320px, 768px, 1024px
- [x] Follows economist-theme SKILL.md
- [x] SCSS variables used (no hardcoded values)

**Approved for merge to main.**
```

**If changes needed:**
```markdown
🔄 **Changes Requested**

**Issues found:**
1. **Typography**: Title font-size should use variable, not hardcoded 1.75rem
   - Location: `_sass/economist-theme.scss:1120`
   - Fix: Use `$font-size-title` variable

2. **Responsive**: Layout breaks at 768px
   - Issue: Image width doesn't adjust
   - Expected: Should stack vertically at < 768px

**Please address and re-request review.**
```

### 2. Monitor CI/CD Pipeline

After PR is merged to `main`:

#### 2a. Watch GitHub Actions
```bash
# View recent workflow runs
gh run list --repo oviney/blog --limit 5

# Watch specific run (get ID from list)
gh run watch <run-id> --repo oviney/blog

# Or open in browser
open https://github.com/oviney/blog/actions
```

**Monitor these jobs:**
- ✅ **Build**: Jekyll site builds successfully
- ✅ **Test**: All tests pass (if applicable)
- ✅ **Deploy**: GitHub Pages deployment succeeds

**Expected timeline:**
- Build: ~30-60 seconds
- Deploy: ~1-2 minutes
- Total: ~2-3 minutes

#### 2b. Handle Pipeline Failures

**If build fails:**
```bash
# View logs
gh run view <run-id> --log --repo oviney/blog

# Common issues:
# - SCSS syntax error
# - Missing file reference
# - Liquid template error
# - Image file not found
```

**Action:**
1. Create new issue for pipeline failure
2. Label: `bug`, `ci/cd`, `P1:high`
3. Assign to agent who made changes
4. Include full error log

**If deploy fails:**
```bash
# Check GitHub Pages status
gh api repos/oviney/blog/pages

# Common issues:
# - GitHub Pages disabled
# - CNAME conflict
# - Build size > 1GB
```

#### 2.5. Update Visual Regression References

**When BackstopJS fails due to intentional design changes:**

**Step 1: Download CI Artifacts**
```bash
# Find the failing workflow run
gh run list --repo oviney/blog --workflow "Quality Tests" --limit 5

# Download artifacts (includes actual screenshots)
gh run download <run-id> --repo oviney/blog --name backstop-report

# Artifacts location: ./backstop-report/
```

**Step 2: Review Screenshots**

Compare new screenshots against issue acceptance criteria:

**Review Checklist:**
- [ ] **Layout** - Matches design mockup/requirements
- [ ] **Typography** - Font sizes, weights, colors correct
- [ ] **Spacing** - Margins and padding match specs
- [ ] **Images** - Proper sizing and aspect ratios
- [ ] **Responsive** - Check all viewports (desktop/tablet/mobile)
- [ ] **Colors** - Match design system variables
- [ ] **Borders/Shadows** - Applied correctly
- [ ] **Interactive States** - Hover/focus states if visible

**Compare against acceptance criteria from issue:**
```bash
# View original issue requirements
gh issue view 33 --repo oviney/blog

# Example criteria for blog layout:
# ✅ Single-column layout, 1040px max-width
# ✅ Card height ~280-320px
# ✅ Image width 280px, 16:9 aspect ratio
# ✅ 48-64px vertical spacing between cards
# ✅ Responsive at 320px, 768px, 1024px
```

**Step 3: Approve or Request Changes**

If design matches requirements:
```bash
# Option A: Approve locally (recommended)
npm run test:visual:approve
# This runs: backstop approve

# Commit updated references
git add backstop_data/bitmaps_reference/
git commit -m "test: update BackstopJS references for Economist blog layout

Approved visual changes from issue #33:
- Single-column layout with centered cards
- Updated typography and spacing
- New 280px image sizing
- Responsive breakpoints verified"
git push
```

**Option B: Approve from CI artifacts**
```bash
# Copy downloaded screenshots to reference folder
cp -r backstop-report/bitmaps_test/* backstop_data/bitmaps_reference/

# Commit
git add backstop_data/bitmaps_reference/
git commit -m "test: update BackstopJS references for Economist blog layout"
git push
```

If design needs changes:
```markdown
**Comment on PR:**

🔄 **Visual Regression Review - Changes Needed**

**Issues Found:**
1. **Image sizing** - Expected 280px width, seeing 240px in mobile view
   - Screenshot: `backstop_test/blog_page_mobile.png`
   - Line 145: Set `width: 280px` for `.topic-card-image`

2. **Spacing** - Cards too close together at tablet breakpoint
   - Expected: 48-64px between cards
   - Actual: ~32px
   - Line 180: Increase `.topic-card + .topic-card` margin

**Request:** Fix issues and re-run visual tests.
```

**Step 4: Tag Creative Director if Uncertain**

If you're unsure whether design matches requirements:
```bash
gh pr comment 35 --repo oviney/blog --body "@Creative-Director: Please review visual regression artifacts and confirm design matches issue #33 requirements.

Artifacts: https://github.com/oviney/blog/actions/runs/<run-id>

Specific areas to verify:
- Card layout and spacing
- Typography sizing
- Image dimensions
- Responsive behavior"
```

#### 2.6. PR Merge Decision Matrix

**Use this matrix to decide whether to merge a PR with failing CI tests:**

| CI Status | Scenario | Action | Approver |
|-----------|----------|--------|----------|
| ✅ All Pass | Standard case | **Merge** | QA Gatekeeper |
| ❌ Build Fail | Syntax/compile error | **Block** - Fix required | Developer |
| ❌ Pa11y Fail | Genuine accessibility issue | **Block** - Fix colors/contrast | Creative Director |
| ⚠️ Pa11y Fail | False positive (verified externally) | **Merge** - Document in PR | QA Gatekeeper + evidence |
| ❌ BackstopJS Fail | Unintended visual change | **Block** - Fix regression | Creative Director |
| ⚠️ BackstopJS Fail | Intended design change | **Merge** - After approval | Creative Director reviews |
| ❌ Lighthouse Fail | Performance regression | **Block** - Optimize | Developer |
| ❌ Multiple Fails | Mixed issues | **Block** - Fix unexpected, approve expected | Multi-agent |

**Decision Process:**

```bash
# Step 1: Classify each failure as Expected or Unexpected (see Section 0e)
# Step 2: For expected failures, verify/approve
# Step 3: For unexpected failures, request fixes
# Step 4: Document decision in PR comment
```

**Merge with Overrides (Requires Documentation):**

When merging despite CI failures:
```markdown
## ✅ Approved for Merge (CI Override)

**Override Reason:** Pa11y false positive

**Evidence:**
- External verification: WebAIM shows 9.5:1 contrast (AAA compliant)
- Screenshot: [attached]
- CI environment rendering issue confirmed

**Other CI Status:**
- ✅ Jekyll Build: Passing
- ⚠️ Pa11y: Failing (false positive - documented above)
- ✅ Visual Regression: Approved (design intentionally changed)

**Sign-off:** @QA-Gatekeeper with @Creative-Director design approval

**Merging to main.**
```

**Real-World Case Study (Issue #33):**
```markdown
## ✅ Approved for Merge (CI Override) - Issue #33

**Override Reason:** Pa11y false positive on color contrast

**Evidence:**
- Colors externally verified as AAA compliant
- External tools confirmed contrast ratios meet WCAG standards
- Pa11y CI environment rendering issue documented

**Other CI Status:**
- ✅ Jekyll Build: Passing
- ⚠️ Pa11y: Override (false positive - AAA verified externally)
- ✅ Visual Regression: Approved (intentional Economist design changes)
- ✅ All acceptance criteria met

**Decision:** Merged using PR Merge Decision Matrix (Section 2.6)
**Sign-off:** Flow Orchestrator with Creative Director approval
**Commit:** 60b6aac
**Date:** January 5, 2026
```

**Merge Without Overrides:**
```markdown
## ✅ Approved for Merge

**CI Status:** All tests passing ✅

**Verified:**
- [x] Code follows SKILL guidelines
- [x] No regressions
- [x] Acceptance criteria met

**Merging to main.**
```

### 3. Verify Production Deployment

After successful deployment:

#### 3a. Test on Production
```bash
# Open production site
open https://www.viney.ca/blog/

# Or use curl to check
curl -I https://www.viney.ca/blog/
```

**Verification checklist:**
- [ ] Page loads without errors
- [ ] Fix is visible (e.g., blog layout changed)
- [ ] Images load correctly
- [ ] CSS applied properly
- [ ] No 404 errors
- [ ] Mobile responsive works
- [ ] Links function correctly

#### 3b. Cross-browser Testing

**Desktop:**
- Chrome (latest)
- Safari (latest)
- Firefox (latest)

**Mobile (if layout change):**
- iOS Safari
- Chrome Mobile
- Firefox Mobile

**Tools:**
- BrowserStack (if available)
- Browser DevTools device emulation
- Real devices (preferred for final check)

#### 3c. Performance Check

```bash
# Run Lighthouse (if configured)
npm run lighthouse

# Check page load time
curl -w "@curl-format.txt" -o /dev/null -s https://www.viney.ca/blog/
```

**Thresholds:**
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 90
- SEO: > 90

### 4. Issue Verification & Closure

After production verification:

#### 4a. Add Verification Comment
```bash
gh issue comment 33 --repo oviney/blog --body "✅ **Verified on Production**

**Deployment**: https://www.viney.ca/blog/
**PR**: #35
**Commit**: 17cfa30

**Tested:**
- [x] Blog layout matches Economist design
- [x] Single-column layout with 1040px max-width
- [x] Date format: \"Jan 2nd 2026|X min read\"
- [x] Horizontal cards with 280px images
- [x] Borders between cards
- [x] Responsive at 320px, 768px, 1024px
- [x] Default gray image fallback works

**Browsers tested:**
- Chrome 120 ✅
- Safari 17 ✅
- Firefox 121 ✅
- iOS Safari ✅

All acceptance criteria met. Closing issue."
```

#### 4b. Close Issue
```bash
# Close with comment
gh issue close 33 --repo oviney/blog --comment "Fixed in PR #35, deployed to production, verified working."
```

**Or close via PR:**
- If commit message included `Closes #33`, GitHub auto-closes
- Verify issue shows "Closed" status

### 5. Update Skill Files (Self-Learning)

If new patterns or lessons learned:

#### 5a. Identify Learning Opportunity
- New edge case discovered
- Better approach found
- Common mistake to document
- Process improvement

#### 5b. Update Relevant SKILL.md
```bash
# Open skill file
code docs/skills/jekyll-qa/SKILL.md

# Add new section or update existing
# Increment version number
# Document date of change
```

**Version bump rules:**
- Patch (1.0.0 → 1.0.1): Minor clarification, typo fix
- Minor (1.0.0 → 1.1.0): New section, significant addition
- Major (1.0.0 → 2.0.0): Breaking change in process

#### 5c. Commit Skill Update
```bash
git add docs/skills/jekyll-qa/SKILL.md
git commit -m "docs: update jekyll-qa SKILL to v1.1.0

Added section on handling X scenario based on PR #35 learnings"
git push origin main
```

## Common Pitfalls

### Pitfall 1: Approving Without Local Testing
**Problem**: PR looks good in code review but breaks locally or on mobile
**Solution**: Always checkout branch and test locally, especially visual changes
**Example**: CSS looks fine but causes horizontal scroll on mobile

### Pitfall 2: Not Checking Related Pages
**Problem**: Fix works on target page but breaks other pages
**Solution**: Test at least 3 other pages (home, about, another article)
**Prevention**: Add regression test checklist to PR template

### Pitfall 3: Missing CI Pipeline Failure
**Problem**: Merge PR, don't watch pipeline, deployment fails silently
**Solution**: Always monitor GitHub Actions after merge until deploy succeeds
**Timeline**: Set 5-minute timer to check pipeline status

### Pitfall 4: Closing Issue Before Production Verification
**Problem**: Issue closed after PR merge, but deployment fails or bug still exists
**Solution**: Only close issues after verifying fix on production (viney.ca)
**Process**: Merge → Wait 2-3 min → Test production → Verify → Close

### Pitfall 5: Not Testing at All Breakpoints
**Problem**: Layout perfect on desktop, broken on mobile
**Solution**: Test every breakpoint in acceptance criteria (320px, 768px, 1024px)
**Tool**: Browser DevTools → Device Mode → Set specific widths

## Code Snippets/Patterns

### Quick PR Review Script
```bash
#!/bin/bash
# save as: scripts/review-pr.sh
PR_NUM=$1

echo "📋 Fetching PR #${PR_NUM}..."
gh pr view $PR_NUM --repo oviney/blog

echo "\n🔀 Checking out branch..."
gh pr checkout $PR_NUM

echo "\n🏗️  Building site..."
bundle exec jekyll build

if [ $? -eq 0 ]; then
  echo "\n✅ Build successful!"
  echo "\n🚀 Starting local server..."
  bundle exec jekyll serve --config _config_dev.yml --livereload
else
  echo "\n❌ Build failed!"
  exit 1
fi
```

**Usage**: `./scripts/review-pr.sh 35`

### Production Verification Checklist
```bash
# Quick production check
PROD_URL="https://www.viney.ca"
PAGE="/blog/"

# Check status
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${PROD_URL}${PAGE})
echo "HTTP Status: ${STATUS}"

# Check response time
TIME=$(curl -s -o /dev/null -w "%{time_total}" ${PROD_URL}${PAGE})
echo "Response Time: ${TIME}s"

# Check for common errors
curl -s ${PROD_URL}${PAGE} | grep -i "error\|404\|500" || echo "✅ No errors found"
```

### CI Pipeline Status Check
```bash
# Get latest workflow run
LATEST_RUN=$(gh run list --repo oviney/blog --limit 1 --json databaseId,status,conclusion --jq '.[0]')

STATUS=$(echo $LATEST_RUN | jq -r '.status')
CONCLUSION=$(echo $LATEST_RUN | jq -r '.conclusion')

echo "Pipeline Status: ${STATUS}"
echo "Conclusion: ${CONCLUSION}"

if [[ "$CONCLUSION" == "success" ]]; then
  echo "✅ Pipeline passed!"
else
  echo "❌ Pipeline failed or in progress"
fi
```

## Related Files

- [`docs/skills/github-issues-workflow/SKILL.md`](../github-issues-workflow/SKILL.md) - Full bug workflow
- [`docs/skills/jekyll-development/SKILL.md`](../jekyll-development/SKILL.md) - Jekyll server operations
- [`docs/skills/economist-theme/SKILL.md`](../economist-theme/SKILL.md) - Design system guidelines
- [`.github/workflows/`](../../../.github/workflows/) - CI/CD configuration
- [`package.json`](../../../package.json) - Test scripts

## Success Criteria

**PR Review:**
- [ ] Code follows relevant SKILL.md guidelines
- [ ] No hardcoded values (uses variables)
- [ ] Tested locally at all breakpoints
- [ ] No regressions on other pages
- [ ] Proper commit message format
- [ ] Approval or change request provided

**Pipeline Monitoring:**
- [ ] Watched GitHub Actions until completion
- [ ] Build passed successfully
- [ ] Deployment succeeded
- [ ] No pipeline errors or warnings

**Production Verification:**
- [ ] Tested on production URL (viney.ca)
- [ ] Fix visible and working
- [ ] No visual regressions
- [ ] Mobile responsive works
- [ ] Cross-browser tested (3+ browsers)

**Issue Closure:**
- [ ] Verification comment added to issue
- [ ] All acceptance criteria met
- [ ] Production testing documented
- [ ] Issue closed with reference to PR

## Version History

- **1.2.0** (2026-01-05): Major enhancements based on PR #35 learnings:
  - Added Section 0e: Distinguish Expected vs Unexpected Failures
  - Added external verification workflow for Pa11y false positives (WebAIM Contrast Checker)
  - Added Section 2.5: Complete visual regression approval workflow with artifact review
  - Added Section 2.6: PR Merge Decision Matrix for handling CI failures
  - Enhanced troubleshooting with step-by-step accessibility verification
- **1.1.0** (2026-01-05): Added "Step 0: Diagnose CI Failures" - Always investigate logs before fixing
- **1.0.0** (2026-01-05): Initial skill creation - QA Gatekeeper workflow for PR review, CI monitoring, and production verification
