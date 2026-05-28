---
name: code-search
description: How to effectively search and navigate codebases using KOR's code graph
tags: [code, search, navigation, symbols]
---

# Code Search Skill

Use this skill when you need to search for code symbols, navigate a codebase,
or understand code structure.

## Available Tools

- `search-symbols`: Search for functions, classes, and variables by name
- `read-file`: Read file contents

## Best Practices

1. **Start with symbol search**: Before reading entire files, search for specific
   symbols to find exactly what you need.

2. **Use partial matches**: The search supports partial name matching, so search
   for `user` to find `UserService`, `get_user`, etc.

3. **Filter by type**: When available, filter by symbol type (function, class, variable).

4. **Navigate from symbols**: Once you find a symbol, use its file path to read
   the surrounding context.

## Example Workflow

1. User asks: "Find the login function"
2. Use `search-symbols` with query "login"
3. Review results: `login_user` in `auth/service.py:42`
4. Use `read-file` to read `auth/service.py` around line 42
