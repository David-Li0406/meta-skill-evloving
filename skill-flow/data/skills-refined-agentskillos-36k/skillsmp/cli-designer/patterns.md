# CLI Code Patterns for HawkOp

Rust/clap templates for common CLI scenarios.

## Command Definition

### Basic Subcommand

```rust
#[derive(Subcommand, Debug)]
pub enum MyCommands {
    /// Brief one-line description
    #[command(
        visible_alias = "ls",  // Short alias
        after_help = "EXAMPLES:\n  \
            hawkop my list              # List all items\n  \
            hawkop my list --limit 10   # First 10 items\n  \
            hawkop my list --json | jq  # Pipe to jq"
    )]
    List {
        #[command(flatten)]
        pagination: PaginationArgs,
    },
}
```

### Command with Drill-Down

```rust
/// Get details with optional drill-down
#[command(
    after_help = "EXAMPLES:\n  \
        hawkop scan get abc123           # Overview\n  \
        hawkop scan get abc123 alerts    # List findings\n  \
        hawkop scan get abc123 40012     # Specific finding"
)]
Get {
    /// Resource ID (UUID)
    id: String,

    /// Optional drill-down target
    target: Option<String>,

    /// Show detailed output
    #[arg(long, short = 'd')]
    detail: bool,
}
```

## Arguments vs Flags

### When to Use Positional Args

```rust
// GOOD: Single obvious argument
Get {
    /// Scan ID to retrieve
    scan_id: String,  // hawkop scan get abc123
}

// GOOD: Variable-length same type
Delete {
    /// IDs to delete
    ids: Vec<String>,  // hawkop delete id1 id2 id3
}
```

### When to Use Flags

```rust
// GOOD: Two different types of values
Fork {
    /// Source application
    #[arg(long)]
    from: String,

    /// Destination application
    #[arg(long)]
    to: String,
}
// hawkop fork --from app1 --to app2

// BAD: Which is source, which is destination?
// hawkop fork app1 app2
```

## Standard Flag Patterns

### Global Flags (in Cli struct)

```rust
#[derive(Parser)]
pub struct Cli {
    #[arg(long, global = true, env = "HAWKOP_FORMAT", default_value = "table")]
    pub format: OutputFormat,

    #[arg(long, global = true, env = "HAWKOP_ORG_ID")]
    pub org: Option<String>,

    #[arg(long, global = true, env = "HAWKOP_CONFIG")]
    pub config: Option<String>,

    #[arg(long, global = true, env = "HAWKOP_DEBUG")]
    pub debug: bool,
}
```

### Pagination Args (reusable)

```rust
#[derive(Args, Debug, Clone)]
pub struct PaginationArgs {
    /// Maximum items to return
    #[arg(long, short = 'l', default_value = "25")]
    pub limit: usize,

    /// Page number (0-indexed)
    #[arg(long, default_value = "0")]
    pub page: usize,

    /// Fetch all results (ignore limit)
    #[arg(long)]
    pub all: bool,
}
```

### Filter Args (reusable)

```rust
#[derive(Args, Debug, Clone)]
pub struct ScanFilterArgs {
    /// Filter by application ID
    #[arg(long, short = 'a')]
    pub app: Option<String>,

    /// Filter by environment
    #[arg(long, short = 'e')]
    pub env: Option<String>,

    /// Filter by status
    #[arg(long, short = 's')]
    pub status: Option<String>,

    /// Filter by date (e.g., 7d, 30d, 2024-01-01)
    #[arg(long)]
    pub since: Option<String>,
}
```

## Error Handling

### Actionable Error Types

```rust
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("Missing API key\n\nRun 'hawkop init' to configure authentication.")]
    MissingApiKey,

    #[error("Organization not found: {0}\n\nUse 'hawkop org list' to see available organizations.")]
    OrgNotFound(String),

    #[error("Invalid configuration at {path}\n\n{details}\n\nRun 'hawkop init' to reconfigure.")]
    InvalidConfig { path: String, details: String },
}
```

### API Error Handling

```rust
#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("Authentication failed\n\nYour API key may have expired. Run 'hawkop init' to re-authenticate.")]
    Unauthorized,

    #[error("Rate limited by API\n\nToo many requests. Wait a moment and try again.")]
    RateLimited,

    #[error("Resource not found: {0}\n\nVerify the ID is correct with 'hawkop {1} list'.")]
    NotFound(String, String),  // (id, resource_type)
}
```

## Output Formatting

### Table Output (via Tabled)

```rust
#[derive(Debug, Clone, Tabled, Serialize)]
pub struct ScanDisplay {
    #[tabled(rename = "ID")]
    pub id: String,

    #[tabled(rename = "APP")]
    pub app: String,

    #[tabled(rename = "STATUS")]
    pub status: String,

    #[tabled(rename = "FINDINGS")]
    pub findings: String,
}
```

### JSON Output Wrapper

```rust
#[derive(Serialize)]
pub struct JsonOutput<T: Serialize> {
    pub data: T,
    pub meta: JsonMeta,
}

#[derive(Serialize)]
pub struct JsonMeta {
    pub total: usize,
    pub page: usize,
    pub limit: usize,
    pub has_more: bool,
}
```

## TTY Detection

### Color Support

```rust
use std::io::IsTerminal;

pub fn supports_color() -> bool {
    std::io::stdout().is_terminal()
        && std::env::var("NO_COLOR").is_err()
        && std::env::var("TERM").map(|t| t != "dumb").unwrap_or(true)
}
```

### Progress Indicators

```rust
use indicatif::{ProgressBar, ProgressStyle};

pub fn create_spinner(message: &str) -> Option<ProgressBar> {
    if !std::io::stderr().is_terminal() {
        return None;
    }

    let pb = ProgressBar::new_spinner();
    pb.set_style(ProgressStyle::default_spinner()
        .template("{spinner:.green} {msg}")
        .unwrap());
    pb.set_message(message.to_string());
    Some(pb)
}
```

## Navigation Hints

### After Command Output

```rust
fn show_scan_overview(scan: &Scan) {
    // ... display scan details ...

    // Suggest next action on stderr
    eprintln!();
    eprintln!("→ hawkop scan get {} alerts", scan.id);
}
```

### After List Commands

```rust
fn show_scan_list(scans: &[Scan], has_more: bool) {
    // ... display table ...

    if has_more {
        eprintln!();
        eprintln!("Showing first {} results. Use --all for complete list.", scans.len());
    }

    if let Some(first) = scans.first() {
        eprintln!();
        eprintln!("→ hawkop scan get {}", first.id);
    }
}
```
