# Handoff: Reverse Engineering → Spec-Driven Development

**The transition point from reverse engineering to standard GitHub Spec Kit workflow**

---

## When This Happens

After completing Gears 1-5 (reverse engineering complete), before starting implementation.

**Triggers:**
- User is on main/master branch
- Gap analysis shows PARTIAL or MISSING features
- Implementation plans exist in .specify/memory/plans/
- User hasn't created feature branch yet

**Purpose:** Celebrate completion, explain transition, guide next steps.

---

## Handoff Procedure

### Step 1: Celebrate Completion

```markdown
# 🎉 Reverse Engineering Complete!

Congratulations! You've successfully transformed your codebase into a
fully-specified, spec-driven project.

## What You've Accomplished

✅ **Gear 1: Analysis** - Tech stack detected, completeness assessed
✅ **Gear 2: Reverse Engineering** - 8 comprehensive documentation files
✅ **Gear 3: Specifications** - GitHub Spec Kit structure created
✅ **Gear 4: Gap Analysis** - Missing features identified and prioritized
✅ **Gear 5: Complete Specification** - All clarifications resolved

## What You Have Now

**Documentation:**
- analysis-report.md
- docs/reverse-engineering/ (8 files)
- docs/gap-analysis-report.md

**GitHub Spec Kit:**
- .specify/memory/constitution.md (project principles)
- .specify/memory/specifications/ (X feature specs)
- .specify/memory/plans/ (Y implementation plans)

**State:**
- .stackshift-state.json (complete history)

**All committed to:** [current branch]
```

### Step 2: Explain the Transition

```markdown
## 🔄 What Happens Next?

You're now transitioning from **reverse engineering** (one-time) to
**standard spec-driven development** (ongoing).

### Two Different Workflows

**StackShift Reverse Engineering (You Just Finished This):**
- Purpose: Transform existing codebase into specifications
- When: One-time (or when major refactor needed)
- Skills: analyze, reverse-engineer, create-specs, gap-analysis, complete-spec
- Output: Complete specification of your system
- ✅ DONE!

**GitHub Spec Kit Standard Workflow (Use Going Forward):**
- Purpose: Implement features, fix bugs, ongoing development
- When: Every day, every feature
- Commands: /speckit.tasks, /speckit.implement, /speckit.analyze
- Workflow: Feature branch → implement → validate → merge
- ⬅️ START USING THIS NOW

### Key Difference

**StackShift** = Creating the specs from existing code
**Spec Kit** = Building features from specs

You've completed the StackShift phase. Now you use Spec Kit!
```

### Step 3: Show Remaining Work

```markdown
## 📋 Your Remaining Work (From Gap Analysis)

You have X features ready for implementation:

### High Priority (P0/P1)
1. **[Feature 1 Name]** - [X hours]
   - Status: ⚠️ PARTIAL (backend done, UI missing)
   - Plan: .specify/memory/plans/[feature-1].md

2. **[Feature 2 Name]** - [X hours]
   - Status: ❌ MISSING (not started)
   - Plan: .specify/memory/plans/[feature-2].md

### Medium Priority (P2)
3. **[Feature 3 Name]** - [X hours]
   - Status: ❌ MISSING
   - Plan: .specify/memory/plans/[feature-3].md

[... list all ...]

## Total Estimated Effort

- P0 features: [X hours]
- P1 features: [Y hours]
- P2 features: [Z hours]
- **Total: [N hours]**
```

### Step 4: Offer Feature Branch Setup

```markdown
## 🚀 Ready to Start Implementing?

I recommend starting with: **[First Feature Name]**

**Why this one first:**
- [Reason: highest priority, foundational, etc.]
- Clear implementation plan already exists
- Estimated effort: [X hours]

**Would you like me to set up the feature branch for you?**

If yes:
1. Create feature branch: `002-[feature-name]`
2. Set up working environment
3. Show you the `/speckit.tasks` and `/speckit.implement` workflow

If no:
- I'll provide instructions for doing it manually
- You can implement when ready
```

### Step 5: If User Says Yes - Set Up Feature Branch

```bash
# Get feature name from plan (e.g., "manual-catch-logging-frontend")
FEATURE_NAME="[feature-name]"
FEATURE_NUMBER="002"  # Increment from existing

# Create and switch to feature branch
git checkout -b ${FEATURE_NUMBER}-${FEATURE_NAME}

# Create README in branch
cat > WORKING_ON.md <<EOF
# Feature: ${FEATURE_NAME}

**Branch:** ${FEATURE_NUMBER}-${FEATURE_NAME}
**Specification:** .specify/memory/specifications/[spec-file].md
**Implementation Plan:** .specify/memory/plans/${FEATURE_NAME}.md

## Status
🔄 In Progress

## Next Steps

1. Generate tasks from implementation plan:
   \`\`\`
   /speckit.tasks
   \`\`\`

2. Execute implementation:
   \`\`\`
   /speckit.implement
   \`\`\`

3. Validate:
   \`\`\`
   /speckit.analyze
   \`\`\`

## Progress
[Will be updated as you work]
EOF

# Commit
git add WORKING_ON.md
git commit -m "chore: set up feature branch for ${FEATURE_NAME}"
git push -u origin ${FEATURE_NUMBER}-${FEATURE_NAME}
```

**Report to user:**
```markdown
✅ Feature branch created: `002-[feature-name]`

## You're All Set!

**Next command to run:**

```
/speckit.tasks
```

This will:
1. Read the implementation plan
2. Generate actionable task checklist
3. Break down the 52-hour plan into specific steps

Then you can run:
```
/speckit.implement
```

To execute the tasks step-by-step!

**I'm ready to help.** Run `/speckit.tasks` when you're ready to start building.
```

### Step 6: If User Says No - Provide Manual Instructions

```markdown
## Manual Feature Branch Workflow

When you're ready to implement a feature:

### 1. Create Feature Branch

```bash
# Pick a feature from .specify/memory/plans/
# Choose a number (001, 002, 003, etc.)
# Name format: {number}-{feature-name}

git checkout -b 002-feature-name
git push -u origin 002-feature-name
```

### 2. Run Spec Kit Commands

```
# Generate tasks
/speckit.tasks

# Implement
/speckit.implement

# Validate
/speckit.analyze
```

### 3. When Complete

```bash
git add .
git commit -m "feat: complete [feature-name] (#002)"
gh pr create --base main
```

### 4. After Merge

```bash
git checkout main
git pull
# Pick next feature and repeat!
```

## Need Help Later?

Just ask! I can help with:
- Setting up feature branches
- Running /speckit commands
- Understanding implementation plans
- Resolving issues
```

---

## Handoff Checklist

Before transitioning to standard workflow:

- [ ] All specifications finalized (no [NEEDS CLARIFICATION])
- [ ] Gap analysis complete with prioritized roadmap
- [ ] Implementation plans exist for PARTIAL/MISSING features
- [ ] Constitution established
- [ ] User understands feature branch workflow
- [ ] User knows to use /speckit.* commands (not stackshift skills)
- [ ] Clear about next steps

---

## Success Criteria

After handoff, user should:

✅ Understand they've completed reverse engineering
✅ Know to use /speckit.* commands going forward
✅ Have clear next steps (either feature branch created or instructions provided)
✅ Feel confident about proceeding
✅ Not confused about what to do next

---

## Notes

- This handoff only happens ONCE (after initial reverse engineering)
- Future feature development uses standard Spec Kit workflow from the start
- If user comes back later: Remind them they're past reverse engineering, use /speckit commands
- Feature branch naming: 001-, 002-, 003- (numeric prefix for ordering)
