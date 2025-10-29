variable "location" {
  description = "The location where resources will be deployed."
  default     = "swedencentral"
}

variable "prefix_app_name" {
  description = "app name before each resource name"
  default = "hr-project"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID used by the provider. Leave unset to read the value from env_variable.sh."
  default     = null
}
