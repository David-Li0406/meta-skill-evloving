# Microsoft Defender for Cloud

Configure and use Defender for Cloud security posture management.

## Enabling Defender Plans

```bicep
// Enable Defender for specific resource types
resource defenderServers 'Microsoft.Security/pricings@2022-03-01' = {
  name: 'VirtualMachines'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderStorage 'Microsoft.Security/pricings@2022-03-01' = {
  name: 'StorageAccounts'
  properties: {
    pricingTier: 'Standard'
    subPlan: 'DefenderForStorageV2'
  }
}

resource defenderContainers 'Microsoft.Security/pricings@2022-03-01' = {
  name: 'Containers'
  properties: {
    pricingTier: 'Standard'
  }
}

resource defenderKeyVaults 'Microsoft.Security/pricings@2022-03-01' = {
  name: 'KeyVaults'
  properties: {
    pricingTier: 'Standard'
  }
}
```

## Security Contacts

```bicep
resource securityContacts 'Microsoft.Security/securityContacts@2020-01-01-preview' = {
  name: 'default'
  properties: {
    emails: 'security@company.com'
    phone: '+1-555-0100'
    alertNotifications: {
      state: 'On'
      minimalSeverity: 'High'
    }
    notificationsByRole: {
      state: 'On'
      roles: ['Owner', 'Contributor']
    }
  }
}
```

## Auto-Provisioning

```bicep
// Enable automatic agent installation
resource autoProvision 'Microsoft.Security/autoProvisioningSettings@2017-08-01-preview' = {
  name: 'default'
  properties: {
    autoProvision: 'On'
  }
}
```

## Security Policies (Azure Policy)

```bash
# Assign built-in security initiative
az policy assignment create \
  --name "ASC Default" \
  --scope "/subscriptions/SUBSCRIPTION_ID" \
  --policy-set-definition "1f3afdf9-d0c9-4c3d-847f-89da613e70a8"  # Azure Security Benchmark

# Check compliance
az policy state summarize \
  --subscription SUBSCRIPTION_ID
```

## Common Recommendations

| Recommendation | Fix |
|----------------|-----|
| Enable MFA for accounts with owner permissions | Azure AD Conditional Access |
| Storage accounts should use private link | Create private endpoint |
| SQL servers should use customer-managed keys | Configure TDE with CMK |
| Key vaults should have soft delete enabled | Enable soft-delete |
| Subnets should have NSG associated | Create and attach NSG |

## Workflow Automation

```bicep
// Auto-respond to high severity alerts
resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: 'security-alert-response'
  location: location
  properties: {
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      triggers: {
        manual: {
          type: 'Request'
          kind: 'Http'
        }
      }
      actions: {
        Send_email: {
          type: 'ApiConnection'
          inputs: {
            method: 'post'
            path: '/Mail'
            body: {
              To: 'security@company.com'
              Subject: 'High Severity Alert'
              Body: '@triggerBody()'
            }
          }
        }
      }
    }
  }
}

resource automation 'Microsoft.Security/automations@2019-01-01-preview' = {
  name: 'high-severity-alerts'
  location: location
  properties: {
    scopes: [
      {
        scopePath: '/subscriptions/${subscription().subscriptionId}'
      }
    ]
    sources: [
      {
        eventSource: 'Alerts'
        ruleSets: [
          {
            rules: [
              {
                propertyJPath: 'Severity'
                propertyType: 'String'
                expectedValue: 'High'
                operator: 'Equals'
              }
            ]
          }
        ]
      }
    ]
    actions: [
      {
        actionType: 'LogicApp'
        logicAppResourceId: logicApp.id
        uri: listCallbackUrl(logicApp.id, '2019-05-01').value
      }
    ]
  }
}
```

## CLI Commands

```bash
# Check secure score
az security secure-score show --name "ascScore"

# List alerts
az security alert list --subscription SUBSCRIPTION_ID

# List recommendations
az security assessment list --subscription SUBSCRIPTION_ID

# Export to Log Analytics
az security workspace-setting create \
  --name default \
  --target-workspace "/subscriptions/.../workspaces/security-logs"
```

## Best Practices

1. **Enable all relevant Defender plans** - Cost varies, prioritize by risk
2. **Configure security contacts** - Ensure alerts reach the right people
3. **Review Secure Score weekly** - Track improvement over time
4. **Automate responses** - Use Logic Apps for common remediations
5. **Integrate with SIEM** - Export to Sentinel or external SIEM
