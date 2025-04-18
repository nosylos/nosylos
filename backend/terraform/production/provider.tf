terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "eu-west-3"
  access_key = var.PROD_ACCESS_KEY_ID
  secret_key = var.PROD_SECRET_ACCESS_KEY
}

terraform {
  backend "http" {
  }
}
