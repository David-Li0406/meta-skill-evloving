# rust-script CLI Reference

## Synopsis

```
rust-script [OPTIONS] <SCRIPT> [SCRIPT_ARGS]...
rust-script [OPTIONS] -e <EXPR>
rust-script [OPTIONS] -l <CLOSURE>
rust-script --clear-cache
```

## Options

### Script Execution

| Option | Short | Description |
|--------|-------|-------------|
| `--expr` | `-e` | Execute `<script>` as a literal expression and display the result |
| `--loop` | `-l` | Execute `<script>` as a closure for each line from stdin |
| `--count` | | Pass line number as second argument to loop closure |

### Dependencies & Features

| Option | Short | Description |
|--------|-------|-------------|
| `--dep <DEP>` | `-d` | Add dependency. Format: name or name=version |
| `--extern <CRATE>` | `-x` | Add `#[macro_use] extern crate` (expr/loop only) |
| `--unstable-feature <FEAT>` | `-u` | Add `#![feature(...)]` declaration |

### Build Options

| Option | Short | Description |
|--------|-------|-------------|
| `--debug` | | Build debug executable (default: release) |
| `--force` | `-f` | Force rebuild even if cached |
| `--toolchain <VER>` | `-t` | Build with specific toolchain (e.g., `nightly`) |
| `--test` | | Compile and run tests |
| `--bench` | | Compile and run benchmarks (requires nightly) |

### Output & Paths

| Option | Short | Description |
|--------|-------|-------------|
| `--cargo-output` | `-c` | Show cargo build output |
| `--package` | `-p` | Generate package and print path, don't run |
| `--pkg-path <PATH>` | | Specify package output directory |
| `--base-path <PATH>` | `-b` | Base path for resolving dependencies |

### Execution

| Option | Short | Description |
|--------|-------|-------------|
| `--wrapper <CMD>` | `-w` | Wrapper command (e.g., `rust-lldb`, `hyperfine`) |

### Cache Management

| Option | Description |
|--------|-------------|
| `--clear-cache` | Clear the script cache |

### Windows Only

| Option | Description |
|--------|-------------|
| `--install-file-association` | Associate `.ers` files with rust-script |
| `--uninstall-file-association` | Remove `.ers` file association |

## Environment Variables

### Set by rust-script (available to scripts)

| Variable | Description |
|----------|-------------|
| `RUST_SCRIPT_PATH` | Absolute path to the script file |
| `RUST_SCRIPT_BASE_PATH` | Base path for resolving relative paths |
| `RUST_SCRIPT_PKG_NAME` | Generated Cargo package name |
| `RUST_SCRIPT_SAFE_NAME` | Filename-safe version of script name |

### For Debugging

| Variable | Description |
|----------|-------------|
| `RUST_LOG=rust_script=trace` | Enable verbose logging |

## Dependency Manifest Format

Use doc comments with a cargo code block:

```rust
//! ```cargo
//! [dependencies]
//! serde = "1.0"
//! tokio = { version = "1", features = ["full"] }
//! ```
```

## Examples

### Basic Usage

```sh
# Run a script
rust-script script.rs

# Run with arguments
rust-script script.rs arg1 arg2

# Separate script args from rust-script args
rust-script -- script.rs -v --help
```

### Expression Mode

```sh
# Simple expression
rust-script -e '2 + 2'

# With dependencies
rust-script -d rand -e 'rand::random::<u32>()'

# Multi-statement (last expression is printed)
rust-script -e 'let x = 5; let y = 3; x * y'
```

### Filter/Loop Mode

```sh
# Uppercase each line
echo "hello" | rust-script -l '|s| s.to_uppercase()'

# With line numbers
cat file.txt | rust-script --count -l '|line, n| format!("{}: {}", n, line)'

# Stateful (sum numbers)
echo -e "1\n2\n3" | rust-script -l 'let mut sum=0; move |s| { sum += s.trim().parse::<i32>().unwrap_or(0); sum }'
```

### Testing & Debugging

```sh
# Run tests
rust-script --test script.rs

# Run tests with output
rust-script --test script.rs -- --nocapture

# Debug build with debugger
rust-script --debug --wrapper rust-lldb script.rs

# Benchmark
rust-script --wrapper "hyperfine --runs 100" script.rs
```

### Toolchain & Cache

```sh
# Use nightly
rust-script -t nightly script.rs

# Force rebuild
rust-script --force script.rs

# Clear all cache
rust-script --clear-cache

# Show cargo output
rust-script -c script.rs
```
