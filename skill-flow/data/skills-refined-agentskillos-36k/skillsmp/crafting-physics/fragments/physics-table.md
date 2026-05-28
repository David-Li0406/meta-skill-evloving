## Physics Table

| Effect | Sync | Timing | Confirmation |
|--------|------|--------|--------------|
| Financial | Pessimistic | 800ms | Required |
| Destructive | Pessimistic | 600ms | Required |
| Soft Delete | Optimistic | 200ms | Toast+Undo |
| Standard | Optimistic | 200ms | None |
| Navigation | Immediate | 150ms | None |
| Query | Optimistic | 150ms | None |
| Local State | Immediate | 100ms | None |
| High-freq | Immediate | 0ms | None |

**Why these values:**
- **800ms for financial**: Time to verify amounts before irreversible transfer
- **600ms for destructive**: Deliberation for permanent actions
- **200ms for standard**: Perceived "instant" with visual feedback
- **100ms for local**: No network latency to hide
- **0ms for high-freq**: Animation becomes friction at 50+/day
