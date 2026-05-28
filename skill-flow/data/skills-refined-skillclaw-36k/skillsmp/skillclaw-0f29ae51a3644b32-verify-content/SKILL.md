---
name: verify-content
description: Use this skill when you need to run comprehensive quality verification on workshop or demo content according to Red Hat standards and validation agents.
---

# Skill body

## When to Use

**Use this skill when you want to**:
- Verify workshop content before publishing.
- Check demo modules for quality and completeness.
- Validate technical accuracy and Red Hat style compliance.
- Review content for accessibility standards.
- Get actionable feedback on content improvements.

**Don't use this for**:
- Creating new content → use `/create-lab` or `/create-demo`.
- Converting between formats → use `/blog-generate`.

## Workflow

### Step 1: Detect and Select Verification Prompts

**CRITICAL: Before running verification, detect which prompt sets are available and let the user choose.**

**Detection Priority:**
1. **Current Git Repo**: `.claude/prompts/` in the current repository (highest priority).
2. **Global Home**: `~/.claude/prompts/` (user's global settings).

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

1. Current repo: /path/to/current/repo/.claude/prompts/
   └─ Last updated: [date] (10 prompts)

2. Global home: ~/.claude/prompts/
   └─ Last updated: [date] (10 prompts)

Which prompts should I use for verification?

Options:
1. Current repo (use repo-specific prompts) - Recommended if customized
2. Global home (use your personal defaults)

Your choice: [1/2]
```

**If only one location found:**
```
✅ Using verification prompts from: ~/.claude/prompts/
   Last updated: [date]
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

### Step 2: Identify Content Type

**Q: What type of content are you verifying?**

Options:
1. Workshop module (hands-on lab content).
2. Demo module (presenter-led demonstration).
3. Multiple files (specify pattern).

### Step 3: Locate Content

**For single file**:
- Provide file path (e.g., `content/modules/ROOT/pages/module-01-install-aap.adoc`).

**For multiple files**:
- Provide glob pattern (e.g., `content/modules/ROOT/pages/*.adoc`).
- Or directory path (e.g., `content/modules/ROOT/pages/`).

### Step 4: Run Verification Agents

I'll run comprehensive verification using these validation frameworks:

**For Workshop Content**:
1. `enhanced_verification_workshop.txt` - Overall quality assessment.
2. `redhat_style_guide_validation.txt` - Red Hat style compliance.
3. `verify_workshop_structure.txt` - Workshop structure validation.
4. `verify_technical_accuracy_workshop.txt` - Technical accuracy.
5. `verify_accessibility_compliance_workshop.txt` - Accessibility standards.
6. `verify_content_quality.txt` - General content quality.

**For Demo Content**:
1. `enhanced_verification_demo.txt` - Overall demo quality.
2. `redhat_style_guide_validation.txt` - Red Hat style compliance.
3. `verify_technical_accuracy_demo.txt` - Demo technical accuracy.
4. `verify_accessibility_compliance_demo.txt` - Accessibility standards.
5. `verify_content_quality.txt` - General content quality.

### Step 5: Present Results

I'll provide:

**Summary Table**:
- Clean table with Issue, Priority, and Files columns.
- No time estimates or fix duration.
- Clear priority levels (Critical, High, Medium, Low).

**Strengths Section**:
- What your content does well.
- Areas for improvement.