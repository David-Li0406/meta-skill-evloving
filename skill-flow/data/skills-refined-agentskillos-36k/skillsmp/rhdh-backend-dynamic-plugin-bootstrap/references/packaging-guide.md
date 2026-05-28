# Dynamic Plugin Packaging Guide

This reference covers all packaging formats for RHDH dynamic plugins.

## Packaging Formats Overview

| Format | Recommended | Use Case |
|--------|-------------|----------|
| OCI Image | Yes | Production deployments on OpenShift/Kubernetes |
| tgz Archive | Sometimes | Simple deployments, development |
| npm Package | Rarely | Private registry distribution |
| Directory | Dev only | Local development and testing |

## OCI Image (Recommended)

OCI container images are the recommended format for production deployments.

### Prerequisites

- `podman` or `docker` installed
- Access to a container registry (quay.io, Docker Hub, etc.)
- Exported dynamic plugin (`dist-dynamic/` directory)

### Creating the Image

Run from the plugin source directory (not `dist-dynamic`):

```bash
npx @red-hat-developer-hub/cli@latest plugin package \
  --tag quay.io/<namespace>/<plugin-name>:v0.1.0
```

### Specifying Container Tool

```bash
# Use Docker instead of Podman
npx @red-hat-developer-hub/cli@latest plugin package \
  --container-tool docker \
  --tag quay.io/<namespace>/<plugin-name>:v0.1.0
```

Available options: `podman` (default), `docker`, `buildah`

### Pushing to Registry

```bash
# Podman
podman push quay.io/<namespace>/<plugin-name>:v0.1.0

# Docker
docker push quay.io/<namespace>/<plugin-name>:v0.1.0
```

### Using in RHDH

```yaml
# dynamic-plugins.yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:v0.1.0!<plugin-id>-backend-dynamic
    disabled: false
```

### Image Digest for Integrity

Use SHA256 digest instead of tag for reproducibility:

```yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>@sha256:28036abec4dffc714394e4ee433f16a59493db8017795049c831be41c02eb5dc!<plugin-id>-backend-dynamic
    disabled: false
```

### Version Inheritance

For included configurations, use `{{inherit}}` to inherit version:

```yaml
# dynamic-plugins.yaml
includes:
  - dynamic-plugins.default.yaml
plugins:
  - package: oci://quay.io/<namespace>/<plugin-name>:{{inherit}}!<plugin-id>-backend-dynamic
    disabled: false
    pluginConfig:
      customSetting: value
```

### Private Registries

Set `REGISTRY_AUTH_FILE` environment variable:

```bash
export REGISTRY_AUTH_FILE=~/.config/containers/auth.json
# or
export REGISTRY_AUTH_FILE=~/.docker/config.json
```

### Multi-Plugin Images

Package multiple plugins in one image:

```bash
# Export both plugins first
cd plugins/frontend-plugin && npx @red-hat-developer-hub/cli@latest plugin export
cd ../backend-plugin && npx @red-hat-developer-hub/cli@latest plugin export

# Package together
cd ../..
npx @red-hat-developer-hub/cli@latest plugin package \
  --tag quay.io/<namespace>/my-plugins:v0.1.0
```

Reference individual plugins:

```yaml
plugins:
  - package: oci://quay.io/<namespace>/my-plugins:v0.1.0!frontend-plugin
    disabled: false
  - package: oci://quay.io/<namespace>/my-plugins:v0.1.0!backend-plugin-dynamic
    disabled: false
```

## tgz Archive

### Creating the Archive

```bash
cd dist-dynamic
npm pack
```

Get integrity hash:

```bash
npm pack --json | jq -r '.[0].integrity'
# Output: sha512-9WlbgEdadJNeQxdn1973r5E4kNFvnT9GjLD627GWgrhCaxjCmxqdNW08cj+Bf47mwAtZMt1Ttyo+ZhDRDj9PoA==
```

### Hosting Options

#### HTTP Server

Host on any web server accessible by RHDH:

```yaml
plugins:
  - package: https://example.com/plugins/my-plugin-1.0.0.tgz
    integrity: sha512-9WlbgEdadJNeQxdn1973r5E4kNFvnT9GjLD627GWgrhCaxjCmxqdNW08cj+Bf47mwAtZMt1Ttyo+ZhDRDj9PoA==
    disabled: false
```

