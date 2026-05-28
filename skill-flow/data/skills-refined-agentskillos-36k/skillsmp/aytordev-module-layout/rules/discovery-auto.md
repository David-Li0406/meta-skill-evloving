## Auto-Discovery

**Impact:** MEDIUM

Modules are automatically imported via `importModulesRecursive`. You do not need manual imports for standard modules; just enable them via options.

**Incorrect:**

**Manual Imports**
`imports = [ ../../some-module/default.nix ];` when the module is already part of the auto-discovery tree.

**Correct:**

**Option Enablement**
Place the file in the correct directory, then enable it:
`aytordev.programs.foo.enable = true;`

(Only use manual imports for `modules/common/` from platform-specific modules).
