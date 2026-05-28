<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright 2026 Edgecast Cloud LLC.
-->

# Phase 3: Generate Client Library

**Standalone skill for generating the Progenitor client library.**

## Inputs

- **Service name**: Name of the service (e.g., "vmapi")
- **Plan file**: `conversion-plans/<service>/plan.md`

## Outputs

- **Client crate**: `clients/internal/<service>-client/`
- **Updated plan file** with Phase 3 status

## Prerequisites

- Phase 2 complete
- OpenAPI spec exists at `openapi-specs/generated/<service>-api.json`

## Tasks

### 1. Create All Client Files FIRST

**IMPORTANT:** Create ALL files before adding to workspace to avoid build failures.

```
clients/internal/<service>-client/
├── Cargo.toml
├── build.rs
└── src/
    └── lib.rs
```

### 2. Create Cargo.toml

```toml
[package]
name = "<service>-client"
version = "<version-from-plan>"
edition.workspace = true
description = "<Service> client library (Progenitor-generated)"

[lib]
name = "<service>_client"
path = "src/lib.rs"

[dependencies]
progenitor-client = { workspace = true }
reqwest = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
<service>-api = { path = "../../../apis/<service>-api" }

[build-dependencies]
progenitor = { workspace = true }
serde_json = { workspace = true }
openapiv3 = { workspace = true }
```

### 3. Create build.rs

```rust
use progenitor::GenerationSettings;
use std::env;
use std::path::Path;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let out_dir = env::var("OUT_DIR")?;
    let spec_path = "../../../openapi-specs/generated/<service>-api.json";

    assert!(Path::new(spec_path).exists(), "{spec_path} does not exist!");
    println!("cargo:rerun-if-changed={}", spec_path);

    let spec = std::fs::read_to_string(spec_path)?;
    let openapi: openapiv3::OpenAPI = serde_json::from_str(&spec)?;

    let mut settings = GenerationSettings::default();
    settings
        .with_interface(progenitor::InterfaceStyle::Builder)
        .with_tag(progenitor::TagStyle::Merged);

    let tokens = progenitor::Generator::new(&settings).generate_tokens(&openapi)?;
    std::fs::write(format!("{}/client.rs", out_dir), tokens.to_string())?;

    println!("Generated client from OpenAPI spec: {}", spec_path);
    Ok(())
}
```

### 4. Create src/lib.rs

**First, read the API crate to find exact type names to re-export.**

```rust
//! <Service> Client Library
//!
//! This client provides typed access to the <Service> API.

include!(concat!(env!("OUT_DIR"), "/client.rs"));

// Re-export types from the API crate.
// VERIFY these names match apis/<service>-api/src/*.rs exactly!
pub use <service>_api::{
    // Path parameter structs
    // Query parameter structs
    // Request body structs
    // Response structs
    // Action enums (if action-dispatch pattern)
};
```

### 5. Add Typed Wrapper Methods (REQUIRED for action-dispatch pattern)

**If the API uses `?action=` query parameters, you MUST add typed wrapper methods.**

This is critical for usability - without wrappers, callers must manually construct JSON bodies and remember action names.

**Read the API crate's action types file** (e.g., `apis/<service>-api/src/types/actions.rs`) to enumerate all actions and their request types.

**Template for typed client wrapper:**

