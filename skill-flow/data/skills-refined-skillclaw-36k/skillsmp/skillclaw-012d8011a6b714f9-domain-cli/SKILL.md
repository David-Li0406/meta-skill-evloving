---
name: domain-cli
description: Use this skill when building command-line interface (CLI) tools in Rust, focusing on argument parsing, configuration management, and user feedback.
---

# Skill body

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| User ergonomics | Clear help, errors | Use clap derive macros |
| Config precedence | CLI > env > file | Implement layered config loading |
| Exit codes | Non-zero on error | Ensure proper Result handling |
| Stdout/stderr | Data vs errors | Use eprintln! for errors |
| Interruptible | Handle Ctrl+C | Implement signal handling |

## Critical Constraints

### User Communication

```
RULE: Errors to stderr, data to stdout
WHY: Pipeable output, scriptability
RUST: Use eprintln! for errors, println! for data
```

### Configuration Priority

```
RULE: CLI args > env vars > config file > defaults
WHY: User expectation, override capability
RUST: Use layered config with clap + figment/config
```

### Exit Codes

```
RULE: Return non-zero on any error
WHY: Script integration, automation
RUST: Use main() -> Result<(), Error> or explicit exit()
```

## Trace Down

From constraints to design (Layer 2):

```
"Need argument parsing"
    ↓ Use clap: #[derive(Parser)]

"Need config layering"
    ↓ Use figment/config for layered sources

"Need progress display"
    ↓ Use indicatif for progress bars
```

## Key Crates

| Purpose | Crate |
|---------|-------|
| Argument parsing | clap |
| Interactive prompts | dialoguer |
| Progress bars | indicatif |
| Colored output | colored |
| Terminal UI | ratatui |
| Terminal control | crossterm |
| Console utilities | console |

## Design Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| Args struct | Type-safe args | `#[derive(Parser)]` |
| Subcommands | Command hierarchy | `#[derive(Subcommand)]` |
| Config layers | Override precedence | CLI > env > file |
| Progress | User feedback | `ProgressBar::new(len)` |

## Code Pattern: CLI Structure

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp", about = "My CLI tool")]
struct Cli {
    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
    
    /// Subcommand
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// A command to do something
    DoSomething {
        /// An argument for the command
        arg: String,
    },
}
```