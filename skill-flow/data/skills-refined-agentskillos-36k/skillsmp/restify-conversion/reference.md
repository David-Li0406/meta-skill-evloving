<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright 2026 Edgecast Cloud LLC.
-->

# Restify to Dropshot Conversion Reference

This document contains detailed mapping rules and patterns for converting Node.js Restify APIs to Rust Dropshot traits.

## Mapping Rules

### HTTP Methods

Different Node.js services use different patterns for defining routes:

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

**Pattern 3 (sapi-style):** Uses service name as variable
```javascript
sapi.get({ path: '/path', name: 'Name' }, handler);
sapi.post({ path: '/path', name: 'Name' }, handler);
```

The variable name varies (`server`, `http`, `sapi`, etc.) but all map the same way:
- `.get(...)` → `method = GET`
- `.post(...)` → `method = POST`
- `.put(...)` → `method = PUT`
- `.del(...)` → `method = DELETE`
- `.patch(...)` → `method = PATCH`
- `.head(...)` → `method = HEAD` (papi uses this for some endpoints)

### Route Parameters
- Restify: `/path/:id` → Dropshot: `/path/{id}`
- Restify: `/users/:userId/posts/:postId` → Dropshot: `/users/{user_id}/posts/{post_id}`

### Parameter Types
- Route params (`req.params.id`) → `Path<PathStruct>`
- Query params (`req.query.foo`) → `Query<QueryStruct>`
- Request body (`req.body`) → `TypedBody<BodyStruct>`
- No params → Just `RequestContext<Self::Context>`

### Response Types
- JSON response (always 200) → `Result<HttpResponseOk<T>, HttpError>`
- Created (201) → `Result<HttpResponseCreated<T>, HttpError>`
- No content (204) → `Result<HttpResponseDeleted, HttpError>`
- HTML response → `Result<Response<Body>, HttpError>`
- Variable status code (e.g., health checks) → `Result<Response<Body>, HttpError>`

### Type Mapping (JS → Rust)
- `string` → `String`
- `number` (integer) → `i64` or `u64`
- `number` (float) → `f64`
- `boolean` → `bool`
- `Date` / ISO string → `String` (or `chrono::DateTime<Utc>` if using chrono)
- `any` / `object` → `serde_json::Value`
- `T[]` / `Array<T>` → `Vec<T>`
- `T | null` / `T | undefined` → `Option<T>`
- `{}` (key-value objects) → `std::collections::HashMap<String, T>`

**Don't assume list endpoints return arrays.** Check the handler:
- `res.json([...])` → `Vec<T>`
- `res.json({name: url, ...})` → `HashMap<String, String>` or custom type

**Don't assume all values are strings.** Tags/metadata may allow mixed types:
- `HashMap<String, String>` if values are always strings
- `HashMap<String, serde_json::Value>` if values can be strings, booleans, or numbers

## Route Conflicts (CRITICAL)

**Dropshot does not support having both a literal path segment and a variable path segment at the same level.**

**Problem Example:**
```
GET /boot/default          # literal "default"
GET /boot/:server_uuid     # variable server_uuid
```

**Solutions (in order of preference):**

### 1. Treat the literal as a special value (PREFERRED - maintains API compatibility)

Unify the routes and treat "default" as a valid value for the path parameter:
```rust
/// Path parameter that accepts either a UUID or "default"
#[derive(Debug, Deserialize, JsonSchema)]
pub struct BootParamsPath {
    /// Server UUID or "default" for default boot parameters
    pub server_uuid_or_default: String,
}

#[endpoint {
    method = GET,
    path = "/boot/{server_uuid_or_default}",
    tags = ["boot"],
}]
async fn get_boot_params(
    rqctx: RequestContext<Self::Context>,
    path: Path<BootParamsPath>,
) -> Result<HttpResponseOk<BootParams>, HttpError>;
```

**This preserves the original API paths** - clients can still call `/boot/default` or `/boot/<uuid>`.

### 2. Change path prefix (BREAKS API COMPATIBILITY - escalate to user)

Move one set of endpoints to a different path. **This breaks API compatibility and requires explicit user approval.** If option 1 cannot be used for any reason, the sub-agent must report this to the orchestrator, which must then ask the user for a decision before proceeding.

### 3. Merge endpoints if semantically equivalent

If the literal endpoint is just a convenience alias for a default value, merge them.

**Strongly prefer option 1** - it maintains full API compatibility. Only escalate to the user if option 1 is truly impossible.

