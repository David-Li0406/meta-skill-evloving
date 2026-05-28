# Clap Derive Patterns

## Basic CLI

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file to process
    #[arg(short, long)]
    input: String,

    /// Output file (optional)
    #[arg(short, long)]
    output: Option<String>,

    /// Enable verbose output
    #[arg(short, long, default_value_t = false)]
    verbose: bool,

    /// Number of iterations
    #[arg(short = 'n', long, default_value_t = 1)]
    count: u32,
}

fn main() {
    let cli = Cli::parse();
    
    if cli.verbose {
        println!("Processing: {}", cli.input);
    }
}
```

## Subcommands

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git-lite")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Clone a repository
    Clone {
        /// Repository URL
        url: String,
        /// Local directory
        #[arg(short, long)]
        directory: Option<String>,
    },
    /// Commit changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,
        /// Amend previous commit
        #[arg(long)]
        amend: bool,
    },
    /// Push to remote
    Push {
        /// Remote name
        #[arg(default_value = "origin")]
        remote: String,
        /// Branch name
        branch: Option<String>,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Clone { url, directory } => {
            println!("Cloning {} to {:?}", url, directory);
        }
        Commands::Commit { message, amend } => {
            println!("Committing: {} (amend: {})", message, amend);
        }
        Commands::Push { remote, branch } => {
            println!("Pushing to {} branch {:?}", remote, branch);
        }
    }
}
```

## Value Parsers

```rust
use clap::{Parser, ValueEnum};
use std::path::PathBuf;

#[derive(Copy, Clone, PartialEq, Eq, ValueEnum)]
enum Format {
    Json,
    Yaml,
    Toml,
}

#[derive(Parser)]
struct Cli {
    /// Output format
    #[arg(short, long, value_enum, default_value_t = Format::Json)]
    format: Format,

    /// Config file path
    #[arg(short, long, value_name = "FILE")]
    config: PathBuf,

    /// Port number (1-65535)
    #[arg(short, long, value_parser = clap::value_parser!(u16).range(1..))]
    port: u16,

    /// Log levels
    #[arg(short, long, value_delimiter = ',')]
    levels: Vec<String>,
}
```

## Environment Variables

```rust
#[derive(Parser)]
struct Cli {
    /// API key (or set API_KEY env var)
    #[arg(long, env = "API_KEY")]
    api_key: String,

    /// Database URL
    #[arg(long, env = "DATABASE_URL", default_value = "postgres://localhost/db")]
    database_url: String,
}
```

## Global Options

```rust
#[derive(Parser)]
struct Cli {
    /// Global verbose flag
    #[arg(short, long, global = true)]
    verbose: bool,

    /// Config file (applies to all subcommands)
    #[arg(short, long, global = true)]
    config: Option<PathBuf>,

    #[command(subcommand)]
    command: Commands,
}
```

## Argument Groups

```rust
use clap::{Args, Parser};

#[derive(Args)]
#[group(required = true, multiple = false)]
struct Target {
    /// Target by ID
    #[arg(long)]
    id: Option<u64>,

    /// Target by name
    #[arg(long)]
    name: Option<String>,
}

#[derive(Parser)]
struct Cli {
    #[command(flatten)]
    target: Target,
}
```

## Validation

```rust
use clap::Parser;

fn validate_port(s: &str) -> Result<u16, String> {
    let port: u16 = s.parse().map_err(|_| "not a number")?;
    if port > 0 {
        Ok(port)
    } else {
        Err("port must be positive".to_string())
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(long, value_parser = validate_port)]
    port: u16,
}
```
