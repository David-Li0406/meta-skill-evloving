# Concourse CI Resource Types Catalog

Comprehensive list of available resource types organized by category.

## Core Resources (Bundled with Concourse)

| Resource | Repository | Description |
|----------|------------|-------------|
| `git` | concourse/git-resource | Track commits in a Git repository branch |
| `registry-image` | concourse/registry-image-resource | OCI/Docker images in container registries |
| `s3` | concourse/s3-resource | AWS S3 and compatible object storage |
| `time` | concourse/time-resource | Trigger on time intervals |
| `pool` | concourse/pool-resource | Manage locks and shared state via Git |
| `semver` | concourse/semver-resource | Semantic version management |
| `github-release` | concourse/github-release-resource | GitHub release artifacts |

---

## Version Control

### Git

| Resource | Repository | Use Case |
|----------|------------|----------|
| `git` | concourse/git-resource | Standard Git operations |
| `git-branches` | aoldershaw/git-branches-resource | Track branch creation/deletion |
| `bitbucket-pr` | zarplata/concourse-bitbucket-pullrequest-resource | Bitbucket pull requests |
| `github-pr` | teliaoss/github-pr-resource | GitHub pull requests |
| `gitlab-mr` | swisscom/gitlab-merge-request-resource | GitLab merge requests |
| `gerrit` | google/concourse-resources/gerrit | Gerrit code review |

### Example: Git Branches Resource

```yaml
resource_types:
- name: git-branches
  type: registry-image
  source:
    repository: aoldershaw/git-branches-resource

resources:
- name: feature-branches
  type: git-branches
  source:
    uri: https://github.com/org/repo
    branch_regex: "feature/.*"
    private_key: ((git.private_key))
```

---

## Container Images

| Resource | Repository | Use Case |
|----------|------------|----------|
| `registry-image` | concourse/registry-image-resource | Modern OCI image handling |
| `docker-image` | concourse/docker-image-resource | Legacy Docker build/push |
| `registry-tag` | tlwr/registry-tag-resource | Track tags without pulling images |
| `harbor-resource` | pivotalservices/concourse-harbor-resource | Harbor registry integration |

### Example: Registry Tag Resource

```yaml
resource_types:
- name: registry-tag
  type: registry-image
  source:
    repository: ghcr.io/tlwr/registry-tag-resource

resources:
- name: base-image-tags
  type: registry-tag
  source:
    repository: node
    tag_regex: "^20-.*"
```

---

## Cloud Providers

### AWS

| Resource | Repository | Use Case |
|----------|------------|----------|
| `s3` | concourse/s3-resource | S3 object storage |
| `ssm` | (var source) | AWS Systems Manager parameters |
| `secretsmanager` | (var source) | AWS Secrets Manager |
| `ecr` | Use registry-image with aws_* params | Elastic Container Registry |
| `cloudformation` | ljfranklin/cloudformation-resource | CloudFormation stacks |
| `lambda` | starkandwayne/lambda-resource | Lambda function deployment |

### Google Cloud

| Resource | Repository | Use Case |
|----------|------------|----------|
| `gcs` | frodenas/gcs-resource | Google Cloud Storage |
| `gke` | google/concourse-resources/gke | GKE cluster operations |
| `gcr` | Use registry-image | Google Container Registry |

### Azure

| Resource | Repository | Use Case |
|----------|------------|----------|
| `azure-blobstore` | pivotal-cf/azure-blobstore-resource | Azure Blob Storage |
| `acr` | Use registry-image | Azure Container Registry |

---

## Kubernetes & Infrastructure

| Resource | Repository | Use Case |
|----------|------------|----------|
| `kubernetes` | zlabjp/kubernetes-resource | kubectl operations |
| `helm` | linkerd/helm-chart-resource | Helm chart management |
| `helm3` | typositoire/concourse-helm3-resource | Helm 3 deployments |
| `terraform` | ljfranklin/terraform-resource | Terraform operations |
| `pulumi` | ringods/pulumi-resource | Pulumi deployments |
| `cf` | concourse/cf-resource | Cloud Foundry apps |
| `bosh-deployment` | cloudfoundry/bosh-deployment-resource | BOSH deployments |
| `ansible-playbook` | troykinsella/concourse-ansible-playbook-resource | Ansible deployments |

### Example: Ansible Playbook Resource

```yaml
resource_types:
- name: ansible-playbook
  type: registry-image
  source:
    repository: troykinsella/concourse-ansible-playbook-resource
    tag: latest

resources:
- name: deploy-playbook
  type: ansible-playbook
  source:
    ssh_private_key: ((ssh.private_key))
    env:
      ANSIBLE_HOST_KEY_CHECKING: "false"
      APP_USER: ((app.user))
      APP_PASSWORD: ((app.password))

jobs:
- name: deploy
  plan:
  - get: source
    trigger: true
    passed: [build]
  - put: deploy-playbook
    params:
      path: source/ansible
      playbook: playbooks/deploy.yml
      inventory: inventory/hosts
      limit: production        # Target specific host group
      tags:                    # Run only tagged tasks
      - deploy
      - configure
      extra_vars:
        app_version: "1.2.3"
      setup_commands:          # Run before playbook
      - "pip install boto3"
```

