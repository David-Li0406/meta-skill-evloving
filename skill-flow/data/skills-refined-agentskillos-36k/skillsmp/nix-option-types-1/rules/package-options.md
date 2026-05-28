## Package Options

**Impact:** MEDIUM

Use `lib.mkPackageOption` for options that accept a package. It automatically searches `pkgs` and generates a good default description.

**Incorrect:**

**Manual Default**
`type = types.package; default = pkgs.git;` works but is less standard.

**Correct:**

**Helper**

```nix
package = lib.mkPackageOption pkgs "git" { };
```
