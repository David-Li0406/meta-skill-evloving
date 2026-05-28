<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright 2026 Edgecast Cloud LLC.
-->

# Phase 1: Analyze Restify API

**Standalone skill for analyzing a Node.js Restify API and creating a conversion plan.**

## Inputs

- **Source path**: Path to local checkout of Restify-based service
- **Service name**: (optional) Derived from path if not provided

## Outputs

- **Plan file**: `conversion-plans/<service>/plan.md`

## Tasks

### 1. Validate Source Path

Verify the path exists and contains a Restify service:
- Check for `package.json`
- Check for `lib/` directory (structure varies - may be `lib/endpoints/`, `lib/server/endpoints/`, or `lib/*.js`)

**Do not assume any specific structure** - always search the entire `lib/` tree recursively for route definitions.

### 2. Extract Service Metadata

From `package.json`:
- `name` - Use to derive service name (strip "sdc-" prefix if present)
- `version` - Use in generated Cargo.toml files

### 3. Read Endpoint Files

Search the entire `lib/` directory for route definitions. Different services use different patterns:

**Pattern 1 (vmapi-style):** Direct server methods
```javascript
server.get('/path', handler);
server.post('/path', handler);
```

**Pattern 2 (cnapi-style):** Via `attachTo(http, app)` function
```javascript
http.get({ path: '/path', name: 'Name' }, middleware, handler);
http.post({ path: '/path', name: 'Name' }, middleware, handler);
```

Search for files containing route definitions. The variable name varies by service:
- `server.get`, `server.post`, `server.put`, `server.del`, `server.patch`, `server.head` (vmapi, imgapi, papi)
- `http.get`, `http.post`, `http.put`, `http.del`, `http.patch` (cnapi)
- `sapi.get`, `sapi.post`, `sapi.put`, `sapi.del` (sapi - uses service name as variable)
- Other services may use different variable names - search for `\.(get|post|put|del|head)\(` pattern

Common locations (check ALL of these):
- `lib/endpoints/*.js` - vmapi, cnapi
- `lib/endpoints/**/*.js` - fwapi has subdirs like `rules/`, `firewalls/`
- `lib/server/endpoints/*.js` - sapi (nested under server/)
- `lib/*.js` - imgapi, cloudapi (routes directly in lib)

**Do not assume any specific structure** - search the entire `lib/` tree recursively.

**Note:** Some services mix variable names (e.g., fwapi uses both `server.get()` and `http.get()`).

For each endpoint, record:
- HTTP method
- Path (with parameters)
- Handler name
- Request body type (if POST/PUT/PATCH)
- Response type (array vs object/map - check carefully!)
- Query parameters

**Response type detection:** Don't assume list endpoints return arrays. Check the handler code:
- `res.json([...])` or `res.send(array)` → `Vec<T>`
- `res.json({key: value, ...})` → `HashMap<String, T>` or custom struct

### 4. Identify Route Conflicts

**CRITICAL:** Check for routes that will conflict in Dropshot.

Dropshot does not support having both a literal path segment and a variable at the same level:
```
GET /boot/default          # literal "default"
GET /boot/:server_uuid     # variable - CONFLICTS!
```

For each conflict found:
1. Document the conflicting routes
2. Recommend treating the literal as a special value (maintains API compatibility)
3. Mark as "RESOLVED" if there's a clear recommended approach, or "NEEDS DECISION" only if truly ambiguous

### 5. Analyze Action-Based Endpoints

For endpoints using the action dispatch pattern (single path handling multiple operations via query param):

1. **Enumerate all actions** from the handler's switch/if-else chain
2. **For each action, document:**
   - Action name
   - Required body fields
   - Optional body fields (look for `req.body.X || default` patterns)
   - Special values (e.g., `size: "remaining"`)
   - Idempotency options (`idempotent`, `sync`)

**Study the handler code carefully** - even "simple" actions like start/stop often have optional parameters.

### 6. Plan File Structure

Based on endpoint count and logical groupings:

**Small APIs (≤5 endpoints):** Single `lib.rs`

**Large APIs:** Split into modules:
```
apis/<service>-api/src/
├── lib.rs          # Re-exports and main trait
├── types.rs        # Shared types
├── <group1>.rs     # Types for endpoint group 1
└── ...
```

Group endpoints by:
- Source file they came from
- Resource type (e.g., vms, jobs, tasks)
- Logical function (e.g., health, admin)

