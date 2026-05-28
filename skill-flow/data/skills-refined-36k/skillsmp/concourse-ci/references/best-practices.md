# Concourse CI Best Practices and Troubleshooting

Optimization patterns, common pitfalls, and debugging strategies.

## Pipeline Organization

### Use YAML Anchors for DRY Configuration

```yaml
# Top of pipeline: define reusable snippets
git-source: &git-source
  username: ((gitlab.USER))
  password: ((gitlab.ACCESS_TOKEN))

registry-source: &registry-source
  username: ((registry.USER))
  password: ((registry.PASSWORD))

notify-failure: &notify-failure
  put: slack
  params:
    text: '((SLACK_ICON_FAILURE)) $BUILD_PIPELINE_NAME/$BUILD_JOB_NAME failed'

notify-success: &notify-success
  put: slack
  params:
    text: '((SLACK_ICON_SUCCESS)) $BUILD_PIPELINE_NAME/$BUILD_JOB_NAME succeeded'

# Use anchors in resources
resources:
- name: repo-main
  type: git
  source:
    <<: *git-source
    uri: https://git.example.com/org/repo.git
    branch: main

- name: repo-staging
  type: git
  source:
    <<: *git-source
    uri: https://git.example.com/org/repo.git
    branch: staging

# Use anchors in jobs
jobs:
- name: build
  plan:
  - get: repo-main
    trigger: true
  - task: build
    file: repo-main/ci/tasks/build.yml
  on_failure:
    <<: *notify-failure
```

### Group Jobs Logically

```yaml
groups:
- name: all
  jobs: ["*"]

- name: build
  jobs:
  - compile
  - test
  - package

- name: deploy
  jobs:
  - deploy-staging
  - deploy-prod

- name: maintenance
  jobs:
  - update-dependencies
  - cleanup-images
```

### Separate Read and Write Resources

Avoid using the same resource for both tracking versions and pushing changes:

```yaml
# BAD: Mixed read/write
resources:
- name: repo
  type: git
  source:
    uri: https://github.com/org/repo
    branch: main
    tag_regex: "^v.*"

jobs:
- name: release
  plan:
  - get: repo
    trigger: true
  - task: bump-version
  - put: repo  # Creates version conflicts!
    params:
      repository: repo
      tag: version/tag

# GOOD: Separate resources
resources:
- name: repo-read
  type: git
  source:
    uri: https://github.com/org/repo
    branch: main
    tag_regex: "^v.*"
    fetch_tags: true
    clean_tags: true

- name: repo-write
  type: git
  source:
    uri: https://github.com/org/repo
    branch: main
    fetch_tags: true

jobs:
- name: release
  plan:
  - get: repo-read
    trigger: true
  - task: bump-version
  - put: repo-write
    params:
      repository: repo-read
      tag: version/tag
```

---

## Git Resource Gotchas

### Tag Detection After Force Push

**Problem**: Concourse stops detecting new tags after force-pushing a branch.

**Root Causes**:

1. **Tags unreachable from branch**: After force push, tags may point to commits no longer on the tracked branch
2. **Version model conflict**: Concourse's append-only version tracking conflicts with rewritten history
3. **Cached tag state**: Old tags cached in resource state

**Diagnosis**:

```bash
# Check if tag is reachable from branch
git fetch --tags origin
git branch -r --contains <tag_commit_sha>  # Should show origin/main
# OR
git merge-base --is-ancestor <tag_commit_sha> origin/main  # Should succeed
```

**Solutions**:

```yaml
# 1. Enable tag cleanup
resources:
- name: repo
  type: git
  source:
    uri: https://github.com/org/repo
    branch: main
    tag_regex: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"
    fetch_tags: true
    clean_tags: true  # Critical: clears cached tags

# 2. Force resource check from specific ref
# fly -t target check-resource -r pipeline/repo --from ref:abc123
```

**Best Practice**: Treat release branches and tags as immutable. Never force-push.

### Regex Escaping

**Problem**: Unescaped dots match any character.

```yaml
# BAD: . matches any character
tag_regex: "^v[0-9]+.[0-9]+.[0-9]+$"  # Matches v1a2b3 too

# GOOD: Escape literal dots
tag_regex: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"
```

### Branch vs Tag Tracking

```yaml
# Track branch commits
- name: repo-branch
  type: git
  source:
    branch: main

# Track tags (no branch needed for triggering)
- name: repo-tags
  type: git
  source:
    branch: main  # Still needed for put operations
    tag_regex: "^v.*"

# Tag filtering modes
tag_filter: "v*"      # Bash glob (simple patterns)
tag_regex: "^v[0-9]"  # Extended grep regex (complex patterns)
```

