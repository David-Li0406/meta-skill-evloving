# AWS Cognito

**Category**: authentication
**Description**: Amazon Cognito user authentication and identity management
**Homepage**: https://aws.amazon.com/cognito/

## Package Detection

### NPM
*AWS Cognito JavaScript SDKs*

- `amazon-cognito-identity-js`
- `@aws-amplify/auth`
- `aws-amplify`
- `@aws-sdk/client-cognito-identity-provider`

### PYPI
*AWS Cognito Python SDKs*

- `warrant`
- `pycognito`

### MAVEN
*AWS Cognito Java SDKs*

- `software.amazon.awssdk:cognitoidentityprovider`
- `com.amazonaws:aws-java-sdk-cognitoidp`

### GO
*AWS Cognito Go SDK*

- `github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider`

### NUGET
*AWS Cognito .NET SDKs*

- `AWSSDK.CognitoIdentityProvider`
- `Amazon.Extensions.CognitoAuthentication`

### Related Packages
- `@aws-amplify/ui-react`
- `aws-jwt-verify`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]amazon-cognito-identity-js['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@aws-amplify/auth['"]`
- Type: esm_import

**Pattern**: `from\s+['"]aws-amplify['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@aws-sdk/client-cognito-identity-provider['"]`
- Type: esm_import

**Pattern**: `require\(['"]amazon-cognito-identity-js['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `from\s+pycognito`
- Type: python_import

**Pattern**: `import\s+pycognito`
- Type: python_import

**Pattern**: `boto3\.client\(['"]cognito-idp['"]\)`
- Type: python_import

### Go

**Pattern**: `"github\.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider"`
- Type: go_import

## Environment Variables

*Cognito user pool ID*

*Cognito app client ID*

*Cognito app client secret*

*Cognito identity pool ID*

*AWS region for Cognito*

*Next.js public Cognito user pool ID*

*Next.js public Cognito client ID*

*AWS prefixed Cognito user pool ID*


## Detection Notes

- Check for COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID environment variables
- Look for cognito-idp.*.amazonaws.com references
- Often used with AWS Amplify

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
