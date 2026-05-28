---
name: "lnx-distributed-setup"
description: "LNX distributed search cluster configuration. Use when setting up multi-node search clusters, need fault tolerance, or horizontal scaling requirements."
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["lnx", "distributed", "raft", "clustering", "text-search", "fault-tolerance"]
---

# LNX Distributed Setup Skill

## Descripción

LNX distributed search cluster configuration skill para búsqueda de texto distribuida con Raft consensus. Especializado en:
- Multi-node cluster setup
- Raft consensus protocol
- Automatic sharding y replication
- Fault tolerance y high availability

## Cuándo Usar

✅ **Usar esta skill cuando:**
- Necesitas búsqueda de texto distribuida
- Dataset >100M documentos
- Requieres alta disponibilidad (99.9%+)
- Necesitas horizontal scaling
- Fault tolerance es crítico
- Multi-tenant isolation necesaria

❌ **No usar cuando:**
- Dataset <10M documentos (usar Tantivy)
- Single-node suficiente
- Setup simple es prioridad
- No tienes múltiples máquinas

## Prerequisites

### Hardware (3-node minimum)
- **CPU**: 8+ cores por nodo
- **RAM**: 32GB+ por nodo
- **Storage**: 500GB+ SSD por nodo
- **Network**: 10Gbps recomendado

### Software
```bash
# Instalar LNX (cada nodo)
curl -sSL https://lnx.rs/install.sh | bash

# O con Docker
docker pull lnx/lnx:latest

# Verificar instalación
lnx --version
```

### Network Requirements
- Puertos 9200 (API), 9300 (Cluster)
- Latencia baja entre nodos (<5ms)
- Firewall rules configurados

## Instrucciones

### 1. Cluster Configuration

#### Node 1 (Leader candidate)
```toml
# /etc/lnx/node1.toml

[cluster]
node_id = "node1"
nodes = ["node1:9200", "node2:9200", "node3:9200"]
bind_address = "0.0.0.0:9200"

[raft]
# Election timeout (milliseconds)
election_timeout_ms = 300
heartbeat_interval_ms = 100
snapshot_interval = 1000
log_retention_count = 10000

[sharding]
strategy = "consistent_hash"
num_shards = 12  # Múltiplo del número de nodos
replication_factor = 3  # Cada shard en 3 nodos

[indices]
default_analyzer = "standard"
max_index_size_gb = 100

[performance]
search_threads = 8
indexing_threads = 4
cache_size_mb = 8192
```

#### Node 2
```toml
# /etc/lnx/node2.toml

[cluster]
node_id = "node2"
nodes = ["node1:9200", "node2:9200", "node3:9200"]
bind_address = "0.0.0.0:9200"

# Resto igual a node1
[raft]
election_timeout_ms = 300
heartbeat_interval_ms = 100
...
```

#### Node 3
```toml
# /etc/lnx/node3.toml

[cluster]
node_id = "node3"
nodes = ["node1:9200", "node2:9200", "node3:9200"]
bind_address = "0.0.0.0:9200"

[raft]
election_timeout_ms = 300
heartbeat_interval_ms = 100
...
```

### 2. Start Cluster

```bash
# Terminal 1 (node1)
lnx --config /etc/lnx/node1.toml

# Terminal 2 (node2)
lnx --config /etc/lnx/node2.toml

# Terminal 3 (node3)
lnx --config /etc/lnx/node3.toml

# Verificar cluster health
curl http://localhost:9200/_cluster/health
```

### 3. Rust Integration

