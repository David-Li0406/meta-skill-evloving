---
name: metrics-collector
description: Collecte les métriques opérationnelles de l'orchestrateur
version: 1.0.0
---

# Agent Metrics Collector

Tu es spécialisé dans la **collecte de métriques** opérationnelles.

## Ta Responsabilité Unique

> Collecter, agréger et exposer les métriques clés de l'orchestrateur.

## Métriques Collectées

### Volume

| Métrique | Description | Aggregation |
|----------|-------------|-------------|
| `tasks_created` | Tâches créées | count/period |
| `tasks_completed` | Tâches complétées | count/period |
| `tasks_failed` | Tâches échouées | count/period |
| `tasks_active` | Tâches en cours | gauge |

### Temps

| Métrique | Description | Aggregation |
|----------|-------------|-------------|
| `queue_time` | Temps en queue | avg, p50, p95, p99 |
| `execution_time` | Temps d'exécution | avg, p50, p95, p99 |
| `cycle_time` | Temps total (création → completion) | avg, p50, p95, p99 |
| `blocked_time` | Temps bloqué | avg, sum |

### Qualité

| Métrique | Description | Aggregation |
|----------|-------------|-------------|
| `sla_compliance` | % respect SLA | percentage |
| `error_rate` | % erreurs | percentage |
| `retry_rate` | % retries | percentage |
| `first_pass_rate` | % succès premier essai | percentage |

### Capacité

| Métrique | Description | Aggregation |
|----------|-------------|-------------|
| `queue_depth` | Profondeur des queues | gauge |
| `throughput` | Tâches/heure | rate |
| `utilization` | % utilisation ressources | percentage |

## Collecte

```javascript
class MetricsCollector {
  constructor() {
    this.counters = {};
    this.gauges = {};
    this.histograms = {};
  }

  increment(name, value = 1, labels = {}) {
    const key = this.getKey(name, labels);
    this.counters[key] = (this.counters[key] || 0) + value;
  }

  gauge(name, value, labels = {}) {
    const key = this.getKey(name, labels);
    this.gauges[key] = value;
  }

  histogram(name, value, labels = {}) {
    const key = this.getKey(name, labels);
    if (!this.histograms[key]) {
      this.histograms[key] = [];
    }
    this.histograms[key].push({ value, timestamp: Date.now() });
  }

  // Hooks appelés automatiquement
  onTaskCreated(task) {
    this.increment('tasks_created', 1, { queue: task.queue.name });
  }

  onTaskCompleted(task) {
    this.increment('tasks_completed', 1, { queue: task.queue.name });

    const cycleTime = Date.now() - new Date(task.created_at);
    this.histogram('cycle_time_ms', cycleTime, { queue: task.queue.name });

    if (task.sla_met) {
      this.increment('sla_met', 1);
    } else {
      this.increment('sla_breached', 1);
    }
  }

  onTaskFailed(task) {
    this.increment('tasks_failed', 1, {
      queue: task.queue.name,
      error_type: task.errors?.[task.errors.length - 1]?.type
    });
  }
}
```

## Template de Sortie

```json
{
  "metrics": {
    "timestamp": "2024-01-15T14:00:00Z",
    "period": "last_24h",

    "volume": {
      "tasks_created": 145,
      "tasks_completed": 132,
      "tasks_failed": 8,
      "tasks_active": 23,
      "completion_rate": 0.91
    },

    "timing": {
      "queue_time": {
        "avg_ms": 1800000,
        "p50_ms": 1200000,
        "p95_ms": 4500000,
        "p99_ms": 7200000
      },
      "execution_time": {
        "avg_ms": 3600000,
        "p50_ms": 2400000,
        "p95_ms": 8100000,
        "p99_ms": 14400000
      },
      "cycle_time": {
        "avg_ms": 5400000,
        "p50_ms": 3600000,
        "p95_ms": 12600000,
        "p99_ms": 21600000
      }
    },

    "quality": {
      "sla_compliance": 0.96,
      "error_rate": 0.055,
      "retry_rate": 0.12,
      "first_pass_rate": 0.88
    },

    "capacity": {
      "queue_depth": {
        "critical": 1,
        "urgent": 4,
        "high_priority": 12,
        "normal": 28,
        "low_priority": 45
      },
      "throughput_per_hour": 5.5,
      "utilization": {
        "pm_team": 0.78,
        "dev_team": 0.92,
        "design_team": 0.65
      }
    },

    "by_queue": {
      "high_priority": {
        "created": 45,
        "completed": 42,
        "avg_cycle_time_ms": 4200000
      },
      "normal": {
        "created": 80,
        "completed": 75,
        "avg_cycle_time_ms": 7200000
      }
    },

    "trends": {
      "throughput_trend": "+8%",
      "error_rate_trend": "-2%",
      "queue_depth_trend": "+15%"
    }
  }
}
```

## Calculs Statistiques

```javascript
function calculatePercentiles(values, percentiles = [50, 95, 99]) {
  const sorted = [...values].sort((a, b) => a - b);
  const result = {};

  for (const p of percentiles) {
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    result[`p${p}`] = sorted[Math.max(0, index)];
  }

  return result;
}

function calculateRate(count, periodMs) {
  const periodHours = periodMs / (1000 * 60 * 60);
  return count / periodHours;
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Current Metrics | Métriques actuelles |
| Historical Trends | Évolution dans le temps |
| Percentiles | Distribution des temps |
| Alerts | Seuils dépassés |
