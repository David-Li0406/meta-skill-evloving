# Multi-Node Cluster Values

Save as `cluster-values.yaml`:

```yaml
# Production cluster configuration
cephClusterSpec:
  cephVersion:
    image: quay.io/ceph/ceph:v19.2.0
    allowUnsupported: false

  dataDirHostPath: /var/lib/rook

  mon:
    count: 3
    allowMultiplePerNode: false

  mgr:
    count: 2
    allowMultiplePerNode: false
    modules:
      - name: rook
        enabled: true
      - name: pg_autoscaler
        enabled: true

  dashboard:
    enabled: true
    ssl: true

  crashCollector:
    disable: false

  # Node selector for Ceph nodes
  placement:
    all:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: ceph-node
                  operator: In
                  values:
                    - "true"

  storage:
    useAllNodes: false
    useAllDevices: false
    nodes:
      - name: "node1"
        devices:
          - name: "sdb"
          - name: "sdc"
      - name: "node2"
        devices:
          - name: "sdb"
          - name: "sdc"
      - name: "node3"
        devices:
          - name: "sdb"
          - name: "sdc"

  resources:
    mgr:
      limits:
        memory: "1Gi"
      requests:
        cpu: "500m"
        memory: "512Mi"
    mon:
      limits:
        memory: "2Gi"
      requests:
        cpu: "1000m"
        memory: "1Gi"
    osd:
      limits:
        memory: "4Gi"
      requests:
        cpu: "1000m"
        memory: "2Gi"

# Block pool with 3x replication
cephBlockPools:
  - name: replicapool
    spec:
      failureDomain: host
      replicated:
        size: 3
        requireSafeReplicaSize: true
    storageClass:
      enabled: true
      name: ceph-block
      isDefault: true
      reclaimPolicy: Delete
      allowVolumeExpansion: true
      volumeBindingMode: Immediate
      parameters:
        imageFormat: "2"
        imageFeatures: layering

# Filesystem with active-standby MDS
cephFileSystems:
  - name: cephfs
    spec:
      metadataPool:
        replicated:
          size: 3
      dataPools:
        - name: data0
          failureDomain: host
          replicated:
            size: 3
      metadataServer:
        activeCount: 1
        activeStandby: true
        resources:
          limits:
            memory: "4Gi"
          requests:
            cpu: "1000m"
            memory: "1Gi"
    storageClass:
      enabled: true
      name: ceph-filesystem
      reclaimPolicy: Delete
      allowVolumeExpansion: true
      volumeBindingMode: Immediate

# Object store (S3-compatible)
cephObjectStores:
  - name: objectstore
    spec:
      metadataPool:
        failureDomain: host
        replicated:
          size: 3
      dataPool:
        failureDomain: host
        replicated:
          size: 3
      gateway:
        port: 80
        instances: 2
    storageClass:
      enabled: true
      name: ceph-bucket
      reclaimPolicy: Delete

# Toolbox for debugging
toolbox:
  enabled: true
```

## Alternative: Use All Devices

For clusters where all nodes contribute storage:

```yaml
cephClusterSpec:
  mon:
    count: 3
    allowMultiplePerNode: false
  mgr:
    count: 2
    allowMultiplePerNode: false
  placement:
    all:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: ceph-node
                  operator: In
                  values:
                    - "true"
  storage:
    useAllNodes: true
    useAllDevices: true
    deviceFilter: "^sd[b-z]"  # Only use sdb, sdc, etc.
```

## Label Nodes

```bash
kubectl label node node1 ceph-node=true
kubectl label node node2 ceph-node=true
kubectl label node node3 ceph-node=true
```
