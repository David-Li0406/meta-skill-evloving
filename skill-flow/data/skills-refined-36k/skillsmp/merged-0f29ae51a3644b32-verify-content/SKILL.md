---
name: verify-content
description: Use this skill to run comprehensive quality verification on workshop or demo content using Red Hat standards and validation agents.
---

# Content Verification Skill

Verify workshop or demo content against Red Hat quality standards, style guidelines, technical accuracy, and accessibility requirements.

## When to Use

**Use this skill when you want to**:
- Verify workshop content before publishing
- Check demo modules for quality and completeness
- Validate technical accuracy and Red Hat style compliance
- Review content for accessibility standards
- Get actionable feedback on content improvements

**Don't use this for**:
- Creating new content → use `/create-lab` or `/create-demo`
- Converting between formats → use `/blog-generate`

## Workflow

### Step 0: Detect and Select Verification Prompts (FIRST)

**CRITICAL: Before running verification, detect which prompt sets are available and let user choose.**

**Detection Priority:**
1. **Current Git Repo**: `.claude/prompts/` in current repository (highest priority)
2. **Global Home**: `~/.claude/prompts/` (user's global settings)

**Prompt Detection Steps:**

1. **Check current directory for git repo:**
   ```bash
   git rev-parse --show-toplevel 2>/dev/null
   ```

2. **If in git repo, check for local `.claude/prompts/`:**
   ```bash
   ls [repo-root]/.claude/prompts/*.txt 2>/dev/null
   ```

3. **Check global home directory:**
   ```bash
   ls ~/.claude/prompts/*.txt 2>/dev/null
   ```

**If multiple locations found, ask user:**

```
🔍 Found verification prompts in multiple locations:

1. Current repo: /Users/psrivast/work/showroom-content/aap-selfserv-intro-showroom/.claude/prompts/
   └─ Last updated: 13 Jan 16:01 (10 prompts)

2. Global home: ~/.claude/prompts/
   └─ Last updated: 13 Jan 14:47 (10 prompts)

Which prompts should I use for verification?

Options:
1. Current repo (use repo-specific prompts) - Recommended if customized
2. Global home (use your personal defaults)

Your choice: [1/2]
```

**If only one location found:**

```
✅ Using verification prompts from: ~/.claude/prompts/
   Last updated: 13 Jan 14:47
   Total prompts: 10
```

**If NO prompts found:**

```
❌ ERROR: No verification prompts found in any location.

Verification prompts should be in:
- Current repo: .claude/prompts/ (if repo-specific)
- Global home: ~/.claude/prompts/ (for all projects)

Please ensure verification prompts are available in one of these locations.
```

**After user selects, confirm and show which prompts will be used:**

```
📋 Using prompts from: Current repo (.claude/prompts/)

Will use these validation frameworks:
✓ enhanced_verification_workshop.txt (43K, updated 16:01)
✓ redhat_style_guide_validation.txt (5.1K, updated 16:01)
✓ verify_workshop_structure.txt (14K, updated 16:01)
✓ verify_technical_accuracy_workshop.txt (9.7K, updated 14:45)
✓ verify_accessibility_compliance_workshop.txt (10K, updated 14:47)
✓ verify_content_quality.txt (13K, updated 14:45)

Continue with verification? [Yes/No]
```

### Step 1: Identify Content Type

**Q: What type of content are you verifying?**

Options:
1. Workshop module (hands-on lab content)
2. Demo module (presenter-led demonstration)
3. Multiple files (specify pattern)

### Step 2: Locate Content

**For single file**:
- Provide file path (e.g., `content/modules/ROOT/pages/module-01-install-aap.adoc`)

**For multiple files**:
- Provide glob pattern (e.g., `content/modules/ROOT/pages/*.adoc`)
- Or directory path (e.g., `content/modules/ROOT/pages/`)

### Step 3: Run Verification Agents

I'll run comprehensive verification using these validation frameworks:

**For Workshop Content**:
1. `enhanced_verification_workshop.txt` - Overall quality assessment
2. `redhat_style_guide_validation.txt` - Red Hat style compliance
3. `verify_workshop_structure.txt` - Workshop structure validation
4. `verify_technical_accuracy_workshop.txt` - Technical accuracy
5. `verify_accessibility_compliance_workshop.txt` - Accessibility standards
6. `verify_content_quality.txt` - General content quality

**For Demo Content**:
1. `enhanced_verification_demo.txt` - Overall demo quality
2. `redhat_style_guide_validation.txt` - Red Hat style compliance
3. `verify_technical_accuracy_demo.txt` - Demo technical accuracy
4. `verify_accessibility_compliance_demo.txt` - Accessibility standards
5. `verify_content_quality.txt` - General content quality

### Step 4: Present Results

I'll provide results in this order:

**1. Detailed Issue Sections FIRST** (top of output):
- Specific file locations and line numbers
- Before/after examples for each issue
- Implementation steps showing exactly how to fix
- Why each issue matters
- Grouped by issue type with exact counts

**2. Validation Summary Table LAST** (bottom of output):
- Clean table with Issue, Priority, and Files columns
- No time estimates or fix duration
- Clear priority levels (Critical, High, Medium, Low)
- Total issue counts

**3. Strengths Section** (after summary table):
- What your content does exceptionally well
- Positive highlights to reinforce good practices
- Recognition of quality work

**CRITICAL OUTPUT RULES:**
- Summary table comes LAST, not first
- Detailed sections are at the TOP
- **STOP IMMEDIATELY after strengths section**
- **DO NOT add any additional summaries, assessments, or recaps**
- **NO "Overall Assessment", NO "Quick Stats", NO "Top 3 Fixes"**
- **NO text after strengths - that's the END of output**

### Step 5: Offer Fixes (Optional)

After showing results, I can:
- Apply fixes automatically (with your approval)
- Provide code snippets for manual fixes
- Explain why each change improves quality

## Example Usage

### Example 1: Verify Single Workshop Module

```
User: /verify-content

Skill: What type of content are you verifying?
User: Workshop module

Skill: File path?
User: content/modules/ROOT/pages/module-01-install-aap.adoc

[Runs all workshop verification agents]

Skill:

## 3 missing verification commands
**Priority: Critical**
**Affected Files:** module-01-install-aap.adoc

### Details:

1. **Line 45, module-01-install-aap.adoc**
   - Current: Deployment step with no verification
   - Required: Add `oc get pods -n ansible-automation-platform` with expected output
   - Why: Learners can't verify deployment success
   - Fix: Add verification command after deployment step showing expected "Running" status

[... additional detailed sections for each issue ...]

---

## Validation Summary

┌──────────────────────────────────┬──────────┬───────────┐
│              Issue               │ Priority │   Files   │
├──────────────────────────────────┼──────────┼───────────┤
│ 3 missing verification commands  │ Critical │ 1 file    │
├──────────────────────────────────┼──────────┼───────────┤
│ 1 incorrect product name "OCP"   │ Critical │ 1 file    │
├──────────────────────────────────┼──────────┼───────────┤
│ 2 images missing alt text        │ Critical │ 1 file    │
├──────────────────────────────────┼──────────┼───────────┤
│ Incomplete troubleshooting       │ High     │ 1 file    │
├──────────────────────────────────┼──────────┼───────────┤
│ Missing learning outcomes        │ High     │ 1 file    │
├──────────────────────────────────┼──────────┼───────────┤
│ Commands lack expected output    │ Medium   │ 1 file    │
└──────────────────────────────────┴──────────┴───────────┘

**Total Issues:** 11 (6 Critical, 3 High, 2 Medium)

---

✅ Strengths Worth Highlighting

Your module excels in these areas:

1. Clear Step-by-Step Instructions - Installation steps are well-structured and easy to follow
2. Proper AsciiDoc Formatting - Code blocks and syntax highlighting are correctly implemented
3. Strong Technical Content - Accurate AAP installation procedures for OpenShift

[END OF VERIFICATION OUTPUT - NOTHING AFTER THIS]
```

### Example 2: Verify All Modules in Workshop

```
User: Verify all my workshop modules

Skill: Content location?
User: content/modules/ROOT/pages/

[Scans and finds 3 modules + index/overview]

Skill: Found 5 files:
- index.adoc
- 01-overview.adoc
- 02-details.adoc
- module-01-install-aap.adoc
- module-02-configure-aap.adoc

Verify all? [Yes/Select specific files]

User: Yes

[Runs verification on all files]

Skill:

## 5 title case headings found across all files
**Priority: High**
**Affected Files:** index.adoc, 01-overview.adoc, 02-details.adoc, module-01-install-aap.adoc, module-02-configure-aap.adoc

### Details:

1. **Line 12, index.adoc**
   - Current: `= Introduction To Ansible Automation Platform`
   - Required: `= Introduction to Ansible Automation Platform`
   - Why: Red Hat style guide requires sentence case
   - Fix: Lowercase "To"

[... additional detailed sections for each issue ...]

---

## Validation Summary

┌──────────────────────────────────┬──────────┬───────────┐
│              Issue               │ Priority │   Files   │
├──────────────────────────────────┼──────────┼───────────┤
│ Inconsistent heading styles      │ Critical │ All files │
├──────────────────────────────────┼──────────┼───────────┤
│ 4 images missing alt text        │ Critical │ 3 files   │
├──────────────────────────────────┼──────────┼───────────┤
│ 5 title case headings            │ High     │ All files │
├──────────────────────────────────┼──────────┼───────────┤
│ 3 missing Red Hat product names  │ High     │ 3 files   │
├──────────────────────────────────┼──────────┼───────────┤
│ Incomplete verification commands │ Medium   │ 2 files   │
└──────────────────────────────────┴──────────┴───────────┘

**Total Issues:** 17 (6 Critical, 8 High, 3 Medium)
**Files Affected:** 5 files

---

✅ Strengths Worth Highlighting

Your workshop excels in these areas:

1. Excellent Business Context - Outstanding scenario in overview addressing real organizational challenges
2. Progressive Learning Flow - Well-structured progression from basic to advanced concepts
3. Strong Technical Depth - Comprehensive AAP configuration coverage across modules
4. Good Documentation Structure - Clear separation of overview, details, and hands-on modules

[END OF VERIFICATION OUTPUT - NOTHING AFTER THIS]
```

## Verification Standards

Every verification includes:

**Red Hat Style Guide**:
- ✓ Sentence case headlines
- ✓ Official Red Hat product names
- ✓ No prohibited terms (whitelist/blacklist, etc.)
- ✓ Proper hyphenation and formatting
- ✓ Serial comma usage

**Technical Accuracy**:
- ✓ Valid commands for current versions
- ✓ Correct syntax and options
- ✓ Working code examples
- ✓ Accurate technical terminology

**Workshop Quality** (for labs):
- ✓ Clear learning objectives
- ✓ Step-by-step instructions
- ✓ Verification commands with expected outputs
- ✓ Troubleshooting guidance
- ✓ Progressive skill building

**Demo Quality** (for demos):
- ✓ Know/Show structure
- ✓ Business value messaging
- ✓ Presenter guidance
- ✓ Visual cues for slides/diagrams
- ✓ Quantified metrics and ROI

**Accessibility**:
- ✓ Alt text for all images
- ✓ Proper heading hierarchy
- ✓ Clear, inclusive language
- ✓ Keyboard-accessible instructions

**Content Quality**:
- ✓ Complete prerequisites
- ✓ Consistent formatting
- ✓ Proper AsciiDoc syntax
- ✓ References and citations
- ✓ Professional tone

## Output Format

Results are presented in clear, actionable format with **detailed sections FIRST, summary table LAST**:

```markdown
## 3 duplicate References sections found
**Priority: Critical**
**Affected Files:** 03-module-01.adoc, 04-module-02.adoc, 05-conclusion.adoc

### Details:

1. **Line 245, 03-module-01.adoc**
   - Current: `== References` section in module
   - Required: Remove - all references go in conclusion module only
   - Why: Multiple References sections confuse readers
   - Fix: Move references to conclusion module, delete from here

2. **Line 189, 04-module-02.adoc**
   - Current: `== References` section in module
   - Required: Remove - consolidate in conclusion
   - Why: Duplicate sections violate Red Hat doc standards
   - Fix: Copy references to conclusion, delete from module

[... additional detailed issue sections ...]

---

## Validation Summary

┌──────────────────────────────────┬──────────┬───────────┐
│              Issue               │ Priority │   Files   │
├──────────────────────────────────┼──────────┼───────────┤
│ Duplicate References sections    │ Critical │ 3 files   │
├──────────────────────────────────┼──────────┼───────────┤
│ Missing descriptive alt text     │ Critical │ 3 files   │
├──────────────────────────────────┼──────────┼───────────┤
│ Title case headings              │ High     │ All files │
├──────────────────────────────────┼──────────┼───────────┤
│ Missing blank lines before lists │ High     │ 2 files   │
├──────────────────────────────────┼──────────┼───────────┤
│ "Powerful" usage                 │ High     │ 4 files   │
└──────────────────────────────────┴──────────┴───────────┘

**Total Issues:** 15 (5 Critical, 7 High, 3 Medium)
**Files Affected:** 5 files

---

✅ Strengths Worth Highlighting

Your workshop excels in these areas:

1. Exceptional RBAC Implementation Guidance - Module 01 provides comprehensive step-by-step RBAC configuration that's production-ready
2. Strong Business Context - Outstanding business scenario addressing real organizational challenges
3. Excellent Verification Sections - Checkpoints with ✅ expected results and troubleshooting are exemplary
4. Perfect External Link Formatting - ALL external links correctly use ^ caret (opens in new tab)
5. Clear Persona-Based Learning - User persona approach effectively demonstrates RBAC in action
```

## Detailed Issue Breakdown

### 1. Missing Verification Commands
**File**: module-01-install-aap.adoc:145
**Impact**: Learners can't verify success, leading to confusion
**Priority**: Critical

**Current**:
```asciidoc
. Deploy the AutomationController:
```

**Fixed**:
```asciidoc
. Deploy the AutomationController:
+
[source,bash]
----
oc get automationcontroller -n ansible-automation-platform
----
+
Expected output:
----
NAME                  STATUS   AGE
platform-controller   Running  5m
----
```

**How to fix**:
1. Add verification command after deployment step
2. Include expected output
3. Add success indicator

## Priority Levels

Issues are categorized by priority:

- **Critical**: Must fix before publishing - impacts functionality, accessibility, or brand compliance
- **High**: Should fix soon - affects quality and user experience significantly
- **Medium**: Recommended fixes - improves overall quality
- **Low**: Nice to have - polish and optimization

## Integration with Other Skills

**After `/create-lab`**:
- Run verification on generated module
- Apply