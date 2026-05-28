## Attribute Organization

**Impact:** MEDIUM

Organize module attributes logically: `imports`, `options`, then `config`. Inside `config`, group settings by module. Ideally use the `cfg` pattern.

**Incorrect:**

**Scattered configs**
Interleaving options and config, or scattering `home.packages` throughout the file.

**Correct:**

**Structured**

```nix
{
  imports = [ ... ];

  options.namespace.module = { ... };

  config = lib.mkIf cfg.enable {
    programs.git = { ... };
    home.packages = [ ... ];
  };
}
```
