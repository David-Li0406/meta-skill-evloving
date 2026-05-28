---
title: Plan Cluster Resharding Carefully
impact: MEDIUM
impactDescription: improper resharding can cause data loss or outages
tags: cluster, resharding, scaling, operations
---

## Plan Cluster Resharding Carefully

Plan and execute cluster resharding carefully. Resharding moves hash slots between nodes and can impact performance during migration. Follow best practices to minimize impact and avoid data loss.

**When Resharding is Needed:**
- Adding nodes to scale out
- Removing nodes to scale in
- Rebalancing uneven data distribution
- Hardware replacement

**Resharding Impact:**
- Increased latency during slot migration
- ASK redirects during migration
- Memory usage spikes on source and target
- Network bandwidth consumption

**Incorrect (dangerous resharding practices):**

```bash
# Anti-pattern 1: Resharding without backup
redis-cli --cluster reshard node1:6379  # No backup first!

# Anti-pattern 2: Moving too many slots at once
redis-cli --cluster reshard node1:6379 \
    --cluster-from xxx --cluster-to yyy \
    --cluster-slots 8192  # Half the cluster at once!

# Anti-pattern 3: Resharding during peak traffic
# Running reshard during business hours

# Anti-pattern 4: Not monitoring during reshard
# No visibility into progress or issues

# Anti-pattern 5: Removing node before emptying
redis-cli --cluster del-node node1:6379 <node-id>
# Will fail or lose data if node still has slots
```

**Correct (safe resharding practices):**

```bash
# Correct 1: Pre-resharding checklist
# 1. Backup all nodes (RDB)
# 2. Check cluster health
# 3. Plan during low-traffic window
# 4. Notify stakeholders
# 5. Have rollback plan

# Check cluster health first
redis-cli --cluster check node1:6379

# Verify cluster state
redis-cli -c -h node1 -p 6379 CLUSTER INFO

# Correct 2: Add new node before resharding
# Add empty node to cluster
redis-cli --cluster add-node new-node:6379 existing-node:6379

# Verify node added
redis-cli --cluster check node1:6379

# Correct 3: Reshard in small batches
# Move 1000 slots at a time, not all at once
redis-cli --cluster reshard node1:6379 \
    --cluster-from <source-node-id> \
    --cluster-to <target-node-id> \
    --cluster-slots 1000 \
    --cluster-yes

# Correct 4: Use redis-cli --cluster rebalance for even distribution
redis-cli --cluster rebalance node1:6379 \
    --cluster-weight <node-id>=1 \
    --cluster-use-empty-masters
```

```python
from redis.cluster import RedisCluster
import time

rc = RedisCluster(host='node1', port=6379)

# Correct 5: Monitor during resharding
def monitor_resharding():
    """Monitor cluster during resharding operations"""
    while True:
        health = check_cluster_during_reshard()
        print(f"Cluster state: {health['state']}")
        print(f"Migrating slots: {health['migrating_slots']}")
        print(f"Importing slots: {health['importing_slots']}")

        if health['migrating_slots'] == 0 and health['importing_slots'] == 0:
            print("Resharding complete!")
            break

        time.sleep(5)

def check_cluster_during_reshard():
    """Check cluster status during resharding"""
    cluster_info = rc.cluster_info()
    nodes_info = rc.cluster_nodes()

    migrating = 0
    importing = 0

    # Count migrating/importing slots
    for node_line in nodes_info.split('\n'):
        migrating += node_line.count('[')
        if 'importing' in node_line.lower():
            importing += 1

    return {
        'state': cluster_info.get('cluster_state'),
        'migrating_slots': migrating,
        'importing_slots': importing,
        'cluster_size': cluster_info.get('cluster_size'),
        'known_nodes': cluster_info.get('cluster_known_nodes'),
    }

# Correct 6: Verify data integrity after resharding
def verify_cluster_after_reshard(sample_keys):
    """Verify data accessible after resharding"""
    issues = []

    for key in sample_keys:
        try:
            value = rc.get(key)
            if value is None:
                issues.append(f"Key {key} not found")
        except Exception as e:
            issues.append(f"Key {key} error: {e}")

    # Check slot coverage
    cluster_info = rc.cluster_info()
    if cluster_info.get('cluster_slots_ok') != 16384:
        issues.append(f"Not all slots covered: {cluster_info.get('cluster_slots_ok')}/16384")

    return {'valid': len(issues) == 0, 'issues': issues}
```

```python
# Correct 7: Safe node removal procedure
def safe_remove_node(rc, node_id):
    """Safely remove a node from cluster"""

    # Step 1: Check if node has slots
    nodes = rc.cluster_nodes()
    node_line = [l for l in nodes.split('\n') if node_id in l]

    if not node_line:
        print(f"Node {node_id} not found")
        return False

    # Check for slots
    if 'master' in node_line[0] and any(c.isdigit() for c in node_line[0].split('connected')[-1]):
        print(f"Node {node_id} still has slots - must reshard first!")
        return False

    # Step 2: Verify node has no slots
    slot_count = 0  # Parse slot ranges from node info
    if slot_count > 0:
        print(f"Node has {slot_count} slots - reshard first")
        return False

    # Step 3: Remove node
    print(f"Removing node {node_id}...")
    # redis-cli --cluster del-node <any-node>:6379 <node-id>

    return True

# Correct 8: Rolling upgrade procedure
def rolling_upgrade_plan(nodes):
    """Plan for rolling cluster upgrade"""
    plan = []

    for i, node in enumerate(nodes):
        step = {
            'order': i + 1,
            'node': node,
            'actions': [
                f"1. Verify cluster health",
                f"2. Take backup of {node}",
                f"3. If master, failover to replica first",
                f"4. Upgrade {node}",
                f"5. Restart {node}",
                f"6. Wait for node to rejoin cluster",
                f"7. Verify cluster health",
                f"8. Wait for replication to catch up (if replica)",
            ]
        }
        plan.append(step)

    return plan
```

```bash
# Correct 9: Complete resharding procedure

# Pre-flight checks
echo "=== Pre-flight Checks ==="
redis-cli --cluster check node1:6379
redis-cli -c -h node1 CLUSTER INFO | grep cluster_state

# Backup
echo "=== Creating Backups ==="
for node in node1 node2 node3; do
    redis-cli -h $node BGSAVE
done
sleep 10

# Add new node
echo "=== Adding New Node ==="
redis-cli --cluster add-node new-node:6379 node1:6379

# Reshard in batches
echo "=== Resharding (batch 1/4) ==="
redis-cli --cluster reshard node1:6379 \
    --cluster-from all \
    --cluster-to <new-node-id> \
    --cluster-slots 1000 \
    --cluster-yes

# Check between batches
redis-cli --cluster check node1:6379

# Continue with more batches...

# Final verification
echo "=== Final Verification ==="
redis-cli --cluster check node1:6379
redis-cli -c -h node1 CLUSTER INFO
```

Reference: [Redis Cluster Administration](https://redis.io/docs/management/scaling/)
