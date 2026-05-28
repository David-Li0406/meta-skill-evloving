---
id: gitlab-cicd
name: "GitLab CI/CD"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# GitLab CI/CD

## Overview

GitLab CI/CD is an integrated continuous integration and delivery platform built into GitLab. It uses a `.gitlab-ci.yml` file to define pipelines with stages, jobs, and rules, supporting complex workflows, container registries, and Kubernetes integration.

## When to Use

- Projects hosted on GitLab (cloud or self-hosted)
- Organizations needing integrated DevSecOps platform
- Complex pipelines with parent-child relationships
- Projects requiring built-in container registry
- Teams using GitLab for project management

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Collection of jobs organized in stages |
| Stage | Group of jobs that run in parallel |
| Job | Individual task with script and configuration |
| Runner | Agent executing CI/CD jobs |
| Artifact | Files passed between jobs |
| Cache | Dependencies cached between pipelines |
| Environment | Deployment target with tracking |
| Rules | Conditional job execution |

### Pipeline Flow

```
┌────────────────────────────────────────────────────────────────┐
│                         Pipeline                               │
├──────────┬──────────┬──────────┬──────────┬──────────────────┤
│  build   │   test   │  scan    │  deploy  │     cleanup      │
├──────────┼──────────┼──────────┼──────────┼──────────────────┤
│ compile  │ unit     │ sast     │ staging  │ cleanup_staging  │
│ docker   │ integ    │ dast     │ prod     │                  │
│          │ e2e      │ secrets  │          │                  │
└──────────┴──────────┴──────────┴──────────┴──────────────────┘
```

## Implementation

### Complete CI/CD Pipeline

```yaml
# .gitlab-ci.yml

# Variables
variables:
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest
  KUBERNETES_VERSION: "1.28"
  NODE_VERSION: "20"

# Default settings
default:
  image: node:${NODE_VERSION}-alpine
  tags:
    - docker
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  interruptible: true

# Stages
stages:
  - build
  - test
  - security
  - package
  - deploy
  - cleanup

# Cache configuration
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/
  policy: pull-push

# Workflow rules
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_TAG

# ============================================
# BUILD STAGE
# ============================================

build:
  stage: build
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
      - node_modules/
    expire_in: 1 day
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_BUILDKIT: 1
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      docker build \
        --cache-from $IMAGE_LATEST \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --build-arg VERSION=$CI_COMMIT_SHA \
        --tag $IMAGE_TAG \
        --tag $IMAGE_LATEST \
        .
    - docker push $IMAGE_TAG
    - docker push $IMAGE_LATEST
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

# ============================================
# TEST STAGE
# ============================================

.test-template:
  stage: test
  needs:
    - build
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

unit-test:
  extends: .test-template
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_DB: test
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
  variables:
    DATABASE_URL: "postgres://test:test@db:5432/test"
  script:
    - npm run test:unit -- --coverage
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

integration-test:
  extends: .test-template
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_DB: test
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
    - name: redis:7
      alias: redis
  variables:
    DATABASE_URL: "postgres://test:test@db:5432/test"
    REDIS_URL: "redis://redis:6379"
  script:
    - npm run test:integration
  artifacts:
    reports:
      junit: junit-integration.xml

e2e-test:
  extends: .test-template
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  services:
    - name: $IMAGE_TAG
      alias: app
      variables:
        NODE_ENV: test
  variables:
    BASE_URL: "http://app:3000"
  script:
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - test-results/
      - playwright-report/
    reports:
      junit: junit-e2e.xml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_MERGE_REQUEST_IID
      changes:
        - "**/*.ts"
        - "**/*.tsx"

lint:
  stage: test
  needs:
    - build
  script:
    - npm run lint
    - npm run format:check
  allow_failure: false

# ============================================
# SECURITY STAGE
# ============================================

sast:
  stage: security
  needs: []

dependency-scan:
  stage: security
  needs: []

container-scan:
  stage: security
  needs:
    - docker-build
  variables:
    GIT_STRATEGY: fetch
    CI_APPLICATION_REPOSITORY: $CI_REGISTRY_IMAGE
    CI_APPLICATION_TAG: $CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

secret-detection:
  stage: security
  needs: []

license-scan:
  stage: security
  needs:
    - build
  script:
    - npm audit --audit-level=high
    - npx license-checker --production --failOn "GPL;AGPL"
  allow_failure: true

trivy-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  needs:
    - docker-build
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ============================================
# DEPLOY STAGE
# ============================================

.deploy-template:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  needs:
    - docker-build
    - unit-test
    - integration-test
    - trivy-scan
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority="$KUBE_CA_PEM_FILE"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab --namespace=$KUBE_NAMESPACE
    - kubectl config use-context default

deploy-staging:
  extends: .deploy-template
  variables:
    KUBE_URL: $STAGING_KUBE_URL
    KUBE_TOKEN: $STAGING_KUBE_TOKEN
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging
  script:
    - |
      kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
      kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=5m
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stop-staging:
  extends: .deploy-template
  variables:
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    action: stop
  script:
    - kubectl scale deployment/app --replicas=0 -n $KUBE_NAMESPACE
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  extends: .deploy-template
  variables:
    KUBE_URL: $PROD_KUBE_URL
    KUBE_TOKEN: $PROD_KUBE_TOKEN
    KUBE_NAMESPACE: production
  environment:
    name: production
    url: https://example.com
  script:
    - |
      # Canary deployment
      kubectl set image deployment/app-canary app=$IMAGE_TAG -n $KUBE_NAMESPACE
      kubectl rollout status deployment/app-canary -n $KUBE_NAMESPACE --timeout=5m

      # Wait for canary validation
      sleep 300

      # Full rollout
      kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
      kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=10m
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_TAG

# Review apps for merge requests
review-app:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  needs:
    - docker-build
    - unit-test
  variables:
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://$CI_MERGE_REQUEST_IID.review.example.com
    on_stop: stop-review
    auto_stop_in: 1 week
  script:
    - kubectl create namespace $REVIEW_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    - |
      cat <<EOF | kubectl apply -f -
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: app
        namespace: $REVIEW_NAMESPACE
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: review-$CI_MERGE_REQUEST_IID
        template:
          metadata:
            labels:
              app: review-$CI_MERGE_REQUEST_IID
          spec:
            containers:
            - name: app
              image: $IMAGE_TAG
              ports:
              - containerPort: 3000
      EOF
  rules:
    - if: $CI_MERGE_REQUEST_IID

stop-review:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  variables:
    GIT_STRATEGY: none
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  script:
    - kubectl delete namespace $REVIEW_NAMESPACE --ignore-not-found
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID

# ============================================
# CLEANUP STAGE
# ============================================

cleanup-registry:
  stage: cleanup
  image: alpine:latest
  script:
    - apk add --no-cache curl jq
    - |
      # Keep last 10 images, delete older
      TAGS=$(curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories" | jq -r '.[0].id')
      curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$TAGS/tags?per_page=100" | \
        jq -r '.[10:] | .[].name' | \
        xargs -I {} curl -X DELETE -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$TAGS/tags/{}"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual

# ============================================
# INCLUDES
# ============================================

include:
  # GitLab templates
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

  # Local includes
  - local: .gitlab/ci/notifications.yml

  # Remote includes
  - remote: https://example.com/shared-ci/release.yml
```

