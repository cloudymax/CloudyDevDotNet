provider "azurerm" {
  subscription_id = ACCOUNT_SUBSCRIPTION_ID
  tenant_id       = ACCOUNT_TENANT_ID
  environment     = TERRAFORM_SEPCIFIC_ENVIRONMENT
  client_id       = SERVICE_PRINCIPAL_CLIENT_ID
  client_secret   = SERVICE_PRINCIPAL_CLIENT_SECRET

  features {
    key_vault {
      recover_soft_deleted_key_vaults = true
      purge_soft_delete_on_destroy    = false
    }
  }
}

provider "azuread" {
  environment = TERRAFORM_SEPCIFIC_ENVIRONMENT
  tenant_id   = ACCOUNT_TENANT_ID
}
