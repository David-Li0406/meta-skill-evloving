# Git Workflow - Sharp Edges

## Force Push Disaster

### **Id**
force-push-disaster
### **Summary**
Force pushing rewrites history others depend on
### **Severity**
critical
### **Situation**
  You rebase your branch and force push, but a teammate has already
  pulled your branch and built on top of it. Their commits are now
  orphaned, and they'll get confusing conflicts.
  
### **Why**
  Force push rewrites the remote history. Anyone who based work on
  the old history now has divergent timelines. This is the #1 cause
  of "git is hard" complaints. We've seen teams lose days of work.
  
### **Solution**
  # SAFE FORCE PUSHING
  
  # Never force push shared branches (main, develop, release/*)
  
  # For your own feature branches, use --force-with-lease
  git push --force-with-lease
  
  # This fails if remote has commits you don't have locally
  # Prevents accidentally overwriting a teammate's push
  
  # If you need to update a branch others use:
  1. Communicate first
  2. Have them push their work
  3. Use --force-with-lease
  4. Have them git fetch && git reset --hard origin/branch
  
  # Alternative: Don't rebase shared branches, only merge
  
### **Symptoms**
  - Teammate gets "divergent branches" message
  - Commits seem to disappear
  - Your branch and origin have diverged
### **Detection Pattern**
git\s+push\s+(-f|--force)\s+(?!.*--force-with-lease)

## Reset Hard Data Loss

### **Id**
reset-hard-data-loss
### **Summary**
git reset --hard discards uncommitted work forever
### **Severity**
critical
### **Situation**
  You want to discard some changes, run git reset --hard, and realize
  you had important uncommitted work. Unlike committed work, this
  cannot be recovered with reflog.
  
### **Why**
  reset --hard modifies three things: HEAD, staging, and working
  directory. Uncommitted work in the working directory is not
  tracked by git and cannot be recovered. Even reflog can't help.
  
### **Solution**
  # SAFER ALTERNATIVES
  
  # Check what you'll lose first
  git status
  git diff
  
  # Stash instead of reset for temporary discard
  git stash
  
  # Reset staged files only (keeps working directory)
  git reset HEAD
  
  # Reset a specific file
  git checkout -- filename
  
  # Discard all changes but make backup first
  git stash
  git reset --hard HEAD
  # If you need the changes back: git stash pop
  
  # If you did reset --hard by accident:
  # Uncommitted work is GONE
  # Committed work: check git reflog
  
### **Symptoms**
  - Hours of work just vanished
  - I had changes in that file...
  - No entry in git reflog for uncommitted work
### **Detection Pattern**
git\s+reset\s+--hard(?!\s+HEAD\s*$)

## Detached Head Commits

### **Id**
detached-head-commits
### **Summary**
Commits made in detached HEAD state are easily lost
### **Severity**
high
### **Situation**
  You checkout a specific commit or tag, make changes and commit,
  then checkout a branch. Your commits are now orphaned and will
  be garbage collected.
  
### **Why**
  Detached HEAD means you're not on any branch. Commits go to
  an anonymous branch. When you switch to a real branch, there's
  no reference to those commits. Git will garbage collect them.
  
### **Solution**
  # DETACHED HEAD
  
  # You'll see this warning:
  "You are in 'detached HEAD' state..."
  
  # If you want to keep commits made in detached HEAD:
  git checkout -b my-new-branch
  
  # If you already left and want to recover:
  git reflog
  # Find your commit
  git checkout -b recovered-work abc1234
  
  # Prevention: always work on a branch
  # If you need to explore an old commit:
  git checkout -b explore-old abc1234
  
  # Check if you're in detached HEAD:
  git branch
  # If you see: * (HEAD detached at abc1234)
  # Create a branch before committing!
  
### **Symptoms**
  - Warning about detached HEAD
  - Commits disappear after checkout
  - "HEAD detached at" in git branch output
### **Detection Pattern**
git\s+checkout\s+[a-f0-9]{7,40}(?!\s+-b)

## Merge Vs Rebase Confusion

