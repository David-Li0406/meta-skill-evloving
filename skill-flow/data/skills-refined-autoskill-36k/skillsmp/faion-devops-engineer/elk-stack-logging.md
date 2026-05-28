---
id: elk-stack-logging
name: "ELK Stack Logging"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# ELK Stack Logging

## Overview

The ELK Stack (Elasticsearch, Logstash, Kibana) is a powerful logging and observability solution for centralized log management, search, and visualization. This methodology covers architecture design, deployment patterns, and operational best practices for production environments.

## When to Use

- Centralizing logs from multiple applications/services
- Building searchable log archives
- Creating operational dashboards for troubleshooting
- Implementing compliance logging requirements
- Setting up alerting based on log patterns

## Process/Steps

### 1. Architecture Overview

**Core Components:**
```
                    ┌─────────────────────────────────────┐
                    │           Kibana                     │
                    │    (Visualization & Dashboards)      │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │         Elasticsearch                │
                    │    (Storage & Search Engine)         │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
┌─────────▼─────────┐    ┌───────────▼───────────┐    ┌─────────▼─────────┐
│     Logstash      │    │        Beats           │    │   Direct API      │
│  (Processing)     │    │   (Lightweight)        │    │   (App SDK)       │
└─────────┬─────────┘    └───────────┬───────────┘    └─────────┬─────────┘
          │                           │                           │
┌─────────▼─────────────────────────────────────────────────────▼─────────┐
│                              Log Sources                                 │
│   (Applications, Servers, Containers, Network Devices, Cloud Services)   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Modern Stack Options:**
| Stack | Components | Use Case |
|-------|------------|----------|
| ELK | Elasticsearch, Logstash, Kibana | Traditional, heavy processing |
| EFK | Elasticsearch, Fluentd, Kibana | Kubernetes-native |
| Elastic Stack | Elasticsearch, Beats, Kibana | Lightweight collection |

### 2. Elasticsearch Configuration

**Cluster Design:**
```yaml
# elasticsearch.yml
cluster.name: production-logs
node.name: es-node-1

# Node roles
node.roles: [master, data, ingest]

# Network
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# Discovery
discovery.seed_hosts: ["es-node-1", "es-node-2", "es-node-3"]
cluster.initial_master_nodes: ["es-node-1", "es-node-2", "es-node-3"]

# Memory
bootstrap.memory_lock: true

# Paths
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

# Security (X-Pack)
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```

**Index Template:**
```json
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "host": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "span_id": { "type": "keyword" }
      }
    }
  }
}
```

**Index Lifecycle Management (ILM):**
```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {},
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### 3. Logstash Configuration

**Pipeline Configuration:**
```ruby
# /etc/logstash/pipelines.yml
- pipeline.id: main
  path.config: "/etc/logstash/conf.d/*.conf"
  pipeline.workers: 4
  pipeline.batch.size: 125

# /etc/logstash/conf.d/main.conf
input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
  }

  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["app-logs"]
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
    }
  }

  # Parse common log formats
  grok {
    match => {
      "message" => [
        "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:log_message}",
        "%{COMBINEDAPACHELOG}"
      ]
    }
  }

  # Add geo-ip information
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geo"
    }
  }

  # Parse dates
  date {
    match => ["timestamp", "ISO8601", "yyyy-MM-dd HH:mm:ss"]
    target => "@timestamp"
  }

  # Add environment tags
  mutate {
    add_field => {
      "environment" => "production"
    }
    remove_field => ["agent", "ecs", "input"]
  }

  # Mask sensitive data
  mutate {
    gsub => [
      "message", "password=\S+", "password=[REDACTED]",
      "message", "\b\d{16}\b", "[CARD_REDACTED]"
    ]
  }
}

output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    index => "logs-%{[service]}-%{+YYYY.MM.dd}"
    user => "logstash"
    password => "${LOGSTASH_PASSWORD}"
    ssl_certificate_verification => true
    cacert => "/etc/logstash/certs/ca.crt"
  }

  # Dead letter queue for failed events
  if "_grokparsefailure" in [tags] {
    file {
      path => "/var/log/logstash/failed-%{+YYYY-MM-dd}.json"
      codec => json_lines
    }
  }
}
```

### 4. Filebeat Configuration

**Basic Configuration:**
```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    fields:
      service: my-app
      environment: production
    multiline:
      pattern: '^\d{4}-\d{2}-\d{2}'
      negate: true
      match: after
    processors:
      - add_host_metadata: ~
      - add_cloud_metadata: ~

  - type: container
    paths:
      - /var/lib/docker/containers/*/*.log
    processors:
      - add_docker_metadata: ~
      - add_kubernetes_metadata: ~

output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  protocol: "https"
  username: "filebeat"
  password: "${FILEBEAT_PASSWORD}"
  ssl:
    certificate_authorities: ["/etc/filebeat/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

setup.kibana:
  host: "https://kibana:5601"

logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
```

**Kubernetes Autodiscover:**
```yaml
filebeat.autodiscover:
  providers:
    - type: kubernetes
      node: ${NODE_NAME}
      hints.enabled: true
      hints.default_config:
        type: container
        paths:
          - /var/log/containers/*${data.kubernetes.container.id}.log

# Pod annotation for custom config:
# co.elastic.logs/enabled: "true"
# co.elastic.logs/json.keys_under_root: "true"
```

