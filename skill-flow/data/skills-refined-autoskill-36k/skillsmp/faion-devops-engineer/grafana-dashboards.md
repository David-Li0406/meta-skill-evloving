---
id: grafana-dashboards
name: "Grafana Dashboards"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Grafana Dashboards

## Overview

Grafana is an open-source observability platform for visualizing metrics, logs, and traces. It supports multiple data sources (Prometheus, Loki, Elasticsearch), provides rich visualization options, and enables alerting based on dashboard panels.

## When to Use

- Visualizing Prometheus metrics
- Creating operational dashboards
- Building SLO/SLI dashboards
- Log analysis with Loki
- Unified observability across multiple data sources

## Key Concepts

| Concept | Description |
|---------|-------------|
| Dashboard | Collection of panels organized in rows |
| Panel | Individual visualization (graph, table, stat) |
| Data Source | Backend providing data (Prometheus, Loki) |
| Variable | Dynamic values for filtering dashboards |
| Alert | Condition-based notifications from panels |
| Annotation | Event markers on graphs |
| Folder | Organizational container for dashboards |

### Visualization Types

| Type | Use Case |
|------|----------|
| Time series | Metrics over time |
| Stat | Single value display |
| Gauge | Value within range |
| Bar gauge | Comparative values |
| Table | Tabular data |
| Heatmap | Distribution over time |
| Logs | Log aggregation display |

## Implementation

### Dashboard JSON Model

```json
{
  "dashboard": {
    "id": null,
    "uid": "myapp-overview",
    "title": "MyApp Overview",
    "description": "Application performance and health metrics",
    "tags": ["myapp", "production"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "templating": {
      "list": [
        {
          "name": "namespace",
          "type": "query",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "query": "label_values(kube_pod_info, namespace)",
          "refresh": 1,
          "includeAll": false,
          "current": {
            "text": "production",
            "value": "production"
          }
        },
        {
          "name": "pod",
          "type": "query",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)",
          "refresh": 2,
          "includeAll": true,
          "multi": true
        },
        {
          "name": "interval",
          "type": "interval",
          "options": [
            {"text": "1m", "value": "1m"},
            {"text": "5m", "value": "5m"},
            {"text": "15m", "value": "15m"},
            {"text": "1h", "value": "1h"}
          ],
          "current": {
            "text": "5m",
            "value": "5m"
          }
        }
      ]
    },
    "annotations": {
      "list": [
        {
          "name": "Deployments",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "enable": true,
          "expr": "changes(kube_deployment_status_observed_generation{namespace=\"$namespace\"}[5m]) > 0",
          "titleFormat": "Deployment",
          "textFormat": "{{ deployment }}"
        }
      ]
    },
    "panels": []
  }
}
```

### Row: Overview Statistics

```json
{
  "type": "row",
  "title": "Overview",
  "collapsed": false,
  "panels": [
    {
      "type": "stat",
      "title": "Request Rate",
      "gridPos": {"h": 4, "w": 4, "x": 0, "y": 1},
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval]))",
          "legendFormat": "Requests/s"
        }
      ],
      "options": {
        "reduceOptions": {
          "calcs": ["lastNotNull"],
          "fields": "",
          "values": false
        },
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "textMode": "auto"
      },
      "fieldConfig": {
        "defaults": {
          "unit": "reqps",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 1000},
              {"color": "red", "value": 5000}
            ]
          }
        }
      }
    },
    {
      "type": "stat",
      "title": "Error Rate",
      "gridPos": {"h": 4, "w": 4, "x": 4, "y": 1},
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[$interval])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) * 100",
          "legendFormat": "Error %"
        }
      ],
      "options": {
        "reduceOptions": {
          "calcs": ["lastNotNull"]
        },
        "colorMode": "value",
        "graphMode": "area"
      },
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "decimals": 2,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 1},
              {"color": "red", "value": 5}
            ]
          }
        }
      }
    },
    {
      "type": "stat",
      "title": "P99 Latency",
      "gridPos": {"h": 4, "w": 4, "x": 8, "y": 1},
      "targets": [
        {
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
          "legendFormat": "P99"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "s",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 0.5},
              {"color": "red", "value": 1}
            ]
          }
        }
      }
    },
    {
      "type": "stat",
      "title": "Available Pods",
      "gridPos": {"h": 4, "w": 4, "x": 12, "y": 1},
      "targets": [
        {
          "expr": "sum(kube_deployment_status_replicas_available{namespace=\"$namespace\"})",
          "legendFormat": "Available"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "short",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "red", "value": null},
              {"color": "yellow", "value": 2},
              {"color": "green", "value": 3}
            ]
          }
        }
      }
    }
  ]
}
```

