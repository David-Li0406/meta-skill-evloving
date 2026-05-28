---
name: Backstage Custom Resource
description: This skill should be used when the user asks to "create Backstage CR", "create RHDH custom resource", "configure rhdh-operator", "create Backstage manifest", "modify Backstage CR", "configure RHDH deployment", "add dynamic plugins to CR", "configure Backstage database", "set up Backstage route", "configure app-config for RHDH", "create rhdh.redhat.com/v1alpha Backstage", or mentions creating or modifying a Backstage Custom Resource for the rhdh-operator.
---

## Purpose

Create and modify Backstage Custom Resources (CR) for the rhdh-operator. The rhdh-operator manages Red Hat Developer Hub (RHDH) deployments on Kubernetes/OpenShift using these CRs.

## API Versions

Ask the user which version they need if not specified:

| API Version | Status | Key Difference |
|-------------|--------|----------------|
| `rhdh.redhat.com/v1alpha3` | Legacy | Base configuration |
| `rhdh.redhat.com/v1alpha4` | Current | Adds `monitoring` field |
| `rhdh.redhat.com/v1alpha5` | Latest | Adds `deployment.kind`, removes `replicas/image` from application |

Consult `references/v1alpha3-spec.md`, `references/v1alpha4-spec.md`, or `references/v1alpha5-spec.md` for complete Go struct definitions and field documentation.

## Workflow

1. **Determine API version** - Ask user or default to v1alpha5
2. **Identify requirements** - Database (local/external), Route, plugins, monitoring
3. **Consult reference** - Read the appropriate version spec from `references/`
4. **Generate CR** - Create valid YAML based on spec
5. **Validate** - Ensure referenced ConfigMaps/Secrets exist

## Minimal CR

```yaml
apiVersion: rhdh.redhat.com/v1alpha5
kind: Backstage
metadata:
  name: my-rhdh
  namespace: rhdh
spec:
  application: {}
```

Creates RHDH with local PostgreSQL, Route enabled, single replica.

## Key Configuration Areas

### Application
- `appConfig.configMaps` - App-config YAML files
- `dynamicPluginsConfigMapName` - Dynamic plugins ConfigMap
- `extraEnvs` - Environment variables from ConfigMaps/Secrets
- `extraFiles` - Files from ConfigMaps/Secrets/PVCs
- `route` - OpenShift Route with TLS

### Database
- `enableLocalDb: true` - Operator-managed PostgreSQL (default)
- `enableLocalDb: false` + `authSecretName` - External database

### Monitoring (v1alpha4+)
- `monitoring.enabled: true` - Prometheus metrics

### Deployment
- `deployment.kind` - Deployment or StatefulSet (v1alpha5)
- `deployment.patch` - Strategic merge patch for workload

## Reference Files

Consult these for complete field definitions:

- **`references/v1alpha3-spec.md`** - v1alpha3 Go structs and YAML mapping
- **`references/v1alpha4-spec.md`** - v1alpha4 with Monitoring
- **`references/v1alpha5-spec.md`** - v1alpha5 with Deployment kind

## Example Files

- **`examples/backstage-cr.yaml`** - Common configuration patterns

## External Resources

- [rhdh-operator Repository](https://github.com/redhat-developer/rhdh-operator)
- [RHDH Documentation](https://docs.redhat.com/en/documentation/red_hat_developer_hub)
