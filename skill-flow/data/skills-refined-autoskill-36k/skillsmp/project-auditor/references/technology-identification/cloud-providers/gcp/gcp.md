# Google Cloud Platform

**Category**: cloud-providers
**Description**: Google Cloud Platform SDK and services
**Homepage**: https://cloud.google.com

## Package Detection

### NPM
*GCP Node.js client libraries*

- `@google-cloud/storage`
- `@google-cloud/pubsub`
- `@google-cloud/firestore`
- `@google-cloud/bigquery`
- `@google-cloud/functions-framework`

### PYPI
*GCP Python client libraries*

- `google-cloud-storage`
- `google-cloud-pubsub`
- `google-cloud-firestore`
- `google-cloud-bigquery`
- `google-api-python-client`

### MAVEN
*GCP Java client libraries*

- `com.google.cloud:google-cloud-storage`
- `com.google.cloud:google-cloud-pubsub`

### GO
*GCP Go client libraries*

- `cloud.google.com/go/storage`
- `cloud.google.com/go/pubsub`
- `cloud.google.com/go/firestore`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@google-cloud/`
- Type: esm_import

**Pattern**: `require\(['"]@google-cloud/`
- Type: commonjs_require

### Python

**Pattern**: `from\s+google\.cloud`
- Type: python_import

**Pattern**: `import\s+google\.cloud`
- Type: python_import

### Go

**Pattern**: `"cloud\.google\.com/go/`
- Type: go_import

## Environment Variables

*Path to service account JSON*

*GCP project ID*

*GCP project ID*

*GCP project ID*

*GCP region*

*Google Cloud Storage bucket*


## Secrets Detection

### Service Account Credentials

#### GCP Service Account JSON Key
**Pattern**: `"type":\s*"service_account"[^}]*"private_key":\s*"-----BEGIN`
**Severity**: critical
**Description**: GCP service account JSON key file - provides full access to authorized GCP services
**Context Required**: Must contain both "type": "service_account" and "private_key"
**Note**: Service account keys are JSON files, not single strings

#### GCP Service Account Private Key
**Pattern**: `-----BEGIN RSA PRIVATE KEY-----[A-Za-z0-9+/=\s]+-----END RSA PRIVATE KEY-----`
**Severity**: critical
**Description**: Private key extracted from GCP service account JSON
**Context Required**: Should appear within service account JSON context

#### GCP API Key
**Pattern**: `AIza[0-9A-Za-z_-]{35}`
**Severity**: high
**Description**: Google Cloud/Firebase API key - used for client-side APIs
**Example**: `AIzaSyAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Note**: Often restricted by referrer/IP, but still sensitive

#### GCP OAuth Client Secret
**Pattern**: `GOCSPX-[A-Za-z0-9_-]{28}`
**Severity**: high
**Description**: Google OAuth 2.0 client secret (new format)
**Example**: `GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Validation

#### API Documentation
- **Service Accounts**: https://cloud.google.com/iam/docs/service-accounts
- **API Keys**: https://cloud.google.com/docs/authentication/api-keys
- **Authentication Best Practices**: https://cloud.google.com/docs/authentication

#### Validation Endpoint
**API**: GCP IAM testIamPermissions
**Method**: POST
**Purpose**: Validates service account credentials by checking permissions
**Note**: Requires valid project ID and authenticated credentials

```bash
# Validate GCP service account key
gcloud auth activate-service-account --key-file=service-account.json
gcloud auth list
```

#### Validation Code (Python)
```python
from google.oauth2 import service_account
from google.cloud import storage

def validate_gcp_service_account(key_path):
    """Validate GCP service account key by listing storage buckets"""
    try:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = storage.Client(credentials=credentials)
        # Simple operation to verify credentials
        buckets = list(client.list_buckets(max_results=1))
        return {
            'valid': True,
            'project_id': credentials.project_id,
            'service_account': credentials.service_account_email
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 90% (HIGH) - Service account JSON structure is distinctive
