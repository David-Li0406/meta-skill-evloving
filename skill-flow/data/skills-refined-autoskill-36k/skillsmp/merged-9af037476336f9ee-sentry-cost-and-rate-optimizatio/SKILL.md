---
name: sentry-cost-and-rate-optimization
description: Use this skill when managing Sentry costs and optimizing event volume to avoid rate limits and reduce expenses.
---

# Sentry Cost and Rate Optimization

## Prerequisites

- Understanding of current event volume and Sentry billing plan
- High-volume endpoints and error sources identified
- Noisy error patterns documented
- Cost reduction targets defined

## Instructions

1. Check current usage and cost breakdown via Sentry API or dashboard stats.
2. Implement error sampling with `sampleRate` to reduce volume (e.g., 50% for non-critical errors).
3. Configure dynamic transaction sampling with `tracesSampler` (1% or lower for high-volume).
4. Add `ignoreErrors` and `denyUrls` patterns for common noisy errors.
5. Enable server-side and client-side inbound filters in project settings.
6. Set project rate limits via API or dashboard to cap maximum events.
7. Reduce event size with `maxValueLength` and `maxBreadcrumbs` limits.
8. Disable unused features (e.g., replays, profiling) if not needed.
9. Configure tiered environment settings (disable in dev, reduce in staging).
10. Monitor event volume and set up spend alerts and quota alerts.

## Output
- Optimized sample rates configured
- Rate limiting and event filtering rules applied
- Cost projection updated
- Spend alerts configured

## Error Handling

See `{baseDir}/references/errors.md` for comprehensive error handling.

## Examples

See `{baseDir}/references/examples.md` for detailed examples.

## Resources
- [Sentry Pricing](https://sentry.io/pricing/)
- [Sentry Quota Management](https://docs.sentry.io/product/accounts/quotas/)
- [Sampling Strategies](https://docs.sentry.io/platforms/javascript/configuration/sampling/)