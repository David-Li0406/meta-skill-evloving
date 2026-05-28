---
name: nix-validation
description: Use this skill when validating Nix code or setting up linting infrastructure with automated tools and manual checks.
---

# Nix Validation & Linting

## Tool Overview

| Tool                      | Purpose                        | Speed   |
| ------------------------- | ------------------------------ | ------- |
| `nix-instantiate --parse` | Syntax check only              | Instant |
| `nixfmt`                  | Official formatter (RFC-style) | Fast    |
| `statix`                  | Linter for anti-patterns       | Fast    |
| `deadnix`                 | Find unused code               | Fast    |
| `nix flake check`         | Full evaluation + checks       | Slow    |

## treefmt-nix Integration

The recommended way to combine all tools:

```nix
# flake.nix
{
  inputs.treefmt-nix.url = "github:numtide/treefmt-nix";

  outputs = { self, nixpkgs, treefmt-nix, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.''${system};
      treefmtEval = treefmt-nix.lib.evalModule pkgs {
        projectRootFile = "flake.nix";
        programs = {
          nixfmt.enable = true;  # or nixfmt-rfc-style
          deadnix.enable = true;
          statix.enable = true;
        };
      };
    in {
      formatter.''${system} = treefmtEval.config.build.wrapper;
      checks.''${system}.formatting = treefmtEval.config.build.check self;
    };
}
```

## Statix Lints (Anti-Patterns)

| Lint                  | Issue                      | Fix                   |
| --------------------- | -------------------------- | --------------------- |
| `bool_comparison`     | `x == true`                | Just use `x`          |
| `empty_let_in`        | `let in expr`              | Remove let-in         |
| `eta_reduction`       | `x: f x`                   | Just use `f`          |
| `manual_inherit`      | `x = x;`                   | Use `inherit x;`      |
| `manual_inherit_from` | `x = a.x;`                 | Use `inherit (a) x;`  |
| `legacy_let_syntax`   | `let { x = 1; body = x; }` | Use `let x = 1; in x` |
| `unquoted_uri`        | `https://...`              | Quote the URI         |
| `useless_parens`      | `(expr)` when not needed   | Remove parens         |

```bash
# Check for anti-patterns
statix check .

# Auto-fix what's possible
statix fix .

# Ignore specific lint
# Add to file: # statix: ignore manual_inherit
```