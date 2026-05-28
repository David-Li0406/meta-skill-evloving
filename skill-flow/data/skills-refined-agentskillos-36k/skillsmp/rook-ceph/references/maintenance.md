# Maintenance Operations

## Health Checks

```bash
# Overall status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status

# Detailed health
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph health detail

# OSD tree (shows node/device layout)
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd tree

# Pool usage
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph df

# PG status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph pg stat
```

## OSD Operations

### List OSDs
```bash
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd ls
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd status
```

### Remove OSD (graceful)
```bash
# Mark out (starts data migration)
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd out <osd-id>

# Wait for data migration
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph -w

# Once HEALTH_OK, purge OSD
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd purge <osd-id> --yes-i-really-mean-it
```

### Replace Failed Disk
1. Remove failed OSD (above)
2. Replace physical disk
3. Update CephCluster storage config
4. Operator auto-provisions new OSD

## Pool Operations

### List Pools
```bash
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd lspools
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd pool ls detail
```

### Pool Stats
```bash
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- rados df
```

## Node Maintenance

### Drain Node (before maintenance)
```bash
# Cordon node
kubectl cordon <node-name>

# Set OSDs on node to noout (prevent rebalancing)
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd set-group noout <node-name>

# Drain workloads
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

### Return Node
```bash
# Uncordon
kubectl uncordon <node-name>

# Unset noout
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd unset-group noout <node-name>
```

## Upgrade Ceph

1. Update `cephVersion.image` in values
2. Helm upgrade
3. Monitor upgrade progress:
```bash
kubectl -n rook-ceph get pods -w
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph versions
```

## Disaster Recovery

### Backup Cluster Config
```bash
kubectl -n rook-ceph get cephcluster -o yaml > cephcluster-backup.yaml
kubectl -n rook-ceph get cephblockpool -o yaml > pools-backup.yaml
kubectl -n rook-ceph get cephfilesystem -o yaml > filesystem-backup.yaml
```

### Export Mon Keyring
```bash
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- \
  ceph auth get mon. -o /tmp/mon.keyring
kubectl -n rook-ceph cp rook-ceph-tools-<pod>:/tmp/mon.keyring ./mon.keyring
```

## Monitoring

### Enable Prometheus
```yaml
# In cluster values
monitoring:
  enabled: true
  createPrometheusRules: true
```

### Dashboard Access
```bash
# Get password
kubectl -n rook-ceph get secret rook-ceph-dashboard-password \
  -o jsonpath="{['data']['password']}" | base64 -d

# Port forward
kubectl -n rook-ceph port-forward svc/rook-ceph-mgr-dashboard 8443:8443
```
