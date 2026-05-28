# Example: Claude Plugin Release Output

Example output from running `/agents:release patch` on a Claude Code plugin.

## Command
```bash
/agents:release patch
```

## Output

```
=== PROJECT DETECTION ===
Detected: Claude Code Plugin
Project Type: claude-plugin

=== ENVIRONMENT CHECK ===
git version 2.43.0
python3 3.12.1
bump-my-version 0.26.0
Environment OK

=== GIT STATUS ===
Branch: main

Uncommitted changes:
 M agents/core-development/frontend-developer.md
 M skills/release/SKILL.md
Total: 2 file(s)

Recent commits (not pushed):
daed188 chore(agents): bump version to 0.7.1
2fc5702 fix: sync bumpversion.toml to current version 0.7.0

=== CURRENT VERSION ===
Plugin version: 0.7.1
Last tag: agents-v0.7.1

=== SDLC VALIDATION ===
Running comprehensive validation suite...

============================================================
RELEASE VALIDATION REPORT
============================================================
Project Type: claude-plugin
Project Path: /Users/user/Projects/agents
Semver Recommendation: patch
============================================================

PASSED:
  [OK] changelog: CHANGELOG.md has [Unreleased] section
  [OK] breaking-changes: No breaking changes detected
  [OK] ci-config: Found 1 CI workflow(s) in workflows
  [OK] plugin.json: Valid plugin.json (v0.7.1)
  [OK] agents: Found 116 agents, 10 with valid frontmatter
  [OK] skills: Found 47 skill directories, 44 with SKILL.md
  [OK] commands: Found 1 commands

============================================================
RESULT: READY FOR RELEASE
============================================================

Validation exit code: 0

=== UNCOMMITTED CHANGES ===
 agents/core-development/frontend-developer.md | 15 ++++++++-------
 skills/release/SKILL.md                       | 42 +++++++++++++++++++++++++++
 2 files changed, 50 insertions(+), 7 deletions(-)

? There are uncommitted changes. Include them in this release?
> Commit all changes (Recommended)

Staging all changes...
Generating commit message...

git add -A
git commit -m "feat(agents): update frontend-developer, add release skill"

[main abc1234] feat(agents): update frontend-developer, add release skill
 2 files changed, 50 insertions(+), 7 deletions(-)
 create mode 100644 skills/release/SKILL.md

=== VERSION BUMP ===
Using bump-my-version...

bump-my-version bump patch

Bumping version 0.7.1 → 0.7.2
  Updated .claude-plugin/plugin.json
  Updated CHANGELOG.md

[main def5678] chore(agents): bump version to 0.7.2
 2 files changed, 4 insertions(+), 2 deletions(-)
 create mode 100644 agents-v0.7.2

=== VERSION VERIFICATION ===
New commits:
def5678 chore(agents): bump version to 0.7.2
abc1234 feat(agents): update frontend-developer, add release skill
daed188 chore(agents): bump version to 0.7.1

New tags:
agents-v0.7.2
agents-v0.7.1
agents-v0.7.0

=== PUSHING RELEASE ===
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 10 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 1.42 KiB | 1.42 MiB/s, done.
Total 8 (delta 5), reused 0 (delta 0), pack-reused 0
To github.com:user/agents.git
   daed188..def5678  main -> main
 * [new tag]         agents-v0.7.2 -> agents-v0.7.2

==========================================
          RELEASE COMPLETE
==========================================

Project:  agents
Type:     claude-plugin
Version:  0.7.1 -> 0.7.2
Release:  patch

Validation:
  - Tests:     PASSED
  - Lint:      PASSED
  - Coverage:  N/A (plugin)
  - Security:  PASSED

Git Status:
  - Branch:    main
  - Tags:      agents-v0.7.2
  - Remote:    Pushed

==========================================
```

## Post-Release Checklist

- [ ] Monitor CI pipeline
- [ ] Verify tag on GitHub: https://github.com/user/agents/releases/tag/agents-v0.7.2
- [ ] Check plugin availability in marketplace
- [ ] Update downstream dependencies if needed
