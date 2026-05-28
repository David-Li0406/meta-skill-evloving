# Crossplane

**Category**: cncf
**Description**: Cloud native control planes for infrastructure management
**Homepage**: https://crossplane.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Crossplane Go packages*

- `github.com/crossplane/crossplane` - Crossplane core
- `github.com/crossplane/crossplane-runtime` - Runtime library
- `github.com/crossplane/provider-aws` - AWS provider
- `github.com/crossplane/provider-azure` - Azure provider
- `github.com/crossplane/provider-gcp` - GCP provider
- `github.com/crossplane/provider-kubernetes` - Kubernetes provider
- `github.com/crossplane/provider-helm` - Helm provider
- `github.com/upbound/provider-aws` - Upbound AWS provider
- `github.com/upbound/provider-azure` - Upbound Azure provider
- `github.com/upbound/provider-gcp` - Upbound GCP provider

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Crossplane usage*

- `crossplane.yaml` - Crossplane package manifest
- `composition.yaml` - Composition definition
- `definition.yaml` - CompositeResourceDefinition
- `provider.yaml` - Provider configuration

### Code Patterns

**Pattern**: `crossplane\.io/|pkg\.crossplane\.io/`
- Crossplane API groups
- Example: `apiVersion: pkg.crossplane.io/v1`

**Pattern**: `kind:\s*(Provider|Configuration|ProviderConfig|Composition|CompositeResourceDefinition)`
- Crossplane CRD kinds
- Example: `kind: Provider`

**Pattern**: `kind:\s*(XR[A-Z]|Composite[A-Z])`
- Composite resource kinds
- Example: `kind: XRDatabase`

**Pattern**: `apiVersion:\s*[a-z]+\.upbound\.io/v[0-9]+|apiVersion:\s*[a-z]+\.aws\.crossplane\.io/v[0-9]+`
- Crossplane provider API versions
- Example: `apiVersion: ec2.aws.upbound.io/v1beta1`

**Pattern**: `forProvider:|providerConfigRef:|connectionDetailsSecretRef:`
- Crossplane spec fields
- Example: `forProvider:\n  region: us-east-1`

**Pattern**: `crossplane\.io/external-name|crossplane\.io/composition-resource-name`
- Crossplane annotations
- Example: `crossplane.io/external-name: my-bucket`

**Pattern**: `compositeTypeRef:|resources:|patchSets:`
- Composition spec fields
- Example: `compositeTypeRef:\n  apiVersion: example.org/v1alpha1`

**Pattern**: `upbound|crossplane-system`
- Crossplane namespaces and Upbound references
- Example: `namespace: crossplane-system`

**Pattern**: `kubectl\s+crossplane|up\s+xpkg|crank`
- Crossplane CLI tools
- Example: `kubectl crossplane build`

---

## Environment Variables

- `CROSSPLANE_NAMESPACE` - Crossplane installation namespace
- `UPBOUND_CONTEXT` - Upbound Cloud context
- `UP_PROFILE` - Upbound CLI profile

## Detection Notes

- Providers manage external cloud resources
- Compositions define infrastructure abstractions
- CompositeResourceDefinitions (XRDs) define APIs
- Claims are namespaced composite resources
- Often used for platform engineering

---

## Secrets Detection

### Credentials

#### AWS Provider Credentials
**Pattern**: `source:\s*Secret\s*\n.*secretRef:\s*\n\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: AWS credentials secret for Crossplane provider
**Multiline**: true

#### Provider Config Secret
**Pattern**: `credentials:\s*\n\s*source:\s*Secret`
**Severity**: high
**Description**: Provider credential configuration
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Provider Name Extraction

**Pattern**: `spec:\s*\n\s*package:\s*['"]?([a-zA-Z0-9./_:-]+)['"]?`
- Provider package reference
- Extracts: `provider_package`
- Example: `package: xpkg.upbound.io/upbound/provider-aws:v0.47.0`
**Multiline**: true

### Composition Name Extraction

**Pattern**: `compositionRef:\s*\n\s*name:\s*['"]?([a-zA-Z0-9-]+)['"]?`
- Referenced composition name
- Extracts: `composition_name`
- Example: `compositionRef:\n  name: xpostgresql.aws.example.org`
**Multiline**: true

### Resource Group Extraction

**Pattern**: `group:\s*['"]?([a-zA-Z0-9.-]+)['"]?`
- XRD group
- Extracts: `api_group`
- Example: `group: example.org`
