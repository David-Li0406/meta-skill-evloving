# Nix Patterns Reference

Detailed Nix language patterns and flake-parts architecture for this repository.

## Flake-Parts Structure

This repository uses flake-parts for modular flake organization:

```nix
{
  outputs = inputs @ { self, nixpkgs, home-manager, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-darwin" ];
      
      perSystem = { self', system, pkgs, lib, config, inputs', ... }: let
        # Per-system definitions
        overlays = [ (import ./overlays/vscode-insiders.nix) ];
        pkgs = import self.inputs.nixpkgs {
          inherit system overlays;
          config.allowUnfree = true;
        };
        util = import ./lib { inherit inputs pkgs home-manager system lib overlays; };
        inherit (util) host user shell;
      in {
        legacyPackages.nixosConfigurations = { ... };
        legacyPackages.homeManagerConfigurations = { ... };
      };
    };
}
```

## lib/ Functions

### host.mkHost
Creates NixOS system configurations:

```nix
mkHost = {
  name,                    # Hostname
  NICs,                    # Network interfaces
  initrdAvailableMods,     # Available kernel modules for initrd
  initrdMods,              # Loaded kernel modules for initrd
  kernelMods,              # Kernel modules to load
  kernelPatches,           # Kernel patches
  kernelParams,            # Kernel command line params
  kernelPackage,           # Kernel package (e.g., pkgs.linuxPackages_latest)
  roles,                   # List of role names from roles/
  machine,                 # List of machine configs from machines/
  cpuCores,                # Number of CPU cores
  users,                   # List of user definitions
  wifi ? [],               # Wireless interfaces
  gpuTempSensor ? null,
  cpuTempSensor ? null
}: ...
```

Key behavior:
- Imports roles from `roles/{role-name}/default.nix`
- Imports machine configs from `machines/{name}/default.nix`
- Creates system users from `users` list
- Passes `util` to all modules via `specialArgs`
- Writes system data to `/etc/hmsystemdata.json`

### user.mkHMUser
Creates home-manager configurations:

```nix
mkHMUser = {
  roles,      # List of role paths from roles/home-manager/
  username    # Username
}: ...
```

Key behavior:
- Imports roles from `roles/home-manager/{role}/default.nix`
- Supports nested paths: `"core-apps/neovim"` → `roles/home-manager/core-apps/neovim/`
- Sets home directory based on platform (Linux vs Darwin)
- Imports sops-nix home-manager module
- Passes `util` and `inputs` via `extraSpecialArgs`

## Role Patterns

### NixOS Role Template
```nix
# roles/my-role/default.nix
{ config, pkgs, lib, util, inputs, ... }:
{
  # Import sub-modules
  imports = [ ./sub-config.nix ];
  
  # System packages
  environment.systemPackages = with pkgs; [ package1 package2 ];
  
  # Services
  services.myservice = {
    enable = true;
    settings = { ... };
  };
  
  # With SOPS secrets (using template API)
  # See sops.nix reference for full pattern
}
```

### Home-Manager Role Template
```nix
# roles/home-manager/my-role/default.nix
{ config, pkgs, lib, util, ... }:
{
  # User packages
  home.packages = with pkgs; [ package1 package2 ];
  
  # Programs configuration
  programs.myprogram = {
    enable = true;
    extraConfig = ''...'';
  };
  
  # Dotfiles
  home.file.".config/myapp/config".source = ./config;
  
  # Session variables
  home.sessionVariables = {
    MY_VAR = "value";
  };
}
```

### Role with SOPS (Template Pattern)
```nix
{ lib, config, pkgs, util, ... }:

(util.sops.mkSecretsAndTemplatesConfig
  # Secrets
  [
    (util.sops.userSecret "secret-name" "file.yaml" "key")
  ]
  # Templates
  [
    (util.sops.envTemplate "env-name" { VAR = "secret-name"; })
  ]
  # Config
  {
    home.packages = [ pkgs.package ];
  }
) { inherit config lib; }
```

## Overlay Creation

Overlays modify or add packages to nixpkgs:

```nix
# overlays/my-overlay.nix
final: prev: {
  my-package = prev.my-package.overrideAttrs (oldAttrs: {
    version = "new-version";
    src = prev.fetchurl { ... };
  });
  
  # Or create new derivation
  new-package = prev.stdenv.mkDerivation { ... };
}
```

Usage in flake.nix:
```nix
overlays = [
  (import ./overlays/my-overlay.nix)
];
pkgs = import nixpkgs { inherit system overlays; };
```

## Common Nix Patterns

### Conditional Configuration
```nix
{ config, lib, ... }:
with lib;
{
  config = mkIf config.services.myservice.enable {
    environment.systemPackages = [ ... ];
  };
}
```

### Merging Configurations
```nix
{
  config = mkMerge [
    { always.applied = true; }
    (mkIf condition { conditional.config = true; })
  ];
}
```

### Optional Attributes
```nix
{
  myConfig = {
    required = "value";
  } // optionalAttrs (condition) {
    optional = "only if condition";
  };
}
```

### Module Options
```nix
{ config, lib, pkgs, ... }:
with lib;
{
  options.mymodule = {
    enable = mkEnableOption "my module";
    setting = mkOption {
      type = types.str;
      default = "default";
      description = "A setting";
    };
  };
  
  config = mkIf config.mymodule.enable {
    # Configuration when enabled
  };
}
```

## Debugging

### Evaluation Errors
```bash
# Full trace
nix build .#nixosConfigurations.HOST.config.system.build.toplevel --show-trace

# Evaluate specific value
nix eval .#nixosConfigurations.HOST.config.networking.hostName

# REPL exploration
nix repl
:lf .
nixosConfigurations.HOST.config.services
```

### Common Errors

**infinite recursion**: Usually caused by self-referential imports or options
```nix
# Wrong - imports itself
imports = [ ./. ];

# Wrong - option references itself in default
myOption = mkOption {
  default = config.myOption;  # infinite recursion!
};
```

**attribute missing**: Check spelling and that module is imported
```bash
# Find where attribute is defined
grep -r "myAttribute" roles/
```

**file not found in flake**: Files must be git-tracked
```bash
git add .
nix build ...
```

## Updating Flake Inputs

```bash
# Update all inputs
nix flake update

# Update specific input
nix flake lock --update-input nixpkgs
nix flake lock --update-input home-manager

# Check what would change
nix flake update --dry-run
```

## Platform-Specific Patterns

### Detecting Platform
```nix
{ pkgs, lib, ... }:
{
  home.packages = with pkgs; [
    common-package
  ] ++ lib.optionals pkgs.stdenv.isLinux [
    linux-only-package
  ] ++ lib.optionals pkgs.stdenv.isDarwin [
    darwin-only-package
  ];
}
```

### Platform-Specific Paths
```nix
let
  homeDirectory = if pkgs.stdenv.isDarwin
    then "/Users/${username}"
    else "/home/${username}";
  
  ageKeyPath = if pkgs.stdenv.isDarwin
    then "${homeDirectory}/Library/Application Support/sops/age/keys.txt"
    else "/var/lib/sops-nix/keys.txt";
in { ... }
```
