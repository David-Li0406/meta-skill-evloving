# containerd

**Category**: cncf
**Description**: Industry-standard container runtime
**Homepage**: https://containerd.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*containerd Go packages*

- `github.com/containerd/containerd` - containerd core
- `github.com/containerd/containerd/api` - API definitions
- `github.com/containerd/containerd/cio` - Container I/O
- `github.com/containerd/cgroups` - cgroups management
- `github.com/containerd/typeurl` - Type URL utilities
- `github.com/containerd/fifo` - FIFO utilities
- `github.com/containerd/continuity` - Filesystem continuity
- `github.com/containerd/go-runc` - runc Go bindings

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate containerd usage*

- `containerd.toml` - containerd configuration
- `config.toml` - containerd config (in /etc/containerd/)
- `cri-containerd.conf` - CRI plugin config

### Configuration Directories
*Known directories that indicate containerd usage*

- `/etc/containerd/` - Configuration directory
- `/var/lib/containerd/` - Data directory
- `/run/containerd/` - Runtime directory

### Code Patterns

**Pattern**: `containerd\.sock|containerd\.io`
- containerd socket and namespace
- Example: `/run/containerd/containerd.sock`

**Pattern**: `ctr\s+(images|containers|tasks|snapshots|namespaces)`
- containerd CLI commands
- Example: `ctr images pull docker.io/library/nginx:latest`

**Pattern**: `\[plugins\."io\.containerd|plugins\.cri`
- containerd plugin configuration
- Example: `[plugins."io.containerd.grpc.v1.cri"]`

**Pattern**: `runtime\s*=\s*["']?io\.containerd\.runc`
- containerd runtime configuration
- Example: `runtime = "io.containerd.runc.v2"`

**Pattern**: `containerd\.New|containerd\.WithDefaultNamespace`
- containerd Go client
- Example: `client, err := containerd.New("/run/containerd/containerd.sock")`

**Pattern**: `crictl|critest`
- CRI tools for containerd
- Example: `crictl ps`

---

## Environment Variables

- `CONTAINERD_ADDRESS` - containerd socket address
- `CONTAINERD_NAMESPACE` - Default namespace
- `CONTAINERD_SNAPSHOTTER` - Snapshotter to use
- `CONTAINERD_RUNTIME` - Runtime to use

## Detection Notes

- Default socket at /run/containerd/containerd.sock
- Used as container runtime for Kubernetes
- Supports OCI images and runtime spec
- CRI plugin enables Kubernetes integration
- Namespaces isolate resources

---

## Secrets Detection

### Credentials

#### Registry Auth
**Pattern**: `\[plugins\."io\.containerd\.grpc\.v1\.cri"\.registry\.configs\."[^"]+"\].*auth`
**Severity**: high
**Description**: Container registry authentication in containerd config
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Snapshotter Extraction

**Pattern**: `snapshotter\s*=\s*["']?([a-z]+)["']?`
- Snapshotter type
- Extracts: `snapshotter`
- Example: `snapshotter = "overlayfs"`

### Runtime Extraction

**Pattern**: `runtime_type\s*=\s*["']?([a-zA-Z0-9._-]+)["']?`
- Container runtime type
- Extracts: `runtime_type`
- Example: `runtime_type = "io.containerd.runc.v2"`
