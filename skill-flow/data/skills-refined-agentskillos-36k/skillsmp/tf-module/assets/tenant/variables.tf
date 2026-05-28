# Tenant Module Variables

variable "portal_name" {
  description = "Portal workspace name"
  type        = string
  default     = "myportal"
}

variable "shared" {
  description = "Shared workspace name"
  type        = string
}

variable "environment" {
  description = "Environment type (dev, staging, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod"
  }
}

variable "github_org" {
  description = "GitHub organization"
  type        = string
  default     = ""
}

variable "github_installation_id" {
  description = "GitHub App installation ID"
  type        = string
  default     = ""
}
