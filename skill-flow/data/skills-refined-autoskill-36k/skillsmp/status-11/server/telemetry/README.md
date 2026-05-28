Telemetry receiver (dev prototype)

Purpose
-------
Lightweight development receiver that accepts POSTed JSON events and persists director decision telemetry for local analysis.

What it does
------------
- Accepts POST requests to `/` with a JSON body.
- Validates that the event represents a `director_decision` (accepts payloads with `type: "director_decision"` or same under `event_type` or `event.type`).
- Appends accepted events as NDJSON lines to `server/telemetry/events.ndjson` (dev ingestion store).

Run locally
-----------
```bash
# starts the receiver on port 4005 by default
node server/telemetry/receiver.js

# to choose a different port (useful in tests):
PORT=0 node server/telemetry/receiver.js
```

The process prints the listening URL to stdout when ready, e.g. `Telemetry receiver listening on http://localhost:4005/`.

API (single endpoint)
---------------------
- POST /
  - Content-Type: application/json
  - Body: arbitrary JSON representing an event
  - Success (200): when the payload identifies as a `director_decision` and was persisted
  - Client error (400): when payload is invalid JSON or not a supported event type
  - Server error (500): when writing to storage failed

Example payload (director_decision)
----------------------------------
```json
{
  "type": "director_decision",
  "proposal_id": "p1",
  "decision": "approve",
  "riskScore": 0.12,
  "reason": "low_risk",
  "metrics": { "latencyMs": 120 }
}
```

Curl example
------------
```bash
curl -X POST http://localhost:4005/ \
  -H 'Content-Type: application/json' \
  -d '{"type":"director_decision","proposal_id":"p1","decision":"approve","riskScore":0.12}'
```

Inspecting persisted events
---------------------------
Events are appended to `server/telemetry/events.ndjson` as one JSON object per line. To inspect recent events:

```bash
tail -n 50 server/telemetry/events.ndjson | jq .
```

Development notes
-----------------
- This receiver is intentionally small and intended for dev/testing only. Production work (SQLite storage, schema validation, auth/token protection, log rotation) is tracked in `ge-apq.1` and should be implemented before using this in production.
- The receiver uses `server/telemetry/backend-ndjson.js` as the storage backend; swap or extend backends as needed.
