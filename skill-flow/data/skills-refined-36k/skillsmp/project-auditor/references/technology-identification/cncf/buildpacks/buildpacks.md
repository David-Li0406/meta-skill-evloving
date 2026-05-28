# Cloud Native Buildpacks

**Category**: cncf
**Description**: Transform source code into OCI images
**Homepage**: https://buildpacks.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Buildpacks Go packages*

- `github.com/buildpacks/pack` - Pack CLI
- `github.com/buildpacks/lifecycle` - Lifecycle
- `github.com/buildpacks/libcnb` - Go library for buildpacks

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Buildpacks usage*

- `project.toml` - Buildpack project descriptor
- `buildpack.toml` - Buildpack descriptor
- `package.toml` - Buildpack package descriptor
- `builder.toml` - Builder descriptor

### Code Patterns

**Pattern**: `buildpacks\.io|buildpack\s+`
- Buildpacks references
- Example: `gcr.io/buildpacks/builder:v1`

**Pattern**: `\[project\]|\[build\]|\[\[build\.env\]\]`
- project.toml sections
- Example: `[project]\nname = "my-app"`

**Pattern**: `pack\s+(build|builder|buildpack|config|inspect)`
- Pack CLI commands
- Example: `pack build my-app --builder gcr.io/buildpacks/builder:v1`

**Pattern**: `CNB_|BP_|BPL_`
- Buildpack environment variables
- Example: `CNB_PLATFORM_API`

**Pattern**: `lifecycle:|detect:|build:|launch:`
- Buildpack lifecycle phases
- Example: `[build]\n  [[build.env]]`

**Pattern**: `paketo|heroku/buildpacks|gcr\.io/buildpacks`
- Popular buildpack registries
- Example: `paketo-buildpacks/java`

**Pattern**: `kpack|image\.kpack\.io`
- kpack for K8s buildpacks
- Example: `kind: Image`

**Pattern**: `--builder|--buildpack|--path`
- Pack build flags
- Example: `--builder paketobuildpacks/builder:base`

---

## Environment Variables

- `CNB_PLATFORM_API` - Platform API version
- `CNB_STACK_ID` - Stack identifier
- `BP_JVM_VERSION` - JVM version (Paketo)
- `BP_NODE_VERSION` - Node.js version (Paketo)
- `BPL_JVM_HEAD_ROOM` - JVM head room
- `CNB_USER_ID` - User ID
- `CNB_GROUP_ID` - Group ID

## Detection Notes

- Transforms source to OCI images
- Builder contains buildpacks and stack
- Stack defines build and run images
- Lifecycle handles phases
- kpack for Kubernetes-native builds

---

## Secrets Detection

### Credentials

#### Registry Credentials
**Pattern**: `CNB_REGISTRY_AUTH\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Registry authentication for buildpacks

---

## TIER 3: Configuration Extraction

### Project Name Extraction

**Pattern**: `name\s*=\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Project name in project.toml
- Extracts: `project_name`
- Example: `name = "my-app"`

### Builder Extraction

**Pattern**: `--builder\s+['"]?([a-zA-Z0-9._\-/:]+)['"]?`
- Builder image
- Extracts: `builder`
- Example: `--builder paketobuildpacks/builder:base`

### Buildpack ID Extraction

**Pattern**: `id\s*=\s*['"]?([a-zA-Z0-9._/-]+)['"]?`
- Buildpack identifier
- Extracts: `buildpack_id`
- Example: `id = "paketo-buildpacks/java"`
