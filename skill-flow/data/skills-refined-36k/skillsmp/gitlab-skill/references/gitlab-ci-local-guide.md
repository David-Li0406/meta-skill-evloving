# GitLab CI Local Testing Guide

Complete guide for setting up and using gitlab-ci-local to test GitLab CI/CD pipelines locally.

## Overview

[gitlab-ci-local](https://github.com/firecow/gitlab-ci-local) is a CLI tool that runs GitLab CI/CD pipelines locally, eliminating commit-push-debug cycles.

**Why use it:**

- Test CI/CD pipeline changes before pushing to GitLab
- Debug pipeline failures locally with full access to logs and artifacts
- Validate release workflows without creating actual releases
- Save CI runner minutes and reduce feedback time

## Prerequisites

Before setup, ensure you have:

1. **Node.js** (version 14 or higher)

   ```bash
   node --version  # Should be >= 14.x
   ```

2. **Container Engine** (Docker or Podman)

   ```bash
   # Check if Docker is available
   docker --version

   # OR check if Podman is available
   podman --version
   ```

3. **gitlab-ci-local** installed globally

   ```bash
   npm install -g gitlab-ci-local

   # Verify installation
   gitlab-ci-local --version
   ```

## Quick Start

### 1. Get a GitLab API Token

Create a personal access token from your GitLab instance:

1. Log in to your GitLab instance (e.g., <https://sourcery.assaabloy.net>)
2. Go to **User Settings** → **Access Tokens**
3. Create a new token with these scopes:

   - `api` - Full API access
   - `read_repository` - Read repository data
   - `write_repository` - Write repository data (for releases)
   - `read_registry` - Read package registry
   - `write_registry` - Publish packages

4. **IMPORTANT**: Copy the token immediately - you cannot view it again!

### 2. Configure Home Directory Variables

Create a global configuration that works for all projects:

```bash
# Create the directory if it doesn't exist
mkdir -p $HOME/.gitlab-ci-local

# Create the variables file
cat > $HOME/.gitlab-ci-local/variables.yml <<'EOF'
---
# GitLab CI Local - Home Variables Configuration
# This file contains global CI/CD variables available across all projects

global:
  # Authentication tokens - replace with your actual token
  GITLAB_TOKEN: glpat-YOUR_TOKEN_HERE
  CI_JOB_TOKEN: glpat-YOUR_TOKEN_HERE
EOF
```

**Security Note**: This file is stored in your home directory and is NOT tracked in git.

### 3. Test Your Setup

From the project root directory:

```bash
# List all jobs in the pipeline
gitlab-ci-local --list

# Run a specific job
gitlab-ci-local test:python

# Run the entire pipeline
gitlab-ci-local
```

## Configuration Files

gitlab-ci-local uses multiple configuration files with different purposes:

### Project-Level Configuration (Tracked in Git)

#### `.gitlab-ci-local-variables.yml`

Contains project-specific CI/CD variables that are safe to commit:

```yaml
# GitLab CI variables for local testing
CI_SERVER_URL: https://gitlab.example.com
CI_SERVER_HOST: gitlab.example.com
CI_PROJECT_PATH: group/project
CI_PROJECT_ID: 1234
CI_API_V4_URL: https://gitlab.example.com/api/v4
CI_PROJECT_URL: https://gitlab.example.com/group/project
CI_PROJECT_NAME: project
CI_PROJECT_NAMESPACE: group
CI_COMMIT_BRANCH: main
CI_DEFAULT_BRANCH: main
# Use the real GitLab token for authentication in local testing
CI_JOB_TOKEN: $GITLAB_TOKEN
```

**Location**: Project root (committed to git) **Purpose**: Project-specific variables that don't contain secrets

### Local Secrets (NOT Tracked in Git)

#### `.gitlab-ci-local-env`

Contains secrets and CLI configuration options:

```bash
# Secrets for local testing (CLI options format)
GITLAB_TOKEN=glpat-YOUR_TOKEN_HERE
CI_JOB_TOKEN=glpat-YOUR_TOKEN_HERE

# Optional: Other secrets
WOKWI_CLI_TOKEN=wok_YOUR_WOKWI_TOKEN
```

**Location**: Project root (added to .gitignore) **Purpose**: Project-specific secrets and CLI options **Format**: Shell environment variable format (`KEY=value`)

### User-Global Configuration (Home Directory)

#### `$HOME/.gitlab-ci-local/variables.yml`

**This is the recommended approach** for storing tokens that work across all projects:

```yaml
---
# GitLab CI Local - Home Variables Configuration
# This file contains global CI/CD variables available across all projects

global:
  # Authentication tokens
  GITLAB_TOKEN: glpat-YOUR_TOKEN_HERE
  CI_JOB_TOKEN: glpat-YOUR_TOKEN_HERE
```

**Location**: `~/.gitlab-ci-local/variables.yml` **Purpose**: User-wide variables that apply to all projects **Format**: YAML with `global:` section **Security**: Stored in your home directory, never committed to any repository

## CLI Usage

### Common Commands

```bash
# List all jobs (excludes jobs with when:never)
gitlab-ci-local --list

# List all jobs including when:never
gitlab-ci-local --list-all

# List jobs in CSV format
gitlab-ci-local --list-csv

# Preview expanded GitLab CI YAML (with all includes/extends resolved)
gitlab-ci-local --preview

# Run a specific job
gitlab-ci-local <job-name>

# Run multiple specific jobs
gitlab-ci-local job1 job2 job3

# Run all jobs in a specific stage
gitlab-ci-local --stage test

# Run a job and all its dependencies (needs)
gitlab-ci-local --needs release

# Pass additional variables
gitlab-ci-local --variable MY_VAR=value --variable ANOTHER=123 job-name

# Use a different variables file
gitlab-ci-local --variables-file custom-variables.yml

# Enable timestamp logging
gitlab-ci-local --timestamps job-name

# Fetch latest external includes before running
gitlab-ci-local --fetch-includes
```

### Running Specific Scenarios

#### Test Before Pushing

```bash
# Run all test jobs
gitlab-ci-local --stage test

# Run linting only
gitlab-ci-local lint:ruff

# Run tests for specific Python version
gitlab-ci-local test:python
```

#### Test Release Workflow

```bash
# Run release job with all dependencies
gitlab-ci-local --needs release

# Check what the release job would do (dry-run via preview)
gitlab-ci-local --preview | grep -A 50 "^release:"
```

#### Debug Failed Jobs

```bash
# Run with timestamps to see timing issues
gitlab-ci-local --timestamps failing-job

# Check the expanded configuration
gitlab-ci-local --preview

# Verify variables are set correctly
gitlab-ci-local --list-json | jq '.[] | select(.name=="failing-job")'
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Failures (403/401 Errors)

**Symptom**: Git push or API calls fail with authentication errors

**Possible Causes**:

- Token doesn't have required scopes
- Token expired or revoked
- Wrong token format (missing `glpat-` prefix)

**Solution**:

```bash
# Test token validity
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/user"

# Test token scopes for package publishing
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/1234/packages/pypi"

# Test git authentication with token
git ls-remote $(git remote get-url origin | sed "s|://|://oauth2:$GITLAB_TOKEN@|") | head -5
```

#### 2. Token Variables Not Available

**Symptom**: Jobs fail because `$GITLAB_TOKEN` is empty or undefined

**Problem**: Token not set in the correct configuration file

**Solution**: Check configuration file hierarchy:

1. First, check home directory configuration:

   ```bash
   cat $HOME/.gitlab-ci-local/variables.yml
   # Should show: GITLAB_TOKEN under global: section
   ```

2. Verify with a test job:

   ```bash
   # Create test job
   cat > .gitlab-ci-test.yml <<'EOF'
   test-token:
     stage: test
     image: alpine
     script:
       - 'echo "GITLAB_TOKEN starts with: ${GITLAB_TOKEN:0:15}..."'
       - 'echo "CI_JOB_TOKEN starts with: ${CI_JOB_TOKEN:0:15}..."'
   EOF

   # Run test
   gitlab-ci-local --file .gitlab-ci-test.yml test-token

   # Clean up
   rm .gitlab-ci-test.yml
   ```

3. If still failing, pass token via command line:

   ```bash
   gitlab-ci-local --variable GITLAB_TOKEN=$GITLAB_TOKEN job-name
   ```

#### 3. Jobs Running with Wrong Configuration

**Symptom**: Jobs use unexpected variables or configuration

**Problem**: Multiple configuration files conflicting

**Solution**: Check configuration precedence:

```bash
# gitlab-ci-local loads variables in this order (later overrides earlier):
# 1. $HOME/.gitlab-ci-local/variables.yml
# 2. .gitlab-ci-local-variables.yml (project default)
# 3. --variables-file argument
# 4. --variable CLI arguments (highest priority)

# Debug by previewing expanded config
gitlab-ci-local --preview | less
```

#### 4. glab Release Creation Fails

**Symptom**: `none of the git remotes configured for this repository point to a known GitLab host`

**Problem**: Missing `GITLAB_HOST` environment variable for self-hosted GitLab

**Solution**: Add to `.gitlab-ci.yml` release job:

```yaml
.release_base:
  variables:
    GITLAB_HOST: $CI_SERVER_HOST # Tells glab about self-hosted instance
```

## Real-World Examples

### Example 1: Testing Pipeline Changes Locally

```bash
# Make changes to .gitlab-ci.yml
vim .gitlab-ci.yml

# Preview expanded configuration
gitlab-ci-local --preview | less

# List all jobs to see what will run
gitlab-ci-local --list

# Run specific stage to test changes
gitlab-ci-local --stage test

# If successful, commit and push
git add .gitlab-ci.yml
git commit -m "ci: update pipeline configuration"
git push
```

### Example 2: Debugging a Failed Release

```bash
# Check release job configuration
gitlab-ci-local --preview | grep -A 100 "^release:"

# Verify all required variables are set
gitlab-ci-local --list-json | jq '.[] | select(.name=="release")'

# Run release job with verbose output and timestamps
gitlab-ci-local --timestamps --needs release

# If it fails, check artifacts directory
ls -la .gitlab-ci-local/artifacts/release/

# Check job logs
cat .gitlab-ci-local/output/release.log
```

### Example 3: Running Tests in Parallel

```bash
# Run all test jobs for both Python versions in parallel
# (gitlab-ci-local automatically runs matrix jobs in parallel)
gitlab-ci-local test:python

# Check artifacts for both Python versions
ls -la .gitlab-ci-local/artifacts/test-reports/
ls -la .gitlab-ci-local/artifacts/coverage/

# View coverage reports
firefox .gitlab-ci-local/artifacts/coverage/htmlcov-py3.11/index.html
```

## Variable Configuration Best Practices

### ✅ Recommended Setup

1. **For tokens and secrets**: Use `$HOME/.gitlab-ci-local/variables.yml`

   - Pros: Works across all projects, never accidentally committed
   - Cons: Must be set up once per developer workstation

2. **For project metadata**: Use `.gitlab-ci-local-variables.yml` (committed)

   - Pros: Shared with team, consistent across developers
   - Cons: Cannot contain secrets

3. **For temporary overrides**: Use `--variable` CLI flag
   - Pros: Quick testing without file changes
   - Cons: Must remember to add each time

### ❌ Common Mistakes

- ❌ Committing `.gitlab-ci-local-env` with tokens
- ❌ Forgetting to set `GITLAB_HOST` for glab in self-hosted instances
- ❌ Using `.env` format in `$HOME/.gitlab-ci-local/.env` (should be `variables.yml` in YAML)
- ❌ Testing with wrong token that lacks required scopes

## Security Considerations

### Token Storage

**✅ Safe locations**:

- `$HOME/.gitlab-ci-local/variables.yml` (user home directory)
- System keychain/credential manager
- Environment variables in your shell config (with caution)

**❌ Never store tokens in**:

- `.gitlab-ci-local-env` (unless in .gitignore)
- `.gitlab-ci-local-variables.yml` (this is tracked in git!)
- `.gitlab-ci.yml` (public in repository)
- Any file tracked by git

### Token Scope Minimization

Only grant the scopes you actually need:

| Scope              | Required For              | Risk Level                |
| ------------------ | ------------------------- | ------------------------- |
| `api`              | Full API access, releases | High - grants wide access |
| `read_repository`  | Cloning, reading code     | Low                       |
| `write_repository` | Pushing tags, releases    | Medium                    |
| `read_registry`    | Pulling packages          | Low                       |
| `write_registry`   | Publishing packages       | Medium                    |

### Token Rotation

- Rotate tokens every 90 days
- Immediately revoke tokens if compromised
- Use separate tokens for CI/CD vs local development
- Never share tokens between team members

## Advanced Usage

### Custom Container Engine

If using Podman instead of Docker:

```bash
# Set container executable
export GCL_CONTAINER_EXECUTABLE=podman

# Or use CLI flag
gitlab-ci-local --container-executable podman job-name
```

### Limit Concurrent Jobs

```bash
# Run maximum 2 jobs in parallel (useful for resource-constrained machines)
gitlab-ci-local --concurrency 2
```

### Artifact Management

```bash
# Prevent artifacts from being copied to source directory
gitlab-ci-local --no-artifacts-to-source

# Clean up Docker resources after pipeline
gitlab-ci-local --cleanup

# View artifacts location
ls -la .gitlab-ci-local/artifacts/
```

### Shell Isolation

```bash
# Enable artifact isolation for shell executor jobs
gitlab-ci-local --shell-isolation

# Force all jobs to use shell executor (for debugging)
gitlab-ci-local --force-shell-executor
```

## Additional Resources

- **gitlab-ci-local GitHub**: <https://github.com/firecow/gitlab-ci-local>
- **GitLab CI/CD Documentation**: <https://docs.gitlab.com/ee/ci/>

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Run `gitlab-ci-local --preview` to see expanded configuration
3. Check `.gitlab-ci-local/output/` for job logs
4. Verify token validity with curl commands shown above
5. Ask in team chat or create an issue in the repository
