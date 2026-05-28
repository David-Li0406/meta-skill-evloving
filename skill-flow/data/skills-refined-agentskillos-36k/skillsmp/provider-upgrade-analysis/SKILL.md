---
name: provider-upgrade-analysis
description: Use when analyzing Terraform provider or module upgrades for breaking changes, deprecations, and migration requirements.
---

# Provider Upgrade Analysis

## Overview

Analyze the impact of upgrading Terraform providers or modules before making changes. Identify breaking changes, deprecations, and required code modifications.

**Announce at start:** "I'm using the provider-upgrade-analysis skill to assess this upgrade."

## Process

### Step 1: Identify Current State

```bash
# Current Terraform version
terraform version

# Current provider versions
terraform providers

# Lock file details
cat .terraform.lock.hcl
```

### Step 2: Identify Target Version

Determine what version to upgrade to:
- Latest stable
- Specific version requested
- Next major/minor version

### Step 3: Research Breaking Changes

For each provider/module upgrade:

#### AWS Provider Example

```bash
# Check CHANGELOG
# https://github.com/hashicorp/terraform-provider-aws/blob/main/CHANGELOG.md

# Check UPGRADE guide for major versions
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/version-5-upgrade
```

#### Key Sources

| Provider | Changelog Location | Upgrade Guide |
|----------|-------------------|---------------|
| AWS | GitHub CHANGELOG.md | /docs/guides/version-X-upgrade |
| Azure | GitHub CHANGELOG.md | /docs/guides/X.0-upgrade-guide |
| Google | GitHub CHANGELOG.md | /docs/guides/version_X_upgrade |

### Step 4: Analyze Impact

#### Breaking Changes Categories

| Category | Impact | Example |
|----------|--------|---------|
| **Removed Resources** | HIGH | Resource type no longer exists |
| **Removed Arguments** | HIGH | Required attribute removed |
| **Changed Defaults** | MEDIUM | Default value changed |
| **Renamed Resources** | MEDIUM | Resource renamed, state migration needed |
| **New Required Args** | MEDIUM | New required argument added |
| **Deprecations** | LOW | Will be removed in future |

#### Code Scan

Search for affected resources/attributes:
```bash
# Find usage of deprecated resource
grep -r "aws_deprecated_resource" --include="*.tf"

# Find usage of removed argument
grep -r "removed_argument" --include="*.tf"
```

### Step 5: Check Memory

Query `memory/global/provider-issues.json` for:
- Known issues with target version
- Past upgrade experiences
- Workarounds needed

### Step 6: Generate Report

```markdown
## Provider Upgrade Analysis

### Summary

| Provider | Current | Target | Risk Level |
|----------|---------|--------|------------|
| aws | 4.67.0 | 5.0.0 | HIGH |

### Breaking Changes

#### 1. [Change Name]
- **Type:** Removed Argument
- **Affected Resource:** `aws_instance`
- **Attribute:** `ebs_optimized` default changed
- **Impact:** Instances may change on next apply
- **Required Action:** Explicitly set `ebs_optimized = true`
- **Files Affected:**
  - `modules/compute/main.tf:45`
  - `environments/prod/instances.tf:23`

#### 2. [Change Name]
...

### Deprecations (Future Concern)

| Resource/Attribute | Deprecated In | Removed In | Replacement |
|-------------------|---------------|------------|-------------|
| `aws_old_thing` | 4.50.0 | 5.0.0 | `aws_new_thing` |

### State Migration Required

- [ ] Resource `aws_old` → `aws_new` requires state mv
- [ ] [Other migrations]

### Recommended Upgrade Path

1. **Backup state**
   ```bash
   terraform state pull > backup-$(date +%Y%m%d).tfstate
   ```

2. **Update version constraint**
   ```hcl
   terraform {
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
   }
   ```

3. **Run init**
   ```bash
   terraform init -upgrade
   ```

4. **Apply code changes**
   [List of required changes]

5. **Run plan**
   ```bash
   terraform plan
   ```

6. **Review and apply**
   [After careful review]

### Risk Assessment

| Factor | Assessment |
|--------|------------|
| Breaking changes | X items |
| State migrations | Y required |
| Code changes | Z files |
| Estimated effort | [Low/Medium/High] |
| Recommended timing | [Now/After testing/Wait] |

### Known Issues

[From memory or research]
```

### Step 7: Update Memory

Store findings in `memory/global/provider-issues.json`:
```json
{
  "aws": {
    "5.0.0": {
      "known_issues": [...],
      "upgrade_notes": [...],
      "last_updated": "2024-01-15"
    }
  }
}
```

## Common Upgrade Patterns

### Major Version Upgrades (e.g., 4.x → 5.x)

- Usually have breaking changes
- Check upgrade guide thoroughly
- Plan for state migrations
- Test in non-prod first

### Minor Version Upgrades (e.g., 5.1 → 5.2)

- Usually backward compatible
- Check for deprecation warnings
- Review CHANGELOG for new features

### Patch Version Upgrades (e.g., 5.1.0 → 5.1.1)

- Bug fixes only
- Generally safe to apply
- Still review CHANGELOG

## Safety Checklist

Before recommending upgrade:
- [ ] Breaking changes documented
- [ ] Code changes identified
- [ ] State migrations planned
- [ ] Rollback procedure defined
- [ ] Test environment validated
- [ ] User informed of risks
