Telemetry module

This lightweight telemetry module provides:

- `src/telemetry/emitter.js` — in-memory telemetry emitter with redact-on-ingest and a simple query API for tests and local analysis.
- `src/telemetry/redact.js` — minimal PII redaction helpers.
- `src/telemetry/backends/console.js` — default backend writing concise logs to console.

Usage (node):

```js
const { defaultTelemetry } = require('./src/telemetry/emitter')
const consoleBackend = require('./src/telemetry/backends/console')
defaultTelemetry.addBackend(consoleBackend)
defaultTelemetry.emit('story_start', { sessionId: 's1', userEmail: 'bob@example.com' })
```

Notes
- Redaction is intentionally conservative; extend `redact.js` for stricter rules.
- Buffer size defaults to 1000 events; override via `new Telemetry({bufferSize})` if needed.
