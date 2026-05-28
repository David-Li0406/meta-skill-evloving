---
name: coding-python
description: Apply this skill when generating Python code
---

## Style

Python code should generally follow the style conventions of the `black` package.

## Comments

Comments should never be added to generated code. Docstrings may be generated, but only for the purpose of adding working doctests.

## Functions

Favor pure functions whenever possible. Structure functions so that they can be demonstrated and tested with doctests.

## Tests

Only use doctests for testing. Do not add unit tests of other forms unless explicitly asked to do so.
