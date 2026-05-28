# Mercurial Troubleshooting

This guide covers common issues and solutions for Mercurial.

## Common Errors and Solutions

### Push Rejected

#### Error: "abort: push creates new remote head"

**Cause**: Created a new remote branch head that hasn't been merged.

**Solution**:
```bash
# Solution 1: Pull and merge first
hg pull
hg merge
hg commit -m "Merge remote updates"
hg push

# Solution 2: Force push (not recommended)
hg push -f

# Solution 3: Rebase to latest
hg pull
hg rebase -d default
hg push
```

#### Error: "abort: repository is unrelated"

**Cause**: Pushing to an unrelated repository.

**Solution**:
```bash
# Solution 1: Clone the correct repository
hg clone https://correct-repo/repo

# Solution 2: Force push (use with caution)
hg push --force
```

### Merge Conflicts

#### Error: "unresolved merge conflicts"

**Solution**:
```bash
# 1. View conflicted files
hg resolve --list

# 2. Manually resolve conflicts
# Edit files marked with <<<<<<

# 3. Mark as resolved
hg resolve --mark filename.txt

# 4. Continue merge
hg commit -m "Resolve conflicts"

# 5. If aborting
hg merge --abort
```

#### Using Merge Tools to Resolve Conflicts

```bash
# Use internal merge tool
hg merge --tool=internal:merge3

# Use external tools
hg merge --tool=vimdiff
hg merge --tool=kdiff3
hg merge --tool=meld
```

### Push Errors

#### Error: "abort: authorization failed"

**Solution**:
```bash
# Solution 1: Check auth configuration
# In ~/.hgrc:
[auth]
example.prefix = https://example.com
example.username = your-username
example.password = your-password

# Solution 2: Use HTTPS
hg push https://username:password@example.com/repo

# Solution 3: Use SSH
# Change protocol to SSH
hg push ssh://user@host/path/to/repo
```

#### Error: "abort: ssl required"

**Solution**:
```ini
# In ~/.hgrc:
[web]
push_ssl = false

[ui]
tls1.2 = true
tls1.1 = true
```

### Pull Errors

#### Error: "abort: unknown revision"

**Solution**:
```bash
# Check if remote exists
hg incoming

# Check available revisions
hg log -r "remote()"

# Pull without specifying revision (pull all available)
hg pull

# Update to latest
hg update -r tip
```

#### Error: "abort: HTTP Error 403"

**Solution**:
```bash
# Check permissions
# Check if username and password are correct

# Reconfigure auth
hg config auth.example.username
hg config auth.example.password
```

## Repository Corruption Recovery

### Verify Repository

```bash
# Basic verification
hg verify

# Verbose verification
hg verify --verbose

# Verify specific file
hg verify path/to/file
```

### Repository Corruption

#### Error: "abort: data/...i: no node!"

**Solution**:
```bash
# 1. Try to recover
hg recover

# 2. If failed, recover from backup
hg clone /backup/repo

# 3. Or recover from bundle
hg unbundle backup.hg
```

### Lost Commits

#### Recover Stripped Commits

```bash
# 1. Find backups
ls .hg/strip-backup/

# 2. Recover specific backup
hg unbundle .hg/strip-backup/1234-backup.hg

# 3. Or use mq
hg qimport -r 1234
hg qpush
```

#### Recover Lost Changesets

```bash
# 1. Find all heads
hg heads

# 2. Find all commits by specific author
hg log -u "username"

# 3. Use debugsetparents
hg debugsetparents --force 1234

# 4. Use debugrebuildfncache
hg debugrebuildfncache
```

## Performance Issues

### Repository Becomes Slow

**Solution**:
```bash
# 1. Rebuild file name cache
hg debugrebuildfncache

# 2. Verify repository integrity
hg verify

# 3. Use shallow clone
hg clone -U https://large-repo/repo
```

### Network Operations Slow

**Solution**:
```ini
# In ~/.hgrc:
[http]
compression = zlib
timeout = 120

[pager]
pager = false  # Disable paging

[progress]
delay = 0.5
```

### Large Repository Operations

**Solution**:
```bash
# Use narrowclone
hg clone --narrow https://repo path/to/subdir

# Use shallow clone
hg clone -U -r tip https://repo

# Disable unnecessary extensions
# Comment out unused extensions in ~/.hgrc
```

## Filesystem Issues

### File Permission Errors

```bash
# Check file permissions
ls -la .hg/

# Fix permissions
chmod -R u+rw .hg/
chown -R user:group .hg/
```

### Insufficient Disk Space

```bash
# Cleanup bundles
rm .hg/*.bundle

# Cleanup strip backups
rm -rf .hg/strip-backup/

# Cleanup cache
rm -rf .hg/cache/
```

### Filename Encoding Issues

```ini
# In ~/.hgrc:
[ui]
# Set correct encoding
fallbackencoding = gbk
# Or
fallbackencoding = utf-8
```

## Extension Issues

### Extension Load Failed

#### Error: "failed to import extension"

