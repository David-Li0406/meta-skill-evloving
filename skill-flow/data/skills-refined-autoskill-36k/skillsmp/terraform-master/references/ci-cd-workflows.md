# CI/CD Workflows Reference

## GitHub Actions

### Complete Terraform Workflow

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - 'terraform/**'
      - '.github/workflows/terraform.yml'

permissions:
  contents: read
  pull-requests: write
  id-token: write  # For OIDC authentication

env:
  TF_VERSION: "1.9.0"
  TF_WORKING_DIR: "terraform/environments/prod"

jobs:
  validate:
    name: Validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Format Check
        run: terraform fmt -check -recursive
        working-directory: terraform/

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Terraform Validate
        run: terraform validate
        working-directory: ${{ env.TF_WORKING_DIR }}

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: 'terraform/'
          exit-code: '1'
          severity: 'HIGH,CRITICAL'

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform/
          quiet: true
          soft_fail: false
          skip_check: CKV_AWS_123,CKV_AWS_456

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: [validate]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Terraform Init
        run: terraform init -backend=false
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Terraform Test
        run: terraform test -json | tee test-results.json
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: terraform-test-results
          path: ${{ env.TF_WORKING_DIR }}/test-results.json

  plan:
    name: Plan
    runs-on: ubuntu-latest
    needs: [validate, security, test]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -no-color -out=tfplan 2>&1 | tee plan-output.txt
          echo "plan_exit_code=${PIPESTATUS[0]}" >> $GITHUB_OUTPUT
        working-directory: ${{ env.TF_WORKING_DIR }}
        continue-on-error: true

      - name: Comment Plan on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.TF_WORKING_DIR }}/plan-output.txt', 'utf8');
            const truncated = plan.length > 65000 
              ? plan.substring(0, 65000) + '\n\n... (truncated)'
              : plan;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Terraform Plan
            
            \`\`\`
            ${truncated}
            \`\`\`
            `
            });

      - name: Upload Plan
        uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: ${{ env.TF_WORKING_DIR }}/tfplan

  apply:
    name: Apply
    runs-on: ubuntu-latest
    needs: [plan]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Terraform Apply
        run: terraform apply -auto-approve
        working-directory: ${{ env.TF_WORKING_DIR }}
```

### PR Workflow with Cost Estimation

```yaml
# .github/workflows/terraform-pr.yml
name: Terraform PR

on:
  pull_request:
    paths: ['terraform/**']

jobs:
  infracost:
    name: Cost Estimation
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate Infracost JSON
        run: |
          infracost breakdown \
            --path=terraform/environments/prod \
            --format=json \
            --out-file=/tmp/infracost.json

      - name: Post Infracost comment
        run: |
          infracost comment github \
            --path=/tmp/infracost.json \
            --repo=$GITHUB_REPOSITORY \
            --github-token=${{ github.token }} \
            --pull-request=${{ github.event.pull_request.number }} \
            --behavior=update
```

---

## GitLab CI

### Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - security
  - test
  - plan
  - apply

variables:
  TF_VERSION: "1.9.0"
  TF_ROOT: "${CI_PROJECT_DIR}/terraform/environments/prod"
  TF_STATE_NAME: default

image:
  name: hashicorp/terraform:${TF_VERSION}
  entrypoint: [""]

cache:
  key: "${TF_ROOT}"
  paths:
    - ${TF_ROOT}/.terraform/

.terraform-init: &terraform-init
  before_script:
    - cd ${TF_ROOT}
    - terraform init
      -backend-config="address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}"
      -backend-config="lock_address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}/lock"
      -backend-config="unlock_address=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}/lock"
      -backend-config="username=gitlab-ci-token"
      -backend-config="password=${CI_JOB_TOKEN}"
      -backend-config="lock_method=POST"
      -backend-config="unlock_method=DELETE"
      -backend-config="retry_wait_min=5"

fmt:
  stage: validate
  script:
    - terraform fmt -check -recursive -diff
  allow_failure: false

validate:
  stage: validate
  <<: *terraform-init
  script:
    - terraform validate

trivy:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy config --exit-code 1 --severity HIGH,CRITICAL ${TF_ROOT}
  allow_failure: false

checkov:
  stage: security
  image:
    name: bridgecrew/checkov:latest
    entrypoint: [""]
  script:
    - checkov -d ${TF_ROOT} --quiet
  allow_failure: true

test:
  stage: test
  <<: *terraform-init
  script:
    - terraform test
  artifacts:
    reports:
      junit: ${TF_ROOT}/test-results.xml

plan:
  stage: plan
  <<: *terraform-init
  script:
    - terraform plan -out=tfplan
    - terraform show -no-color tfplan > plan.txt
  artifacts:
    name: plan
    paths:
      - ${TF_ROOT}/tfplan
      - ${TF_ROOT}/plan.txt
    reports:
      terraform: ${TF_ROOT}/tfplan
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'

apply:
  stage: apply
  <<: *terraform-init
  script:
    - terraform apply -auto-approve tfplan
  dependencies:
    - plan
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
  environment:
    name: production
```

