## Override Precedence

**Impact:** MEDIUM

Use `lib.mkDefault` in lower layers (modules) to allow effortless overrides in higher layers (host/user configs). Avoid `lib.mkForce` unless absolutely necessary.

**Incorrect:**

**Hardcoded Module Values**
`programs.git.userName = "Default";` in a module prevents the user from overriding it without `mkForce`.

**Correct:**

**Overridable Defaults**
Define defaults in modules, specific values in configs.

```nix
# In module (Low Priority)
programs.git.userName = lib.mkDefault "Default Name";

# In host/user config (High Priority)
programs.git.userName = "Real Name";
```
