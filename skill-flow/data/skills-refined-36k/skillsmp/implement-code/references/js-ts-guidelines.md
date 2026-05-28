# JavaScript/TypeScript Implementation Guidelines

Use when implementing JS/TS code in this project.

## Null/Undefined Checks

- Prefer strict equality against `null`/`undefined`; avoid loose truthiness for critical paths.
- Use optional chaining/Nullish Coalescing (`?.`, `??`) instead of nested checks.
    ```typescript
    const name = user?.profile?.name ?? "unknown";
    ```

## Comments/Docs

- Use JSDoc for shared helpers and utilities; public API should be documented; avoid inline/block comments for behavior.
    ```typescript
    /** Formats a user name into display form. */
    function formatName(user: User): string {
      return `${user.first} ${user.last}`;
    }
    ```

## Comparisons

- Put constants/smaller values on the left; prefer `<` / `<=` and reorder instead of `>` / `>=`.
    ```typescript
    if (1 < value && value <= 10) {
      doSomething();
    }
    ```

## Whitespace

- Avoid extra blank lines; keep formatting consistent.

## Tests/Assertions

- Use framework assertions (`expect`, `toBe`, `toEqual`); group related checks in the same test.

## Control Flow

- Always use braces for `if/else`, `for`, `while`, `do-while`, even for single statements.
    ```typescript
    if (user) {
      process(user);
    }
    ```

## Async

- Prefer `async/await` over promise chains; handle errors with `try/catch` or `.catch` at the boundary.
    ```typescript
    try {
      const data = await fetchData();
      return transform(data);
    } catch (err) {
      handle(err);
    }
    ```

## Formatting

- Keep blank lines minimal; follow project lint/format rules.
