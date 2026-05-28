# Nushell Data Types

## Type Hierarchy

```
any
├── nothing (null/void)
├── bool
├── int
├── float
├── number (int | float)
├── string
├── date
├── duration
├── filesize
├── binary
├── range
├── glob
├── list<T>
├── record<K, V>
├── table<T> (list<record<T>>)
├── closure
├── block
└── error
```

## Type System Overview

Nushell has a gradual type system. Types are checked at runtime but can be annotated for documentation and early error detection.

```nu
# Type annotations in function signatures
def process [data: record, count: int = 10] -> table {
    # ...
}

# Pipeline type signatures
def func [multiplier: int]: list<int> -> list<int> {
    $in | each {|x| $x * $multiplier}
}

# Check types
42 | describe        # => int
{a: 1} | describe    # => record<a: int>

# Union types
def func [value: int | string] { ... }
```

## Records

Records are key-value structures (like objects/dictionaries).

```nu
# Creation
let person = {name: "Alice", age: 30, active: true}

# Access
$person.name                    # => Alice
$person | get name              # => Alice
$person | get -i missing        # => null (ignore missing)

# Modification (creates new record)
$person | insert email "a@b.com"
$person | update age {|r| $r.age + 1}
$person | upsert nickname "Ali"  # Insert or update
$person | reject age             # Remove field

# Merge records
$person | merge {role: "admin"}

# Nested access
$config.database.connection.host
$config | get database.connection.host
```

## Lists

Ordered collections of values.

```nu
# Creation
let nums = [1, 2, 3, 4, 5]
let range = (1..5)              # Same result
let empty = []

# Access
$nums.0                         # First element
$nums | first                   # First element
$nums | last 2                  # Last 2 elements
$nums | get 2                   # Third element (0-indexed)
$nums | skip 1 | first 3        # Slice (skip 1, take 3)

# Modification
$nums | append 6
$nums | prepend 0
$nums | insert 2 "inserted"     # Insert at index
$nums | update 0 100            # Replace at index

# Operations
$nums | reverse
$nums | shuffle
$nums | uniq
$nums | flatten                 # Flatten nested lists
$nums | zip [a, b, c, d, e]     # Pair elements
```

## Tables

Tables are lists of records with consistent columns.

```nu
# Creation - literal syntax
let users = [[name, age, role];
    [alice, 30, admin],
    [bob, 25, user],
    [carol, 35, admin]]

# Creation - from records
[{name: alice, age: 30}, {name: bob, age: 25}]

# Selection
$users | select name age
$users | reject role
$users | get name                # Just the name column as list

# Filtering
$users | where age > 25
$users | where role == "admin"
$users | where name =~ "^a"      # Regex match
$users | find "ali"              # Fuzzy search

# Sorting
$users | sort-by age
$users | sort-by age --reverse
$users | sort-by role age        # Multiple columns

# Aggregation
$users | group-by role
$users | uniq-by role
$users.age | math avg
$users | length

# Joins
$users | join $other_table common_column
```

## Strings

```nu
# Interpolation
let name = "world"
$"Hello ($name)!"               # => Hello world!
$"Math: (1 + 2)"                # => Math: 3

# Raw strings (single quotes - no escapes except '')
'Path: C:\Users\name'

# Multi-line
let text = "line 1
line 2
line 3"

# Operations
"hello" | str upcase            # => HELLO
"  trim  " | str trim           # => trim
"hello" | str replace "l" "L"   # => heLLo (first)
"hello" | str replace -a "l" "L" # => heLLo (all)
"a,b,c" | split row ","         # => [a, b, c]
["a", "b"] | str join ", "      # => a, b
"hello" | str substring 1..3    # => ell
"hello" | str length            # => 5
"hello" | str contains "ell"    # => true
"hello" | str starts-with "he"  # => true
```

## Numbers

```nu
# Types
42                              # int
3.14                            # float
0x1F                            # hex
0b1010                          # binary
0o755                           # octal
1_000_000                       # underscores for readability

# Math
10 + 3                          # => 13
10 / 3                          # => 3 (int division)
10 / 3.0                        # => 3.333... (float)
10 mod 3                        # => 1
2 ** 10                         # => 1024

# List math
[1, 2, 3] | math sum            # => 6
[1, 2, 3] | math avg            # => 2
[1, 2, 3] | math max            # => 3
```

## Durations and Filesizes

```nu
# Durations
1hr + 30min + 45sec
2day - 12hr
(3wk).nanosecond                # Convert to nanoseconds

# Filesizes
1gb + 500mb
10mb / 2                        # => 5mb
(1gb).bytes                     # => 1073741824
```

## Dates

```nu
# Current time
date now

# Parsing
"2024-01-15" | into datetime
"Jan 15, 2024" | into datetime

# Components
(date now).year
(date now).month
(date now).day

# Arithmetic
(date now) + 1day
(date now) - 1wk

# Formatting
date now | format date "%Y-%m-%d"
```

## Closures

Closures capture their environment and can be passed to commands.

```nu
# Basic closure
let double = {|x| $x * 2}
3 | do $double                  # => 6

# With pipeline input ($in)
let process = { $in | str upcase }
"hello" | do $process           # => HELLO

# In higher-order functions
[1, 2, 3] | each {|x| $x * 2}
[1, 2, 3] | filter {|x| $x > 1}
[1, 2, 3] | reduce {|it, acc| $acc + $it}
```

## Type Conversions

```nu
# Explicit conversions
"42" | into int
42 | into string
"true" | into bool
"1gb" | into filesize

# Format conversions
open data.json                  # Auto-detect
"json string" | from json
{data: 1} | to json
{data: 1} | to yaml
{data: 1} | to toml

# Table to other formats
$table | to csv
$table | to md                  # Markdown table
```

## Null and Nothing

```nu
# Null handling
null | is-empty                 # => true
null | default "fallback"       # => fallback
$record.missing?                # => null (safe access)

# Filtering nulls
[1, null, 2, null, 3] | compact # => [1, 2, 3]
$table | where field != null
```

## Type Checking

```nu
# Check type
42 | describe                   # => int
{a: 1} | describe               # => record<a: int>

# Type predicates (custom)
def is-number [val] { ($val | describe) in ["int", "float"] }
```
