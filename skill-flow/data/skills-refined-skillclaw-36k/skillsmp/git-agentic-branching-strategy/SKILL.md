---
name: git-agentic-branching-strategy
description: Branching strategy guide for Lighthouse LM agentic development. Provides branch selection guidance based on work type (epic/feature/wave), scope, and Progressive Coherence principles. Use when starting new work, implementing epics/features, or deciding branch strategy. Helps agents choose correct branch type and workflow.
---

# Git Agentic Branching Strategy

Branching strategy guidance for agentic development using Lighthouse LM agents, commands, and skills.

## Quick Start

**Get branch recommendation:**
```
"What branch should I create for implementing Epic 1 with 3 features?"
"Should I create wave branch or work directly on feature branch?"
```

**Common scenarios:**
```
- Single wave implementation → wave branch from development
- Feature with 2+ waves → feature branch from development or epic
- Multi-feature epic → epic branch → feature branches
- Bug fix → work directly on development
- Hotfix → hotfix branch from development
```

## Core Principle

**Progressive Coherence and Git Workflow**:
- Each branch represents a coherent unit of work
- Epic branches contain coherent set of features
- Feature branches contain coherent set of waves
- Each commit represents completed wave (atomic, verifiable)

---

## Branch Hierarchy

```
main (protected)
  └── development (integration branch)
       ├── epic-1-progressive-coherence (epic branch)
       │    ├── feature-1.10-infrastructure (feature branch)
       │    │    └── [commits for waves 1.10.1, 1.10.2, 1.10.3...]
       │    ├── feature-1.4-msa-templates (feature branch)
       │    │    └── [commits for waves 1.4.1, 1.4.2...]
       │    └── feature-1.5-addendum-templates (feature branch)
       │         └── [commits for waves 1.5.1, 1.5.2...]
       ├── epic-2-azure-integration (epic branch)
       │    └── feature-2.1-devops-mcp (feature branch)
       │         └── [commits for waves 2.1.1, 2.1.2...]
       ├── wave-3.1.1-standalone-skill (standalone wave from dev)
       └── hotfix-auth-token-validation (hotfix branch)
```

---

## Branch Types

### 1. Main Branch (Protected)

**Purpose**: Production-ready code

**Characteristics**:
- Always deployable
- Protected with branch protection rules
- Only accepts PRs from development
- Linear history (squash or rebase merges)

**Who uses**: Release manager, automated releases

**Agents**: NEVER work directly on main

---

### 2. Development Branch (Integration)

**Purpose**: Integration point for all feature work

**Naming**: `development`

**Merge from**:
- Epic branches (after all features complete)
- Standalone feature branches
- Standalone wave branches
- Hotfix branches

**Merge to**: `main` (via PR only)

**Who uses**: All agents by default

**Work directly on development for**:
- Small changes (1-2 files, <1 hour)
- Bug fixes (non-critical)
- Documentation updates
- README changes
- Minor refactoring

**Characteristics**:
- NOT protected (allows direct merges from features)
- May have failing tests temporarily
- Receives frequent merges
- Testing ground before main

---

### 3. Epic Branches (Long-Lived)

**Purpose**: Isolate work for entire epic with multiple features

**Naming**: `epic-{number}-{short-description}`

**Examples**:
- `epic-1-progressive-coherence`
- `epic-2-azure-integration`
- `epic-5-security-enhancements`

**Who uses**: Agents working on multi-feature epics

**Merge from**: Feature branches within epic

**Merge to**: `development` when epic complete

**Lifespan**: Weeks to months

**Work pattern**:
1. Create epic branch from development
2. Create feature branches from epic
3. Merge features → epic as they complete
4. Merge epic → development when all features complete

**When to use**:
- ✅ Epic has 2+ features
- ✅ Epic will take >1 week
- ✅ Want to integrate features before merging to development
- ✅ Multiple agents working on same epic (different features)

---

### 4. Feature Branches (Medium-Lived)

**Purpose**: Implement entire feature with all its waves

**Naming**: `feature-{epic}.{feature}-{short-description}`

**Examples**:
- `feature-1.10-infrastructure` (part of epic 1)
- `feature-1.4-msa-templates` (part of epic 1)
- `feature-2.1-devops-mcp` (part of epic 2)

**Who uses**: Agents implementing features

