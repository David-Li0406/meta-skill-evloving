---
name: sd-repos
description: Quick reference for SD/SIC (Sustainability Dashboard/Sustainability Insight Center) repositories. Use when answering questions about (1) which repositories are SD/SIC repos, (2) which repos are ADS apps, (3) where repositories are located locally or remotely, (4) repository categorization, (5) SD terminology equivalence, (6) management scripts in SD directory, or (7) deployment/Kubernetes information for SD applications.
---

# SD/SIC Repository Finder

## Overview

Quickly locate and identify SD/SIC repositories both locally and remotely. Understand the equivalence between SD (Sustainability Dashboard) and SIC (Sustainability Insight Center) terminology, and distinguish ADS applications from other infrastructure repositories.

## Key Terminology

**SD = Sustainability Dashboard = SIC = Sustainability Insight Center**

These terms are completely interchangeable and refer to the same product.

**ADS = Application Deployment Service**

ADS refers to applications tagged with the `ads-app` GitHub topic. NOT "Anomaly Detection Service" or "Application Delivery Service".

## Quick Repository Locations

- **Local:** `/Users/kevin/git/glcp/sd/`
- **Remote:** GitHub organization `glcp` (https://github.com/glcp/)

## Finding Repositories

### Check if a Repository is an ADS App

```bash
# Single repository check
gh api "repos/glcp/{repo_name}/topics" --jq '.names[]' | grep -q "ads-app"

# Using bundled script
bash scripts/check_ads_app.sh sd-data-service
```

### List All Remote SD Repositories

```bash
# Most efficient method - all SD repos
gh search repos --owner glcp --topic sustainability-dashboard --limit 100 --json name,description,language

# Only ADS-tagged repos
gh search repos --owner glcp --topic ads-app sd- --limit 100 --json name,description,language
```

### List All Local ADS Apps

```bash
# Manual check in SD directory
cd /Users/kevin/git/glcp/sd
for repo in sd-*/; do 
  repo_name=$(basename "$repo")
  topics=$(gh api "repos/glcp/$repo_name/topics" --jq '.names[]' 2>/dev/null)
  if echo "$topics" | grep -q "ads-app"; then 
    echo "$repo_name"
  fi
done

# Using bundled script
bash scripts/list_all_ads_apps.sh
```

## Repository Categories

**14 ADS Applications** - Tagged with both `sustainability-dashboard` AND `ads-app`:
- Backend Services (Kotlin): 11 microservices
- Frontend (TypeScript): sd-frontend
- ML/Data Science (Python): sd-ad-*, sd-ml-forecasting

**Non-ADS Repositories** - Tagged with `sustainability-dashboard` only:
- Infrastructure: sd-deploy-repo, sd-ops, sd-terraform-alerts
- Frontend: sd-ops-frontend

For the complete repository list with descriptions, see [repository-catalog.md](references/repository-catalog.md).

## Management Scripts

Located in `/Users/kevin/git/glcp/sd/`:
- `create_*_prs.sh` - PR creation automation
- `update_*.sh` - Repository update scripts
- `check_*.sh` - Verification scripts
- `merge_all_prs.sh` - PR merge automation

## Deployment & Kubernetes

For comprehensive cluster access and deployment information:
```bash
cat /Users/kevin/git/glcp/sd/sd-ops/copilot/comprehensive-cluster-guide.md
```

## Bundled Resources

### scripts/
- `check_ads_app.sh` - Check if a repository has the ads-app topic
- `list_all_ads_apps.sh` - List all ADS apps in local SD directory

### references/
- `repository-catalog.md` - Complete repository list with descriptions, categories, and locations
