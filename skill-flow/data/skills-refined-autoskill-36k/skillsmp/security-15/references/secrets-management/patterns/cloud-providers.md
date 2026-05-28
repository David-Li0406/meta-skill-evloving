# Cloud Provider Credentials

**Category**: devops/secrets/cloud-providers
**Description**: Detection patterns for cloud provider API keys and credentials
**CWE**: CWE-798, CWE-312

---

## AWS (Amazon Web Services)

### AWS Access Key ID
**Pattern**: `AKIA[0-9A-Z]{16}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- AWS Access Key IDs always start with `AKIA`
- CWE-798: Use of Hard-coded Credentials

### AWS Secret Access Key
**Pattern**: `[A-Za-z0-9/+=]{40}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- 40-character base64-encoded strings
- Usually found near AKIA access key IDs

### AWS Session Token
**Pattern**: `FwoGZXIvYXdzE[A-Za-z0-9/+=]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Temporary credentials from STS
- Starts with `FwoGZXIvYXdzE`

### AWS ARN Pattern
**Pattern**: `arn:aws:[a-z0-9-]+:[a-z0-9-]*:[0-9]*:[a-zA-Z0-9-_/:.]+`
**Type**: regex
**Severity**: informational
**Languages**: [all]
- Not secrets but may expose infrastructure details

---

## GCP (Google Cloud Platform)

### GCP Service Account Key
**Pattern**: `"type": "service_account"`
**Type**: regex
**Severity**: critical
**Languages**: [json]
- JSON files containing service account credentials
- Look for: project_id, private_key_id, private_key, client_email

### GCP API Key
**Pattern**: `AIza[0-9A-Za-z_-]{35}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GCP API keys start with `AIza`

### GCP OAuth Client ID
**Pattern**: `[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com`
**Type**: regex
**Severity**: high
**Languages**: [all]
- OAuth 2.0 client IDs for Google APIs

---

## Azure

### Azure Storage Account Key
**Pattern**: `[A-Za-z0-9+/]{86}==`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Base64-encoded 64-byte keys
- Context: Near "AccountKey=" or storage connection strings

### Azure Storage Connection String
**Pattern**: `DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/]{86}==`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Full Azure Storage connection strings

### Azure Service Principal Secret
**Pattern**: `[a-zA-Z0-9_~.-]{34}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Azure AD application secrets
- Context: Near "client_secret" or "AZURE_CLIENT_SECRET"

### Azure SAS Token
**Pattern**: `sv=[0-9-]+&s[a-z]=[a-z]+&[a-z]+=[^&]+(&[a-z]+=[^&]+)*&sig=[A-Za-z0-9%/+=]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Shared Access Signature tokens for Azure resources

---

## DigitalOcean

### DigitalOcean Personal Access Token
**Pattern**: `dop_v1_[a-f0-9]{64}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- DigitalOcean API tokens start with `dop_v1_`

### DigitalOcean Spaces Key
**Pattern**: `DO[0-9A-Z]{18}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- DigitalOcean Spaces access keys

---

## Heroku

### Heroku API Key
**Pattern**: `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- UUID-formatted API keys
- Context: HEROKU_API_KEY environment variable

---

## Detection Notes

### Critical Indicators
- Files named `credentials`, `secrets`, `.aws/credentials`
- Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Configuration files with embedded credentials

### Common False Positives
- Example/placeholder values: `AKIAIOSFODNN7EXAMPLE`
- Documentation strings
- Test fixtures with mock credentials
- Base64-encoded non-secret data matching patterns

### Remediation Priority
1. **Critical**: Rotate immediately, revoke old credentials
2. **High**: Rotate within 24 hours
3. **Medium**: Schedule rotation, assess exposure

---

## References

- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
