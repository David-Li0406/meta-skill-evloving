#!/usr/bin/env bash
# flake-scaffold.sh - Advanced flake generator

set -euo pipefail

PROJECT_NAME="${1:-my-project}"
PROJECT_TYPE="${2:-multi-env}"

echo "🚀 Creating advanced Flake structure: $PROJECT_NAME"
echo "   Type: $PROJECT_TYPE"

mkdir -p "$PROJECT_NAME"/{hosts,modules,packages,overlays,lib}

# Generate flake.nix based on type
cat > "$PROJECT_NAME/flake.nix" << 'EOF'
{
  description = "Advanced multi-environment flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    
    # Home Manager
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    
    # Rust toolchain
    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    
    # Pre-commit hooks
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, home-manager, rust-overlay, pre-commit-hooks }@inputs:
    let
      lib = nixpkgs.lib.extend (final: prev: import ./lib { lib = prev; });
      
      # Per-system outputs
      systemOutputs = flake-utils.lib.eachDefaultSystem (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              rust-overlay.overlays.default
              self.overlays.default
            ];
            config.allowUnfree = true;
          };
          
        in {
          # Development environments
          devShells = import ./shells { inherit pkgs lib system; };
          
          # Custom packages
          packages = import ./packages { inherit pkgs lib self; };
          
          # Pre-commit hooks
          checks = {
            pre-commit = pre-commit-hooks.lib.${system}.run {
              src = ./.;
              hooks = {
                nixpkgs-fmt.enable = true;
                statix.enable = true;
                deadnix.enable = true;
              };
            };
          };
          
          # Formatters
          formatter = pkgs.nixpkgs-fmt;
        }
      );
      
    in systemOutputs // {
      # System-agnostic outputs
      overlays.default = import ./overlays { inherit lib; };
      
      nixosModules.default = import ./modules;
      
      # NixOS configurations
      nixosConfigurations = import ./hosts { 
        inherit inputs lib self; 
        inherit (nixpkgs) lib;
      };
      
      # Templates
      templates = {
        rust-app = {
          path = ./templates/rust-app;
          description = "Rust application with full flake integration";
        };
        node-app = {
          path = ./templates/node-app;
          description = "Node.js application with TypeScript";
        };
      };
      
      # Library functions
      lib = import ./lib { inherit (nixpkgs) lib; };
    };
}
EOF

# Create development shells structure
mkdir -p "$PROJECT_NAME/shells"
cat > "$PROJECT_NAME/shells/default.nix" << 'EOF'
{ pkgs, lib, system }:

{
  # Rust development environment
  rust = pkgs.mkShell {
    name = "rust-dev";
    
    buildInputs = with pkgs; [
      (rust-bin.stable.latest.default.override {
        extensions = [ "rust-src" "rust-analyzer" ];
        targets = [ "x86_64-unknown-linux-gnu" "wasm32-unknown-unknown" ];
      })
      cargo-watch
      cargo-audit
      cargo-edit
      bacon
    ];
    
    shellHook = ''
      export RUST_BACKTRACE=1
      echo "🦀 Rust dev environment loaded"
      rustc --version
    '';
  };
  
  # Python with ML/AI stack
  python = pkgs.mkShell {
    name = "python-ml";
    
    buildInputs = with pkgs; [
      (python311.withPackages (ps: with ps; [
        numpy
        pandas
        pytorch
        scikit-learn
        jupyter
        matplotlib
      ]))
      ruff
      mypy
      black
    ];
    
    shellHook = ''
      export PYTHONPATH="$PWD:$PYTHONPATH"
      echo "🐍 Python ML environment loaded"
      python --version
    '';
  };
  
  # Node.js/TypeScript
  node = pkgs.mkShell {
    name = "node-dev";
    
    buildInputs = with pkgs; [
      nodejs_20
      nodePackages.typescript
      nodePackages.typescript-language-server
      nodePackages.prettier
      nodePackages.eslint
      yarn
      pnpm
    ];
    
    shellHook = ''
      export NODE_ENV=development
      echo "⬢ Node.js environment loaded"
      node --version
      npm --version
    '';
  };
  
  # Go development
  go = pkgs.mkShell {
    name = "go-dev";
    
    buildInputs = with pkgs; [
      go_1_21
      gopls
      gotools
      go-tools
      delve
    ];
    
    shellHook = ''
      export GOPATH="$HOME/go"
      export PATH="$GOPATH/bin:$PATH"
      echo "🔷 Go environment loaded"
      go version
    '';
  };
  
  # Full-stack development
  fullstack = pkgs.mkShell {
    name = "fullstack-dev";
    
    buildInputs = with pkgs; [
      # Backend
      nodejs_20
      (python311.withPackages (ps: [ ps.fastapi ps.uvicorn ]))
      
      # Frontend
      nodePackages.typescript
      tailwindcss
      
      # Database
      postgresql
      redis
      
      # Tools
      docker
      docker-compose
      git
      curl
      jq
    ];
    
    shellHook = ''
      export DATABASE_URL="postgres://localhost/dev"
      export REDIS_URL="redis://localhost:6379"
      echo "🌐 Full-stack environment loaded"
    '';
  };
  
  # Default to rust
  default = self.rust;
}
EOF

