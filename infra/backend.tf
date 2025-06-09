terraform {
  backend "s3" {
    bucket = "finbot-app-terraform-state"
    key    = "finbot/terraform.tfstate"
    region = "us-east-2"
  }
}
