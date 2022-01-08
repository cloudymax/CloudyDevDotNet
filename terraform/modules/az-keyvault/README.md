# terraform-azurerm-keyvault

Usage
```hcl
#create a keyvault to hold our keys and secrets
module "tf_azurerm_keyvault" {
  source         = ""
  version        = ""
  name           = "${var.resource_group}-vault"
  location       = azurerm_resource_group.my-resource-group.location
  resource_group = azurerm_resource_group.my-resource-group.name
  tenant_id      = var.tenant_id
}

#create a key for the keyvault
resource "azurerm_key_vault_key" "tf_kv_key" {
  name         = "${var.resource_group}-key"
  key_vault_id = module.tf_azurerm_keyvault.azurerm_key_vault_id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]
}
```


## notes
- Terraform will automatically recover a soft-deleted Key Vault during Creation if one is found.
you can opt out of this using the features block within the Provider block.

- As of 2020-12-15 Azure now requires that Soft Delete is enabled on Key Vaults and this can no longer be disabled. 

```hcl
provider "azurerm" {
  version         = 
  environment     = 
  client_id       = 
  client_secret   =
  subscription_id = 
  tenant_id       = 

  features {
    key_vault {
      recover_soft_deleted_key_vaults = false
      purge_soft_delete_on_destroy  = true
    }
  }
}
```