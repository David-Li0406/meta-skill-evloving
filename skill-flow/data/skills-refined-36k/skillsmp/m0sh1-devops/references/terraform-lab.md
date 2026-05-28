# Terraform Lab Workflow (m0sh1.cc)

## Table of Contents

1. Location and Scope
2. Standard Workflow
3. Module Rules
4. Provider Rules

## 1. Location and Scope

- Active env: `terraform/envs/lab`
- No environment proliferation beyond `lab`.

## 2. Standard Workflow

```bash
export $(cat terraform/op.env | xargs)
terraform -chdir=terraform fmt -recursive
terraform -chdir=terraform/envs/lab init -backend=false
terraform -chdir=terraform/envs/lab validate
terraform -chdir=terraform/envs/lab plan \
  -var-file=defaults.auto.tfvars \
  -var-file=secrets.auto.tfvars
```

## 3. Module Rules

- Use `terraform/modules/**` for reusable modules.
- Keep env-specific values in auto tfvars, not in modules.

## 4. Provider Rules

- Providers and backends defined in `terraform/envs/lab` only.
- Use `versions.tf` and `providers.tf` in that directory.
