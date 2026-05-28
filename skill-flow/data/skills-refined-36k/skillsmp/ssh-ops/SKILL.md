---
name: ssh-ops
description: SSH operations for remote server management, tunneling, and proxy-based connections. Use when connecting to remote servers, running remote commands, setting up SSH tunnels, port forwarding, managing jump hosts/bastions, or executing kubectl/k9s on remote clusters. Triggers on SSH, remote, tunnel, bastion, jump host, port forward, or remote kubernetes access.
---

# SSH Operations

## Connection Patterns

### Direct Connection

```bash
# Basic connection
ssh user@host

# With specific key
ssh -i ~/.ssh/id_rsa user@host

# With specific port
ssh -p 2222 user@host

# Execute single command
ssh user@host "command"

# Execute multiple commands
ssh user@host << 'EOF'
cd /app
ls -la
cat config.yaml
EOF
```

### Through Jump Host / Bastion

```bash
# ProxyJump (OpenSSH 7.3+) - preferred
ssh -J jumpuser@bastion user@target

# Multiple jumps
ssh -J jump1@bastion1,jump2@bastion2 user@target

# Legacy ProxyCommand
ssh -o ProxyCommand="ssh -W %h:%p jumpuser@bastion" user@target

# Execute command through jump
ssh -J jumpuser@bastion user@target "kubectl get pods"
```

### SSH Config for Persistent Setup

```bash
# ~/.ssh/config
Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/bastion_key
    
Host target
    HostName 10.0.1.50
    User admin
    ProxyJump bastion
    IdentityFile ~/.ssh/target_key

Host k8s-*
    User ubuntu
    ProxyJump bastion
    IdentityFile ~/.ssh/k8s_key

Host k8s-prod
    HostName 10.0.1.100

Host k8s-staging
    HostName 10.0.2.100
```

Then simply: `ssh target` or `ssh k8s-prod "kubectl get pods"`

## Port Forwarding / Tunneling

### Local Port Forward (access remote service locally)

```bash
# Forward local:8080 → remote:80
ssh -L 8080:localhost:80 user@host

# Forward to service behind remote host
ssh -L 8080:internal-service:80 user@bastion

# Kubernetes API access through tunnel
ssh -L 6443:kubernetes.default:443 user@bastion
# Then: kubectl --server=https://localhost:6443 --insecure-skip-tls-verify get pods

# Database access
ssh -L 5432:db.internal:5432 user@bastion
# Then: psql -h localhost -p 5432 -U dbuser mydb

# Multiple forwards
ssh -L 8080:web:80 -L 5432:db:5432 -L 6379:redis:6379 user@bastion
```

### Remote Port Forward (expose local service remotely)

```bash
# Expose local:3000 on remote:8080
ssh -R 8080:localhost:3000 user@host

# Expose to all interfaces on remote (requires GatewayPorts yes)
ssh -R 0.0.0.0:8080:localhost:3000 user@host
```

### Dynamic SOCKS Proxy

```bash
# Create SOCKS5 proxy on local:1080
ssh -D 1080 user@bastion

# Use with curl
curl --socks5 localhost:1080 http://internal-service/api

# Use with kubectl (via proxychains or similar)
HTTPS_PROXY=socks5://localhost:1080 kubectl get pods
```

### Tunnel in Background

```bash
# Background tunnel with connection keep-alive
ssh -f -N -L 8080:service:80 user@host

# With autossh for auto-reconnect (install: brew install autossh)
autossh -M 0 -f -N -L 8080:service:80 user@host \
    -o "ServerAliveInterval 30" \
    -o "ServerAliveCountMax 3"

# Kill background tunnel
pkill -f "ssh.*-L 8080"

# Or find and kill specific tunnel
ps aux | grep "ssh.*-L" | grep -v grep
kill <pid>
```

## Remote Kubernetes Access

### Through SSH Tunnel

```bash
# Setup: Tunnel to k8s API
ssh -L 6443:kubernetes.default.svc:443 user@bastion -N &
TUNNEL_PID=$!

# Configure kubectl for tunnel
kubectl config set-cluster tunnel-cluster \
    --server=https://localhost:6443 \
    --insecure-skip-tls-verify=true

kubectl config set-context tunnel-context \
    --cluster=tunnel-cluster \
    --user=admin

kubectl config use-context tunnel-context

# Use kubectl normally
kubectl get pods -A

# Cleanup
kill $TUNNEL_PID
```

