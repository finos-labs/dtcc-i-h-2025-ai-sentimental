provider "aws" {
  region = var.region
  profile = var.profile
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.1"
    } 
  }
}

resource "aws_s3_bucket" "secure_bucket" {
  bucket = "finbot-app-terraform-state"
  tags = {
    Name        = "Finbot Terraform State"
    Environment = "Hackathon"
  }
}



