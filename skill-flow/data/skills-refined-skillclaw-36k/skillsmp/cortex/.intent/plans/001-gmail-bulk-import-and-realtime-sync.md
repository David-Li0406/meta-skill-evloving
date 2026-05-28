## Goal

Replicate a user’s Gmail state into `comms.db` quickly and durably:

- **Fast bootstrap**: get “most of the mailbox” as quickly as possible
- **Complete history**: eventually ingest *all* messages (inbox + archive; exclude spam/trash unless explicitly requested)
- **Durable catch-up**: if the machine is off, we recover without losing changes
- **Near real-time**: when the machine is on, updates arrive quickly and trigger downstream actions
- **Resumable**: backfills survive restarts/crashes without redoing work
- **Transparent**: show progress, ETA, and guidance (including Takeout) when it’s going to take too long

Non-goals (for now):

- Full fidelity of every Gmail feature (e.g., filters, settings). We focus on messages + state transitions.
- Attachment blob storage (we can store metadata and optionally fetch blobs later).

## Why “Poke feels instant” (hypothesis + what it implies for us)

Most products that feel “instant” typically do a combination of:

- **OAuth + narrow initial fetch**: they fetch “recent” data first (last 7–30 days, or top N threads), then backfill in the background.
- **Aggressive indexing**: they immediately parse headers/bodies and build their own search index (embedding or keyword), so UX feels complete even if backfill is ongoing.
- **Parallelism + server-side infra**: they do backfill on their servers 24/7; your laptop going to sleep doesn’t pause the job.
- **History API / push**: they subscribe to updates so once bootstrapped, they rarely need a full scan again.
- **Higher effective quota**: not “special rate limits”, but:
  - they may use **Google Workspace** projects with billing/verification that improve quota ceilings,
  - they may use multiple projects/clients,
  - they may batch, cache, and retry well so they sustain near-limit throughput without falling over.

Implication: we should explicitly implement “fast recent first” + background backfill + durable change capture (History / PubSub).

## Product onboarding UX (what we want)

During onboarding for each Gmail account:

1. Start **immediate API sync** (recent-first) with a background backfill.
2. Compute a **rough size estimate** and an **ETA** (and show both).
3. If ETA exceeds ~4 hours (configurable), recommend **Google Takeout**:
   - show exactly where to go: `takeout.google.com`
   - explain that it’s a one-time bulk snapshot that can complete much faster than API crawling
4. Once the initial snapshot exists (API or Takeout), enable durable incremental updates (History API, optionally Pub/Sub).

## Data model direction (channel-agnostic)

We should extend `comms` in a way that is usable across all channels, not “Gmail-only”.

### Proposed universal message state fields

- **read state**: `read_at` (NULL = unread)
- **flagged**: starred/important/pinned equivalents
- **archived**: removed from primary view (Gmail archive; other channels can also “archive”)
- **status**: `draft | sent | received | failed | deleted` (channel may not support all)
- **tags**: general-purpose tagging (Gmail labels map cleanly)

Recommended representation:

- **Core**: keep `events` as the immutable “message occurrence”
- **State**: track mutable per-message state in a dedicated table, keyed by `event_id`
- **Tags**: many-to-many `event_tags`

This avoids contorting `events` into a mutable state machine while still enabling “latest state” queries.

### Gmail mapping to universal fields

- Gmail `UNREAD` label → `read_at = NULL` (or remove it to set read_at)
- Gmail `STARRED` / `IMPORTANT` → `flagged = true` (and/or tag)
- Gmail “archived” means “not in INBOX”:
  - option A: `archived = true` when INBOX absent
  - option B: represent INBOX presence as a tag; derive archived in queries
- Gmail `DRAFT` → `status = 'draft'`
- Gmail custom labels → `event_tags.tag = <label-name>`

Note: “mailboxes / hierarchy” can be treated as tags with namespaces:

- `gmail/system/INBOX`
- `gmail/system/SENT`
- `gmail/label/Receipts`

Or as generic:

- `inbox`, `sent`, `draft`, `label:Receipts`

We can decide the exact tag taxonomy later; core need is that it’s queryable and portable.

## Bulk ingestion options (initial snapshot)

### Option 1: API backfill (works today, slower)

We already have the month-by-month backfill approach. We should evolve it into:

- **Recent-first**: sync last 30–90 days first (fast UX)
- **Backfill in windows**: then go year/month windows until complete
- **Resumable cursor**: persist a cursor in `sync_watermarks` per adapter instance
- **Predictable throttling**: configurable `qps`, `workers`, and adaptive backoff on 429/403 rate limits

#### Progress + ETA

We need:

- a counter for:
  - windows completed
  - messages discovered
  - messages ingested
  - average msgs/sec over last N minutes
- ETA estimate:
  - remaining_windows / windows_per_minute (coarse)
  - or remaining_messages_estimate / msgs_per_sec (requires estimation strategy)

