# Investigation Patterns

## K8s Troubleshooting Pattern

### Pod Not Starting
```bash
# 1. Check pod status
kubectl get pods -n <namespace>

# 2. Describe pod (shows events, conditions)
kubectl describe pod <pod> -n <namespace>

# 3. Check logs
kubectl logs <pod> -n <namespace> --tail=50

# 4. If image issues, check image pull secrets
kubectl get secret <secret> -n <namespace> -o yaml

# 5. If resource issues, check limits
kubectl describe node <node> | grep -A5 "Allocated resources"
```

### Service Port Not Accessible
```bash
# 1. Check service
kubectl get svc -n <namespace>

# 2. Check endpoints
kubectl get endpoints <service> -n <namespace>

# 3. Check pod selector
kubectl get pod -n <namespace> -l <label-selector>

# 4. Check hostNetwork setting
kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.hostNetwork}'

# 5. Port forward test
kubectl port-forward -n <namespace> pod/<pod> <local-port>:<pod-port>
```

### ConfigMap Mount Issues
```bash
# 1. Check ConfigMap
kubectl get cm <name> -n <namespace>

# 2. Check mount paths in pod
kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.containers[*].volumeMounts}'

# 3. Check volumes
kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.volumes}'

# 4. Verify mount inside pod
kubectl exec <pod> -n <namespace> -- ls -la <mount-path>
```

## Service Pattern

### Service Not Running
```bash
# 1. Check service status
systemctl status <service>

# 2. Check for recent errors
journalctl -u <service> -n 100 --no-pager

# 3. Check logs
tail -100 /var/log/<service>.log

# 4. Check dependencies
systemctl list-dependencies <service>

# 5. Check ports
ss -tlnp | grep <port>
```

### Service Fails to Start
```bash
# 1. Try manual start with error output
systemctl start <service> --verbose

# 2. Check config syntax
/usr/sbin/<service> -t

# 3. Check permissions
ls -la /etc/<service>/
ls -la /var/log/<service>/log

# 4. Check SELinux/AppArmor
getenforce
aa-status
```

## Network Pattern

### Port Not Listening
```bash
# 1. Check port binding
ss -tlnp | grep :<port>
netstat -tlnp | grep :<port>

# 2. Check firewall
iptables -L -n | grep <port>
firewall-cmd --list-ports

# 3. Check process
ps aux | grep <service-name>
lsof -i :<port>

# 4. Check socket state
cat /proc/net/tcp | grep <hex-port>
```

### Connectivity Issues
```bash
# 1. Local test
curl -v http://localhost:<port>
nc -zv localhost <port>

# 2. Remote test
telnet <host> <port>
nc -zv <host> <port>

# 3. Traceroute
traceroute <host>
tracepath <host>

# 4 DNS
nslookup <host>
dig <host>
```

## Configuration Pattern

### Config Modification Detection
```bash
# 1. Find modified files
find /etc/<service>/ -cmin -60

# 2. Compare with backup
diff /etc/<service>/config /backup/config

# 3. Check git status (if using etckeeper)
cd /etc
git status

# 4. Verify config syntax
<service> -t
<service> --configtest
```

### Config File Analysis
```bash
# 1. File info
stat /path/to/config
wc -l /path/to/config

# 2. Key settings
grep -n -E "port|host|address|enabled|listen" /path/to/config

# 3. Comments vs active
grep -v "^\s*#" /path/to/config | grep -v "^$"

# 4. Find referenced files
grep -hE "include|Import|Include" /path/to/config
```
