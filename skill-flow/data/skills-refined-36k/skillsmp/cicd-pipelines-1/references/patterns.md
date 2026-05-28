# CI/CD Pipelines

## Patterns


---
  #### **Name**
GitHub Actions - Basic Workflow
  #### **Description**
Standard CI workflow with caching
  #### **When**
Any Node.js/Python/Go project on GitHub
  #### **Example**
    # GITHUB ACTIONS - BASIC CI:
    
    """
    Fast, reliable CI with:
    1. Caching for dependencies
    2. Parallel test and lint jobs
    3. Matrix for multiple versions
    """
    
    # .github/workflows/ci.yml
    name: CI
    
    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]
    
    jobs:
      lint:
        name: Lint
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
    
          - uses: actions/setup-node@v4
            with:
              node-version: '20'
              cache: 'npm'
    
          - run: npm ci
          - run: npm run lint
          - run: npm run typecheck
    
      test:
        name: Test (Node ${{ matrix.node }})
        runs-on: ubuntu-latest
        strategy:
          matrix:
            node: ['18', '20', '22']
        steps:
          - uses: actions/checkout@v4
    
          - uses: actions/setup-node@v4
            with:
              node-version: ${{ matrix.node }}
              cache: 'npm'
    
          - run: npm ci
          - run: npm test -- --coverage
    
          - uses: codecov/codecov-action@v4
            if: matrix.node == '20'
            with:
              token: ${{ secrets.CODECOV_TOKEN }}
    
      build:
        name: Build
        runs-on: ubuntu-latest
        needs: [lint, test]
        steps:
          - uses: actions/checkout@v4
    
          - uses: actions/setup-node@v4
            with:
              node-version: '20'
              cache: 'npm'
    
          - run: npm ci
          - run: npm run build
    
          - uses: actions/upload-artifact@v4
            with:
              name: build
              path: dist/
              retention-days: 7
    

---
  #### **Name**
GitHub Actions - Docker Build & Push
  #### **Description**
Build and push container images
  #### **When**
Containerized applications
  #### **Example**
    # DOCKER BUILD & PUSH:
    
    """
    Multi-platform builds with:
    1. Layer caching
    2. Registry push
    3. Version tagging
    """
    
    name: Docker
    
    on:
      push:
        branches: [main]
        tags: ['v*']
    
    env:
      REGISTRY: ghcr.io
      IMAGE_NAME: ${{ github.repository }}
    
    jobs:
      build:
        runs-on: ubuntu-latest
        permissions:
          contents: read
          packages: write
    
        steps:
          - uses: actions/checkout@v4
    
          - uses: docker/setup-qemu-action@v3
    
          - uses: docker/setup-buildx-action@v3
    
          - uses: docker/login-action@v3
            with:
              registry: ${{ env.REGISTRY }}
              username: ${{ github.actor }}
              password: ${{ secrets.GITHUB_TOKEN }}
    
          - uses: docker/metadata-action@v5
            id: meta
            with:
              images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
              tags: |
                type=ref,event=branch
                type=semver,pattern={{version}}
                type=semver,pattern={{major}}.{{minor}}
                type=sha,prefix=
    
          - uses: docker/build-push-action@v5
            with:
              context: .
              platforms: linux/amd64,linux/arm64
              push: true
              tags: ${{ steps.meta.outputs.tags }}
              labels: ${{ steps.meta.outputs.labels }}
              cache-from: type=gha
              cache-to: type=gha,mode=max
    

---
  #### **Name**
GitHub Actions - Deploy to Kubernetes
  #### **Description**
GitOps deployment workflow
  #### **When**
Kubernetes deployments
  #### **Example**
    # KUBERNETES DEPLOYMENT:
    
    """
    Deploy with:
    1. Environment protection
    2. Approval gates
    3. Rollback capability
    """
    
    name: Deploy
    
    on:
      push:
        branches: [main]
      workflow_dispatch:
        inputs:
          environment:
            type: choice
            options: [staging, production]
    
    jobs:
      deploy-staging:
        runs-on: ubuntu-latest
        environment: staging
        steps:
          - uses: actions/checkout@v4
    
          - uses: azure/setup-kubectl@v3
    
          - uses: azure/k8s-set-context@v3
            with:
              kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
          - run: |
              kubectl set image deployment/my-app \
                my-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
                -n staging
    
          - run: kubectl rollout status deployment/my-app -n staging
    
      deploy-production:
        runs-on: ubuntu-latest
        needs: [deploy-staging]
        if: github.ref == 'refs/heads/main'
        environment:
          name: production
          url: https://myapp.com
        steps:
          - uses: actions/checkout@v4
    
          - uses: azure/setup-kubectl@v3
    
          - uses: azure/k8s-set-context@v3
            with:
              kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
    
          - run: |
              kubectl set image deployment/my-app \
                my-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
                -n production
    
          - run: kubectl rollout status deployment/my-app -n production
    

---
  #### **Name**
Reusable Workflows
  #### **Description**
DRY CI/CD with shared workflows
  #### **When**
Multiple repositories with similar pipelines
  #### **Example**
    # REUSABLE WORKFLOWS:
    
    """
    Create once, use everywhere.
    Reduces duplication across repos.
    """
    
    # .github/workflows/reusable-node-ci.yml (in shared repo)
    name: Reusable Node CI
    
    on:
      workflow_call:
        inputs:
          node-version:
            type: string
            default: '20'
          working-directory:
            type: string
            default: '.'
        secrets:
          npm-token:
            required: false
    
    jobs:
      ci:
        runs-on: ubuntu-latest
        defaults:
          run:
            working-directory: ${{ inputs.working-directory }}
    
        steps:
          - uses: actions/checkout@v4
    
          - uses: actions/setup-node@v4
            with:
              node-version: ${{ inputs.node-version }}
              cache: 'npm'
              cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json
    
          - run: npm ci
            env:
              NPM_TOKEN: ${{ secrets.npm-token }}
    
          - run: npm run lint
          - run: npm test
          - run: npm run build
    
    
    # Using in another repo:
    # .github/workflows/ci.yml
    name: CI
    on: [push, pull_request]
    
    jobs:
      ci:
        uses: org/shared-workflows/.github/workflows/reusable-node-ci.yml@main
        with:
          node-version: '20'
        secrets:
          npm-token: ${{ secrets.NPM_TOKEN }}
    

