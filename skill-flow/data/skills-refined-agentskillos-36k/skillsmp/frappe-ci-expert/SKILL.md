---
name: frappe-ci-expert
description: Expert guidance for setting up CI/CD tests for Frappe apps. Use when users ask about GitHub Actions workflows, CI test setup, continuous integration for Frappe apps, running tests in CI environments, database setup for CI, bench configuration in CI, or automating tests for Frappe/ERPNext applications.
---

# Frappe CI Expert

## Overview

This skill provides comprehensive guidance for setting up Continuous Integration (CI) testing for Frappe applications using GitHub Actions. It covers the complete CI setup process including database services, bench initialization, site creation, and test execution based on official Frappe and ERPNext patterns.

## What This Skill Covers

Setting up CI tests for Frappe apps requires several components working together:

1. **GitHub Actions Workflow** - Define when and how tests run
2. **Database Services** - Configure MariaDB or PostgreSQL containers
3. **Dependencies** - Install system packages, Python packages, and Node.js
4. **Bench Setup** - Initialize bench and create test sites
5. **Test Execution** - Run server tests, UI tests, or parallel tests
6. **Debugging** - Access logs and troubleshoot CI failures

## Quick Start

For a standard Frappe app with server tests:

1. Create `.github/workflows/server-tests.yml` based on [references/workflow-templates.md](references/workflow-templates.md)
2. Add helper scripts from [references/helper-scripts.md](references/helper-scripts.md)
3. Configure database services from [references/database-services.md](references/database-services.md)
4. Follow the setup steps in [references/ci-setup-process.md](references/ci-setup-process.md)

## Reference Documentation

### Workflow Templates
See [references/workflow-templates.md](references/workflow-templates.md) for:
- Complete server tests workflow
- UI tests (Cypress) workflow
- Patch migration tests workflow
- Customizing workflows for your app

### Database Services
See [references/database-services.md](references/database-services.md) for:
- MariaDB service configuration
- PostgreSQL service configuration
- Database credentials and configuration
- Site config JSON templates

### CI Setup Process
See [references/ci-setup-process.md](references/ci-setup-process.md) for:
- Step-by-step bench initialization
- Installing dependencies
- Creating and configuring test sites
- Process management (Procfile modifications)
- Starting bench services in CI

### Helper Scripts
See [references/helper-scripts.md](references/helper-scripts.md) for:
- install_dependencies.sh - System packages setup
- install.sh - Bench initialization and site creation
- Database setup scripts
- Best practices for helper scripts

### Test Execution
See [references/test-execution.md](references/test-execution.md) for:
- Running parallel tests for server
- Running UI tests with Cypress
- Test output and logging
- Code coverage setup

### CI Patterns and Best Practices
See [references/ci-patterns.md](references/ci-patterns.md) for:
- Caching strategies (pip, yarn, Cypress)
- Performance optimization
- Debugging CI failures
- Common pitfalls and solutions
- Multi-matrix testing strategies

## Key Concepts

### Services in GitHub Actions

Frappe apps typically require:
- **Database**: MariaDB 10.6+ or PostgreSQL 12+
- **Redis**: For caching and background jobs (optional for basic tests)
- **SMTP**: For email testing (smtp4dev)

These run as Docker containers in the GitHub Actions runner.

### Test Site Configuration

CI tests use a dedicated test site (typically `test_site`) with:
- Specific database credentials
- Test-safe email configuration
- Monitoring and server scripts enabled
- Host entry in `/etc/hosts` for proper URL resolution

### Bench in CI

The bench setup in CI differs from development:
- Installed via pip (not git clone)
- Uses `--skip-assets` flag for speed
- Disables watch/schedule processes
- Runs in background for tests

## Common Use Cases

### Setting Up Server Tests
Follow the complete example in [references/workflow-templates.md](references/workflow-templates.md#server-tests-workflow) which includes:
- Workflow triggers (PR, workflow_dispatch, schedule)
- MariaDB and PostgreSQL services
- Full setup steps
- Parallel test execution

### Adding UI Tests (Cypress)
See [references/workflow-templates.md](references/workflow-templates.md#ui-tests-workflow) for:
- Cypress binary caching
- Matrix strategy for parallel execution
- Setup wizard completion
- Headless browser configuration

### Testing Database Migrations
Check [references/workflow-templates.md](references/workflow-templates.md#patch-tests-workflow) for:
- Testing upgrades from older versions
- Restoring production backups
- Sequential migration testing

### Custom App Testing
When setting up CI for your own app:
1. Start with the server tests template
2. Modify the app name and repository references
3. Add any app-specific dependencies
4. Adjust test commands if needed
5. See [references/ci-patterns.md](references/ci-patterns.md#custom-app-setup) for details

## Environment Details

### Standard Paths
- Bench directory: `~/frappe-bench` or `/home/runner/frappe-bench`
- Apps directory: `~/frappe-bench/apps/`
- Sites directory: `~/frappe-bench/sites/`
- Logs: `~/frappe-bench/logs/`

### Standard Configuration
- Test site name: `test_site`
- Database name: `test_frappe`
- Database user: `test_frappe`
- Database password: `test_frappe`
- Root password: `travis`
- Admin password: `admin`

### Python and Node Versions
Based on Frappe requirements:
- Python: 3.10+ (typically 3.10 or 3.11)
- Node.js: 24 (use setup-node@v3 or higher with check-latest)

## Debugging CI Failures

When tests fail in CI:

1. **Check the logs** - Workflow outputs bench logs and error logs
2. **Reproduce locally** - Use the same commands from the workflow
3. **Enable tmate** - Add `debug-gha` label for interactive debugging
4. **Check services** - Ensure database services are healthy
5. **Review build output** - Asset build failures are common issues

See [references/ci-patterns.md](references/ci-patterns.md#debugging-failures) for detailed troubleshooting.

## Integration with Frappe Apps

### For Apps in the Frappe Ecosystem
If building an app to work with ERPNext or other Frappe apps:
- Install the dependent app in your CI workflow
- Use `bench get-app` to fetch dependencies
- Install apps in the correct order
- Test against multiple versions if needed

### For Standalone Apps
If your app doesn't depend on other Frappe apps:
- Test against the base Frappe framework only
- Keep the setup minimal
- Focus on your app's specific tests

## Additional Resources

All reference files are located in the `references/` directory:
- `workflow-templates.md` - Complete workflow YAML examples
- `database-services.md` - Database service configurations
- `ci-setup-process.md` - Detailed setup steps explanation
- `helper-scripts.md` - Script templates and explanations
- `test-execution.md` - Test running strategies
- `ci-patterns.md` - Best practices and patterns

## License

This skill documentation is licensed under Apache License 2.0.
