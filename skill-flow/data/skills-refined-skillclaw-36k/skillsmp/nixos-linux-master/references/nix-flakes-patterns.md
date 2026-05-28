# Advanced Nix Flakes Patterns

## Multi-System Flake Architecture

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = nixpkgs.lib;
      in {
        # Development environments
        devShells = import ./shells { inherit pkgs lib; };
        
        # Custom packages
        packages = import ./packages { inherit pkgs lib self; };
        
        # Overlays for package modifications
        overlays.default = final: prev: {
          # Your custom packages here
        };
      }
    ) // {
      # NixOS configurations (not system-specific)
      nixosConfigurations = import ./hosts { inherit inputs; };
      
      # Home Manager configurations
      homeConfigurations = import ./home { inherit inputs; };
    };
}
```

## Modular Package Development

### Pattern: Derivation with Multiple Outputs

```nix
{ stdenv, lib, fetchFromGitHub, cmake, pkg-config }:

stdenv.mkDerivation rec {
  pname = "multi-output-pkg";
  version = "1.0.0";
  
  outputs = [ "out" "dev" "doc" "man" ];
  
  src = fetchFromGitHub {
    owner = "example";
    repo = pname;
    rev = version;
    sha256 = lib.fakeSha256;  # Replace with actual hash
  };
  
  nativeBuildInputs = [ cmake pkg-config ];
  
  cmakeFlags = [
    "-DBUILD_SHARED_LIBS=ON"
    "-DENABLE_OPTIMIZATIONS=ON"
  ];
  
  postInstall = ''
    moveToOutput "include" "$dev"
    moveToOutput "share/doc" "$doc"
    moveToOutput "share/man" "$man"
  '';
  
  meta = with lib; {
    description = "Example multi-output package";
    license = licenses.mit;
    platforms = platforms.linux;
    maintainers = with maintainers; [ /* your name */ ];
  };
}
```

## Cross-Compilation Patterns

```nix
# Build for ARM64 from x86_64
let
  crossSystem = {
    config = "aarch64-unknown-linux-gnu";
  };
  
  pkgs = import nixpkgs { 
    inherit system crossSystem;
  };
in pkgs.yourPackage
```

## Binary Cache Integration

```nix
# In flake.nix or NixOS configuration
nix.settings = {
  substituters = [
    "https://cache.nixos.org"
    "https://your-private-cache.example.com"
  ];
  trusted-public-keys = [
    "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
    "your-cache:YOUR_PUBLIC_KEY_HERE"
  ];
  builders-use-substitutes = true;
};
```

## Override and Overlay Techniques

### Advanced Override Pattern

```nix
# Override specific dependency versions
pkgs.pythonPackages.yourPackage.override {
  numpy = pkgs.python3Packages.numpy.overridePythonAttrs (old: {
    version = "1.24.0";
    src = pkgs.fetchPypi {
      pname = "numpy";
      version = "1.24.0";
      sha256 = "...";
    };
  });
}

# Override build inputs
pkgs.yourPackage.overrideAttrs (old: {
  buildInputs = old.buildInputs ++ [ pkgs.additionalDep ];
  patches = old.patches or [] ++ [ ./custom.patch ];
  NIX_CFLAGS_COMPILE = "-O3 -march=native";
})
```

### Overlay for System-Wide Modifications

```nix
# In configuration.nix or flake overlays
nixpkgs.overlays = [
  (final: prev: {
    # Replace package entirely
    customPkg = prev.customPkg.override { enableFeature = true; };
    
    # Add new package
    myTool = final.callPackage ./pkgs/my-tool { };
    
    # Modify existing package
    vim = prev.vim.overrideAttrs (old: {
      postInstall = old.postInstall + ''
        echo "Custom vim build"
      '';
    });
  })
];
```

## Development Shell Best Practices

```nix
pkgs.mkShell {
  name = "rust-dev-env";
  
  # Build-time dependencies
  nativeBuildInputs = with pkgs; [
    rustc
    cargo
    rust-analyzer
    rustfmt
    clippy
  ];
  
  # Runtime dependencies
  buildInputs = with pkgs; [
    openssl
    pkg-config
    libgit2
  ];
  
  # Environment variables
  RUST_BACKTRACE = "1";
  DATABASE_URL = "postgres://localhost/devdb";
  
  # Shell hook for setup
  shellHook = ''
    export PATH="$PWD/target/debug:$PATH"
    echo "Rust development environment loaded"
    echo "Rust version: $(rustc --version)"
    
    # Auto-create directories
    mkdir -p .cargo
    
    # Set up pre-commit hooks
    if [ ! -f .git/hooks/pre-commit ]; then
      cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
cargo fmt --check && cargo clippy
EOF
      chmod +x .git/hooks/pre-commit
    fi
  '';
  
  # Passthru for additional metadata
  passthru = {
    updateScript = ./update.sh;
  };
}
```

## Flake Lock Management

```bash
# Update specific input
nix flake lock --update-input nixpkgs

# Update all inputs
nix flake update

# Use specific commit
nix flake lock --override-input nixpkgs github:NixOS/nixpkgs/COMMIT_HASH

# Show flake metadata without building
nix flake metadata

# Show dependency tree
nix flake show
```

## Non-Reproducible Source Handling

```nix
# For git repos without tags
src = pkgs.fetchFromGitHub {
  owner = "user";
  repo = "repo";
  rev = "main";  # Branch name
  sha256 = pkgs.lib.fakeSha256;
  # Use: nix-prefetch-url --unpack https://github.com/user/repo/archive/main.tar.gz
};

# For frequently updated sources
src = pkgs.fetchzip {
  url = "https://example.com/archive.zip";
  sha256 = pkgs.lib.fakeSha256;
  stripRoot = false;
};

# Git with fetchgit for submodules
src = pkgs.fetchgit {
  url = "https://github.com/user/repo.git";
  rev = "COMMIT_HASH";
  sha256 = pkgs.lib.fakeSha256;
  fetchSubmodules = true;
  deepClone = false;
  leaveDotGit = false;
};
```

## Conditional Build Logic

```nix
{ stdenv, lib, enableCuda ? false, cudaPackages ? null }:

assert enableCuda -> cudaPackages != null;

stdenv.mkDerivation {
  pname = "conditional-pkg";
  
  buildInputs = lib.optionals enableCuda [
    cudaPackages.cuda_cudart
    cudaPackages.cuda_nvcc
  ];
  
  configureFlags = lib.optional enableCuda "--enable-cuda";
  
  meta = {
    platforms = if enableCuda 
                then lib.platforms.linux 
                else lib.platforms.unix;
  };
}
```

## Testing and CI Integration

```nix
# tests.nix
{ pkgs, lib }:

let
  myPackage = pkgs.callPackage ./default.nix { };
in {
  # Unit tests
  unit = pkgs.runCommand "unit-tests" { } ''
    ${myPackage}/bin/my-tool --test
    touch $out
  '';
  
  # Integration tests
  integration = pkgs.nixosTest {
    name = "my-service-test";
    nodes.machine = { pkgs, ... }: {
      services.myService.enable = true;
    };
    testScript = ''
      machine.wait_for_unit("my-service.service")
      machine.succeed("curl http://localhost:8080")
    '';
  };
  
  # VM tests
  vm-test = import ./vm-test.nix { inherit pkgs lib; };
}
```
