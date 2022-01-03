location          = "West Europe"
subscription_id   = "268a4d72-ad25-43fe-859a-96c7cadb5173"
subscription_name = "tnt_sandbox1"
organization      = "myfedex"
tenant_id         = "b945c813-dce6-41f8-8457-5a12c2fe15bf"
resource_group    = "az-tkg-root-rg"
friendly_name     = "az-tkg"
security_groups = {
  azure_fxei_platform_team = "f342325b-e70e-478f-be67-1a64cef88d86"
}


bot_group                         = "tanzu-bots"
human_group                       = "tanzu-humans"
tf_identity_name                  = "az-tkg-terraform"
service_principal_application_url = "https://az-tkg-tf-automation-account"
root_keyvault_name                = "aztkgrootkv0"
container_registry_name           = "aztkgregistry0"
container_registry_sku            = "Premium"
storage_account_name              = "aztkgstorage0"
storage_account_tier              = "Standard"
account_replication_type          = "GRS"
state_container_name              = "az-tkg-state-0"
container_access_type             = "private"
root_secret_name                  = "azTKGrootSecret0"

admin_roles = {
  secret       = "Key Vault Secrets Officer"
  crypto       = "Key Vault Crypto Officer"
  certificates = "Key Vault Certificates Officer"
  useraccess   = "User Access Administrator"
}

automation_roles = {
  contributor = "Contributor"
  mio         = "Managed Identity Operator"
  vmc         = "Virtual Machine Contributor"
}

key_permissions = [
  "backup", "create", "decrypt",
  "delete", "encrypt", "get",
  "import", "list", "purge",
  "recover", "restore", "sign",
  "unwrapkey", "update",
  "verify", "wrapkey"
]

secret_permissions = [
  "backup", "delete", "get",
  "list", "purge", "recover",
  "restore", "set"
]

storage_permissions = [
  "backup", "delete", "deletesas",
  "get", "getsas", "list",
  "listsas", "purge", "recover",
  "regeneratekey", "restore", "set",
  "setsas", "update"
]

certificate_permissions = [
  "backup", "create", "delete",
  "deleteissuers", "get", "getissuers",
  "import", "list", "listissuers",
  "managecontacts", "manageissuers", "purge",
  "recover", "restore", "setissuers",
  "update"
]