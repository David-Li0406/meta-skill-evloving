# EKS Cluster Stack
# Deploys: EKS cluster + EKS config (addons) + Karpenter + ArgoCD registration

locals {
  cluster_name = "${values.cluster_name_prefix}-${values.environment}"
  environment  = values.environment

  # Common tags for all resources
  common_tags = merge(try(values.tags, {}), {
    Stack       = "eks-cluster"
    Cluster     = local.cluster_name
    Environment = values.environment
  })
}

# Core EKS cluster
unit "eks" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/eks?ref=${values.catalog_version}"
  path   = "eks"

  values = {
    version            = try(values.eks_module_version, "v1.0.0")
    name               = local.cluster_name
    kubernetes_version = try(values.kubernetes_version, "1.32")

    vpc_id     = values.vpc_id
    subnet_ids = values.subnet_ids

    # Control plane settings
    endpoint_private_access = try(values.endpoint_private_access, true)
    endpoint_public_access  = try(values.endpoint_public_access, true)

    # Logging
    enabled_log_types                        = try(values.enabled_log_types, ["api", "audit", "authenticator"])
    cloudwatch_log_group_retention_in_days   = try(values.cloudwatch_log_group_retention_in_days, 14)
    enable_cluster_creator_admin_permissions = true

    # Managed node groups
    eks_managed_node_groups = try(values.eks_managed_node_groups, {
      general = {
        instance_types = ["t3.xlarge"]
        min_size       = 2
        max_size       = 10
        desired_size   = 3
        block_device_mappings = {
          xvda = {
            device_name = "/dev/xvda"
            ebs = {
              volume_size           = 100
              volume_type           = "gp3"
              encrypted             = true
              delete_on_termination = true
            }
          }
        }
      }
    })

    # VPC-CNI addon (must be installed before compute)
    addons = {
      "vpc-cni" = {
        addon_version               = try(values.vpc_cni_version, "v1.20.4-eksbuild.1")
        before_compute              = true
        resolve_conflicts_on_create = "OVERWRITE"
        resolve_conflicts_on_update = "OVERWRITE"
      }
    }

    tags = local.common_tags
  }
}

# EKS configuration (addons, ENI config)
unit "eks-config" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/eks-config?ref=${values.catalog_version}"
  path   = "eks-config"

  values = {
    version  = try(values.eks_config_module_version, "main")
    eks_path = "../eks"

    # Additional addons (CoreDNS, kube-proxy, EBS CSI, etc.)
    eks_addons = try(values.eks_addons, [
      {
        name                        = "coredns"
        version                     = "v1.11.4-eksbuild.24"
        resolve_conflicts_on_create = "OVERWRITE"
        resolve_conflicts_on_update = "OVERWRITE"
      },
      {
        name                        = "kube-proxy"
        version                     = "v1.32.6-eksbuild.12"
        resolve_conflicts_on_create = "OVERWRITE"
        resolve_conflicts_on_update = "OVERWRITE"
      },
      {
        name                        = "aws-ebs-csi-driver"
        version                     = "v1.46.0-eksbuild.1"
        resolve_conflicts_on_create = "OVERWRITE"
        resolve_conflicts_on_update = "OVERWRITE"
      }
    ])

    # Secondary subnets for ENI config (custom networking)
    sub_availability_zones = try(values.availability_zones, [])
    sec_subnet_ids         = try(values.secondary_subnet_ids, [])

    # Node rollout configuration
    node_groups_to_rollout = try(values.node_groups_to_rollout, [])
    rollout_type           = try(values.rollout_type, "asg")
    role_arn               = try(values.role_arn, "")

    tags = local.common_tags
  }
}

# Karpenter for autoscaling
unit "karpenter" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/eks-karpenter?ref=${values.catalog_version}"
  path   = "karpenter"

  values = {
    version  = try(values.karpenter_module_version, "v1.0.0")
    eks_path = "../eks"

    enable_spot_termination = try(values.enable_spot_termination, true)

    node_iam_role_additional_policies = try(values.node_iam_role_additional_policies, {
      AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
    })

    tags = local.common_tags
  }
}

# ArgoCD cluster registration (optional)
unit "argocd-registration" {
  source = "git::git@github.com:YOUR_ORG/infrastructure-catalog.git//units/argocd-cluster-configuration?ref=${values.catalog_version}"
  path   = "argocd-registration"

  values = {
    version  = try(values.argocd_module_version, "v1.0.0")
    eks_path = "../eks"

    # ArgoCD hub configuration
    argocd_hub_account_id   = values.argocd_hub_account_id
    argocd_hub_region       = try(values.argocd_hub_region, "us-east-1")
    argocd_hub_role_arn     = values.argocd_hub_role_arn
    argocd_server_addr      = values.argocd_server_addr
    argocd_token_secret_arn = values.argocd_token_secret_arn

    # Cluster labels for ArgoCD
    argocd_labels = merge(
      {
        environment = values.environment
        cluster     = local.cluster_name
      },
      try(values.argocd_labels, {})
    )

    tags = local.common_tags
  }
}
