variable "location" {
  description = "(Required)"
  type        = string
}

variable "subscription_id" {
  description = "(Required)"
  type        = string
}

variable "subscription_name" {
  description = "(Required)"
  type        = string
}

variable "organization" {
  description = "(Required)"
  type        = string
}

variable "tenant_id" {
  description = "(Required)"
  type        = string
}

variable "resource_group" {
  description = "(Required)"
  type        = string
}

variable "friendly_name" {
  description = "(Required) similar to app name but only alphanumeric and numbers."
  type        = string
}

variable "labels_context" {
  description = "null-label module context"
  type        = any
  default     = {}
}

variable "label_order" {
  description = "Null Label order for ID output"
  type        = list(string)
  default     = ["cluster_name", "environment"]
}

variable "security_groups" {
  description = "map of security group names"
  type        = map(any)
}

variable "bot_group" {
  description = ""
  type        = string
}

variable "human_group" {
  description = ""
  type        = string
}

variable "tf_identity_name" {
  description = ""
  type        = string
}
variable "service_principal_application_url" {
  description = ""
  type        = string
}
variable "root_keyvault_name" {
  description = ""
  type        = string
}
variable "container_registry_name" {
  description = ""
  type        = string
}
variable "container_registry_sku" {
  description = ""
  type        = string
}
variable "storage_account_tier" {
  description = ""
  type        = string
}
variable "storage_account_name" {
  description = ""
  type        = string
}
variable "account_replication_type" {
  description = ""
  type        = string
}
variable "state_container_name" {
  description = ""
  type        = string
}
variable "container_access_type" {
  description = ""
  type        = string
}

variable "admin_roles" {
  description = ""
  type        = map(any)
}

variable "automation_roles" {
  description = ""
  type        = map(any)
}

variable "root_secret_name" {
  description = ""
  type        = string
}

variable "key_permissions" {
  description = "Null Label order for ID output"
  type        = list(string)
}

variable "certificate_permissions" {
  description = ""
  type        = list(string)
}
variable "secret_permissions" {
  description = ""
  type        = list(string)
}
variable "storage_permissions" {
  description = ""
  type        = list(string)
}