# Cicd Pipelines - Validations

## Possible secret exposure in echo/print

### **Id**
secrets-in-echo
### **Severity**
error
### **Type**
regex
### **Pattern**
  - echo.*\$\{\{\s*secrets\.
  - print.*\$\{\{\s*secrets\.
  - console\.log.*secrets\.
### **Message**
Never echo secrets - they'll appear in logs
### **Fix Action**
Pass secrets as environment variables instead
### **Applies To**
  - *.yml
  - *.yaml

## Using pull_request_target event

### **Id**
pull-request-target
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - on:\s*\n\s*pull_request_target
  - on:\s*\[?pull_request_target
### **Message**
pull_request_target can expose secrets to fork PRs
### **Fix Action**
Use pull_request instead, or audit checkout carefully
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Action pinned to mutable tag only

### **Id**
mutable-action-version
### **Severity**
info
### **Type**
regex
### **Pattern**
  - uses:\s*[^@]+@v\d+\s*$
  - uses:\s*[^@]+@main\s*$
  - uses:\s*[^@]+@master\s*$
### **Message**
Pin actions to full version or SHA for reproducibility
### **Fix Action**
Use actions/checkout@v4.1.1 or @sha
### **Applies To**
  - *.yml
  - *.yaml

## workflow_dispatch without inputs

### **Id**
workflow-dispatch-no-inputs
### **Severity**
info
### **Type**
regex
### **Pattern**
  - workflow_dispatch:\s*$
### **Message**
Consider adding inputs for manual workflow runs
### **Fix Action**
Add inputs for environment, version, etc.
### **Applies To**
  - .github/workflows/*.yml

## Job without timeout

### **Id**
no-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - jobs:\s*\n\s*\w+:\s*\n(?!.*timeout-minutes)
### **Message**
Jobs without timeout can run for 6 hours
### **Fix Action**
Add timeout-minutes to each job
### **Applies To**
  - *.yml
  - *.yaml

## Deploy workflow without concurrency control

### **Id**
no-concurrency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deploy(?!.*concurrency)
### **Message**
Deploy workflows should have concurrency control
### **Fix Action**
Add concurrency group to prevent race conditions
### **Applies To**
  - .github/workflows/*.yml

## Using ubuntu-latest

### **Id**
hardcoded-runner
### **Severity**
info
### **Type**
regex
### **Pattern**
  - runs-on:\s*ubuntu-latest
### **Message**
ubuntu-latest can change - consider pinning
### **Fix Action**
Use ubuntu-22.04 for reproducibility
### **Applies To**
  - *.yml
  - *.yaml

## npm/pip install without caching

### **Id**
no-caching
### **Severity**
info
### **Type**
regex
### **Pattern**
  - npm ci(?!.*cache)
  - npm install(?!.*cache)
  - pip install(?!.*cache)
### **Message**
Consider caching dependencies for faster builds
### **Fix Action**
Use setup-node/setup-python with cache option
### **Applies To**
  - *.yml
  - *.yaml

## Using deprecated set-output command

### **Id**
deprecated-set-output
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ::set-output name=
### **Message**
set-output is deprecated
### **Fix Action**
Use $GITHUB_OUTPUT instead
### **Applies To**
  - *.yml
  - *.yaml

## Using deprecated set-env command

### **Id**
deprecated-set-env
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ::set-env name=
### **Message**
set-env is deprecated and disabled for security
### **Fix Action**
Use $GITHUB_ENV instead
### **Applies To**
  - *.yml
  - *.yaml

## Using deprecated add-path command

### **Id**
add-path-deprecated
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ::add-path::
### **Message**
add-path is deprecated
### **Fix Action**
Use $GITHUB_PATH instead
### **Applies To**
  - *.yml
  - *.yaml

## GitLab job without rules

### **Id**
gitlab-no-rules
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^\w+:\s*\n\s+stage:(?!.*rules:)(?!.*only:)(?!.*except:)
### **Message**
Consider adding rules to control when job runs
### **Fix Action**
Add rules clause to control job execution
### **Applies To**
  - .gitlab-ci.yml