---
name: azure
description: "Azure infrastructure security review process. Use when reviewing RBAC and managed identities, auditing Storage account configurations, securing Azure Functions and App Service, reviewing Bicep/ARM templates or Terraform, or configuring VNet and NSGs. Also use when service principals use secrets, Storage allows public blob access, Azure SQL uses SQL auth instead of Azure AD, or NSG rules allow 0.0.0.0/0. Essential for Key Vault integration, Microsoft Defender, private endpoints, and Azure security scanning."
---

# Azure Skill

## Overview

Azure provides strong security controls, but they must be explicitly configured. This skill guides systematic review of Azure infrastructure for security misconfigurations.

**Core principle:** Use managed identities, not service principal secrets. Azure AD authentication with managed identities eliminates credential management and reduces attack surface.

## The Azure Security Review Process

### Phase 1: Check Identity First

**Identity is the foundation. Start here:**

1. **Review Role Assignments**
   - Scoped to resource group or resource (not subscription)?
   - Using built-in roles (not Owner/Contributor)?
   - No classic administrators?

2. **Check Managed Identities**
   - User-assigned for critical workloads?
   - No service principal secrets?
   - Proper role assignments?

3. **Verify Azure AD Integration**
   - Azure AD only for Azure SQL?
   - No shared key access for Storage?
   - Conditional Access where appropriate?

### Phase 2: Check Network Boundaries

**Then verify network isolation:**

1. **Network Security Groups**
   - No 0.0.0.0/0 ingress (except Application Gateway)?
   - Deny rules for sensitive resources?
   - Flow Logs enabled?

2. **Private Endpoints**
   - PaaS services use private endpoints?
   - No public endpoints for data stores?
   - DNS configured for private resolution?

3. **Access Restrictions**
   - App Service access restrictions?
   - Function App access restrictions?
   - Azure Bastion for VMs?

### Phase 3: Check Data Protection

**Finally, verify data security:**

1. **Encryption**
   - Customer-managed keys for sensitive data?
   - HTTPS only / TLS 1.2+?
   - Key Vault for secrets?

2. **Storage Security**
   - Public blob access disabled?
   - Shared key access disabled?
   - Soft delete enabled?

## Red Flags - STOP and Investigate

### RBAC Red Flags

```bicep
// ❌ CRITICAL: Owner at subscription
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: subscription()
  properties: {
    roleDefinitionId: 'Owner'  // Too broad!
    principalId: principalId
  }
}

// ❌ HIGH: Contributor role (still too broad)
roleDefinitionId: 'Contributor'

// ❌ HIGH: Service principal with secret
// (Should use managed identity)

// ❌ MEDIUM: Assignment at subscription level
scope: subscription()  // Should be resource group or resource
```

### Storage Red Flags

```bicep
// ❌ CRITICAL: Public blob access
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  properties: {
    allowBlobPublicAccess: true  // Public!
  }
}

// ❌ HIGH: Shared key access
allowSharedKeyAccess: true  // Use Azure AD only

// ❌ HIGH: HTTP allowed
supportsHttpsTrafficOnly: false

// ❌ MEDIUM: Old TLS
minimumTlsVersion: 'TLS1_0'  // Use TLS1_2
```

### Network Red Flags

```bicep
// ❌ CRITICAL: Open to internet
resource nsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  properties: {
    securityRules: [
      {
        properties: {
          direction: 'Inbound'
          sourceAddressPrefix: '*'  // From anywhere!
          destinationPortRange: '22'
          access: 'Allow'
        }
      }
    ]
  }
}

// ❌ HIGH: Public SQL
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  properties: {
    publicNetworkAccess: 'Enabled'  // Should be Disabled
  }
}
```

### App Service Red Flags

```bicep
// ❌ HIGH: HTTP allowed
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  properties: {
    httpsOnly: false  // Should be true
  }
}

// ❌ HIGH: FTP enabled
siteConfig: {
  ftpsState: 'AllAllowed'  // Should be Disabled
}

// ❌ HIGH: Secrets in app settings
appSettings: [
  {
    name: 'DB_PASSWORD'
    value: 'actual-password-here'  // Use Key Vault reference!
  }
]
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Owner role is easiest" | Built-in roles exist. Use Storage Blob Data Reader, etc. |
| "Managed identity is complex" | It's simpler than managing secrets. Enable it. |
| "We need public storage" | Use SAS tokens or Azure CDN with auth. |
| "SQL auth is fine" | Azure AD only is more secure. Migrate to it. |
| "Bastion is expensive" | Cheaper than a breach. Use it for VM access. |
| "Key Vault refs are overhead" | Secrets in settings are visible in portal. Use KV. |

## Azure Security Checklist

Before approving Azure infrastructure:

**Identity:**
- [ ] No Owner/Contributor at subscription level
- [ ] Managed identities (not SP secrets)
- [ ] Azure AD only for data services
- [ ] Scoped role assignments

**Network:**
- [ ] No 0.0.0.0/0 in NSG rules
- [ ] Private endpoints for PaaS
- [ ] NSG Flow Logs enabled
- [ ] Azure Bastion for VM access

**Storage:**
- [ ] Public blob access disabled
- [ ] Shared key access disabled
- [ ] HTTPS only, TLS 1.2+
- [ ] Soft delete enabled

**Compute:**
- [ ] Managed identity enabled
- [ ] Secrets from Key Vault
- [ ] Access restrictions configured
- [ ] FTP disabled

## Quick Patterns

### Secure Storage Account

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: { name: 'Standard_GRS' }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
      virtualNetworkRules: [
        { id: subnet.id, action: 'Allow' }
      ]
    }
    encryption: {
      services: {
        blob: { enabled: true, keyType: 'Account' }
      }
      keySource: 'Microsoft.Keyvault'
      keyvaultproperties: {
        keyname: keyVaultKey.name
        keyvaulturi: keyVault.properties.vaultUri
      }
    }
  }
}
```

### Secure Role Assignment

```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentity.id, 'blob-reader')
  scope: storageAccount  // Resource-level, not subscription!
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'  // Storage Blob Data Reader
    )
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
```

### Key Vault Reference

```bicep
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'DatabasePassword'
          value: '@Microsoft.KeyVault(SecretUri=${keyVault.properties.vaultUri}secrets/db-password/)'
        }
      ]
    }
  }
}
```

## Quick Security Scans

```bash
# Azure CLI
az security assessment list
az storage account list --query "[?allowBlobPublicAccess==true]"
az network nsg list --query "[].securityRules[?sourceAddressPrefix=='*']"

# Third-party scanners
checkov -f main.bicep           # Bicep scanning
tfsec .                         # Terraform scanning
az policy assignment list       # Azure Policy compliance

# Microsoft tools
# - Microsoft Defender for Cloud (portal)
# - Azure Advisor (portal)
```

## References

Detailed patterns and examples in `references/`:
- `rbac-patterns.md` - Advanced RBAC and managed identities
- `network-security.md` - VNet and NSG patterns
- `defender.md` - Microsoft Defender configuration
