# Garbage Collection Protocol

Some capabilities create server-side state (OIDC clients, tokens, etc.). The GC protocol ensures this state is cleaned up when no longer needed.

## Overview

1. **Provider** creates state when fulfilling a need, keyed by `{origin}:{need_id}`
2. **Provider** periodically queries consumer's `/fort/needs` endpoint
3. If the need is no longer declared, provider can garbage collect the associated state

## Enabling GC

Capabilities that create persistent state should use async mode:

```nix
fort.host.capabilities.oidc-register = {
  handler = ./handlers/oidc-register;
  mode = "async";  # Enables state tracking and GC
};
```

## Provider State Tracking

When handling async capability requests, `fort-provider`:

1. Records the request in `/var/lib/fort/provider-state.json`
2. Structure: `{capability → {origin:need_id → {request, response?, updated_at}}}`
3. Response can be cached for re-delivery if consumer re-requests

## GC Process (Provider Side)

The provider runs a timer (`fort-provider-gc`) that:

1. Lists all state entries in `/var/lib/fort/provider-state.json`
2. For each `{origin, need_id}`, queries the origin's `/fort/needs`
3. If the need is still declared: keep the state
4. If the need is absent: eligible for GC (after grace period)

**Two Generals Safety**: Only delete on positive absence (200 OK with need not in list). Never delete on connection failure or timeout.

## Example: OIDC Client Lifecycle

1. **Declare**: Host A declares `fort.host.needs.oidc.myapp = { from = "idp"; ... }`
2. **Fulfill**: fort-consumer calls `oidc-register` on Identity Provider
3. **Create**: IP creates OIDC client, stores state keyed by `hostA:oidc-myapp`
4. **Poll**: IP timer queries Host A's `/fort/needs` - `oidc/myapp` present, keep state
5. **Remove**: Host A removes the need from its manifest, deploys
6. **GC**: IP timer sees `oidc/myapp` absent from needs, deletes OIDC client

## Debugging

Check declared needs on a host:

```bash
fort hostname needs
```

Check provider state:

```bash
cat /var/lib/fort/provider-state.json
```

Check consumer fulfillment state:

```bash
cat /var/lib/fort/fulfillment-state.json
```