**Merge from**: None (agents commit wave implementations directly)

**Merge to**:
- Epic branch (if part of epic)
- `development` (if standalone feature)

**Lifespan**: Days to weeks

**Work pattern**:
- Commit wave 1 directly to feature branch (NO wave branch)
- Commit wave 2 directly to feature branch
- Commit wave 3 directly to feature branch
- Merge entire feature when all waves complete

**Commit format**:
```bash
git commit -m "feat(wave-1.10.1): Implement catalog change monitor"
git commit -m "feat(wave-1.10.2): Implement template staleness detection"
git commit -m "feat(wave-1.10.3): Implement impact analysis"
```

**When to use**:
- ✅ Feature has 2+ waves
- ✅ Feature is part of epic (create from epic branch)
- ✅ Feature is standalone but multi-wave (create from development)

---

### 5. Standalone Wave Branches (Short-Lived)

**Purpose**: Implement single standalone wave (not part of epic)

**Naming**: `wave-{epic}.{feature}.{wave}-{short-description}`

**Examples**:
- `wave-3.1.1-standalone-skill`
- `wave-4.2.1-quick-enhancement`
- `wave-5.3.1-bug-fix-validation`

**Who uses**: Agents implementing standalone waves

**Merge from**: None (leaf branches)

**Merge to**: `development` (skip epic/feature branches)

**Lifespan**: Hours to days

**Work pattern**:
- Create wave branch from development
- Implement wave completely
- Merge directly to development

**When to use**:
- ✅ Single wave implementation (not part of epic/feature)
- ✅ Quick enhancement or addition
- ✅ Standalone work item

**When NOT to use**:
- ❌ Wave is part of multi-wave feature (commit directly to feature branch instead)
- ❌ Simple bug fix (work directly on development)

---

### 6. Hotfix Branches (Urgent Fixes)

**Purpose**: Critical fixes that can't wait for normal workflow

**Naming**: `hotfix-{short-description}`

**Examples**:
- `hotfix-auth-token-validation`
- `hotfix-security-vulnerability`
- `hotfix-data-corruption-fix`

**Who uses**: Agents fixing critical bugs

**Merge from**: None

**Merge to**: `development` AND potentially `main` (fast-track)

**Lifespan**: Hours

**Work pattern**:
1. Create hotfix branch from development
2. Implement fix
3. Merge to development
4. If critical, merge to main via expedited PR

**When to use**:
- ✅ Critical production bug
- ✅ Security vulnerability
- ✅ Data integrity issue
- ✅ Service outage fix

---

## Decision Framework

### Quick Decision Tree

```
Is this a hotfix?
  └─ YES → Create hotfix branch from development
  └─ NO → Continue...

Is this a small change (<1 hour, 1-2 files)?
  └─ YES → Work directly on development
  └─ NO → Continue...

Is this a single wave?
  └─ YES → Create wave branch from development
  └─ NO → Continue...

Is this a feature with 2+ waves?
  └─ YES → Is feature part of epic?
       └─ YES → Create feature branch from epic branch
       └─ NO → Create feature branch from development
  └─ NO → Continue...

Is this an epic with 2+ features?
  └─ YES → Create epic branch from development, then create feature branches from epic
```

---

### When to Create Epic Branch

**Create Epic Branch If**:
- ✅ Epic has multiple features (2+ features)
- ✅ Epic will take >1 week to complete
- ✅ Want to integrate features together before merging to development
- ✅ Multiple agents working on same epic simultaneously (different features)

**Examples**:
```
Epic 1: Progressive Coherence System
  - Feature 1.10: Infrastructure (3 waves)
  - Feature 1.4: MSA Templates (2 waves)
  - Feature 1.5: Addendum Templates (1 wave)
  → Create epic-1-progressive-coherence from development
```

**Skip Epic Branch If**:
- ❌ Only 1 wave total (use wave branch from development)
- ❌ Single feature with 1-3 waves (use feature branch from development)
- ❌ Epic is simple documentation update (work on development)
- ❌ Want immediate integration with other work

---

### When to Create Feature Branch

**Create Feature Branch If**:
- ✅ Feature has 2+ waves
- ✅ Feature is part of larger epic (create from epic branch)
- ✅ OR feature is standalone but has multiple waves (create from development)

