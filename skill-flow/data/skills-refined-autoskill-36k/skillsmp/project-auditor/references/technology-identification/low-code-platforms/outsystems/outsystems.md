# OutSystems

**Category**: low-code-platforms
**Description**: Enterprise low-code platform for application development
**Homepage**: https://outsystems.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*OutSystems-related packages*

- `outsystems-ui` - OutSystems UI framework
- `@nicegui/outsystems` - OutSystems integration

#### NUGET
*OutSystems .NET packages*

- `OutSystems.RuntimePublic` - OutSystems runtime
- `OutSystems.ExternalLibraries.SDK` - External libraries SDK

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate OutSystems usage*

- `*.oml` - OutSystems module files
- `*.oap` - OutSystems application package
- `outsystems.json` - OutSystems configuration

### Code Patterns

**Pattern**: `outsystems\.com|outsystemscloud\.com`
- OutSystems platform URLs
- Example: `https://myenv.outsystemscloud.com`

**Pattern**: `OUTSYSTEMS_`
- OutSystems environment variables
- Example: `OUTSYSTEMS_API_KEY`

**Pattern**: `OutSystems\.|OS_Runtime`
- OutSystems code references
- Example: `OutSystems.RuntimePublic`

**Pattern**: `/ServiceCenter/|/LifeTimeSDK/`
- OutSystems service URLs
- Example: `https://env.outsystems.com/ServiceCenter/`

---

## Environment Variables

- `OUTSYSTEMS_API_KEY` - LifeTime API key
- `OUTSYSTEMS_ENVIRONMENT_KEY` - Environment key
- `OUTSYSTEMS_PLATFORM_SERVER` - Platform server URL
- `OUTSYSTEMS_DEPLOYMENT_ZONE` - Deployment zone

## Detection Notes

- OutSystems uses proprietary .oml and .oap file formats
- LifeTime is the deployment management tool
- ServiceCenter is the administration console
- Look for outsystemscloud.com for cloud deployments
- Integration Services use REST/SOAP APIs

---

## Secrets Detection

### API Keys

#### OutSystems LifeTime API Key
**Pattern**: `(?:outsystems|OUTSYSTEMS).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{32,})['"]?`
**Severity**: high
**Description**: OutSystems LifeTime API key
**Example**: `OUTSYSTEMS_API_KEY=abc123...`

#### OutSystems Service Account Token
**Pattern**: `(?:outsystems|OUTSYSTEMS).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]{64,})['"]?`
**Severity**: high
**Description**: Service account authentication token

### Validation

#### API Documentation
- **LifeTime API**: https://success.outsystems.com/Documentation/11/Reference/OutSystems_APIs/LifeTime_API_v2
