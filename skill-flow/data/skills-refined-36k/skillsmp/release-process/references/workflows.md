# Release Workflows

Step-by-step workflows for common release scenarios.

## Workflow 1: Simple Patch Release (Single Project)

**When:** Bug fix + documentation updates, no new features

**Time to complete:** 10-15 minutes

### Step 1: Verify What's Changed

```bash
git status          # See all modified files
git diff            # See exact changes
git log -1          # See last commit
```

**Ask yourself:** Do all changes fit PATCH scope?
- Only bug fixes? ✓
- Only documentation/wording? ✓
- No new features? ✓
→ Proceed to Step 2

**If any changes are MINOR or MAJOR scope:**
→ Jump to Workflow 2 or 3 instead

### Step 2: Find Current Version

```bash
grep '"version"' package.json
# or
grep 'version:' SKILL.md
```

**Current:** 1.2.3

### Step 3: Bump Version (PATCH)

Increment Z: 1.2.3 → 1.2.4

**Update all version files:**
- `package.json`: `"version": "1.2.4"`
- `SKILL.md`: `version: 1.2.4`
- Any other file with version

### Step 4: Write CHANGELOG Entry

```markdown
## [1.2.4] - 2026-01-21

### Fixed
- Fix timeout bug in API requests
- Fix typo in README documentation
```

**Rules:**
- Date in ISO format
- Use "Fixed" section for bug fixes
- Describe user impact, not internal changes
- Verify each entry is in `git diff`

### Step 5: Stage and Commit

```bash
git add package.json SKILL.md CHANGELOG.md
git commit -m "Release version 1.2.4

Fixed:
- Timeout bug in API requests
- Typo in README
"
git tag v1.2.4
```

### Step 6: Verify

```bash
git log -1          # Confirm commit
git tag -l          # Confirm tag
grep '"version"' package.json  # Confirm version updated
```

---

## Workflow 2: Feature Release (New Capability)

**When:** Adding new features or capabilities, backward compatible

**Time to complete:** 15-30 minutes (depending on feature count)

### Step 1: Verify Scope

```bash
git diff            # See all changes
```

**Ask:** Do changes include:
- Only new features? ✓
- Only new capabilities? ✓
- No breaking changes? ✓
- No bug fixes only? (optional)
→ Proceed

**If any breaking changes exist:**
→ Jump to Workflow 3 instead

### Step 2: Find Current Version

```bash
grep '"version"' package.json
```

**Current:** 1.2.3

### Step 3: Bump Version (MINOR)

Increment Y, reset Z: 1.2.3 → 1.3.0

**Update all version files:**
- `package.json`: `"version": "1.3.0"`
- Child skill versions if updated

### Step 4: Write CHANGELOG Entry

```markdown
## [1.3.0] - 2026-01-22

### Added
- Support for encrypted document transport
- New `--dry-run` flag for preview mode
- Webhook endpoints for real-time updates

### Changed
- Improved error messages with actionable suggestions

### Fixed
- Fix timeout in request handling
```

**Rules:**
- Document what users can NOW do
- Be specific about new capabilities
- Include any bug fixes in separate section
- Verify against `git diff`

### Step 5: Stage and Commit

```bash
git add package.json skills/*/SKILL.md CHANGELOG.md
git commit -m "Release version 1.3.0

Added:
- Support for encrypted document transport
- New --dry-run flag for preview mode
- Webhook endpoints for real-time updates

Changed:
- Improved error messages
"
git tag v1.3.0
```

---

## Workflow 3: Breaking Change Release (MAJOR)

**When:** Removing features, changing API, incompatible changes

**Time to complete:** 20-45 minutes (includes migration planning)

### Step 1: Identify Breaking Changes

```bash
git diff            # See all changes
```

**Ask:** What's breaking?
- Command removed/renamed? → MAJOR
- API changed incompatibly? → MAJOR
- Output format changed? → MAJOR
- Config structure changed? → MAJOR
- Required migration guide? → MAJOR

### Step 2: Find Current Version

```bash
grep '"version"' package.json
```

**Current:** 1.5.2

