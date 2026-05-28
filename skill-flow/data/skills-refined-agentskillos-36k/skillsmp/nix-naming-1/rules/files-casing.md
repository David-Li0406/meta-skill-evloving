## File Naming

**Impact:** HIGH

Use `kebab-case` for all files and directories. This is standard in the Nix community and avoids case-sensitivity issues on some filesystems.

**Incorrect:**

**Camel or Snake**
`modules/home/myApp/default.nix` or `my_service.nix`.

**Correct:**

**kebab-case**

```
modules/home/programs/my-app/default.nix
modules/nixos/services/my-service.nix
```
