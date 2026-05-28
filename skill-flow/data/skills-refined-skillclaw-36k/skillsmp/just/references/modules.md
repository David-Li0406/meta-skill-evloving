# Just Modules Reference

Modules provide namespaced recipe organization. Unlike `import` (which merges recipes), `mod` creates separate namespaces called with `::` syntax.

## Basic Usage

```just
# justfile
mod docker    # Loads docker.just, recipes called as docker::*
mod go        # Loads go.just, recipes called as go::*
```

```just
# docker.just
build:
    docker build -t myapp .

push:
    docker push myapp
```

```bash
# Calling module recipes
just docker::build
just docker::push
just go::test
```

## Module Declaration

```just
# Load from same directory (default)
mod name                    # Loads name.just

# Load from subdirectory
mod name 'path/to/name.just'

# Optional module (no error if missing)
mod? optional
```

## Directory Structure Patterns

### Flat Structure

```
project/
├── justfile         # mod docker, mod go
├── docker.just
├── go.just
└── release.just
```

### Nested Structure

```
project/
├── justfile         # import 'just/justfile'
└── just/
    ├── justfile     # mod docker, mod go, import 'dev.just'
    ├── dev.just     # Imported (no namespace)
    ├── docker.just  # Module (docker::*)
    ├── go.just      # Module (go::*)
    └── release.just # Module (release::*)
```

## Import vs Module

| Feature | `import` | `mod` |
|---------|----------|-------|
| Syntax | `import 'file.just'` | `mod name` |
| Namespace | Merged into parent | Separate (`name::*`) |
| Calling | `just recipe` | `just name::recipe` |
| Use case | Shared settings, dev recipes | Categorized tooling |

## Module Recipes

Recipes inside modules are simple - the namespace comes from the `mod` statement:

```just
# go.just - recipes called as go::build, go::test, etc.

build tool:
    go build -o bin/{{tool}} .

test tool:
    go test ./...

lint:
    golangci-lint run
```

## Variables in Modules

Modules have their own variable scope. Use `env_var()` for paths:

```just
# docker.just
PROJECT_ROOT := env_var("PWD")
DOCKERFILE := PROJECT_ROOT / "docker" / "Dockerfile"

build:
    cd {{PROJECT_ROOT}} && docker build -f {{DOCKERFILE}} .
```

## Calling Between Modules

Use full namespace syntax:

```just
# justfile
mod go
mod docker

# Build and containerize
release: (go::build "myapp")
    just docker::build
```

## Nested Modules

Modules can contain submodules:

```just
# cloud.just
mod aws
mod gcp
```

```bash
just cloud::aws::deploy
just cloud::gcp::deploy
```

## Listing Module Recipes

```bash
just --list              # Shows all including module::recipe
just --list --unsorted   # Preserve definition order
```

## Common Patterns

### Top-level Aliases

```just
# justfile
mod go
mod docker

# Convenience aliases
build:
    just go::build myapp

test:
    just go::test myapp

lint:
    just go::lint
```

### Module with Parameters

```just
# release.just
DIST := env_var("PWD") / "dist"

all: linux darwin windows

linux:
    GOOS=linux GOARCH=amd64 go build -o {{DIST}}/app-linux .

darwin:
    GOOS=darwin GOARCH=arm64 go build -o {{DIST}}/app-darwin .

windows:
    GOOS=windows GOARCH=amd64 go build -o {{DIST}}/app.exe .
```

```bash
just release::all
just release::linux
```
