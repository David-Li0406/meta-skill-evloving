# Operations Guide - Content Management

Guide opérationnel pour la gestion des erreurs, la résilience et la performance.

## Error Handling

### Politique de Retry

```yaml
retry_policy:
  default:
    max_attempts: 3
    backoff: exponential
    initial_delay: 1s
    max_delay: 30s
    jitter: true

  by_operation:
    api_call:
      max_attempts: 5
      backoff: exponential
      initial_delay: 2s
      retryable_errors: [timeout, 5xx, connection_refused]

    file_upload:
      max_attempts: 3
      backoff: linear
      initial_delay: 5s
      retryable_errors: [timeout, network_error]

    translation:
      max_attempts: 2
      backoff: fixed
      delay: 10s
      retryable_errors: [rate_limit, service_unavailable]

    cdn_purge:
      max_attempts: 5
      backoff: exponential
      initial_delay: 1s
      retryable_errors: [timeout, 5xx]
```

### Circuit Breaker

```yaml
circuit_breaker:
  translation_service:
    failure_threshold: 5
    success_threshold: 2
    timeout: 60s
    half_open_requests: 3

  cdn_service:
    failure_threshold: 10
    success_threshold: 5
    timeout: 30s

  image_processing:
    failure_threshold: 3
    success_threshold: 1
    timeout: 120s
```

### Gestion des Erreurs par Type

| Type d'erreur | Action | Retry | Notification |
|---------------|--------|-------|--------------|
| Validation error | Reject + log | Non | User |
| Network timeout | Retry avec backoff | Oui (5x) | Si échec final |
| Rate limit | Attendre + retry | Oui (3x) | Si persistant |
| Service unavailable | Circuit breaker | Oui | Ops team |
| Data corruption | Rollback | Non | Immediate |
| Authentication | Refresh token | Oui (1x) | Si échec |

## Rollback Mechanisms

### Rollback de Publication

```
┌─────────────────────────────────────────────────────────────┐
│                    ROLLBACK PUBLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   TRIGGER                 ACTION                 VERIFY      │
│                                                              │
│   ┌──────────┐      ┌──────────────┐      ┌──────────┐     │
│   │ Détection│─────►│ Restore prev │─────►│ Health   │     │
│   │ erreur   │      │ version      │      │ check    │     │
│   └──────────┘      └──────────────┘      └──────────┘     │
│        │                   │                    │           │
│        ▼                   ▼                    ▼           │
│   ┌──────────┐      ┌──────────────┐      ┌──────────┐     │
│   │ Alert    │      │ Purge cache  │      │ Notify   │     │
│   │ ops      │      │              │      │ team     │     │
│   └──────────┘      └──────────────┘      └──────────┘     │
│                                                              │
│   TTR cible: < 5 minutes                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Stratégies de Rollback

| Scope | Méthode | Données préservées | TTR |
|-------|---------|-------------------|-----|
| Single content | Version restore | Toutes versions | < 1 min |
| Batch publish | Transaction rollback | Pre-batch state | < 5 min |
| Asset update | CDN version restore | Previous URLs valid | < 2 min |
| Translation | Fallback to source | Source content | Immediate |
| Full workflow | Checkpoint restore | All checkpoints | < 10 min |

### Checkpoints

```yaml
checkpoints:
  brief-to-article:
    - name: brief_validated
      data: [brief_id, validation_result]
      retention: 30d

    - name: draft_created
      data: [content_id, draft_content]
      retention: 90d

    - name: seo_optimized
      data: [content_id, seo_metadata]
      retention: 90d

    - name: review_approved
      data: [content_id, reviewer, timestamp]
      retention: 1y

    - name: published
      data: [content_id, url, cdn_urls]
      retention: 1y

  recovery:
    auto_recover: true
    max_checkpoint_age: 7d
    notification_on_recovery: true
```

## Failure Recovery

### Dead Letter Queue

```yaml
dead_letter_queue:
  enabled: true
  max_retries_before_dlq: 5
  retention: 14d

  handlers:
    translation_failed:
      action: manual_review
      notify: [content-team, localization-team]
      sla: 24h

    publish_failed:
      action: auto_retry_with_fallback
      fallback: draft_state
      notify: [ops-team]
      sla: 1h

    asset_processing_failed:
      action: queue_for_reprocessing
      notify: [content-team]
      sla: 4h
```

### Recovery Procedures

```bash
# Lister les échecs en attente
/content dlq list --status=pending

# Retry manuel d'un job
/content dlq retry JOB-ID

# Retry tous les jobs d'un type
/content dlq retry-all --type=translation

# Marquer comme résolu (skip)
/content dlq resolve JOB-ID --reason="Manual fix applied"

