terraform {
  required_providers {
    random = {
      source = "hashicorp/random"
      version = "3.1.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.51.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "1.4.0"
    }
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id

  features {
      key_vault {
        recover_soft_deleted_key_vaults = true
        purge_soft_delete_on_destroy  = true
    }
  }
}

provider "azuread" {
  tenant_id = var.tenant_id
}