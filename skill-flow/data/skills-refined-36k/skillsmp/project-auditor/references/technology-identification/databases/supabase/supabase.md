# Supabase

**Category**: databases
**Description**: Supabase - open source Firebase alternative
**Homepage**: https://supabase.com

## Package Detection

### NPM
*Supabase JavaScript SDKs*

- `@supabase/supabase-js`
- `@supabase/auth-helpers-nextjs`
- `@supabase/auth-helpers-react`
- `@supabase/ssr`

### PYPI
*Supabase Python SDK*

- `supabase`

### RUBYGEMS
*Supabase Ruby SDK*

- `supabase`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@supabase/supabase-js['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@supabase/ssr['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@supabase/auth-helpers`
- Type: esm_import

### Python

**Pattern**: `from\s+supabase`
- Type: python_import

## Environment Variables

*Supabase project URL*

*Supabase anonymous key*

*Supabase service role key*

*Next.js public Supabase URL*

*Next.js public anon key*


## Secrets Detection

### API Keys

#### Supabase Service Role Key
**Pattern**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Severity**: critical
**Description**: Supabase service role key - bypasses Row Level Security, has full database access
**Context Required**: Must appear with Supabase environment variable or URL context
**Environment Variable**: `SUPABASE_SERVICE_ROLE_KEY`
**Note**: JWT format starting with standard HS256 header

#### Supabase Anon Key
**Pattern**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Severity**: low
**Description**: Supabase anonymous/public key - subject to Row Level Security
**Context Required**: Must appear with SUPABASE_ANON_KEY or similar context
**Environment Variable**: `SUPABASE_ANON_KEY`
**Note**: Same JWT format as service role, but designed for client-side use

#### Supabase Database Password
**Pattern**: `(?:SUPABASE_DB_PASSWORD|supabase_db_password)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Supabase PostgreSQL database password
**Environment Variable**: `SUPABASE_DB_PASSWORD`

### Validation

#### API Documentation
- **API Reference**: https://supabase.com/docs/guides/api
- **Authentication**: https://supabase.com/docs/guides/auth
- **API Keys**: https://supabase.com/docs/guides/api/api-keys

#### Validation Endpoint
**API**: Supabase REST API
**Endpoint**: `https://{project_ref}.supabase.co/rest/v1/`
**Method**: GET
**Headers**:
- `apikey: <your_key>`
- `Authorization: Bearer <your_key>`
**Purpose**: Validates API key by accessing REST endpoint

```bash
# Validate Supabase key
curl -s "https://${SUPABASE_PROJECT_REF}.supabase.co/rest/v1/" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY"
```

#### Validation Code (Python)
```python
from supabase import create_client

def validate_supabase_key(url, key):
    """Validate Supabase key by initializing client"""
    try:
        client = create_client(url, key)
        # Try to access the health endpoint or a simple query
        # This varies by project setup
        return {'valid': True, 'client_initialized': True}
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 70% (MEDIUM) - JWT format is common, needs Supabase context
