---
name: terraform-modules
title: ASU Terraform Modules
description: Custom Terraform modules from dco-terraform hosted on JFrog Artifactory
subtypes:
  - compute
  - database
  - networking
  - kubernetes
  - cloudflare
  - iam
  - observability
  - tags
---

# ASU Terraform Modules

Custom Terraform modules from dco-terraform hosted on JFrog Artifactory.
These are ASU-specific modules with built-in tagging standards, security
configurations, and Ansible integration.

## Registry

```
jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform
```

## Module Source Pattern

```hcl
module "example" {
  source  = "jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform/<module>/aws"
  version = ">= 1.0"
}
```

## Requirements

| Requirement | Version |
|-------------|---------|
| Terraform | >= 1.5.6 |
| AWS Provider | >= 5.82.0 |

## Compute

| Module | Description |
|--------|-------------|
| ec2-instance | Linux EC2 with Ansible integration |
| ec2-instance-linux-lowlevel | Low-level Linux EC2 configuration |
| ec2-windows | Windows EC2 instances |
| ec2-windows-v2 | Windows EC2 v2 |
| ec2-macos-instance | macOS EC2 instances |
| ec2-public-instance | Public-facing EC2 instances |
| nutanix-vm | Nutanix virtual machines |

## Database

| Module | Description |
|--------|-------------|
| aurora | Aurora clusters |
| aurora-mysql | Aurora MySQL |
| aurora-postgres | Aurora PostgreSQL |
| rds-mssql | RDS SQL Server |
| rds-oracle | RDS Oracle |

## Networking

| Module | Description |
|--------|-------------|
| vpc-core-v3 | VPC with subnets, NAT, VPN (v3) |
| vpc-core-v5 | VPC with subnets, NAT, VPN, Route53 (v5) |
| security-group | Security groups |
| core-security-groups | Standard org-wide security groups |
| route53-host | Route53 DNS records |
| route53-private-zone | Private hosted zones |
| route53-public-zone | Public hosted zones |

## Kubernetes

| Module | Description |
|--------|-------------|
| eks-oidc-provider | EKS OIDC identity provider |
| eks-pod-identity-role | EKS pod identity IAM roles |
| eks-service-account-role | IRSA (IAM Roles for Service Accounts) |
| vault-kubernetes-auth-role | Vault K8s authentication |

## Cloudflare

| Module | Description |
|--------|-------------|
| cloudflare-tunnel | Cloudflare Tunnel setup |
| cloudflare-tunnel-route53-dns | Tunnel with Route53 DNS |
| cloudflare-access-app | Cloudflare Access applications |
| cloudflare-access-edna-group | EDNA-integrated access groups |
| cloudflare-origin-ca-certificate | Origin CA certificates |
| cloudflare-zone-logpush-logging-lake | Zone logs to data lake |
| cloudflare-zero-trust-device-posture-rules | ZT posture rules |
| cloudflare-zero-trust-edna-list | Zero Trust EDNA lists |

## IAM

| Module | Description |
|--------|-------------|
| iam-role-github-actions | GitHub Actions OIDC federation |
| iam-role-datadog | Datadog integration role |
| iam-role-vault | HashiCorp Vault role |
| iam-role-packer | Packer image building |
| iam-role-servicenow | ServiceNow integrations |
| iam-role-prismacloud | Prisma Cloud security |
| iam-role-splunk | Splunk logging |
| iam-saml-adfs | SAML ADFS federation |
| iam-shibboleth | Shibboleth federation |
| github-oidc-provider | GitHub OIDC provider setup |
| aws-identity-center-permission-set | AWS SSO permission sets |

## Observability

| Module | Description |
|--------|-------------|
| cloudwatch-logs-to-datadog | CloudWatch to Datadog |
| cloudwatch-logs-to-log-lake | CloudWatch to S3 data lake |
| cloudwatch-to-splunk | CloudWatch to Splunk |
| datadog-lambda-forwarder | Datadog Lambda forwarder |
| datadog-logs-firehose-forwarder | Datadog Kinesis Firehose |
| datadog-mule-monitors | MuleSoft Datadog monitors |
| amazon-inspector | AWS Inspector config |

## Tags

**IMPORTANT: product-tags is MANDATORY for all resources**

| Module | Description |
|--------|-------------|
| product-tags | ASU standard tagging (REQUIRED) |
| generate-tags | Tag generation utilities |
| product-map | Product key to metadata mapping |

### Required Tags
- ProductCategory, ProductFamily, ProductFamilyKey
- Product, ProductKey
- TechContact, AdminContact (ASURITE IDs)
- env (infradev, sandbox, dev, qa, uat, test, scan, non-prod, prod)

Tagging Standard Version: 2025.0.2

## Custom Providers

| Provider | Description |
|----------|-------------|
| terraform-provider-edna | EDNA resource management |
| terraform-provider-mandiantasm | Security scanning |

## Related Commands

```bash
discover.sh pattern --name terraform-modules --type compute
discover.sh pattern --name terraform-modules --type database
discover.sh pattern --name terraform-modules --type kubernetes
discover.sh pattern --name terraform-modules --type tags
discover.sh repos --domain terraform
```
