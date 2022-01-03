terraform {
  required_version = REQUIRED_VERSION
  backend "azurerm" {
    storage_account_name = STATE_DATA_STORAGE_ACCOUNT_NAME
    container_name       = STATE_DATA_STATE_CONTAINER
    resource_group_name  = RESOURCE_GROUP_NAME
    key                  = TERRAFORM_SEPCIFIC_KEY
    subscription_id      = ACCOUNT_SUBSCRIPTION_ID
    tenant_id            = ACCOUNT_TENANT_ID
  }
}