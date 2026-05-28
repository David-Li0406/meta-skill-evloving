---
name: k9s-ui
description: k9s terminal UI for Kubernetes cluster management. Use when navigating clusters interactively, viewing logs in real-time, managing resources through terminal UI, or when user mentions k9s, terminal kubernetes, or interactive cluster management. Covers keyboard shortcuts, navigation, plugins, and configuration.
---

# k9s Terminal UI

k9s provides a terminal-based UI for Kubernetes cluster management with real-time updates and keyboard-driven navigation.

## Launch Options

```bash
k9s                                    # Default kubeconfig
k9s --kubeconfig /path/to/config       # Specific kubeconfig
k9s --context <context-name>           # Specific context
k9s -n <namespace>                     # Start in namespace
k9s --readonly                         # Read-only mode (no modifications)
k9s --headless                         # No splash screen
k9s -c <resource>                      # Start with resource view (e.g., k9s -c pods)
k9s info                               # Show config/log locations
```

## Navigation Commands (`:` prefix)

### Resource Views

| Command | Resource |
|---------|----------|
| `:pod` / `:po` | Pods |
| `:deploy` / `:dp` | Deployments |
| `:svc` | Services |
| `:ns` | Namespaces |
| `:node` / `:no` | Nodes |
| `:rs` | ReplicaSets |
| `:ds` | DaemonSets |
| `:sts` | StatefulSets |
| `:cm` | ConfigMaps |
| `:secret` / `:sec` | Secrets |
| `:pvc` | PersistentVolumeClaims |
| `:pv` | PersistentVolumes |
| `:ing` | Ingresses |
| `:cj` | CronJobs |
| `:job` | Jobs |
| `:hpa` | HorizontalPodAutoscalers |
| `:ep` | Endpoints |
| `:sa` | ServiceAccounts |
| `:ctx` | Contexts |
| `:event` / `:ev` | Events |

### Special Commands

| Command | Action |
|---------|--------|
| `:aliases` | Show all resource aliases |
| `:xray <resource>` | Tree view of resource dependencies |
| `:pulse` | Cluster health pulse view |
| `:popeye` | Run cluster linter (if installed) |
| `:dir <path>` | Browse saved files |
| `:q` / `:quit` | Exit k9s |

## Global Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `?` | Help / Show all shortcuts |
| `Esc` | Back / Cancel / Exit mode |
| `Ctrl+a` | Show all resources in namespace |
| `Ctrl+e` | Toggle header |
| `Ctrl+w` | Toggle wide columns |
| `Ctrl+s` | Save resource YAML to file |
| `/` | Filter mode (regex search) |
| `0-9` | Quick namespace switch (favorites) |

## Resource-Specific Actions

### Pods

| Key | Action |
|-----|--------|
| `l` | View logs |
| `p` | View previous container logs |
| `s` | Shell into container |
| `a` | Attach to container |
| `d` | Describe |
| `y` | View YAML |
| `e` | Edit |
| `Ctrl+d` | Delete |
| `Ctrl+k` | Kill (force delete) |
| `f` | Port forward |
| `Shift+f` | Port forward menu |

### Deployments

| Key | Action |
|-----|--------|
| `s` | Scale replicas |
| `r` | Restart (rollout restart) |
| `d` | Describe |
| `y` | View YAML |
| `e` | Edit |
| `Ctrl+l` | Rollback |

### General Resources

| Key | Action |
|-----|--------|
| `Enter` | Select / View details |
| `d` | Describe |
| `y` | View YAML |
| `e` | Edit (opens $EDITOR) |
| `Ctrl+d` | Delete (with confirmation) |
| `Ctrl+k` | Kill (no confirmation) |

## Sorting

| Key | Sort By |
|-----|---------|
| `Shift+c` | CPU |
| `Shift+m` | Memory |
| `Shift+s` | Status |
| `Shift+p` | Namespace |
| `Shift+n` | Name |
| `Shift+o` | Node |
| `Shift+i` | IP Address |
| `Shift+a` | Age |

## Filtering & Search

