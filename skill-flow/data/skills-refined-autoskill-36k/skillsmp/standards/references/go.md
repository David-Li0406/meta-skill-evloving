# Go Standards (Tier 1)

## Required
- `gofmt` (automatic)
- `golangci-lint run` passes
- All exported symbols documented

## Error Handling
- Always check errors: `if err != nil`
- Wrap errors with context: `fmt.Errorf("doing X: %w", err)`
- Never `_ = err` without `// nolint:errcheck` comment

## Common Issues
| Pattern | Problem | Fix |
|---------|---------|-----|
| `%v` for errors | Breaks error chain | Use `%w` |
| `panic()` in library | Crashes caller | Return error |
| Naked goroutine | No error handling | errgroup or channels |
| `interface{}` | Type safety loss | Use generics or specific types |

## Interfaces
- Accept interfaces, return structs
- Keep interfaces small (1-3 methods)
- Define interfaces where used, not implemented

## Concurrency
- Always pass `context.Context` as first param
- Use `sync.Mutex` for shared state
- Prefer channels for communication
