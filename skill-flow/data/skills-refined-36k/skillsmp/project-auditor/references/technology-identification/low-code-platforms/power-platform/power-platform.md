# Microsoft Power Platform

**Category**: low-code-platforms
**Description**: Microsoft's suite of low-code tools (Power Apps, Power Automate, Power BI)
**Homepage**: https://powerplatform.microsoft.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Power Platform packages*

- `@microsoft/powerapps-portals-cli` - Power Apps portals CLI
- `@microsoft/generator-pcf` - Power Apps Component Framework generator
- `pcf-scripts` - PCF build scripts
- `powerapps-component-framework` - PCF library
- `@microsoft/power-platform-cli` - Power Platform CLI

#### NUGET
*Power Platform .NET packages*

- `Microsoft.PowerPlatform.Dataverse.Client` - Dataverse client
- `Microsoft.CrmSdk.CoreAssemblies` - Dynamics CRM SDK
- `Microsoft.Xrm.Tooling.Connector` - XRM tooling
- `Microsoft.PowerApps.Checker.Client` - Power Apps checker

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Power Platform usage*

- `*.msapp` - Power Apps application file
- `CanvasManifest.json` - Power Apps manifest
- `pcfconfig.json` - PCF configuration
- `solution.xml` - Solution configuration
- `.pcfproj` - PCF project file
- `pac.exe` - Power Platform CLI

### Configuration Directories
*Known directories that indicate Power Platform usage*

- `CanvasApps/` - Canvas app directory
- `Entities/` - Dataverse entities
- `Workflows/` - Power Automate flows
- `PluginAssemblies/` - Custom plugins

### Code Patterns

**Pattern**: `powerapps\.com|dynamics\.com|crm\.dynamics\.com`
- Power Platform URLs
- Example: `https://org.crm.dynamics.com`

**Pattern**: `POWERPLATFORM_|DATAVERSE_|CRM_`
- Power Platform environment variables
- Example: `POWERPLATFORM_CLIENT_ID`

**Pattern**: `Microsoft\.PowerPlatform|Microsoft\.Xrm`
- Power Platform namespace imports
- Example: `using Microsoft.Xrm.Sdk;`

**Pattern**: `/api/data/v[0-9.]+/`
- Dataverse Web API pattern
- Example: `/api/data/v9.2/accounts`

---

## Environment Variables

- `POWERPLATFORM_CLIENT_ID` - Azure AD app client ID
- `POWERPLATFORM_CLIENT_SECRET` - Azure AD app secret
- `POWERPLATFORM_TENANT_ID` - Azure AD tenant ID
- `DATAVERSE_URL` - Dataverse environment URL
- `CRM_CONNECTION_STRING` - CRM connection string
- `POWERPLATFORM_SPN_ID` - Service principal ID
- `POWERPLATFORM_SPN_SECRET` - Service principal secret

## Detection Notes

- Power Platform uses Azure AD for authentication
- Dataverse (formerly CDS) is the underlying data platform
- Look for .msapp files for canvas apps
- PCF components use TypeScript/React
- Solution.xml indicates Dataverse solutions
- API endpoints use /api/data/v9.x/ format

---

## Secrets Detection

### API Keys and Secrets

#### Power Platform Client Secret
**Pattern**: `(?:POWERPLATFORM|DATAVERSE|CRM).*(?:SECRET|secret)\s*[=:]\s*['"]?([a-zA-Z0-9~._-]{34,})['"]?`
**Severity**: critical
**Description**: Azure AD client secret for Power Platform
**Example**: `POWERPLATFORM_CLIENT_SECRET=abc~123...`

#### CRM Connection String
**Pattern**: `(?:CRM_CONNECTION_STRING|connectionstring).*Url=([^;]+).*ClientSecret=([^;]+)`
**Severity**: critical
**Description**: Full CRM connection string with credentials
**Example**: `Url=https://org.crm.dynamics.com;ClientId=...;ClientSecret=...`

### Validation

#### API Documentation
- **Dataverse Web API**: https://docs.microsoft.com/en-us/powerapps/developer/data-platform/webapi/overview
- **Power Platform CLI**: https://docs.microsoft.com/en-us/powerapps/developer/data-platform/powerapps-cli