### Step 3: Bump Version (MAJOR)

Increment X, reset Y and Z: 1.5.2 → 2.0.0

**Update all version files:**
- `package.json`: `"version": "2.0.0"`
- All child components updated accordingly

### Step 4: Create Migration Guide

Before writing changelog, create migration guide in README or separate file:

**Example README section:**

```markdown
## Migrating from v1.x to v2.0

### Command Changes

#### Before (v1.x)
```bash
validate --file config.yaml
```

#### After (v2.0)
```bash
verify --config config.yaml
```

### Config Format Changes

V2.0 uses JSON format instead of YAML:

```json
{
  "version": "2.0",
  "settings": { ... }
}
```
```

### Step 5: Write CHANGELOG Entry

```markdown
## [2.0.0] - 2026-01-23

### Added
- Migration guide in README.md
- New verification workflow

### Changed
- **BREAKING**: Renamed 'validate' command to 'verify'
- **BREAKING**: Config format changed from YAML to JSON
- **BREAKING**: API now requires authentication header

### Removed
- Deprecated 'validate' command (use 'verify' instead)
- Support for YAML config files (use JSON instead)
- Anonymous API access (authentication now required)

### Fixed
- Fix handling of special characters in paths
```

**Rules:**
- Mark all breaking changes with **BREAKING**
- Explain why each change was necessary
- Provide migration path for each change
- Include both "Changed" (what's different) and "Removed" (what's gone)

### Step 6: Stage and Commit

```bash
git add package.json CHANGELOG.md README.md
git commit -m "Release version 2.0.0

BREAKING CHANGES:
- Renamed 'validate' command to 'verify'
- Config format changed from YAML to JSON
- API now requires authentication header

See README.md for migration guide.
"
git tag v2.0.0
```

---

## Workflow 4: Scope Creep (Multiple Bracket Jumps)

**When:** Discovering work across multiple brackets during one cycle

**Time to complete:** Varies by scope

### Scenario

```
Last commit: 1.2.0
Start work: Bug fix discovered → 1.2.1 (patch frozen)
Continue: New feature needed → 1.3.0 (minor frozen)
Continue: Breaking change required → 2.0.0 (major frozen)
More work: Another bug found → 2.0.0 (major, don't bump)
Commit: 2.0.0
```

### Step 1: Document Discoveries

As you work, keep notes of what's being found:

```
Discoveries:
- Bug in request handler (PATCH)
- Need new encryption support (MINOR)
- API changes incompatible (MAJOR)
- Another bug in logging (PATCH, within MAJOR scope)
```

### Step 2: Apply Bracket Jumps

```bash
# Start with bug fix
Current version: 1.2.0
Bump to: 1.2.1 (patch bracket)

# Discover new feature
Current version: 1.2.1
Jump to: 1.3.0 (minor bracket, reset Z)

# Discover breaking change
Current version: 1.3.0
Jump to: 2.0.0 (major bracket, reset Y, Z)

# Discover another bug
Current version: 2.0.0
Stay at: 2.0.0 (already in major, don't bump)
```

### Step 3: Update Version Files

Update to final version: 2.0.0

### Step 4: Write Single CHANGELOG Entry

Document all work under the final version:

```markdown
## [2.0.0] - 2026-01-24

### Added
- New encryption algorithm support
- Migration guide in README.md

### Changed
- **BREAKING**: API endpoint changed from /users to /api/users

### Fixed
- Fix timeout bug in request handler
- Fix memory leak in logging

### Removed
- Old /users endpoint (use /api/users)
```

**Key:** Single entry for 2.0.0 documents the full journey from 1.2.0

### Step 5: Commit

```bash
git add package.json CHANGELOG.md README.md
git commit -m "Release version 2.0.0

Added:
- New encryption algorithm support

Changed:
- **BREAKING**: API endpoint changed from /users to /api/users

Fixed:
- Timeout bug in request handler
- Memory leak in logging
"
git tag v2.0.0
```

---

## Workflow 5: Multi-Component Release

**When:** Updating multiple components in monorepo or plugin

**Time to complete:** 20-40 minutes

