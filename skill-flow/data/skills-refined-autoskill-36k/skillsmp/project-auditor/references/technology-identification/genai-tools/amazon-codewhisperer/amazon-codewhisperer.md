# Amazon CodeWhisperer (Amazon Q Developer)

**Category**: genai-tools
**Description**: AWS AI-powered code suggestions and security scanning
**Homepage**: https://aws.amazon.com/codewhisperer/

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*AWS Toolkit packages*

- `@aws/amazon-q-developer-cli` - Amazon Q CLI
- `aws-toolkit-vscode` - AWS Toolkit for VS Code

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate CodeWhisperer usage*

- `.aws/` - AWS configuration directory
- `codewhisperer-settings.json` - CodeWhisperer settings

### Code Patterns

**Pattern**: `codewhisperer|amazon[_-]?q`
- CodeWhisperer/Amazon Q references
- Example: `codewhisperer.enable`

**Pattern**: `AWS_CODEWHISPERER|AMAZON_Q_`
- Environment variables
- Example: `AWS_CODEWHISPERER_ENABLED`

**Pattern**: `"AmazonWebServices\.aws-toolkit-vscode"`
- VS Code extension ID

**Pattern**: `com\.aws\.toolkit`
- JetBrains plugin ID

### IDE Extension Patterns

**Pattern**: `"amazonwebservices\.aws-toolkit-vscode"`
- VS Code AWS Toolkit extension
- Example: In extensions.json

---

## Environment Variables

- `AWS_ACCESS_KEY_ID` - AWS access key (for authentication)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_CODEWHISPERER_PROFILE` - CodeWhisperer profile
- `AWS_BUILDER_ID` - AWS Builder ID

## Detection Notes

- Part of AWS Toolkit for VS Code and JetBrains
- Uses AWS credentials or AWS Builder ID
- Now rebranded as Amazon Q Developer
- Includes security scanning features
- Free tier available

---

## Secrets Detection

### AWS Credentials

See AWS patterns for credential detection. CodeWhisperer uses standard AWS authentication.

---

## TIER 3: Configuration Extraction

### Profile Extraction

**Pattern**: `(?:codewhisperer[_-]?profile|AWS_CODEWHISPERER_PROFILE)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- CodeWhisperer profile name
- Extracts: `profile_name`