# Voir les détails d'un échec
/content dlq inspect JOB-ID
```

## Performance

### Batch Processing

```yaml
batch_processing:
  # Environment-specific configurations
  environments:
    development:
      image_optimization:
        batch_size: 2
        max_concurrent: 1
        timeout_per_item: 120s
      translation:
        batch_size: 2
        max_concurrent: 1
        rate_limit: 10/min
      cdn_upload:
        batch_size: 5
        max_concurrent: 2

    staging:
      image_optimization:
        batch_size: 5
        max_concurrent: 2
        timeout_per_item: 90s
      translation:
        batch_size: 3
        max_concurrent: 1
        rate_limit: 50/min
      cdn_upload:
        batch_size: 10
        max_concurrent: 3

    production:
      image_optimization:
        batch_size: 10
        max_concurrent: 3
        timeout_per_item: 60s
      translation:
        batch_size: 5
        max_concurrent: 2
        rate_limit: 100/min
      cdn_upload:
        batch_size: 20
        max_concurrent: 5

  # Shared settings
  defaults:
    priority_queue: true
    multipart_threshold: 5MB
    retry_failed: true
    max_retries: 3

  # Auto-scaling rules (production only)
  auto_scaling:
    enabled: ${ENVIRONMENT === 'production'}
    min_workers: 2
    max_workers: 10
    scale_up_threshold: 100  # Queue depth
    scale_down_threshold: 10
    cooldown: 300s
```

### Async Processing

```yaml
async_jobs:
  video_transcoding:
    queue: high-priority
    timeout: 30m
    progress_updates: true
    callback_url: /api/webhooks/video-ready

  bulk_translation:
    queue: default
    timeout: 2h
    progress_updates: true
    chunk_size: 50

  sitemap_generation:
    queue: low-priority
    timeout: 10m
    schedule: "0 3 * * *"  # 3h du matin
```

### Progress Tracking

```json
{
  "job_id": "JOB-2025-001234",
  "type": "bulk_translation",
  "status": "in_progress",
  "progress": {
    "total": 150,
    "completed": 87,
    "failed": 2,
    "percentage": 58
  },
  "started_at": "2025-01-10T10:00:00Z",
  "estimated_completion": "2025-01-10T10:45:00Z",
  "current_item": {
    "id": "CONTENT-088",
    "title": "Guide SEO 2025",
    "status": "translating"
  }
}
```

### Caching Strategy

| Resource | Cache | TTL | Invalidation |
|----------|-------|-----|--------------|
| Published content | CDN + App | 1h | On publish |
| Assets (images) | CDN | 1 year | Versioned URL |
| Translations | App | 24h | On update |
| Metadata | App | 15min | On change |
| Search index | Elasticsearch | Real-time | Incremental |

### Rate Limiting

```yaml
rate_limits:
  api:
    requests_per_minute: 100
    burst: 20

  upload:
    files_per_minute: 10
    max_file_size: 100MB
    total_size_per_hour: 1GB

  translation:
    requests_per_minute: 50
    characters_per_day: 1000000

  publishing:
    publishes_per_minute: 5
    batch_size: 50
```

## Monitoring

### Health Checks

```yaml
health_checks:
  endpoints:
    - name: content-api
      url: /health
      interval: 30s
      timeout: 5s
      unhealthy_threshold: 3

    - name: translation-service
      url: /api/translation/health
      interval: 60s
      timeout: 10s

    - name: cdn
      url: https://cdn.example.com/health
      interval: 60s
      timeout: 5s

  alerts:
    slack: "#ops-alerts"
    pagerduty: content-management
```

### Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTENT MANAGEMENT METRICS                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Publishing                    Assets                       │
│   ───────────                   ──────                       │
│   Success rate: 99.2%           Processed: 1,234/day        │
│   Avg time: 2.3s                Avg size: 450KB → 85KB      │
│   Queue depth: 12               Compression: 81%             │
│                                                              │
│   Translation                   Workflows                    │
│   ───────────                   ─────────                    │
│   Languages: 5                  Active: 23                   │
│   Avg time: 45s/page            Completed: 156/day          │
│   Coverage: 98.5%               Failed: 2 (1.3%)            │
│                                                              │
│   Error rates (last 24h)                                     │
│   ─────────────────────                                      │
│   │████████░░│ API: 0.8%                                    │
│   │██░░░░░░░░│ CDN: 0.2%                                    │
│   │███░░░░░░░│ Translation: 0.3%                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Alerting Rules

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Error rate | > 1% | > 5% | Page on-call |
| Queue depth | > 100 | > 500 | Scale workers |
| Latency p99 | > 5s | > 15s | Investigate |
| Disk usage | > 80% | > 95% | Cleanup + alert |
| Failed jobs | > 5/h | > 20/h | Investigate |

## Disaster Recovery

### Backup Strategy

| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Content DB | Hourly | 30 days | S3 cross-region |
| Assets | Real-time sync | 1 year | Multi-CDN |
| Configs | On change | 90 days | Git + S3 |
| Logs | Daily | 90 days | CloudWatch |

### RTO/RPO Targets

| Scenario | RTO | RPO |
|----------|-----|-----|
| Single content loss | 5 min | 0 (versioned) |
| Asset CDN failure | 15 min | 0 (multi-CDN) |
| Database failure | 1 hour | 1 hour |
| Full region outage | 4 hours | 1 hour |

## Références

- [SKILL.md](./SKILL.md) - Vue d'ensemble du skill
- [SECURITY.md](./SECURITY.md) - Guide de sécurité
- [devops/SKILL.md](../devops/SKILL.md) - Infrastructure et déploiement
