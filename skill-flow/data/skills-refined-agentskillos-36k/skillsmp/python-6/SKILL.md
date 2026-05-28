---
name: python
description: Always use this skill when writing or editing python code!
---
# python

- Keep lines short and avoid horizontal alignment.
- isort and black (unless the project specifies otherwise).
  - Install them with pip if not already installed.
- Avoid try except Exception that swallows errors.
  - Prefer logging, re-raising it, or handling specific exceptions.
- Always add type hints to code; especially anything non-obvious.
  - Prefer `|` over `Union[]` and `| None` over `Optional`.
  - Run a type checker (e.g.: `mypy`) and fix all errors after writing the code.
- Whenever possible, extract logic out to staticmethods and classmethods.
- Don't return multiline statements; prefer assigning then returning.
- When using pydantic, prefer the new [validators](https://docs.pydantic.dev/latest/concepts/validators/#field-validators) over the older `@validator` decorators.
  - e.g.: `number: Annotated[int, AfterValidator(is_even)]`
- Don't write useless getters and setters such as:
  ```py
    def get_my_items(self) -> list[MyItem]:
      return self.my_items
  ```
  - Access the attributes directly.
- Don't setup `logging` in libraries; leave that to the application using the library.

## dependencies

- Prefer adding dependencies without version constraints unless absolutely necessary.
- Never try except missing imports; assume users of our code will install all needed dependencies.
  - Add them to requirements.txt or equivalent.
  - Also, imports should always be at the top of the file.
- When installing packages for source code that's local, use `pip install -e ./path`.
  - So we don't confuse ourselves editing local code and running things from site-packages.