### Execute kubectl Remotely

```bash
# Single command
ssh user@k8s-master "kubectl get pods -n production"

# With context
ssh user@k8s-master "kubectl --context=prod get pods"

# Watch (needs pseudo-terminal)
ssh -t user@k8s-master "kubectl get pods -w"

# Logs
ssh user@k8s-master "kubectl logs -l app=myapp --tail=100"

# Multiple commands
ssh user@k8s-master << 'EOF'
kubectl get pods -n production
kubectl get events -n production --sort-by='.lastTimestamp' | tail -20
kubectl top pods -n production
EOF
```

### Interactive k9s Remotely

```bash
# Run k9s interactively (requires -t for TTY)
ssh -t user@k8s-master "k9s"

# In specific namespace
ssh -t user@k8s-master "k9s -n production"

# Read-only mode
ssh -t user@k8s-master "k9s --readonly"

# With specific context
ssh -t user@k8s-master "k9s --context production"
```

## Remote Script Execution

### Run Local Script Remotely

```bash
# Execute local script on remote
ssh user@host 'bash -s' < local-script.sh

# With arguments
ssh user@host 'bash -s' < local-script.sh arg1 arg2

# Inline script
ssh user@host << 'SCRIPT'
#!/bin/bash
set -euo pipefail
echo "Running on $(hostname)"
kubectl get pods -n production
SCRIPT
```

### Deploy and Execute

```bash
# Copy and run
scp deploy.sh user@host:/tmp/
ssh user@host "chmod +x /tmp/deploy.sh && /tmp/deploy.sh"

# Or one-liner with heredoc
ssh user@host << 'EOF'
cat > /tmp/check.sh << 'INNER'
#!/bin/bash
kubectl get pods -A | grep -v Running
kubectl get events -A --field-selector type=Warning | tail -20
INNER
chmod +x /tmp/check.sh
/tmp/check.sh
EOF
```

## File Transfer

### SCP

```bash
# Copy to remote
scp file.yaml user@host:/path/

# Copy from remote
scp user@host:/path/file.yaml ./

# Through jump host
scp -J jumpuser@bastion file.yaml user@target:/path/

# Recursive directory
scp -r ./manifests user@host:/deploy/

# With specific key
scp -i ~/.ssh/mykey file.yaml user@host:/path/
```

### Rsync over SSH

```bash
# Sync directory
rsync -avz -e ssh ./local/ user@host:/remote/

# Through jump host
rsync -avz -e "ssh -J jumpuser@bastion" ./local/ user@target:/remote/

# Dry run first
rsync -avzn -e ssh ./local/ user@host:/remote/

# Delete files on remote not in local
rsync -avz --delete -e ssh ./local/ user@host:/remote/
```

## Connection Management

### Keep Connection Alive

```bash
# In command
ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 user@host

# In ~/.ssh/config (global)
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
```

### Connection Multiplexing (reuse connections)

```bash
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# Create socket directory
mkdir -p ~/.ssh/sockets
```

First connection creates socket, subsequent connections reuse it (faster).

### Check Connection

```bash
# Test SSH connectivity
ssh -o ConnectTimeout=5 -o BatchMode=yes user@host echo "OK" 2>/dev/null && echo "Connected" || echo "Failed"

# Verbose connection debugging
ssh -vvv user@host

# Test through bastion
ssh -J jumpuser@bastion -o ConnectTimeout=10 user@target echo "OK"
```

## Automation Scripts

### Tunnel Manager

