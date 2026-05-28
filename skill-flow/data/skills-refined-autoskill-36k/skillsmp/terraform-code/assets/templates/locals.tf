# Local values

locals {
  # Common tags applied to all resources
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
  }

  # Resource naming pattern
  resource_prefix = "${var.project_name}-${var.environment}"

  # Example: Network configuration
  # network_config = {
  #   vnet_name = "${local.resource_prefix}-vnet"
  #   subnets = {
  #     app = {
  #       address_prefix    = "10.0.1.0/24"
  #       service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
  #     }
  #     data = {
  #       address_prefix    = "10.0.2.0/24"
  #       service_endpoints = ["Microsoft.Sql"]
  #     }
  #   }
  # }
}
