# Mercurial Team Collaboration

This guide covers collaborative workflows and best practices for Mercurial in a team environment.

## Team Collaboration Workflows

### Centralized Workflow

Suitable for small teams or scenarios requiring centralized control.

```bash
# Developer A
hg clone https://central-repo/repo
hg update master
# Develop
hg commit -m "New feature"
hg push -r .

# Developer B
hg pull -u
# Develop
hg commit -m "Another feature"
hg pull  # Pull A's changes
hg merge
hg commit -m "Merge A's changes"
hg push -r .
```

### Feature Branch Workflow

Recommended for medium to large teams, using bookmarks.

```bash
# 1. Create feature branch from main branch
hg update master
hg bookmark feature/user-auth

# 2. Develop on feature branch
hg commit -m "Add auth module"
hg commit -m "Implement login UI"

# 3. Request code review
# Push feature branch (requires server support)
hg push -B feature/user-auth

# 4. Continue development after feedback
hg commit -m "Fix review issues"

# 5. Merge into main branch
hg update master
hg pull
hg merge feature/user-auth
hg commit -m "Merge user auth feature"
hg push -r .

# 6. Cleanup feature branch
hg bookmark -d feature/user-auth
hg push -B feature/user-auth
```

### Release Branch Workflow

Suitable for projects requiring version releases.

```bash
# 1. Create release branch from development branch
hg update develop
hg branch release-1.0
hg commit -m "Start 1.0 release"

# 2. Prepare for release
hg commit -m "Update version to 1.0.0"
hg commit -m "Fix release issues"

# 3. Create tag
hg tag v1.0.0

# 4. Merge into main branch
hg update master
hg merge release-1.0
hg commit -m "Merge 1.0.0 release"
hg push -r .

# 5. Close release branch
hg commit --close-branch -m "Close 1.0 release branch"

# 6. Return to development branch
hg update develop
```

### Maintenance Branch Workflow

Used for long-term support of stable versions.

```bash
# 1. Create maintenance branch from release tag
hg update v1.0.0
hg branch maintain-1.0
hg commit -m "Create 1.0 maintenance branch"
hg push -r .

# 2. Fix bug in maintenance branch
hg commit -m "Fix critical security vulnerability"
hg push -r .

# 3. Merge fix into main branch (if applicable)
hg update master
hg merge maintain-1.0
hg commit -m "Merge security fix"
hg push -r .
```

## Multi-Repository Collaboration

### Fork and Pull (Tiered Repositories)

```bash
# 1. Create fork
hg clone https://upstream/repo my-repo
cd my-repo

# 2. Add upstream repository
hg paths
# default = https://upstream/repo
# upstream = https://upstream/repo

# 3. Develop in fork
hg bookmark feature/my-change
hg commit -m "My changes"
hg push -B feature/my-change

# 4. Pull upstream updates
hg pull -u upstream

# 5. Push after resolving conflicts
hg resolve --mark
hg commit -m "Merge upstream updates"
hg push -B feature/my-change
```

### Multiple Remote Repositories

```bash
# Configure multiple remote repositories
# In .hg/hgrc:
[paths]
default = https://primary-repo.example.com
backup = https://backup-repo.example.com
upstream = https://upstream.example.com

# Push to specific repository
hg push backup

# Pull from specific repository
hg pull upstream
```

## Code Review Workflow

### Using Built-in Tools

```bash
# 1. Create patch bundle for review
hg bundle review.hg -r "ancestors('tip') and not ancestors('last-reviewed')"

# 2. Send bundle for review
# (Send via email or other means)

# 3. Reviewer applies bundle
hg unbundle review.hg

# 4. View changes
hg update -r tip
hg log -G
hg diff

# 5. Feedback and modification
# Developer modifies based on feedback
hg commit --amend  # or create new commit

# 6. Resend for review
hg bundle review-v2.hg -r "ancestors('tip') and not ancestors('last-reviewed')"
```

### Using Code Review Platforms

Most code review platforms (e.g., Bitbucket, RhodeCode) natively support Mercurial:

```bash
# Create pull request
# 1. Push feature branch
hg push -B feature/my-change

# 2. Create PR on platform
# (Via Web interface or API)

# 3. Update PR
hg commit -m "Fix review feedback"
hg push -B feature/my-change
```

## Tag Management

### Create Tag

```bash
# Create lightweight tag
hg tag v1.0.0

# Create annotated tag
hg tag -m "1.0.0 release" v1.0.0

# Specify local tag
hg tag -l v1.0.0-local

# Tag specific revision
hg update 1234
hg tag v1.0.0
```

### List Tags

```bash
# List all tags
hg tags

# List local tags
hg tags -l

# View tag details
hg log -r v1.0.0
```

### Delete Tag

```bash
# Delete tag (creates a new "removal" commit)
hg tag --remove v1.0.0

# Delete local tag
hg tag -l --remove v1.0.0-local
```

### Tag Best Practices