### Path Filtering Optimization

```yaml
resources:
- name: app-source
  type: git
  source:
    uri: https://github.com/org/repo
    branch: main
    # Only trigger on application code changes
    paths:
    - src/**
    - lib/**
    - package.json
    - package-lock.json
    # Ignore documentation and CI changes
    ignore_paths:
    - "**/*.md"
    - docs/**
    - ci/**
    - .github/**
```

---

## Performance Optimization

### Parallel Execution

```yaml
# Parallel independent steps
- in_parallel:
    limit: 5  # Control concurrency
    fail_fast: true  # Stop on first failure
    steps:
    - get: dependency-a
    - get: dependency-b
    - get: dependency-c

# Parallel tests
- in_parallel:
    steps:
    - task: unit-tests
    - task: integration-tests
    - task: e2e-tests
```

### Task Caching

```yaml
# Cache dependencies between runs
platform: linux
image_resource:
  type: registry-image
  source:
    repository: node
    tag: 20

caches:
- path: source/node_modules
- path: source/.npm

run:
  path: /bin/bash
  args:
  - -c
  - |
    cd source
    npm ci  # Uses cache if available
    npm run build
```

### Shallow Clones

```yaml
# For builds that don't need git history
- get: source
  params:
    depth: 1
```

### Resource Check Intervals

```yaml
# Reduce load for stable resources
resources:
- name: base-image
  type: registry-image
  check_every: 24h  # Daily check
  source:
    repository: node
    tag: 20-alpine

- name: source-code
  type: git
  check_every: 1m  # Frequent check for active development
  source:
    uri: https://github.com/org/repo
```

### Serial Groups

```yaml
# Prevent resource contention
jobs:
- name: deploy-staging
  serial_groups: [deploy]
  plan:
  - get: app-image
  - task: deploy

- name: deploy-prod
  serial_groups: [deploy]
  plan:
  - get: app-image
  - task: deploy
```

---

## Security Best Practices

### Credential Management

```yaml
# Use var sources (Vault, SSM, etc.)
var_sources:
- name: vault
  type: vault
  config:
    url: https://vault.example.com
    path_prefix: /concourse/main

# Reference credentials
resources:
- name: repo
  type: git
  source:
    username: ((vault:git.username))
    password: ((vault:git.token))
```

### Minimize Privileged Tasks

```yaml
# Only use privileged when absolutely necessary
- task: docker-build
  privileged: true  # Required for Docker-in-Docker
  file: source/ci/tasks/build-image.yml

# Prefer oci-build-task over Docker-in-Docker
- task: build-image
  privileged: true  # Still needed but more secure
  config:
    platform: linux
    image_resource:
      type: registry-image
      source:
        repository: concourse/oci-build-task
    inputs:
    - name: source
    outputs:
    - name: image
    run:
      path: build
```

### Resource Visibility

```yaml
# Keep sensitive resources private
resources:
- name: credentials
  type: git
  public: false  # Default, but be explicit
  source:
    uri: git@github.com:org/secrets.git

# Only expose what's necessary
- name: public-docs
  type: git
  public: true
  source:
    uri: https://github.com/org/docs.git
```

---

## Debugging Strategies

### Hijack into Containers

```bash
# Hijack into a running or failed build
fly -t target hijack -j pipeline/job -b 123

# Hijack specific step
fly -t target hijack -j pipeline/job -s task-name

# List hijack targets
fly -t target hijack -j pipeline/job --list
```

### Check Resource Versions

```bash
# List versions
fly -t target resource-versions -r pipeline/resource

# Force check
fly -t target check-resource -r pipeline/resource

# Check from specific version
fly -t target check-resource -r pipeline/resource --from ref:abc123
```

### Watch Build Logs

```bash
# Stream live logs
fly -t target watch -j pipeline/job

# Specific build
fly -t target watch -j pipeline/job -b 123
```

### Validate Pipeline

```bash
# Syntax check
fly -t target validate-pipeline -c pipeline.yml

# With variables
fly -t target validate-pipeline -c pipeline.yml -l vars.yml
```

### Debug Task Locally

```bash
# Execute task with local inputs
fly -t target execute -c ci/tasks/build.yml \
  -i source=. \
  -o artifacts=./out

# Include ignored files (e.g., .gitignore'd)
fly -t target execute --include-ignored -c ci/tasks/build.yml -i source=.
```