### Time Series Panel

```json
{
  "type": "timeseries",
  "title": "Request Rate by Status",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 5},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) by (status)",
      "legendFormat": "{{status}}"
    }
  ],
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "right",
      "showLegend": true,
      "calcs": ["mean", "max", "last"]
    },
    "tooltip": {
      "mode": "multi",
      "sort": "desc"
    }
  },
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "lineWidth": 2,
        "fillOpacity": 20,
        "gradientMode": "opacity",
        "spanNulls": false,
        "showPoints": "never",
        "stacking": {
          "mode": "none"
        }
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byRegexp", "options": "/5../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "red", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byRegexp", "options": "/2../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "green", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

### Latency Heatmap

```json
{
  "type": "heatmap",
  "title": "Request Latency Distribution",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 5},
  "targets": [
    {
      "expr": "sum(increase(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le)",
      "format": "heatmap",
      "legendFormat": "{{le}}"
    }
  ],
  "options": {
    "calculate": false,
    "cellGap": 1,
    "color": {
      "mode": "scheme",
      "scheme": "Spectral",
      "steps": 64
    },
    "yAxis": {
      "unit": "s"
    },
    "tooltip": {
      "show": true,
      "yHistogram": true
    },
    "legend": {
      "show": true
    }
  }
}
```

### Resource Usage Panels

```json
{
  "type": "timeseries",
  "title": "CPU Usage",
  "gridPos": {"h": 6, "w": 12, "x": 0, "y": 13},
  "targets": [
    {
      "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\",container!=\"\",container!=\"POD\"}[$interval])) by (pod)",
      "legendFormat": "{{pod}}"
    },
    {
      "expr": "sum(kube_pod_container_resource_limits{namespace=\"$namespace\",resource=\"cpu\"}) by (pod)",
      "legendFormat": "{{pod}} limit"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "short",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 10
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byRegexp", "options": "/.* limit/"},
        "properties": [
          {"id": "custom.drawStyle", "value": "line"},
          {"id": "custom.lineStyle", "value": {"fill": "dash", "dash": [10, 10]}},
          {"id": "custom.fillOpacity", "value": 0}
        ]
      }
    ]
  }
},
{
  "type": "timeseries",
  "title": "Memory Usage",
  "gridPos": {"h": 6, "w": 12, "x": 12, "y": 13},
  "targets": [
    {
      "expr": "sum(container_memory_working_set_bytes{namespace=\"$namespace\",container!=\"\",container!=\"POD\"}) by (pod)",
      "legendFormat": "{{pod}}"
    },
    {
      "expr": "sum(kube_pod_container_resource_limits{namespace=\"$namespace\",resource=\"memory\"}) by (pod)",
      "legendFormat": "{{pod}} limit"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "bytes",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 10
      }
    }
  }
}
```

### Table Panel

```json
{
  "type": "table",
  "title": "Pod Status",
  "gridPos": {"h": 6, "w": 24, "x": 0, "y": 19},
  "targets": [
    {
      "expr": "kube_pod_info{namespace=\"$namespace\"}",
      "format": "table",
      "instant": true
    },
    {
      "expr": "kube_pod_status_phase{namespace=\"$namespace\"}",
      "format": "table",
      "instant": true
    },
    {
      "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\"}[5m])) by (pod)",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "merge"
    },
    {
      "id": "organize",
      "options": {
        "excludeByName": {
          "Time": true,
          "__name__": true,
          "job": true,
          "instance": true
        },
        "renameByName": {
          "pod": "Pod",
          "node": "Node",
          "phase": "Status",
          "Value #C": "CPU Usage"
        }
      }
    }
  ],
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Status"},
        "properties": [
          {
            "id": "mappings",
            "value": [
              {"type": "value", "options": {"Running": {"color": "green", "text": "Running"}}},
              {"type": "value", "options": {"Pending": {"color": "yellow", "text": "Pending"}}},
              {"type": "value", "options": {"Failed": {"color": "red", "text": "Failed"}}}
            ]
          }
        ]
      }
    ]
  }
}
```

### SLO Dashboard Panel

```json
{
  "type": "gauge",
  "title": "Availability SLO (99.9%)",
  "gridPos": {"h": 6, "w": 6, "x": 0, "y": 25},
  "targets": [
    {
      "expr": "(1 - sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[30d]))) * 100",
      "legendFormat": "Availability"
    }
  ],
  "options": {
    "showThresholdLabels": false,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 99,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "red", "value": null},
          {"color": "yellow", "value": 99.5},
          {"color": "green", "value": 99.9}
        ]
      }
    }
  }
},
{
  "type": "stat",
  "title": "Error Budget Remaining",
  "gridPos": {"h": 6, "w": 6, "x": 6, "y": 25},
  "targets": [
    {
      "expr": "((1 - 0.999) - (sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[30d])))) / (1 - 0.999) * 100",
      "legendFormat": "Budget"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "red", "value": null},
          {"color": "yellow", "value": 25},
          {"color": "green", "value": 50}
        ]
      }
    }
  }
}
```

### Logs Panel (Loki)

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 31},
  "datasource": {
    "type": "loki",
    "uid": "loki"
  },
  "targets": [
    {
      "expr": "{namespace=\"$namespace\", pod=~\"$pod\"} |= \"\" | json | line_format \"{{.level}} {{.message}}\"",
      "refId": "A"
    }
  ],
  "options": {
    "showTime": true,
    "showLabels": false,
    "showCommonLabels": false,
    "wrapLogMessage": true,
    "prettifyLogMessage": true,
    "enableLogDetails": true,
    "dedupStrategy": "none",
    "sortOrder": "Descending"
  }
}
```

