---
id: aws-architecture
name: "AWS Architecture"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# AWS Architecture

## Overview

AWS (Amazon Web Services) provides comprehensive cloud infrastructure services. This methodology covers architectural patterns, service selection, and best practices for building production-grade applications on AWS following the Well-Architected Framework.

## When to Use

- Building new cloud-native applications
- Migrating on-premises workloads to cloud
- Designing scalable microservices architectures
- Implementing disaster recovery solutions
- Optimizing existing AWS infrastructure

## Key Concepts

### AWS Well-Architected Pillars

| Pillar | Focus Areas |
|--------|-------------|
| Operational Excellence | Automation, monitoring, continuous improvement |
| Security | IAM, encryption, network security, compliance |
| Reliability | Fault tolerance, recovery, scaling |
| Performance Efficiency | Right-sizing, caching, serverless |
| Cost Optimization | Reserved capacity, spot instances, rightsizing |
| Sustainability | Resource efficiency, managed services |

### Core Services

| Category | Services |
|----------|----------|
| Compute | EC2, ECS, EKS, Lambda, Fargate |
| Storage | S3, EBS, EFS, FSx |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Networking | VPC, ALB/NLB, CloudFront, Route 53 |
| Security | IAM, KMS, Secrets Manager, WAF |
| Monitoring | CloudWatch, X-Ray, CloudTrail |

## Implementation

### VPC Architecture

```hcl
# Three-tier VPC architecture
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  one_nat_gateway_per_az = var.environment == "prod"

  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
  flow_log_max_aggregation_interval    = 60

  # Tags for Kubernetes
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}
```

### EKS Cluster

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Encryption
  cluster_encryption_config = {
    provider_key_arn = aws_kms_key.eks.arn
    resources        = ["secrets"]
  }

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      name           = "general"
      instance_types = ["t3.medium"]

      min_size     = 2
      max_size     = 10
      desired_size = 3

      disk_size = 50

      labels = {
        workload = "general"
      }
    }

    spot = {
      name           = "spot"
      instance_types = ["t3.medium", "t3.large", "t3a.medium"]
      capacity_type  = "SPOT"

      min_size     = 0
      max_size     = 10
      desired_size = 2

      labels = {
        workload = "spot"
      }

      taints = [{
        key    = "spot"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # Add-ons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent              = true
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  # IRSA
  enable_irsa = true

  # Cluster access
  manage_aws_auth_configmap = true
  aws_auth_roles = [
    {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Admin"
      username = "admin"
      groups   = ["system:masters"]
    }
  ]
}
```

### RDS Aurora

```hcl
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 8.0"

  name           = "${var.project}-${var.environment}"
  engine         = "aurora-postgresql"
  engine_version = "15.4"
  instance_class = "db.r6g.large"
  instances = {
    1 = {}
    2 = {
      instance_class = "db.r6g.large"
    }
  }

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name
  security_group_rules = {
    vpc_ingress = {
      cidr_blocks = module.vpc.private_subnets_cidr_blocks
    }
  }

  # Encryption
  storage_encrypted   = true
  kms_key_id         = aws_kms_key.rds.arn

  # Backup
  backup_retention_period = var.environment == "prod" ? 30 : 7
  preferred_backup_window = "02:00-04:00"

  # Maintenance
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  auto_minor_version_upgrade   = true

  # High availability
  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  # Performance Insights
  performance_insights_enabled          = true
  performance_insights_retention_period = var.environment == "prod" ? 731 : 7

  # Enhanced monitoring
  monitoring_interval = 60

  # IAM authentication
  iam_database_authentication_enabled = true
}
```

### Application Load Balancer

```hcl
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name    = "${var.project}-${var.environment}"
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  # Security
  security_group_ingress_rules = {
    all_http = {
      from_port   = 80
      to_port     = 80
      ip_protocol = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
    }
    all_https = {
      from_port   = 443
      to_port     = 443
      ip_protocol = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
    }
  }
  security_group_egress_rules = {
    all = {
      ip_protocol = "-1"
      cidr_ipv4   = module.vpc.vpc_cidr_block
    }
  }

  # Access logs
  access_logs = {
    bucket = module.alb_logs.s3_bucket_id
    prefix = "alb"
  }

  listeners = {
    http-redirect = {
      port     = 80
      protocol = "HTTP"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
    https = {
      port            = 443
      protocol        = "HTTPS"
      certificate_arn = module.acm.acm_certificate_arn

      forward = {
        target_group_key = "app"
      }
    }
  }

  target_groups = {
    app = {
      name_prefix          = "app-"
      protocol             = "HTTP"
      port                 = 8000
      target_type          = "ip"
      deregistration_delay = 30

      health_check = {
        enabled             = true
        path                = "/health"
        port                = "traffic-port"
        healthy_threshold   = 2
        unhealthy_threshold = 3
        timeout             = 5
        interval            = 30
        matcher             = "200"
      }
    }
  }
}
```

### S3 with CloudFront

```hcl
# S3 bucket for static assets
module "s3_static" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = "${var.project}-${var.environment}-static"

  # Block public access
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  # Versioning
  versioning = {
    enabled = true
  }

  # Encryption
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  # Lifecycle rules
  lifecycle_rule = [
    {
      id      = "archive"
      enabled = true

      transition = [
        {
          days          = 90
          storage_class = "STANDARD_IA"
        },
        {
          days          = 180
          storage_class = "GLACIER"
        }
      ]

      noncurrent_version_expiration = {
        days = 30
      }
    }
  ]

  # CORS
  cors_rule = [
    {
      allowed_methods = ["GET", "HEAD"]
      allowed_origins = ["https://${var.domain}"]
      allowed_headers = ["*"]
      max_age_seconds = 3600
    }
  ]
}