### Scenario

```
Plugin: 1.2.0 (no changes)
Skill-A: 1.0.0 → 1.1.0 (new feature)
Skill-B: 1.0.0 → 1.0.1 (bug fix)
Skill-C: 1.0.0 (no changes)
```

### Step 1: Identify Changed Components

```bash
git status              # See which files changed
git diff --stat         # Summary by directory
```

**Result:**
- Skills/skill-a/: Modified (new feature)
- Skills/skill-b/: Modified (bug fix)
- Skills/skill-c/: Unchanged

### Step 2: Bump Each Component

**Skill-A** (new feature):
- Current: 1.0.0
- Scope: MINOR
- New: 1.1.0

**Skill-B** (bug fix):
- Current: 1.0.0
- Scope: PATCH
- New: 1.0.1

**Skill-C** (no changes):
- Stays: 1.0.0

### Step 3: Determine Parent Version

**Rule: Parent ≥ highest child**
- Highest child: skill-a at 1.1.0
- Parent current: 1.2.0
- Parent new: 1.2.0 (already ≥ 1.1.0) OR bump to 1.3.0 if plugin also has changes

**Decision:**
- Parent stays 1.2.0 (only coordinating children) OR
- Parent bumps to 1.3.0 (if plugin itself has changes to document)

### Step 4: Update Version Files

```bash
# Skill-A
skills/skill-a/SKILL.md: version: 1.1.0

# Skill-B
skills/skill-b/SKILL.md: version: 1.0.1

# Parent
plugin.json: version: 1.3.0
```

### Step 5: Write CHANGELOG

```markdown
## [1.3.0] - 2026-01-25

### Added (skill-a)
- Support for encrypted documents
- New parameter for custom rules

### Fixed (skill-b)
- Fix timeout in request handling
```

### Step 6: Stage and Commit

```bash
git add skills/skill-a/SKILL.md skills/skill-b/SKILL.md \
        plugin.json CHANGELOG.md
git commit -m "Release version 1.3.0

skill-a: Added support for encrypted documents
skill-b: Fixed timeout in request handling
"
git tag v1.3.0
```

---

## Pre-Release Versions

For testing before stable release:

### Workflow

```
Development: 2.0.0-alpha.1 (early testing)
            → 2.0.0-alpha.2 (more testing)
            → 2.0.0-beta.1 (beta testing)
            → 2.0.0-rc.1 (release candidate)
Stable: 2.0.0 (production ready)
```

### Implementation

Each pre-release is a separate version bump:

```bash
# Pre-release 1
npm version prerelease  # 2.0.0-alpha.0
git tag v2.0.0-alpha.0

# Pre-release 2
npm version prerelease  # 2.0.0-alpha.1
git tag v2.0.0-alpha.1

# ... more pre-releases ...

# Stable
npm version major       # 2.0.0
git tag v2.0.0
```

### CHANGELOG for Pre-Releases

Include pre-release entry:

```markdown
## [2.0.0-rc.1] - 2026-01-20
### Added
- (pre-release features)

## [2.0.0] - 2026-01-25
### Added
- (final features after RC testing)
```

---

## Troubleshooting Common Issues

### Issue: "I already updated version files, can I fix it?"

**Don't use `git commit --amend`**. Instead:
1. Create new commit with correct version
2. Mark previous commit as "reverted" if already pushed
3. Explain in commit message

### Issue: "I forgot to update a version file"

Don't amend. Create a new commit:

```bash
git add forgotten-file
git commit -m "Update version in forgotten file"
```

Then tag the correct commit.

### Issue: "Version doesn't match git diff"

Stop. Investigate what's different:

```bash
git diff
git status
```

Fix the discrepancy before committing.

### Issue: "I documented something not in git diff"

Remove it from CHANGELOG. Only document changes that exist in code.

### Issue: "Should I bump to pre-release version?"

Use pre-releases if:
- Testing major changes with team before stable
- Want multiple test cycles before release
- Need feedback on new API/behavior

Skip pre-releases if:
- Simple patch releases
- Internal testing only
- No public users to test
