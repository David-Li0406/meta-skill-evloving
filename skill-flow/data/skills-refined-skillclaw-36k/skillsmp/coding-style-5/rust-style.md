# Rust Style Guide

## Building & Running

### WSL with Windows Filesystem
When building on WSL with a Windows filesystem (paths like `/mnt/a/` or `a:\`), use `CARGO_TARGET_DIR` to avoid cross-filesystem linking errors:

```bash
export CARGO_TARGET_DIR="/tmp/cargo-target"
cargo run -p sc-interdiction -- dashboard --location Crusader
```

This redirects build artifacts to a native Linux path, avoiding "Operation not permitted" errors when Cargo tries to link files across filesystems.

---

## Project Structure

### Workspace Organization
```
project/
├── Cargo.toml              # Workspace root
├── crates/
│   ├── core/               # Core library
│   ├── formats/            # File format parsers
│   │   ├── dcx/
│   │   ├── bnd4/
│   │   └── flver/
│   └── cli/                # Command-line tool
└── tests/                  # Integration tests
```

### Workspace Cargo.toml
```toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT OR Apache-2.0"

[workspace.dependencies]
thiserror = "1.0"
zerocopy = { version = "0.8", features = ["derive"] }
byteorder = "1.5"

[workspace.lints.clippy]
unwrap_used = "warn"
doc_markdown = "warn"
undocumented_unsafe_blocks = "warn"
ptr_as_ptr = "warn"
ptr_cast_constness = "warn"
```

### Crate Cargo.toml
```toml
[package]
name = "my-crate"
version.workspace = true
edition.workspace = true

[dependencies]
thiserror.workspace = true

[lints]
workspace = true
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `world_chr_man`, `bullet_ins` |
| Types/Structs | PascalCase | `WorldChrMan`, `BulletIns` |
| Functions | snake_case | `get_row()`, `find_table()` |
| Constants | SCREAMING_SNAKE | `MAX_BUFFER_SIZE` |
| Game prefixes | CS, World, Field | `CSBulletIns`, `WorldAreaChr` |
| Unknown fields | unk + offset | `unk50`, `unk_0x54` |

---

## Error Handling

### Use thiserror for Error Types
```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ParseError {
    #[error("Invalid magic bytes: expected {expected:?}, got {actual:?}")]
    InvalidMagic {
        expected: [u8; 4],
        actual: [u8; 4],
    },

    #[error("Invalid value at offset {offset:#x}: expected {expected}, got {actual}")]
    InvalidValue {
        offset: u64,
        expected: u64,
        actual: u64,
    },

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Decompression failed: {0}")]
    Decompress(#[from] DecompressError),
}
```

### Helper Constructors on Error Types
```rust
impl ParseError {
    pub fn invalid_value<S: io::Seek>(expected: u64, actual: u64, stream: &mut S) -> Self {
        Self::InvalidValue {
            offset: stream.stream_position().unwrap_or(0),
            expected,
            actual,
        }
    }
}
```

### Use eyre for Application Code
```rust
// In binaries/CLI tools
use eyre::{Result, WrapErr};

fn main() -> Result<()> {
    let config = load_config()
        .wrap_err("Failed to load configuration")?;

    process(&config)
        .wrap_err_with(|| format!("Failed to process {}", config.path))?;

    Ok(())
}
```

---

## Binary Format Parsing

### Zero-Copy with zerocopy
```rust
use zerocopy::{FromBytes, FromZeroes, Ref, U32, U64, LE};

#[derive(Debug, Clone, FromBytes, FromZeroes)]
#[repr(C, packed)]
pub struct Header<O: ByteOrder = LE> {
    pub magic: [u8; 4],
    pub version: U32<O>,
    pub file_size: U64<O>,
    pub entry_count: U32<O>,
    _padding: [u8; 4],
}

impl Header {
    pub fn from_bytes(bytes: &[u8]) -> Result<Ref<&[u8], Self>, ParseError> {
        Ref::new_from_prefix(bytes)
            .map(|(header, _)| header)
            .ok_or(ParseError::BufferTooSmall)
    }
}
```

### Generic ByteOrder Support
```rust
use byteorder::{ByteOrder, LE, BE};
use zerocopy::U32;

#[derive(FromBytes)]
#[repr(C, packed)]
pub struct Entry<O: ByteOrder = LE> {
    pub id: U32<O>,
    pub offset: U32<O>,
    pub size: U32<O>,
}

// Usage
let entry: Entry<LE> = parse_le(bytes)?;
let entry: Entry<BE> = parse_be(bytes)?;
```

---

## Statics and Lazy Initialization

### Use LazyLock (not lazy_static or OnceCell)
```rust
use std::sync::LazyLock;

static PATTERNS: LazyLock<Vec<Pattern>> = LazyLock::new(|| {
    vec![
        Pattern::new("*.dcx"),
        Pattern::new("*.bnd"),
    ]
});

static CONFIG: LazyLock<Config> = LazyLock::new(Config::load);

// For Windows module base
static MODULE_BASE: LazyLock<NonNull<u8>> = LazyLock::new(|| {
    let handle = unsafe { GetModuleHandleW(PCWSTR::null()) }
        .expect("GetModuleHandleW failed");
    NonNull::new(handle.0 as *mut u8).expect("null module handle")
});
```

---

## Unsafe Code

### Always Document Safety
```rust
/// Returns the module base address.
///
/// # Safety
/// This function is safe to call from any thread after module initialization.
pub fn module_base() -> NonNull<u8> {
    // SAFETY: GetModuleHandleW with null returns the current module,
    // which is always valid after the module is loaded.
    let handle = unsafe { GetModuleHandleW(PCWSTR::null()) }
        .expect("GetModuleHandleW failed");

    NonNull::new(handle.0 as *mut u8).expect("null module handle")
}

pub fn read_at<T: FromBytes>(offset: usize) -> T {
    // SAFETY: Caller guarantees offset is within valid memory and aligned for T.
    unsafe { std::ptr::read(base.as_ptr().add(offset) as *const T) }
}
```

---

## Procedural Macros

### Attribute Macros for Boilerplate
```rust
// Definition in proc-macro crate
#[proc_macro_attribute]
pub fn singleton(args: TokenStream, input: TokenStream) -> TokenStream {
    let struct_def = parse_macro_input!(input as ItemStruct);
    let name = parse_macro_input!(args as LitStr).value();
    let ident = &struct_def.ident;

    quote! {
        #struct_def

        impl crate::DLRFSingleton for #ident {
            const NAME: &'static str = #name;
        }
    }.into()
}

// Usage
#[singleton("WorldChrMan")]
pub struct WorldChrMan {
    // ...
}
```

---

## Testing

### Integration Tests Over Unit Tests
```
tests/
├── common/
│   └── mod.rs          # Shared test utilities
├── parse_dcx.rs        # DCX parsing tests
├── parse_bnd.rs        # BND parsing tests
└── fixtures/           # Test data files
    ├── valid.dcx
    └── corrupted.dcx
```

### Test Structure
```rust
// tests/parse_dcx.rs
mod common;

use common::{load_fixture, FIXTURE_DIR};

#[test]
fn parse_valid_dcx() {
    let bytes = load_fixture("valid.dcx");
    let result = dcx::parse(&bytes);
    assert!(result.is_ok());
}

#[test]
fn reject_corrupted_dcx() {
    let bytes = load_fixture("corrupted.dcx");
    let result = dcx::parse(&bytes);
    assert!(matches!(result, Err(ParseError::InvalidMagic { .. })));
}
```

### Snapshot Testing with insta
```rust
use insta::assert_snapshot;

#[test]
fn parse_header_snapshot() {
    let header = parse_header(FIXTURE_BYTES);
    assert_snapshot!(format!("{header:#?}"));
}
```

---

## Release Profile

```toml
[profile.release]
lto = true              # Link-time optimization
codegen-units = 1       # Single codegen unit for better optimization
panic = "abort"         # No unwinding overhead
strip = true            # Strip symbols
opt-level = "z"         # Optimize for size (use "3" for speed)
```

---

## Common Dependencies

| Purpose | Crate |
|---------|-------|
| Error types | `thiserror` |
| Error context | `eyre`, `anyhow` |
| Zero-copy parsing | `zerocopy` |
| Byte order | `byteorder` |
| Serialization | `serde` (with `serde_json`, `toml`) |
| Windows API | `windows` |
| Memory mapping | `memmap2` |
| Parallelism | `rayon` |
| Logging | `tracing` |
| CLI | `clap` |
| PE parsing | `pelite` |

---

## Clippy Configuration

```toml
[workspace.lints.clippy]
# Correctness
unwrap_used = "warn"
expect_used = "warn"
panic = "warn"

# Style
doc_markdown = "warn"
redundant_else = "warn"
semicolon_if_nothing_returned = "warn"
match_same_arms = "warn"
manual_let_else = "warn"

# Safety
undocumented_unsafe_blocks = "warn"
ptr_as_ptr = "warn"
ptr_cast_constness = "warn"
```
