# CRI-O

**Category**: cncf
**Description**: OCI-based container runtime for Kubernetes
**Homepage**: https://cri-o.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*CRI-O Go packages*

- `github.com/cri-o/cri-o` - CRI-O core
- `github.com/cri-o/ocicni` - OCI CNI plugin

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate CRI-O usage*

- `crio.conf` - CRI-O configuration
- `crio.conf.d/*.conf` - Drop-in configs
- `policy.json` - Image signature policy
- `registries.conf` - Registry configuration

### Configuration Directories
*Known directories that indicate CRI-O usage*

- `/etc/crio/` - Configuration directory
- `/var/lib/containers/` - Container storage
- `/run/crio/` - Runtime directory

### Code Patterns

**Pattern**: `crio|cri-o`
- CRI-O references
- Example: `--container-runtime=cri-o`

**Pattern**: `crio\.sock|cri-o\.sock`
- CRI-O socket
- Example: `/var/run/crio/crio.sock`

**Pattern**: `crictl|crio-status`
- CRI-O tools
- Example: `crictl ps`

**Pattern**: `\[crio\]|\[crio\.runtime\]|\[crio\.image\]|\[crio\.network\]`
- CRI-O config sections
- Example: `[crio.runtime]`

**Pattern**: `runtime_path|conmon_cgroup|seccomp_profile`
- CRI-O config options
- Example: `runtime_path = "/usr/bin/runc"`

**Pattern**: `pause_image|signature_policy`
- CRI-O image settings
- Example: `pause_image = "k8s.gcr.io/pause:3.6"`

**Pattern**: `container-runtime-endpoint.*crio`
- kubelet CRI-O configuration
- Example: `--container-runtime-endpoint=unix:///var/run/crio/crio.sock`

---

## Environment Variables

- `CONTAINER_RUNTIME_ENDPOINT` - CRI socket path
- `CRIO_CONFIG` - Configuration file path
- `CRIO_LOG_LEVEL` - Log level

## Detection Notes

- Designed specifically for Kubernetes CRI
- Lightweight alternative to containerd/Docker
- Supports runc and other OCI runtimes
- Red Hat OpenShift default runtime
- Default socket at /var/run/crio/crio.sock

---

## Secrets Detection

### Credentials

#### Registry Auth
**Pattern**: `\[\[registry\]\].*auth\s*=`
**Severity**: high
**Description**: Container registry authentication in registries.conf
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Runtime Path Extraction

**Pattern**: `runtime_path\s*=\s*['"]?([^\s'"]+)['"]?`
- OCI runtime path
- Extracts: `runtime_path`
- Example: `runtime_path = "/usr/bin/runc"`

### Pause Image Extraction

**Pattern**: `pause_image\s*=\s*['"]?([^\s'"]+)['"]?`
- Pause container image
- Extracts: `pause_image`
- Example: `pause_image = "k8s.gcr.io/pause:3.6"`

### Storage Driver Extraction

**Pattern**: `storage_driver\s*=\s*['"]?([a-z]+)['"]?`
- Container storage driver
- Extracts: `storage_driver`
- Example: `storage_driver = "overlay"`
