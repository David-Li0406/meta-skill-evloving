# AWS Credentials Management with Doppler

**Secure credential storage, rotation, and documentation workflow**

---

## Overview

This workflow manages AWS IAM credentials using Doppler for secure storage, rotation, and comprehensive documentation. All credentials are stored with contextual notes for future reference.

**Key Features:**

- ✅ Zero-exposure credential creation (never displayed on screen)
- ✅ Safe dual-key rotation (old key remains active during testing)
- ✅ Comprehensive access audits (read-only, non-intrusive)
- ✅ Full documentation in Doppler (notes, activity logs, versioning)

---

## Doppler Project Structure

**Project**: `aws-credentials`
**Config**: `dev` (or `staging`, `production`)

**Secrets**:

```
AWS_ACCESS_KEY_ID              # Active primary credential
AWS_SECRET_ACCESS_KEY          # Active primary credential
AWS_ACCESS_KEY_ID_OLD          # Archived for rollback (30-day retention)
AWS_SECRET_ACCESS_KEY_OLD      # Archived for rollback
AWS_DEFAULT_REGION             # Primary AWS region
AWS_ACCOUNT_ID                 # AWS account ID (for reference)
AWS_ACCESS_INVENTORY_REPORT    # Full JSON audit report
AWS_ACCESS_SUMMARY             # Human-readable access summary
AWS_LAST_AUDIT_DATE            # Last audit timestamp
```

All secrets include detailed notes explaining their purpose, history, and usage.

---

## Credential Rotation Workflow

### Prerequisites

- AWS allows max 2 access keys per IAM user
- Current setup: 1 active key → 1 available slot
- Both keys attached to same IAM user = identical permissions

### Phase 1: Store Old Credentials

Store existing credentials for rollback safety:

```bash
# Store old credentials
echo 'AKIAXXXXXXXXXX' | doppler secrets set AWS_ACCESS_KEY_ID_OLD --project aws-credentials --config dev
echo 'old-secret-key' | doppler secrets set AWS_SECRET_ACCESS_KEY_OLD --project aws-credentials --config dev

# Document retention policy
doppler secrets notes set AWS_ACCESS_KEY_ID_OLD \
  "DEPRECATED - Created 2025-XX-XX, exposed 2025-XX-XX. Kept for 30-day rollback period. AWS IAM key remains ACTIVE during testing. Delete after 2025-XX-XX." \
  --project aws-credentials
```

### Phase 2: Create New Credentials (Zero Exposure)

Create new AWS access key and pipe directly to Doppler:

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Create key and save to temp file
aws iam create-access-key --user-name <username> --profile <profile> --output json > /tmp/new_aws_key.json

# Extract and store in Doppler (never displayed)
cat /tmp/new_aws_key.json | jq -r '.AccessKey.AccessKeyId' | \
  doppler secrets set AWS_ACCESS_KEY_ID --project aws-credentials --config dev --silent

cat /tmp/new_aws_key.json | jq -r '.AccessKey.SecretAccessKey' | \
  doppler secrets set AWS_SECRET_ACCESS_KEY --project aws-credentials --config dev --silent

# Securely delete temp file
shred -u /tmp/new_aws_key.json 2>/dev/null || rm -f /tmp/new_aws_key.json

# Document the new credential
doppler secrets notes set AWS_ACCESS_KEY_ID \
  "PRIMARY - Created $(date +%Y-%m-%d) via secure rotation. Replaces AWS_ACCESS_KEY_ID_OLD after security exposure. This is the active production credential." \
  --project aws-credentials
CONFIG_EOF
```

### Phase 3: Testing Period (Both Keys Active)

**Verify both keys work:**

```bash
# Verify both keys exist in AWS IAM
aws iam list-access-keys --user-name <username> --profile <profile>
# Should show 2 active keys

# Test new credential
doppler run --project aws-credentials --config dev -- aws sts get-caller-identity
doppler run --project aws-credentials --config dev -- aws s3 ls