**Solution**:
```bash
# 1. Check extension path
hg showconfig extensions

# 2. Confirm extension file exists
ls -la /path/to/extension.py

# 3. Test extension
python -c "import extension"

# 4. Fix Python path
export PYTHONPATH=/path/to/extensions
```

### MQ Issues

#### Patch Cannot Apply

```bash
# 1. View conflicts
hg qdiff

# 2. Manually resolve
hg resolve --mark

# 3. Force apply
hg qpush -f

# 4. Or re-import
hg qimport -r 1234
```

#### Patch Queue Messed Up

```bash
# Reset queue
hg qpop -a
hg qdelete -a

# Or create new queue
hg qqueue --create new-queue
hg qqueue new-queue
```

## Network Issues

### Connection Timeout

```ini
# In ~/.hgrc:
[http]
timeout = 300

[ui]
ssh = ssh -o ConnectTimeout=30 -o ServerAliveInterval=60
```

### Proxy Issues

```ini
# In ~/.hgrc:
[http]
proxy = http://proxy.example.com:8080
proxyauth = username:password

[ui]
# Or via environment variable
# export http_proxy=http://proxy.example.com:8080
```

### DNS Issues

```bash
# Use IP address instead of domain
hg clone http://192.168.1.100/repo

# Or configure hosts file
# /etc/hosts
192.168.1.100 repo.example.com
```

## User Interface Issues

### Encoding Display Errors

```ini
# In ~/.hgrc:
[ui]
# Correct encoding settings
# Linux/Mac
username = username <email@example.com>
fallbackencoding = utf-8

# Windows
username = username <email@example.com>
fallbackencoding = gbk
```

### Pager Issues

```ini
# In ~/.hgrc:
[pager]
# Disable paging
pager = false

# Or use specific pager
pager = less -FRSX
```

## Debugging Tips

### Enable Debug Output

```bash
# Enable debug mode
hg --debug status

# Enable verbose output
hg --verbose status

# Enable traceback
hg --debug --traceback status
```

### View Internal Information

```bash
# View .hg directory
ls -la .hg/

# View store
ls -la .hg/store/

# View cache
ls -la .hg/cache/

# View branch information
hg debugbranchmap

# View index
hg debugindex .hg/store/00changelog.i
```

### Use debug Commands

```bash
# Debug pull/push
hg debugpushkey
hg debugwireargs

# Debug merge
hg debugmergebase

# Debug state
hg debugstate

# Debug DAG
hg debugdag
```

## Log and Analysis

### Log Operations

```ini
# In ~/.hgrc:
[devel]
# Enable debug
devel-warn = true

[commands]
# Log all commands
logtemplate = "{date|isodate} {rev}:{node|short} {author}\n{desc}\n"
```

### Performance Analysis

```bash
# Use --time flag
hg --time pull

# Use Python profiler
hg --profile log

# View statistics
hg --debug --config "extensions.blackbox=!"
```

## Backup and Recovery

### Create Full Backup

```bash
# Clone backup
hg clone . /backup/repo-$(date +%Y%m%d)

# Create bundle
hg bundle --all backup.hg

# Create incremental bundle
hg bundle backup-$(date +%Y%m%d).hg -r "tip~100::tip"
```

### Restore from Backup

```bash
# Restore from clone
hg clone /backup/repo-20240101

# Restore from bundle
hg init restored
cd restored
hg unbundle /backup/backup.hg
```

### Periodic Backup Script

```bash
#!/bin/bash
# backup.sh
REPO_DIR="/path/to/repo"
BACKUP_DIR="/backup/mercurial"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cd $REPO_DIR

# Create bundle
hg bundle $BACKUP_DIR/repo-$DATE.hg --all

# Keep backups for last 30 days
find $BACKUP_DIR -name "repo-*.hg" -mtime +30 -delete
```

## Get Help

### Built-in Help

```bash
# Help system
hg help

# Specific command help (use --verbose for detailed information)
hg help --verbose commit

# Config help
hg help config

# Extension help
hg help extensions
```

**Tip**: For any unclear command, always use `hg help --verbose <command>` to view the official documentation with complete options and examples.

### Online Resources

- Official Documentation: https://www.mercurial-scm.org/guide
- Issue Tracker: https://bz.mercurial-scm.org/
- Mailing Lists: https://www.mercurial-scm.org/wiki/MailingLists
- Stack Overflow: Tag "mercurial"

### Community Support

```bash
# View version
hg version

# View all config
hg showconfig

# View all commands
hg debugcomplete
```

## Common Troubleshooting Commands

| Command | Description |
|---------|-------------|
| `hg verify` | Verify repository integrity |
| `hg recover` | Recover from interrupted operation |
| `hg debugrebuildfncache` | Rebuild file name cache |
| `hg debugsetparents` | Set parent nodes |
| `hg debugindex` | View index |
| `hg debugstate` | View state |
| `hg --debug` | Enable debug output |
| `hg --traceback` | Show Python traceback |
| `hg help --verbose <command>` | View command help |