```rust
// motores/text_search/lnx/lnx_engine.rs
use lnx_client::{Client, IndexSettings, SearchRequest};
use std::time::Duration;

pub struct LnxDistributedEngine {
    client: Client,
    cluster_nodes: Vec<String>,
}

impl LnxDistributedEngine {
    pub async fn new(nodes: Vec<String>) -> Result<Self, LnxError> {
        // Connect to cluster
        let client = Client::builder()
            .nodes(nodes.clone())
            .timeout(Duration::from_secs(5))
            .retry_on_failure(true)
            .max_retries(3)
            .build()?;
        
        Ok(LnxDistributedEngine {
            client,
            cluster_nodes: nodes,
        })
    }
    
    pub async fn create_distributed_index(
        &self,
        name: &str,
        settings: IndexSettings
    ) -> Result<(), LnxError> {
        // Create index with automatic sharding
        let settings = IndexSettings {
            shards: 12,
            replicas: 2,  // Each shard has 2 replicas
            analyzer: "standard".to_string(),
            ..settings
        };
        
        self.client.create_index(name, settings).await?;
        Ok(())
    }
    
    pub async fn distributed_search(
        &self,
        query: &str,
        indices: Vec<&str>
    ) -> Result<Vec<SearchResult>, LnxError> {
        let request = SearchRequest {
            query: query.to_string(),
            indices: indices.iter().map(|s| s.to_string()).collect(),
            size: 20,
            timeout: Duration::from_secs(5),
            distributed: true,  // Enable distributed search
        };
        
        // LNX handles:
        // - Query routing to appropriate shards
        // - Parallel search across nodes
        // - Result merging and ranking
        // - Automatic failover on node failure
        let results = self.client.search(request).await?;
        
        Ok(self.convert_results(results))
    }
    
    pub async fn check_cluster_health(&self) -> ClusterHealth {
        match self.client.cluster_health().await {
            Ok(health) => health,
            Err(e) => ClusterHealth::unhealthy(e.to_string())
        }
    }
    
    pub async fn get_shard_allocation(&self) -> ShardAllocation {
        // Visualize how shards are distributed
        self.client.get_shard_allocation().await.unwrap()
    }
}

// Failover handling
impl LnxDistributedEngine {
    pub async fn handle_node_failure(&self, failed_node: &str) -> Result<()> {
        // LNX automatically handles:
        // 1. Detect node failure via Raft heartbeats
        // 2. Elect new leader if needed
        // 3. Redistribute shards from failed node
        // 4. Update routing table
        
        // Wait for cluster to stabilize
        tokio::time::sleep(Duration::from_secs(5)).await;
        
        let health = self.check_cluster_health().await;
        
        if health.status == "green" {
            println!("✅ Cluster recovered from node failure");
            Ok(())
        } else {
            Err(LnxError::ClusterUnhealthy)
        }
    }
}
```

### 4. Docker Compose Deployment

```yaml
version: '3.8'

services:
  lnx-node1:
    image: lnx/lnx:latest
    container_name: lnx-node1
    ports:
      - "9201:9200"
      - "9301:9300"
    environment:
      - NODE_ID=node1
      - CLUSTER_NODES=node1,node2,node3
      - BIND_ADDRESS=0.0.0.0:9200
      - RAFT_ELECTION_TIMEOUT=300
      - RAFT_HEARTBEAT_INTERVAL=100
    volumes:
      - lnx1_data:/data
      - ./config/lnx-node1.toml:/etc/lnx/config.toml:ro
    networks:
      - lnx-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  lnx-node2:
    image: lnx/lnx:latest
    container_name: lnx-node2
    ports:
      - "9202:9200"
      - "9302:9300"
    environment:
      - NODE_ID=node2
      - CLUSTER_NODES=node1,node2,node3
    volumes:
      - lnx2_data:/data
      - ./config/lnx-node2.toml:/etc/lnx/config.toml:ro
    networks:
      - lnx-network
    restart: unless-stopped

  lnx-node3:
    image: lnx/lnx:latest
    container_name: lnx-node3
    ports:
      - "9203:9200"
      - "9303:9300"
    environment:
      - NODE_ID=node3
      - CLUSTER_NODES=node1,node2,node3
    volumes:
      - lnx3_data:/data
      - ./config/lnx-node3.toml:/etc/lnx/config.toml:ro
    networks:
      - lnx-network
    restart: unless-stopped

networks:
  lnx-network:
    driver: bridge

volumes:
  lnx1_data:
  lnx2_data:
  lnx3_data:
```

### 5. Kubernetes Deployment

```yaml
# k8s/lnx-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: lnx
  namespace: memory-p
spec:
  serviceName: lnx-service
  replicas: 3
  selector:
    matchLabels:
      app: lnx
  template:
    metadata:
      labels:
        app: lnx
    spec:
      containers:
      - name: lnx
        image: lnx/lnx:latest
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: cluster
        env:
        - name: NODE_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: CLUSTER_NODES
          value: "lnx-0.lnx-service,lnx-1.lnx-service,lnx-2.lnx-service"
        volumeMounts:
        - name: data
          mountPath: /data
        resources:
          requests:
            memory: "16Gi"
            cpu: "4000m"
          limits:
            memory: "32Gi"
            cpu: "8000m"
        readinessProbe:
          httpGet:
            path: /health
            port: 9200
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 9200
          initialDelaySeconds: 60
          periodSeconds: 30
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 500Gi

---
# Headless service for StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: lnx-service
  namespace: memory-p
spec:
  clusterIP: None
  selector:
    app: lnx
  ports:
  - port: 9200
    name: http
  - port: 9300
    name: cluster
```

