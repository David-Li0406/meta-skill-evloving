# SendGrid

**Category**: business-tools/email
**Homepage**: https://sendgrid.com

## Package Detection

### NPM
*SendGrid Node.js SDK*

- `@sendgrid/mail`
- `@sendgrid/client`

### PYPI
*SendGrid Python SDK*

- `sendgrid`

### RUBYGEMS
*SendGrid Ruby SDK*

- `sendgrid-ruby`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@sendgrid/mail['"]`
- Type: esm_import

### Python

**Pattern**: `from\s+sendgrid`
- Type: python_import

## Environment Variables


## Secrets Detection

### API Keys

#### SendGrid API Key
**Pattern**: `SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}`
**Severity**: critical
**Description**: SendGrid API key - provides access to send emails and manage account
**Example**: `SG.xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `SENDGRID_API_KEY`

### Validation

#### API Documentation
- **API Reference**: https://docs.sendgrid.com/api-reference
- **Authentication**: https://docs.sendgrid.com/for-developers/sending-email/authentication
- **API Keys**: https://docs.sendgrid.com/ui/account-and-settings/api-keys

#### Validation Endpoint
**API**: SendGrid Scopes API
**Endpoint**: `https://api.sendgrid.com/v3/scopes`
**Method**: GET
**Headers**:
- `Authorization: Bearer <your_api_key>`
**Purpose**: Validates API key by retrieving key permissions (free endpoint)

```bash
# Validate SendGrid API key
curl -s https://api.sendgrid.com/v3/scopes \
  -H "Authorization: Bearer $SENDGRID_API_KEY" | head -c 200
```

#### Validation Code (Python)
```python
import requests

def validate_sendgrid_key(api_key):
    """Validate SendGrid API key by fetching scopes"""
    try:
        response = requests.get(
            'https://api.sendgrid.com/v3/scopes',
            headers={'Authorization': f'Bearer {api_key}'}
        )
        if response.status_code == 200:
            return {'valid': True, 'scopes': response.json().get('scopes', [])}
        return {'valid': False, 'status': response.status_code}
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 99% (HIGH) - Very distinctive `SG.` prefix with specific format