### Dashboard as Code (Grafonnet)

```jsonnet
// dashboard.jsonnet
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local row = grafana.row;
local prometheus = grafana.prometheus;
local graphPanel = grafana.graphPanel;
local statPanel = grafana.statPanel;

local promDatasource = 'prometheus';

dashboard.new(
  'MyApp Overview',
  schemaVersion=38,
  tags=['myapp', 'production'],
  time_from='now-1h',
  refresh='30s',
)
.addTemplate(
  grafana.template.datasource(
    'datasource',
    'prometheus',
    'Prometheus',
  )
)
.addTemplate(
  grafana.template.query(
    name='namespace',
    datasource=promDatasource,
    query='label_values(kube_pod_info, namespace)',
    refresh='load',
  )
)
.addRow(
  row.new(title='Overview')
  .addPanel(
    statPanel.new(
      'Request Rate',
      datasource=promDatasource,
      unit='reqps',
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace="$namespace"}[5m]))',
        legendFormat='Requests/s',
      )
    ),
    gridPos={h: 4, w: 6, x: 0, y: 0}
  )
  .addPanel(
    graphPanel.new(
      'Request Rate by Status',
      datasource=promDatasource,
      span=12,
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace="$namespace"}[5m])) by (status)',
        legendFormat='{{status}}',
      )
    ),
    gridPos={h: 8, w: 12, x: 0, y: 4}
  )
)
```

### Provisioning Dashboards

```yaml
# provisioning/dashboards/dashboards.yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    folderUid: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards

  - name: 'infrastructure'
    orgId: 1
    folder: 'Infrastructure'
    type: file
    options:
      path: /var/lib/grafana/dashboards/infrastructure

  - name: 'applications'
    orgId: 1
    folder: 'Applications'
    type: file
    options:
      path: /var/lib/grafana/dashboards/applications
```

## Best Practices

1. **Use variables** - Enable filtering by namespace, pod, environment
2. **Set appropriate time ranges** - Match dashboard purpose (real-time vs historical)
3. **Use consistent colors** - Red for errors, green for success across dashboards
4. **Add descriptions** - Panel descriptions explain what metrics mean
5. **Group related panels** - Use rows for logical organization
6. **Set thresholds** - Visual indicators for healthy/warning/critical states
7. **Include annotations** - Mark deployments, incidents on graphs
8. **Version control dashboards** - Export JSON and store in Git
9. **Use dashboard links** - Connect related dashboards for drill-down
10. **Optimize queries** - Use recording rules for complex queries

## Common Pitfalls

1. **Too many panels** - Information overload. Focus on key metrics per dashboard.

2. **Missing variables** - Static dashboards don't scale. Add namespace/pod filters.

3. **No thresholds** - Requires mental calculation. Set visual thresholds for quick assessment.

4. **Inconsistent naming** - Hard to find dashboards. Use consistent naming conventions.

5. **Manual dashboard creation** - Changes lost on reinstall. Use provisioning and version control.

6. **Complex queries in panels** - Slow dashboards. Use recording rules for heavy queries.

## References

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [Grafonnet](https://github.com/grafana/grafonnet-lib)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
