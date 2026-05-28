# Falco

**Category**: cncf
**Description**: Cloud-native runtime security
**Homepage**: https://falco.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Falco Go packages*

- `github.com/falcosecurity/falco` - Falco core
- `github.com/falcosecurity/client-go` - Falco Go client
- `github.com/falcosecurity/falcoctl` - Falco CLI tool
- `github.com/falcosecurity/falcosidekick` - Falco output router

#### PYPI
*Falco Python packages*

- `falco` - Falco Python client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Falco usage*

- `falco.yaml` - Falco configuration
- `falco_rules.yaml` - Falco rules
- `falco_rules.local.yaml` - Local rules
- `rules.d/*.yaml` - Additional rules

### Code Patterns

**Pattern**: `falco\.org|falcosecurity`
- Falco references
- Example: `github.com/falcosecurity/falco`

**Pattern**: `- rule:|condition:|output:|priority:`
- Falco rule structure
- Example: `- rule: Terminal shell in container`

**Pattern**: `(spawned_process|container\.id|fd\.name|proc\.name|evt\.type)`
- Falco rule fields
- Example: `condition: container.id != host and proc.name = bash`

**Pattern**: `WARNING|ERROR|INFORMATIONAL|NOTICE|DEBUG|CRITICAL|ALERT|EMERGENCY`
- Falco priority levels
- Example: `priority: WARNING`

**Pattern**: `falco\s+(--list|--help|--rules-file|-r)`
- Falco CLI usage
- Example: `falco -r /etc/falco/falco_rules.yaml`

**Pattern**: `falcoctl|falcosidekick`
- Falco ecosystem tools
- Example: `falcoctl driver install`

**Pattern**: `syscall|k8s_audit|cloudtrail|okta`
- Falco event sources
- Example: `source: syscall`

**Pattern**: `/dev/falco|falco\.sock`
- Falco device and socket
- Example: `/dev/falco0`

---

## Environment Variables

- `FALCO_HOSTNAME` - Hostname for outputs
- `FALCO_BPF_PROBE` - BPF probe path
- `FALCO_GRPC_ENABLED` - Enable gRPC output
- `FALCO_K8S_API_URL` - Kubernetes API URL
- `FALCOSIDEKICK_URL` - Falcosidekick webhook URL

## Detection Notes

- Uses eBPF/kernel module for syscall monitoring
- Rules written in Falco rules language
- Integrates with Kubernetes audit logs
- Falcosidekick routes alerts to various outputs
- Driver can be kernel module or eBPF

---

## Secrets Detection

### Credentials

#### Slack Webhook
**Pattern**: `slack_webhook_url:\s*['"]?(https://hooks\.slack\.com[^\s'"]+)['"]?`
**Severity**: high
**Description**: Slack webhook URL for Falco alerts

#### Falco gRPC Certificate
**Pattern**: `grpc_cert:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: gRPC TLS certificate path

---

## TIER 3: Configuration Extraction

### Rules File Extraction

**Pattern**: `rules_file:\s*\n(?:\s*-\s*['"]?([^\s'"]+)['"]?\n?)+`
- Falco rules file paths
- Extracts: `rules_files`
- Example: `rules_file:\n  - /etc/falco/falco_rules.yaml`
**Multiline**: true

### Output Format Extraction

**Pattern**: `json_output:\s*(true|false)`
- JSON output enabled
- Extracts: `json_output`
- Example: `json_output: true`

### Priority Extraction

**Pattern**: `priority:\s*['"]?([A-Z]+)['"]?`
- Rule priority level
- Extracts: `priority`
- Example: `priority: WARNING`
