---
name: performance-pwa
description: Expert Performance Monitoring and PWA optimization.
---

# Performance & PWA Optimizer Skill

This skill enables the agent to maintain the application's speed, stability, and offline capabilities.

## Core Capabilities
- **Bundle Analysis**: Checking `vite.config.ts` for proper `manualChunks` splitting.
- **Service Worker Management**: Auditing `public/sw.js` (if exists) or PWA configuration to ensure assets are cached correctly.
- **Memory Safety**: Managing `localStorage` quotas and base64 string lifecycle (preventing QuotaExceededError).
- **Responsive Audit**: Ensuring "Mobile First" principles and correct CSS safe area insets.

## Performance Targets
- Lighthouse Score: >90 for Performance and PWA.
- Initial Load (FCP): <1.5s.
- Local Storage usage: <4MB (monitored via AIGenerationContext).

## Best Practices
- Use `React.lazy` for heavy pages (Studio, Profile).
- Compressed images before upload via `closetService`.
- Avoid layout shifts by using fixed aspect-ratio placeholders.