## JSON Field Naming (API Compatibility)

The original Node.js API often uses camelCase in JSON responses, but **not always**. Check actual responses.

1. Use snake_case for Rust field names (idiomatic Rust)
2. Add `#[serde(rename_all = "camelCase")]` on structs **if** the API uses camelCase
3. For individual fields that differ, use `#[serde(rename = "originalName")]`

```rust
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct VmInfo {
    pub vm_uuid: String,        // Serializes as "vmUuid"
    pub owner_uuid: String,     // Serializes as "ownerUuid"
    #[serde(rename = "RAM")]    // Override for specific field
    pub ram: u64,
}
```

**Common exceptions to watch for:**
- Fields with hyphens: `role-tag` → `#[serde(rename = "role-tag")]`
- Fields that stay snake_case: `triton_cns_enabled`, `published_at`
- All-caps fields: `RAM`, `DNS`

Document these in the Phase 1 plan under "Field Naming Exceptions".

## UUID Handling (IMPORTANT Behavior Change)

**Node.js Triton services only accept lowercase UUIDs.** This is a strict requirement:
- `69cd99e2-eccc-11f0-88a8-17e540bad9e0` - Valid
- `69CD99E2-ECCC-11F0-88A8-17E540BAD9E0` - **Invalid** (rejected by Node.js)
- `69Cd99e2-eccc-11f0-88a8-17e540bad9e0` - **Invalid** (even one uppercase char)

**Rust's `uuid` crate follows Postel's Law** - be liberal in what you accept:
- **Parses** UUIDs in any case (uppercase, lowercase, mixed all work)
- **Always emits** UUIDs in lowercase hyphenated format

**This means Rust services will be MORE PERMISSIVE on input** while maintaining compatibility on output. This is an intentional, documented behavior change.

### Using uuid::Uuid

Prefer `uuid::Uuid` over `String` for UUID fields to get automatic parsing and validation:

```rust
use uuid::Uuid;

#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct VmPath {
    pub uuid: Uuid,  // Automatically parses any case, always serializes lowercase
}
```

When the Rust service makes calls to existing Node.js services, the uuid crate will emit lowercase UUIDs, maintaining compatibility.

### When UUIDs Accept Special Values

When a field accepts either a UUID or special string values (e.g., "default", "latest"), use an untagged enum instead of `String`:

```rust
use uuid::Uuid;

/// Accepts either a UUID or the literal "default"
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(untagged)]
pub enum UuidOrDefault {
    Uuid(Uuid),
    Special(SpecialValue),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "lowercase")]
pub enum SpecialValue {
    Default,
}
```

This approach:
- Validates UUIDs are properly formatted (and normalizes to lowercase)
- Only accepts the specific special values you define
- Rejects invalid inputs like typos ("defualt") at parse time
- Makes the API contract explicit in the OpenAPI spec

**Use plain `String` only when:**
- You need to preserve the original casing for logging/debugging
- The value is passed through without validation to another service

## Variable HTTP Status Codes

Some endpoints return different status codes based on conditions (e.g., 200 when healthy, 503 when unhealthy).

**Use `Response<Body>` for full control:**
```rust
use dropshot::Body;
use http::Response;

#[endpoint {
    method = GET,
    path = "/ping",
    tags = ["health"],
}]
async fn ping(
    rqctx: RequestContext<Self::Context>,
) -> Result<Response<Body>, HttpError>;
```

## Modeling Complex/Nested Objects

1. **Fully model** types that are part of the public API contract
2. **Use `serde_json::Value`** for:
   - Highly dynamic objects with unpredictable structure
   - Internal details that shouldn't be part of the API spec
   - Objects that are just passed through without inspection

```rust
// Fully modeled - stable API contract
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct VmNic {
    pub mac: String,
    pub ip: String,
    pub primary: bool,
}

// Dynamic/pass-through - use Value
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct VmDetails {
    pub uuid: String,
    /// Additional VM-specific fields (varies by brand)
    pub extra: serde_json::Value,
}
```

## Action Dispatch Pattern

Some APIs use an action-based pattern where a single endpoint handles multiple operations via a query parameter:

```
POST /vms/:uuid?action=start
POST /vms/:uuid?action=stop
POST /vms/:uuid?action=update    (body: {ram: 1024, ...})
POST /vms/:uuid?action=add_nics  (body: {nics: [...]})
```

### Recommended Approach

