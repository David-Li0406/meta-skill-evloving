# Nushell Pipeline Patterns

## Pipeline Composition

### Branching Pipelines

```nu
# Process same data multiple ways
let data = (open data.json)
let summary = ($data | length)
let filtered = ($data | where active)
{total: $summary, active: ($filtered | length)}
```

### Conditional Pipelines

```nu
# Apply transformation conditionally
ls | each {|f|
    if $f.type == "dir" {
        {name: $f.name, kind: "directory", count: (ls $f.name | length)}
    } else {
        {name: $f.name, kind: "file", size: $f.size}
    }
}
```

### Parallel Processing

```nu
# par-each for parallel execution
ls *.txt | par-each {|f| open $f.name | lines | length } | math sum
```

## Table Transformations

### Reshape Data

```nu
# Wide to long (transpose)
{a: 1, b: 2, c: 3} | transpose key value

# Long to wide (pivot)
[[key, value]; [a, 1], [b, 2]] | reduce -f {} {|it, acc| $acc | insert $it.key $it.value}

# Flatten nested structures
[[name, scores]; [alice, [90, 85, 92]], [bob, [78, 82]]] | flatten scores
```

### Windowing and Grouping

```nu
# Sliding window
[1, 2, 3, 4, 5] | window 3 | each {|w| $w | math avg }

# Group consecutive items
ls | group-by type | transpose type files

# Running totals
[10, 20, 30] | reduce -f [] {|it, acc| $acc | append (($acc | last | default 0) + $it)}
```

## Working with External Commands

### Capturing Output

```nu
# Structured capture
let result = (^git status --porcelain | complete)
if $result.exit_code == 0 {
    $result.stdout | lines | parse "{status} {file}"
}

# Streaming large output
^find . -name "*.log" | lines | each {|f| {file: $f, size: (ls $f | get size.0)}}
```

### Mixed Pipelines

```nu
# External -> internal -> external
^curl -s https://api.example.com/data
    | from json
    | where status == "active"
    | to json
    | ^jq '.[] | .name'
```

## Error Handling Patterns

### Safe Navigation

```nu
# Multiple fallbacks
$data | get -i field | default "fallback"

# Optional chain through nested structure
$config.database?.connection?.timeout? | default 30
```

### Batch Processing with Error Recovery

```nu
# Collect errors without stopping
ls *.csv | each {|f|
    try {
        {file: $f.name, data: (open $f.name)}
    } catch {
        {file: $f.name, error: "failed to parse"}
    }
}
```

## Performance Patterns

### Lazy Evaluation

```nu
# Use first/last/take to limit work
open huge.json | get items | take 100 | where condition

# Skip expensive operations on unused data
ls | select name size | sort-by size | last 10  # Don't compute unused columns
```

### Batching

```nu
# Process in chunks
1..1000 | chunks 100 | each {|batch|
    # Process 100 items at a time
    $batch | each {|x| expensive_operation $x }
}
```

## Common Pipeline Recipes

### File Processing

```nu
# Find duplicates by content
ls *.txt | insert hash {|f| open $f.name | hash md5} | group-by hash | transpose hash files | where {|r| ($r.files | length) > 1}

# Bulk rename
ls *.jpeg | each {|f| mv $f.name ($f.name | str replace ".jpeg" ".jpg")}

# Directory size summary
ls | where type == dir | insert dir_size {|d| ls $d.name | get size | math sum} | sort-by dir_size
```

### Log Analysis

```nu
# Parse and aggregate logs
open app.log | lines | parse "{timestamp} [{level}] {message}"
    | group-by level
    | transpose level entries
    | insert count {|r| $r.entries | length}
    | reject entries
```

### API Data Processing

```nu
# Paginated API fetch
def fetch-all [base_url: string] {
    mut results = []
    mut page = 1
    loop {
        let resp = (http get $"($base_url)?page=($page)")
        if ($resp.items | is-empty) { break }
        $results = ($results | append $resp.items)
        $page += 1
    }
    $results
}
```

## Functional Programming Patterns

### The Core Trinity: Map, Filter, Reduce

```nu
# map: transform each element
$list | each { |x| $x * 2 }

# filter: select elements matching predicate
$list | where { |x| $x > 10 }

# reduce: aggregate to single value
$list | reduce { |it, acc| $acc + $it }

# Combined pipeline
$sales
| where amount > 100               # filter
| each { |s| $s.amount * $s.qty }  # map
| reduce { |it, acc| $acc + $it }  # reduce
```

### Function Composition

