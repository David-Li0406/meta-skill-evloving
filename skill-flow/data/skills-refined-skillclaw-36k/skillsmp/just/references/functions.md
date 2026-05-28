# Just Built-in Functions

## System Info

```just
arch()        # CPU: "x86_64", "aarch64"
os()          # OS: "linux", "macos", "windows"
os_family()   # "unix" or "windows"
num_cpus()    # Logical CPU count
```

## Environment

```just
env("KEY")              # Get env var (error if missing)
env("KEY", "default")   # Get with fallback
```

## Paths & Executables

```just
require("cmd")          # Find in PATH or error
which("cmd")            # Find in PATH or empty string
```

## Justfile Locations

```just
justfile()              # Path to current justfile
justfile_directory()    # Parent dir of justfile
source_file()           # Current source file path
source_directory()      # Current source file dir
invocation_directory()  # Dir where just was run
just_executable()       # Path to just binary
just_pid()              # Process ID
home_directory()        # User home (~)
```

## String Manipulation

```just
# Trim
trim(s)                 # Both ends
trim_start(s)           # Leading whitespace
trim_end(s)             # Trailing whitespace
trim_start_match(s, m)  # Remove prefix once
trim_end_match(s, m)    # Remove suffix once

# Transform
replace(s, from, to)    # Replace all occurrences
replace_regex(s, re, r) # Regex replace
quote(s)                # Shell-safe quoting
encode_uri_component(s) # URL encode

# Whitespace-separated operations
append(suffix, s)       # Append to each word
prepend(prefix, s)      # Prepend to each word
```

## Case Conversion

```just
uppercase(s)            # HELLO
lowercase(s)            # hello
capitalize(s)           # Hello
titlecase(s)            # Hello World
snakecase(s)            # hello_world
shoutysnakecase(s)      # HELLO_WORLD
kebabcase(s)            # hello-world
shoutykebabcase(s)      # HELLO-WORLD
lowercamelcase(s)       # helloWorld
uppercamelcase(s)       # HelloWorld
```

## Path Operations

```just
# May fail
absolute_path(p)        # Resolve to absolute
canonicalize(p)         # Resolve symlinks
extension(p)            # File extension
file_name(p)            # Filename only
file_stem(p)            # Name without extension
parent_directory(p)     # Parent dir
without_extension(p)    # Remove extension

# Always succeed
clean(p)                # Normalize path
join(a, b, ...)         # Join path parts
```

## Filesystem

```just
path_exists(p)          # Check if exists
read(p)                 # Read file contents
```

## Shell Execution

```just
shell("command", args...) # Run command, return stdout
```

## Random & Hashing

```just
uuid()                  # Random UUID v4
choose(n, alphabet)     # Random string from chars
sha256(s)               # SHA-256 hash
sha256_file(p)          # SHA-256 of file
blake3(s)               # BLAKE3 hash
blake3_file(p)          # BLAKE3 of file
```

## Datetime

```just
datetime(format)        # Local time (strftime)
datetime_utc(format)    # UTC time
```

## Misc

```just
error(msg)              # Abort with message
is_dependency()         # "true" if running as dep
semver_matches(v, req)  # Check version match
```

## Usage Example

```just
version := `git describe --tags`
build_dir := join(justfile_directory(), "build")
timestamp := datetime("%Y%m%d-%H%M%S")

build:
    echo "Building {{version}} at {{timestamp}}"
    mkdir -p {{build_dir}}
```
