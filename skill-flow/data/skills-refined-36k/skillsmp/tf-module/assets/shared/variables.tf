# Shared Module Variables

variable "portal_name" {
  description = "Portal workspace name"
  type        = string
}

variable "infra" {
  description = "Infrastructure name"
  type        = string
}

variable "rds" {
  description = "RDS configuration"
  type = object({
    engine_version = string
    instance_class = optional(string, "db.t3.micro")
    multi_az       = optional(bool, false)
    scaling_configuration = optional(object({
      min_capacity = number
      max_capacity = number
    }))
  })
  default = null
}
