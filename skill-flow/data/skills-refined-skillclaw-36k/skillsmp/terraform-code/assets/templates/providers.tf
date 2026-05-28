# Azure Provider Configuration

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }

    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }
  }

  # Optional: Specify subscription
  # subscription_id = var.subscription_id
}

provider "azapi" {
  # Optional: Use same subscription as azurerm
  # subscription_id = var.subscription_id
}
