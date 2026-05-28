# Git Workflow Excellence for Nix Projects

## Commit Philosophy

**Atomic commits**: Each commit should be a complete, logical unit.
**Descriptive messages**: Tell the story of *why*, not just *what*.
**Builds clean**: Every commit should build successfully.

## Conventional Commits

Use structured commit messages for automation and clarity:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests
- `build`: Build system changes
- `ci`: CI configuration
- `chore`: Maintenance tasks

### Examples

```
feat(flake): add cross-compilation for ARM64

- Implement crossSystem configuration
- Add platform-specific build flags  
- Update CI to test ARM builds
- Add documentation for cross-compilation

Closes #123
```

```
fix(module): resolve circular dependency in network config

The wireguard module was importing firewall rules that
imported network configuration, creating a cycle.

Solution: Extract common network types to lib and import
from both modules.

Fixes #456
```

```
perf(build): enable LTO and PGO for release builds

Measured 40% performance improvement in benchmarks.
Build time increased by 2 minutes but worth the tradeoff.

Benchmark results:
- fibonacci(45): 3.2s -> 1.9s
- matrix_mult: 850ms -> 510ms
```

## Branch Strategy

### Main Branches
- `main`: Production-ready, always stable, tagged releases
- `develop`: Integration branch for features

### Supporting Branches
- `feature/*`: New features or enhancements
- `fix/*`: Bug fixes
- `hotfix/*`: Critical production fixes
- `experiment/*`: Experimental/POC work (may not be merged)

### Workflow

```bash
# Start feature
git checkout -b feature/add-rust-overlay develop

# Work on feature, commit atomically
git commit -m "feat(overlay): add rust-overlay integration"

# Keep up to date
git fetch origin
git rebase origin/develop

# When ready, merge to develop
git checkout develop
git merge --no-ff feature/add-rust-overlay

# Create release
git checkout -b release/1.2.0 develop
# Bump version, update CHANGELOG
git commit -m "chore: prepare release 1.2.0"

# Merge to main and tag
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
```

## Pre-commit Hooks

Automate quality checks before commits:

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash

set -e

echo "Running pre-commit checks..."

# Nix formatting
if command -v nixpkgs-fmt &> /dev/null; then
    echo "Formatting Nix files..."
    git diff --cached --name-only --diff-filter=ACM | \
        grep '\.nix$' | \
        xargs nixpkgs-fmt
fi

# Nix linting
if command -v statix &> /dev/null; then
    echo "Linting Nix files..."
    git diff --cached --name-only --diff-filter=ACM | \
        grep '\.nix$' | \
        xargs statix check
fi

# Deadnix (unused bindings)
if command -v deadnix &> /dev/null; then
    echo "Checking for dead code..."
    git diff --cached --name-only --diff-filter=ACM | \
        grep '\.nix$' | \
        xargs deadnix
fi

# Nix evaluation check
echo "Checking Nix expressions..."
if [ -f flake.nix ]; then
    nix flake check --no-build
fi

# Shell scripts
if command -v shellcheck &> /dev/null; then
    echo "Checking shell scripts..."
    git diff --cached --name-only --diff-filter=ACM | \
        grep '\.sh$' | \
        xargs shellcheck
fi

echo "All checks passed!"
```

## Flake-Integrated Pre-commit

Use `pre-commit-hooks.nix` in your flake:

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
  };

  outputs = { self, nixpkgs, pre-commit-hooks }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      checks.${system}.pre-commit = pre-commit-hooks.lib.${system}.run {
        src = ./.;
        hooks = {
          # Nix
          nixpkgs-fmt.enable = true;
          statix.enable = true;
          deadnix.enable = true;
          
          # Shell
          shellcheck.enable = true;
          shfmt.enable = true;
          
          # Markdown
          markdownlint.enable = true;
          
          # YAML
          yamllint.enable = true;
        };
      };
      
      devShells.${system}.default = pkgs.mkShell {
        inherit (self.checks.${system}.pre-commit) shellHook;
        buildInputs = self.checks.${system}.pre-commit.enabledPackages;
      };
    };
}
```

## Changelog Management

Maintain `CHANGELOG.md` using Keep a Changelog format:

```markdown
# Changelog

## [Unreleased]

### Added
- Cross-compilation support for ARM64
- Rust overlay integration

### Changed
- Updated nixpkgs to latest unstable

### Fixed
- Circular dependency in network module

## [1.2.0] - 2024-01-15

### Added
- New flake templates for Rust projects
- Pre-commit hooks integration

### Changed
- Improved build performance with LTO

## [1.1.0] - 2023-12-01
...
```