**Examples**:
```
Feature 1.10: Infrastructure
  - Wave 1.10.1: Catalog change monitor
  - Wave 1.10.2: Template staleness detection
  - Wave 1.10.3: Impact analysis
  → Create feature-1.10-infrastructure from epic-1 (or development if standalone)
  → Commit all waves directly to feature branch
```

**Skip Feature Branch If**:
- ❌ Single wave only (create standalone wave branch from development)
- ❌ Simple bug fix or documentation (work directly on development)

---

### When to Create Standalone Wave Branch

**Create Wave Branch If**:
- ✅ Single wave implementation
- ✅ Not part of existing epic or feature
- ✅ Standalone work item

**Examples**:
```
Wave 3.1.1: Create new standalone skill
  → Create wave-3.1.1-standalone-skill from development
  → Implement wave completely
  → Merge directly to development
```

**Don't Create Wave Branch If**:
- ❌ Wave is part of multi-wave feature (commit directly to feature branch)
- ❌ Simple change (work directly on development)

---

## Workflow Examples

### Example 1: Multi-Feature Epic

**Scenario**: Epic 1 (Progressive Coherence) has 3 features with multiple waves each

**Workflow**:
```bash
# 1. Create epic branch from development
git checkout development
git pull origin development
git checkout -b epic-1-progressive-coherence
git push -u origin epic-1-progressive-coherence

# 2. Create feature branch from epic for Feature 1.10
git checkout -b feature-1.10-infrastructure epic-1-progressive-coherence
git push -u origin feature-1.10-infrastructure

# 3. Implement Wave 1.10.1 directly on feature branch (NO wave branch)
# ... implement wave 1.10.1 ...
git add .
git commit -m "feat(wave-1.10.1): Implement catalog change monitor"
git push

# 4. Implement Wave 1.10.2 on same feature branch
# ... implement wave 1.10.2 ...
git add .
git commit -m "feat(wave-1.10.2): Implement template staleness detection"
git push

# 5. Implement Wave 1.10.3 on same feature branch
# ... implement wave 1.10.3 ...
git add .
git commit -m "feat(wave-1.10.3): Implement impact analysis"
git push

# 6. After all waves for feature 1.10 complete, merge feature → epic
gh pr create --base epic-1-progressive-coherence --head feature-1.10-infrastructure \
  --title "Feature 1.10: Infrastructure Complete" \
  --body "Completed waves 1.10.1, 1.10.2, 1.10.3"

# 7-9. Repeat for other features in epic...

# 10. After ALL features in epic complete, merge epic → development
git checkout epic-1-progressive-coherence
git pull origin epic-1-progressive-coherence
gh pr create --base development --head epic-1-progressive-coherence \
  --title "Epic 1: Progressive Coherence Complete" \
  --body "Completed features 1.10, 1.4, 1.5"

# 11. After epic merged to development, merge to main
git checkout development
git pull origin development
gh pr create --base main --head development
```

---

### Example 2: Standalone Wave

**Scenario**: Implement single new skill (Wave 3.1.1), not part of epic

**Workflow**:
```bash
# 1. Create wave branch from development
git checkout development
git pull origin development
git checkout -b wave-3.1.1-standalone-skill
git push -u origin wave-3.1.1-standalone-skill

# 2. Implement wave completely
# ... implement skill ...
git add .
git commit -m "feat(wave-3.1.1): Create new standalone skill"
git push

# 3. Merge wave → development
gh pr create --base development --head wave-3.1.1-standalone-skill \
  --title "Wave 3.1.1: Standalone Skill Complete"
```

---

### Example 3: Standalone Feature (No Epic)

**Scenario**: Feature 4.2 (Reporting Enhancement) has 2 waves, not part of epic

**Workflow**:
```bash
# 1. Create feature branch from development
git checkout development
git pull origin development
git checkout -b feature-4.2-reporting-enhancement
git push -u origin feature-4.2-reporting-enhancement

# 2. Implement Wave 4.2.1 directly on feature branch
# ... implement wave 4.2.1 ...
git add .
git commit -m "feat(wave-4.2.1): Add export functionality"
git push

# 3. Implement Wave 4.2.2 directly on feature branch
# ... implement wave 4.2.2 ...
git add .
git commit -m "feat(wave-4.2.2): Add visualization options"
git push

# 4. Merge feature → development
gh pr create --base development --head feature-4.2-reporting-enhancement \
  --title "Feature 4.2: Reporting Enhancement Complete" \
  --body "Completed waves 4.2.1, 4.2.2"
```