---

## Common Patterns

### Build-Test-Release with Gates

```yaml
jobs:
- name: build
  plan:
  - get: source
    trigger: true
  - task: compile
    file: source/ci/tasks/compile.yml
  - put: artifact-rc
    params:
      file: build/app-*.tar.gz

- name: test
  plan:
  - get: artifact-rc
    passed: [build]
    trigger: true
  - get: source
    passed: [build]
  - task: integration-test
    file: source/ci/tasks/test.yml

- name: release
  plan:
  - get: artifact-rc
    passed: [test]
    trigger: true
  - get: version
    params:
      bump: minor
  - put: artifact-release
    params:
      file: artifact-rc/app-*.tar.gz
      tag: version/version
  - put: version
    params:
      file: version/version
```

### Manual Deployment Gate

```yaml
- name: deploy-prod
  plan:
  - get: app-image
    passed: [deploy-staging]
    # No trigger: true - requires manual click
  - task: deploy
    file: source/ci/tasks/deploy.yml
    params:
      ENVIRONMENT: production
```

### Scheduled Jobs

```yaml
resources:
- name: nightly
  type: time
  source:
    start: 2:00 AM
    stop: 3:00 AM
    location: America/New_York

- name: weekday-morning
  type: time
  source:
    start: 9:00 AM
    stop: 9:30 AM
    location: Europe/Berlin
    days: [Monday, Tuesday, Wednesday, Thursday, Friday]

jobs:
- name: nightly-cleanup
  plan:
  - get: nightly
    trigger: true
  - task: cleanup
    file: ci/tasks/cleanup.yml

- name: weekday-update
  plan:
  - get: weekday-morning
    trigger: true
  - get: source
  - task: update-dependencies
    file: source/ci/tasks/update.yml
```

### Multi-Environment Deploy with `across`

Modern approach using the `across` step modifier:

```yaml
jobs:
- name: deploy
  plan:
  - get: app-image
    trigger: true
  - get: source
  - task: deploy
    across:
    - var: env
      values: [dev, staging, prod]
      max_in_flight: 1  # Sequential deployment
    file: source/ci/tasks/deploy.yml
    params:
      ENVIRONMENT: ((.:env))
      CONFIG: source/config/((.:env)).yml
```

### Environment-Specific Resources (Traditional Pattern)

When `across` isn't suitable, use separate resources per environment:

```yaml
# Define anchor for common settings
git-source: &git-source
  uri: https://github.com/org/repo
  username: ((git.username))
  password: ((git.password))

resources:
- name: repo-staging
  type: git
  source:
    <<: *git-source
    branch: staging

- name: repo-prod
  type: git
  source:
    <<: *git-source
    branch: prod

- name: image-staging
  type: registry-image
  source:
    repository: registry.example.com/org/app
    tag: staging
    username: ((registry.user))
    password: ((registry.pass))

- name: image-prod
  type: registry-image
  source:
    repository: registry.example.com/org/app
    tag: prod
    username: ((registry.user))
    password: ((registry.pass))
```

---

## Notification Patterns

### Modern: Dedicated Notification Resources

Use specialized resources for better formatting and features:

**Slack (Recommended: arbourd/concourse-slack-alert-resource)**

```yaml
resource_types:
- name: slack-alert
  type: registry-image
  source:
    repository: arbourd/concourse-slack-alert-resource

resources:
- name: notify
  type: slack-alert
  source:
    url: ((slack.webhook_url))
    channel: "#builds"

jobs:
- name: build
  plan:
  - get: source
    trigger: true
  - task: build
    file: source/ci/tasks/build.yml
  on_success:
    put: notify
    params:
      alert_type: success
  on_failure:
    put: notify
    params:
      alert_type: failed
```

**Microsoft Teams**

```yaml
resource_types:
- name: teams-notification
  type: registry-image
  source:
    repository: navicore/teams-notification-resource

resources:
- name: teams
  type: teams-notification
  source:
    url: ((teams.webhook_url))

jobs:
- name: deploy
  on_failure:
    put: teams
    params:
      text: "Deploy failed: $BUILD_PIPELINE_NAME/$BUILD_JOB_NAME"
      color: "FF0000"
```

### Generic: HTTP Resource for Custom Webhooks

For Matrix, Element, Discord, or custom endpoints:

