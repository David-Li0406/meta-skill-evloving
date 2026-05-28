# Mercurial Configuration and Extensions

This guide covers Mercurial configuration, extensions, and custom settings.

## Configuration File Locations

Mercurial loads configuration files in the following order:

1. **System-level**: `/etc/mercurial/hgrc` (Linux/Mac), `Mercurial.ini` (Windows)
2. **User-level**: `~/.hgrc` (Linux/Mac), `%USERPROFILE%\mercurial.ini` (Windows)
3. **Repository-level**: `.hg/hgrc`

## Basic Configuration

### User Information

```ini
[ui]
username = Your Name <your.email@example.com>
```

### Editor Configuration

```ini
[ui]
editor = vim
# or
editor = code --wait
# or
editor = notepad
```

### Diff Tools

```ini
[ui]
[merge-tools]
# Visual diff tool
diff3.executable = diff3
diff3.args = $parent1 $parent2 $ancestor $output

# KDiff3
kdiff3.executable = kdiff3
kdiff3.args = $base $local $other -o $output

# Meld
meld.executable = meld
meld.args = $local $base $other --output $output
```

### Pager

```ini
[ui]
# Use less
pager = less -FRSX

# Or disable pager
pager = false
```

## Extensions

### Enable Extensions

```ini
[extensions]
# Built-in extensions
color =
progress =
pager =
rebase =
histedit =

# External extensions (specify path)
# myextension = /path/to/extension.py
```

### Common Built-in Extensions

#### color (Syntax Highlighting)

```ini
[extensions]
color =

[color]
status.modified = green bold
status.added = green bold
status.removed = red bold
status.deleted = red bold
status.unknown = magenta bold
status.ignored = cyan bold

diff.changed = white
diff.added = green
diff.deleted = red
```

#### progress (ProgressBar)

```ini
[extensions]
progress =

[progress]
delay = 1.0
refresh = 0.1
width = 60
```

#### rebase

```ini
[extensions]
rebase =

[rebase]
# Tool used for automatic conflict resolution
conflictstyle = merge

# Source branch
sourcenode = tip
```

#### histedit (History Editing)

```ini
[extensions]
histedit =

[histedit]
# Number of commits to edit by default
defaultrev = -8
```

#### shelve

```ini
[extensions]
shelve =

[shelve]
# Shelf directory
shelfdir = .hg/shelves
```

### Third-party Extensions

#### hg-git (Interoperability with Git)

```ini
[extensions]
hggit = /path/to/hg-git/hgit

[git]
# Git repository configuration
infixes =

# Convert to Git on push
accepts-push = hg+git
```

#### hg-evolve (Advanced History Operations)

```ini
[extensions]
evolve = /path/to/hg-evolve/hgext3rd/evolve/

[experimental]
evolution = all
```

#### hg-gitlab (GitLab Integration)

```ini
[extensions]
gitlab = /path/to/hg-gitlab/hggitlab

[gitlab]
host = gitlab.example.com
token = your-api-token
```

## Aliases

### Create Aliases

```ini
[alias]
# Simplify common commands
st = status
ci = commit
co = update
br = branches

# Complex aliases
logg = log -G --template "{rev}:{node|short} {desc|firstline}\n"
outgoing = outgoing -T "{node|short}\n"
incoming = incoming -T "{node|short}\n"
```

### Alias Examples

```ini
[alias]
# Useful aliases
last = log -l 1
diffstat = diff --stat
grafted = log -r "sort(first(extra(graftr, revset), -date))"
parents = log -r "parents(.)"
head = log -r "tip"

# Combined operations
# Commit and push
ci-push = !hg commit -m "$1" && hg push
# Backup current state
backup = !hg clone . ../backup-`date +%Y%m%d`
```

## Hooks

### Client-side Hooks

```ini
[hooks]
# Check before commit
pre-commit = python:/path/to/check_style.py:run

# Check before update
pre-update = python:/path/to/check_branch.py:run

# Notify after update
post-update = python:/path/to/notify.py:run

# Test before push
pre-push = python:/path/to/run_tests.py:run
```

### Server-side Hooks

```ini
[hooks]
# Check before receiving changegroup
pretxnchangegroup.check_message = python:/path/to/check_commit.py:run

# Run tests
pretxnchangegroup.run_tests = python:/path/to/tests.py:run

# Notify after changegroup
changegroup.notify = python:/path/to/notify.py:run
```

### Hook Example Script

```python
# check_commit.py
import re

def check_commit_message(ui, repo, hooktype, node=None, **kwargs):
    """Check commit message format"""
    for rev in repo.changelog.revs(node):
        ctx = repo[rev]
        message = ctx.description()
        # Check format
        if not re.match(r'^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: ', message):
            ui.warn('Incorrect commit message format\n')
            ui.warn('Format: <type>(<scope>): <subject>\n')
            return True
    return False
```