```bash
# Version tag format
v1.0.0
v1.1.0-beta
v1.2.0-rc1

# Release candidate tag format
rc-1.0.0
rc-1.0.0-rc2

# Hotfix tag format
hotfix-1.0.1
hotfix-1.0.1-critical
```

## Permission Management

### User Permissions

Configure on server side (e.g., RhodeCode, Bitbucket):

```bash
# Common permission levels
# - read: Read-only
# - write: Push allowed
# - admin: Administrator
# - none: No permission

# Example: Read-only access
[hooks]
pretxnchangegroup.access = python:hgext.accesscontrol.check_access
```

### Branch Permissions

```bash
# Restrict push to main branch
[hooks]
prechangegroup.protect-main = python:check_branch.main_only

# In check_branch.py:
def check_branch_main_only(ui, repo, hooktype, **kwargs):
    for rev in repo.changelog.revs(kwargs['node']):
        ctx = repo[rev]
        if ctx.branch() == 'default' and not ctx.user().endswith('@trusted.com'):
            ui.warn('Only trusted users can push to default branch\n')
            return True
    return False
```

## Hooks

### Client-side Hooks

Configure in `~/.hgrc`:

```ini
[hooks]
# Check before commit
pre-commit = python:check_code_style.main

# Check before push
pre-push = python:run_tests.main

# Notify after update
post-update = python:notify_team.main
```

### Server-side Hooks

```ini
[hooks]
# Check commit message format
pretxnchangegroup.check_message = python:check_commit_message.main

# Run test suite
pretxnchangegroup.run_tests = python:run_test_suite.main

# Notify team
changegroup.notify = python:notify_team.main
```

### Common Hook Scripts

```python
# check_commit_message.py
import re

def check_commit_message(ui, repo, hooktype, node=None, **kwargs):
    for rev in repo.changelog.revs(node):
        ctx = repo[rev]
        message = ctx.description()
        # Check commit message format
        if not re.match(r'^\w+: ', message):
            ui.warn('Commit message should start with "Type: "\n')
            ui.warn('Example: "feat: Add new feature" or "fix: Fix bug"\n')
            return True
    return False
```

## Backup and Recovery

### Create Backup

```bash
# Full clone backup
hg clone /path/to/repo /path/to/backup

# Create bundle backup
hg bundle backup.hg --all

# Create incremental backup
hg bundle backup-incremental.hg -r "tip~100::tip"
```

### Recover from Backup

```bash
# Recover from clone
hg clone /path/to/backup /path/to/restored

# Recover from bundle
hg clone empty-repo
cd empty-repo
hg unbundle /path/to/backup.hg
```

### Automatic Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/mercurial"
REPO_DIR="/path/to/repo"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR

# Create bundle
cd $REPO_DIR
hg bundle $BACKUP_DIR/repo-$DATE.hg --all

# Keep recent 7 days backup
find $BACKUP_DIR -name "repo-*.hg" -mtime +7 -delete
```

## Multi-person Merge Strategies

### 3-way Merge

```bash
# 1. Get latest code
hg pull -u

# 2. View incoming changes
hg incoming

# 3. Preview before merge
hg merge --preview

# 4. Perform merge
hg merge

# 5. Resolve conflicts
hg resolve --mark

# 6. Commit merge
hg commit -m "Merge team updates"
```

### Continuous Merge

```bash
# When multiple developers push simultaneously
hg pull
hg update
hg merge default
hg merge another-branch
hg commit -m "Merge multiple branches"
```

### Arbitrary Merge

```bash
# Specify merge tool
hg merge --tool=internal:local   # Use local version
hg merge --tool=internal:other   # Use other version
hg merge --tool=internal:base    # Use base version
hg merge --tool=internal:union   # Merge all changes
```

## Performance Optimization

### Large Repository Optimization

```bash
# Disable some extensions to speed up
# In ~/.hgrc:
[extensions]
# hgext.purge =
# hgext.largefiles =

# Use clone -U to speed up cloning
hg clone -U https://large-repo/repo
hg update -r tip
```

### Network Optimization

```bash
# Use compression
[server]
uncompressed = false

# Increase buffer size
[http]
timeout = 120
maxrequests = 100
```

## Security Best Practices

### HTTPS Authentication

```ini
[auth]
example.prefix = https://example.com
example.username = your-username
example.password = your-password

# Or use credential helper
[extensions]
mercurial_keyring =

[auth]
example.prefix = https://example.com
example.username = your-username
```

### SSH Key Authentication

```ini
[ui]
ssh = ssh -i ~/.ssh/hg_key -o StrictHostKeyChecking=no

[paths]
default = ssh://user@host//path/to/repo
```

### Signed Commits

```ini
[extensions]
hgext.gpg =

[gpg]
keyring = ~/.gnupg/pubring.gpg
secretkeyring = ~/.gnupg/secring.gpg
```

```bash
# Sign commit
hg commit -m "Signed commit" --sign
hg sign 1234  # Sign existing commit
```