1. **API trait uses `serde_json::Value` for the body** - allows any JSON
2. **Define an Action enum** for the query parameter
3. **Define typed request structs FOR EVERY ACTION** in the API crate
4. **Implementation dispatches** based on action and deserializes appropriately
5. **Client library** depends on API crate and provides typed wrapper methods

```rust
// In API trait
#[derive(Debug, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum VmAction {
    Start,
    Stop,
    Update,
    AddNics,
    // ... all actions
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct VmActionQuery {
    pub action: VmAction,
}

// Typed request structs (exported for client use)
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct UpdateVmRequest {
    pub ram: Option<u64>,
    pub cpu_cap: Option<u32>,
}

// The endpoint accepts generic JSON body
#[endpoint {
    method = POST,
    path = "/vms/{uuid}",
    tags = ["vms"],
}]
async fn vm_action(
    rqctx: RequestContext<Self::Context>,
    path: Path<VmPath>,
    query: Query<VmActionQuery>,
    body: TypedBody<serde_json::Value>,
) -> Result<HttpResponseAccepted<JobResponse>, HttpError>;
```

### Action-Specific Request Body Types (CRITICAL)

**Every action needs a dedicated typed struct**, even actions that appear to take "no body". Study the original handler code carefully - most actions have optional parameters like `idempotent` or `sync`.

```rust
/// Request body for `start` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct StartVmRequest {
    /// If true, don't error if VM is already running
    #[serde(default)]
    pub idempotent: Option<bool>,
}

/// Request body for `stop` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct StopVmRequest {
    /// If true, don't error if VM is already stopped
    #[serde(default)]
    pub idempotent: Option<bool>,
}

/// Request body for `kill` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct KillVmRequest {
    /// Signal to send (default: SIGKILL). Examples: "SIGTERM", "SIGKILL"
    #[serde(default)]
    pub signal: Option<String>,
    /// If true, don't error if VM is already stopped
    #[serde(default)]
    pub idempotent: Option<bool>,
}

/// Request body for `reboot` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct RebootVmRequest {
    /// If true, don't error if VM is not running
    #[serde(default)]
    pub idempotent: Option<bool>,
}

/// Request body for `reprovision` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct ReprovisionVmRequest {
    /// Image UUID to reprovision with (required)
    pub image_uuid: String,
}

/// Request body for `create_snapshot` action
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct CreateSnapshotRequest {
    /// Snapshot name (optional, auto-generated if not provided)
    #[serde(default)]
    pub snapshot_name: Option<String>,
}

/// Request body for `create_disk` action (bhyve only)
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct CreateDiskRequest {
    /// Disk size in MB, or the literal "remaining" for remaining space
    pub size: serde_json::Value,  // Can be number or "remaining"
    /// PCI slot (optional, auto-assigned if not specified)
    #[serde(default)]
    pub pci_slot: Option<String>,
    /// Disk UUID (optional)
    #[serde(default)]
    pub disk_uuid: Option<String>,
}

/// Request body for `resize_disk` action (bhyve only)
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct ResizeDiskRequest {
    /// PCI slot of disk to resize
    pub pci_slot: String,
    /// New size in MB
    pub size: i64,
    /// Allow shrinking (dangerous operation)
    #[serde(default)]
    pub dangerous_allow_shrink: Option<bool>,
}
```

**Key insights:**
- Even "simple" actions like start/stop often have `idempotent` options
- Some fields accept multiple types (e.g., `size: number | "remaining"`) - use `serde_json::Value`
- Look for `req.body.X || default` patterns to find optional fields
- Document defaults in doc comments

### Client Library Pattern

The client crate depends on the API crate and provides typed wrappers. Since we cannot add impl blocks to Progenitor's generated `Client` type directly (Rust's orphan rule), we use a wrapper struct:

```rust
// clients/internal/vmapi-client/src/lib.rs
include!(concat!(env!("OUT_DIR"), "/client.rs"));

// Re-export action enum and request types from API crate
pub use vmapi_api::{VmAction, UpdateVmRequest, AddNicsRequest, ...};

/// Typed wrapper around Progenitor's Client for action-based APIs
pub struct TypedClient {
    inner: Client,
}

impl TypedClient {
    pub fn new(base_url: &str) -> Self {
        Self { inner: Client::new(base_url) }
    }

    /// Access the underlying Progenitor client for non-wrapped methods
    pub fn inner(&self) -> &Client {
        &self.inner
    }

    pub async fn start_vm(&self, uuid: &str) -> Result<types::AsyncJobResponse, Error<types::Error>> {
        self.inner.vm_action()
            .uuid(uuid)
            .action(vmapi_api::VmAction::Start)
            .body(serde_json::json!({}))
            .send()
            .await
            .map(|r| r.into_inner())  // Unwrap ResponseValue<T>
    }

    pub async fn update_vm(
        &self,
        uuid: &str,
        request: &vmapi_api::UpdateVmRequest,
    ) -> Result<types::AsyncJobResponse, Error<types::Error>> {
        self.inner.vm_action()
            .uuid(uuid)
            .action(vmapi_api::VmAction::Update)
            .body(serde_json::to_value(request).unwrap_or_default())
            .send()
            .await
            .map(|r| r.into_inner())
    }
}
```

