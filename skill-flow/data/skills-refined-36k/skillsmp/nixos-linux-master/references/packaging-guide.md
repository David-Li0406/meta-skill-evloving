# Advanced Packaging & Compilation Guide

## Out-of-the-Box Packaging Strategies

### Zero-Config Package from Source

```nix
{ lib, stdenv, fetchFromGitHub, autoreconfHook, pkg-config }:

stdenv.mkDerivation rec {
  pname = "auto-detect-pkg";
  version = "unstable-${lib.substring 0 7 src.rev}";
  
  src = fetchFromGitHub {
    owner = "user";
    repo = "repo";
    rev = "main";
    sha256 = lib.fakeSha256;
  };
  
  # Auto-detect build system
  nativeBuildInputs = [ autoreconfHook pkg-config ]
    ++ lib.optionals (builtins.pathExists "${src}/CMakeLists.txt") [ cmake ]
    ++ lib.optionals (builtins.pathExists "${src}/meson.build") [ meson ninja ];
  
  # Auto-discover dependencies via pkg-config
  buildInputs = let
    pkgConfigDeps = builtins.fromJSON (builtins.readFile (
      runCommand "discover-deps" { buildInputs = [ pkg-config ]; } ''
        find ${src} -name "*.pc.in" -o -name "configure.ac" \
          | xargs grep -h "PKG_CHECK_MODULES" \
          | sed 's/.*PKG_CHECK_MODULES(\[.*\], \[\(.*\)\].*/\1/' \
          | jq -R . | jq -s . > $out
      ''
    ));
  in map (dep: pkgs.${dep} or null) pkgConfigDeps;
  
  meta = with lib; {
    description = "Auto-detected package";
    license = licenses.unfree;  # Detect from LICENSE file
    platforms = platforms.unix;
  };
}
```

### Language-Agnostic Build Wrapper

```nix
# buildUniversalPackage.nix
{ lib, stdenv, makeWrapper, ... }@pkgs:

{ src
, pname
, version
, buildPhase ? null
, installPhase ? null
, runtimeDeps ? []
}:

let
  # Detect language/framework
  detectBuildSystem = src:
    if builtins.pathExists "${src}/Cargo.toml" then "rust"
    else if builtins.pathExists "${src}/package.json" then "node"
    else if builtins.pathExists "${src}/setup.py" then "python"
    else if builtins.pathExists "${src}/go.mod" then "go"
    else if builtins.pathExists "${src}/Makefile" then "make"
    else "unknown";
  
  buildSystem = detectBuildSystem src;
  
  # Auto-select buildInputs
  autoBuildInputs = {
    rust = with pkgs; [ cargo rustc ];
    node = with pkgs; [ nodejs yarn ];
    python = with pkgs; [ python3 python3Packages.pip ];
    go = with pkgs; [ go ];
    make = with pkgs; [ gnumake gcc ];
  }.${buildSystem} or [];
  
  # Auto-generate build phase
  autoBuildPhase = {
    rust = "cargo build --release";
    node = "npm install && npm run build";
    python = "python setup.py build";
    go = "go build -o $pname";
    make = "make";
  }.${buildSystem} or "echo 'Unknown build system'";
  
  # Auto-generate install phase
  autoInstallPhase = {
    rust = "install -Dm755 target/release/${pname} $out/bin/${pname}";
    node = "mkdir -p $out && cp -r dist/* $out/";
    python = "python setup.py install --prefix=$out";
    go = "install -Dm755 ${pname} $out/bin/${pname}";
    make = "make install PREFIX=$out";
  }.${buildSystem} or "echo 'Unknown install system'";

in stdenv.mkDerivation {
  inherit pname version src;
  
  buildInputs = autoBuildInputs ++ runtimeDeps;
  nativeBuildInputs = [ makeWrapper ];
  
  buildPhase = buildPhase or autoBuildPhase;
  installPhase = installPhase or (autoInstallPhase + ''
    # Auto-wrap with runtime dependencies
    for bin in $out/bin/*; do
      wrapProgram $bin \
        --prefix PATH : ${lib.makeBinPath runtimeDeps}
    done
  '');
  
  meta.detectedBuildSystem = buildSystem;
}
```

## Cross-Language Compilation Patterns

### Rust + C FFI Package