```nu
# Pipelines ARE function composition
# data | f | g | h  ===  h(g(f(data)))

def normalize_name []: string -> string {
    str trim | str downcase | str replace -a " " "_"
}

def validate_length [min: int]: string -> bool {
    str length | $in >= $min
}

# Compose into processing pipeline
$input | normalize_name | validate_length 3
```

### Higher-Order Functions

```nu
# Functions that take/return functions
def apply_twice [f: closure]: any -> any {
    $in | do $f | do $f
}

def compose [f: closure, g: closure]: any -> any {
    $in | do $f | do $g
}

# Custom mapper
def map_transform [transform: closure]: list -> list {
    $in | each $transform
}

10 | apply_twice { |x| $x * 2 }  # => 40
```

### Lazy Sequences with generate

```nu
# Infinite counter (take limits output)
generate { |x| { out: $x, next: ($x + 1) } } 0 | take 10

# Fibonacci sequence
generate { |s| {
    out: $s.0,
    next: [$s.1, ($s.0 + $s.1)]
} } [0, 1] | take 20

# Custom sequence with state
def powers_of_two []: nothing -> list {
    generate { |n| { out: (2 ** $n), next: ($n + 1) } } 0 | take 10
}
```

### Fold Patterns (reduce)

```nu
# Sum with explicit initial value
$list | reduce -f 0 { |it, acc| $acc + $it }

# Build structure from list
["name", "age", "city"] | reduce -f {} { |key, acc|
    $acc | insert $key null
}
# => {name: null, age: null, city: null}

# Running total (scan-like)
[10, 20, 30] | reduce -f [] { |it, acc|
    $acc | append (($acc | last | default 0) + $it)
}
# => [10, 30, 60]
```

### Partition and Group

```nu
# Group by computed key
$sales | group-by { |row| $row.date | format date '%Y-%m' }

# Partition by predicate (manual)
def partition [pred: closure]: list -> record {
    let data = $in
    {
        true: ($data | where {|x| do $pred $x})
        false: ($data | where {|x| not (do $pred $x)})
    }
}

[1, 2, 3, 4, 5] | partition {|x| $x mod 2 == 0}
# => {true: [2, 4], false: [1, 3, 5]}
```

### Monadic Chains (Maybe/Result patterns)

```nu
# Safe navigation chain
$data
| get -i user
| get -i profile
| get -i email
| default "no-email@example.com"

# Optional chaining with ?
$config.database?.host? | default "localhost"

# Error chain with try
try { step1 } | try { step2 } catch { default_value }

# Result type pattern
def safe_divide [a: float, b: float]: nothing -> record {
    if $b == 0 {
        {err: "Division by zero"}
    } else {
        {ok: ($a / $b)}
    }
}
```

### Partial Application via Closures

```nu
# Closures capture environment
def make_multiplier [factor: int]: nothing -> closure {
    { |x| $x * $factor }
}

let double = (make_multiplier 2)
let triple = (make_multiplier 3)

5 | do $double  # => 10
5 | do $triple  # => 15

# Threshold capture
let min_age = 18
$users | where { |u| $u.age >= $min_age }
```

## Streaming Best Practices

### Stream vs Collect Decision

```nu
# STREAM: Large data, early exit, memory constrained
open huge.csv | where status == "active" | first 100  # Stops after 100

# COLLECT: Multiple passes needed, data fits in memory
let data = (open medium.json)
let stats = ($data | describe)
let filtered = ($data | where active)
{stats: $stats, count: ($filtered | length)}
```

### Memory-Efficient Patterns

```nu
# Good: Stream with early exit
open huge.log | lines | where {$in =~ "ERROR"} | first 10

# Bad: Collect everything first
let all = (open huge.log | lines)
$all | where {$in =~ "ERROR"} | first 10

# Good: Streaming aggregation (constant memory)
open huge.csv | reduce { |row, acc| $acc + $row.value }

# Good: Batch I/O operations
$large_list | chunks 100 | each { |batch|
    batch_insert $batch
}
```

### Parallel Processing Considerations

```nu
# Good: Expensive operations (>100ms per item)
$files | par-each { |f| expensive_analysis $f }

# Bad: Simple operations (overhead exceeds benefit)
$numbers | par-each { |n| $n * 2 }  # Just use each

# Preserve order when needed
$items
| enumerate
| par-each { |x| {index: $x.index, result: (process $x.item)} }
| sort-by index
| get result
```

## Declarative vs Imperative

```nu
# Imperative (avoid)                    # Declarative (prefer)
mut sum = 0                             $list.value | math sum
for item in $list { $sum += $item.value }

mut result = []                         $users | where active | get name
for user in $users {
    if $user.active { $result = ($result | append $user.name) }
}
```