---

### Example 4: Hotfix

**Scenario**: Critical security vulnerability needs immediate fix

**Workflow**:
```bash
# 1. Create hotfix branch from development
git checkout development
git pull origin development
git checkout -b hotfix-security-vulnerability
git push -u origin hotfix-security-vulnerability

# 2. Implement fix
# ... implement fix ...
git add .
git commit -m "fix(hotfix): Patch security vulnerability CVE-2025-1234"
git push

# 3. Merge to development
gh pr create --base development --head hotfix-security-vulnerability \
  --title "Hotfix: Security Vulnerability CVE-2025-1234"

# 4. If critical, create expedited PR to main
gh pr create --base main --head development \
  --title "Emergency Release: Security Fix"
```

---

## Integration with Lighthouse LM

### Skill Returns Branch Recommendation

**Input from user/agent**:
```
"I'm implementing Epic 1 which has 3 features, each with 2-3 waves. What branch strategy should I use?"
```

**Skill output**:
```markdown
## Branch Strategy Recommendation

**Work Type**: Multi-feature epic (3 features, 8 total waves)

**Recommended Strategy**: Epic → Feature → Commits

### Step-by-Step:

1. **Create Epic Branch**
   ```bash
   git checkout development
   git pull origin development
   git checkout -b epic-1-progressive-coherence
   git push -u origin epic-1-progressive-coherence
   ```

2. **For Each Feature** (1.10, 1.4, 1.5):
   ```bash
   git checkout epic-1-progressive-coherence
   git checkout -b feature-1.10-infrastructure epic-1-progressive-coherence
   git push -u origin feature-1.10-infrastructure
   ```

3. **Implement Waves as Commits** (on feature branch):
   ```bash
   # Wave 1.10.1
   git add .
   git commit -m "feat(wave-1.10.1): Implement catalog change monitor"
   git push

   # Wave 1.10.2
   git add .
   git commit -m "feat(wave-1.10.2): Implement template staleness detection"
   git push

   # ... continue for all waves ...
   ```

4. **Merge Feature → Epic** (after all waves complete):
   ```bash
   gh pr create --base epic-1-progressive-coherence --head feature-1.10-infrastructure
   ```

5. **Merge Epic → Development** (after all features complete):
   ```bash
   gh pr create --base development --head epic-1-progressive-coherence
   ```

### Why This Strategy:
- ✅ Isolates epic work from development
- ✅ Organizes waves by feature
- ✅ No wave branches (commit directly to feature)
- ✅ Progressive integration (feature → epic → development)
```

---

## Questions to Ask User

**What are you implementing?** (required)
- Single wave
- Feature with multiple waves
- Epic with multiple features
- Bug fix or documentation

**Is this part of existing epic?** (if feature)
- Yes (create feature branch from epic)
- No (create feature branch from development)

**How many waves in feature?** (if feature)
- 1 wave → Use wave branch
- 2+ waves → Use feature branch

**How many features in epic?** (if epic)
- 1 feature → Skip epic branch, use feature branch
- 2+ features → Use epic branch

**Is this urgent/critical?** (if bug fix)
- Yes → Use hotfix branch
- No → Work on development or create wave branch

---

## Available Resources

### References

- **references/branching-scenarios.md** — Detailed scenarios with examples
- **references/branch-naming-conventions.md** — Naming standards and examples
- **references/merge-strategies.md** — When to merge, how to merge, merge conflicts

---

## Success Criteria

- ✅ Agent understands which branch type to use
- ✅ Agent knows where to create branch from (development, epic, feature)
- ✅ Agent knows when to commit directly vs. create branch
- ✅ Agent follows Progressive Coherence principles in branching
- ✅ Branch names follow conventions
- ✅ Merge targets correct

---

## Tips for Effective Branching

1. **Default to development** for small changes
2. **Use wave branches** only for standalone single waves
3. **Commit waves directly** to feature branches (no wave branches)
4. **Create epic branches** only for multi-feature epics
5. **Keep branch names descriptive** but concise
6. **Merge frequently** to avoid long-lived divergence
7. **Use conventional commit** format for wave commits

---

**Last Updated**: 2025-01-30
