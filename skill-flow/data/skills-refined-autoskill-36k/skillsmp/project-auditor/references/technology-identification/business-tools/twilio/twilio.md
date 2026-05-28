# Twilio

**Category**: business-tools
**Description**: Cloud communications platform (SMS, Voice, Video)
**Homepage**: https://twilio.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Twilio JavaScript packages*

- `twilio` - Twilio Node.js SDK
- `twilio-video` - Video SDK
- `twilio-chat` - Chat SDK
- `@twilio/voice-sdk` - Voice SDK

#### PYPI
*Twilio Python packages*

- `twilio` - Twilio Python SDK

#### RUBYGEMS
*Twilio Ruby packages*

- `twilio-ruby` - Ruby SDK

#### GO
*Twilio Go packages*

- `github.com/twilio/twilio-go` - Go SDK

#### MAVEN
*Twilio Java packages*

- `com.twilio.sdk:twilio` - Java SDK

#### NUGET
*Twilio .NET packages*

- `Twilio` - .NET SDK

#### PACKAGIST
*Twilio PHP packages*

- `twilio/sdk` - PHP SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]twilio['"]`
- Twilio SDK import
- Example: `import twilio from 'twilio';`

**Pattern**: `require\(['"]twilio['"]\)`
- Twilio require
- Example: `const twilio = require('twilio');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+twilio\s+import`
- Twilio Python import
- Example: `from twilio.rest import Client`

**Pattern**: `^from\s+twilio\.rest\s+import`
- Twilio REST client import

### Code Patterns

**Pattern**: `twilio\.com|api\.twilio\.com`
- Twilio URLs

**Pattern**: `TWILIO_|twilio_`
- Twilio environment variables
- Example: `TWILIO_ACCOUNT_SID`

**Pattern**: `AC[a-f0-9]{32}`
- Twilio Account SID format
- Example: `ACabc123def456...`

**Pattern**: `twilio\(\s*['"]AC[a-f0-9]{32}['"]`
- Twilio client initialization
- Example: `twilio('ACabc123...', 'authToken')`

**Pattern**: `messages\.create|calls\.create|client\.messages`
- Twilio API operations

---

## Environment Variables

- `TWILIO_ACCOUNT_SID` - Account SID
- `TWILIO_AUTH_TOKEN` - Auth Token
- `TWILIO_API_KEY` - API Key SID
- `TWILIO_API_SECRET` - API Key Secret
- `TWILIO_PHONE_NUMBER` - Phone number

## Detection Notes

- Account SID starts with "AC"
- Auth Token is 32 hex characters
- API keys for fine-grained access
- SMS, Voice, Video, Chat products
- Webhook URLs for callbacks

---

## Secrets Detection

### Credentials

#### Twilio Account SID
**Pattern**: `AC[a-f0-9]{32}`
**Severity**: medium
**Description**: Twilio Account SID (public identifier)
**Example**: `ACabc123def456789...`

#### Twilio Auth Token
**Pattern**: `(?:twilio|TWILIO).*(?:auth[_-]?token|AUTH[_-]?TOKEN)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Twilio authentication token
**Example**: `TWILIO_AUTH_TOKEN=abc123def456...`

#### Twilio API Key Secret
**Pattern**: `(?:twilio|TWILIO).*(?:api[_-]?secret|API[_-]?SECRET)\s*[=:]\s*['"]?([a-zA-Z0-9]{32})['"]?`
**Severity**: critical
**Description**: Twilio API key secret

### Validation

#### API Documentation
- **REST API**: https://www.twilio.com/docs/usage/api
- **Authentication**: https://www.twilio.com/docs/iam/credentials/api

#### Validation Endpoint
**API**: Account
**Endpoint**: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}.json`
**Method**: GET
**Auth**: Basic Auth (AccountSid:AuthToken)
**Purpose**: Validates credentials

```bash
curl -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
     "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID.json"
```

---

## TIER 3: Configuration Extraction

### Account SID Extraction

**Pattern**: `(?:accountSid|account[_-]?sid|TWILIO_ACCOUNT_SID)\s*[=:]\s*['"]?(AC[a-f0-9]{32})['"]?`
- Twilio Account SID
- Extracts: `account_sid`

### Phone Number Extraction

**Pattern**: `(?:phoneNumber|phone[_-]?number|TWILIO_PHONE_NUMBER)\s*[=:]\s*['"]?(\+[0-9]{11,15})['"]?`
- Twilio phone number
- Extracts: `phone_number`
- Example: `+15551234567`
