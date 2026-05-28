# Go Implementation Guidelines

Use when implementing Go code in this project.

## Null/Nil Checks

- Compare against `nil` directly; keep nil handling explicit.
    ```go
    if value == nil {
        return defaultValue
    }
    ```

## Comments/Docs

- Use GoDoc (`// Name ...`) for exported helpers; public API must be documented; avoid inline comments for behavior.
    ```go
    // FormatName returns the display name.
    func FormatName(u User) string {
        return fmt.Sprintf("%s %s", u.First, u.Last)
    }
    ```

## Comparisons

- Place constants/smaller values on the left; prefer `<` / `<=` and reorder instead of `>` / `>=`.
    ```go
    if 1 < value && value <= 10 {
        doWork()
    }
    ```

## Control Flow

- Always use braces; avoid single-line `if/for` without braces.
    ```go
    if value != nil {
        doSomething()
    }
    ```

## Concurrency

- Pass `context.Context`; avoid goroutine leaks; ensure cancel/Done handling.
    ```go
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    go worker(ctx)
    ```

## Error Handling

- Handle errors explicitly; wrap with context if helpful.
    ```go
    result, err := doWork()
    if err != nil {
        return fmt.Errorf("doWork: %w", err)
    }
    ```

## Tests/Assertions

- Use Go testing assertions in subtests; keep related checks together.
    ```go
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
    ```

## Formatting

- Keep blank lines minimal; follow `gofmt`/project style.