```nix
{ lib, stdenv, rustPlatform, fetchFromGitHub, cmake, pkg-config, openssl }:

rustPlatform.buildRustPackage rec {
  pname = "rust-ffi-app";
  version = "0.1.0";
  
  src = fetchFromGitHub {
    owner = "example";
    repo = pname;
    rev = "v${version}";
    sha256 = lib.fakeSha256;
  };
  
  cargoSha256 = lib.fakeSha256;
  
  # C dependencies for FFI
  nativeBuildInputs = [ cmake pkg-config ];
  buildInputs = [ openssl ];
  
  # Build C library first
  preBuild = ''
    pushd c-lib
    cmake . -DCMAKE_INSTALL_PREFIX=$out
    make -j$NIX_BUILD_CORES
    make install
    popd
    
    export PKG_CONFIG_PATH=$out/lib/pkgconfig:$PKG_CONFIG_PATH
  '';
  
  # Link Rust against C lib
  postInstall = ''
    patchelf --set-rpath "${lib.makeLibraryPath [ openssl ]}:$out/lib" \
      $out/bin/${pname}
  '';
  
  meta = with lib; {
    description = "Rust app with C FFI";
    license = licenses.mit;
    maintainers = with maintainers; [ ];
  };
}
```

### Python Extension with Native Code

```nix
{ lib, python3Packages, fetchFromGitHub, cmake, boost }:

python3Packages.buildPythonPackage rec {
  pname = "native-extension";
  version = "1.0.0";
  format = "setuptools";
  
  src = fetchFromGitHub {
    owner = "example";
    repo = pname;
    rev = version;
    sha256 = lib.fakeSha256;
  };
  
  nativeBuildInputs = [ cmake python3Packages.pybind11 ];
  buildInputs = [ boost ];
  
  # Pass CMake flags to setuptools
  preBuild = ''
    export CMAKE_ARGS="-DBOOST_ROOT=${boost}"
  '';
  
  propagatedBuildInputs = with python3Packages; [
    numpy
    scipy
  ];
  
  pythonImportsCheck = [ pname ];
  
  meta = with lib; {
    description = "Python package with native extensions";
    license = licenses.asl20;
  };
}
```

## Advanced Compiler Optimization

### Profile-Guided Optimization (PGO)

```nix
{ stdenv, lib, fetchFromGitHub }:

stdenv.mkDerivation rec {
  pname = "optimized-app";
  version = "1.0.0";
  
  src = fetchFromGitHub {
    owner = "example";
    repo = pname;
    rev = version;
    sha256 = lib.fakeSha256;
  };
  
  # Two-phase build for PGO
  buildPhase = ''
    # Phase 1: Build with profiling instrumentation
    make CFLAGS="-fprofile-generate" \
         LDFLAGS="-fprofile-generate"
    
    # Run typical workload to generate profile data
    ./benchmark-suite --quick
    
    # Merge profile data
    llvm-profdata merge -output=default.profdata *.profraw || true
    
    # Phase 2: Rebuild with profile-guided optimizations
    make clean
    make CFLAGS="-fprofile-use -O3 -march=native -flto" \
         LDFLAGS="-fprofile-use -flto"
  '';
  
  installPhase = ''
    mkdir -p $out/bin
    install -Dm755 ${pname} $out/bin/${pname}
  '';
  
  meta.optimizationLevel = "pgo+lto";
}
```

### LTO (Link-Time Optimization) Pattern

```nix
{ stdenv, lib, llvmPackages }:

stdenv.mkDerivation {
  pname = "lto-optimized";
  version = "1.0.0";
  
  nativeBuildInputs = [ llvmPackages.bintools ];
  
  NIX_CFLAGS_COMPILE = [
    "-flto=thin"
    "-O3"
    "-march=native"
    "-fomit-frame-pointer"
  ];
  
  NIX_LDFLAGS = [
    "-flto=thin"
    "-fuse-ld=lld"
  ];
  
  # Parallel LTO jobs
  preBuild = ''
    export NIX_BUILD_CORES_FOR_LTO=''${NIX_BUILD_CORES:-$(nproc)}
  '';
}
```

## Containerized Build Environments

### Docker-to-Nix Bridge