### 5. Kibana Configuration

**kibana.yml:**
```yaml
server.host: "0.0.0.0"
server.port: 5601
server.name: "kibana"

elasticsearch.hosts: ["https://elasticsearch:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "${KIBANA_PASSWORD}"
elasticsearch.ssl.certificateAuthorities: ["/etc/kibana/ca.crt"]

xpack.security.enabled: true
xpack.encryptedSavedObjects.encryptionKey: "your-32-char-encryption-key-here"

logging.dest: /var/log/kibana/kibana.log
```

**Dashboard Configuration:**
```json
// Export dashboard via API
GET /api/kibana/dashboards/export?dashboard=<dashboard-id>

// Import dashboard
POST /api/kibana/dashboards/import
{
  "objects": [
    {
      "type": "dashboard",
      "attributes": {
        "title": "Application Logs",
        "panelsJSON": "[...]"
      }
    }
  ]
}
```

### 6. Docker Compose Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - node.name=es01
      - cluster.name=docker-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config:/usr/share/logstash/config:ro
    ports:
      - "5044:5044"
      - "9600:9600"
    environment:
      - "LS_JAVA_OPTS=-Xms1g -Xmx1g"
    depends_on:
      - elasticsearch
    networks:
      - elk

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - elk

volumes:
  elasticsearch-data:

networks:
  elk:
    driver: bridge
```

### 7. Kubernetes Deployment (ECK)

```yaml
# Elastic Cloud on Kubernetes (ECK)
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: production-logs
  namespace: elastic-system
spec:
  version: 8.11.0
  nodeSets:
    - name: master
      count: 3
      config:
        node.roles: ["master"]
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 4Gi
                  cpu: 2
                limits:
                  memory: 4Gi
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            resources:
              requests:
                storage: 100Gi
            storageClassName: fast

    - name: data
      count: 3
      config:
        node.roles: ["data", "ingest"]
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 8Gi
                  cpu: 4
                limits:
                  memory: 8Gi
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            resources:
              requests:
                storage: 500Gi
            storageClassName: fast

---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: production-kibana
  namespace: elastic-system
spec:
  version: 8.11.0
  count: 2
  elasticsearchRef:
    name: production-logs
  http:
    tls:
      selfSignedCertificate:
        disabled: true
```

## Best Practices

### Cluster Design
1. **Separate node roles** - Master, data, ingest, coordinating
2. **Right-size shards** - 20-40GB per shard optimal
3. **Replica planning** - At least 1 replica for HA
4. **Hot-warm-cold architecture** - Cost-effective retention

### Index Management
1. **Use ILM policies** - Automate lifecycle
2. **Time-based indices** - Daily or weekly rollover
3. **Index templates** - Consistent mappings
4. **Alias strategy** - Abstract index names

### Performance
1. **Bulk indexing** - Batch requests
2. **Refresh interval** - Increase for write-heavy
3. **Shard sizing** - Balance search and indexing
4. **Heap sizing** - 50% of RAM, max 32GB

### Security
1. **Enable TLS** - Node-to-node and client
2. **RBAC** - Role-based access control
3. **Audit logging** - Track access
4. **Network isolation** - Private network for cluster

## Templates/Examples

### Structured Logging Format

```json
{
  "@timestamp": "2024-01-15T10:30:00.000Z",
  "level": "ERROR",
  "logger": "com.example.service.UserService",
  "message": "Failed to process user request",
  "service": "user-service",
  "version": "1.2.3",
  "environment": "production",
  "host": "pod-abc123",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user-12345",
  "request_id": "req-67890",
  "duration_ms": 1523,
  "error": {
    "type": "ValidationException",
    "message": "Invalid email format",
    "stack_trace": "..."
  },
  "context": {
    "endpoint": "/api/users",
    "method": "POST",
    "status_code": 400
  }
}
```

### Kibana Query Examples

```
# KQL (Kibana Query Language)

# Find errors in specific service
level: ERROR AND service: "user-service"

# Time range with log level
@timestamp >= "2024-01-15" AND level: (ERROR OR WARN)

# Full text search
message: "connection timeout"

# Exists check
trace_id: *

# Range query
duration_ms > 1000

# Combined complex query
(level: ERROR OR level: WARN) AND service: "api-*" AND NOT host: "test-*"
```

### Alerting Rule

```json
PUT _watcher/watch/error_rate_alert
{
  "trigger": {
    "schedule": { "interval": "5m" }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "filter": [
                { "range": { "@timestamp": { "gte": "now-5m" } } },
                { "term": { "level": "ERROR" } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": { "ctx.payload.hits.total.value": { "gt": 100 } }
  },
  "actions": {
    "slack_notification": {
      "slack": {
        "account": "team-alerts",
        "message": {
          "to": ["#alerts"],
          "text": "High error rate detected: {{ctx.payload.hits.total.value}} errors in last 5 minutes"
        }
      }
    }
  }
}
```

## References

- [Elastic Stack Documentation](https://www.elastic.co/guide/index.html)
- [Elasticsearch Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html)
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Elastic Cloud on Kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html)
