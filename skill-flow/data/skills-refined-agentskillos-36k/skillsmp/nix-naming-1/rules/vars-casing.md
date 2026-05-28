## Variable Naming

**Impact:** CRITICAL

Use `camelCase` for standard variables and `UPPER_CASE` for constants.

**Incorrect:**

**Mixed styles**
`user_name = "..."` (snake_case) or `UserName = "..."` (PascalCase).

**Correct:**

**camelCase**

```nix
let
  userName = "khaneliman";
  enableAutoStart = true;
  MAX_RETRIES = 5;
in
# ...
```
