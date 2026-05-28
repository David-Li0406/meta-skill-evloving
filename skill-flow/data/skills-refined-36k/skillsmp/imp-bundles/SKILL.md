---
name: imp-bundles
description: Guide on imp-nix's 'bundles' concept and structure. Use when needing info about bundles in relation to nix, imp, git submodules, packages. 
---

# Bundles

- Drop-in reusable nix modules that get auto-imported by `imp`
- Can contain outputs and inputs with no explicit wiring to parent flake
- Derivations and configs are auto-loaded on flake reload
- Can also contain agent skills, can be managed by provided script
- Bundles are often their own git repo, and added as submodules to parent repo

## Structure

```
nix/bundles/            # parent repo's collection of bundles
  my-bundle/            # single bundle dir; often a git submodule
    default.nix         # bundle entrypoint, receives config
    config.nix          # defaults for all config values
    skills/             # optional claude code/agent skills
  my-bundle.config.nix  # project-specific overrides of config
                        # (outside of bundle dir, tracked by parent repo)
```

## config.nix (inner)

Must have all config values bundle uses. No optional fields.

```nix
{
  version = "1.0.0";
  enableFoo = true;
  exclude = [ "dist" "target" ];
}
```

## project.config.nix (outer)

Optional. Overrides inner values. Uses `lib.recursiveUpdate`. Copy `config.nix` to create this.

```nix
{
  enableFoo = false;
  exclude = [ "dist" "target" "vendor" ];  # replaces, not appends
}
```

## default.nix

Receives merged config. No fallbacks; config.nix must exist.

```nix
{
  pkgs,
  config,  # required, always provided
  ...
}:
{
  __outputs.perSystem.packages.foo = mkFoo {
    inherit (config) version;
  };
}
```

## Special Attributes

### `__outputs`

Maps to flake outputs. imp auto-collects and merges.

```nix
{
  __outputs.perSystem.packages.foo = drv;
  __outputs.perSystem.devShells.foo = mkShell { ... };
  __outputs.perSystem.checks.foo = drv;
  __outputs.perSystem.formatter = { ... };  # treefmt config
  __outputs.flake.overlays.default = final: prev: { ... };
}
```

### `__inputs`

Declare flake inputs. imp collects into parent flake.

```nix
{
  __inputs.foo.url = "github:owner/repo";
  __inputs.foo.inputs.nixpkgs.follows = "nixpkgs";
}
```

### `__functor`

Makes attrset callable. Required when using `__inputs`.

```nix
{
  __inputs.rust-overlay.url = "github:oxalica/rust-overlay";

  __functor = _: { pkgs, inputs, config, ... }: {
    __outputs.perSystem.packages.foo =
      pkgs.extend inputs.rust-overlay.overlays.default;
  };
}
```

Standard args: `pkgs`, `lib`, `system`, `self`, `self'`, `inputs`, `inputs'`, `config`, `buildDeps`

Custom args via `imp.args` in flake config (e.g. `rootSrc`).

### `buildDeps`

Share build deps between bundles.

```nix
# bundle A: provide
{ __outputs.perSystem.buildDeps.ssl.buildInputs = [ pkgs.openssl ]; }

# bundle B: consume
{ buildDeps, ... }: {
  buildInputs = buildDeps.ssl.buildInputs or [];
}
```

## Bundle Management

Use `scripts/bundle-manager.nu`. Bundles sourced from `github.com/imp-nix/bundle.<name>`.

```nu
nu bundle-manager.nu add <name>       # git submodule add
nu bundle-manager.nu remove <name>    # deinit + rm + cleanup .git/modules
nu bundle-manager.nu update [name]    # update remote (all if no name)
nu bundle-manager.nu list             # show installed (table)
nu bundle-manager.nu available        # list from imp-nix org (requires gh)
nu bundle-manager.nu info <name>      # show details (requires gh)
```

## Skill Management

Use `scripts/skill-manager.nu`. Links skills from bundles to `.claude/skills/` (project) or `~/.claude/skills/` (global).

```nu
nu skill-manager.nu link [name]       # symlink skill(s), all if no name
nu skill-manager.nu unlink <name>     # remove skill symlink
nu skill-manager.nu list              # show linked skills (table)
nu skill-manager.nu available         # list skills with descriptions (table)
nu skill-manager.nu status            # show link status for all (table)
nu skill-manager.nu link -g           # link to global ~/.claude/skills/
nu skill-manager.nu status --global   # check global skill status
```

## References

- [Migration workflow](references/migration.md) - Convert existing flake.nix to imp bundles
- [Skills structure](references/skills.md) - SKILL.md, AGENTS.md, references, scripts

## Rust Bundle

The `bundle.rust` provides nightly toolchain and rustPlatform via buildDeps.

### Consuming rust buildDeps

```nix
{ buildDeps, ... }:
let
  inherit (buildDeps.rust) rustPlatform rustToolchain;
in {
  __outputs.perSystem.packages.default = rustPlatform.buildRustPackage {
    # ...
  };
}
```

### Git Dependencies (cargoOutputHashes)

For projects with git dependencies in Cargo.lock, provide hashes via config:

```nix
# nix/bundles/rust.config.nix
{
  pname = "my-project";
  build.cargoOutputHashes = {
    "some-crate-0.1.0" = "sha256-...";
    "other-crate-0.2.0" = "sha256-...";
  };
}
```

The rust bundle merges these with any hashes from buildDeps.

### Wrapped Binary with Runtime PATH

```nix
postInstall = ''
  wrapProgram $out/bin/mytool \
    --prefix PATH : ${buildDeps.rust.rustToolchain}/bin
'';
```

## Common Patterns

### Project Bundle Consuming Shared Bundle

```nix
# nix/bundles/myproject/default.nix
{
  __functor = _: { pkgs, buildDeps, rootSrc, ... }:
  let
    inherit (buildDeps.rust) rustPlatform;
  in {
    __outputs.perSystem.packages.default = rustPlatform.buildRustPackage {
      pname = "myproject";
      src = rootSrc;
      cargoLock.lockFile = rootSrc + "/Cargo.lock";
    };

    __outputs.perSystem.buildDeps.myproject = {
      buildInputs = [ pkgs.openssl ];
    };
  };
}
```

## Gotchas

- Run `git add -A` before `nix flake check`.
- buildDeps from other bundles may not be available during evaluation. Use config options for values needed at eval time.
- The rust bundle's `checks.rust` builds a generic package. Projects with custom builds should use their own bundle's package/checks.
