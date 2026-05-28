---
name: tf.gen_module_stack
description: Generate a greenfield, modular Terraform stack using the DuploCloud Terraform Provider (path-agnostic, spec-driven, validates cleanly)
---

# tf.gen_module_stack — Greenfield Modular Terraform Generator (DuploCloud Provider)

You are an **Operator DevOps agent** that generates a **new** modular Terraform stack from a YAML spec using the **DuploCloud Terraform Provider** (`duplocloud/duplocloud`).

This skill is **path-agnostic**: it must work in any repo layout without requiring `aiops.config.yaml`.

## Provider authentication (mandatory)

- Provider credentials MUST be supplied via environment variables:
  - `DUPLO_HOST`
  - `DUPLO_TOKEN`
- Never write credentials into `.tf` files or commit them.

Provider supports env var configuration for host/token.  [oai_citation:1‡Terraform Registry](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs?utm_source=chatgpt.com)

---

## Non-negotiable safety rules

- Never execute: `terraform apply`, `terraform import`, or any `terraform state *` commands.
- Never hardcode secrets, tokens, passwords, or backend credentials in generated code.
- Always run, in this order (where feasible):
  - `terraform fmt -recursive`
  - `terraform init -backend=false`
  - `terraform validate`
- Run `terraform plan -refresh=false -lock=false` only if credentials allow and validation succeeded; otherwise skip and report why.
- If *any* plan indicates deletes or replacements for an existing stack, STOP and report (greenfield should not do that).

---

## Inputs supplied when invoking this skill

- `ENV`: Target environment name (e.g., `dev`, `stage`, `prod`)
- `SPEC`: Path to a YAML requirements spec file in the repository

---

## Output layout (path-agnostic)

Generate into the first matching option below; if none exist, create option (1):

1. `terraform/`
   - `terraform/modules/<stack_name>/...`
   - `terraform/envs/<ENV>/main.tf`
2. `infra/terraform/`
3. `iac/terraform/`

If multiple exist, pick the one that already contains a `versions.tf` or `providers.tf`; otherwise choose the shortest path.

Within the chosen `TF_ROOT`, always create:
- `modules/<stack_name>/` (module(s))
- `envs/<ENV>/` (environment composition root)

---

## Supported Duplo resources (verified schema)

To guarantee `terraform validate` passes, only generate “real” resource blocks for components whose required args we can verify from accessible docs/snippets:

### 1) Infrastructure
Resource: `duplocloud_infrastructure`

Example shows the key required fields used in practice: `infra_name`, `region`, `enable_k8_cluster`, `address_prefix`, and optionally `cloud`, `azcount`, `subnet_cidr`.  [oai_citation:2‡Terraform Registry](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/infrastructure?utm_source=chatgpt.com)

### 2) Tenant
Resource: `duplocloud_tenant`

Example shows `account_name` and `plan_id` (often set to the infrastructure name).  [oai_citation:3‡Terraform Registry](https://registry.terraform.io/providers/duplocloud/duplocloud/0.11.30/docs/resources/tenant?utm_source=chatgpt.com)

### 3) S3 bucket
Resource: `duplocloud_s3_bucket`

Schema snippet confirms required: `name`, `tenant_id`; optional includes `allow_public_access`, `enable_versioning`, and encryption blocks.  [oai_citation:4‡Terraform Registry](https://registry.terraform.io/providers/duplocloud/duplocloud/latest/docs/resources/s3_bucket?utm_source=chatgpt.com)

### 4) Tenant network security rule
Resource: `duplocloud_tenant_network_security_rule`

Schema snippet confirms required: `description`, `tenant_id` (with optional `from_port`, `protocol`, `source_address` / `source_tenant`, etc.).  [oai_citation:5‡Terraform Registry](https://registry.terraform.io/providers/duplocloud/duplocloud/0.11.32/docs/resources/tenant_network_security_rule?utm_source=chatgpt.com)

---

## Components that are intentionally skipped (until you supply mappings)

Some Duplo resources (notably **Duplo services** and **RDS**) have Terraform Registry docs that are **JavaScript-gated** here, so their “required arguments” cannot be verified reliably in this environment.

Therefore:
- If the spec requests these components, DO NOT emit resource blocks.
- Instead, write a `README.md` in the stack module explaining what was requested and what exact mappings are needed to enable codegen later.

This is not negotiable: do not guess required fields.

---

## Spec Input Format (YAML)

The spec MUST match this schema. Fields marked “optional” may be omitted.

```yaml
stack_name: <string>
name_prefix: <string>   # e.g. "acme-dev"
tags:                   # optional
  <key>: <value>

provider:               # optional
  duplocloud:
    tenant_name: <string|null>   # optional hint only
    tenant_id: <string|null>     # optional if you want to reference existing tenant
    create_tenant: <bool>        # default false
    plan_id: <string|null>       # usually infra_name, see examples

components:
  infrastructure:               # optional
    enabled: <bool>             # default false
    infra_name: <string>        # required if enabled
    region: <string>            # required if enabled
    cloud: <int|null>           # optional (0=AWS default)
    enable_k8_cluster: <bool>   # required if enabled
    address_prefix: <string>    # required if enabled (CIDR, e.g. "10.20.0.0/16")
    azcount: <int|null>         # optional
    subnet_cidr: <int|null>     # optional

  tenant:                       # optional
    enabled: <bool>             # default false
    account_name: <string>      # required if enabled
    plan_id: <string|null>      # required if enabled; if null and infrastructure enabled, use infra_name

  s3_buckets:                   # optional
    - name: <string>            # short name; Duplo adds prefix/suffix
      enable_versioning: <bool|null>
      allow_public_access: <bool|null>
      # encryption is optional; if set to "sse-s3" emit the provider’s default encryption block if supported;
      # if set to "sse-kms" you must also provide kms_key_arn (or skip and document)
      encryption: sse-s3|sse-kms|null
      kms_key_arn: <string|null>

  tenant_network_security_rules:  # optional
    - description: <string>
      protocol: tcp|udp|icmp|null
      from_port: <int|null>
      to_port: <int|null>
      source_address: <string|null>  # CIDR
      source_tenant: <string|null>   # tenant name (not GUID)

  # Requested but currently skipped:
  duplo_services: []            # skipped (see above)
  rds_instances: []             # skipped (see above)