# CloudFront distribution
module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 3.0"

  aliases = ["static.${var.domain}"]

  comment             = "${var.project} static assets"
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  retain_on_delete    = false
  wait_for_deployment = false

  # Origin Access Control for S3
  create_origin_access_control = true
  origin_access_control = {
    s3_oac = {
      description      = "CloudFront access to S3"
      origin_type      = "s3"
      signing_behavior = "always"
      signing_protocol = "sigv4"
    }
  }

  origin = {
    s3_static = {
      domain_name           = module.s3_static.s3_bucket_bucket_regional_domain_name
      origin_access_control = "s3_oac"
    }
  }

  default_cache_behavior = {
    target_origin_id       = "s3_static"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD"]
    compress        = true

    cache_policy_id          = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
    origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf" # CORS-S3Origin
  }

  viewer_certificate = {
    acm_certificate_arn = module.acm_cloudfront.acm_certificate_arn
    ssl_support_method  = "sni-only"
  }
}
```

### IAM Roles and Policies

```hcl
# EKS Pod Identity (IRSA)
module "app_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "${var.project}-${var.environment}-app"

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["app:app"]
    }
  }

  role_policy_arns = {
    policy = aws_iam_policy.app.arn
  }
}

resource "aws_iam_policy" "app" {
  name = "${var.project}-${var.environment}-app"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          module.s3_static.s3_bucket_arn,
          "${module.s3_static.s3_bucket_arn}/*"
        ]
      },
      {
        Sid    = "SecretsAccess"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/${var.environment}/*"
        ]
      },
      {
        Sid    = "KMSDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = [
          aws_kms_key.secrets.arn
        ]
      }
    ]
  })
}
```

### Monitoring and Alerting

```hcl
# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project}-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "EKS Cluster CPU"
          region = var.region
          metrics = [
            ["ContainerInsights", "pod_cpu_utilization", "ClusterName", module.eks.cluster_name]
          ]
          period = 300
          stat   = "Average"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "RDS Connections"
          region = var.region
          metrics = [
            ["AWS/RDS", "DatabaseConnections", "DBClusterIdentifier", module.aurora.cluster_id]
          ]
          period = 300
          stat   = "Average"
        }
      }
    ]
  })
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${var.project}-${var.environment}-rds-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "RDS CPU utilization high"

  dimensions = {
    DBClusterIdentifier = module.aurora.cluster_id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

# SNS Topic for alerts
resource "aws_sns_topic" "alerts" {
  name = "${var.project}-${var.environment}-alerts"

  kms_master_key_id = aws_kms_key.sns.id
}
```

## Best Practices

1. **Use multi-AZ deployments** - Spread resources across availability zones for high availability
2. **Implement least privilege IAM** - Grant minimum permissions required for each role
3. **Enable encryption everywhere** - Use KMS for data at rest, TLS for data in transit
4. **Use managed services** - Prefer RDS, ElastiCache, EKS over self-managed
5. **Implement proper networking** - Use private subnets, security groups, NACLs
6. **Enable logging and monitoring** - CloudWatch, CloudTrail, VPC Flow Logs
7. **Use Infrastructure as Code** - Terraform/CDK for all resources
8. **Implement cost controls** - Reserved instances, savings plans, budgets
9. **Automate backups** - Enable automated backups with appropriate retention
10. **Use tags consistently** - Environment, project, owner tags on all resources

## Common Pitfalls

1. **Overly permissive IAM** - Using * resources and actions. Always scope to specific ARNs.

2. **Public S3 buckets** - Always enable block public access. Use CloudFront or presigned URLs.

3. **Single AZ deployments** - All critical workloads should span multiple AZs.

4. **No encryption** - All storage and data transfer must be encrypted.

5. **Missing monitoring** - Without CloudWatch alarms, issues go unnoticed until customer impact.

6. **Hardcoded credentials** - Use IAM roles, Secrets Manager, or Parameter Store. Never hardcode.

## References

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
