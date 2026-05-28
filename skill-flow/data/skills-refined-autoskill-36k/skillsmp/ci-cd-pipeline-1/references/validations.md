# Ci Cd Pipeline - Validations

## Unpinned GitHub Actions

### **Id**
cicd-unpinned-actions
### **Severity**
error
### **Type**
regex
### **Pattern**
  - uses:\s*[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@main
  - uses:\s*[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@master
  - uses:\s*[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@latest
### **Message**
Action using mutable reference (@main/@master/@latest). Supply chain attack vector.
### **Fix Action**
Pin to specific version (@v4) or SHA digest
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Secrets Potentially Logged

### **Id**
cicd-secrets-in-logs
### **Severity**
error
### **Type**
regex
### **Pattern**
  - echo.*\$\{\{\s*secrets\.
  - echo.*\$SECRET
  - echo.*\$TOKEN
  - echo.*\$PASSWORD
  - echo.*\$API_KEY
### **Message**
Secrets may be logged. GitHub Actions logs are visible to repo collaborators.
### **Fix Action**
Remove echo statements with secrets or use ::add-mask:: for derived values
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Dangerous pull_request_target Usage

### **Id**
cicd-pull-request-target-checkout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pull_request_target[\s\S]*?checkout[\s\S]*?head\.sha
  - pull_request_target[\s\S]*?checkout[\s\S]*?head\.ref
### **Message**
pull_request_target with checkout of PR head. Enables pwn request attacks.
### **Fix Action**
Use pull_request trigger or require manual approval label before checkout
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Missing Permissions Block

### **Id**
cicd-no-permissions-block
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*permissions:).*on:\s*\n\s*push:
### **Message**
No explicit permissions block. Workflow may have broader access than needed.
### **Fix Action**
Add permissions block with minimal required permissions
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Overly Broad Permissions

### **Id**
cicd-write-all-permissions
### **Severity**
error
### **Type**
regex
### **Pattern**
  - permissions:\s*write-all
  - permissions:\s*\n\s*contents:\s*write\s*\n\s*packages:\s*write\s*\n\s*issues:\s*write
### **Message**
Workflow has overly broad permissions. Compromised workflow can modify repo.
### **Fix Action**
Use minimal permissions. contents: read for most jobs, write only when needed.
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Self-Hosted Runner Potential Risk

### **Id**
cicd-self-hosted-public
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - runs-on:\s*self-hosted
  - runs-on:\s*\[self-hosted
### **Message**
Self-hosted runner detected. Dangerous if used in public repositories.
### **Fix Action**
Use GitHub-hosted runners for public repos or implement strict runner groups
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Hardcoded Secrets in Workflow

### **Id**
cicd-hardcoded-secrets
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password:\s*["'][^\${]+
  - api_key:\s*["'][^\${]+
  - token:\s*["'][^\${]+
  - secret:\s*["'][^\${]+
  - AWS_SECRET_ACCESS_KEY:\s*["'][^\${]+
### **Message**
Hardcoded secret value in workflow file. Will be visible in version control.
### **Fix Action**
Use GitHub Secrets and reference with ${{ secrets.SECRET_NAME }}
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Production Deploy Without Environment

### **Id**
cicd-no-environment-protection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)deploy.*prod(?!.*environment:)
  - (?i)release.*production(?!.*environment:)
### **Message**
Production deployment without environment protection. No approval required.
### **Fix Action**
Add environment: production to job and configure required reviewers
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Workflow Run Artifact Consumption

### **Id**
cicd-workflow-run-artifacts
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - workflow_run[\s\S]*?download-artifact
### **Message**
workflow_run consuming artifacts. Validate artifact source to prevent privilege escalation.
### **Fix Action**
Check github.event.workflow_run.head_repository.full_name matches base repo
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Debug Mode Enabled

### **Id**
cicd-debug-enabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ACTIONS_STEP_DEBUG:\s*true
  - ACTIONS_RUNNER_DEBUG:\s*true
### **Message**
Debug mode enabled. May expose sensitive information in logs.
### **Fix Action**
Remove debug flags for production workflows
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Job Without Timeout

### **Id**
cicd-no-timeout
### **Severity**
info
### **Type**
regex
### **Pattern**
  - runs-on:(?![\s\S]*?timeout-minutes)
### **Message**
Job without timeout-minutes. Hung jobs will consume runner minutes.
### **Fix Action**
Add timeout-minutes appropriate for job (e.g., 30 for most jobs)
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## No Concurrency Control

### **Id**
cicd-no-concurrency-control
### **Severity**
info
### **Type**
regex
### **Pattern**
  - on:\s*\n\s*push:(?![\s\S]*?concurrency:)
### **Message**
No concurrency control. Multiple runs may conflict or waste resources.
### **Fix Action**
Add concurrency group to cancel in-progress runs on new push
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Using Latest Docker Image Tag

### **Id**
cicd-latest-image-tag
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - image:\s*[a-zA-Z0-9_/-]+:latest
  - container:\s*[a-zA-Z0-9_/-]+:latest
### **Message**
Using :latest tag for container. Build not reproducible.
### **Fix Action**
Pin to specific image version or SHA digest
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Artifacts Without Retention Policy

### **Id**
cicd-artifact-no-retention
### **Severity**
info
### **Type**
regex
### **Pattern**
  - upload-artifact(?![\s\S]*?retention-days)
### **Message**
Artifact upload without retention-days. Default is 90 days.
### **Fix Action**
Add retention-days to limit storage costs
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Dependency Install Without Cache

### **Id**
cicd-no-cache
### **Severity**
info
### **Type**
regex
### **Pattern**
  - npm install(?![\s\S]{0,200}cache)
  - npm ci(?![\s\S]{0,200}cache)
  - pip install(?![\s\S]{0,200}cache)
### **Message**
Package install without caching. Slower builds and higher costs.
### **Fix Action**
Add actions/cache or setup-node with cache option
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Potential Shell Injection

### **Id**
cicd-shell-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - run:.*\$\{\{\s*github\.event\.issue\.title
  - run:.*\$\{\{\s*github\.event\.issue\.body
  - run:.*\$\{\{\s*github\.event\.pull_request\.title
  - run:.*\$\{\{\s*github\.event\.pull_request\.body
  - run:.*\$\{\{\s*github\.event\.comment\.body
### **Message**
User-controlled input in run command. Shell injection vulnerability.
### **Fix Action**
Use environment variable or escape input: env: TITLE: ${{ github.event.issue.title }}
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Continue on Error Without Handling

### **Id**
cicd-continue-on-error
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - continue-on-error:\s*true(?![\s\S]*?if:.*failure)
### **Message**
continue-on-error without failure handling. Errors may be silently ignored.
### **Fix Action**
Add conditional step to handle failures or remove continue-on-error
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml