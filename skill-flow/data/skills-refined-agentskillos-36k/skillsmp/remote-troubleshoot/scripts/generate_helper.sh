#!/bin/bash
# Generate investigation helper script on local machine for upload to remote server

if [ -z "$1" ]; then
    echo "Usage: $0 <helper-type> [args...]"
    echo ""
    echo "Helper types:"
    echo "  service <service-name>      - Service status and log checks"
    echo "  port <port-number>          - Port listening and connectivity"
    echo "  k8s <namespace> <app>      - K8s pods and resources"
    echo "  config <config-path>       - Configuration file inspection"
    echo "  process <name>             - Process status check"
    exit 1
fi

HELPER_TYPE=$1
shift

case "$HELPER_TYPE" in
    service)
        SERVICE=$1
        cat << EOF
#!/bin/bash
# Service investigation helper for $SERVICE

echo "=== Service Status: $SERVICE ==="
systemctl status $SERVICE 2>/dev/null || echo "Service not found with systemctl"
systemctl is-active $SERVICE 2>/dev/null || echo "is-active check failed"

echo -e "\n=== Recent Logs ==="
journalctl -u $SERVICE -n 50 --no-pager 2>/dev/null || echo "Journalctl failed"
tail -n 50 /var/log/$SERVICE*.log 2>/dev/null || echo "Log file not found"

echo -e "\n=== Process ==="
ps aux | grep $SERVICE | grep -v grep
EOF
        ;;
    port)
        PORT=$1
        cat << EOF
#!/bin/bash
# Port investigation for $PORT

echo "=== Port $PORT Status ==="
ss -tlnp 2>/dev/null | grep ":$PORT " || netstat -tlnp 2>/dev/null | grep ":$PORT "
echo "Exit code: \$?"

echo -e "\n=== Socket details ==="
ss -tlnp 2>/dev/null | grep -E "Local Address.*:$PORT"

echo -e "\n=== Listening process ==="
lsof -i :$PORT 2>/dev/null || echo "lsof not available"

echo -e "\n=== Test connection ==="
timeout 3 bash -c "echo > /dev/tcp/127.0.0.1/$PORT" 2>&1 && echo "Port is accessible" || echo "Port cannot be connected"
EOF
        ;;
    k8s)
        NAMESPACE=$1
        APP=$2
        cat << EOF
#!/bin/bash
# K8s investigation for namespace=$NAMESPACE app=$APP

echo "=== Pods in namespace $NAMESPACE with app=$APP ==="
kubectl get pods -n $NAMESPACE -l app=$APP -o wide

echo -e "\n=== Pod Details ==="
POD=\$(kubectl get pods -n $NAMESPACE -l app=$APP -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod \$POD -n $NAMESPACE

echo -e "\n=== Pod Logs ==="
kubectl logs \$POD -n $NAMESPACE --tail=50

echo -e "\n=== Events ==="
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | grep \$POD
EOF
        ;;
    config)
        CONFIG=$1
        cat << EOF
#!/bin/bash
# Configuration inspection for $CONFIG

echo "=== Config File: $CONFIG ==="
ls -la $CONFIG 2>/dev/null || echo "File not found"

echo -e "\n=== File Info ==="
stat $CONFIG 2>/dev/null || echo "Stat failed"

echo -e "\n=== Content (first 50 lines) ==="
head -50 $CONFIG 2>/dev/null

echo -e "\n=== Content (last 20 lines if applicable) ==="
tail -20 $CONFIG 2>/dev/null

echo -e "\n=== File grep for common keywords ==="
grep -n -E "listen|port|host|address|path|enabled" $CONFIG 2>/dev/null | head -20
EOF
        ;;
    process)
        NAME=$1
        cat << EOF
#!/bin/bash
# Process check for $NAME

echo "=== Process Status: $NAME ==="
ps aux | grep $NAME | grep -v grep

echo -e "\n=== Process Count ==="
pgrep -f $NAME | wc -l

echo -e "\n=== Process Details (last matching) ==="
pgrep -f $NAME | tail -1 | xargs -I {} ps -fp {}

echo -e "\n=== Open Files (last matching) ==="
pgrep -f $NAME | tail -1 | xargs -I {} lsof -p {} 2>/dev/null | head -20
EOF
        ;;
    *)
        echo "Unknown helper type: $HELPER_TYPE"
        exit 1
        ;;
esac
