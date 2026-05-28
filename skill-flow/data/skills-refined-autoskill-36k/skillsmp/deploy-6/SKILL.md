---
name: deploy
description: Deploy CDKTF infrastructure stacks to AWS. Handles stack deployment, asset staging, output management, and environment configuration. Understands deployment sequences and stack dependencies.
allowed-tools: Read, Bash, Glob, Grep, Task
user-invocable: true
---

# Deploy Skill

## Purpose

Execute CDKTF infrastructure deployments using the unified `cdk.mjs` orchestrator. Handles stack dependencies, asset staging, output management, and environment configuration.

**Key Tool**: `node scripts/cdk.mjs` for all CDK operations

## Usage

```
/deploy status                    # Check deployment status of all stacks
/deploy <stack|group>             # Deploy specific stack or group
/deploy all                       # Deploy all stacks in dependency order
/deploy lambdas                   # Deploy only lambda stacks (common for code changes)
/deploy --prod <stack|group>      # Deploy to production environment
/deploy outputs <stack|group>     # Pull outputs from deployed stacks
/deploy prepare                   # Build all apps and stage assets
```

## Architecture Reference

### Stacks

| Stack | Purpose | Group |
|-------|---------|-------|
| `myapp-api-stack` | DynamoDB tables (users, verification, rate limit, deny list) | infra |
| `myapp-analytics-stack` | EventBridge, DLQ, analytics tables, log groups | infra |
| `myapp-api-lambda-stack` | Lambda packaging, IAM role, analytics permissions | lambdas |
| `myapp-analytics-lambda-stack` | Analytics processor Lambda | lambdas |
| `myapp-client-website-stack` | S3 + CloudFront static hosting | website |
| `myapp-bootstrap-stack` | CDKTF backend/state resources | (standalone) |

### Stack Groups

| Group | Stacks | Typical Use |
|-------|--------|-------------|
| `infra` | api-stack, analytics-stack | Infrastructure changes |
| `lambdas` | api-lambda-stack, analytics-lambda-stack | Code deployments |
| `website` | client-website-stack | Frontend deployments |
| `all` | All stacks in dependency order | Full deployment |

### Dependency Order

```
bootstrap -> infra -> lambdas -> website
```

Infrastructure stacks must be deployed before lambdas (lambdas reference table ARNs).

## Deployment Process

### Step 1: Check Current Status

```bash
node scripts/cdk.mjs status
```

Review:
- Which stacks are deployed
- Which stacks have pending changes
- Any stacks in error state

### Step 2: Validate Prerequisites

```bash
node scripts/cdk.mjs validate <stack|group>
```

This checks:
- Required assets exist
- Dependencies are deployed
- Environment configuration is valid

### Step 3: Prepare Assets (If Needed)

If validation fails due to missing assets:

```bash
# Build all apps and copy assets
node scripts/cdk.mjs prepare
```

This produces:
- `cdk/platform-cdk/dist/lambda.zip`
- `cdk/platform-cdk/dist/lambdas/`
- `cdk/platform-cdk/dist/client-website/`

### Step 4: Deploy

```bash
# Deploy specific stack or group
node scripts/cdk.mjs deploy <stack|group> --auto-approve

# Deploy all stacks
node scripts/cdk.mjs deploy all --auto-approve
```

**IMPORTANT**: Always use `--auto-approve` for non-interactive execution.

### Step 5: Refresh Outputs

After infrastructure changes, refresh outputs for local development:

```bash
node scripts/cdk.mjs outputs infra
```

### Step 6: Report Results

```markdown
## Deployment Complete

**Environment**: dev
**Stacks Deployed**:
- myapp-api-stack
- myapp-api-lambda-stack

**Outputs Refreshed**: Yes

**Next Steps**:
- Run `npm test` to verify deployment
- Check CloudWatch logs for any errors
```

## Common Operations

### Deploy Everything (Dev)

```bash
# Full deployment with automatic prerequisite handling
node scripts/cdk.mjs deploy all --auto-approve
```

Or step by step:

```bash
# 1. Prepare assets
node scripts/cdk.mjs prepare

# 2. Deploy infrastructure first
node scripts/cdk.mjs deploy infra --auto-approve

# 3. Deploy lambdas
node scripts/cdk.mjs deploy lambdas --auto-approve

# 4. Deploy website
node scripts/cdk.mjs deploy website --auto-approve
```

### Deploy to Production

**Always preview first**:

```bash
# Preview changes
node scripts/cdk.mjs deploy all --prod --dry-run

# Review output carefully, then deploy
node scripts/cdk.mjs deploy all --prod --auto-approve
```

### Deploy Only Lambdas (Code Change)

Most common for code-only changes:

```bash
node scripts/cdk.mjs deploy lambdas --auto-approve
```

### Refresh Local Outputs

After someone else deploys or after infrastructure changes:

```bash
node scripts/cdk.mjs outputs infra
```

### Check Deployment Status

```bash
node scripts/cdk.mjs status
```

### List Available Stacks

```bash
node scripts/cdk.mjs list
```

### Destroy Stacks

```bash
# Destroy specific stack (use with caution)
node scripts/cdk.mjs destroy <stack|group> --auto-approve
```

### Bootstrap CDKTF Backend

If the S3 backend doesn't exist:

```bash
node scripts/cdk.mjs bootstrap --auto-approve
```

## Sequence Runner

For predefined command sequences:

```bash
# List available sequences
npm run sequence -- list

# Run a sequence
npm run sequence -- run <name> [--dry-run]
```

### Available Sequences

| Sequence | Description |
|----------|-------------|
| `build-deploy-api-lambda` | Build and deploy API lambda |
| `deploy-infra` | Deploy infrastructure stacks |
| `deploy-lambdas` | Build and deploy all lambdas |
| `full-deploy` | Full deployment: prepare + deploy all |
| `clean-and-deploy` | Clean rebuild + full deployment + tests |
| `refresh-outputs` | Pull fresh outputs from infra stacks |

