# Microsoft Azure

**Category**: cloud-providers
**Description**: Microsoft Azure SDK and services
**Homepage**: https://azure.microsoft.com

## Package Detection

### NPM
*Azure Node.js SDKs*

- `@azure/storage-blob`
- `@azure/identity`
- `@azure/cosmos`
- `@azure/service-bus`
- `@azure/functions`

### PYPI
*Azure Python SDKs*

- `azure-storage-blob`
- `azure-identity`
- `azure-cosmos`
- `azure-servicebus`
- `azure-functions`

### NUGET
*Azure .NET SDKs*

- `Azure.Storage.Blobs`
- `Azure.Identity`
- `Microsoft.Azure.Cosmos`

### MAVEN
*Azure Java SDKs*

- `com.azure:azure-storage-blob`
- `com.azure:azure-identity`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@azure/`
- Type: esm_import

**Pattern**: `require\(['"]@azure/`
- Type: commonjs_require

### Python

**Pattern**: `^from azure import`
- Type: python_import

**Pattern**: `^import azure`
- Type: python_import

**Pattern**: `^from azure.storage import`
- Type: python_import

**Pattern**: `^from azure.identity import`
- Type: python_import

### Csharp

**Pattern**: `using Azure\.`
- Type: regex

**Pattern**: `using Microsoft\.Azure\.`
- Type: regex

## Environment Variables

*Azure subscription ID*

*Azure tenant ID*

*Azure client/app ID*

*Azure client secret*

*Azure Storage connection*

*Azure Storage account name*


## Secrets Detection

### API Keys and Credentials

#### Azure Storage Connection String
**Pattern**: `DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{88};`
**Severity**: critical
**Description**: Azure Storage account connection string with access key
**Example**: `DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=xxx...==;EndpointSuffix=core.windows.net`
**Environment Variable**: `AZURE_STORAGE_CONNECTION_STRING`

#### Azure Storage Account Key
**Pattern**: `(?<![A-Za-z0-9+/=])[A-Za-z0-9+/=]{88}(?![A-Za-z0-9+/=])`
**Severity**: critical
**Description**: Azure Storage account access key (88 characters, base64)
**Context Required**: Must appear near `AccountKey`, `azure`, or storage-related context
**Note**: High false positive rate without context

#### Azure Client Secret
**Pattern**: `(?:client_secret|AZURE_CLIENT_SECRET)\s*[=:]\s*['"]?([A-Za-z0-9_~.-]{34,})['"]?`
**Severity**: critical
**Description**: Azure AD application client secret
**Example**: `AZURE_CLIENT_SECRET=xxxx~xxxx.xxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `AZURE_CLIENT_SECRET`

#### Azure SAS Token
**Pattern**: `sv=\d{4}-\d{2}-\d{2}&[^&]*sig=[A-Za-z0-9%+/=]+`
**Severity**: high
**Description**: Azure Shared Access Signature (SAS) token
**Example**: `?sv=2021-06-08&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=...&sig=...`
**Note**: Time-limited but provides delegated access

#### Azure Cosmos DB Key
**Pattern**: `AccountEndpoint=https://[^;]+\.documents\.azure\.com[^;]*;AccountKey=[A-Za-z0-9+/=]{88};`
**Severity**: critical
**Description**: Azure Cosmos DB connection string
**Example**: `AccountEndpoint=https://mydb.documents.azure.com:443/;AccountKey=xxx...==;`

#### Azure Service Bus Connection String
**Pattern**: `Endpoint=sb://[^;]+\.servicebus\.windows\.net/;SharedAccessKeyName=[^;]+;SharedAccessKey=[A-Za-z0-9+/=]{44}`
**Severity**: critical
**Description**: Azure Service Bus connection string with SAS key
**Example**: `Endpoint=sb://mybus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xxx...=`

### Validation

#### API Documentation
- **Authentication Overview**: https://docs.microsoft.com/en-us/azure/active-directory/develop/
- **Storage Auth**: https://docs.microsoft.com/en-us/azure/storage/common/storage-auth
- **Service Principal**: https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal

#### Validation Endpoint
**API**: Azure Resource Manager
**Endpoint**: `https://management.azure.com/subscriptions?api-version=2020-01-01`
**Method**: GET
**Headers**: `Authorization: Bearer <access_token>`
**Purpose**: Validates credentials by listing accessible subscriptions

```bash
# Validate Azure credentials via CLI
az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
az account list
```

#### Validation Code (Python)
```python
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient

def validate_azure_credentials(tenant_id, client_id, client_secret):
    """Validate Azure service principal credentials"""
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        sub_client = SubscriptionClient(credential)
        subscriptions = list(sub_client.subscriptions.list())
        return {
            'valid': True,
            'subscription_count': len(subscriptions),
            'subscriptions': [s.display_name for s in subscriptions[:5]]
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 85% (MEDIUM) - Connection strings have distinctive format
