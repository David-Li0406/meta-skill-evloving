# Git Workflow

## Patterns


---
  #### **Name**
Conventional Commits
  #### **Description**
Structured commit messages for automation
  #### **When**
Auto-generating changelogs, semantic versioning, commit search
  #### **Example**
    # CONVENTIONAL COMMITS:
    
    """
    Format: <type>(<scope>): <description>
    
    Types:
    - feat: New feature
    - fix: Bug fix
    - docs: Documentation only
    - style: Formatting, no code change
    - refactor: Code change, no feature/fix
    - perf: Performance improvement
    - test: Adding tests
    - chore: Maintenance, build, etc.
    
    Breaking changes: Add ! after type or BREAKING CHANGE in footer
    """
    
    # Examples:
    feat(auth): add OAuth2 login with Google
    
    fix(api): handle null response from payment gateway
    
    refactor(users): extract validation into separate module
    
    feat!: change API response format
    BREAKING CHANGE: responses now wrapped in { data: ... }
    
    # Multi-line with body and footer:
    fix(cart): prevent duplicate items on rapid clicks
    
    The add-to-cart button was not disabled during the API call,
    allowing users to add the same item multiple times.
    
    Closes #123
    

---
  #### **Name**
Interactive Rebase for Clean History
  #### **Description**
Squash, reorder, and edit commits before sharing
  #### **When**
Before opening a PR, cleaning up local work
  #### **Example**
    # INTERACTIVE REBASE:
    
    """
    Clean up your commits before pushing. Your PR should tell a story.
    """
    
    # Start interactive rebase for last 5 commits
    git rebase -i HEAD~5
    
    # Or rebase onto main
    git rebase -i main
    
    # In editor, you'll see:
    pick abc1234 Add user model
    pick def5678 Fix typo
    pick ghi9012 Add user validation
    pick jkl3456 Another typo fix
    pick mno7890 Add user tests
    
    # Change to:
    pick abc1234 Add user model
    fixup def5678 Fix typo         # Merge into previous, discard message
    pick ghi9012 Add user validation
    fixup jkl3456 Another typo fix
    pick mno7890 Add user tests
    
    # Commands:
    # pick   = use commit as-is
    # reword = use commit but edit message
    # edit   = stop for amending
    # squash = merge with previous, combine messages
    # fixup  = merge with previous, discard message
    # drop   = remove commit
    
    # Save and close. If conflicts, resolve and:
    git rebase --continue
    
    # If things go wrong:
    git rebase --abort
    

---
  #### **Name**
Atomic Commits
  #### **Description**
Each commit does one thing and can be reverted independently
  #### **When**
Every commit - this is the foundation of good git hygiene
  #### **Example**
    # ATOMIC COMMITS:
    
    """
    Each commit should:
    1. Do one logical thing
    2. Leave the codebase in a working state
    3. Be revertable without breaking other features
    """
    
    # BAD: One giant commit
    git commit -m "Add user feature"
    # 47 files changed, 2000 insertions
    
    # GOOD: Series of atomic commits
    git commit -m "feat(users): add User model and migration"
    git commit -m "feat(users): add user validation rules"
    git commit -m "feat(users): add user API endpoints"
    git commit -m "test(users): add user model unit tests"
    git commit -m "test(users): add user API integration tests"
    
    # Staging parts of files
    git add -p  # Interactive staging, hunk by hunk
    
    # Unstage a file but keep changes
    git reset HEAD filename
    

---
  #### **Name**
Branch Naming Convention
  #### **Description**
Consistent branch names for team workflows
  #### **When**
Any team project, CI/CD integration
  #### **Example**
    # BRANCH NAMING:
    
    """
    Convention: <type>/<ticket>-<short-description>
    """
    
    # Feature branches
    feature/AUTH-123-oauth-login
    feat/AUTH-123-oauth-login
    
    # Bug fixes
    fix/BUG-456-cart-duplicate
    bugfix/BUG-456-cart-duplicate
    
    # Hotfixes (urgent production fixes)
    hotfix/PROD-789-payment-timeout
    
    # Chores/refactors
    chore/upgrade-dependencies
    refactor/extract-validation
    
    # Experiments
    experiment/new-payment-flow
    
    # Release branches (if using GitFlow)
    release/v1.2.0
    
    # Create and switch to new branch
    git checkout -b feature/AUTH-123-oauth-login
    
    # Or with git switch (newer)
    git switch -c feature/AUTH-123-oauth-login
    

