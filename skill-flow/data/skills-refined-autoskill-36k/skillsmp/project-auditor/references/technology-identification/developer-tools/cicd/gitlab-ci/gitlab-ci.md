# GitLab CI

**Category**: developer-tools/cicd
**Description**: GitLab's built-in CI/CD automation platform
**Homepage**: https://docs.gitlab.com/ee/ci/

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `@gitlab/ui` - GitLab UI components
- `gitlab` - GitLab API client for Node.js
- `@gitbeaker/node` - Full GitLab API Node.js library
- `@gitbeaker/rest` - GitLab REST API client

#### PYPI
- `python-gitlab` - Python library for GitLab API
- `gitlab` - GitLab Python client

#### RUBY
- `gitlab` - GitLab API Ruby wrapper

#### GO
- `github.com/xanzy/go-gitlab` - GitLab Go client

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate GitLab CI usage*

- `.gitlab-ci.yml` - Main GitLab CI configuration file (strong indicator)
- `.gitlab-ci.yaml` - Alternative extension
- `.gitlab/ci/*.yml` - Included CI configuration files
- `.gitlab/ci/*.yaml` - Included CI configuration files

### Configuration Directories
*Known directories that indicate GitLab CI usage*

- `.gitlab/` - GitLab configuration directory
- `.gitlab/ci/` - GitLab CI includes directory

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `import\s+.*\s+from\s+['"]@gitbeaker`
- Gitbeaker import
- Example: `import { Gitlab } from '@gitbeaker/rest';`

**Pattern**: `import\s+.*\s+from\s+['"]gitlab['"]`
- GitLab client import
- Example: `import Gitlab from 'gitlab';`

**Pattern**: `require\(['"]@gitbeaker`
- Gitbeaker require
- Example: `const { Gitlab } = require('@gitbeaker/rest');`

**Pattern**: `require\(['"]gitlab['"]\)`
- GitLab client require
- Example: `const Gitlab = require('gitlab');`

#### Python
Extensions: `.py`

**Pattern**: `^import\s+gitlab`
- GitLab Python import
- Example: `import gitlab`

**Pattern**: `^from\s+gitlab\s+import`
- GitLab Python from import
- Example: `from gitlab import Gitlab`

### Code Patterns
*GitLab CI YAML patterns in config files*

**Pattern**: `^stages:\s*$`
- Stages declaration
- Example: `stages:`

**Pattern**: `^include:\s*$`
- Include section for templates
- Example: `include:`

**Pattern**: `^\s+- template:\s*`
- GitLab CI template reference
- Example: `- template: Security/SAST.gitlab-ci.yml`

**Pattern**: `^\s+- project:\s*`
- Include from another project
- Example: `- project: 'my-group/my-project'`

**Pattern**: `^\s+- remote:\s*`
- Include from remote URL
- Example: `- remote: 'https://example.com/ci-template.yml'`

**Pattern**: `^\s+script:\s*$`
- Script section
- Example: `script:`

**Pattern**: `^\s+before_script:\s*$`
- Before script section
- Example: `before_script:`

**Pattern**: `^\s+after_script:\s*$`
- After script section
- Example: `after_script:`

**Pattern**: `^\s+image:\s*`
- Docker image specification
- Example: `image: node:18`

**Pattern**: `^\s+services:\s*$`
- Services section
- Example: `services:`

**Pattern**: `^\s+cache:\s*$`
- Cache section
- Example: `cache:`

**Pattern**: `^\s+artifacts:\s*$`
- Artifacts section
- Example: `artifacts:`

**Pattern**: `^\s+rules:\s*$`
- Rules section (GitLab-specific)
- Example: `rules:`

**Pattern**: `^\s+- if:\s*`
- Conditional rule
- Example: `- if: $CI_COMMIT_BRANCH == "main"`

**Pattern**: `^\s+only:\s*$`
- Only conditions (legacy)
- Example: `only:`

**Pattern**: `^\s+except:\s*$`
- Except conditions (legacy)
- Example: `except:`

**Pattern**: `^\s+environment:\s*`
- Environment specification
- Example: `environment: production`

**Pattern**: `^\s+needs:\s*$`
- Job dependencies (DAG)
- Example: `needs:`

**Pattern**: `^\s+extends:\s*`
- Template extension
- Example: `extends: .base-job`

**Pattern**: `^\.[a-z_-]+:\s*$`
- Hidden job template
- Example: `.base-job:`

---

## Environment Variables

- `GITLAB_CI` - Set to true in GitLab CI
- `CI` - Set to true in GitLab CI
- `CI_COMMIT_REF_NAME` - Branch or tag name
- `CI_COMMIT_REF_SLUG` - Slug of branch or tag
- `CI_COMMIT_SHA` - Full commit SHA
- `CI_COMMIT_SHORT_SHA` - Short commit SHA (8 chars)
- `CI_COMMIT_BRANCH` - Branch name
- `CI_COMMIT_TAG` - Tag name if building a tag
- `CI_COMMIT_MESSAGE` - Full commit message
- `CI_JOB_ID` - Unique job ID
- `CI_JOB_NAME` - Job name
- `CI_JOB_STAGE` - Stage name
- `CI_JOB_TOKEN` - CI job token
- `CI_PIPELINE_ID` - Pipeline ID
- `CI_PIPELINE_SOURCE` - How pipeline was triggered
- `CI_PROJECT_DIR` - Full path of repository
- `CI_PROJECT_ID` - Project ID
- `CI_PROJECT_NAME` - Project name
- `CI_PROJECT_NAMESPACE` - Project namespace
- `CI_PROJECT_PATH` - Full project path
- `CI_PROJECT_URL` - Project URL
- `CI_REGISTRY` - Container registry address
- `CI_REGISTRY_IMAGE` - Registry image for project
- `CI_SERVER_URL` - GitLab server URL
- `GITLAB_USER_EMAIL` - User email
- `GITLAB_USER_LOGIN` - Username

