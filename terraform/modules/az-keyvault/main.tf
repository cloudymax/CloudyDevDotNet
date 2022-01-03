data "azurerm_client_config" "current_tf_user" {}
data "azurerm_resource_group" "rg" {
  name = var.resource_group
}

resource "azurerm_key_vault" "keyvault" {
  tenant_id                   = var.tenant_id
  location                    = var.location
  resource_group_name         = var.resource_group
  name                        = var.name
  purge_protection_enabled    = var.purge_protection
  enabled_for_deployment      = true
  enable_rbac_authorization   = true
  enabled_for_disk_encryption = true
  soft_delete_retention_days  = 7
  sku_name                    = var.sku_name

}

# Create role assignments for the user otherwise the vault will lock you out
module "tf_user_role_assignment" {
  source       = "../az-role-assignment"
  scope        = data.azurerm_resource_group.rg.id
  principal_id = data.azurerm_client_config.current_tf_user.object_id
  role_list = {
    "secret"       = "Key Vault Secrets Officer",
    "crypto"       = "Key Vault Crypto Officer",
    "certificates" = "Key Vault Certificates Officer",
    "useraccess"   = "User Access Administrator"
  }
}

output "azurerm_key_vault_id" {
  value = azurerm_key_vault.keyvault.id
}

output "azurerm_key_vault_data" {
  value = azurerm_key_vault.keyvault
}