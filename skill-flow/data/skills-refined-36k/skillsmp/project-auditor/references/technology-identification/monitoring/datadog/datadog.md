# Datadog

**Category**: monitoring
**Description**: Datadog monitoring, APM, and observability platform
**Homepage**: https://www.datadoghq.com

## Package Detection

### NPM
*Datadog Node.js APM and browser SDK*

- `dd-trace`
- `datadog-metrics`
- `@datadog/browser-rum`
- `@datadog/browser-logs`

### PYPI
*Datadog Python APM and API client*

- `ddtrace`
- `datadog`
- `datadog-api-client`

### RUBYGEMS
*Datadog Ruby APM and StatsD client*

- `ddtrace`
- `dogapi`
- `dogstatsd-ruby`

### MAVEN
*Datadog Java APM*

- `com.datadoghq:dd-trace-api`
- `com.datadoghq:dd-java-agent`

### GO
*Datadog Go APM and StatsD client*

- `gopkg.in/DataDog/dd-trace-go.v1`
- `github.com/DataDog/datadog-go`

### Related Packages
- `@datadog/datadog-ci`
- `serverless-plugin-datadog`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]dd-trace['"]`
- Type: esm_import

**Pattern**: `require\(['"]dd-trace['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]@datadog/browser-rum['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@datadog/browser-logs['"]`
- Type: esm_import

### Python

**Pattern**: `from\s+ddtrace`
- Type: python_import

**Pattern**: `import\s+ddtrace`
- Type: python_import

**Pattern**: `from\s+datadog`
- Type: python_import

### Go

**Pattern**: `"gopkg\.in/DataDog/dd-trace-go`
- Type: go_import

**Pattern**: `"github\.com/DataDog/datadog-go`
- Type: go_import

## Environment Variables

*Datadog API key*

*Datadog application key*

*Datadog agent host*

*Service name for APM*

*Environment tag*

*Version tag*

*Enable APM tracing*

*Enable log correlation*

*Datadog site (datadoghq.com, datadoghq.eu)*


## Detection Notes

- Check for DD_API_KEY environment variable
- Look for datadog-agent in Docker configs
- Common with APM tracing and custom metrics

## Secrets Detection

### API Keys

#### Datadog API Key
**Pattern**: `(?:DD_API_KEY|datadog_api_key)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: high
**Description**: Datadog API key - used to submit metrics, events, and logs
**Example**: `DD_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `DD_API_KEY`
**Note**: 32-character hexadecimal string

#### Datadog Application Key
**Pattern**: `(?:DD_APP_KEY|datadog_app_key)\s*[=:]\s*['"]?([a-f0-9]{40})['"]?`
**Severity**: high
**Description**: Datadog application key - used for programmatic API access
**Example**: `DD_APP_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `DD_APP_KEY`
**Note**: 40-character hexadecimal string

### Validation

#### API Documentation
- **API Reference**: https://docs.datadoghq.com/api/latest/
- **Authentication**: https://docs.datadoghq.com/api/latest/authentication/
- **API and App Keys**: https://docs.datadoghq.com/account_management/api-app-keys/

#### Validation Endpoint
**API**: Datadog Validate API Key
**Endpoint**: `https://api.datadoghq.com/api/v1/validate`
**Method**: GET
**Headers**:
- `DD-API-KEY: <your_api_key>`
**Purpose**: Validates API key (specifically designed for validation)

```bash
# Validate Datadog API key
curl -s "https://api.datadoghq.com/api/v1/validate" \
  -H "DD-API-KEY: $DD_API_KEY"
```

#### Validation Code (Python)
```python
import requests

def validate_datadog_key(api_key, site='datadoghq.com'):
    """Validate Datadog API key"""
    try:
        response = requests.get(
            f'https://api.{site}/api/v1/validate',
            headers={'DD-API-KEY': api_key}
        )
        if response.status_code == 200:
            return {'valid': True, 'response': response.json()}
        return {'valid': False, 'status': response.status_code}
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 80% (MEDIUM) - Keys are hex strings, need context for confidence