Estimation strategies:

- **Cheap**: during backfill, count thread IDs returned per window; sum remaining windows heuristically.
- **Better**: call Gmail profile (`messagesTotal`, `threadsTotal`) as a rough ceiling, then adjust based on query scope `in:anywhere -in:spam -in:trash` (may not match exactly).

### Option 2: Google Takeout + MBOX import (best bootstrap)

Takeout gives a “full dump” without API rate limiting:

- export Gmail as **MBOX**
- includes full bodies, attachments, and labels (depending on how Google packages them)

We implement:

`comms import mbox --account tyler@intent-systems.com --file <path> [--source takeout]`

Importer responsibilities:

- parse MBOX messages
- derive stable IDs:
  - best: Gmail `X-GM-MSGID` / `X-GM-THRID` if present
  - fallback: Message-ID header + date + from (less perfect)
- map to comms:
  - event content: subject/body
  - participants: from/to/cc
  - timestamp: Date header (plus received time if present)
  - tags/state: import labels (INBOX, SENT, etc.)
- commit in large transactions; use prepared statements; avoid per-row selects (raw SQL only)

Important: Takeout is a snapshot; after import we still need incremental capture (History API).

## Incremental updates (durable catch-up)

### Gmail History API (the primary mechanism)

Concept:

- Gmail maintains a monotonic `historyId`
- You store the last processed `historyId`
- You ask: “what changed since X?”

History returns:

- messagesAdded
- messagesDeleted
- labelsAdded / labelsRemoved

Implementation sketch:

- Store `gmail.history_id` in adapter watermark (`sync_watermarks.last_event_id` or a new typed field).
- On sync:
  1. read stored history id
  2. call `users.history.list` with `startHistoryId`
  3. apply changes in comms state tables
  4. store the newest history id seen

Durability:

- If machine is off for days: on next run, History API returns all changes since last `historyId` (within Gmail’s retention window).
- If `startHistoryId` is too old: API returns `404` / “historyId not found”; we must fall back to a rescan strategy (e.g., query last N days) and reset the baseline.

### Pub/Sub watch (optional “wake up”)

Gmail can push “mailbox changed” notifications to Pub/Sub.

Important: watch notifications do **not** contain all details; they mainly tell you:

- “something changed” + the newest `historyId`

So the durable logic is still “call History API and catch up”.

We can run:

- a long-running `comms watch` process (or integrate with `gogcli watch serve` if it provides useful plumbing)
- on notification: trigger the History catch-up sync for that account

## Background job architecture in comms (local-first)

We want an “optimal resumable background task” that can run unattended:

- `comms sync --adapter gmail-<acct> --full` should:
  - run recent-first snapshot if no baseline exists
  - then backfill windows until completion
  - continuously save cursor + perf stats

Add a “daemon-ish” mode:

- `comms sync --all --background`
- persists job state in SQLite (comms db) so it’s resumable
- exposes status:
  - `comms sync status`
  - prints per-adapter progress, ETA, last error, last run, current phase (recent/backfill/history)

Job state tables (proposal):

- `sync_jobs`:
  - job_id
  - adapter_name
  - phase (`recent|backfill|history`)
  - cursor (opaque string)
  - started_at, updated_at
  - last_error
  - counters json (for progress/eta)

We should keep this generic so Eve/AIX can use the same mechanism later.

## Raw SQL requirement

All querying and migrations are raw SQL. ORM models (structs) are fine for schema representation, but SQL remains the source of truth.

## Implementation plan (order of attack)

### Phase 0: Document + agreement (this file)

- Keep this plan as the single “north star” for Gmail bulk + realtime in comms.

### Phase 1: Background sync runner + ETA

- Add job state storage + status command
- Make Gmail adapter report progress counters (threads fetched, messages ingested, window cursor)
- Implement “recent-first” phase before month backfill
- Implement “ETA > 4 hours → suggest Takeout” messaging

### Phase 2: MBOX importer

- Add `comms import mbox` command
- Parse Takeout MBOX, map labels → tags/state
- Ensure deterministic IDs and idempotency (re-import safe)

### Phase 3: History API incremental sync

- Store `historyId` watermark per gmail adapter instance
- Implement history catch-up loop with resilience (handling invalid/expired historyId)

### Phase 4: Pub/Sub / watch integration (optional)

- Add `comms watch` that receives notifications and triggers history sync
- Make it robust to downtime and backpressure

### Phase 5: Event bus hooks (bridge to agents)

- Define an internal event stream interface (append-only)
- Emit “message.created/updated” events from adapters and importers
- Allow downstream “agent runners” to subscribe and take actions

## Open questions (to resolve during implementation)

- Canonical tag taxonomy (namespaced vs simple)
- Whether “archive” is derived from tags or stored as a boolean state
- Whether to store per-message labels as “current set” or as “label change events” (probably both: state + audit trail)
- Attachment handling (metadata now, blobs later)

