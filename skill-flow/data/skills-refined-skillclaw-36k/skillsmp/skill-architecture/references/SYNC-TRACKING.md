**Skill**: [Skill Architecture](../SKILL.md)

# Marketplace Sync Tracking

Track content merged from Anthropic's skill-creator marketplace for future updates.

## Last Sync

- **Date**: 2025-11-07
- **Marketplace Version**: `example-skills@anthropic-agent-skills` commit `c74d647`
- **Sync Method**: Manual merge (comprehensive)
- **Synced By**: User (Terry) via Claude Code

## Content Sources

### From Marketplace skill-creator (209 lines total)

**Merged into SKILL.md** (245 lines):

- [x] 6-step creation process (Steps 1-6)
- [x] Progressive disclosure explanation (3-level loading)
- [x] Bundled resources guidance (scripts/, references/, assets/)
- [x] YAML frontmatter requirements
- [x] Good vs Bad description examples
- [x] Writing style guidance (imperative form)

**Extracted to references/**:

- [x] 4 structural patterns → `structural-patterns.md`
- [x] Progressive disclosure deep-dive → `progressive-disclosure.md`
- [x] Script usage documentation → `scripts-reference.md`

**Script References** (not copied, links only):

- [x] init_skill.py - Location documented
- [x] package_skill.py - Location documented
- [x] quick_validate.py - Location documented

### From Original \_agent-skill-builder.disabled (91 lines + 5 references)

**Preserved Content**:

- [x] CLI-specific features (allowed-tools restriction)
- [x] Security focus (threat model, CVE references)
- [x] File naming conventions (SKILL.md vs Skill.md)
- [x] Token efficiency patterns
- [x] Advanced topics (CLI vs API differences)

**Existing References Kept**:

- [x] security-practices.md (254 words) - Your unique CVE content
- [x] token-efficiency.md (129 words)
- [x] validation-reference.md (382 words)
- [x] advanced-topics.md (465 words)
- [x] creation-workflow.md (335 words) - To be enhanced

### User Additions (Terry's Conventions)

**Integrated into SKILL.md**:

- [x] Absolute path requirements (iTerm2 Cmd+click)
- [x] Unix-only platform scope
- [x] PEP 723 inline dependencies
- [x] Link to ~/.claude/CLAUDE.md
- [x] Link to specifications/ (OpenAPI 3.1.1)
- [x] `uv run` preference for Python

**New References Created**:

- [x] structural-patterns.md - Marketplace Pattern 1-4 extracted
- [x] progressive-disclosure.md - Context management deep-dive
- [x] scripts-reference.md - Marketplace script usage guide
- [x] SYNC-TRACKING.md - This file

## Marketplace File Inventory

**As of commit c74d647**:

```
skill-creator/
├── SKILL.md (209 lines)
├── LICENSE.txt
└── scripts/
    ├── init_skill.py (303 lines)
    ├── package_skill.py (110 lines)
    └── quick_validate.py (65 lines)
```

**Scripts**: Referenced, not copied. See `scripts-reference.md` for usage.

## Future Sync Process

### 1. Check for Marketplace Updates

```bash
cd plugins/marketplaces/anthropic-agent-skills
git fetch origin
git log c74d647..origin/main -- skill-creator/
```

### 2. Review Changes

```bash
git diff c74d647..origin/main -- skill-creator/SKILL.md
```

### 3. Selective Merge Decision Matrix

| Change Type             | Action                         | Rationale                          |
| ----------------------- | ------------------------------ | ---------------------------------- |
| New best practices      | Merge to SKILL.md              | Keep guidance current              |
| Script improvements     | Update references              | Don't copy, just update paths/docs |
| New structural patterns | Add to structural-patterns.md  | Expand pattern library             |
| Updated examples        | Evaluate & merge               | Improve clarity                    |
| API changes             | Skip                           | CLI-only skill                     |
| Security guidance       | Merge to security-practices.md | Critical updates                   |

### 4. Update This File

After syncing:

- Update "Last Sync" section with new commit SHA
- Document merged changes in "Content Sources"
- Update file inventory if structure changed

### 5. Test

```bash
# Verify skill loads
claude # Test: "How to create a skill?"

# Check references work
claude # Test: "What are the 4 structural patterns?"
```

## Version History

| Date       | Marketplace Commit | Changes Merged              | Notes                                                                        |
| ---------- | ------------------ | --------------------------- | ---------------------------------------------------------------------------- |
| 2025-11-07 | c74d647            | Initial comprehensive merge | Created skill-architecture from \_agent-skill-builder.disabled + marketplace |

## Marketplace vs User Skill Positioning

**Marketplace `skill-creator`**:

- Role: Executable tooling provider
- Focus: Scripts (init, package, validate)
- Auto-updates: Yes
- When used: Direct script execution needs

**User `skill-architecture`**:

- Role: Comprehensive creation guide
- Focus: Best practices, security, CLI features, your conventions
- Auto-updates: Manual sync (this process)
- When used: Learning, guidance, advanced topics

**Relationship**: Complementary, not competitive. Both enabled.

## Questions for Future Syncs

**Before merging new marketplace content, consider**:

1. **Does it duplicate existing content?**
   - If yes: Consolidate or reference

2. **Is it CLI-specific or API-only?**
   - API-only: Skip

3. **Does it conflict with user conventions?**
   - If yes: Adapt to Terry's standards

4. **Is it security-relevant?**
   - If yes: High priority merge

5. **Can it be referenced vs copied?**
   - Scripts: Always reference
   - Documentation: Consider progressive disclosure

## Contact for Marketplace Updates

**Marketplace**: https://github.com/anthropics/skills
**Issues**: Report at anthropics/skills repo
**PRs**: Contribute improvements back to marketplace

## Maintenance Notes

**Estimated Sync Frequency**: Quarterly (every 3 months)
**Sync Complexity**: Moderate (30-60 minutes)
**Risk**: Low (user skill is customized, selective merge)
**Automation Potential**: Low (requires judgment on content relevance)