## Example Conversion

### Input (Node.js Restify)
```javascript
server.get('/users/:id', async (req, res, next) => {
    const user = await getUser(req.params.id);
    res.json(user);
});

server.post('/users', async (req, res, next) => {
    const user = await createUser(req.body);
    res.status(201).json(user);
});
```

### Output (Dropshot Trait)
```rust
use dropshot::{HttpError, HttpResponseCreated, HttpResponseOk, Path, RequestContext, TypedBody};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, JsonSchema)]
pub struct UserPath {
    pub id: String,
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct CreateUserRequest {
    pub name: String,
    pub email: String,
}

#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct User {
    pub id: String,
    pub name: String,
    pub email: String,
}

#[dropshot::api_description]
pub trait UsersApi {
    type Context: Send + Sync + 'static;

    /// Get a user by ID
    #[endpoint {
        method = GET,
        path = "/users/{id}",
        tags = ["users"],
    }]
    async fn get_user(
        rqctx: RequestContext<Self::Context>,
        path: Path<UserPath>,
    ) -> Result<HttpResponseOk<User>, HttpError>;

    /// Create a new user
    #[endpoint {
        method = POST,
        path = "/users",
        tags = ["users"],
    }]
    async fn create_user(
        rqctx: RequestContext<Self::Context>,
        body: TypedBody<CreateUserRequest>,
    ) -> Result<HttpResponseCreated<User>, HttpError>;
}
```

## Using Enums vs Strings

When a field has a fixed set of known values, prefer an enum:

```rust
// Good - typed enum
#[derive(Debug, Clone, Copy, Serialize, Deserialize, JsonSchema, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum Brand {
    Bhyve,
    Joyent,
    #[serde(rename = "joyent-minimal")]
    JoyentMinimal,
    Kvm,
    Lx,
}

// Use in struct
pub struct Machine {
    pub brand: Brand,  // Not String
}
```

Use `String` only when:
- The set of values is truly unbounded
- New values are added frequently and backward compatibility matters
- The field is rarely used for logic

## Checklist

Before completing any phase, verify:

**API Trait:**
- [ ] License header is present
- [ ] All necessary imports are included
- [ ] Types are defined before the trait
- [ ] All types have appropriate derives
- [ ] Path parameters use `{param}` syntax (not `:param`)
- [ ] **No route conflicts** - if conflicts exist, resolve using the "special value" pattern
- [ ] Each endpoint has a doc comment
- [ ] Tags are meaningful and consistent
- [ ] Optional fields use `Option<T>` with `#[serde(default)]`
- [ ] JSON field names match original API (check for exceptions!)
- [ ] Variable status code endpoints use `Response<Body>` return type
- [ ] Action dispatch endpoints use `serde_json::Value` body with typed request structs exported
- [ ] WebSocket/channel endpoints use `#[channel]` attribute

**Build Order (CRITICAL):**
- [ ] API crate builds successfully BEFORE proceeding to client
- [ ] OpenAPI spec generated successfully BEFORE proceeding to client
- [ ] All client files created BEFORE adding to workspace
- [ ] All CLI files created BEFORE adding to workspace

**For Action-Dispatch Patterns:**
- [ ] Action enum exported from API crate
- [ ] **Every action has a dedicated typed request struct** (even "no-body" actions like start/stop)
- [ ] Optional fields like `idempotent`, `sync`, `signal` are captured
- [ ] Special value types handled (e.g., `size: number | "remaining"` → `serde_json::Value`)
- [ ] Doc comments document defaults and valid values
- [ ] Typed request structs exported from API crate
- [ ] Client re-exports action enum and request types
- [ ] Typed wrapper methods use builder pattern
- [ ] Wrapper methods unwrap ResponseValue with `.map(|r| r.into_inner())`
