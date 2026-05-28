# Testing Patterns in GitHub Actions

Comprehensive testing strategies for CI workflows, including unit tests, E2E tests, interactive testing, and error handling.

---

## Unit Tests

Simple test execution:

```yaml
- name: Run Tests
  run: go test -race -v ./...
  working-directory: installer
```

### With Coverage

```yaml
- name: Run Tests with Coverage
  run: |
    go test -race -coverprofile=coverage.out -covermode=atomic ./...
    go tool cover -html=coverage.out -o coverage.html
  working-directory: installer

- name: Upload Coverage
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: installer/coverage.html
```

---

## E2E Tests

### Testing Against Current Branch

Always test PR/branch changes:

```bash
# Get current branch name with fallbacks
if [ -n "$GITHUB_HEAD_REF" ]; then
  CURRENT_BRANCH="$GITHUB_HEAD_REF"  # PR branch
elif [ -n "$GITHUB_REF" ]; then
  CURRENT_BRANCH="${GITHUB_REF#refs/heads/}"  # Push branch
else
  CURRENT_BRANCH="main"
  echo "Warning: Could not detect branch, defaulting to main"
fi
echo "Using branch: $CURRENT_BRANCH"

# Use in commands
./installer install --git-branch="$CURRENT_BRANCH"
```

### With Timeout

Prevent hanging tests:

```yaml
- name: Test Non-Interactive Installation
  run: |
    echo "Testing installer in non-interactive mode..."
    
    # Set up test environment
    export HOME="/tmp/test-home"
    mkdir -p "$HOME"
    
    # Create test prerequisites
    mkdir -p "$HOME/.gnupg"
    chmod 700 "$HOME/.gnupg"
    
    # Run with timeout to prevent hangs
    timeout 300 ./dotfiles-installer install \
      --non-interactive \
      --plain \
      --extra-verbose \
      --install-prerequisites=true \
      --git-clone-protocol=https \
      --git-branch="$CURRENT_BRANCH" \
      --work-env=false
```

### Platform-Specific Binary Selection

```bash
- name: Make Binary Executable
  run: |
    # Find the correct binary for the current platform
    if [ "${{ matrix.platform }}" = "macos" ]; then
      # Only ARM64 supported for macOS
      BINARY_PATH="installer/dist/dotfiles_installer_darwin_arm64_v8.0/dotfiles-installer"
    else
      # Linux platforms
      if [ "$(uname -m)" = "aarch64" ]; then
        BINARY_PATH="installer/dist/dotfiles_installer_linux_arm64_v8.0/dotfiles-installer"
      else
        BINARY_PATH="installer/dist/dotfiles_installer_linux_amd64_v1/dotfiles-installer"
      fi
    fi
    
    echo "Using binary: $BINARY_PATH"
    chmod +x "$BINARY_PATH"
    cp "$BINARY_PATH" ./dotfiles-installer
```

---

## Interactive Tests with Expect

### Installing Expect

Platform-specific installation:

```yaml
- name: Install expect tool
  run: |
    if [ "${{ matrix.platform }}" = "macos" ]; then
      brew install expect
    elif [ "${{ matrix.platform }}" = "fedora" ] || [ "${{ matrix.platform }}" = "centos" ]; then
      # For Fedora/CentOS - install expect via dnf
      dnf install -y expect
    else
      # For Ubuntu/Debian - check if sudo exists, otherwise run directly (containers)
      if command -v sudo >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y expect
      else
        apt-get update && apt-get install -y expect
      fi
    fi
```

### Running Expect Scripts

```yaml
- name: Test Interactive GPG Installation
  run: |
    echo "Testing installer in interactive mode with expect automation..."
    
    # Set up separate test environment for interactive test
    export HOME="/tmp/test-interactive-home"
    mkdir -p "$HOME"
    
    # Create a fake GPG directory to simulate existing setup
    mkdir -p "$HOME/.gnupg"
    chmod 700 "$HOME/.gnupg"
    
    # Get current branch name for testing with fallbacks
    if [ -n "$GITHUB_HEAD_REF" ]; then
      CURRENT_BRANCH="$GITHUB_HEAD_REF"
    elif [ -n "$GITHUB_REF" ]; then
      CURRENT_BRANCH="${GITHUB_REF#refs/heads/}"
    else
      CURRENT_BRANCH="main"
      echo "Warning: Could not detect branch, defaulting to main"
    fi
    echo "Using branch: $CURRENT_BRANCH"
    
    # Run the expect script with test parameters and current branch
    installer/test-interactive-gpg.exp \
      "./dotfiles-installer" \
      "test-user@example.com" \
      "Test CI User" \
      "test-ci-passphrase" \
      "$CURRENT_BRANCH"
```

---

## Error Handling in Tests

### Proper Exit Code Handling

