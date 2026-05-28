# Backstage CR API v1alpha5 Specification

API Version: `rhdh.redhat.com/v1alpha5`

Source: https://github.com/redhat-developer/rhdh-operator/blob/main/api/v1alpha5/backstage_types.go

## Changes from v1alpha4

- **Added**: `spec.deployment.kind` field (Deployment or StatefulSet)
- **Removed**: `spec.application.replicas` (use deployment.patch)
- **Removed**: `spec.application.image` (use deployment.patch)
- **Removed**: `spec.application.imagePullSecrets` (use deployment.patch)

## Go Struct Definitions

### Core Types

```go
type Backstage struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec              BackstageSpec   `json:"spec,omitempty"`
    Status            BackstageStatus `json:"status,omitempty"`
}

type BackstageSpec struct {
    Application      *Application         `json:"application,omitempty"`
    RawRuntimeConfig *RuntimeConfig       `json:"rawRuntimeConfig,omitempty"`
    Database         *Database            `json:"database,omitempty"`
    Monitoring       Monitoring           `json:"monitoring,omitempty"`
    Deployment       *BackstageDeployment `json:"deployment,omitempty"`
}

type BackstageStatus struct {
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}
```

### BackstageDeployment (UPDATED)

```go
type BackstageDeployment struct {
    Patch *apiextensionsv1.JSON `json:"patch,omitempty"`
    Kind  string                `json:"kind,omitempty"`  // NEW: "Deployment" or "StatefulSet"
}
```

### Condition Constants

```go
type BackstageConditionType string
type BackstageConditionReason string

const (
    BackstageConditionTypeDeployed     BackstageConditionType   = "Deployed"
    BackstageConditionReasonDeployed   BackstageConditionReason = "Deployed"
    BackstageConditionReasonFailed     BackstageConditionReason = "DeployFailed"
    BackstageConditionReasonInProgress BackstageConditionReason = "DeployInProgress"
)
```

### Application (SIMPLIFIED)

```go
type Application struct {
    AppConfig                   *AppConfig  `json:"appConfig,omitempty"`
    DynamicPluginsConfigMapName string      `json:"dynamicPluginsConfigMapName,omitempty"`
    ExtraFiles                  *ExtraFiles `json:"extraFiles,omitempty"`
    ExtraEnvs                   *ExtraEnvs  `json:"extraEnvs,omitempty"`
    Route                       *Route      `json:"route,omitempty"`
    // REMOVED: Replicas, Image, ImagePullSecrets - use Deployment.Patch
}
```

### Monitoring

```go
type Monitoring struct {
    Enabled bool `json:"enabled,omitempty"`
}
```

### AppConfig

```go
type AppConfig struct {
    MountPath  string          `json:"mountPath,omitempty"`
    ConfigMaps []FileObjectRef `json:"configMaps,omitempty"`
}
```

### ExtraFiles

```go
type ExtraFiles struct {
    MountPath  string          `json:"mountPath,omitempty"`
    ConfigMaps []FileObjectRef `json:"configMaps,omitempty"`
    Secrets    []FileObjectRef `json:"secrets,omitempty"`
    Pvcs       []PvcRef        `json:"pvcs,omitempty"`
}
```

### ExtraEnvs

```go
type ExtraEnvs struct {
    ConfigMaps []EnvObjectRef `json:"configMaps,omitempty"`
    Secrets    []EnvObjectRef `json:"secrets,omitempty"`
    Envs       []Env          `json:"envs,omitempty"`
}
```

### Reference Types

```go
type FileObjectRef struct {
    Name       string   `json:"name"`
    Key        string   `json:"key,omitempty"`
    MountPath  string   `json:"mountPath"`
    Containers []string `json:"containers,omitempty"`
}

type EnvObjectRef struct {
    Name       string   `json:"name"`
    Key        string   `json:"key,omitempty"`
    Containers []string `json:"containers,omitempty"`
}

type PvcRef struct {
    Name       string   `json:"name"`
    MountPath  string   `json:"mountPath"`
    Containers []string `json:"containers,omitempty"`
}

type Env struct {
    Name       string   `json:"name"`
    Value      string   `json:"value"`
    Containers []string `json:"containers,omitempty"`
}
```

### Database

```go
type Database struct {
    EnableLocalDb  *bool  `json:"enableLocalDb,omitempty"`
    AuthSecretName string `json:"authSecretName,omitempty"`
}
```

### Route and TLS

```go
type Route struct {
    Enabled   *bool  `json:"enabled,omitempty"`
    Host      string `json:"host,omitempty"`
    Subdomain string `json:"subdomain,omitempty"`
    TLS       *TLS   `json:"tls,omitempty"`
}

type TLS struct {
    Certificate                   string `json:"certificate,omitempty"`
    ExternalCertificateSecretName string `json:"externalCertificateSecretName,omitempty"`
    Key                           string `json:"key,omitempty"`
    CACertificate                 string `json:"caCertificate,omitempty"`
}
```

### RuntimeConfig

```go
type RuntimeConfig struct {
    BackstageConfigName string `json:"backstageConfig,omitempty"`
    LocalDbConfigName   string `json:"localDbConfig,omitempty"`
}
```

## Helper Methods

```go
func (s *BackstageSpec) IsLocalDbEnabled() bool
func (s *BackstageSpec) IsRouteEnabled() bool
func (s *BackstageSpec) IsAuthSecretSpecified() bool
func (s *BackstageSpec) IsMonitoringEnabled() bool
```

## Migration from v1alpha4

Fields moved to `deployment.patch`:

```yaml
# v1alpha4
spec:
  application:
    replicas: 2
    image: quay.io/my-org/rhdh:latest
    imagePullSecrets:
      - my-secret

# v1alpha5
spec:
  deployment:
    patch:
      spec:
        replicas: 2
        template:
          spec:
            containers:
              - name: backstage
                image: quay.io/my-org/rhdh:latest
            imagePullSecrets:
              - name: my-secret
```

## YAML Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `spec.application.appConfig.mountPath` | string | Mount path for app-config files |
| `spec.application.appConfig.configMaps` | []FileObjectRef | ConfigMaps with app-config YAML |
| `spec.application.dynamicPluginsConfigMapName` | string | ConfigMap for dynamic-plugins.yaml |
| `spec.application.extraFiles` | ExtraFiles | Additional files to mount |
| `spec.application.extraEnvs` | ExtraEnvs | Additional environment variables |
| `spec.application.route.enabled` | *bool | Enable OpenShift Route |
| `spec.application.route.host` | string | Route hostname |
| `spec.application.route.tls` | TLS | TLS configuration |
| `spec.database.enableLocalDb` | *bool | Enable local PostgreSQL |
| `spec.database.authSecretName` | string | Database credentials secret |
| `spec.monitoring.enabled` | bool | Enable Prometheus metrics |
| `spec.deployment.kind` | string | **NEW**: "Deployment" or "StatefulSet" |
| `spec.deployment.patch` | JSON | Strategic merge patch |
| `spec.rawRuntimeConfig.backstageConfig` | string | Runtime config ConfigMap |

## Database Secret Format

For external database (`enableLocalDb: false`):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  POSTGRES_HOST: "db.example.com"
  POSTGRES_PORT: "5432"
  POSTGRES_USER: "backstage"
  POSTGRES_PASSWORD: "password"
```
