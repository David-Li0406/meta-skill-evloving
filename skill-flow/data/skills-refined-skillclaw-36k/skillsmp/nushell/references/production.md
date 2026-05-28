# Production Nushell: Testing, Quality, and Observability

## Testing Framework

Nushell's standard library provides a complete testing framework via `std/assert`.

### Stdlib Assert Commands

```nu
use std/assert

# Basic assertion - fails if condition is false
assert (1 == 1)
assert ($value > 0) "Value must be positive"

# Equality assertions (better error messages than raw assert)
assert equal $actual $expected
assert not equal $a $b

# String assertions
assert str contains $haystack "needle"

# Length assertions
assert length $list 5

# Type checking
assert ($value | describe) == "int"
```

### Custom Assertions

Extend the stdlib with domain-specific assertions:

```nu
use std/assert

# Custom assertion with labeled error
def "assert even" [number: int] {
    assert ($number mod 2 == 0) --error-label {
        text: $"($number) is not even",
        span: (metadata $number).span,
    }
}

# Custom type assertion
def "assert type" [value: any, expected: string] {
    let actual = ($value | describe)
    assert ($actual == $expected) --error-label {
        text: $"Expected ($expected), got ($actual)",
        span: (metadata $value).span,
    }
}

# Range assertion
def "assert between" [value: number, min: number, max: number] {
    assert ($value >= $min and $value <= $max) --error-label {
        text: $"($value) not in range [($min), ($max)]",
        span: (metadata $value).span,
    }
}
```

### Test File Structure

Option 1: Nupm Package Tests

```
my-project/
├── mod.nu              # Main module
└── tests/
    └── mod.nu          # Test module (export test functions)
```

```nu
# tests/mod.nu
use std/assert

export def "test addition" [] {
    assert equal (2 + 2) 4
}

export def "test string ops" [] {
    assert str contains "hello world" "world"
}

# Run with: nupm test
```

Option 2: Standalone Test Script

```nu
#!/usr/bin/env nu
# tests.nu
use std/assert

def "test math operations" [] {
    assert equal (add 2 3) 5
    assert equal (add -1 1) 0
    assert (add 0 0) == 0
}

def "test string processing" [] {
    assert equal ("hello" | str upcase) "HELLO"
    assert str contains "foobar" "bar"
}

# Auto-discover and run tests
def main [] {
    let tests = (scope commands | where name starts-with "test " | get name)
    mut passed = 0
    mut failed = 0

    for test_name in $tests {
        print -n $"Running ($test_name)... "
        try {
            do (scope commands | where name == $test_name | first | get closure)
            print "✓"
            $passed += 1
        } catch {|e|
            print $"✗ ($e.msg)"
            $failed += 1
        }
    }

    print $"\n($passed) passed, ($failed) failed"
    if $failed > 0 { exit 1 }
}
```

### Data-Driven Tests

```nu
use std/assert

def "test with cases" [] {
    let cases = [
        { input: 0, expected: "zero" }
        { input: 1, expected: "one" }
        { input: 2, expected: "two" }
    ]

    for case in $cases {
        let result = (number_to_word $case.input)
        assert equal $result $case.expected
    }
}

# Table-driven tests with descriptions
def "test parsing" [] {
    [[input, expected, desc];
     ["1,2,3", [1, 2, 3], "comma-separated"]
     ["a|b|c", ["a", "b", "c"], "pipe-separated"]
    ] | each {|case|
        let result = (parse_values $case.input)
        assert equal $result $case.expected $case.desc
    }
}
```

### Integration Tests with Setup/Teardown

```nu
use std/assert

def with_temp_file [test: closure] {
    let path = $"/tmp/test_(random uuid).json"
    try {
        do $test $path
    } catch {|e|
        rm -f $path
        error make {msg: $e.msg}
    }
    rm -f $path
}

def "test file processing" [] {
    with_temp_file {|path|
        [{name: "Alice"}, {name: "Bob"}] | to json | save $path
        let result = (process_users $path)
        assert equal ($result | length) 2
    }
}

def "test api integration" [] {
    let test_data = {name: "test", value: 123}
    let response = (http post http://localhost:8080/api/test $test_data)

    assert equal $response.status 200
    assert type $response.body.id "int"

    # Cleanup
    http delete $"http://localhost:8080/api/test/($response.body.id)"
}
```

