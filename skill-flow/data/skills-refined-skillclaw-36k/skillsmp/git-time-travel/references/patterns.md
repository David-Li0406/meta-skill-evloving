# Git Time Travel

## Patterns


---
  #### **Name**
Git Bisect Mastery
  #### **Description**
Finding exactly when bugs were introduced
  #### **When To Use**
When hunting for a regression
  #### **Implementation**
    ## Finding Bugs with Bisect
    
    ### 1. Basic Bisect
    
    ```bash
    # Start bisecting
    git bisect start
    
    # Mark current (broken) as bad
    git bisect bad
    
    # Mark known good commit
    git bisect good abc1234  # or: git bisect good v1.0.0
    
    # Git checks out middle commit
    # Test it, then:
    git bisect good  # or: git bisect bad
    
    # Repeat until found
    # When done:
    git bisect reset
    ```
    
    ### 2. Automated Bisect
    
    ```bash
    # Write a test script that exits 0 for good, 1 for bad
    git bisect start HEAD v1.0.0
    git bisect run npm test
    
    # Or with a custom script:
    git bisect run ./test-for-bug.sh
    ```
    
    ### 3. Bisect Tips
    
    | Situation | Solution |
    |-----------|----------|
    | Can't test this commit | `git bisect skip` |
    | Made a mistake | `git bisect log` → edit → `git bisect replay` |
    | Need to see progress | `git bisect visualize` |
    | Wrong starting points | `git bisect reset` and start over |
    
    ### 4. The Binary Search Math
    
    ```
    Number of commits: N
    Maximum steps: log2(N)
    
    1000 commits → ~10 tests
    10000 commits → ~14 tests
    100000 commits → ~17 tests
    
    MUCH faster than linear search!
    ```
    

---
  #### **Name**
Commit Archaeology
  #### **Description**
Understanding why code exists
  #### **When To Use**
When you need context on code decisions
  #### **Implementation**
    ## Reading History
    
    ### 1. Essential Commands
    
    ```bash
    # Who changed this line and when?
    git blame -w -C -C -C path/to/file
    
    # When was this function changed?
    git log -p -S "functionName" -- path/
    
    # What files changed together with this one?
    git log --stat -- path/to/file
    
    # Show commit with context
    git show abc1234 --stat
    ```
    
    ### 2. Blame Options
    
    | Option | Purpose |
    |--------|---------|
    | `-w` | Ignore whitespace |
    | `-C` | Detect moved lines |
    | `-C -C` | Detect copies too |
    | `-C -C -C` | Detect across files |
    | `-L 10,20` | Specific lines only |
    
    ### 3. Log Archaeology
    
    ```bash
    # Search commit messages
    git log --grep="bug fix"
    
    # Search code changes
    git log -S "functionName"  # When added/removed
    git log -G "pattern"        # When changed
    
    # By author
    git log --author="name"
    
    # By date range
    git log --since="2024-01-01" --until="2024-02-01"
    ```
    
    ### 4. Finding Context
    
    | Question | Command |
    |----------|---------|
    | Why does this exist? | `git blame` → `git show <commit>` |
    | What PR added this? | Check commit message for PR # |
    | What else changed? | `git show <commit> --stat` |
    | Was this reverted? | `git log --grep="Revert.*<message>"` |
    

---
  #### **Name**
Recovery Operations
  #### **Description**
Recovering lost work and commits
  #### **When To Use**
When you've lost code or made mistakes
  #### **Implementation**
    ## Recovering Lost Work
    
    ### 1. The Reflog (Your Safety Net)
    
    ```bash
    # See all recent HEAD positions
    git reflog
    
    # Output like:
    # abc1234 HEAD@{0}: commit: Current work
    # def5678 HEAD@{1}: reset: moving to HEAD~5
    # ghi9012 HEAD@{2}: commit: Lost commit!
    
    # Recover by:
    git checkout ghi9012       # Just look
    git cherry-pick ghi9012    # Copy commit
    git reset --hard ghi9012   # Restore completely
    ```
    
    ### 2. Recovery Scenarios
    
    | Lost | Recovery |
    |------|----------|
    | Uncommitted changes | Check stash, IDE history |
    | Committed then reset | `git reflog` → cherry-pick |
    | Deleted branch | `git reflog` → create branch |
    | Force pushed over | `git reflog` on local |
    | Amended away | `git reflog` → ORIG_HEAD |
    
    ### 3. Stash Recovery
    
    ```bash
    # List all stashes
    git stash list
    
    # Show stash contents
    git stash show -p stash@{0}
    
    # Apply without removing
    git stash apply stash@{0}
    
    # Recover dropped stash (if recent)
    git fsck --no-reflog | grep commit
    # Then cherry-pick the orphan commit
    ```
    
    ### 4. Nuclear Recovery
    
    ```bash
    # If truly desperate, look for dangling commits
    git fsck --lost-found
    
    # Check .git/lost-found/other/
    # Contains blobs of lost content
    ```
    

---
  #### **Name**
Safe History Rewriting
  #### **Description**
Modifying history without disaster
  #### **When To Use**
When you must change committed history
  #### **Implementation**
    ## Rewriting History Safely
    
    ### 1. The Golden Rules
    
    ```
    RULE 1: Never rewrite shared history
            (unless coordinated)
    
    RULE 2: Always have a backup branch
    
    RULE 3: Communicate before force push
    
    RULE 4: Use --force-with-lease not --force
    ```
    
    ### 2. Safe Rebase
    
    ```bash
    # Create backup first!
    git branch backup-before-rebase
    
    # Interactive rebase
    git rebase -i HEAD~5
    
    # In editor:
    # pick abc1234 Good commit
    # squash def5678 Squash into above
    # reword ghi9012 Change message
    # drop jkl3456 Remove this commit
    
    # If things go wrong:
    git rebase --abort
    # Or restore from backup
    ```
    
    ### 3. Amending Safely
    
    ```bash
    # Only amend unpushed commits!
    git commit --amend
    
    # Add forgotten file
    git add forgotten.js
    git commit --amend --no-edit
    
    # Change last commit message
    git commit --amend -m "Better message"
    ```
    
    ### 4. Force Push Protocol
    
    ```bash
    # NEVER: git push --force
    # ALWAYS: git push --force-with-lease
    
    # This fails if remote changed
    # (Someone else pushed)
    
    # Before force pushing to shared branch:
    # 1. Announce in Slack/team chat
    # 2. Wait for acknowledgment
    # 3. Use --force-with-lease
    # 4. Confirm with team
    ```
    

## Anti-Patterns


---
  #### **Name**
The Force Push Surprise
  #### **Description**
Force pushing without warning
  #### **Why Bad**
    Destroys teammates' work.
    Creates confusion.
    Can lose production code.
    
  #### **What To Do Instead**
    Always announce.
    Use --force-with-lease.
    Coordinate with team.
    

---
  #### **Name**
The Giant Commit
  #### **Description**
Huge commits that can't be bisected
  #### **Why Bad**
    Can't find bugs with bisect.
    Blame is useless.
    Review is impossible.
    
  #### **What To Do Instead**
    Atomic commits.
    One logical change per commit.
    Split before pushing.
    

---
  #### **Name**
The Lost in History
  #### **Description**
Not checking git for context
  #### **Why Bad**
    Reinvent solutions.
    Miss important context.
    Repeat mistakes.
    
  #### **What To Do Instead**
    git blame before changing.
    Read the commit message.
    Check linked PRs/issues.
    