## Ejemplos

### Example 1: Code Search Cluster

```rust
// Create LNX cluster for code search
let engine = LnxDistributedEngine::new(vec![
    "node1:9200".to_string(),
    "node2:9200".to_string(),
    "node3:9200".to_string(),
]).await?;

// Create distributed index
engine.create_distributed_index(
    "code",
    IndexSettings {
        shards: 12,
        replicas: 2,
        analyzer: "code".to_string(),
    }
).await?;

// Index code documents
engine.index_bulk(documents).await?;

// Distributed search
let results = engine.distributed_search(
    "async await tokio",
    vec!["code"]
).await?;
```

### Example 2: Failover Test

```rust
// Simulate node failure
println!("Simulating node2 failure...");
docker_stop("lnx-node2").await;

// Search should still work
let results = engine.distributed_search("rust", vec!["code"]).await?;
assert!(!results.is_empty(), "Cluster should handle node failure");

// Check cluster status
let health = engine.check_cluster_health().await;
println!("Cluster status: {:?}", health);

// Restore node
docker_start("lnx-node2").await;
tokio::time::sleep(Duration::from_secs(10)).await;

// Verify recovery
let health = engine.check_cluster_health().await;
assert_eq!(health.status, "green");
```

## Monitoring

### Cluster Health Check

```bash
# Check overall health
curl http://localhost:9200/_cluster/health

# Response:
{
  "status": "green",
  "number_of_nodes": 3,
  "active_shards": 36,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0
}
```

### Raft Status

```bash
# Check Raft consensus
curl http://localhost:9200/_cluster/raft

# Response:
{
  "leader": "node1",
  "term": 5,
  "commit_index": 1024,
  "last_applied": 1024,
  "nodes": {
    "node1": "Leader",
    "node2": "Follower",
    "node3": "Follower"
  }
}
```

### Shard Allocation

```bash
# View shard distribution
curl http://localhost:9200/_cluster/shards

# Response:
{
  "shards": [
    {"shard": 0, "primary": "node1", "replicas": ["node2", "node3"]},
    {"shard": 1, "primary": "node2", "replicas": ["node1", "node3"]},
    ...
  ]
}
```

## Best Practices

### ✅ DO's
1. **Use odd number of nodes** (3, 5, 7) for Raft quorum
2. **Configure proper replication** (factor 2-3)
3. **Monitor cluster health** continuously
4. **Use consistent hashing** for even distribution
5. **Plan for capacity** (scale before 80% utilization)
6. **Test failover** regularly

### ❌ DON'Ts
1. Don't use 2 nodes (no quorum)
2. Don't ignore Raft election timeouts
3. Don't mix slow and fast nodes
4. Don't skip health monitoring
5. Don't manually edit Raft logs

## Troubleshooting

### Split-Brain Prevention

```toml
# Ensure proper Raft configuration
[raft]
election_timeout_ms = 300  # Not too low
heartbeat_interval_ms = 100
min_quorum = 2  # For 3-node cluster
```

### Node Can't Join Cluster

```bash
# Check network connectivity
ping node2

# Check firewall
telnet node2 9200
telnet node2 9300

# Check logs
docker logs lnx-node1
```

### Slow Queries

```toml
# Optimize search settings
[performance]
search_threads = 16  # Increase
cache_size_mb = 16384  # Increase cache

[sharding]
num_shards = 24  # More shards for parallelism
```

## Resources

### Official Documentation
- [LNX GitHub](https://github.com/lnx-search/lnx)
- [Raft Consensus](https://raft.github.io/)

### Integration Examples
- See `motores/text_search/lnx/` for implementation
- See `docs/DISTRIBUTED_ARCHITECTURE.md` for architecture

---

**Última actualización:** Enero 2026  
**Proyecto:** MEMORY_P v2.0 - Nuclear MCP Toolkit  
**Autor:** Rigohl
