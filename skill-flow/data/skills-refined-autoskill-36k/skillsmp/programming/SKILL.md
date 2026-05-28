---
name: programming
description: Always use this skill when writing or editing code of any sort!
---
# programming

- Avoid adding comments to code; they usually clutter the code and get stale easily.
  - Only use them to explain difficult to read behavior and other out-of-band info.
  - Actively remove stale comments and docstrings that don't add value.
  - Use intention-revealing names instead and maintain a consistent vocabulary across the codebase.
- Functions
  - Prefer stateless/pure functions, as they're easier to test and reason about.
  - Separate I/O operations from business logic (Functional Core, Imperative Shell pattern).
    - [Googleblog source](references/functional-core.md)
    - Extract decision logic into pure functions.
    - Keep side effects (database calls, API requests, file I/O) in the outer shell layer.
    - This makes core logic testable without mocking and reusable across features.
  - Aim for one level of abstraction per function.
  - Try to keep them short.
  - If a function needs many arguments, consider using an object or splitting it into multiple functions.
- Run code that you write unless explicitly told not to.
  - It is imperative that you verify the code you write works as intended.
- Avoid mutable global state; it leads to unintended side effects.
- Prefer reusing and extending things.
  - e.g.: if fixtures exist, use them or generalize them.
  - But beware: existing code might be broken; build on top of it, but always test it.
- Avoid unnecessary breaklines in the code; they make the file needlessly longer.
  - Keep related code vertically dense.
    - Declare variables close to usage.
    - Place functions that are dependent on one another close together to make it easier to follow the flow of logic.
      - Place functions in a downward direction, with higher-level functions appearing before lower-level ones.
- When writing validation logic, prefer early returns on errors.
