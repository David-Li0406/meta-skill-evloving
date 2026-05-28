# API Keys

**Category**: devops/secrets/api-keys
**Description**: Detection patterns for API keys and service credentials
**CWE**: CWE-798, CWE-312

---

## AI/ML Services

### OpenAI API Key
**Pattern**: `sk-[A-Za-z0-9]{48}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- OpenAI API keys start with `sk-` followed by 48 alphanumeric characters

### OpenAI Project API Key
**Pattern**: `sk-proj-[A-Za-z0-9]{48}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- OpenAI project-scoped API keys

### Anthropic API Key
**Pattern**: `sk-ant-[A-Za-z0-9_-]{90,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Anthropic API keys start with `sk-ant-` followed by ~95 characters

### Hugging Face Token
**Pattern**: `hf_[A-Za-z0-9]{34}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Hugging Face tokens start with `hf_`

---

## Payment Services

### Stripe Live Secret Key
**Pattern**: `sk_live_[0-9a-zA-Z]{24,}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Stripe live secret keys - critical as they access real payment data

### Stripe Test Secret Key
**Pattern**: `sk_test_[0-9a-zA-Z]{24,}`
**Type**: regex
**Severity**: low
**Languages**: [all]
- Stripe test keys - lower severity, no real payment access

### Stripe Restricted Key
**Pattern**: `rk_live_[0-9a-zA-Z]{24,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Stripe restricted API keys

### PayPal Access Token
**Pattern**: `access_token\$[a-zA-Z0-9]{32}\$[a-zA-Z0-9]{64}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- PayPal OAuth access tokens

### PayPal Client ID
**Pattern**: `A[a-zA-Z0-9_-]{79}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- PayPal client ID credentials

### Square Access Token
**Pattern**: `sq0[a-z]{3}-[A-Za-z0-9_-]{22}`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Square API access tokens

### Square Sandbox Token
**Pattern**: `sandbox-sq0[a-z]{3}-[A-Za-z0-9_-]{22}`
**Type**: regex
**Severity**: low
**Languages**: [all]
- Square sandbox tokens

---

## Communication Services

### Twilio Account SID
**Pattern**: `AC[a-f0-9]{32}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Twilio Account SID identifier

### Twilio Auth Token
**Pattern**: `[a-f0-9]{32}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Twilio auth token (requires context: TWILIO_ env vars)
- CWE-798: Use of Hard-coded Credentials

### SendGrid API Key
**Pattern**: `SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- SendGrid API keys with distinctive dot-separated format

### Mailgun API Key
**Pattern**: `key-[a-f0-9]{32}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Mailgun API keys start with `key-`

### Mailchimp API Key
**Pattern**: `[a-f0-9]{32}-us[0-9]{1,2}`
**Type**: regex
**Severity**: low
**Languages**: [all]
- Mailchimp API keys include datacenter suffix

---

## Developer Platforms

### GitHub Classic PAT
**Pattern**: `ghp_[A-Za-z0-9_]{36,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitHub personal access tokens (classic)

### GitHub Fine-grained PAT
**Pattern**: `github_pat_[A-Za-z0-9_]{22,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitHub fine-grained personal access tokens

### GitHub OAuth Token
**Pattern**: `gho_[A-Za-z0-9_]{36,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitHub OAuth access tokens

### GitHub App Token
**Pattern**: `ghs_[A-Za-z0-9_]{36,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitHub App installation access tokens

### GitHub Refresh Token
**Pattern**: `ghr_[A-Za-z0-9_]{36,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitHub refresh tokens

### GitLab PAT
**Pattern**: `glpat-[A-Za-z0-9-]{20,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitLab personal access tokens

### GitLab Runner Token
**Pattern**: `GR1348941[A-Za-z0-9_-]{20}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- GitLab CI runner registration tokens

### NPM Token
**Pattern**: `npm_[A-Za-z0-9]{36}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- NPM automation tokens for package publishing

### PyPI Token
**Pattern**: `pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- PyPI API tokens (base64-encoded)

---

## Monitoring & Analytics

### Datadog API Key
**Pattern**: `[a-f0-9]{32}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Datadog API key (requires context: DD_API_KEY, DD_APP_KEY)

### Sentry DSN Key
**Pattern**: `[a-f0-9]{32}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Sentry DSN key component (requires context: SENTRY_DSN, sentry.io URLs)

### New Relic API Key
**Pattern**: `NRAK-[A-Z0-9]{27}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- New Relic REST API keys

### New Relic License Key
**Pattern**: `[a-f0-9]{40}NRAL`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- New Relic license keys

---

## Social Platforms

### Slack Bot Token
**Pattern**: `xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Slack bot tokens

### Slack User Token
**Pattern**: `xoxp-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Slack user tokens

### Slack App Token
**Pattern**: `xoxa-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Slack app-level tokens

### Slack Webhook URL
**Pattern**: `https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Slack incoming webhook URLs

### Discord Bot Token
**Pattern**: `[MN][A-Za-z0-9_-]{23,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27}`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Discord bot tokens

### Discord Webhook URL
**Pattern**: `https://discord(app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Discord webhook URLs

### Twitter Bearer Token
**Pattern**: `AAAAAAAAAAAAA[A-Za-z0-9%]+`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Twitter/X API bearer tokens

---

## Detection Notes

### Context Clues
- Environment variable assignments
- Configuration file keys
- SDK initialization calls
- Header values in HTTP code

### Common False Positives
- Placeholder strings (YOUR_API_KEY)
- Example documentation values
- Test/mock values in test files
- Base64 data that matches patterns

### Severity Considerations
- **Production vs Test**: Test keys are lower severity
- **Scope**: Keys with broad permissions are higher severity
- **Exposure**: Public repos vs private repos

---

## References

- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
