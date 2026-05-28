# Automation & Testing

## Table of Contents

1. [Makefile Orchestration](#makefile-orchestration)
2. [CI/CD Integration](#cicd-integration)
3. [Testing Strategies](#testing-strategies)
4. [Docker Testing](#docker-testing)

## Makefile Orchestration

Use Makefile as the single entry point:

```makefile
all: init link defaults packages

init:
	local/bin/init.sh

link:
	local/bin/link.sh

defaults:
	local/bin/defaults.sh

packages:
	local/bin/packages.sh install

test:
	local/bin/test.sh

verify:
	local/bin/verify.sh

ci: test
	@echo "CI tests complete"
```

### Target Guidelines

| Target | Purpose | Idempotent |
|--------|---------|------------|
| `init` | First-time setup (Homebrew, Xcode) | Yes |
| `link` | Create symlinks | Yes |
| `defaults` | Set OS defaults | Yes |
| `packages` | Install packages | Yes |
| `test` | Run all tests | Yes |
| `verify` | Verify setup | Yes |

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Dotfiles

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make ci

  test-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make ci
```

### CI-Specific Behavior

Detect CI and adjust behavior:

```bash
if isRunningOnCI; then
    info "CI environment detected"
    # Skip interactive prompts
    # Skip shell changes (chsh)
    # Use non-interactive package install
fi
```

## Testing Strategies

### verify.sh Structure

```bash
#!/bin/bash
set -eu
source "$(dirname "$0")/common.sh"

errors=0

verify_symlink() {
    local link="$1" target="$2"
    if [[ -L "$link" ]] && [[ "$(readlink "$link")" == "$target" ]]; then
        success "Symlink OK: $link"
    else
        error "Symlink FAILED: $link"
        ((errors++))
    fi
}

verify_command() {
    local cmd="$1"
    if command -v "$cmd" >/dev/null 2>&1; then
        success "Command available: $cmd"
    else
        error "Command missing: $cmd"
        ((errors++))
    fi
}

# Run verifications
verify_symlink "$HOME/.zshenv" "$DOTFILES_DIR/.zshenv"
verify_symlink "$XDG_CONFIG_HOME/zsh/.zshrc" "$DOTFILES_DIR/config/zsh/.zshrc"
verify_command "git"
verify_command "brew"

# Report results
if [[ $errors -eq 0 ]]; then
    success "All verifications passed"
else
    error "$errors verification(s) failed"
    exit 1
fi
```

### Test Categories

1. **Syntax tests**: `bash -n script.sh`
2. **Symlink tests**: Verify links exist and point correctly
3. **Command tests**: Verify required tools are installed
4. **Config tests**: Verify config files are valid (e.g., JSON syntax)

## Docker Testing

Test on multiple platforms without actual machines:

### docker-compose.test.yml

```yaml
version: '3.8'
services:
  ubuntu:
    build:
      context: .
      dockerfile: docker/Dockerfile.ubuntu22
    volumes:
      - .:/dotfiles:ro
    command: /dotfiles/local/bin/test.sh

  debian:
    build:
      context: .
      dockerfile: docker/Dockerfile.debian
    volumes:
      - .:/dotfiles:ro
    command: /dotfiles/local/bin/test.sh
```

### Dockerfile Example

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CI=true

RUN apt-get update && apt-get install -y \
    curl wget git build-essential zsh sudo

RUN useradd -m -s /bin/bash testuser && \
    echo "testuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER testuser
WORKDIR /home/testuser

ENTRYPOINT ["/bin/bash"]
```

### Running Docker Tests

```bash
# Test all platforms
docker-compose -f docker-compose.test.yml up --build

# Test specific platform
docker-compose -f docker-compose.test.yml up ubuntu
```
