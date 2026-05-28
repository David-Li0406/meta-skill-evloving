# Python Implementation Guidelines

Use when implementing Python code in this project.

## Null/None Checks

- Prefer `is None` / `is not None`; avoid equality for None checks.
- Keep optional handling explicit; avoid relying on truthiness for `0`, `""`, `[]`.
    ```python
    if value is None:
        return default
    ```

## Comments/Docs

- Use reStructuredText docstrings for public/helpers (public API must be documented); avoid inline/block comments for behavior explanation.
    ```python
    def calculate(value: int) -> int:
        """
        Double the value.
    
        :param value: input integer
        :return: doubled integer
        """
        return value * 2
    ```

## Whitespace

- Avoid extra blank lines; keep formatting consistent.

## Tests/Assertions

- Use `unittest`/`pytest` assertions; group related checks in a single test.

## Comparisons

- Place constants/smaller values on the left; prefer `<` / `<=` and reorder instead of `>` / `>=`.
    ```python
    if 1 < value <= 10:
        ...
    ```

## Typing

- Add type hints for functions/classes; prefer explicit return types.
    ```python
    def add(a: int, b: int) -> int:
        return a + b
    ```
- Prefer typed collections and TypedDict/dataclasses over untyped `dict`/`list` for public APIs.

## Control Flow

- Avoid one-line `if`/`for`/`while`; keep blocks indented and readable.
    ```python
    if is_valid(user):
        process(user)
    ```

## Logging

- Use `logging` (not `print`) for runtime diagnostics.
    ```python
    import logging
    log = logging.getLogger(__name__)
    log.info("processing user %s", user_id)
    ```

## Formatting

- Minimize extraneous blank lines; follow project style.