## Network Configuration

### HTTP Configuration

```ini
[http]
# Timeout settings (seconds)
timeout = 60

# Compression
compression = zlib

# Cache
cache = true

# Proxy
proxy = http://proxy.example.com:8080
```

### SSH Configuration

```ini
[ui]
ssh = ssh -i ~/.ssh/hg_key -o StrictHostKeyChecking=no -o ConnectTimeout=10

[paths]
default = ssh://user@host/path/to/repo
```

### Auth Configuration

```ini
[auth]
# HTTPS Auth
example.prefix = https://example.com
example.username = username
example.password = password

# Or use credential helper
example.prefix = https://example.com
example.username = username
example.keyring = true
```

## Performance Optimization

### Memory and Cache

```ini
[merge]
# Memory usage during merge
merge-dirs = 1000000

[pager]
# Pager configuration
pager = less -FRSX
```

### Network Optimization

```ini
[server]
# Server configuration
uncompressed = false
preferuncompressed = true
stream = true

[diff]
# Git diff format
git = true

[pager]
# Disable pager for faster output
pager = false
```

### Index Optimization

```ini
[format]
# Use more efficient format
usestore = true
usefncache = true
dotencode = true
```

## Template Configuration

### Log Templates

```ini
[templates]
# Short log
shortlog = "{rev}:{node|short} {desc|firstline}\n"

# Detailed log
detailedlog = """
rev: {rev}
node: {node}
author: {author}
date: {date|isodate}
description:
{desc}
"""

# Graph log
graphlog = "{rev}:{node|short} {branches} {desc|firstline}\n"
```

### Usage

```bash
# Use defined template
hg log -T shortlog

# Or specify template directly
hg log -T "{node|short} {desc}\n"
```

## Editor Integration

### Vim Configuration

```vim
" In .vimrc
let g:mercurial_diffcommand = 'hg diff'
let g:mercurial_statuscommand = 'hg status'

" Install vim-mercurial plugin
Plug 'vim-scripts/mercurial.vim'
```

### VS Code Configuration

```json
{
  "extensions": ["mhutchie.git-graph"],
  "scm.inputFontSize": 13,
  "scm.providerCountBadge": "commits"
}
```

### Emacs Configuration

```elisp
;; In .emacs
(require 'mercurial)
(global-set-key (kbd "C-x v l") 'hg-log)
(global-set-key (kbd "C-x v d") 'hg-diff)
```

## Subrepository Configuration

```ini
[subpaths]
# Subrepo mapping
library = https://github.com/user/library

[extensions]
subrepo =
```

```bash
# Add subrepo
hg subrepo add library https://github.com/user/library

# Update subrepo
hg subrepo update

# Clone project with subrepos
hg clone --subrepos https://example.com/repo
```

## Large Files Support

### largefiles Extension

```ini
[extensions]
largefiles =

[largefiles]
# Size threshold (bytes)
minsize = 10

# Match patterns
patterns = *.psd *.iso *.zip

# Cache location
usercache = ~/.hg/largefiles
```

```bash
# Add large file
hg add --large large-file.iso

# Get large files
hg lfconvert

# Pull large files
hg pull --lfpull http://example.com/repo
```

## Security Configuration

### GPG Signing

```ini
[extensions]
gpg =

[gpg]
# GPG Keyring
keyring = ~/.gnupg/pubring.gpg
secretkeyring = ~/.gnupg/secring.gpg

# Default key
key = 0x12345678
```

```bash
# Sign commit
hg commit -m "Commit" --sign

# Sign existing commit
hg sign 1234

# Verify signatures
hg verify --signatures
```

### Encryption

```ini
[ui]
# Use HTTPS
tls1.2 = true
tls1.1 = true
tls1 = false

[web]
# Disable insecure protocols
push_ssl = true
```

## Theme Configuration

### Color Theme

```ini
[color]
status.modified = red bold
status.added = green bold
status.removed = red bold
status.deleted = red bold
status.unknown = magenta bold
status.ignored = black bold

diff.changed = white
diff.added = green
diff.deleted = red

# Log colors
log.changeset = cyan
log.tag = yellow bold
log.parent = magenta
```

### Custom Colors

```ini
[color]
# Hex color
custom = #00ff00

# Named color
custom = green bold

# ANSI color
custom = 32
```

## Experimental Features

```ini
[experimental]
# Enable evolution
evolution = all
evolution.createmarkers = true
evolution.allowunstable = true

# Enable new storage format
narrow = true
```

## Configuration Verification

### Check Config

```bash
# Show current config
hg showconfig

# Show specific section
hg showconfig ui

# Show all aliases
hg showconfig alias

# Show all extensions
hg showconfig extensions
```

### Syntax Verification

```bash
# Verify config file
hg debugconfig

# Check config errors
hg debugconfig --debug
```
