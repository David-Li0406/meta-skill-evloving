---
name: python-best-practices
description: Use this skill when writing or editing Python code to ensure high quality and maintainability.
---

# Skill body

- Keep lines short and avoid horizontal alignment.
- Use `isort` and `black` for code formatting, unless the project specifies otherwise. Install them with pip if not already installed.
- Avoid `try except Exception` that swallows errors. Prefer logging, re-raising, or handling specific exceptions.
- Always add type hints to code, especially for anything non-obvious. Prefer `|` over `Union[]` and `| None` over `Optional`. Run a type checker (e.g., `mypy`) and fix all errors after writing the code.
- Extract logic into `staticmethods` and `classmethods` whenever possible.
- Avoid returning multiline statements; prefer assigning then returning.
- When using Pydantic, prefer the new validators over the older `@validator` decorators. For example:
  ```python
  number: Annotated[int, AfterValidator(is_even)]
  ```
- Avoid writing useless getters and setters. Access attributes directly instead:
  ```python
  def get_my_items(self) -> list[MyItem]:
      return self.my_items
  ```
- Do not set up logging in libraries; leave that to the application using the library.
- Prefer adding dependencies without version constraints unless absolutely necessary. Never use `try except` for missing imports; assume users will install all needed dependencies. Add them to `requirements.txt` or equivalent, and ensure imports are at the top of the file.
- When installing packages for local source code, use `pip install -e ./path` to avoid confusion between local code and site-packages.
- Avoid adding comments to code; they can clutter and become stale. Use intention-revealing names instead and maintain a consistent vocabulary across the codebase.
- Prefer stateless/pure functions, as they are easier to test and reason about. Separate I/O operations from business logic (Functional Core, Imperative Shell pattern).
- Run code that you write to verify it works as intended.
- Avoid mutable global state to prevent unintended side effects.
- Reuse and extend existing code where possible, but ensure it is tested.
- Avoid unnecessary breaklines in the code; keep related code vertically dense.
- When writing validation logic, prefer early returns on errors.