## Detection Notes

- `.gitlab-ci.yml` is the strongest indicator of GitLab CI usage
- `include:` directive enables modular CI configuration
- `rules:` is the modern replacement for `only:`/`except:`
- Hidden jobs (starting with `.`) are templates
- `needs:` enables directed acyclic graph (DAG) pipelines
- GitLab CI supports both self-hosted and SaaS (gitlab.com)

---

## TIER 3: Configuration Extraction

These patterns extract specific configuration values from GitLab CI configuration.

### Variable Reference Extraction

**Pattern**: `\$([A-Z_][A-Z0-9_]*)`
- GitLab CI variables referenced
- Extracts: `variable_name`
- Example: `$AWS_ACCESS_KEY_ID`
- Filter out: `CI_*`, `GITLAB_*` (built-in variables)

**Pattern**: `\$\{([A-Z_][A-Z0-9_]*)\}`
- GitLab CI variables (braced syntax)
- Extracts: `variable_name`
- Example: `${DOCKER_REGISTRY}`

### Container Registry Extraction

**Pattern**: `image:\s*['"]?([a-z0-9.-]+(?::[0-9]+)?/[^:'"]+)(?::([^'"]+))?['"]?`
- Container image with registry
- Extracts: `registry`, `image`, `tag`
- Example: `image: registry.gitlab.com/mygroup/myproject:latest`

**Pattern**: `CI_REGISTRY_IMAGE`
- GitLab Container Registry used
- Extracts: Indicates GitLab registry usage
- Example: `image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA`

### Include Template Extraction

**Pattern**: `-\s*template:\s*['"]?([^'"]+)['"]?`
- GitLab CI template references
- Extracts: `template_name`
- Example: `- template: Security/SAST.gitlab-ci.yml`

**Pattern**: `-\s*project:\s*['"]([^'"]+)['"]`
- Cross-project CI includes
- Extracts: `project_path`
- Example: `- project: 'my-group/ci-templates'`

### Environment Extraction

**Pattern**: `environment:\s*(?:name:\s*)?['"]?([a-zA-Z0-9_-]+)['"]?`
- Deployment environment
- Extracts: `environment_name`
- Example: `environment: production`

**Pattern**: `url:\s*['"]?(https?://[^'"]+)['"]?`
- Environment URL
- Extracts: `environment_url`
- Example: `url: https://app.example.com`

### AWS Integration Extraction

**Pattern**: `AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_ACCOUNT_ID`
- AWS variables used
- Extracts: `aws_integration`
- Example: `$AWS_ACCESS_KEY_ID`

**Pattern**: `([0-9]{12})\.dkr\.ecr\.([a-z]{2}-[a-z]+-[0-9])\.amazonaws\.com`
- AWS ECR registry
- Extracts: `aws_account_id`, `aws_region`
- Example: `123456789012.dkr.ecr.us-west-2.amazonaws.com`

### Kubernetes Deployment Extraction

**Pattern**: `KUBE_CONTEXT:\s*['"]?([^'"]+)['"]?`
- Kubernetes context/cluster
- Extracts: `kube_context`
- Example: `KUBE_CONTEXT: my-cluster`

**Pattern**: `KUBE_NAMESPACE:\s*['"]?([^'"]+)['"]?`
- Kubernetes namespace
- Extracts: `kube_namespace`
- Example: `KUBE_NAMESPACE: production`

### Runner Tag Extraction

**Pattern**: `tags:\s*\n(\s+-\s*[a-zA-Z0-9_-]+\s*\n?)+`
- Runner tags used
- Extracts: `runner_tags`
- Example: `tags: [docker, aws, production]`

### Extraction Output Example

```json
{
  "extractions": {
    "variables_referenced": [
      "DOCKER_REGISTRY",
      "AWS_ACCESS_KEY_ID",
      "DEPLOY_TOKEN"
    ],
    "container_registries": [
      {
        "type": "gitlab",
        "url": "registry.gitlab.com/mygroup/myproject",
        "source_file": ".gitlab-ci.yml"
      }
    ],
    "templates_included": [
      "Security/SAST.gitlab-ci.yml",
      "Jobs/Build.gitlab-ci.yml"
    ],
    "cross_project_includes": [
      {
        "project": "my-group/ci-templates",
        "file": "/templates/deploy.yml"
      }
    ],
    "environments": [
      {
        "name": "production",
        "url": "https://app.example.com"
      },
      {
        "name": "staging",
        "url": "https://staging.example.com"
      }
    ],
    "kubernetes": {
      "contexts": ["prod-cluster", "staging-cluster"],
      "namespaces": ["production", "staging"]
    }
  }
}
```