```yaml
resource_types:
- name: http-resource
  type: registry-image
  source:
    repository: jgriff/http-resource

resources:
- name: webhook
  type: http-resource
  source:
    url: https://hooks.example.com/notify
    headers:
      Content-Type: application/json
      Authorization: Bearer ((webhook.token))
    out_only: true          # No check/get operations
    sensitive: true         # Hide response in logs
    build_metadata: [headers, body]  # Enable CI variable resolution

# Usage with CI metadata variables
- put: webhook
  params:
    body: |
      {
        "pipeline": "$BUILD_PIPELINE_NAME",
        "job": "$BUILD_JOB_NAME",
        "build": "$BUILD_NAME",
        "url": "$ATC_EXTERNAL_URL/builds/$BUILD_ID",
        "status": "failed"
      }
```

### Notification Anchor Pattern

DRY notification configuration:

```yaml
# Top of pipeline
notify-success: &notify-success
  put: notify
  params:
    alert_type: success

notify-failure: &notify-failure
  put: notify
  params:
    alert_type: failed

jobs:
- name: build
  plan:
  - get: source
  - task: build
    file: source/ci/tasks/build.yml
  on_success:
    <<: *notify-success
  on_failure:
    <<: *notify-failure

- name: deploy
  plan:
  - get: source
    passed: [build]
  - task: deploy
    file: source/ci/tasks/deploy.yml
  on_success:
    <<: *notify-success
  on_failure:
    <<: *notify-failure
```

---

## Deployment Patterns

### Ansible Playbook Execution

For infrastructure provisioning with Ansible:

```yaml
resource_types:
- name: ansible-playbook
  type: registry-image
  source:
    repository: troykinsella/concourse-ansible-playbook-resource
    tag: latest

resources:
- name: ansible-deploy
  type: ansible-playbook
  source:
    ssh_private_key: ((ssh.private_key))
    env:
      ANSIBLE_HOST_KEY_CHECKING: "false"
      SSH_USER: ((ssh.user))

jobs:
- name: provision
  plan:
  - get: infrastructure-repo
    trigger: true
  - put: ansible-deploy
    params:
      path: infrastructure-repo/ansible
      playbook: playbooks/provision.yml
      inventory: inventory/hosts
      limit: production  # Target host group
      extra_vars:
        app_version: "1.2.3"
```

### Task-Based Ansible (Alternative)

For simpler setups without the resource type:

```yaml
- task: ansible-deploy
  config:
    platform: linux
    image_resource:
      type: registry-image
      source:
        repository: cytopia/ansible
        tag: latest
    inputs:
    - name: source
    params:
      ANSIBLE_HOST_KEY_CHECKING: "false"
      SSH_PRIVATE_KEY: ((ssh.private_key))
    run:
      path: /bin/sh
      args:
      - -c
      - |
        mkdir -p ~/.ssh
        echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa
        cd source/ansible
        ansible-playbook -i inventory/hosts playbook.yml
```

### Cross-Repository Pipeline Triggers

Trigger downstream pipelines by pushing to other repositories:

```yaml
- task: trigger-downstream
  config:
    platform: linux
    image_resource:
      type: registry-image
      source:
        repository: alpine/git
    inputs:
    - name: source
    params:
      GIT_USER: ((git.username))
      GIT_TOKEN: ((git.token))
      DOWNSTREAM_REPO: https://github.com/org/downstream.git
    run:
      path: /bin/sh
      args:
      - -c
      - |
        VERSION=$(cat source/version)
        git clone https://${GIT_USER}:${GIT_TOKEN}@${DOWNSTREAM_REPO#https://} downstream
        cd downstream
        echo "$VERSION" > app-version
        git config user.email "ci@example.com"
        git config user.name "CI Bot"
        git add app-version
        git commit -m "Update app version to $VERSION"
        git push origin main
```

---

## Troubleshooting Checklist

### Pipeline Not Triggering

1. Check resource is not paused: `fly -t target unpause-resource -r pipeline/resource`
2. Verify `trigger: true` on get step
3. Check resource versions: `fly -t target resource-versions -r pipeline/resource`
4. Force resource check: `fly -t target check-resource -r pipeline/resource`
5. Verify path filters aren't excluding changes

### Build Failing Silently

1. Check `ensure` steps for errors masking failures
2. Review `try` steps that swallow failures
3. Check container limits (OOM kills)
4. Hijack and inspect logs/state

### Credentials Not Working

1. Verify var source configuration
2. Check credential path/field names
3. Test credentials outside Concourse
4. Check var source connectivity from workers

### Resource Check Hanging

1. Increase `check_timeout`
2. Check network connectivity from workers
3. Verify worker tags match resource tags
4. Check for rate limiting on external services
