# Git Automation Scripts Toolkit (2026)

A collection of high-utility scripts for common Git maintenance tasks.

## 1. The "Prune Everything" Script
Removes merged branches and cleans up local caches.
```bash
git fetch --prune
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
```

## 2. The "Nuke and Reinstall" Script
Use this for deep build corruption.
```bash
rm -rf node_modules .next
bun install
```

## 3. The "Semantic Release" Alias
Automates versioning and changelog generation.
```bash
alias g-release="npx semantic-release --no-ci"
```

## 4. The "Security Scrub"
Scan for secrets before pushing.
```bash
alias g-scan="npx gitleaks detect --source . --verbose"
```

## 5. The "Stacked PR" Helper
Automatically restacks local branches against main.
```bash
gt restack
```

---
*Updated: January 22, 2026 - 19:05*
