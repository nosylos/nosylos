variable "application" {
  default = "production-backend"
}
variable "environment" {
  default = "backend-prod"
}
variable "solution_stack_name" {
  default = "64bit Amazon Linux 2023 v4.0.6 running Python 3.11"
}
variable "PROD_ACCESS_KEY_ID" {
  type = string
}
variable "PROD_SECRET_ACCESS_KEY" {
  type = string
}
variable "PROD_POSTGRES_PASSWORD" {
  type = string
}