### Property-Based Testing

```nu
use std/assert

def "test map preserves length" [] {
    let original = (1..100 | each {|_| random int 0..1000} | collect)
    let mapped = ($original | each {|x| $x * 2})
    assert equal ($mapped | length) ($original | length)
}

def "test filter returns subset" [] {
    let original = (1..50 | collect)
    let filtered = ($original | where {|x| $x mod 2 == 0})
    assert (($filtered | length) <= ($original | length))
}

def "test sort idempotent" [] {
    let data = [3, 1, 4, 1, 5, 9, 2, 6]
    let once = ($data | sort)
    let twice = ($once | sort)
    assert equal $once $twice
}

def "test reverse involutory" [] {
    let data = [1, 2, 3, 4, 5]
    assert equal ($data | reverse | reverse) $data
}
```

## Input Validation

### Schema Validation

```nu
def validate_record [r: record, required_fields: list<string>]: nothing -> bool {
    let missing = ($required_fields | where { |f| not ($f in ($r | columns)) })
    if ($missing | length) > 0 {
        error make {
            msg: "Validation failed",
            label: { text: $"Missing required fields: ($missing | str join ', ')" }
        }
    }
    true
}

def validate_user [user: record]: nothing -> record {
    let required = ["name", "email", "age"]
    validate_record $user $required

    if $user.age < 0 or $user.age > 150 {
        error make {
            msg: "Invalid age",
            label: { text: $"Age must be 0-150, got ($user.age)" }
        }
    }

    if not ($user.email =~ '@') {
        error make { msg: "Invalid email format" }
    }

    $user
}
```

### Path Sanitization

```nu
def validate_file_path [path: string, allowed_dirs: list<string>]: nothing -> string {
    # Prevent directory traversal
    if ($path | str contains "..") {
        error make { msg: "Invalid path: directory traversal detected" }
    }

    let absolute = ($path | path expand)
    let is_allowed = ($allowed_dirs | any { |dir|
        $absolute | str starts-with ($dir | path expand)
    })

    if not $is_allowed {
        error make { msg: "Access denied: path outside allowed directories" }
    }

    $absolute
}
```

## Error Handling Patterns

### Result Type Pattern

```nu
def safe_operation [input: any]: nothing -> record {
    try {
        {ok: true, value: (dangerous_op $input)}
    } catch { |e|
        {ok: false, error: $e.msg}
    }
}

# Usage
let result = safe_operation $data
if $result.ok {
    process $result.value
} else {
    log "error" $result.error
}
```

### Rich Error Context

```nu
def process_file [path: string]: nothing -> any {
    if not ($path | path exists) {
        error make {
            msg: "File not found",
            label: {
                text: $"No such file: ($path)",
                span: (metadata $path).span
            },
            help: "Ensure the file exists and path is correct"
        }
    }

    try {
        open $path
    } catch { |e|
        error make {
            msg: $"Failed to process file: ($path)",
            label: { text: $e.msg },
            help: "Check file format and permissions"
        }
    }
}
```

## Logging Framework

```nu
const LOG_LEVELS = {
    DEBUG: 0
    INFO: 1
    WARN: 2
    ERROR: 3
}

export def log [level: string, message: string, --data: record]: nothing -> nothing {
    let current_level = ($env.LOG_LEVEL? | default "INFO")
    let level_value = ($LOG_LEVELS | get ($level | str upcase))
    let current_value = ($LOG_LEVELS | get $current_level)

    if $level_value >= $current_value {
        let timestamp = (date now | format date "%Y-%m-%d %H:%M:%S")
        let log_entry = {
            timestamp: $timestamp
            level: ($level | str upcase)
            message: $message
            data: ($data | default {})
        }

        # Output as JSON for structured logging
        $log_entry | to json --raw | print
    }
}

# Usage
log "info" "Processing started" --data {file: "data.csv", records: 1000}
log "error" "Failed to connect" --data {host: "db.example.com", retry: 3}
```

### Masking Sensitive Data

```nu
def log_safe [level: string, message: string, --mask: list<string>]: nothing -> nothing {
    mut masked = $message
    if $mask != null {
        for secret in $mask {
            $masked = ($masked | str replace -a $secret "***REDACTED***")
        }
    }
    log $level $masked
}
```

## Observability

### Health Checks