```nix
{ pkgs, dockerTools, lib }:

dockerTools.buildLayeredImage {
  name = "nix-build-env";
  tag = "latest";
  
  contents = with pkgs; [
    # Base system
    coreutils bash findutils gnused gnugrep
    
    # Build essentials
    gcc gnumake cmake ninja meson
    pkg-config autoconf automake libtool
    
    # Languages
    rustc cargo go nodejs python3
    
    # Nix itself for hybrid builds
    nix cacert git
  ];
  
  config = {
    Env = [
      "PATH=/bin:/usr/bin"
      "NIX_PAGER=cat"
      "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    ];
    
    WorkingDir = "/workspace";
    
    Cmd = [ "${pkgs.bash}/bin/bash" ];
  };
  
  extraCommands = ''
    mkdir -p workspace nix/var/nix tmp
    chmod 1777 tmp
  '';
}
```

## Dynamic Library Patching

### Auto-Patchelf Wrapper

```nix
{ lib, stdenv, autoPatchelfHook, makeWrapper }:

{ pname, version, src, runtimeDependencies ? [] }:

stdenv.mkDerivation {
  inherit pname version src;
  
  nativeBuildInputs = [ autoPatchelfHook makeWrapper ];
  buildInputs = runtimeDependencies;
  
  # Don't strip - breaks some binaries
  dontStrip = true;
  
  installPhase = ''
    runHook preInstall
    
    mkdir -p $out/{bin,lib}
    cp -r * $out/
    
    # Auto-detect and patch all ELF files
    find $out -type f -executable | while read exe; do
      if file "$exe" | grep -q ELF; then
        echo "Patching: $exe"
        patchelf --set-interpreter "$(cat $NIX_CC/nix-support/dynamic-linker)" "$exe" || true
        patchelf --set-rpath "${lib.makeLibraryPath runtimeDependencies}:$out/lib" "$exe" || true
      fi
    done
    
    # Wrap binaries with LD_LIBRARY_PATH
    for bin in $out/bin/*; do
      [ -f "$bin" ] || continue
      wrapProgram "$bin" \
        --prefix LD_LIBRARY_PATH : "${lib.makeLibraryPath runtimeDependencies}:$out/lib"
    done
    
    runHook postInstall
  '';
  
  meta.platforms = lib.platforms.linux;
}
```

## Build Cache Optimization

### Incremental Build System

```nix
# In flake.nix
{
  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.default = 
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
        
        # Cache build artifacts between builds
        incrementalBuild = { name, src, buildPhase }:
          pkgs.stdenv.mkDerivation {
            inherit name src;
            
            # Use ccache for C/C++
            nativeBuildInputs = [ pkgs.ccache ];
            
            preBuild = ''
              export CCACHE_DIR=/var/cache/ccache/${name}
              mkdir -p $CCACHE_DIR
            '';
            
            inherit buildPhase;
            
            # Store ccache between builds
            postBuild = ''
              echo "Cache hit rate: $(ccache -s)"
            '';
          };
      in incrementalBuild {
        name = "my-project";
        src = ./.;
        buildPhase = "make -j$NIX_BUILD_CORES";
      };
  };
}
```

## Advanced Debugging Techniques

### Instrumented Build for Debugging

```nix
{ stdenv, lib, gdb, valgrind }:

stdenv.mkDerivation rec {
  pname = "debug-build";
  version = "dev";
  
  src = ./.;
  
  nativeBuildInputs = [ gdb valgrind ];
  
  # Debug-friendly compilation
  NIX_CFLAGS_COMPILE = [
    "-g3"              # Maximum debug info
    "-O0"              # No optimization
    "-fno-omit-frame-pointer"
    "-fno-inline"
    "-DDEBUG"
    "-fsanitize=address,undefined"  # AddressSanitizer
  ];
  
  NIX_LDFLAGS = [ "-fsanitize=address,undefined" ];
  
  # Install with debug symbols
  dontStrip = true;
  separateDebugInfo = true;
  
  installPhase = ''
    mkdir -p $out/bin $out/lib/debug
    cp -r .debug/* $out/lib/debug/ || true
    cp ${pname} $out/bin/
  '';
  
  passthru.debug = {
    run = "${gdb}/bin/gdb $out/bin/${pname}";
    valgrind = "${valgrind}/bin/valgrind --leak-check=full $out/bin/${pname}";
  };
}
```
