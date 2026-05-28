#!/bin/bash
set -euo pipefail

# Rook Ceph Multi-Node Install Script
# Usage: ./install.sh [values-file]

NAMESPACE="rook-ceph"
VALUES_FILE="${1:-}"

echo "=== Rook Ceph Multi-Node Installation ==="

# Add Helm repo
echo "Adding Rook Helm repository..."
helm repo add rook-release https://charts.rook.io/release
helm repo update

# Install operator
echo "Installing Rook Ceph operator..."
helm upgrade --install --create-namespace --namespace "$NAMESPACE" \
  rook-ceph rook-release/rook-ceph

# Wait for operator
echo "Waiting for operator to be ready..."
kubectl -n "$NAMESPACE" wait --for=condition=ready pod \
  -l app=rook-ceph-operator --timeout=300s

# Install cluster
if [ -n "$VALUES_FILE" ]; then
  echo "Installing Rook Ceph cluster with $VALUES_FILE..."
  helm upgrade --install --namespace "$NAMESPACE" rook-ceph-cluster \
    --set operatorNamespace="$NAMESPACE" \
    rook-release/rook-ceph-cluster -f "$VALUES_FILE"
else
  echo "Installing Rook Ceph cluster with default multi-node values..."

  # Generate default multi-node values
  TMP_VALUES=$(mktemp)
  cat > "$TMP_VALUES" << 'EOF'
cephClusterSpec:
  mon:
    count: 3
    allowMultiplePerNode: false
  mgr:
    count: 2
    allowMultiplePerNode: false
  dashboard:
    enabled: true
    ssl: true
  storage:
    useAllNodes: true
    useAllDevices: true

cephBlockPools:
  - name: replicapool
    spec:
      failureDomain: host
      replicated:
        size: 3
    storageClass:
      enabled: true
      name: ceph-block
      isDefault: true
      reclaimPolicy: Delete
      allowVolumeExpansion: true

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
    storageClass:
      enabled: true
      name: ceph-filesystem
      reclaimPolicy: Delete
      allowVolumeExpansion: true

cephObjectStores: []

toolbox:
  enabled: true
EOF

  helm upgrade --install --namespace "$NAMESPACE" rook-ceph-cluster \
    --set operatorNamespace="$NAMESPACE" \
    rook-release/rook-ceph-cluster -f "$TMP_VALUES"

  rm -f "$TMP_VALUES"
fi

echo ""
echo "=== Installation initiated ==="
echo "Monitor progress with:"
echo "  kubectl -n $NAMESPACE get pods -w"
echo "  kubectl -n $NAMESPACE get cephcluster -w"
echo ""
echo "Once healthy, check Ceph status:"
echo "  kubectl -n $NAMESPACE exec -it deploy/rook-ceph-tools -- ceph status"
echo "  kubectl -n $NAMESPACE exec -it deploy/rook-ceph-tools -- ceph osd tree"
