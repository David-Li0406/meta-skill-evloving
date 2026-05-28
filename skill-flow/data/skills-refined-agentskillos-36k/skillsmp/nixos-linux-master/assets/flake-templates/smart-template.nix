{
  description = "Production-ready multi-language flake template";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      rust-overlay,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        overlays = [ rust-overlay.overlays.default ];
        pkgs = import nixpkgs { inherit system overlays; };

        # Intelligent language detection
        projectType =
          if builtins.pathExists ./Cargo.toml then
            "rust"
          else if builtins.pathExists ./package.json then
            "node"
          else if builtins.pathExists ./go.mod then
            "go"
          else if builtins.pathExists ./pyproject.toml then
            "python"
          else
            "generic";

        # Language-specific toolchains
        rustTools = with pkgs; [
          (rust-bin.stable.latest.default.override {
            extensions = [
              "rust-src"
              "rust-analyzer"
            ];
          })
          cargo-watch
          cargo-edit
          cargo-audit
        ];

        nodeTools = with pkgs; [
          nodejs_20
          nodePackages.typescript
          nodePackages.pnpm
          yarn
        ];

        pythonTools = with pkgs; [
          (python311.withPackages (
            ps: with ps; [
              pip
              setuptools
              wheel
            ]
          ))
          ruff
          black
          mypy
        ];

        goTools = with pkgs; [
          go_1_21
          gopls
          gotools
          delve
        ];

        # Select tools based on project type
        devTools =
          {
            rust = rustTools;
            node = nodeTools;
            python = pythonTools;
            go = goTools;
            generic = [ ];
          }
          .${projectType};

      in
      {
        devShells.default = pkgs.mkShell {
          name = "${projectType}-dev-shell";

          buildInputs =
            devTools
            ++ (with pkgs; [
              # Universal tooling
              git
              direnv
              just
              ripgrep
              fd
            ]);

          shellHook = ''
            echo "🚀 ${projectType} development environment"
            echo "   Project: ${self.lastModifiedDate or "unknown"}"

            # Language-specific setup
            ${
              if projectType == "rust" then
                ''
                  export RUST_BACKTRACE=1
                  rustc --version
                ''
              else if projectType == "node" then
                ''
                  export NODE_ENV=development
                  node --version
                ''
              else if projectType == "python" then
                ''
                  export PYTHONPATH="$PWD:$PYTHONPATH"
                  python --version
                ''
              else if projectType == "go" then
                ''
                  export GOPATH="$HOME/go"
                  go version
                ''
              else
                ""
            }
          '';
        };

        # Auto-generated package based on type
        packages.default =
          if projectType == "rust" then
            pkgs.rustPlatform.buildRustPackage {
              pname = "rust-app";
              version = "0.1.0";
              src = ./.;
              cargoLock.lockFile = ./Cargo.lock;
            }
          else
            pkgs.writeShellScriptBin "build-script" ''
              echo "No package definition for ${projectType}"
            '';
      }
    );
}
