variable "application" {
  default = "staging-backend"
}
variable "environment" {
  default = "backend-staging"
}
variable "solution_stack_name" {
  default = "64bit Amazon Linux 2023 v4.0.6 running Python 3.11"
}
variable "ACCESS_KEY_ID" {
  type = string
}
variable "SECRET_ACCESS_KEY" {
  type = string
}
variable "POSTGRES_PASSWORD" {
  type = string
}
variable "DJANGO_STAGING_SECRET" {
  type = string
}
variable "STAGING_MASTER_USER_PASS" {
  type = string
}
