# Secrets Scanner RAG Knowledge Base

Knowledge base for detecting exposed secrets and credentials in source code.

## Directory Structure

```
secrets-scanner/
├── patterns/           # Secret detection patterns by type
│   ├── cloud-providers.md    # AWS, GCP, Azure credentials
│   ├── api-keys.md           # API keys for various services
│   ├── tokens.md             # OAuth, JWT, session tokens
│   ├── database.md           # Database connection strings
│   └── certificates.md       # Private keys and certificates
├── remediation/        # Remediation guidance
│   ├── rotation.md           # Secret rotation procedures
│   ├── prevention.md         # Prevention best practices
│   └── incident-response.md  # Steps when secrets are exposed
└── detection-rules/    # Detection configuration
    ├── severity.md           # Severity classification
    ├── false-positives.md    # Common false positives
    └── exclusions.md         # Files/patterns to exclude
```

## Usage

This RAG is used by the secrets-scanner-data.sh extractor to provide context for:
- Pattern matching and detection
- Severity classification
- Remediation recommendations
- False positive reduction

## Integration

The secrets scanner supports:
- **TruffleHog**: Enhanced scanning when available
- **Pattern matching**: Regex-based detection as fallback
- **Git history**: Can scan commit history for leaked secrets
