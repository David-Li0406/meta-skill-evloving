---
name: nix-devenv
description: Sets up reproducible development environments using Nix, devenv, and direnv. Manages secrets with SOPS and age encryption. Use when setting up dev environments, configuring project dependencies, or managing environment-specific secrets.
---

# Nix + devenv + direnv + SOPS

## Quick Setup

```bash
# Initialize in existing project
nix flake init -t github:cachix/devenv

# Or create files manually (see templates below)
```

## Project Structure

```
project/
├── flake.nix          # Nix flake (inputs, outputs)
├── flake.lock         # Locked dependencies
├── devenv.nix         # Dev environment config
├── devenv.yaml        # devenv settings
├── .envrc             # direnv auto-activation
├── .sops.yaml         # SOPS encryption rules
└── secrets/
    ├── dev.yaml       # Dev secrets (encrypted)
    ├── staging.yaml   # Staging secrets (encrypted)
    └── prod.yaml      # Prod secrets (encrypted)
```

## flake.nix

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, ... }@inputs:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSystem = f: nixpkgs.lib.genAttrs systems (system: f {
        pkgs = import nixpkgs { inherit system; };
        inherit system;
      });
    in {
      devShells = forEachSystem ({ pkgs, system }: {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [ ./devenv.nix ];
        };
      });
    };
}
```

## devenv.nix

```nix
{ pkgs, ... }:

{
  name = "my-project";

  # Packages
  packages = with pkgs; [
    git gh jq yq-go
    # Add project-specific tools
  ];

  # Languages
  languages.go.enable = true;
  languages.javascript.enable = true;

  # Services (auto-managed)
  services.postgres = {
    enable = true;
    initialDatabases = [{ name = "myapp_dev"; }];
  };

  # Environment variables
  env.APP_ENV = "development";

  # Scripts
  scripts.dev.exec = "go run ./cmd/app";
  scripts.test.exec = "go test ./...";

  # Pre-commit hooks
  pre-commit.hooks = {
    nixpkgs-fmt.enable = true;
    gofmt.enable = true;
  };

  # Shell hook
  enterShell = ''
    echo "Dev environment ready"
    # Load secrets if available
    if [ -f secrets/dev.yaml ]; then
      export $(sops -d secrets/dev.yaml | yq -o=shell '.' | xargs)
    fi
  '';
}
```

## .envrc

```bash
if ! has nix_direnv_version || ! nix_direnv_version 3.0.4; then
  source_url "https://raw.githubusercontent.com/nix-community/nix-direnv/3.0.4/direnvrc" \
    "sha256-DzlYZ33mWF/Gs8DDeyjr8mnVmQGx7ASYqA5WlxwrBG4="
fi

use flake . --impure
```

After creating: `direnv allow`

## SOPS Secrets

### Setup

```bash
# Generate age key
age-keygen -o ~/.config/sops/age/keys.txt
age-keygen -y ~/.config/sops/age/keys.txt  # Get public key
```

### .sops.yaml

```yaml
creation_rules:
  - path_regex: secrets/dev\.yaml$
    age: age1xxxxx  # Dev public key

  - path_regex: secrets/staging\.yaml$
    age: age1yyyyy  # Staging public key

  - path_regex: secrets/prod\.yaml$
    kms: arn:aws:kms:...  # Production uses KMS
    age: age1zzzzz
```

### Manage Secrets

```bash
# Create/edit secrets
sops secrets/dev.yaml

# Example secrets file (before encryption)
database:
  password: secret123
api:
  jwt_secret: my-jwt-key
```

### Use in Code

```bash
# In shell/scripts
export $(sops -d secrets/dev.yaml | yq -o=shell '.' | xargs)
echo $database_password
```

## Common Commands

```bash
# Enter environment
direnv allow        # First time
cd project/         # Auto-activates after

# Manage services
devenv up           # Start all services
devenv up postgres  # Start specific service

# Update dependencies
nix flake update

# Check environment
devenv info
```

## Environment Parity

| Environment | Config Source | Secrets |
|-------------|---------------|---------|
| Development | devenv.nix + services | SOPS (age key) |
| Staging | Same flake, different vars | SOPS (age key) |
| Production | Container from flake | SOPS (KMS + age) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `direnv: error .envrc blocked` | Run `direnv allow` |
| SOPS decrypt fails | Check `~/.config/sops/age/keys.txt` |
| Slow builds | Set up Cachix: `cachix use devenv` |
| Service port in use | `devenv down` or check `lsof -i :PORT` |