# Create packages structure
cat > "$PROJECT_NAME/packages/default.nix" << 'EOF'
{ pkgs, lib, self }:

{
  # Example package
  hello-world = pkgs.writeShellScriptBin "hello-world" ''
    echo "Hello from ${self.rev or "development"}!"
  '';
  
  # Import other packages
  # my-package = pkgs.callPackage ./my-package { };
}
EOF

# Create overlays
cat > "$PROJECT_NAME/overlays/default.nix" << 'EOF'
{ lib }:

final: prev: {
  # Custom package modifications
  # my-modified-pkg = prev.my-pkg.overrideAttrs (old: {
  #   version = "custom";
  # });
}
EOF

# Create lib structure
cat > "$PROJECT_NAME/lib/default.nix" << 'EOF'
{ lib }:

{
  # Helper functions
  mkFlakeApp = { drv, name ? drv.pname or drv.name }:
    {
      type = "app";
      program = "${drv}/bin/${name}";
    };
  
  # More utilities...
}
EOF

# Create modules structure
cat > "$PROJECT_NAME/modules/default.nix" << 'EOF'
{ ... }:

{
  imports = [
    # ./my-module.nix
  ];
}
EOF

# Create a sample host configuration
mkdir -p "$PROJECT_NAME/hosts/example"
cat > "$PROJECT_NAME/hosts/default.nix" << 'EOF'
{ inputs, lib, self, ... }:

{
  example = lib.nixosSystem {
    system = "x86_64-linux";
    specialArgs = { inherit inputs; };
    modules = [
      ./example/configuration.nix
      self.nixosModules.default
      inputs.home-manager.nixosModules.home-manager
    ];
  };
}
EOF

cat > "$PROJECT_NAME/hosts/example/configuration.nix" << 'EOF'
{ config, pkgs, ... }:

{
  imports = [ ];

  system.stateVersion = "24.05";
  
  networking.hostName = "example";
  
  # Example configuration
  environment.systemPackages = with pkgs; [
    vim
    git
  ];
}
EOF

# Create .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'EOF'
result
result-*
.direnv
.envrc
*.qcow2
EOF

# Create README
cat > "$PROJECT_NAME/README.md" << 'EOF'
# Advanced Nix Flake

## Quick Start

```bash
# Enter development environment
nix develop

# Enter specific environment
nix develop .#python
nix develop .#rust
nix develop .#node

# Build packages
nix build .#hello-world

# Run checks
nix flake check
```

## Structure

- `flake.nix` - Main flake definition
- `shells/` - Development environments
- `packages/` - Custom packages
- `overlays/` - Package overlays
- `modules/` - NixOS modules
- `hosts/` - NixOS configurations
- `lib/` - Helper functions

## Development Environments

Multiple specialized environments available:
- Rust (default)
- Python with ML/AI
- Node.js/TypeScript
- Go
- Full-stack

## NixOS Configuration

```bash
# Build system configuration
nixos-rebuild switch --flake .#example
```
EOF

# Create direnv support
cat > "$PROJECT_NAME/.envrc" << 'EOF'
use flake
EOF

# Make it executable
chmod +x "$PROJECT_NAME/flake-scaffold.sh" 2>/dev/null || true

cd "$PROJECT_NAME"

# Initialize git
git init
git add .

echo ""
echo "✅ Flake structure created successfully!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  nix develop    # Enter default dev environment"
echo "  nix flake show # See all outputs"
echo ""
echo "Available shells:"
echo "  nix develop .#rust      - Rust development"
echo "  nix develop .#python    - Python ML/AI"
echo "  nix develop .#node      - Node.js/TypeScript"
echo "  nix develop .#go        - Go development"
echo "  nix develop .#fullstack - Full-stack development"