```
/                    # Enter filter mode
/<term>              # Filter by term (regex)
/-f <term>           # Fuzzy search
/!<term>             # Inverse filter (exclude)
/-l app=nginx        # Filter by label
Esc                  # Clear filter
```

## Namespace Operations

| Key/Command | Action |
|-------------|--------|
| `:ns` | List namespaces |
| `u` | Mark as favorite (adds `+`) |
| `0-9` | Quick switch to favorite |
| `Enter` | Switch to namespace |

Favorites appear in header for quick access.

## Logs View

Within pod logs (`l`):

| Key | Action |
|-----|--------|
| `0` | Tail all containers |
| `1-9` | Tail specific container |
| `w` | Toggle wrap |
| `t` | Toggle timestamps |
| `s` | Toggle auto-scroll |
| `/` | Search in logs |
| `Ctrl+s` | Save logs to file |
| `m` | Mark current position |
| `Ctrl+b` | Page up |
| `Ctrl+f` | Page down |

## Port Forwarding

After selecting a pod and pressing `Shift+f`:

1. Select container/port
2. Enter local port
3. Port forward starts in background
4. View active forwards: `:pf`

## Configuration

### Config Location
```
~/.config/k9s/config.yaml     # Main config (Linux)
~/Library/Application Support/k9s/config.yaml  # macOS
```

### Key Settings

```yaml
k9s:
  refreshRate: 2              # Refresh interval (seconds)
  maxConnRetry: 5
  readOnly: false             # Disable modifications
  ui:
    enableMouse: false
    headless: false           # Hide header
    logoless: false           # Hide logo
    crumbsless: false         # Hide breadcrumbs
  logger:
    tail: 1000                # Log lines to keep
    buffer: 5000
    sinceSeconds: -1          # -1 = all logs
```

### Custom Views

`~/.config/k9s/views.yaml`:

```yaml
k9s:
  views:
    v1/pods:
      sortColumn: AGE:desc
      columns:
        - AGE
        - NAMESPACE
        - NAME
        - STATUS
        - RESTARTS
        - CPU
        - MEM
        - IP
        - NODE
```

### Skins/Themes

`~/.config/k9s/skins/<name>.yaml` - Custom color schemes

Set in config: `skin: <name>`

## Plugins

Location: `~/.config/k9s/plugins.yaml`

### Example Plugin

```yaml
plugins:
  stern:
    shortCut: Shift+L
    description: "Multi-pod logs with stern"
    scopes:
      - pods
    command: stern
    background: false
    args:
      - --context
      - $CONTEXT
      - --namespace
      - $NAMESPACE
      - $FILTER
```

Available variables: `$NAMESPACE`, `$NAME`, `$CONTEXT`, `$CLUSTER`, `$USER`, `$COL-<column>`

## Workflow Examples

### Debug Failing Deployment

1. `:deploy` → find deployment
2. `Enter` to see pods
3. Select failing pod → `d` describe (check events)
4. `l` for logs
5. `p` for previous logs (if crashed)
6. `s` to shell in for live debugging

### Monitor Rollout

1. `:deploy` → select deployment
2. `Enter` to see ReplicaSets
3. Watch old RS scale down, new RS scale up
4. Check pod status in new RS

### Quick Cluster Health

1. `:pulse` for overview
2. `:node` → check node status
3. `:event` → recent cluster events
4. `Shift+c` / `Shift+m` to sort by resource usage

### Investigate Memory Issues

1. `:pod` → `Shift+m` (sort by memory)
2. Identify high consumers
3. `d` describe for limits/requests
4. `l` logs for memory-related errors

## Tips

- **Speed**: Learn `:po`, `:dp`, `:svc` shortcuts
- **Favorites**: Mark frequently-used namespaces with `u`
- **Save often**: `Ctrl+s` saves current view to `/tmp/k9s-screens-<user>/`
- **Mouse**: Enable in config if preferred
- **Context switching**: `:ctx` to quickly switch clusters
- **Wide view**: `Ctrl+w` shows more columns (node, IP, etc.)
- **Xray**: `:xray deploy` shows deployment→RS→pod tree
