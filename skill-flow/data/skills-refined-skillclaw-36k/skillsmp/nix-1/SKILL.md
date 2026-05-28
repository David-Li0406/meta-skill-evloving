---
name: nix
description: Write Nix code and manage NixOS/home-manager configurations. Use when writing Nix expressions, flakes, modules, or debugging derivations.
---

# Nix

## References

- **Nix Manual**: https://nix.dev/manual/nix/latest/
- **Nixpkgs Manual**: https://nixos.org/manual/nixpkgs/stable/
- **NixOS Manual**: https://nixos.org/manual/nixos/stable/
- **NixOS Wiki**: https://wiki.nixos.org/
- **home-manager Manual**: https://nix-community.github.io/home-manager/
- **nix.dev** (tutorials): https://nix.dev/
- **Flakes**: https://wiki.nixos.org/wiki/Flakes

## CLI Tools

```sh
nix-search <query>           # Package search (nix-search-cli, fast)
nix-search --name <name>     #   by package name (supports glob: 'emacsPackages.*')
nix-search --program <prog>  #   by installed program
nix-search --details <query> #   show details (description, programs, etc.)
nix-search --flakes <query>  #   search flakes instead of nixpkgs
nix flake show            # Show flake outputs
nix flake check           # Validate flake
nix repl                  # Interactive REPL
nix eval .#<attr>         # Evaluate expression
nix build .#<pkg>         # Build package
nix develop               # Enter dev shell
nix-tree                  # Dependency tree visualization
nixos-rebuild switch      # Apply NixOS config
home-manager switch       # Apply home-manager config
```

## Workflow

- **Always `git add` new files** - Flakes only see git-tracked files

## MCP Servers

- **context7**: Use `mcp__context7__resolve-library-id` with "nix" or "nixos" to fetch docs

## Module Pattern

```nix
{ config, lib, pkgs, ... }:
let
  cfg = config.my.module;
in {
  options.my.module = {
    enable = lib.mkEnableOption "my module";
    package = lib.mkPackageOption pkgs "pkg-name" {};
  };

  config = lib.mkIf cfg.enable {
    # configuration here
  };
}
```

or, flat:

```nix
{
  programs.git.enable = true;
}
```

## Best Practices

1. **Use `lib.mkIf`** - Not raw `if` for conditional config
2. **Use `lib.mkMerge`** - Combine multiple config sets
3. **Avoid `with pkgs;`** - Pollutes scope, use explicit `pkgs.foo`
4. **Use `lib.optionals`** - For conditional list items
5. **Pin nixpkgs** - Lock flake inputs for reproducibility

## Anti-Patterns

1. **`import <nixpkgs>`** - Use flake inputs instead
2. **Hardcoded paths** - Use `${pkg}` interpolation
3. **`rec { }`** - Prefer `let ... in` or recursive `finalAttrs` pattern
4. **`assert` for user errors** - Use `lib.assertMsg` with message

## Debugging

```sh
nix repl                           # Then :l <nixpkgs>
nix eval --raw .#foo               # Print derivation path
nix log /nix/store/<hash>-foo      # Build logs
nix-store -qR <drv>                # Runtime deps
nix-store -qd <drv>                # Build deps
nix why-depends .#a .#b            # Dependency chain
```

## Common Fixes

**"infinite recursion"** - Check for self-referencing `rec`, use `let` instead
**"attribute not found"** - Check spelling, use `pkgs.lib.attrNames` to list
**"cannot coerce"** - Wrap strings: `"${toString val}"`
**"IFD (import from derivation)"** - Avoid in flakes, causes evaluation-time builds
