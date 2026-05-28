# KubeVirt

**Category**: cncf
**Description**: Run virtual machines on Kubernetes
**Homepage**: https://kubevirt.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*KubeVirt Go packages*

- `kubevirt.io/kubevirt` - KubeVirt core
- `kubevirt.io/client-go` - Go client
- `kubevirt.io/api` - API types
- `kubevirt.io/containerized-data-importer` - CDI

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate KubeVirt usage*

- `kubevirt.yaml` - KubeVirt deployment
- `vm.yaml` - VirtualMachine definition
- `vmi.yaml` - VirtualMachineInstance

### Code Patterns

**Pattern**: `kubevirt\.io/|cdi\.kubevirt\.io/`
- KubeVirt API groups
- Example: `kubevirt.io/v1`

**Pattern**: `kind:\s*(VirtualMachine|VirtualMachineInstance|VirtualMachineInstanceMigration|DataVolume)`
- KubeVirt CRD kinds
- Example: `kind: VirtualMachine`

**Pattern**: `apiVersion:\s*kubevirt\.io/v[0-9]+`
- KubeVirt API version
- Example: `apiVersion: kubevirt.io/v1`

**Pattern**: `domain:|devices:|volumes:|interfaces:`
- VM spec sections
- Example: `domain:\n  cpu:\n    cores: 2`

**Pattern**: `cloudInitNoCloud:|cloudInitConfigDrive:`
- Cloud-init configuration
- Example: `cloudInitNoCloud:\n  userData:`

**Pattern**: `virtctl|virt-launcher|virt-handler`
- KubeVirt components
- Example: `virtctl start my-vm`

**Pattern**: `containerDisk:|dataVolume:|persistentVolumeClaim:`
- VM volume sources
- Example: `containerDisk:\n  image: quay.io/kubevirt/cirros`

**Pattern**: `running:\s*(true|false)|runStrategy:`
- VM run state
- Example: `running: true`

---

## Environment Variables

- `KUBEVIRT_NAMESPACE` - KubeVirt namespace
- `KUBEVIRT_CLIENT_GO_KUBECONFIG` - Kubeconfig path

## Detection Notes

- Runs VMs as Kubernetes pods
- CDI for disk image management
- Live migration support
- virtctl CLI for VM operations
- Supports cloud-init for configuration

---

## Secrets Detection

### Credentials

#### Cloud-Init User Password
**Pattern**: `password:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Cloud-init user password

#### SSH Public Key
**Pattern**: `ssh_authorized_keys:`
**Severity**: medium
**Description**: SSH public keys in cloud-init (not secret but sensitive)

---

## TIER 3: Configuration Extraction

### CPU Cores Extraction

**Pattern**: `cores:\s*([0-9]+)`
- VM CPU cores
- Extracts: `cpu_cores`
- Example: `cores: 4`

### Memory Extraction

**Pattern**: `memory:\s*['"]?([0-9]+[GMK]i?)['"]?`
- VM memory allocation
- Extracts: `memory`
- Example: `memory: 4Gi`

### Disk Image Extraction

**Pattern**: `image:\s*['"]?([a-zA-Z0-9._\-/:]+)['"]?`
- Container disk image
- Extracts: `disk_image`
- Example: `image: quay.io/kubevirt/fedora-cloud`
