# LLM Observability Stack (2026)

## Problem

Production AI requires comprehensive monitoring beyond basic logging.

## Solution: Full-Stack LLM Observability

**Platform Comparison:**

| Platform | Focus | Self-Host | Pricing |
|----------|-------|-----------|---------|
| Langfuse | Tracing, prompts, evals | Yes (MIT) | Free / $29/mo |
| Helicone | Cost analytics, caching | Yes | Free (10K req) / $79/mo |
| Arize Phoenix | Evaluation, embeddings | Yes | Free / $50/mo managed |
| Braintrust | Multi-agent tracing | No | Enterprise |
| Portkey | Gateway, fallbacks | Limited | Usage-based |

**Essential Metrics:**

| Category | Metrics |
|----------|---------|
| Cost | Token usage, cost/conversation, cache hit rate |
| Quality | Relevance scores, hallucination rate, user feedback |
| Performance | Latency (P50/P95/P99), throughput, TTFT |
| Reliability | Error rate, retry rate, fallback triggers |
| Agent-specific | Tool call success, reasoning steps, iteration count |

**Integration Architecture:**
```
Application
    |
Observability SDK (OpenTelemetry/OpenInference)
    |
+-- Tracing -> Langfuse/Phoenix
+-- Analytics -> Helicone Dashboard
+-- Evaluation -> Automated quality gates
+-- Alerting -> Cost/quality thresholds
```

**Setup Times:**
- Helicone: 15 minutes (proxy-based)
- Langfuse: Few hours (SDK-based)
- Cost savings: 20-30% with caching

---

*AI/ML Best Practices 2026*