---

## Cost Optimization

### Infracost Configuration

```yaml
# infracost.yml
version: 0.1

projects:
  - path: terraform/environments/dev
    name: Development
    terraform_var_files:
      - dev.tfvars

  - path: terraform/environments/staging
    name: Staging
    terraform_var_files:
      - staging.tfvars

  - path: terraform/environments/prod
    name: Production
    terraform_var_files:
      - prod.tfvars
```

### Cost Policy

```rego
# policy.rego
package infracost

deny[msg] {
  maxDiff := 100.0
  msg := sprintf(
    "Total monthly cost diff must be less than $%.2f (current diff is $%.2f)",
    [maxDiff, to_number(input.diffTotalMonthlyCost)]
  )
  to_number(input.diffTotalMonthlyCost) > maxDiff
}

deny[msg] {
  r := input.projects[_].breakdown.resources[_]
  r.name == "aws_instance.expensive"
  monthlyCost := to_number(r.monthlyCost)
  maxCost := 500.0
  msg := sprintf(
    "Instance %s monthly cost ($%.2f) exceeds limit ($%.2f)",
    [r.name, monthlyCost, maxCost]
  )
  monthlyCost > maxCost
}
```

---

## Pre-commit Hooks

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.0
    hooks:
      # Formatting
      - id: terraform_fmt
      
      # Validation
      - id: terraform_validate
        args:
          - --hook-config=--retry-once-with-cleanup=true
      
      # Linting
      - id: terraform_tflint
        args:
          - --args=--config=__GIT_WORKING_DIR__/.tflint.hcl
          - --args=--enable-plugin=aws
      
      # Security
      - id: terraform_trivy
        args:
          - --args=--severity=HIGH,CRITICAL
      
      - id: terraform_checkov
        args:
          - --args=--quiet
          - --args=--compact
      
      # Documentation
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
          - --hook-config=--add-to-existing-file=true
          - --args=--config=.terraform-docs.yml

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

### TFLint Configuration

```hcl
# .tflint.hcl
config {
  format = "compact"
  module = true
}

plugin "aws" {
  enabled = true
  version = "0.30.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

rule "aws_instance_invalid_type" {
  enabled = true
}

rule "aws_instance_previous_type" {
  enabled = true
}
```

---

## Workspace Management

### Environment-Based Workspaces

```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Select workspace
terraform workspace select prod

# Apply with workspace-specific vars
terraform apply -var-file="${TF_WORKSPACE}.tfvars"
```

### Workspace in CI

```yaml
# GitHub Actions
- name: Select Workspace
  run: |
    terraform workspace select ${{ github.event.inputs.environment }} || \
    terraform workspace new ${{ github.event.inputs.environment }}

- name: Apply
  run: terraform apply -var-file="${{ github.event.inputs.environment }}.tfvars" -auto-approve
```

---

## Atlantis Configuration

```yaml
# atlantis.yaml
version: 3
automerge: true
parallel_plan: true
parallel_apply: true

projects:
  - name: production
    dir: terraform/environments/prod
    workspace: default
    terraform_version: v1.9.0
    autoplan:
      when_modified: ["*.tf", "../modules/**/*.tf"]
      enabled: true
    apply_requirements: [approved, mergeable]
    workflow: production

workflows:
  production:
    plan:
      steps:
        - init
        - run: terraform validate
        - run: trivy config --exit-code 1 .
        - plan:
            extra_args: ["-var-file=prod.tfvars"]
    apply:
      steps:
        - apply
```
