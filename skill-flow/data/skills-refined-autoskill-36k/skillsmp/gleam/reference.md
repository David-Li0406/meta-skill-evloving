# Reference Guide

## Research

**Priority**: `query-docs` → fallback to `gh` CLI

### 1. Context7 (Primary)

Query Context7 library IDs (GitHub project = libraryId) for accurate, up-to-date information:

| Topic | Library ID |
|-------|---------------|
| Standard library (list, dict, result, option) | `/gleam-lang/stdlib` |
| Regular expressions | `/gleam-lang/regexp` |
| Practical code examples, recipes | `/gleam-lang/cookbook` |
| Testing with gleeunit | `/lpil/gleeunit` |
| HTTP types (Request, Response, Method) | `/gleam-lang/http` |
| Time, timestamps, durations, dates | `/gleam-lang/time` |
| JSON encoding/decoding | `/gleam-lang/json` |
| Data structures (heap, map, set, deque) | `/schurhammer/gleamy_structures` |
| HTTP server (mist, WebSocket, SSE) | `/rawhat/mist` |
| Package discovery, ecosystem | `/gleam-lang/awesome-gleam` |

```
task(
  subagent_type="general",
  description="Query Gleam stdlib",
  prompt="Use query-docs with libraryId '/gleam-lang/stdlib' and query: 'How does the list module handle sorting and filtering?'"
)
```

### 2. GitHub CLI (Fallback)

When Context7 is unavailable or lacks detail, use `gh` to search/read repos directly:

```bash
# Search code in a repo
gh search code "websocket" --repo rawhat/mist

# Read specific file
gh api repos/gleam-lang/stdlib/contents/src/gleam/list.gleam --jq '.content' | base64 -d

# Browse repo structure
gh api repos/gleam-lang/stdlib/contents/src/gleam --jq '.[].name'

# Search issues/discussions
gh search issues "json decode" --repo gleam-lang/json
```

**Query multiple repos in parallel** when topics overlap (e.g., HTTP server + HTTP types).


## Patterns

### Error Propagation with `use`

```gleam
pub fn process(path: String) -> Result(Data, Error) {
  use content <- result.try(read(path))
  use parsed <- result.try(parse(content))
  use valid <- result.try(validate(parsed))
  Ok(transform(valid))
}

// Wrap external errors
use raw <- result.map_error(read(path), FileError)

// Early return
use <- bool.guard(string.is_empty(name), Error(EmptyName))
```

### Opaque Types (Enforce Invariants)

```gleam
pub opaque type Email {
  Email(String)
}

pub fn from_string(s: String) -> Result(Email, String) {
  case string.contains(s, "@") {
    True -> Ok(Email(s))
    False -> Error("Invalid email")
  }
}
```

### Make Illegal States Unrepresentable

```gleam
// BAD: allows invalid combinations
pub type Request {
  Request(status: String, data: Option(Data), error: Option(Error))
}

// GOOD: impossible states are unrepresentable
pub type Request {
  Pending
  Success(Data)
  Failed(Error)
}
```

### Subject-First for Pipelines

```gleam
pub fn add(to num: Int, value: Int) -> Int

items
|> list.filter(fn(x) { x > 0 })
|> list.map(fn(x) { x * 2 })
|> int.sum
```

### Pattern Matching

```gleam
// Multi-subject
case x, y {
  0, 0 -> "origin"
  _, 0 -> "x-axis"
  0, _ -> "y-axis"
  _, _ -> "plane"
}

// List destructuring
case items {
  [] -> empty()
  [only] -> single(only)
  [first, ..rest] -> many(first, rest)
}

// Guards
case n {
  x if x > 0 -> "positive"
  x if x < 0 -> "negative"
  _ -> "zero"
}

// let assert for guaranteed matches only
let assert Ok(config) = load_required_config()
```

### Custom Error Types

```gleam
pub type UserError {
  InvalidEmail(String)
  InvalidAge(Int)
  NotFound(UserId)
}

// Wrap externals
pub type AppError {
  DbError(postgres.Error)
  ValidationError(UserError)
}
```

### Labelled Arguments

Proactively use labels for readability.

```gleam
pub fn create(name name: String, email email: String) -> User

// Shorthand when var matches label
let name = "Alice"
create(name:, email: "a@b.com")
```


## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| `import gleam/io.{println}` | `io.println(...)` |
| `panic` for expected failures | Return `Result` |
| `let assert` on user input | Pattern match + handle |
| `list.at(items, n)` indexing | Pattern match or fold |
| Nested `result.try` callbacks | `use` expressions |
| Boolean flags for states | Sum types |
