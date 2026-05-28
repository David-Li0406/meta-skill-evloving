# Backstage CR API v1alpha3 Specification

API Version: `rhdh.redhat.com/v1alpha3`

Source: https://github.com/redhat-developer/rhdh-operator/blob/main/api/v1alpha3/backstage_types.go

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
    Application      *Application        `json:"application,omitempty"`
    RawRuntimeConfig *RuntimeConfig      `json:"rawRuntimeConfig,omitempty"`
    Database         *Database           `json:"database,omitempty"`
    Deployment       *BackstageDeployment `json:"deployment,omitempty"`
}

type BackstageStatus struct {
    Conditions []metav1.Condition `json:"conditions,omitempty"`
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

### Application

```go
type Application struct {
    AppConfig                   *AppConfig  `json:"appConfig,omitempty"`
    DynamicPluginsConfigMapName string      `json:"dynamicPluginsConfigMapName,omitempty"`
    ExtraFiles                  *ExtraFiles `json:"extraFiles,omitempty"`
    ExtraEnvs                   *ExtraEnvs  `json:"extraEnvs,omitempty"`
    Replicas                    *int32      `json:"replicas,omitempty"`
    Image                       *string     `json:"image,omitempty"`
    ImagePullSecrets            []string    `json:"imagePullSecrets,omitempty"`
    Route                       *Route      `json:"route,omitempty"`
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

### BackstageDeployment

```go
type BackstageDeployment struct {
    Patch *apiextensionsv1.JSON `json:"patch,omitempty"`
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
func (s *BackstageSpec) IsRouteEnabled() bool      // defaults to true
func (s *BackstageSpec) IsAuthSecretSpecified() bool
```

## YAML Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `spec.application.appConfig.mountPath` | string | Mount path for app-config files |
| `spec.application.appConfig.configMaps` | []FileObjectRef | ConfigMaps with app-config YAML |
| `spec.application.dynamicPluginsConfigMapName` | string | ConfigMap name for dynamic-plugins.yaml |
| `spec.application.extraFiles` | ExtraFiles | Additional files to mount |
| `spec.application.extraEnvs` | ExtraEnvs | Additional environment variables |
| `spec.application.replicas` | *int32 | Number of replicas |
| `spec.application.image` | *string | Custom Backstage image |
| `spec.application.imagePullSecrets` | []string | Image pull secret names |
| `spec.application.route.enabled` | *bool | Enable OpenShift Route |
| `spec.application.route.host` | string | Route hostname |
| `spec.application.route.tls` | TLS | TLS configuration |
| `spec.database.enableLocalDb` | *bool | Enable local PostgreSQL |
| `spec.database.authSecretName` | string | Database credentials secret |
| `spec.deployment.patch` | JSON | Strategic merge patch |
| `spec.rawRuntimeConfig.backstageConfig` | string | Runtime config ConfigMap |