### **Id**
merge-vs-rebase-confusion
### **Summary**
Using rebase on already-pushed commits causes divergence
### **Severity**
high
### **Situation**
  You push commits to a shared branch, then rebase locally, creating
  new commit hashes. Now local and remote have diverged with the
  "same" changes having different hashes.
  
### **Why**
  Rebase creates new commits with new hashes. If the original commits
  are already on the remote, you now have two sets of "same" commits.
  Force pushing causes the force-push-disaster problem.
  
### **Solution**
  # REBASE RULES
  
  # Golden rule: Don't rebase commits that exist on the remote
  
  # Safe: Rebase local work before pushing
  git fetch origin
  git rebase origin/main
  git push
  
  # Safe: Rebase before first push of feature branch
  git checkout feature
  git rebase main
  git push -u origin feature
  
  # UNSAFE: Rebase after pushing
  git push origin feature
  # ... later ...
  git rebase main  # Creates new commits!
  git push --force  # Rewrites remote history!
  
  # If branch is already pushed, use merge instead
  git checkout feature
  git merge main
  git push
  
### **Symptoms**
  - Your branch and origin have diverged
  - Duplicate commits in history
  - Teammates complain about conflicts
### **Detection Pattern**
git\s+rebase\s+\w+(?=.*git\s+push\s+--force)

## Cherry Pick Conflicts

### **Id**
cherry-pick-conflicts
### **Summary**
Cherry-picking creates duplicate commits and merge conflicts
### **Severity**
medium
### **Situation**
  You cherry-pick commits from one branch to another, then later merge
  the branches. Git sees the same changes with different hashes and
  may create conflicts or duplicate the changes.
  
### **Why**
  Cherry-pick copies the change with a new hash. When branches merge,
  git doesn't know these commits are related. You might get conflicts
  on "already applied" changes or actual duplicate code.
  
### **Solution**
  # CHERRY-PICK BEST PRACTICES
  
  # Cherry-pick is best for:
  - Hotfixes: pick fix to release branch
  - Backports: pick feature to older version
  - Recovery: grab specific commit from lost branch
  
  # Avoid when possible:
  - Features between active branches (merge instead)
  - Multiple commits (rebase instead)
  
  # If you must cherry-pick:
  git cherry-pick abc1234
  
  # Cherry-pick range (last commit excluded)
  git cherry-pick main~3..main
  
  # When merging later, expect to resolve as "already applied"
  # Mark as resolved even if no actual conflict
  
  # Alternative: Use merge with strategy
  git merge -X theirs feature  # Accept incoming for conflicts
  
### **Symptoms**
  - Merge conflicts on code that "should already be there"
  - Duplicate code after merge
  - Same logical change with two different commit hashes
### **Detection Pattern**
git\s+cherry-pick

## Gitignore After Tracking

### **Id**
gitignore-after-tracking
### **Summary**
Adding to .gitignore doesn't untrack already-tracked files
### **Severity**
medium
### **Situation**
  You add a file pattern to .gitignore, but the files are still being
  tracked and showing up in diffs. You committed them before adding
  to .gitignore.
  
### **Why**
  .gitignore only affects untracked files. Once a file is tracked
  (committed), git continues tracking it. You see config files with
  secrets, node_modules, or IDE files in your repo.
  
### **Solution**
  # REMOVE TRACKED FILES
  
  # Remove from git but keep on disk
  git rm --cached filename
  git rm --cached -r directory/
  
  # For multiple files matching pattern
  git rm --cached '*.log'
  
  # Then add to .gitignore and commit
  echo "*.log" >> .gitignore
  git add .gitignore
  git commit -m "chore: stop tracking log files"
  
  # For sensitive files already in history, see git-filter-repo
  # WARNING: This rewrites history!
  
  # Prevention: Add .gitignore FIRST before adding files
  
### **Symptoms**
  - .gitignore pattern doesn't seem to work
  - Secrets keep appearing in diffs
  - IDE files pollute the repo
### **Detection Pattern**


## Submodule Confusion

