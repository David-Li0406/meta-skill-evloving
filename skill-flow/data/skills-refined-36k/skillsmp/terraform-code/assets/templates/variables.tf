# Input variables
# Variables should be alphabetically ordered

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "japaneast"
}

variable "project_name" {
  description = "Project name used in resource naming"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]{3,24}$", var.project_name))
    error_message = "Project name must be 3-24 characters, lowercase alphanumeric and hyphens only."
  }
}

# Example: Network configuration
# variable "vnet_address_space" {
#   description = "Address space for virtual network"
#   type        = list(string)
#   default     = ["10.0.0.0/16"]
# }

# Example: Sensitive variable
# variable "admin_password" {
#   description = "Administrator password"
#   type        = string
#   sensitive   = true
# }
