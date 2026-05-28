# Azure RBAC Security Patterns

## Built-in Roles Reference

### Storage Roles (Use Instead of Contributor)

| Instead of | Use | Scope |
|------------|-----|-------|
| Contributor | Storage Blob Data Reader | Read blobs |
| Contributor | Storage Blob Data Contributor | Read/write blobs |
| Contributor | Storage Queue Data Contributor | Read/write queues |
| Owner | Storage Account Contributor | Manage storage accounts |

### Compute Roles

| Role | Use Case |
|------|----------|
| Virtual Machine Contributor | Manage VMs, not network/storage |
| Virtual Machine User Login | RDP/SSH login only |
| Virtual Machine Administrator Login | Admin login |

### Database Roles

| Role | Use Case |
|------|----------|
| SQL DB Contributor | Manage SQL databases |
| SQL Server Contributor | Manage SQL servers |
| Cosmos DB Account Reader | Read Cosmos DB |
| Cosmos DB Operator | Manage Cosmos DB (not keys) |

### Key Vault Roles

| Role | Use Case |
|------|----------|
| Key Vault Secrets User | Read secrets |
| Key Vault Secrets Officer | Manage secrets |
| Key Vault Certificates Officer | Manage certificates |
| Key Vault Crypto Officer | Manage keys |

## Managed Identity Patterns

### User-Assigned Managed Identity

```bicep
// Create user-assigned identity
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'my-app-identity'
  location: location
}

// Assign to App Service
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: appServiceName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
}

// Grant role
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, managedIdentity.id, 'blob-reader')
  scope: storageAccount
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

### System-Assigned vs User-Assigned

| Aspect | System-Assigned | User-Assigned |
|--------|-----------------|---------------|
| Lifecycle | Tied to resource | Independent |
| Sharing | One resource only | Multiple resources |
| Use Case | Simple scenarios | Shared identity |
| Recommendation | Quick setup | Production workloads |

## Role Assignment Scopes

### Resource-Level (Most Restrictive)

```bicep
// Grant access to specific storage account
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, principalId, roleDefinitionId)
  scope: storageAccount  // Resource level
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

### Resource Group Level

```bicep
// Grant access to all resources in resource group
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, principalId, roleDefinitionId)
  scope: resourceGroup()  // Resource group level
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

### Subscription Level (Avoid)

```bicep
// Only for cross-resource-group access
// Avoid unless necessary
targetScope = 'subscription'

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, principalId, roleDefinitionId)
  scope: subscription()  // Too broad!
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```

## Custom Role Definitions

### Minimal Deployer Role

```bicep
resource customRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(subscription().id, 'minimal-deployer')
  properties: {
    roleName: 'Minimal Deployer'
    description: 'Deploy web apps without admin access'
    type: 'CustomRole'
    assignableScopes: [
      resourceGroup().id
    ]
    permissions: [
      {
        actions: [
          'Microsoft.Web/sites/read',
          'Microsoft.Web/sites/write',
          'Microsoft.Web/sites/restart/action',
          'Microsoft.Web/sites/slots/read',
          'Microsoft.Web/sites/slots/write'
        ]
        notActions: [
          'Microsoft.Web/sites/delete',
          'Microsoft.Web/sites/config/write'
        ]
      }
    ]
  }
}
```

### Read-Only Security Auditor

```bicep
resource securityAuditorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(subscription().id, 'security-auditor')
  properties: {
    roleName: 'Security Auditor'
    description: 'Read security configurations'
    type: 'CustomRole'
    assignableScopes: [
      subscription().id
    ]
    permissions: [
      {
        actions: [
          '*/read',
          'Microsoft.Security/*/read',
          'Microsoft.Authorization/*/read',
          'Microsoft.KeyVault/vaults/read',
          'Microsoft.Network/networkSecurityGroups/read'
        ]
        notActions: []
      }
    ]
  }
}
```

## Conditional Access Integration

### Require MFA for Role Assignment

```json
{
  "conditions": {
    "signInRisk": {
      "value": "high"
    }
  },
  "grantControls": {
    "builtInControls": [
      "mfa"
    ]
  }
}
```

### Require Compliant Device

```json
{
  "grantControls": {
    "builtInControls": [
      "compliantDevice",
      "domainJoinedDevice"
    ],
    "operator": "OR"
  }
}
```

## Privileged Identity Management (PIM)

### Just-In-Time Access

```bicep
// PIM requires Azure AD Premium P2
// Configure via Azure Portal or Microsoft Graph API

// Example: Grant eligible assignment
// User must activate role when needed
resource pimRoleAssignment 'Microsoft.Authorization/roleEligibilityScheduleRequests@2022-04-01-preview' = {
  name: guid(principalId, roleDefinitionId, 'eligible')
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: principalId
    requestType: 'AdminAssign'
    scheduleInfo: {
      startDateTime: utcNow()
      expiration: {
        type: 'AfterDuration'
        duration: 'P90D'  // 90 days
      }
    }
  }
}
```

## Deny Assignments

### Block Specific Actions

```bicep
resource denyAssignment 'Microsoft.Authorization/denyAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, 'deny-delete')
  properties: {
    denyAssignmentName: 'Deny Delete Operations'
    description: 'Prevent accidental deletion'
    permissions: [
      {
        actions: [
          '*/delete'
        ]
      }
    ]
    principals: [
      {
        id: developersGroupId
        type: 'Group'
      }
    ]
    excludePrincipals: [
      {
        id: adminsGroupId
        type: 'Group'
      }
    ]
    scope: resourceGroup().id
  }
}
```

## Audit Queries

```bash
# List role assignments at subscription level
az role assignment list --scope /subscriptions/SUB_ID --query "[?scope=='/subscriptions/SUB_ID']"

# Find Owner/Contributor assignments
az role assignment list --all --query "[?roleDefinitionName=='Owner' || roleDefinitionName=='Contributor']"

# Find assignments for specific principal
az role assignment list --assignee PRINCIPAL_ID

# List custom roles
az role definition list --custom-role-only true

# Check for classic administrators
az role assignment list --include-classic-administrators

# Find unused service principals
az ad sp list --filter "servicePrincipalType eq 'Application'" \
  --query "[?signInAudience=='AzureADMyOrg']"
```

## Role Assignment Best Practices

| Practice | Implementation |
|----------|----------------|
| Principle of least privilege | Use specific roles, not Owner/Contributor |
| Scope appropriately | Resource > Resource Group > Subscription |
| Use groups | Assign roles to groups, not individuals |
| Use managed identities | Avoid service principal secrets |
| Enable PIM | Just-in-time access for privileged roles |
| Regular review | Use Access Reviews in Azure AD |
| Audit changes | Monitor role assignment changes |
