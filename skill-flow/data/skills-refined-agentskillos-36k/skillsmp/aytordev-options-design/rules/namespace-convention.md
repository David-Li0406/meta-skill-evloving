## Namespace Convention

**Impact:** CRITICAL

ALL option definitions must live under the `aytordev.*` namespace. This prevents collisions with standard NixOS/Home Manager options.

**Incorrect:**

**Global Pollution**
Defining `programs.git.myCustomOption = ...` directly in the global namespace.

**Correct:**

**Namespaced**
`options.aytordev.programs.terminal.tools.git.enable = ...`
Always nest custom options under `aytordev`.

```nix
options.aytordev.{category}.{module}.{option} = { ... };
```