### **Id**
submodule-confusion
### **Summary**
Submodules create confusing state and require extra commands
### **Severity**
medium
### **Situation**
  You clone a repo with submodules and they're empty. Or you update
  a submodule and teammates don't see the changes. Or you're in a
  submodule and think you're in the main repo.
  
### **Why**
  Submodules are repos within repos. They have their own git state,
  own branches, own commits. Main repo only tracks a commit hash,
  not the submodule's branch. Many commands don't recurse by default.
  
### **Solution**
  # SUBMODULE BASICS
  
  # Clone with submodules
  git clone --recurse-submodules repo-url
  
  # Initialize after regular clone
  git submodule update --init --recursive
  
  # Update submodules to latest
  git submodule update --remote
  
  # Pull with submodule update
  git pull --recurse-submodules
  
  # After updating submodule, commit the change
  cd submodule/
  git checkout new-version
  cd ..
  git add submodule/
  git commit -m "chore: update submodule to v2.0"
  
  # Consider alternatives:
  - Package managers (npm, pip)
  - Monorepo tools (nx, turborepo)
  - git subtree (simpler than submodules)
  
### **Symptoms**
  - Empty directories after clone
  - Submodule "stuck" on old commit
  - Confusing detached HEAD in submodule
### **Detection Pattern**
git\s+submodule

## Merge Conflict Panic

### **Id**
merge-conflict-panic
### **Summary**
Panicking during merge conflicts makes things worse
### **Severity**
medium
### **Situation**
  You hit a merge conflict, panic, try various commands, and end up
  in a worse state. Maybe you reset in the middle of a merge, or
  added conflict markers to the commit.
  
### **Why**
  Merge conflicts are normal. Panicking leads to git reset, abandoned
  merges, or committed conflict markers. Take a breath - git tells
  you exactly what to do.
  
### **Solution**
  # MERGE CONFLICT RESOLUTION
  
  # When you see conflicts:
  git status  # Shows which files have conflicts
  
  # In each file, you'll see:
  <<<<<<< HEAD
  your changes
  =======
  their changes
  >>>>>>> branch-name
  
  # Edit the file to resolve:
  1. Remove the markers (<<<<, ====, >>>>)
  2. Keep the code you want
  3. Save the file
  
  # Mark as resolved
  git add filename
  
  # Complete the merge
  git commit  # Message is pre-filled
  
  # If you want to abort and start over:
  git merge --abort
  
  # If things are really bad:
  git reset --hard HEAD  # Only if you haven't committed!
  
  # Tools help:
  git mergetool  # Opens configured merge tool
  
### **Symptoms**
  - Conflict markers in committed code
  - Aborting merge due to unresolved conflicts
  - Files stuck in unmerged state
### **Detection Pattern**
<<<<<<< HEAD|=======|>>>>>>> \w+

## Amend Pushed Commit

### **Id**
amend-pushed-commit
### **Summary**
Amending a pushed commit requires force push
### **Severity**
medium
### **Situation**
  You commit with a typo in the message or forgot a file, amend the
  commit, then can't push because remote has the original commit.
  
### **Why**
  Amend creates a new commit with a new hash. If you've pushed the
  original, git sees your amended commit as different. You need
  force push, which has the force-push-disaster risks.
  
### **Solution**
  # SAFE AMENDING
  
  # Amend is safe for: commits you haven't pushed yet
  git commit --amend  # Edit message
  git commit --amend --no-edit  # Add staged files, keep message
  
  # If already pushed to your own branch:
  git push --force-with-lease
  
  # If already pushed to shared branch:
  # Don't amend! Make a new commit instead:
  git commit -m "fix: correct typo from previous commit"
  
  # Alternative: Use fixup for later squashing
  git commit --fixup abc1234
  # Later, before PR merge:
  git rebase -i --autosquash main
  
### **Symptoms**
  - Updates were rejected because the tip of your branch is behind
  - Need to force push after amend
  - Teammate has old version of commit
### **Detection Pattern**
git\s+commit\s+--amend.*\n.*git\s+push(?!\s+--force)