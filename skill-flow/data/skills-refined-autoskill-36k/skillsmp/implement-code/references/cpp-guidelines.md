# C/C++ Implementation Guidelines

Use when implementing C/C++ code in this project.

## Null Checks

- Use `nullptr` comparisons explicitly; avoid legacy `NULL`/`0` pointers.
    ```cpp
    if (ptr == nullptr) {
        return default_value;
    }
    ```

## Comments/Docs

- Use Doxygen-style comments for shared helpers; public API must be documented; avoid inline/block comments for behavior.
    ```cpp
    /** Formats a user name into display form. */
    std::string FormatName(const User& user);
    ```

## Comparisons

- Place constants/smaller values on the left; prefer `<` / `<=` and reorder instead of `>` / `>=`.
    ```cpp
    if (1 < value && value <= 10) {
        process();
    }
    ```

## Whitespace

- Avoid extra blank lines; keep formatting consistent.

## Tests/Assertions

- Use test framework assertions (`EXPECT_EQ`/`ASSERT_EQ` or project standard); group related checks together.

## Control Flow

- Always use braces on `if/else`, `for`, `while`, `do-while`, even for single statements.
    ```cpp
    if (is_valid) {
        process();
    }
    ```

## Error Handling

- Prefer exceptions where appropriate or consistent project pattern; document chosen approach.
    ```cpp
    try {
        auto v = parse(input);
        return v;
    } catch (const ParseError& e) {
        throw;
    }
    ```

## Formatting

- Keep blank lines minimal; follow project formatting/lint rules.
