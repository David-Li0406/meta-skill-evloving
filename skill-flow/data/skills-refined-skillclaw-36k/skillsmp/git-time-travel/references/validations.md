# Git Time Travel - Validations

## Force Push to Main

### **Id**
force-push-main
### **Severity**
high
### **Type**
conceptual
### **Check**
Should not force push to main/master
### **Indicators**
  - git push --force origin main
  - git push -f main
  - Force pushing to master
### **Message**
Attempting force push to main branch.
### **Fix Action**
Use regular push or coordinate if absolutely necessary

## Rebase Without Backup

### **Id**
no-backup-rebase
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should backup before risky operations
### **Indicators**
  - Rebase without backup branch
  - No safety tag
  - Interactive rebase on shared branch
### **Message**
Risky operation without backup.
### **Fix Action**
Create backup branch before rebasing

## Force Push Without Lease

### **Id**
force-without-lease
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should use --force-with-lease
### **Indicators**
  - git push --force
  - git push -f
  - Not using --force-with-lease
### **Message**
Force push without safety check.
### **Fix Action**
Use --force-with-lease instead of --force

## Commits Too Large for Bisect

### **Id**
giant-commits
### **Severity**
low
### **Type**
conceptual
### **Check**
Commits should be atomic for bisectability
### **Indicators**
  - Many files in one commit
  - Multiple features per commit
  - Days of work in one commit
### **Message**
Commits may be too large for effective bisect.
### **Fix Action**
Split into smaller, atomic commits

## Changing Code Without Checking History

### **Id**
no-commit-context
### **Severity**
low
### **Type**
conceptual
### **Check**
Should check git blame before significant changes
### **Indicators**
  - No git blame check
  - Removing code without understanding
  - No commit message reference
### **Message**
Changing code without checking history for context.
### **Fix Action**
Run git blame, read commit message before changing

## Recovery Without Checking Reflog

### **Id**
reflog-not-checked
### **Severity**
low
### **Type**
conceptual
### **Check**
Should check reflog when looking for lost work
### **Indicators**
  - Lost commit
  - No reflog check
  - Assuming work is gone
### **Message**
Check reflog before assuming work is lost.
### **Fix Action**
Run git reflog to find lost commits