#### 7. Check for WebSocket/Streaming Endpoints

Search for WebSocket or upgrade handling:
- `ws.on('connection', ...)` or similar WebSocket patterns
- `req.upgrade` or connection upgrade handling
- SSE (Server-Sent Events) endpoints

Document these separately - they need Dropshot `#[channel]` attributes.

### 8. Review Existing Clients/Tests for Field Accuracy

If an existing client exists (e.g., node-triton for cloudapi), review it for:
- Field names and types that differ from handler code assumptions
- Required vs optional fields
- Nested type structures

Test fixtures in `test/` directories are valuable sources of actual response shapes.

## 9. Write Plan File

Create `conversion-plans/<service>/plan.md`:

```markdown
# <Service> API Conversion Plan

## Source
- Path: <source-path>
- Version: <version>
- Package name: <npm-package-name>

## Endpoints Summary
- Total: <count>
- By method: GET: X, POST: Y, PUT: Z, DELETE: W
- Source files: <list>

## Endpoints Detail

### <group1> (from <source-file>)
| Method | Path | Handler | Notes |
|--------|------|---------|-------|
| GET | /resource | listResources | |
| GET | /resource/:id | getResource | |
...

### <group2> (from <source-file>)
...

## Route Conflicts

### Conflict 1: <path>
- Routes: `GET /boot/default` vs `GET /boot/:server_uuid`
- Recommended resolution: Treat "default" as special value
- **Status: RESOLVED** (or NEEDS DECISION if truly ambiguous)

## Action Dispatch Endpoints

### POST /vms/:uuid?action=<action>

**Common query parameters for all actions:**
- `sync` (optional): If `true`, wait for job completion before returning (default: `false`)

| Action | Required Fields | Optional Fields | Notes |
|--------|-----------------|-----------------|-------|
| start | (none) | idempotent | |
| stop | (none) | idempotent | |
| kill | (none) | signal, idempotent | signal defaults to SIGKILL |
| reboot | (none) | idempotent | |
| reprovision | image_uuid | | |
| update | (varies) | ram, cpu_cap, quota, ... | Many optional fields |
| add_nics | networks OR macs | | One of these required |
| update_nics | nics | | Array of NIC updates |
| remove_nics | macs | | Array of MAC addresses |
| create_snapshot | (none) | snapshot_name | Auto-generated if omitted |
| rollback_snapshot | snapshot_name | | |
| delete_snapshot | snapshot_name | | |
| create_disk | size | pci_slot, disk_uuid | size can be number or "remaining" |
| resize_disk | pci_slot, size | dangerous_allow_shrink | |
| delete_disk | pci_slot | | |
| migrate | (none) | migration_action, target_server_uuid, affinity | |

**Example usage:**
```bash
# Async (default) - returns immediately with job_uuid
POST /vms/{uuid}?action=start

# Sync - waits for job completion before returning
POST /vms/{uuid}?action=start&sync=true
```

## Planned File Structure
```
apis/<service>-api/src/
├── lib.rs
├── types.rs
└── <modules>
```

## Types to Define
- <list major request/response types>

## Field Naming Exceptions
- <list any fields that use snake_case instead of camelCase in the JSON API>
- Example: `triton_cns_enabled` (not `tritonCnsEnabled`)

## WebSocket/Channel Endpoints
- <list any WebSocket or streaming endpoints>

## Phase Status
- [x] Phase 1: Analyze - COMPLETE
- [ ] Phase 2: Generate API
- [ ] Phase 3: Generate Client
- [ ] Phase 4: Generate CLI
- [ ] Phase 5: Validate
```

## Success Criteria

Phase 1 is complete when:
- [ ] All endpoint files have been read
- [ ] Version extracted from package.json
- [ ] All route conflicts identified
- [ ] Action dispatch endpoints analyzed with field details
- [ ] WebSocket/channel endpoints identified
- [ ] Response types verified (array vs map for each list endpoint)
- [ ] Field naming exceptions documented
- [ ] File structure planned
- [ ] Plan file written to `conversion-plans/<service>/plan.md`

## Error Handling

If the source path doesn't exist or isn't a Restify service:
- Document the error in plan.md with status "FAILED"
- Return error to orchestrator

## After Phase Completion

The orchestrator will run:
```bash
make check
git add conversion-plans/<service>/plan.md
git commit -m "Add <service> conversion plan (Phase 1)"
```