## Tagging Strategy

Use semantic versioning (MAJOR.MINOR.PATCH):

```bash
# Annotated tag for releases
git tag -a v1.2.0 -m "Release version 1.2.0

- Add feature X
- Fix bug Y
- Improve performance Z"

# Lightweight tag for internal milestones
git tag milestone-20240115

# Push tags
git push origin v1.2.0
git push origin --tags
```

## Flake Lock Management

Treat `flake.lock` as a lockfile (like `Cargo.lock`):

```bash
# Update all inputs
git commit -m "chore(flake): update all inputs"
nix flake update
git add flake.lock
git commit --amend --no-edit

# Update specific input
nix flake lock --update-input nixpkgs
git add flake.lock
git commit -m "chore(flake): update nixpkgs to latest"

# Pin to specific commit
nix flake lock --override-input nixpkgs github:NixOS/nixpkgs/COMMIT_HASH
```

## Commit History Management

### Interactive Rebase

Clean up commits before merging:

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Common operations:
# - pick: keep commit as-is
# - reword: change commit message
# - squash: combine with previous commit
# - fixup: like squash but discard message
# - drop: remove commit
```

### Amend Last Commit

```bash
# Add more changes to last commit
git add changed-file
git commit --amend --no-edit

# Change last commit message
git commit --amend -m "Better message"
```

### Cherry-pick

Apply specific commits from other branches:

```bash
# Apply single commit
git cherry-pick COMMIT_HASH

# Apply range of commits
git cherry-pick START_HASH..END_HASH
```

## Bisect for Debugging

Find which commit introduced a bug:

```bash
# Start bisecting
git bisect start

# Mark current as bad
git bisect bad

# Mark last known good commit
git bisect good v1.0.0

# Git will checkout middle commit
# Test and mark:
git bisect good  # or bad

# Continue until found
# When done:
git bisect reset
```

## Merge vs Rebase

**Use merge** when:
- Integrating feature branches into develop/main
- Preserving branch history is important
- Working on public/shared branches

**Use rebase** when:
- Keeping feature branch up to date with main
- Cleaning up local commits before push
- Working on private branches

```bash
# Update feature branch with latest main
git checkout feature/my-feature
git rebase main

# Interactive rebase to clean up
git rebase -i main
```

## Stash Management

Temporarily store changes:

```bash
# Stash current changes
git stash save "WIP: working on feature X"

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Show stash contents
git stash show -p stash@{0}

# Drop stash
git stash drop stash@{0}
```

## Aliases for Efficiency

Add to `~/.gitconfig`:

```ini
[alias]
    # Short status
    st = status -sb
    
    # Pretty log
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    
    # Amend without editing message
    amend = commit --amend --no-edit
    
    # Show files in last commit
    last = show --name-only
    
    # Undo last commit but keep changes
    undo = reset HEAD~1 --soft
    
    # Clean up merged branches
    cleanup = "!git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d"
```

## Troubleshooting

### Undo Last Push

```bash
# If you haven't pushed to shared branch
git reset --hard HEAD~1
git push --force

# Safer: create revert commit
git revert HEAD
git push
```

### Fix Diverged Branches

```bash
# Pull with rebase
git pull --rebase origin main

# Resolve conflicts
git add .
git rebase --continue
```

### Remove Sensitive Data

```bash
# Remove file from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch PATH/TO/FILE" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

## Best Practices

1. **Commit often**: Small, focused commits are easier to understand and revert
2. **Write meaningful messages**: Future you will thank present you
3. **Review before push**: Use `git diff` and `git log` to verify changes
4. **Keep branches short-lived**: Merge or delete after use
5. **Use `.gitignore`**: Don't commit generated files or secrets
6. **Test before commit**: Ensure builds work and tests pass
7. **Sign commits**: Use GPG signatures for security (optional but recommended)

## Integration with Nix

### Nix-specific .gitignore

```
# Nix build results
result
result-*

# direnv
.direnv/
.envrc

# Nix develop shells
.devenv/

# VM images
*.qcow2

# Nix profile links
profile/
```

### Flake Metadata in Commits

Reference flake revisions in commits:

```
feat(flake): update nixpkgs

Updated to latest unstable branch.

Flake revision: nixpkgs/aabc123...
Date: 2024-01-15
```
