#initialize an empty data structure to hold our config
data "azurerm_client_config" "current-tf-user-config" {}

#use local backed
terraform {
  backend "local" {
  }
}

#create a resource group
resource "azurerm_resource_group" "my-resource-group" {
  name     = "tfdrg-${var.resource_group}"
  location = var.location
}

#create a service account with role based authentication, and some basic permissions
module "terraform_service_account" {
  source  = "./modules/az-sp-4-rbac"
  app_name = "https://${var.resource_group}-automation-account"
  resource_group = azurerm_resource_group.my-resource-group.name
  subscription = var.subscription_id
  role_name = "Contributor"
}

#create a keyvault to hold our keys and secrets
module "tf_azurerm_keyvault" {
  source  = "./modules/az-keyvault"
  name = var.keyvault_name
  location = azurerm_resource_group.my-resource-group.location
  resource_group = azurerm_resource_group.my-resource-group.name
  tenant_id = var.tenant_id
}

#create a key for the keyvault
resource "azurerm_key_vault_key" "tf_kv_key" {
  name         = var.keyvault_key_name
  key_vault_id = module.tf_azurerm_keyvault.azurerm_key_vault_id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]
}

#create a secret. we will reference it for our backend
resource "azurerm_key_vault_secret" "client_secret" {
  name         = var.client_secret_name
  value        = module.terraform_service_account.client_secret
  key_vault_id = module.tf_azurerm_keyvault.azurerm_key_vault_id
}

#create a container registry that will be used for aks
resource "azurerm_container_registry" "acr" {
  name                     = var.container_registry_name
  resource_group_name      = azurerm_resource_group.my-resource-group.name
  location                 = var.location
  sku                      = "Premium"
  admin_enabled            = true
}

#create a storage account to hold state container
resource "azurerm_storage_account" "storage_account" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.my-resource-group.name
  location                 = azurerm_resource_group.my-resource-group.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    environment = "staging"
  }
}

#create the storage container that will hold the state
resource "azurerm_storage_container" "state-container" {
  name                  = var.terraform_state_container_name
  storage_account_name  = "state-container"
  container_access_type = "private"
}

#create the storage container that will hold the website
resource "azurerm_storage_container" "website-container" {
  name                  = var.terraform_state_container_name
  storage_account_name  = "website-container"
  container_access_type = "private"
}

#create the storage container that will hold the state
resource "azurerm_storage_container" "media-container" {
  name                  = var.terraform_state_container_name
  storage_account_name  = "media-container"
  container_access_type = "private"
}