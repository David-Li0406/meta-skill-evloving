# CircleCI

**Category**: developer-tools/cicd
**Description**: Continuous integration and delivery platform
**Homepage**: https://circleci.com

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `@circleci/circleci-config-sdk` - CircleCI Config SDK for Node.js
- `circleci` - CircleCI CLI wrapper

#### PYPI
- `circleci` - CircleCI Python client
- `pycircleci` - Python wrapper for CircleCI API

#### RUBY
- `circleci` - CircleCI Ruby client

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate CircleCI usage*

- `.circleci/config.yml` - Main CircleCI configuration file (strong indicator)
- `.circleci/config.yaml` - Alternative extension

### Configuration Directories
*Known directories that indicate CircleCI usage*

- `.circleci/` - CircleCI configuration directory (strong indicator)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `import\s+.*\s+from\s+['"]@circleci/circleci-config-sdk['"]`
- CircleCI Config SDK import
- Example: `import { Config } from '@circleci/circleci-config-sdk';`

**Pattern**: `require\(['"]@circleci/circleci-config-sdk['"]\)`
- CircleCI Config SDK require
- Example: `const { Config } = require('@circleci/circleci-config-sdk');`

#### Python
Extensions: `.py`

**Pattern**: `^import\s+circleci`
- CircleCI Python import
- Example: `import circleci`

**Pattern**: `^from\s+circleci\s+import`
- CircleCI Python from import
- Example: `from circleci.api import Api`

**Pattern**: `^from\s+pycircleci\s+import`
- PyCircleCI import
- Example: `from pycircleci.api import Api`

### Code Patterns
*CircleCI YAML patterns in config files*

**Pattern**: `^version:\s*2(\.[01])?`
- CircleCI config version
- Example: `version: 2.1`

**Pattern**: `^orbs:\s*$`
- Orbs section (CircleCI-specific)
- Example: `orbs:`

**Pattern**: `^\s+[a-z-]+:\s+circleci/`
- CircleCI orb reference
- Example: `node: circleci/node@5.0`

**Pattern**: `^jobs:\s*$`
- Jobs section
- Example: `jobs:`

**Pattern**: `^workflows:\s*$`
- Workflows section
- Example: `workflows:`

**Pattern**: `^\s+docker:\s*$`
- Docker executor
- Example: `docker:`

**Pattern**: `^\s+machine:\s*`
- Machine executor
- Example: `machine: true`

**Pattern**: `^\s+macos:\s*$`
- macOS executor
- Example: `macos:`

**Pattern**: `^\s+resource_class:\s*`
- Resource class specification
- Example: `resource_class: large`

**Pattern**: `^\s+- checkout\s*$`
- Checkout step
- Example: `- checkout`

**Pattern**: `^\s+- run:\s*`
- Run step
- Example: `- run: npm install`

**Pattern**: `^\s+- persist_to_workspace:\s*$`
- Persist to workspace step
- Example: `- persist_to_workspace:`

**Pattern**: `^\s+- attach_workspace:\s*$`
- Attach workspace step
- Example: `- attach_workspace:`

**Pattern**: `^\s+- store_artifacts:\s*$`
- Store artifacts step
- Example: `- store_artifacts:`

**Pattern**: `^\s+- store_test_results:\s*$`
- Store test results step
- Example: `- store_test_results:`

**Pattern**: `^\s+- save_cache:\s*$`
- Save cache step
- Example: `- save_cache:`

**Pattern**: `^\s+- restore_cache:\s*$`
- Restore cache step
- Example: `- restore_cache:`

---

## Environment Variables

- `CIRCLECI` - Set to true in CircleCI environment
- `CI` - Set to true in CircleCI
- `CIRCLE_BRANCH` - Branch being built
- `CIRCLE_BUILD_NUM` - Build number
- `CIRCLE_BUILD_URL` - URL to build
- `CIRCLE_JOB` - Current job name
- `CIRCLE_NODE_INDEX` - Parallelism index
- `CIRCLE_NODE_TOTAL` - Total parallelism nodes
- `CIRCLE_PR_NUMBER` - Pull request number
- `CIRCLE_PR_USERNAME` - PR author username
- `CIRCLE_PROJECT_REPONAME` - Repository name
- `CIRCLE_PROJECT_USERNAME` - Organization/user name
- `CIRCLE_REPOSITORY_URL` - Repository URL
- `CIRCLE_SHA1` - Commit SHA
- `CIRCLE_TAG` - Git tag if present
- `CIRCLE_USERNAME` - GitHub username
- `CIRCLE_WORKFLOW_ID` - Workflow ID
- `CIRCLE_WORKING_DIRECTORY` - Working directory
- `CIRCLE_TOKEN` - API token (for API access)

## Detection Notes

- `.circleci/config.yml` is the strongest indicator of CircleCI usage
- CircleCI uses `orbs:` for reusable configuration packages (unique feature)
- `version: 2.1` enables modern CircleCI features
- Executors define the build environment (docker, machine, macos)
- Workflows orchestrate multiple jobs
- CircleCI-specific steps like `persist_to_workspace` are strong indicators
