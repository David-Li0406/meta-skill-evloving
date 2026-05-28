<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright 2026 Edgecast Cloud LLC.
-->

# Phase 5: Validate Conversion

**Standalone skill for validating the Rust conversion against the original Node.js service.**

## Purpose

Compare the generated Rust API trait, client, and CLI against the original Node.js Restify implementation to identify:
- Missing endpoints
- Type mismatches
- Behavioral differences
- API compatibility issues

## Inputs

- **Service name**: Name of the service (e.g., "vmapi")
- **Source path**: Path to original Node.js service
- **Plan file**: `conversion-plans/<service>/plan.md`

## Outputs

- **Validation report**: `conversion-plans/<service>/validation.md`
- **Updated plan file** with Phase 5 status

## Prerequisites

- Phases 1-4 complete
- All crates build successfully

## Validation Tasks

### 1. Endpoint Coverage Check

Compare endpoints in the original Node.js service against the generated API trait:

**Read from Node.js:**
Search `lib/` for route definitions using either pattern:
- `server.get/post/put/del/patch` (vmapi-style)
- `http.get/post/put/del/patch` via `attachTo()` (cnapi-style)

Common locations: `lib/endpoints/*.js`, `lib/*.js`

**Read from Rust:**
- `apis/<service>-api/src/lib.rs` - API trait endpoints

**Check:**
- [ ] Every Node.js endpoint has a corresponding Rust endpoint
- [ ] HTTP methods match
- [ ] Paths match (accounting for `:param` → `{param}` conversion)
- [ ] Query parameters are captured

### 2. Type Completeness Check

For each endpoint, compare request/response types:

**From Node.js:**
- Look at handler implementations for `res.json()` calls
- Check any TypeScript types or JSDoc annotations
- Review test fixtures in `test/` directory

**From Rust:**
- Check struct definitions in `apis/<service>-api/src/`

**Check:**
- [ ] All response fields are present
- [ ] Field types are compatible (string→String, number→i64/u64/f64, etc.)
- [ ] Optional fields are marked as `Option<T>`
- [ ] Arrays are `Vec<T>`

### 3. Route Conflict Resolution Verification

Review any route conflicts identified in Phase 1:

**Check:**
- [ ] Conflicts were resolved correctly
- [ ] API paths remain compatible (clients can still call original paths)
- [ ] Documentation explains the resolution

### 4. CLI Command Coverage

Compare CLI commands against API endpoints:

**Check:**
- [ ] Every API endpoint has a CLI command
- [ ] Action-dispatch endpoints have individual action commands
- [ ] Nested resources have appropriate subcommands

### 5. Behavioral Analysis

Review handler implementations for behaviors that may need special handling:

**Look for in Node.js:**
- Conditional responses (different status codes based on state)
- Side effects (writes to other services, job creation)
- Pagination patterns
- Error response formats
- Authentication/authorization checks

**Document:**
- Behaviors that need implementation attention
- Patterns that differ from standard CRUD

### 6. API Compatibility Assessment

Assess overall API compatibility:

**Check:**
- [ ] JSON field names match (camelCase preserved via serde)
- [ ] HTTP status codes match expected behavior
- [ ] Error response format is compatible
- [ ] Query parameter names match

## Validation Report Format

Create `conversion-plans/<service>/validation.md`:

```markdown
# <Service> Conversion Validation Report

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Endpoint Coverage | ✅/⚠️/❌ | X of Y endpoints |
| Type Completeness | ✅/⚠️/❌ | X issues |
| Route Conflicts | ✅/⚠️/❌ | X conflicts resolved |
| CLI Coverage | ✅/⚠️/❌ | X of Y commands |
| API Compatibility | ✅/⚠️/❌ | X concerns |

## Endpoint Coverage

### ✅ Converted Endpoints
| Node.js | Rust | Notes |
|---------|------|-------|
| `GET /vms` | `list_vms` | |
| `GET /vms/:uuid` | `get_vm` | |
...

### ❌ Missing Endpoints
| Node.js | Reason |
|---------|--------|
| `GET /debug/...` | Internal debugging endpoint, intentionally omitted |
...

## Type Analysis

### ✅ Complete Types
- `Vm` - All fields mapped
- `Job` - All fields mapped

### ⚠️ Partial Types
- `VmDetails` - Using `serde_json::Value` for `extra` field (dynamic content)

### ❌ Missing Types
- None

## Route Conflict Resolutions

### Conflict 1: `/boot/default` vs `/boot/{server_uuid}`
- **Resolution**: Unified as `/boot/{server_uuid_or_default}`
- **Compatibility**: ✅ Original paths still work
- **Documentation**: Added to API docs

## CLI Command Analysis

### ✅ Implemented Commands
- `<service> list` → `GET /resources`
- `<service> get <id>` → `GET /resources/{id}`
...

### ❌ Missing Commands
- None

## Behavioral Notes

### Pagination
- Node.js uses `?offset=N&limit=M` pattern
- Rust API preserves this in query parameters

### Error Responses
- Node.js returns `{ code: "...", message: "..." }`
- Rust HttpError provides similar structure

### Special Behaviors
1. **Job creation**: POST endpoints return 202 with job UUID
2. **Sync mode**: `?sync=true` waits for job completion

## Recommendations

### High Priority
1. [ ] Add integration tests comparing responses
2. [ ] ...

### Medium Priority
1. [ ] Consider typed error responses
2. [ ] ...

### Low Priority
1. [ ] Add OpenAPI examples from real responses
2. [ ] ...

## Conclusion

**Overall Status**: ✅ READY FOR TESTING / ⚠️ NEEDS ATTENTION / ❌ INCOMPLETE

<Summary of conversion quality and any blocking issues>
```

## Success Criteria

Phase 5 is complete when:
- [ ] All endpoints compared
- [ ] Type coverage analyzed
- [ ] Route conflict resolutions verified
- [ ] CLI commands verified
- [ ] Behavioral notes documented
- [ ] Recommendations provided
- [ ] Validation report written
- [ ] Plan file updated with final status

## Final Plan Update

Add to `conversion-plans/<service>/plan.md`:

```markdown
## Phase 5 Complete - CONVERSION VALIDATED

- Validation report: `conversion-plans/<service>/validation.md`
- Overall status: <READY/NEEDS ATTENTION/INCOMPLETE>
- Endpoint coverage: X/Y (Z%)
- Issues found: <count>

## Phase Status
- [x] Phase 1: Analyze - COMPLETE
- [x] Phase 2: Generate API - COMPLETE
- [x] Phase 3: Generate Client - COMPLETE
- [x] Phase 4: Generate CLI - COMPLETE
- [x] Phase 5: Validate - COMPLETE

## Conversion Complete

The <service> API has been converted to Rust. See validation.md for details.

### Generated Artifacts
- API crate: `apis/<service>-api/`
- Client crate: `clients/internal/<service>-client/`
- CLI crate: `cli/<service>-cli/`
- OpenAPI spec: `openapi-specs/generated/<service>-api.json`

### Next Steps
1. Run integration tests against live Node.js service
2. Address any issues in validation report
3. Deploy Rust service for parallel testing
```

## After Phase Completion

The orchestrator will run:
```bash
make check
git add conversion-plans/<service>/
git commit -m "Add <service> validation report (Phase 5 - conversion complete)"
```