# Test old credential (still works)
aws sts get-caller-identity --profile <profile>
```

**Both keys have identical permissions** - test thoroughly before deletion.

### Phase 4: Cleanup (User Approval Required)

**⚠️ Only proceed after confirming new credential works perfectly**

```bash
/usr/bin/env bash << 'DOPPLER_EOF'
# Delete old AWS IAM key
aws iam delete-access-key --access-key-id AKIAXXXXXXXXXX --user-name <username> --profile <profile>

# Update Doppler notes
doppler secrets notes set AWS_ACCESS_KEY_ID_OLD \
  "ARCHIVED - Created 2025-XX-XX, exposed 2025-XX-XX, AWS IAM key deleted $(date +%Y-%m-%d). Kept for audit trail. No longer valid in AWS." \
  --project aws-credentials
DOPPLER_EOF
```

---

## Access Audit & Inventory

### Read-Only Audit Commands

**100% safe** - only list/describe/get operations, zero modifications:

```bash
# IAM permissions
aws iam get-account-authorization-details --output json
aws iam list-attached-user-policies --user-name <username>
aws iam list-groups-for-user --user-name <username>

# Resource inventory
aws s3api list-buckets
aws lambda list-functions --region us-west-2
aws dynamodb list-tables --region us-west-2
aws ecs list-clusters --region us-west-2
aws ecr describe-repositories --region us-west-2
aws cloudwatch describe-alarms --region us-west-2
aws logs describe-log-groups --region us-west-2 --max-items 100
```

### Generate Comprehensive Report

```bash
/usr/bin/env bash << 'CONFIG_EOF_2'
# Run comprehensive audit (15+ services)
# Store results in /tmp/aws_*.json files
# Generate JSON report: /tmp/aws_access_report.json
# Generate summary: /tmp/aws_access_summary.txt

# Store in Doppler
cat /tmp/aws_access_report.json | doppler secrets set AWS_ACCESS_INVENTORY_REPORT --project aws-credentials --config dev
cat /tmp/aws_access_summary.txt | doppler secrets set AWS_ACCESS_SUMMARY --project aws-credentials --config dev
date -u +"%Y-%m-%dT%H:%M:%SZ" | doppler secrets set AWS_LAST_AUDIT_DATE --project aws-credentials --config dev

# Add documentation notes
doppler secrets notes set AWS_ACCESS_INVENTORY_REPORT \
  "Complete AWS resource inventory (JSON format) generated $(date +%Y-%m-%d). Documents all accessible services, resources, IAM permissions, and credential verification results. Generated via read-only audit commands. Use this for: compliance audits, permission reviews, onboarding documentation." \
  --project aws-credentials
CONFIG_EOF_2
```

---

## Usage Patterns

### Basic Usage

```bash
# General pattern
doppler run --project aws-credentials --config dev -- aws <command>

# Examples
doppler run --project aws-credentials --config dev -- aws s3 ls
doppler run --project aws-credentials --config dev -- aws lambda list-functions --region us-west-2
doppler run --project aws-credentials --config dev -- python my_aws_script.py
```

### Query Documentation

```bash
# View all secrets with notes
doppler secrets --project aws-credentials --config dev

# View specific report
doppler secrets get AWS_ACCESS_SUMMARY --project aws-credentials --config dev --plain
doppler secrets get AWS_ACCESS_INVENTORY_REPORT --project aws-credentials --config dev --plain | jq .

# View activity history
doppler activity --project aws-credentials