```nu
def health_check []: nothing -> record {
    let checks = [
        {
            name: "disk_space"
            check: { (sys disks | where mount == "/" | first | get free) > 1GB }
            message: "Sufficient disk space"
        }
        {
            name: "memory"
            check: { (sys mem | get used) < ((sys mem | get total) * 0.9) }
            message: "Memory within limits"
        }
        {
            name: "config"
            check: { validate_config }
            message: "Config valid"
        }
    ]

    let results = ($checks | each { |check|
        try {
            let passed = (do $check.check)
            {name: $check.name, status: (if $passed { "pass" } else { "fail" })}
        } catch { |e|
            {name: $check.name, status: "error", error: $e.msg}
        }
    })

    let failed = ($results | where status != "pass" | length)

    {
        status: (if $failed == 0 { "healthy" } else { "unhealthy" })
        checks: $results
        timestamp: (date now | format date "%Y-%m-%dT%H:%M:%SZ")
    }
}
```

### Benchmarking

```nu
def benchmark [name: string, operation: closure]: nothing -> record {
    let start = (date now)
    let result = (do $operation)
    let end = (date now)
    let duration = ($end - $start)

    {
        benchmark: $name
        duration: $duration
        duration_ms: (($duration | into int) / 1_000_000)
        result: $result
    }
}

# Usage
benchmark "file_processing" { open large.csv | where status == "active" | length }
```

### Pipeline Profiling

```nu
def tap [label: string]: any -> any {
    let data = $in
    print $"DEBUG ($label): ($data | describe) - ($data | length? | default 'N/A') items"
    $data
}

def profile [label: string]: any -> any {
    let start = (date now)
    let data = $in
    let duration = ((date now) - $start)
    print $"PROFILE ($label): ($duration)"
    $data
}

# Usage in pipeline
$data
| tap "initial"
| where active == true
| tap "after_filter"
| profile "transformation"
```

## Configuration Management

### Environment-Specific Config

```nu
def load_config [env: string]: nothing -> record {
    let base = (open "config/base.toml")
    let env_file = $"config/($env).toml"

    if ($env_file | path exists) {
        $base | merge (open $env_file)
    } else {
        log "warn" $"No config for ($env), using base"
        $base
    }
}

# Usage
let config = load_config ($env.ENVIRONMENT? | default "development")
```

### Secure Secrets

```nu
def load_secrets [path: string]: nothing -> record {
    if not ($path | path exists) {
        error make { msg: $"Secrets file not found: ($path)" }
    }

    # Check permissions (Unix)
    let perms = (ls -l $path | first | get mode)
    if not ($perms =~ "^-rw-------") {
        error make { msg: "Secrets file has insecure permissions (should be 600)" }
    }

    open $path
}

def get_secret [key: string]: nothing -> string {
    let value = ($env | get -i $key)
    if $value == null {
        error make { msg: $"Required secret not set: ($key)" }
    }
    $value
}
```

## Anti-Patterns to Avoid

| Anti-Pattern                                         | Problem                    | Better Approach                                             |
| ---------------------------------------------------- | -------------------------- | ----------------------------------------------------------- |
| `mut total = 0; for x in $list { $total += $x }`     | Mutation, imperative       | `$list \| math sum`                                         |
| `ps \| to text \| lines \| split column " "`         | Parsing structured as text | `ps \| select pid name cpu`                                 |
| `let all = (open huge \| collect); $all \| first 10` | Premature collection       | `open huge \| first 10`                                     |
| `def process [x] { ... }`                            | Missing types              | `def process [x: int]: int -> int { ... }`                  |
| `try { risky } catch { null }`                       | Silent failure             | `try { risky } catch { \|e\| log "error" $e.msg; default }` |

## Production Checklist

### Code Quality

- [ ] All functions have type signatures
- [ ] Error handling is explicit
- [ ] Input validation performed
- [ ] Functions are pure (no hidden side effects)
- [ ] Code is documented

### Testing

- [ ] Unit tests cover happy path and errors
- [ ] Integration tests verify E2E
- [ ] Tests run in CI/CD

### Observability

- [ ] Structured logging
- [ ] Health checks
- [ ] Error tracking

### Security

- [ ] Input sanitization
- [ ] Secure secret management
- [ ] Audit logging for sensitive ops
- [ ] Principle of least privilege
