# Git Workflow - Validations

## Force push without --force-with-lease

### **Id**
force-push-without-lease
### **Severity**
error
### **Type**
regex
### **Pattern**
  - git\s+push\s+(-f|--force)(?!\s*--force-with-lease)
### **Message**
Force push can overwrite others' work - use --force-with-lease instead
### **Fix Action**
Replace -f/--force with --force-with-lease
### **Applies To**
  - *.sh
  - *.bash
  - *.md
  - *.yml
  - *.yaml

## Hard reset to remote branch

### **Id**
reset-hard-to-remote
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - git\s+reset\s+--hard\s+origin/
### **Message**
Hard reset discards local commits - make sure this is intentional
### **Fix Action**
Consider git rebase or git merge instead
### **Applies To**
  - *.sh
  - *.bash

## Direct push to main/master

### **Id**
direct-push-to-main
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - git\s+push\s+(origin\s+)?(main|master)(?!\s*:)
### **Message**
Pushing directly to main bypasses code review
### **Fix Action**
Create a feature branch and open a PR
### **Applies To**
  - *.sh
  - *.bash

## Commit message too short

### **Id**
short-commit-message
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - git\s+commit\s+-m\s+["'][^"']{1,10}["']
### **Message**
Commit message is too short - explain what and why
### **Fix Action**
Write a descriptive message: what changed and why
### **Applies To**
  - *.sh
  - *.bash

## WIP commit message

### **Id**
wip-commit-message
### **Severity**
info
### **Type**
regex
### **Pattern**
  - git\s+commit\s+-m\s+["']([Ww][Ii][Pp]|wip|WIP)["']
### **Message**
WIP commits should be squashed before merge
### **Fix Action**
Use git rebase -i to squash WIP commits
### **Applies To**
  - *.sh
  - *.bash

## Generic commit message

### **Id**
generic-commit-message
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - git\s+commit\s+-m\s+["'](fix|update|change|modify|misc|stuff)["']
### **Message**
Commit message is too generic - describe what was changed
### **Fix Action**
Describe the specific change: 'fix(auth): prevent session timeout'
### **Applies To**
  - *.sh
  - *.bash

## Sensitive files should be gitignored

### **Id**
sensitive-files-not-ignored
### **Severity**
error
### **Type**
file
### **Pattern**
  - .env
  - .env.local
  - *.pem
  - *.key
  - credentials.json
### **Message**
Sensitive files should be in .gitignore
### **Fix Action**
Add to .gitignore and remove from tracking: git rm --cached filename
### **Applies To**
  - .gitignore

## node_modules should be gitignored

### **Id**
node-modules-committed
### **Severity**
error
### **Type**
regex
### **Pattern**
  - node_modules/
### **Message**
node_modules should not be committed
### **Fix Action**
Add 'node_modules/' to .gitignore and run: git rm -r --cached node_modules
### **Applies To**
  - .gitignore

## Branch doesn't follow naming convention

### **Id**
branch-naming-convention
### **Severity**
info
### **Type**
regex
### **Pattern**
  - checkout\s+-b\s+[a-z]+(?!/)
### **Message**
Branch names should follow pattern: type/description
### **Fix Action**
Use: feature/AUTH-123-description, fix/BUG-456-issue, etc.
### **Applies To**
  - *.sh
  - *.bash

## Merge conflict markers in code

### **Id**
conflict-markers-in-code
### **Severity**
error
### **Type**
regex
### **Pattern**
  - <<<<<<< HEAD
  - =======
  - >>>>>>> \w+
### **Message**
Unresolved merge conflict markers in file
### **Fix Action**
Resolve the conflict by editing the file and removing markers
### **Applies To**
  - *