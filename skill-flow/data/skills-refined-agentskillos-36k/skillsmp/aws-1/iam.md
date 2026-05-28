# IAM & Permissions

## Quick Status Checks
```bash
# Check if role exists
aws iam get-role --role-name ROLE_NAME

# List attached managed policies
aws iam list-attached-role-policies --role-name ROLE_NAME

# List inline policies (if any)
aws iam list-role-policies --role-name ROLE_NAME
```

## Check Role Existence & Policies
```bash
# Check if role exists
aws iam get-role --role-name ROLE_NAME

# List attached managed policies
aws iam list-attached-role-policies --role-name ROLE_NAME

# List inline policies (if any)
aws iam list-role-policies --role-name ROLE_NAME

# Get specific inline policy
aws iam get-role-policy --role-name ROLE_NAME --policy-name POLICY_NAME
```

## Permission Issues
1. Look for "Access Denied" in logs
2. Check IAM role policies with `list-attached-role-policies`
3. For KMS issues, verify `get-key-policy` includes the role
4. Check CloudWatch Logs permissions if log access fails

## Common Placeholders
- `ROLE_NAME` - IAM role name (e.g., `app-instance-role`, `lambda-execution-role`)
- `POLICY_NAME` - Inline policy name
- `KEY_ID` - KMS key ID for encryption/decryption checks

## JSON Parsing Examples
```bash
# Query attached policies
aws iam list-attached-role-policies --role-name ROLE_NAME --query 'AttachedPolicies[].PolicyName'

# Get policy document
aws iam get-role-policy --role-name ROLE_NAME --policy-name POLICY_NAME --output json | jq '.PolicyDocument'
```