### Example: Terraform Resource

```yaml
resource_types:
- name: terraform
  type: registry-image
  source:
    repository: ljfranklin/terraform-resource

resources:
- name: infrastructure
  type: terraform
  source:
    env_name: production
    backend_type: s3
    backend_config:
      bucket: terraform-state
      key: infra/terraform.tfstate
      region: us-east-1

jobs:
- name: provision
  plan:
  - get: infra-repo
    trigger: true
  - put: infrastructure
    params:
      terraform_source: infra-repo/terraform
      vars:
        instance_type: t3.medium
        environment: production
```

---

## Notifications

| Resource | Repository | Use Case |
|----------|------------|----------|
| `slack-notification` | cfcommunity/slack-notification-resource | Slack webhooks |
| `slack-alert` | arbourd/concourse-slack-alert-resource | Formatted Slack alerts |
| `teams-notification` | navicore/teams-notification-resource | Microsoft Teams |
| `email` | mdomke/concourse-email-resource | Email notifications |
| `http-resource` | jgriff/http-resource | Generic HTTP/webhook |

### Example: Slack Notification

```yaml
resource_types:
- name: slack-notification
  type: registry-image
  source:
    repository: cfcommunity/slack-notification-resource

resources:
- name: slack
  type: slack-notification
  source:
    url: ((slack.webhook_url))

jobs:
- name: build
  plan:
  - get: source
    trigger: true
  - task: build
    file: source/ci/tasks/build.yml
  on_success:
    put: slack
    params:
      text: ":white_check_mark: Build succeeded!"
      channel: "#ci-notifications"
  on_failure:
    put: slack
    params:
      text: ":x: Build failed!"
      channel: "#ci-notifications"
```

---

## Artifact Management

| Resource | Repository | Use Case |
|----------|------------|----------|
| `artifactory` | pivotalservices/artifactory-resource | JFrog Artifactory |
| `maven` | pivotalservices/maven-resource | Maven repositories |
| `npm` | idahobean/npm-resource | NPM packages |
| `pypi` | cfmobile/pypi-resource | Python packages |
| `rubygems` | troykinsella/concourse-rubygems-resource | Ruby gems |
| `github-release` | concourse/github-release-resource | GitHub releases |

---

## Databases

| Resource | Repository | Use Case |
|----------|------------|----------|
| `pool` | concourse/pool-resource | Database/resource locking |
| `postgres` | (via scripts) | PostgreSQL operations |
| `flyway` | troykinsella/concourse-flyway-resource | Flyway migrations |

---

## Monitoring & Metrics

| Resource | Repository | Use Case |
|----------|------------|----------|
| `datadog-event` | concourse/datadog-event-resource | Datadog events |
| `prometheus-alertmanager` | (community) | Alert management |
| `cogito` | Pix4D/cogito | GitHub commit status |

### Example: GitHub Commit Status

```yaml
resource_types:
- name: cogito
  type: registry-image
  source:
    repository: pix4d/cogito

resources:
- name: commit-status
  type: cogito
  check_every: never
  source:
    owner: org
    repo: repo
    access_token: ((github.token))

jobs:
- name: build
  plan:
  - get: source
    trigger: true
  - put: commit-status
    params:
      state: pending
      context: build
  - task: build
    file: source/ci/tasks/build.yml
    on_success:
      put: commit-status
      params:
        state: success
        context: build
    on_failure:
      put: commit-status
      params:
        state: failure
        context: build
```

---

## Build Tools

| Resource | Repository | Use Case |
|----------|------------|----------|
| `oci-build-task` | concourse/oci-build-task | Container image building |
| `builder-task` | concourse/builder-task | Alternative image builder |

### Example: OCI Build Task

```yaml
jobs:
- name: build-image
  plan:
  - get: source
    trigger: true
  - task: build
    privileged: true
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
      params:
        CONTEXT: source
        DOCKERFILE: source/Dockerfile
      run:
        path: build
  - put: app-image
    params:
      image: image/image.tar
```

---

## RSS & Feeds

| Resource | Repository | Use Case |
|----------|------------|----------|
| `rss` | suhlig/concourse-rss-resource | RSS feed monitoring |
| `feed` | (community) | Generic feed parsing |

---

## Custom Resource Development

Create custom resources by implementing three scripts:

```bash
/opt/resource/check   # Detect versions
/opt/resource/in      # Fetch version
/opt/resource/out     # Update/push
```

### Minimal Custom Resource

```dockerfile
FROM alpine:latest

RUN apk add --no-cache bash jq curl

COPY check /opt/resource/check
COPY in /opt/resource/in
COPY out /opt/resource/out

RUN chmod +x /opt/resource/*
```

### Pipeline Registration

```yaml
resource_types:
- name: custom-resource
  type: registry-image
  source:
    repository: myregistry/custom-resource
    tag: latest

resources:
- name: my-custom
  type: custom-resource
  source:
    config_option: value
```

---

## Resource Discovery

Find more resources at:
- [Concourse Resource Types Catalog](https://concourse-ci.org/resource-types-list/)
- [Concourse GitHub Organization](https://github.com/concourse)
- [Community Resources on GitHub](https://github.com/topics/concourse-resource)
