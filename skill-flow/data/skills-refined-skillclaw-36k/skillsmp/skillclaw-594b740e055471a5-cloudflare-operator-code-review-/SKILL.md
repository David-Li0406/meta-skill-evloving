---
name: cloudflare-operator-code-review-and-e2e-testing
description: Use this skill when you need to perform code reviews and end-to-end testing for the Cloudflare Operator project, ensuring code quality and functionality against the Cloudflare API.
---

# Skill body

## Code Review Guidelines

### Overview

Review code changes according to the Cloudflare Operator project standards. This skill checks for common issues and ensures compliance with project specifications.

### Quick Review Commands

```bash
# Run all checks
make fmt vet test lint

# Check a specific file
go vet ./path/to/file.go
```

### Critical Checks (P0 - Must Fix)

1. **Status Update Without Retry**
   - **Incorrect:**
     ```go
     obj.Status.State = "active"
     r.Status().Update(ctx, obj)
     ```
   - **Correct:**
     ```go
     controller.UpdateStatusWithConflictRetry(ctx, r.Client, obj, func() {
         obj.Status.State = "active"
     })
     ```

2. **Finalizer Not Using Retry**
   - **Incorrect:**
     ```go
     controllerutil.RemoveFinalizer(obj, FinalizerName)
     r.Update(ctx, obj)
     ```
   - **Correct:**
     ```go
     controller.UpdateWithConflictRetry(ctx, r.Client, obj, func() {
         controllerutil.RemoveFinalizer(obj, FinalizerName)
     })
     ```

3. **Sensitive Data in Events**
   - **Incorrect:**
     ```go
     r.Recorder.Event(obj, "Warning", "Failed", err.Error())
     ```
   - **Correct:**
     ```go
     r.Recorder.Event(obj, "Warning", "Failed", cf.SanitizeErrorMessage(err))
     ```

4. **Not Checking NotFound on Deletion**
   - **Incorrect:**
     ```go
     if err := r.cfAPI.Delete(id); err != nil {
         return err
     }
     ```
   - **Correct:**
     ```go
     if err := r.cfAPI.Delete(id); err != nil {
         if !cf.IsNotFoundError(err) {
             return err
         }
         // Already deleted
     }
     ```

5. **Cluster Scoped Resource Using Empty Namespace**
   - **Incorrect:**
     ```go
     cf.NewAPIClientFromDetails(ctx, r.Client, "", obj.Spec.Cloudflare)
     ```
   - **Correct:**
     ```go
     cf.NewAPIClientFromDetails(ctx, r.Client, controller.OperatorNamespace, obj.Spec.Cloudflare)
     ```

### Important Checks (P1 - Should Fix)

6. **Condition Management**
   - **Incorrect:**
     ```go
     obj.Status.Conditions = append(obj.Status.Conditions, condition)
     ```
   - **Correct:**
     ```go
     meta.SetStatusCondition(&obj.Status.Conditions, metav1.Condition{
         Type:               "Ready",
         Status:             metav1.ConditionTrue,
         Reason:             "Reconciled",
         ObservedGeneration: obj.Generation,
     })
     ```

7. **Missing Dependency Resource Watch**
   - Ensure to add Watch for resources that reference others (e.g., Tunnel, VirtualNetwork).

8. **Error Aggregation on Deletion**
   - Aggregate errors when deleting multiple items.

## End-to-End Testing Guidelines

### Overview

This skill guides the Cloudflare Operator in performing end-to-end tests against the real Cloudflare API.

### Prerequisites

- **Required Credentials:**
  - Cloudflare API Token or Global API Key
  - Cloudflare Account ID
  - Cloudflare Domain (for DNS-related tests)

- **Required Permissions:**
  | Feature | Permission | Scope |
  |---------|------------|-------|
  | Tunnel  | `Account:Cloudflare Tunnel:Edit` | Account |
  | DNS     | `Zone:DNS:Edit` | Zone |
  | Access   | `Account:Access: Apps and Policies:Edit` | Account |
  | Zero Trust | `Account:Zero Trust:Edit` | Account |

### Setup

1. **Deploy Operator**
   ```bash
   # Install CRD
   kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.crds.yaml

   # Install Operator
   kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.yaml

   # Verify
   kubectl get pods -n cloudflare-operator-system
   ```

2. **Create Credential Secret**
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: cloudflare-credentials
     namespace: cloudflare-operator-system
   type: Opaque
   stringData:
     CLOUDFLARE_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
   ```

3. **Create CloudflareCredentials Resource**
   ```yaml
   apiVersion: networking.cloudflare-operator.io/v1alpha2
   kind: CloudflareCredentials
   metadata:
     name: default-credentials
   spec:
     accountId: "${CLOUDFLARE_ACCOUNT_ID}"
     secretRef:
       name: cloudflare-credentials
       namespace: cloudflare-operator-system
   ```

### Testing Sequence

Follow the dependency order to test CRDs:

1. **Infrastructure**
   - CloudflareCredentials
   - ClusterTunnel / Tunnel
   - VirtualNetwork

2. **Network**
   - NetworkRoute
   - TunnelBinding
   - DNSRecord
   - PrivateService

3. **Access Control**
   - AccessGroup
   - AccessIdentityProvider
   - AccessServiceToken
   - AccessApplication

4. **Zero Trust**
   - GatewayConfiguration
   - GatewayList
   - GatewayRule
   - DevicePostureRule
   - DeviceSettingsPolicy