```bash
# Create temporary file to capture output
temp_output=$(mktemp)

echo "Running compatibility check..."

# Use tee to both display output and capture it, handle exit code properly
set +e  # Don't exit on command failure
./dotfiles-installer check-compatibility --non-interactive --plain 2>&1 | tee "$temp_output"
exit_code=$?
set -e  # Re-enable exit on error

echo "Exit code: $exit_code"

# Read the captured output
output=$(cat "$temp_output")
rm -f "$temp_output"

# Check if output contains "missing prerequisites" - this is expected and should pass
if echo "$output" | grep -i "missing prerequisites" >/dev/null 2>&1; then
  echo "✅ Found 'missing prerequisites' in output - this is expected behavior"
  exit 0
fi

# If exit code is 0, that's also a pass
if [ $exit_code -eq 0 ]; then
  echo "✅ Compatibility check passed with exit code 0"
  exit 0
fi

# Any other scenario is unexpected
echo "❌ Unexpected compatibility check result - exit code: $exit_code"
exit $exit_code
```

### Testing Help Commands

```yaml
- name: Test Binary Help
  run: ./dotfiles-installer --help

- name: Test Install Command Help
  run: ./dotfiles-installer install --help
```

---

## Verification Steps

### Post-Installation Verification

```yaml
- name: Verify Installation Artifacts (if created)
  run: |
    echo "Checking for any artifacts created during installation..."
    ls -la /tmp/test-home/ || echo "No test home directory created"
    ls -la /tmp/test-interactive-home/ || echo "No interactive test home directory created"
    
    # Check if any dotfiles manager was initialized
    ls -la /tmp/test-home/.local/share/chezmoi/ 2>/dev/null || echo "No chezmoi directory found (expected in CI)"
    ls -la /tmp/test-interactive-home/.local/share/chezmoi/ 2>/dev/null || echo "No interactive chezmoi directory found (expected in CI)"
```

---

## Container Testing

### Running Tests in Containers

```yaml
jobs:
  test-debian:
    runs-on: ubuntu-latest
    container: debian:bookworm
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Tools
        run: |
          apt-get update
          apt-get install -y git curl
      
      - name: Run Tests
        run: ./run-tests.sh
```

**Notes:**
- Containers run on Linux runners only
- Use for testing specific distros (Debian, Fedora, Alpine, etc.)
- Actions like `checkout` work inside containers
- Install prerequisites in container (git, curl, etc.)

### Multi-Platform Matrix with Containers

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-latest
        platform: ubuntu
      - os: ubuntu-latest
        platform: debian
        container: debian:bookworm
      - os: ubuntu-latest
        platform: fedora
        container: fedora:latest
      - os: ubuntu-latest
        platform: centos
        container: quay.io/centos/centos:latest
      - os: macos-latest
        platform: macos

runs-on: ${{ matrix.os }}
container: ${{ matrix.container }}
```

---

## Working with Test Environments

### Setting Up Isolated Test Environments

```bash
# Set up test environment
export HOME="/tmp/test-home"
mkdir -p "$HOME"

# Create test prerequisites
mkdir -p "$HOME/.gnupg"
chmod 700 "$HOME/.gnupg"

# Run tests
./installer install --non-interactive
```

### Conditional Setup Based on Platform

```yaml
- name: Set up Prerequisites (macOS)
  if: matrix.platform == 'macos'
  run: |
    # Install coreutils for `timeout` command
    brew install coreutils

- name: Set up Prerequisites (Linux)
  if: matrix.platform != 'macos'
  run: |
    apt-get update && apt-get install -y timeout
```

---

## Test Organization

### Multi-Stage Testing

```yaml
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: make build
      
      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: dist/

  unit-test:
    name: Unit Tests
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Run Unit Tests
        run: go test -v ./...

  integration-test:
    name: Integration Tests
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts
      
      - name: Run Integration Tests
        run: ./run-integration-tests.sh

  e2e-test:
    name: E2E Tests
    needs: build
    strategy:
      matrix:
        platform: [ubuntu, debian, fedora, macos]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts
      
      - name: Run E2E Tests
        run: ./run-e2e-tests.sh
```

---

## Best Practices

1. **Always test against current branch**: Use `GITHUB_HEAD_REF` or `GITHUB_REF` to test PR changes
2. **Use timeouts**: Prevent hanging tests with `timeout` command
3. **Capture output**: Use `tee` to both display and capture output for assertions
4. **Isolate environments**: Use temporary directories for test homes
5. **Clean up**: Remove test artifacts after verification
6. **Platform-specific handling**: Use matrix conditionals for OS differences
7. **Expect for interactive**: Use expect scripts to automate interactive prompts
8. **Verify exit codes**: Don't just rely on command success/failure
9. **Test help commands**: Ensure CLI help is accessible and doesn't crash
10. **Container testing**: Test on actual target distros, not just Ubuntu