```rust
// Wrapper struct - required because we cannot impl on Progenitor's Client directly
pub struct TypedClient {
    inner: Client,
}

impl TypedClient {
    /// Create a new typed client wrapper
    pub fn new(base_url: &str) -> Self {
        Self {
            inner: Client::new(base_url),
        }
    }

    /// Access the underlying Progenitor client for non-wrapped methods
    pub fn inner(&self) -> &Client {
        &self.inner
    }

    /// Start a VM
    ///
    /// # Arguments
    /// * `uuid` - VM UUID
    /// * `idempotent` - If true, don't error if already running
    pub async fn start_vm(
        &self,
        uuid: &str,
        idempotent: bool,
    ) -> Result<types::AsyncJobResponse, Error<types::Error>> {
        let body = <service>_api::StartVmRequest {
            idempotent: if idempotent { Some(true) } else { None },
        };
        self.inner.vm_action()
            .uuid(uuid)
            .action(<service>_api::VmAction::Start)
            .body(serde_json::to_value(&body).unwrap_or_default())
            .send()
            .await
            .map(|r| r.into_inner())
    }

    /// Stop a VM
    pub async fn stop_vm(
        &self,
        uuid: &str,
        idempotent: bool,
    ) -> Result<types::AsyncJobResponse, Error<types::Error>> {
        let body = <service>_api::StopVmRequest {
            idempotent: if idempotent { Some(true) } else { None },
        };
        self.inner.vm_action()
            .uuid(uuid)
            .action(<service>_api::VmAction::Stop)
            .body(serde_json::to_value(&body).unwrap_or_default())
            .send()
            .await
            .map(|r| r.into_inner())
    }

    /// Update VM properties
    ///
    /// Takes a typed request struct with all updateable fields.
    pub async fn update_vm(
        &self,
        uuid: &str,
        request: &<service>_api::UpdateVmRequest,
    ) -> Result<types::AsyncJobResponse, Error<types::Error>> {
        self.inner.vm_action()
            .uuid(uuid)
            .action(<service>_api::VmAction::Update)
            .body(serde_json::to_value(request).unwrap_or_default())
            .send()
            .await
            .map(|r| r.into_inner())
    }

    // ... MUST add one wrapper per action in the VmAction enum
}
```

**Wrapper requirements:**
- One method per action enum variant (no exceptions)
- Use the typed request struct from the API crate
- Include doc comments with parameter descriptions
- Common parameters (like `idempotent`) should be explicit function parameters
- Complex requests (like `update`) should take the full request struct

### 6. Add to Workspace

**Only after ALL files exist**, edit root `Cargo.toml`:

```toml
members = [
    # ... existing
    "clients/internal/<service>-client",
]
```

### 7. Build Client

```bash
make format package-build PACKAGE=<service>-client
```

Common errors:
- Wrong type names in re-exports (read API crate source!)
- Missing dependency on API crate

### 8. Update Plan File

Add to `conversion-plans/<service>/plan.md`:

```markdown
## Phase 3 Complete

- Client crate: `clients/internal/<service>-client/`
- Build status: SUCCESS
- Typed wrappers: <YES/NO - list if yes>

## Phase Status
- [x] Phase 1: Analyze - COMPLETE
- [x] Phase 2: Generate API - COMPLETE
- [x] Phase 3: Generate Client - COMPLETE
- [ ] Phase 4: Generate CLI
- [ ] Phase 5: Validate
```

## Success Criteria

Phase 3 is complete when:
- [ ] All client files created before workspace addition
- [ ] Cargo.toml has API crate dependency
- [ ] build.rs points to correct spec path
- [ ] lib.rs re-exports verified type names
- [ ] **Typed wrapper methods added for ALL actions** (if action-dispatch pattern)
- [ ] Added to workspace Cargo.toml
- [ ] `make format package-build PACKAGE=<service>-client` succeeds
- [ ] Plan file updated

**Action-Dispatch Checklist** (if applicable):
- [ ] Read API crate's action enum to enumerate all actions
- [ ] One wrapper method per action variant
- [ ] Each wrapper uses the corresponding typed request struct
- [ ] Wrappers documented with parameter descriptions
- [ ] All action request types re-exported from client

## Error Handling

If build fails:
- Document specific errors in plan.md
- Common fix: verify re-export type names against API crate
- Set Phase 3 status to "FAILED: <reason>"

## After Phase Completion

The orchestrator will run:
```bash
make check
git add clients/internal/<service>-client/ conversion-plans/<service>/plan.md Cargo.toml Cargo.lock
git commit -m "Add <service> client library (Phase 3)"
```
