**Skill**: [Doppler Credential Workflows](../SKILL.md)

## Use Case 2: AWS Credential Management

### Quick Start

```bash
# Use AWS credentials
doppler run --project aws-credentials --config dev \
  --command='aws s3 ls --region $AWS_DEFAULT_REGION'
```

### Credential Setup

**Doppler Storage:**

- Project: `aws-credentials`
- Configs: `dev`, `staging`, `prod` (one per AWS account)

**Required Secrets:**

```
AWS_ACCESS_KEY_ID           # IAM access key (20 chars)
AWS_SECRET_ACCESS_KEY       # IAM secret (40 chars)
AWS_DEFAULT_REGION          # e.g., us-east-1
AWS_ACCOUNT_ID              # For audit trail
AWS_LAST_ROTATED_DATE       # Timestamp
AWS_ROTATION_INTERVAL_DAYS  # e.g., 90
```

### AWS Rotation Workflow

**Step 1: Create New Credentials**

```bash
# In AWS IAM Console:
# Users → Select user → Security credentials → Create access key
```

**Step 2: Store in Doppler**

```bash
/usr/bin/env bash << 'CONFIG_EOF'
echo -n 'AKIAIOSFODNN7EXAMPLE' | doppler secrets set AWS_ACCESS_KEY_ID \
  --project aws-credentials --config dev

echo -n 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY' | \
  doppler secrets set AWS_SECRET_ACCESS_KEY \
  --project aws-credentials --config dev

doppler secrets set AWS_LAST_ROTATED_DATE \
  --project aws-credentials --config dev \
  --value "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CONFIG_EOF
```

**Step 3: Verify Injection**

```bash
/usr/bin/env bash << 'CONFIG_EOF_2'
doppler run --project aws-credentials --config dev \
  --command='echo "KEY: ${#AWS_ACCESS_KEY_ID}; SECRET: ${#AWS_SECRET_ACCESS_KEY}"'
# Expected: KEY: 20; SECRET: 40
CONFIG_EOF_2
```

**Step 4: Test AWS Access**

```bash
doppler run --project aws-credentials --config dev \
  --command='aws sts get-caller-identity'
# Expected output: UserId, Account, Arn
```

**Step 5: Deactivate Old Key**

```bash
# In AWS IAM Console:
# Mark old key as Inactive → Wait 24 hours → Delete
```

### AWS Troubleshooting

**Issue: 403 Forbidden / InvalidClientTokenId**

- Root cause: Credentials expired/rotated elsewhere, or wrong region
- Verify: `doppler run --command='aws sts get-caller-identity'`
- Check region: `doppler secrets get AWS_DEFAULT_REGION --plain`

**Issue: Works on One Machine, Not Another**

- Root cause: Different Doppler config or HOME variable
- Verify: `doppler me` (check logged-in user), `echo $HOME`