## Environment Management

### Environment Files

| File | Purpose |
|------|---------|
| `cdk/platform-cdk/.env.dev` | Dev AWS credentials/config |
| `cdk/platform-cdk/.env.production` | Prod AWS credentials/config |
| `apps/node-server/.env.dev` | Server dev config |
| `apps/node-server/.env.production` | Server prod config |

### Decrypt/Encrypt Envs

```bash
# Decrypt for local editing
npm -w @cdk/platform-cdk run decrypt-envs

# Re-encrypt after edits
npm -w @cdk/platform-cdk run encrypt-envs
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `node scripts/cdk.mjs status` | Check deployment status |
| `node scripts/cdk.mjs validate <target>` | Validate prerequisites |
| `node scripts/cdk.mjs deploy <target> --auto-approve` | Deploy stack/group |
| `node scripts/cdk.mjs outputs <target>` | Pull outputs |
| `node scripts/cdk.mjs build` | Build apps and copy assets |
| `node scripts/cdk.mjs prepare` | Full preparation: build + assets + outputs |
| `node scripts/cdk.mjs synth` | Synthesize Terraform configuration |
| `node scripts/cdk.mjs list` | List available stacks |
| `node scripts/cdk.mjs destroy <target> --auto-approve` | Destroy stacks |
| `node scripts/cdk.mjs bootstrap --auto-approve` | Bootstrap CDKTF backend |

### Flags

| Flag | Purpose |
|------|---------|
| `--prod` | Target production environment |
| `--dry-run` | Preview without executing |
| `--force` | Force deployment even if validation fails |
| `--auto-approve` | Skip interactive prompts (REQUIRED) |

## Troubleshooting

### Missing Outputs

If app can't find CDK outputs:

```bash
node scripts/cdk.mjs outputs infra
```

### Validation Failures

```bash
# Check what's missing
node scripts/cdk.mjs validate <stack|group>

# Run preparation
node scripts/cdk.mjs prepare

# Retry deploy
node scripts/cdk.mjs deploy <stack|group> --auto-approve
```

### Stale Artifacts

Force rebuild:

```bash
node scripts/cdk.mjs build --force --no-cache
```

### Bootstrap Issues

If the S3 backend doesn't exist:

```bash
node scripts/cdk.mjs bootstrap --auto-approve
```

### Build Failures

1. Check error output
2. Run `npm run build` directly to see detailed errors
3. Fix code issues
4. Retry deployment

### Deployment Failures

1. Check error message for specific stack
2. Run `node scripts/cdk.mjs status` to see state
3. Check AWS console for resource-level errors
4. Report with specific error details

## Subagent Dispatch

This skill invokes the `deployer` subagent for operations:

```javascript
Task({
  description: "Deploy lambdas to dev",
  prompt: `Deploy the lambdas stack group to dev environment.

  1. Check current status
  2. Validate prerequisites
  3. Deploy with --auto-approve
  4. Report results

  Use node scripts/cdk.mjs for all operations.`,
  subagent_type: "deployer"
})
```

## Integration with Other Skills

### After Implementation

After `/implement` completes, deploy to verify:

```
/deploy lambdas           # Deploy code changes
```

### After Security Review

Before merge, ensure deployment works:

```
/deploy all --dry-run     # Verify deployment will succeed
```

### Production Deployment

After merge to main:

```
/deploy all --prod        # Deploy to production
```

## Success Criteria

Deployment is complete when:

- All requested stacks deployed successfully
- Outputs refreshed and available to apps
- No deployment errors in output
- Status shows all stacks in sync

## Error Handling

### Build Failures

**Action**:
1. Check error output
2. Run `npm run build` directly for details
3. Fix code issues
4. Retry deployment

### Deployment Failures

**Action**:
1. Check error message for specific stack
2. Run `node scripts/cdk.mjs status`
3. Check AWS console for resource errors
4. Report to orchestrator with specific error

### Dependency Failures

If a dependency isn't deployed:

```bash
# Check what's needed
node scripts/cdk.mjs validate <target>

# Deploy dependencies first
node scripts/cdk.mjs deploy infra --auto-approve

# Then deploy target
node scripts/cdk.mjs deploy lambdas --auto-approve
```

## Examples

### Example 1: Quick Lambda Deployment

```
User: Deploy my lambda changes

/deploy lambdas

Result:
## Deployment Complete

**Environment**: dev
**Stacks Deployed**:
- myapp-api-lambda-stack
- myapp-analytics-lambda-stack

**Duration**: 45s
**Status**: All stacks in sync
```

### Example 2: Full Production Deployment

```
User: Deploy everything to production

/deploy --prod all

Steps:
1. Preview: node scripts/cdk.mjs deploy all --prod --dry-run
2. User confirms changes look correct
3. Deploy: node scripts/cdk.mjs deploy all --prod --auto-approve
4. Verify: node scripts/cdk.mjs status

Result:
## Production Deployment Complete

**Environment**: production
**Stacks Deployed**: 5/5
**Outputs Refreshed**: Yes
```

### Example 3: Troubleshooting Failed Deployment

```
User: Deployment failed, help me fix it

/deploy status

Steps:
1. Check status: node scripts/cdk.mjs status
2. Identify failed stack
3. Check validation: node scripts/cdk.mjs validate <failed-stack>
4. Run preparation if needed: node scripts/cdk.mjs prepare
5. Retry deployment

Result:
## Issue Resolved

**Problem**: Missing lambda.zip artifact
**Solution**: Ran prepare to rebuild assets
**Status**: All stacks now deployed successfully
```
