output "location" { value = azurerm_resource_group.my-resource-group.location }
output "subscription_id" { value = var.subscription_id }
output "subscription_name" { value = var.subscription_name }
output "organizarion" { value = var.organization }
output "tenant_id" { value = var.tenant_id }
output "keyvault_name" { value = var.keyvault_name }
output "keyvault_id" { value = azurerm_key_vault_key.tf_kv_key.key_vault_id }
output "provider-secret-name" { value = var.client_secret_name }
output "resource_group" { value = azurerm_resource_group.my-resource-group.name }

output "storage-account" { value = azurerm_storage_account.storage_account.name }
output "state-container" { value = azurerm_storage_container.container.name }
output "sp-name" { value = module.terraform_service_account.display_name }
output "sp-client-id" { value = module.terraform_service_account.client_id }
output "sp-object-id" { value = module.terraform_service_account.object_id }
output "key-kv-name" { value = var.keyvault_key_name }
output "container-registry-name" { value = var.container_registry_name }