# Dashboard access
open https://dashboard.doppler.com
```

---

## Stored Reports

### AWS_ACCESS_INVENTORY_REPORT (JSON)

Machine-readable inventory with:

- IAM permissions and policies
- Resource counts by service
- Detailed resource lists
- Credential verification results
- Audit metadata

**Use for:** Automation, compliance reporting, detailed analysis

### AWS_ACCESS_SUMMARY (Text)

Human-readable summary with:

- IAM user and permissions
- Resource inventory counts
- Key resources by service
- Credential comparison results
- Access level explanation

**Use for:** Quick reference, onboarding, permission review

### AWS_LAST_AUDIT_DATE (Timestamp)

Last comprehensive audit date.

**Recommended cadence:** Quarterly or after permission changes

---

## Security Best Practices

### Credential Handling

✅ **DO**:

- Use Doppler for all credential storage
- Pipe credentials directly to Doppler (never display)
- Test thoroughly before deleting old credentials
- Document all changes with notes
- Rotate credentials quarterly or when exposed

✗ **DON'T**:

- Store credentials in plain text files
- Display credentials on screen
- Share credentials via chat/email
- Delete old credentials without testing new ones
- Skip documentation/notes

### Audit Safety

✅ **Safe commands** (read-only):

- `list-*` - List resources
- `describe-*` - Describe resources
- `get-*` - Get resource details

✗ **Avoid during audits**:

- `create-*`, `delete-*`, `update-*` - Modify resources
- `put-*` - Write operations
- Any command without `--dry-run` flag when available

---

## Account Details

**Current Setup:**

- **IAM User**: `terryli`
- **Account ID**: `050214414362` (EonLabs)
- **Group**: `fullstack-eng`
- **Region**: `us-west-2`

**Effective Permissions:** Near-Administrator

- ✅ Full access to S3, Lambda, DynamoDB, ECS, ECR, CloudWatch
- ✅ Can create/modify/delete most resources
- ✗ Cannot modify IAM users/policies
- ✗ Cannot modify AWS Organizations

**Key Resources:**

- 33 S3 buckets (ML models, portfolios, predictions)
- 28 Lambda functions (Touchstone, Cron, Realtime)
- 19 DynamoDB tables (ModelPredictions, TradeModels, etc.)
- 2 ECS clusters, 3 ECR repositories

---

## Troubleshooting

### "Config not found"

```bash
# List available configs
doppler configs --project aws-credentials

# Doppler defaults to dev/stg/prd
# Use --config flag explicitly if using custom names
```

### Credentials not working

```bash
# Verify Doppler is injecting credentials
doppler run --project aws-credentials --config dev -- env | grep AWS

# Test with simple command
doppler run --project aws-credentials --config dev -- aws sts get-caller-identity

# Check AWS CLI version
aws --version
```

### Need to rollback to old credential

```bash
/usr/bin/env bash << 'CONFIG_EOF_3'
# Copy OLD credentials to primary names
doppler secrets get AWS_ACCESS_KEY_ID_OLD --plain | \
  doppler secrets set AWS_ACCESS_KEY_ID --project aws-credentials --config dev

doppler secrets get AWS_SECRET_ACCESS_KEY_OLD --plain | \
  doppler secrets set AWS_SECRET_ACCESS_KEY --project aws-credentials --config dev

# Update notes
doppler secrets notes set AWS_ACCESS_KEY_ID \
  "ROLLED BACK - Restored from AWS_ACCESS_KEY_ID_OLD on $(date +%Y-%m-%d) due to [reason]" \
  --project aws-credentials
CONFIG_EOF_3
```

---

## Related Documentation

**Hub (User Memory)**:

- **User Memory**: `~/.claude/CLAUDE.md` - Global workspace configuration and conventions
- **Documentation Index**: `docs/INDEX.md` - Hub-and-spoke navigation

**Specifications (Machine-Readable)**:

- **Doppler Integration**: `specifications/doppler-integration.yaml` - OpenAPI 3.1.0 spec
- **AWS Credentials Management**: `specifications/aws-credentials-management.yaml` - Complete workflow spec

**Setup Guides (Human-Readable)**:

- **This Document**: Rotation and usage workflows
- **Elimination Plan**: `docs/setup/aws-credentials-elimination.md` - Reference implementation for ml-feature-experiments

---

**Last Updated**: 2025-10-11
