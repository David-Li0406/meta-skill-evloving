# Helm Commands Reference

## Release Management

### Install
```bash
helm install [RELEASE] [CHART] [flags]

# Examples
helm install myapp ./mychart                    # Local chart
helm install myapp bitnami/wordpress            # From repo
helm install myapp ./mychart -f values.yaml     # With values file
helm install myapp ./mychart --set key=value    # With inline values
helm install myapp ./mychart --namespace prod --create-namespace
```

Flags:
- `-f, --values` - Values file(s)
- `--set` - Inline values (key=value)
- `--set-string` - Force string type
- `--set-file` - Set from file content
- `--namespace, -n` - Target namespace
- `--create-namespace` - Create namespace if missing
- `--wait` - Wait for resources ready
- `--timeout` - Wait timeout (default 5m)
- `--dry-run` - Simulate install
- `--debug` - Show debug output

### Upgrade
```bash
helm upgrade [RELEASE] [CHART] [flags]

# Examples
helm upgrade myapp ./mychart
helm upgrade myapp ./mychart -f values.yaml
helm upgrade --install myapp ./mychart     # Install if not exists
helm upgrade myapp ./mychart --reuse-values  # Keep existing values
helm upgrade myapp ./mychart --reset-values  # Use chart defaults
```

### Rollback
```bash
helm rollback [RELEASE] [REVISION] [flags]

# Examples
helm rollback myapp 1          # Rollback to revision 1
helm rollback myapp 0          # Rollback to previous
```

### Uninstall
```bash
helm uninstall [RELEASE] [flags]

helm uninstall myapp
helm uninstall myapp --keep-history    # Allow rollback after uninstall
```

### List & Status
```bash
helm list                      # List releases in current namespace
helm list -A                   # All namespaces
helm list --all                # Include failed/pending
helm status [RELEASE]          # Detailed release status
helm history [RELEASE]         # Revision history
```

## Chart Development

### Create & Package
```bash
helm create [NAME]             # Scaffold new chart
helm package [CHART_PATH]      # Create .tgz archive
helm lint [CHART_PATH]         # Check for issues
```

### Template Rendering
```bash
helm template [NAME] [CHART] [flags]

# Examples
helm template myapp ./mychart                   # Render to stdout
helm template myapp ./mychart -f values.yaml    # With values
helm template myapp ./mychart --debug           # Include debug info
helm template myapp ./mychart -s templates/deployment.yaml  # Single template
```

### Debugging
```bash
helm install myapp ./mychart --dry-run --debug   # Test without installing
helm get values myapp                            # Show deployed values
helm get manifest myapp                          # Show deployed manifests
helm get all myapp                               # All release info
```

## Repository Management

```bash
helm repo add [NAME] [URL]     # Add repository
helm repo update               # Update repo indexes
helm repo list                 # List configured repos
helm repo remove [NAME]        # Remove repository

helm search repo [KEYWORD]     # Search in repos
helm search hub [KEYWORD]      # Search Artifact Hub
```

## Chart Information

```bash
helm show chart [CHART]        # Show Chart.yaml
helm show values [CHART]       # Show default values
helm show readme [CHART]       # Show README
helm show all [CHART]          # All info
helm pull [CHART]              # Download chart archive
helm pull [CHART] --untar      # Download and extract
```

## Dependencies

```bash
helm dependency update [CHART]  # Download dependencies
helm dependency build [CHART]   # Rebuild charts/ directory
helm dependency list [CHART]    # List dependencies
```
