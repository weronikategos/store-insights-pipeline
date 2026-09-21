variable "project_name" {
  description = "Prefix for resource names (no spaces, lowercase)"
  type        = string
  default     = "storeinsights"
}

variable "location" {
  description = "Azure region. On an Azure for Students subscription you may need to switch to an available region."
  type        = string
  default     = "switzerlandnorth"
}

variable "sql_admin_login" {
  description = "Azure SQL administrator login"
  type        = string
  default     = "sqladminuser"
}

variable "sql_admin_password" {
  description = "Azure SQL administrator password (passed via the TF_VAR_sql_admin_password environment variable, never stored in the repo!)"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment (dev/prod) — used as a tag and part of resource names"
  type        = string
  default     = "dev"
}
