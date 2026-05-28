## Accessing User Context

**Impact:** MEDIUM

When you need user details (name, email), access them via `config.aytordev.user`.

**Incorrect:**

**Hardcoded Users**
Using `"aytordev"` string literals in configuration files.

**Correct:**

**Dynamic User**

```nix
let
  user = config.aytordev.user;
in
{
  programs.git.userName = user.fullName;
  programs.git.userEmail = user.email;
}
```
