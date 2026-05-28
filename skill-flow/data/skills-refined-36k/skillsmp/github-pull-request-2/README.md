# GitHub Pull Request Skill

This directory contains the GitHub Pull Request Management skill for The Simpsons API project.

## Files

### Core Skill

- **SKILL.md** - Complete skill documentation with workflows, patterns, and best practices

### Release Management

- **RELEASE_TAGGING.md** - Guide for automated PR merge and release tag creation
- **scripts/merge-and-release.sh** - Automated merge + semantic versioning script

## Quick Start

### Create a Pull Request

```bash
gh pr create --title "feat: your feature" --body-file pr-body.md --base main
```

### Merge PR and Create Release Tag

```bash
./scripts/merge-and-release.sh 42          # Merge PR #42 and create release
./scripts/merge-and-release.sh 42 --dry-run # Preview first
```

## Key Workflows

### 1. PR Creation

- Create PR with proper title format
- Add description and checklist
- Assign reviewers
- Add labels

### 2. PR Management

- Update PR content
- Add/remove labels
- Assign reviewers
- Add comments

### 3. PR Merge

- Validate PR is ready
- Squash and merge
- Automatic release tagging
- Generate GitHub release

## File Structure

```
.github/skills/github-pull-request/
├── SKILL.md                    # Main skill documentation
├── RELEASE_TAGGING.md          # Release tagging guide
├── README.md                   # This file
└── scripts/
    └── merge-and-release.sh    # Automation script
```

## Documentation

- **SKILL.md** - Start here for complete skill documentation
- **RELEASE_TAGGING.md** - Guides for release tagging workflow
- **README.md** - This overview

## Related Skills

- [Vercel Environment Sync](../) - Environment variable management
- [Component Development](../) - React component patterns
- [Server Actions Patterns](../) - Next.js server actions

## Support

For questions about PR workflows, see [SKILL.md](./SKILL.md).
For release tagging, see [RELEASE_TAGGING.md](./RELEASE_TAGGING.md).