---
  #### **Name**
Stash for Context Switching
  #### **Description**
Save work-in-progress without committing
  #### **When**
Need to switch branches but have uncommitted changes
  #### **Example**
    # GIT STASH:
    
    """
    Stash saves your working directory state for later.
    """
    
    # Basic stash
    git stash
    
    # Stash with a message (recommended)
    git stash push -m "WIP: auth validation"
    
    # Stash including untracked files
    git stash -u
    
    # List stashes
    git stash list
    # stash@{0}: On feature: WIP: auth validation
    # stash@{1}: On main: debugging
    
    # Apply most recent stash (keeps stash)
    git stash apply
    
    # Apply and remove from stash
    git stash pop
    
    # Apply specific stash
    git stash apply stash@{1}
    
    # View stash contents
    git stash show -p stash@{0}
    
    # Drop a stash
    git stash drop stash@{0}
    
    # Clear all stashes
    git stash clear
    

---
  #### **Name**
Recovery with Reflog
  #### **Description**
Recover from almost any git disaster
  #### **When**
Accidentally deleted branch, bad reset, lost commits
  #### **Example**
    # GIT REFLOG - YOUR SAFETY NET:
    
    """
    Git reflog records every change to HEAD. Almost nothing is truly lost.
    """
    
    # View reflog
    git reflog
    # abc1234 HEAD@{0}: reset: moving to HEAD~3
    # def5678 HEAD@{1}: commit: Add feature
    # ghi9012 HEAD@{2}: commit: Another change
    
    # Recover from bad reset
    git reset --hard def5678  # Go back to that commit
    
    # Recover deleted branch
    git checkout -b recovered-branch def5678
    
    # Find a specific commit
    git reflog | grep "commit message"
    
    # Reflog expires after 90 days by default
    # For critical recovery, act quickly
    

## Anti-Patterns


---
  #### **Name**
Working Directly on Main
  #### **Description**
Making commits directly to the main branch
  #### **Why**
    No review, no CI check, no rollback point. One bad commit breaks
    production for everyone. You can't easily revert without affecting
    other changes.
    
  #### **Instead**
    Always branch:
    git checkout -b feature/my-change
    # make changes
    git push -u origin feature/my-change
    # open PR for review
    

---
  #### **Name**
Force Push to Shared Branches
  #### **Description**
Using git push --force on branches others are using
  #### **Why**
    Rewrites history that others have based their work on. They'll get
    conflicts, potentially lose work, and definitely lose trust.
    
  #### **Instead**
    # For your own branches, use --force-with-lease
    git push --force-with-lease
    
    # This fails if remote has commits you don't have
    # Prevents accidentally overwriting others' work
    
    # Never force push to main/develop
    

---
  #### **Name**
Giant Commits
  #### **Description**
One commit with thousands of lines changing many things
  #### **Why**
    Impossible to review properly. Can't revert one change without
    reverting everything. Blame and bisect become useless. Nobody
    will actually review 50 files.
    
  #### **Instead**
    Commit frequently as you work:
    - Model change? Commit.
    - Tests for that model? Commit.
    - API endpoint? Commit.
    
    git add -p for partial file staging
    

---
  #### **Name**
Cryptic Commit Messages
  #### **Description**
Messages like "fix", "wip", "update", "asdf"
  #### **Why**
    Future you will have no idea what this changed or why. Can't
    search history effectively. Blame is useless. Changelogs are
    meaningless.
    
  #### **Instead**
    Answer: What does this commit do and why?
    
    BAD:  git commit -m "fix"
    GOOD: git commit -m "fix(auth): prevent session timeout during checkout"
    
    BAD:  git commit -m "update"
    GOOD: git commit -m "refactor(users): extract validation into middleware"
    

---
  #### **Name**
Long-Lived Feature Branches
  #### **Description**
Branches that exist for weeks or months
  #### **Why**
    Diverges from main, merge conflicts pile up, integration issues
    compound. The longer the branch, the harder the merge, the more
    bugs in the integration.
    
  #### **Instead**
    - Break features into smaller incremental changes
    - Use feature flags to merge incomplete features
    - Merge to main daily if possible
    - If branch > 3 days old, split it up
    