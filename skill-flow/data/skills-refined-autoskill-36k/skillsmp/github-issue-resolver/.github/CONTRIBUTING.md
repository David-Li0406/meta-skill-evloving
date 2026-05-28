# Contributing to OpenShift Cluster Health MCP

Thank you for your interest in contributing to the OpenShift Cluster Health MCP server! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Branch Strategy](#branch-strategy)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Commit Message Format](#commit-message-format)
- [Code Review Requirements](#code-review-requirements)
- [Testing Requirements](#testing-requirements)
- [Code Style Guidelines](#code-style-guidelines)

## Prerequisites

Before contributing, ensure you have the following installed:

- **Go 1.24+** - The project requires Go 1.24 or later
- **Docker** - For building and testing container images
- **kubectl** - For Kubernetes cluster interactions
- **OpenShift CLI (oc)** - Optional but recommended for OpenShift-specific testing
- **Access to OpenShift 4.18+** - For integration testing (optional)
- **golangci-lint** - For code linting
- **Helm 3+** - For chart validation

## Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/openshift-cluster-health-mcp.git
   cd openshift-cluster-health-mcp
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/tosin2013/openshift-cluster-health-mcp.git
   ```

4. **Install dependencies**:
   ```bash
   go mod download
   ```

5. **Run tests to verify setup**:
   ```bash
   make test
   ```

6. **Build the binary**:
   ```bash
   make build
   ```

For detailed development commands, see the [CLAUDE.md](../CLAUDE.md) file.

## Branch Strategy

This project maintains multiple branches for different OpenShift versions:

- **`main`** - Primary development branch (OpenShift 4.18 / Kubernetes 1.31)
- **`release-4.18`** - OpenShift 4.18 release branch
- **`release-4.19`** - OpenShift 4.19 release branch (Kubernetes 1.32)
- **`release-4.20`** - OpenShift 4.20 release branch (Kubernetes 1.33)

### Which Branch to Target?

- **Bug fixes**: Target the earliest affected release branch, it will be merged forward
- **New features**: Target `main` branch
- **Backports**: Target specific release branch with justification in PR description

## Making Changes

1. **Keep your fork updated**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch** from the appropriate base:
   ```bash
   # For features targeting OpenShift 4.18
   git checkout -b feature/your-feature-name main

   # For fixes to OpenShift 4.19
   git checkout -b fix/your-fix-name release-4.19
   ```

3. **Make your changes** following the code style guidelines

4. **Add tests** for new functionality

5. **Run local validation**:
   ```bash
   make test          # Run unit tests
   make lint          # Run linters
   make build         # Verify compilation
   make helm-lint     # Validate Helm charts (if modified)
   ```

## Pull Request Process

1. **Ensure all tests pass** locally before opening a PR

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub:
   - Use the PR template (it will auto-populate)
   - Provide a clear, descriptive title
   - Fill out all sections of the template
   - Link related issues using `Fixes #123` or `Relates to #456`

4. **Required CI checks** must pass:
   - **Test** - Unit tests with race detection
   - **Lint** - Code quality checks
   - **Build** - Binary compilation and size verification
   - **Security** - Trivy vulnerability scanning
   - **Helm** - Helm chart validation
   - **build-and-push** - Container image build

5. **Address review feedback**:
   - Respond to all comments
   - Make requested changes
   - Mark conversations as resolved when addressed
   - Request re-review after updates

6. **Merge requirements**:
   - All CI checks must pass
   - Code owner approval required
   - All conversations must be resolved
   - Branch must be up-to-date with base branch

## Commit Message Format

This project follows [Conventional Commits](https://www.conventionalcommits.org/) for clear, standardized commit messages.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **chore**: Maintenance tasks (dependencies, build config)
- **test**: Test additions or updates
- **refactor**: Code refactoring without feature changes
- **ci**: CI/CD pipeline changes
- **perf**: Performance improvements

### Scope (Optional)

The scope should be the area of the codebase affected:
- `tools` - MCP tool implementations
- `resources` - MCP resource implementations
- `clients` - K8s/CE/KServe clients
- `server` - HTTP server and MCP protocol
- `cache` - Caching layer
- `helm` - Helm chart changes
- `ci` - GitHub Actions workflows

### Examples

```
feat(tools): add analyze-anomalies tool for ML-based detection

Implements a new MCP tool that integrates with KServe to detect
anomalies in cluster metrics using machine learning models.

Fixes #42
```

```
fix(clients): handle connection timeout in Coordination Engine client

The CE client was not properly handling connection timeouts, causing
the server to hang. Added retry logic with exponential backoff.

Fixes #67
```

```
docs: update CONTRIBUTING.md with branch protection guidelines
```

## Code Review Requirements

### For `main` Branch
- **1 approval required** from code owners
- All required status checks must pass
- All conversations must be resolved
- Branch must be up-to-date with `main`

### For Release Branches (`release-4.18`, `release-4.19`, `release-4.20`)
- **2 approvals required** from code owners
- All required status checks must pass
- All conversations must be resolved
- Branch must be up-to-date with target release branch
- Higher scrutiny for changes affecting production deployments

See [docs/BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md) for detailed information about branch protection rules.

## Testing Requirements

### Unit Tests

- **Required for all new code** (functions, methods, tools, resources)
- Minimum coverage: No decrease from current baseline
- Tests must be fast (<1s per test)
- Use table-driven tests for multiple scenarios
- Mock external dependencies (K8s API, CE, KServe)

Example:
```go
func TestClusterHealthTool_Execute(t *testing.T) {
    tests := []struct {
        name     string
        args     map[string]interface{}
        want     interface{}
        wantErr  bool
    }{
        // test cases
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test implementation
        })
    }
}
```

### Integration Tests

- **Optional but recommended** for tools/resources
- Requires access to a Kubernetes/OpenShift cluster
- Use `KUBECONFIG` environment variable for cluster access
- Should be skippable if cluster is unavailable

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific package
go test -v ./internal/tools

# Run specific test
go test -v ./internal/tools -run TestClusterHealthTool
```

## Code Style Guidelines

### Go Code Standards

1. **Follow effective Go**: https://go.dev/doc/effective_go
2. **Use gofmt**: All code must be formatted with `gofmt`
3. **Pass golangci-lint**: Run `make lint` before committing
4. **Document exported functions**: All exported functions must have doc comments
5. **Error handling**: Always check and handle errors, avoid `_` for errors
6. **Context propagation**: Pass `context.Context` for cancellation support

### Security Best Practices

1. **No hardcoded secrets**: Use environment variables or Kubernetes secrets
2. **Validate inputs**: Sanitize all user inputs to tools/resources
3. **Least privilege**: Request minimum RBAC permissions needed
4. **Dependency scanning**: Run `make security-gosec` to check for vulnerabilities

### OpenShift Compatibility

1. **Use SecurityContext**: Set `runAsNonRoot: true`, don't hardcode `runAsUser`
2. **Respect resource limits**: Test with realistic CPU/memory constraints
3. **Support multiple versions**: Test against OpenShift 4.18, 4.19, 4.20

### MCP Protocol Adherence

1. **Follow MCP spec**: https://modelcontextprotocol.io/
2. **Use official SDK**: Leverage `github.com/modelcontextprotocol/go-sdk`
3. **Tool naming**: Use kebab-case (e.g., `get-cluster-health`)
4. **Resource URIs**: Follow pattern `scheme://path` (e.g., `cluster://health`)

## Documentation Requirements

When adding new features or making significant changes, update:

- **README.md** - High-level overview and quick start
- **CLAUDE.md** - Detailed development instructions
- **Code comments** - Document exported functions and complex logic
- **ADRs** - Create Architecture Decision Record for significant architectural choices (see `docs/adrs/`)

## Questions or Need Help?

- **GitHub Issues**: Open an issue for bugs or feature requests
- **GitHub Discussions**: Ask questions or discuss ideas
- **Code Owners**: Reach out to `@tosin2013` for guidance

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

Thank you for contributing to OpenShift Cluster Health MCP! 🎉