### Parent-Child Pipeline

```yaml
# .gitlab-ci.yml (parent)
stages:
  - trigger

trigger-microservices:
  stage: trigger
  trigger:
    include:
      - local: services/api/.gitlab-ci.yml
        rules:
          - changes:
              - services/api/**/*
      - local: services/web/.gitlab-ci.yml
        rules:
          - changes:
              - services/web/**/*
      - local: services/worker/.gitlab-ci.yml
        rules:
          - changes:
              - services/worker/**/*
    strategy: depend
```

### Dynamic Child Pipeline

```yaml
# Generate pipeline dynamically
generate-pipeline:
  stage: build
  script:
    - |
      cat > generated-pipeline.yml << EOF
      stages:
        - deploy

      $(for service in $(find services -maxdepth 1 -type d -name "*"); do
        name=$(basename $service)
        echo "deploy-$name:"
        echo "  stage: deploy"
        echo "  script:"
        echo "    - echo Deploying $name"
      done)
      EOF
  artifacts:
    paths:
      - generated-pipeline.yml

trigger-generated:
  stage: deploy
  needs:
    - generate-pipeline
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

### Multi-Project Pipeline

```yaml
# Trigger downstream project
trigger-deploy:
  stage: deploy
  variables:
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  trigger:
    project: devops/kubernetes-deployments
    branch: main
    strategy: depend
```

### Rules and Conditions

```yaml
# Complex rules examples
job-with-rules:
  script: echo "Running"
  rules:
    # Run on default branch
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      variables:
        DEPLOY_ENV: production

    # Run on merge requests to main
    - if: $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"
      variables:
        DEPLOY_ENV: staging

    # Run on tags
    - if: $CI_COMMIT_TAG
      variables:
        DEPLOY_ENV: release

    # Run on schedule
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        DEPLOY_ENV: nightly

    # Run when specific files change
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.py"
        - requirements*.txt
      variables:
        DEPLOY_ENV: test

    # Manual trigger
    - if: $CI_PIPELINE_SOURCE == "web"
      when: manual

    # Never run
    - when: never
```

### Environments with Auto DevOps

```yaml
# Using Auto DevOps features
include:
  - template: Auto-DevOps.gitlab-ci.yml

variables:
  AUTO_DEVOPS_PLATFORM_TARGET: EKS
  KUBE_INGRESS_BASE_DOMAIN: example.com
  POSTGRES_ENABLED: "true"
  STAGING_ENABLED: "true"
  CANARY_ENABLED: "true"
  INCREMENTAL_ROLLOUT_MODE: manual
```

## Best Practices

1. **Use stages effectively** - Group related jobs, parallel where possible
2. **Cache dependencies** - Reduce build times with proper caching
3. **Use artifacts wisely** - Pass only necessary files between jobs
4. **Implement rules** - Control when jobs run with rules syntax
5. **Use templates** - DRY with extends and include
6. **Secure variables** - Use protected/masked variables for secrets
7. **Define environments** - Track deployments with environment URLs
8. **Use needs keyword** - Create DAG for faster pipelines
9. **Implement review apps** - Preview changes in merge requests
10. **Clean up resources** - Auto-stop environments, prune registry

## Common Pitfalls

1. **Sequential stages** - Not using `needs` creates unnecessary waiting. Use DAG for parallelism.

2. **Large artifacts** - Passing entire node_modules slows pipelines. Cache instead.

3. **Missing rules** - Jobs run unexpectedly. Use workflow rules and job rules.

4. **Unprotected variables** - Secrets exposed in logs. Mark as protected and masked.

5. **No retry policy** - Flaky tests fail pipelines. Add retry with appropriate conditions.

6. **Orphaned environments** - Review apps not cleaned up. Use auto_stop_in.

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [.gitlab-ci.yml Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [GitLab Runner](https://docs.gitlab.com/runner/)