```bash
#!/usr/bin/env bash
# tunnel.sh - Manage SSH tunnels

ACTION="${1:-status}"
TUNNEL_NAME="${2:-default}"

BASTION="user@bastion.example.com"
PIDFILE="/tmp/ssh-tunnel-${TUNNEL_NAME}.pid"

case "$ACTION" in
    start)
        if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            echo "Tunnel already running (PID: $(cat "$PIDFILE"))"
            exit 0
        fi
        
        case "$TUNNEL_NAME" in
            k8s)
                ssh -f -N -L 6443:kubernetes:443 "$BASTION" \
                    -o ServerAliveInterval=30 \
                    -o ExitOnForwardFailure=yes
                ;;
            db)
                ssh -f -N -L 5432:postgres.internal:5432 "$BASTION" \
                    -o ServerAliveInterval=30 \
                    -o ExitOnForwardFailure=yes
                ;;
            *)
                echo "Unknown tunnel: $TUNNEL_NAME"
                exit 1
                ;;
        esac
        
        pgrep -f "ssh.*-L.*$TUNNEL_NAME" > "$PIDFILE"
        echo "Tunnel $TUNNEL_NAME started (PID: $(cat "$PIDFILE"))"
        ;;
        
    stop)
        if [[ -f "$PIDFILE" ]]; then
            kill "$(cat "$PIDFILE")" 2>/dev/null
            rm "$PIDFILE"
            echo "Tunnel $TUNNEL_NAME stopped"
        else
            pkill -f "ssh.*-L.*$TUNNEL_NAME"
            echo "Tunnel $TUNNEL_NAME stopped (by pattern)"
        fi
        ;;
        
    status)
        if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            echo "Tunnel $TUNNEL_NAME: running (PID: $(cat "$PIDFILE"))"
        else
            echo "Tunnel $TUNNEL_NAME: not running"
        fi
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status} [tunnel-name]"
        echo "Tunnels: k8s, db"
        ;;
esac
```

### Remote Health Check

```bash
#!/usr/bin/env bash
# remote-k8s-check.sh - Check k8s cluster health via SSH

HOST="${1:?Usage: $0 <ssh-host> [namespace]}"
NS="${2:-default}"

echo "=== Checking $HOST ($NS namespace) ==="

ssh "$HOST" << EOF
echo "--- Pod Status ---"
kubectl get pods -n $NS -o wide

echo ""
echo "--- Non-Running Pods ---"
kubectl get pods -n $NS | grep -v Running | grep -v Completed | grep -v NAME

echo ""
echo "--- Recent Events ---"
kubectl get events -n $NS --sort-by='.lastTimestamp' | tail -15

echo ""
echo "--- Resource Usage ---"
kubectl top pods -n $NS 2>/dev/null || echo "Metrics unavailable"
EOF
```

### Batch Remote Execution

```bash
#!/usr/bin/env bash
# run-on-hosts.sh - Run command on multiple hosts

HOSTS=("k8s-prod" "k8s-staging" "k8s-dev")
CMD="${1:?Usage: $0 'command'}"

for host in "${HOSTS[@]}"; do
    echo "=== $host ==="
    ssh -o ConnectTimeout=10 "$host" "$CMD" 2>&1 || echo "FAILED: $host"
    echo ""
done
```

## Security Best Practices

### Key Management

```bash
# Generate ed25519 key (preferred)
ssh-keygen -t ed25519 -C "description" -f ~/.ssh/mykey

# Copy public key to server
ssh-copy-id -i ~/.ssh/mykey.pub user@host

# Restrict key permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_*
chmod 644 ~/.ssh/*.pub
chmod 600 ~/.ssh/config
```

### Agent Forwarding (careful!)

```bash
# Enable agent forwarding (only to trusted hosts)
ssh -A user@bastion

# Then on bastion, can SSH to other hosts using local keys
ssh target-server

# Safer: ProxyJump instead of agent forwarding
ssh -J bastion target  # Keys never leave your machine
```

### Restrict Commands per Key

In remote `~/.ssh/authorized_keys`:

```
command="kubectl get pods",no-port-forwarding,no-X11-forwarding ssh-ed25519 AAAA... readonly-key
```

## Troubleshooting

### Connection Issues

```bash
# Verbose output
ssh -vvv user@host

# Check key being offered
ssh -v user@host 2>&1 | grep "Offering"

# Test specific key
ssh -i ~/.ssh/specific_key -v user@host

# Check server allows key auth
ssh -o PreferredAuthentications=publickey user@host
```

### Tunnel Issues

```bash
# Check if tunnel port is listening
lsof -i :8080
netstat -an | grep 8080

# Test tunnel connectivity
nc -zv localhost 8080

# Debug tunnel
ssh -v -L 8080:target:80 user@bastion
```

### Permission Denied

Common causes:
1. Wrong key permissions: `chmod 600 ~/.ssh/id_*`
2. Wrong .ssh dir permissions: `chmod 700 ~/.ssh`
3. Key not in agent: `ssh-add ~/.ssh/mykey`
4. Server doesn't have public key: `ssh-copy-id`
5. SELinux/firewall blocking
