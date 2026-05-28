# Supabase Realtime Overview

## Three realtime modes

- Postgres Changes: streams INSERT/UPDATE/DELETE events from Postgres via replication.
- Broadcast: low-latency, ephemeral messages between clients, REST, or from the database.
- Presence: shared user state (online, typing, cursor, etc.) per channel.

## When to choose which

- Postgres Changes: authoritative DB events; good when the database is the source of truth.
- Broadcast: high-frequency or ephemeral events (chat typing, cursors, game state). Prefer DB triggers + broadcast for scalable database-driven notifications.
- Presence: use sparingly for shared session state and user lists.

## Setup & constraints (server-side)

- Realtime must be enabled. Postgres Changes are disabled by default on new projects and require replication setup.
- To receive old records on UPDATE/DELETE, set `REPLICA IDENTITY FULL` on the table.
- RLS does not apply to DELETE statements; with RLS + REPLICA IDENTITY FULL, only primary keys are sent for deletes.
- Postgres Changes for private schemas require SELECT privileges for the role used by the client token.
- Broadcast is recommended for scalability and security; Postgres Changes is simpler but does not scale as well.

## Security

- Use RLS policies and private channels for broadcasted database messages.
- Never expose service role keys on the client.

## Channel naming

- Avoid `realtime` as the channel name.
- Prefer names that encode scope and entity, e.g. `room:123` or `topic:game:42`.
