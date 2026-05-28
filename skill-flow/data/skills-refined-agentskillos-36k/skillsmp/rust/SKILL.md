---
name: rust
description: Rust programming language and Cargo package manager commands including build, test, and cross-compilation.
---

# Rust — Cargo Package Manager

**Common Commands**

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# . "$HOME/.cargo/env"

rustup update stable
rustup default $RUST_VERSION  # e.g., stable-x86_64-unknown-linux-gnu
rustup target add x86_64-unknown-linux-gnu
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
cargo install cross --git https://github.com/cross-rs/cross (windows depend docker)
cross build --target x86_64-unknown-linux-gnu --release

cargo rustc -- -Z unpretty=hir-tree
cargo rustc -- -Z unpretty=hir


cargo new my_project             # Create new project
cargo build                      # Compile project
cargo build --release            # Compile optimized binary
cargo run                        # Run main.rs
cargo test                       # Run tests
cargo check                      # Type-check only
cargo add <crate> --features a,b # Add dependencies
cargo update                     # Update Cargo.lock
cargo clean                      # Remove build artifacts
cargo publish                    # Publish to crates.io
cargo doc --open                 # Generate and open docs
```