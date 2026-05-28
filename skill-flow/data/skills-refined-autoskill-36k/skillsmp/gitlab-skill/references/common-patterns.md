# Common GitLab CI/CD Patterns

Collection of reusable GitLab CI/CD pipeline patterns and configuration examples.

## Table of Contents

- [Python Projects](#python-projects)
- [Node.js Projects](#nodejs-projects)
- [Docker Build and Push](#docker-build-and-push)
- [Multi-Environment Deployment](#multi-environment-deployment)
- [Monorepo Patterns](#monorepo-patterns)
- [Release Management](#release-management)
- [Security Scanning](#security-scanning)
- [Performance Testing](#performance-testing)

## Python Projects

### Basic Python Pipeline with uv

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"

stages:
  - lint
  - test
  - build
  - deploy

cache:
  key:
    files:
      - pyproject.toml
      - uv.lock
  paths:
    - .cache/pip
    - .cache/uv
    - .venv/

.python_base:
  image: python:3.12-slim
  before_script:
    - pip install uv
    - uv venv
    - uv sync --frozen

lint:ruff:
  extends: .python_base
  stage: lint
  script:
    - uv run ruff check

lint:mypy:
  extends: .python_base
  stage: lint
  script:
    - uv run mypy .

test:
  extends: .python_base
  stage: test
  script:
    - uv run pytest --cov --cov-report=html --cov-report=xml
  artifacts:
    paths:
      - htmlcov/
      - coverage.xml
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  coverage: '/(?i)total.*? (100(?:\.0+)?|[1-9]?\d(?:\.\d+)?)%/'

build:
  extends: .python_base
  stage: build
  script:
    - uv build
  artifacts:
    paths:
      - dist/

deploy:pypi:
  stage: deploy
  needs: [build]
  script:
    - uv publish --token $PYPI_TOKEN
  rules:
    - if: $CI_COMMIT_TAG
```

### Python Matrix Testing

Test across multiple Python versions:

```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.11", "3.12", "3.13"]
  image: python:${PYTHON_VERSION}-slim
  script:
    - pip install uv
    - uv venv
    - uv sync --frozen
    - uv run pytest
```

## Node.js Projects

### Basic Node.js Pipeline

```yaml
variables:
  NPM_CONFIG_CACHE: "$CI_PROJECT_DIR/.npm"

stages:
  - install
  - lint
  - test
  - build
  - deploy

cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/

install:
  stage: install
  script:
    - npm ci --cache .npm --prefer-offline
  cache:
    policy: pull-push

lint:
  stage: lint
  script:
    - npm run lint
  cache:
    policy: pull

test:
  stage: test
  script:
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  script:
    - npm publish
  rules:
    - if: $CI_COMMIT_TAG
```

## Docker Build and Push

### Basic Docker Build

```yaml
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
```

### Multi-Architecture Docker Build

```yaml
build:docker:multiarch:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    - docker buildx create --use
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        --tag $CI_REGISTRY_IMAGE:latest \
        --push \
        .
```

### Docker Build with Kaniko

Kaniko builds without Docker-in-Docker:

```yaml
build:kaniko:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:debug
    entrypoint: [""]
  script:
    - mkdir -p /kaniko/.docker
    - echo "{\"auths\":{\"$CI_REGISTRY\":{\"auth\":\"$(echo -n $CI_REGISTRY_USER:$CI_REGISTRY_PASSWORD | base64)\"}}}" > /kaniko/.docker/config.json
    - |
      /kaniko/executor \
        --context $CI_PROJECT_DIR \
        --dockerfile $CI_PROJECT_DIR/Dockerfile \
        --destination $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        --destination $CI_REGISTRY_IMAGE:latest
```

## Multi-Environment Deployment

### Deploy to Multiple Environments

```yaml
stages:
  - build
  - deploy:dev
  - deploy:staging
  - deploy:production

.deploy_base:
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - curl -X POST $WEBHOOK_URL -H "Authorization: Bearer $DEPLOY_TOKEN"

deploy:dev:
  extends: .deploy_base
  stage: deploy:dev
  environment:
    name: development
    url: https://dev.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy:staging:
  extends: .deploy_base
  stage: deploy:staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:production:
  extends: .deploy_base
  stage: deploy:production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG
  when: manual
```

### Environment-Specific Variables

```yaml
.deploy_base:
  script:
    - deploy.sh $ENVIRONMENT

deploy:dev:
  extends: .deploy_base
  variables:
    ENVIRONMENT: development
    API_URL: https://api-dev.example.com

deploy:staging:
  extends: .deploy_base
  variables:
    ENVIRONMENT: staging
    API_URL: https://api-staging.example.com

deploy:production:
  extends: .deploy_base
  variables:
    ENVIRONMENT: production
    API_URL: https://api.example.com
```

## Monorepo Patterns

### Selective Job Execution

Run jobs only when relevant files change:

```yaml
build:frontend:
  script:
    - cd frontend && npm run build
  rules:
    - changes:
        - frontend/**/*
        - package.json

build:backend:
  script:
    - cd backend && uv run build
  rules:
    - changes:
        - backend/**/*
        - pyproject.toml

build:shared:
  script:
    - cd shared && npm run build
  rules:
    - changes:
        - shared/**/*
```

### Child Pipelines

Trigger separate pipelines for each component:

```yaml
trigger:frontend:
  stage: trigger
  trigger:
    include: frontend/.gitlab-ci.yml
    strategy: depend
  rules:
    - changes:
        - frontend/**/*

trigger:backend:
  stage: trigger
  trigger:
    include: backend/.gitlab-ci.yml
    strategy: depend
  rules:
    - changes:
        - backend/**/*
```

## Release Management

### Semantic Versioning Release

```yaml
release:
  stage: deploy
  image: node:latest
  before_script:
    - npm install -g semantic-release @semantic-release/gitlab
  script:
    - semantic-release
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### GitLab Release with glab

```yaml
variables:
  GITLAB_HOST: $CI_SERVER_HOST

release:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache curl bash
    - curl -sSL https://gitlab.com/gitlab-org/cli/-/releases/permalink/latest/downloads/glab_Linux_x86_64.tar.gz | tar -xz -C /usr/local/bin
  script:
    - |
      glab release create $CI_COMMIT_TAG \
        --notes "Release $CI_COMMIT_TAG" \
        --assets-links "[{\"name\":\"Package\",\"url\":\"$CI_PROJECT_URL/-/packages\"}]"
  rules:
    - if: $CI_COMMIT_TAG
```

### Changelog Generation

```yaml
changelog:
  stage: deploy
  image: node:latest
  script:
    - npx conventional-changelog-cli -p angular -i CHANGELOG.md -s
    - git add CHANGELOG.md
    - git commit -m "chore: update changelog [skip ci]"
    - git push origin HEAD:$CI_COMMIT_REF_NAME
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Security Scanning

### SAST (Static Application Security Testing)

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml

sast:
  stage: test
  variables:
    SAST_EXCLUDED_PATHS: "spec, test, tests, tmp"
```

### Dependency Scanning

```yaml
include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

dependency_scanning:
  stage: test
```

### Secret Detection

```yaml
include:
  - template: Security/Secret-Detection.gitlab-ci.yml

secret_detection:
  stage: test
```

### Container Scanning

```yaml
include:
  - template: Security/Container-Scanning.gitlab-ci.yml

container_scanning:
  stage: test
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Performance Testing

### Load Testing with k6

```yaml
load_test:
  stage: test
  image: grafana/k6:latest
  script:
    - k6 run --out json=results.json load-test.js
  artifacts:
    paths:
      - results.json
    reports:
      junit: results.xml
```

### Lighthouse Performance Testing

```yaml
lighthouse:
  stage: test
  image: cypress/browsers:node14.17.0-chrome91-ff89
  script:
    - npm install -g @lhci/cli
    - lhci autorun --config=.lighthouserc.json
  artifacts:
    paths:
      - .lighthouseci/
```

## Reusable Configuration Patterns

### Job Templates

```yaml
.test_template:
  stage: test
  script:
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:unit:
  extends: .test_template
  script:
    - npm run test:unit

test:integration:
  extends: .test_template
  script:
    - npm run test:integration
```

### Include External Configuration

```yaml
include:
  - local: ".gitlab-ci-templates/*.yml"
  - project: "group/ci-templates"
    file: "/templates/python.yml"
    ref: main
  - remote: "https://example.com/ci-template.yml"
```

### Dynamic Child Pipeline

```yaml
generate-pipeline:
  stage: prepare
  script:
    - python generate_pipeline.py > generated-pipeline.yml
  artifacts:
    paths:
      - generated-pipeline.yml

child-pipeline:
  stage: execute
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

## Best Practices

1. **Use templates** - DRY principle with `.template` and `extends`
2. **Cache dependencies** - Speed up pipeline with proper caching
3. **Parallelize jobs** - Run independent jobs concurrently
4. **Use DAG with needs** - Optimize job execution order
5. **Conditional execution** - Use `rules` to run only necessary jobs
6. **Secure secrets** - Use masked and protected variables
7. **Set timeouts** - Prevent hanging jobs
8. **Version control configs** - Track `.gitlab-ci.yml` changes
9. **Monitor performance** - Track pipeline duration and resource usage
10. **Document patterns** - Share common patterns with team