---
  #### **Name**
GitLab CI Pipeline
  #### **Description**
GitLab CI/CD configuration
  #### **When**
GitLab repositories
  #### **Example**
    # GITLAB CI:
    
    """
    GitLab CI with:
    1. Stages for organization
    2. Caching
    3. Environments
    """
    
    # .gitlab-ci.yml
    stages:
      - lint
      - test
      - build
      - deploy
    
    variables:
      DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    
    default:
      image: node:20-alpine
      cache:
        key: ${CI_COMMIT_REF_SLUG}
        paths:
          - node_modules/
    
    before_script:
      - npm ci --cache .npm
    
    lint:
      stage: lint
      script:
        - npm run lint
        - npm run typecheck
    
    test:
      stage: test
      script:
        - npm test -- --coverage
      coverage: '/Statements\s*:\s*(\d+\.?\d*)%/'
      artifacts:
        reports:
          coverage_report:
            coverage_format: cobertura
            path: coverage/cobertura-coverage.xml
    
    build:
      stage: build
      image: docker:24
      services:
        - docker:24-dind
      before_script:
        - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
      script:
        - docker build -t $DOCKER_IMAGE .
        - docker push $DOCKER_IMAGE
    
    deploy-staging:
      stage: deploy
      environment:
        name: staging
        url: https://staging.myapp.com
      script:
        - kubectl set image deployment/my-app my-app=$DOCKER_IMAGE -n staging
      only:
        - main
    
    deploy-production:
      stage: deploy
      environment:
        name: production
        url: https://myapp.com
      script:
        - kubectl set image deployment/my-app my-app=$DOCKER_IMAGE -n production
      when: manual
      only:
        - main
    

---
  #### **Name**
Composite Actions
  #### **Description**
Reusable action steps
  #### **When**
Repeated steps across workflows
  #### **Example**
    # COMPOSITE ACTIONS:
    
    """
    Package multiple steps into a single action.
    Better than copy-pasting setup steps.
    """
    
    # .github/actions/setup-node-project/action.yml
    name: Setup Node Project
    description: Install Node.js and dependencies
    
    inputs:
      node-version:
        description: Node.js version
        required: false
        default: '20'
    
    runs:
      using: composite
      steps:
        - uses: actions/setup-node@v4
          with:
            node-version: ${{ inputs.node-version }}
            cache: 'npm'
    
        - run: npm ci
          shell: bash
    
        - run: echo "::notice::Node ${{ inputs.node-version }} ready"
          shell: bash
    
    
    # Usage in workflow:
    - uses: ./.github/actions/setup-node-project
      with:
        node-version: '20'
    

## Anti-Patterns


---
  #### **Name**
No Caching
  #### **Description**
Downloading all dependencies on every run
  #### **Why**
    Builds take forever. You're paying for network bandwidth and compute.
    Developers stop running CI because it's too slow. They merge without
    waiting for checks.
    
  #### **Instead**
    # Cache dependencies
    - uses: actions/setup-node@v4
      with:
        cache: 'npm'
    
    # Or manual cache
    - uses: actions/cache@v4
      with:
        path: ~/.npm
        key: npm-${{ hashFiles('**/package-lock.json') }}
    

---
  #### **Name**
Sequential Everything
  #### **Description**
Running all checks one after another
  #### **Why**
    A 5-minute lint, 10-minute test, and 5-minute build becomes 20 minutes.
    With parallelization, it could be 10 minutes. Developers wait twice as long.
    
  #### **Instead**
    # Parallel jobs
    jobs:
      lint:
        runs-on: ubuntu-latest
        # ...
      test:
        runs-on: ubuntu-latest
        # ...
      build:
        needs: [lint, test]  # Only build waits
    

---
  #### **Name**
Secrets in Logs
  #### **Description**
Printing or exposing secrets
  #### **Why**
    Anyone with read access to the repo can see workflow logs. If secrets
    appear in logs, they're compromised. GitHub masks them, but not always.
    
  #### **Instead**
    # Never echo secrets
    # WRONG:
    - run: echo "Deploying with key ${{ secrets.API_KEY }}"
    
    # RIGHT:
    - run: ./deploy.sh
      env:
        API_KEY: ${{ secrets.API_KEY }}
    
    # Mask manual values
    - run: echo "::add-mask::$MY_SECRET"
    

---
  #### **Name**
No Concurrency Control
  #### **Description**
Multiple deployments running simultaneously
  #### **Why**
    Push twice quickly, get two deployments racing. One might overwrite
    the other. Or deployments run in wrong order.
    
  #### **Instead**
    # Cancel in-progress runs
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true
    
    # Or queue deployments
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    

---
  #### **Name**
Monolithic Workflows
  #### **Description**
One giant workflow file doing everything
  #### **Why**
    Hard to maintain, hard to debug, runs everything on every change.
    Changes to the workflow itself require full CI run to test.
    
  #### **Instead**
    # Split by concern
    .github/workflows/
    ├── ci.yml           # Lint, test, build
    ├── deploy.yml       # Deployment only
    ├── release.yml      # Release process
    └── security.yml     # Security scanning
    