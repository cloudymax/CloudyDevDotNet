variable "location" {
  description = "(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created."
  type        = string
}

variable "resource_group" {
  description = "(Required) azure resource group name"
  type        = string
}

variable "sku_name" {
  description = "(Optional) sku option for keyvault"
  type        = string
  default     = "standard"
}

variable "purge_protection" {
  description = "(Optional) enable/disable purge protection"
  type        = bool
  default     = false
}

variable "name" {
  description = "(Optional) name of the keyvault."
  type        = string
}

variable "tenant_id" {
  description = "(Required) azure tenant idt."
  type        = string
}