#### OpenShift httpd

Use httpd builder on OpenShift:

```bash
# Pack plugins
npm pack --pack-destination ~/plugins/

# Create httpd service
oc project rhdh
oc new-build httpd --name=plugin-registry --binary
oc start-build plugin-registry --from-dir=~/plugins/ --wait
oc new-app --image-stream=plugin-registry
```

Configure RHDH:

```yaml
plugins:
  - package: http://plugin-registry:8080/my-plugin-1.0.0.tgz
    integrity: sha512-...
    disabled: false
```

## npm Package

### Publishing

```bash
cd dist-dynamic
npm publish --registry https://your-private-registry.com
```

Or configure in package.json:

```json
{
  "publishConfig": {
    "registry": "https://your-private-registry.com"
  }
}
```

### Using in RHDH

```yaml
plugins:
  - package: '@my-org/my-plugin-dynamic@1.0.0'
    integrity: sha512-...
    disabled: false
```

### Custom Registry Configuration

Create `.npmrc` secret for OpenShift:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dynamic-plugins-npmrc
type: Opaque
stringData:
  .npmrc: |
    registry=https://your-registry.com
    //your-registry.com:_authToken=<auth-token>
```

For Helm chart, name it `{{ .Release.Name }}-dynamic-plugins-npmrc`.

### Getting Integrity Hash

```bash
npm view --registry https://your-registry.com \
  @my-org/my-plugin-dynamic@1.0.0 dist.integrity
```

## Local Directory (Development Only)

### Setup

```bash
# Copy dist-dynamic to RHDH's plugin root
cp -r dist-dynamic /path/to/rhdh/dynamic-plugins-root/my-plugin-dynamic
```

### Configuration

```yaml
# app-config.yaml
dynamicPlugins:
  rootDirectory: dynamic-plugins-root
```

```yaml
# dynamic-plugins.yaml
plugins:
  - package: ./dynamic-plugins-root/my-plugin-dynamic
    disabled: false
```

### Pre-installed Plugins

RHDH container includes pre-installed plugins. Enable them:

```yaml
plugins:
  - package: ./dynamic-plugins/dist/backstage-plugin-catalog-backend-module-github-dynamic
    disabled: false
```

## Integrity Hashes

### Why Integrity Matters

Integrity hashes ensure the downloaded package hasn't been tampered with.

### Required For

- tgz archives: Always required
- npm packages: Always required
- OCI images: Use digest instead of tag

### Generating Hash

```bash
# For tgz
npm pack --json | jq -r '.[0].integrity'

# For npm package
npm view @package/name@version dist.integrity
```

### Hash Format

SHA-512 base64 encoded:
```
sha512-9WlbgEdadJNeQxdn1973r5E4kNFvnT9GjLD627GWgrhCaxjCmxqdNW08cj+Bf47mwAtZMt1Ttyo+ZhDRDj9PoA==
```

## Best Practices

### 1. Use OCI for Production

OCI images provide:
- Version tagging
- Digest-based integrity
- Standard container tooling
- Easy updates

### 2. Use Semantic Versioning

```
quay.io/namespace/plugin:v1.0.0
quay.io/namespace/plugin:v1.0.1
quay.io/namespace/plugin:v1.1.0
```

### 3. Include Metadata

The CLI adds annotations to OCI images:
- `com.redhat.rhdh.plugins` - Plugin metadata
- `io.backstage.dynamic-packages` - Package paths

### 4. Test Before Publishing

```bash
# Test locally first
cp -r dist-dynamic /path/to/rhdh/dynamic-plugins-root/my-plugin

# Verify it loads
yarn workspace backend start

# Then publish
podman push quay.io/namespace/plugin:v1.0.0
```

### 5. Document Configuration

Include example configuration with published plugins:

```yaml
# Example dynamic-plugins.yaml entry
plugins:
  - package: oci://quay.io/namespace/my-plugin:v1.0.0!my-plugin-dynamic
    disabled: false
    pluginConfig:
      myPlugin:
        apiUrl: https://api.example.com
```
