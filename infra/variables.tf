variable "region" {
    description = "AWS region"
    default = "us-east-2"
}

variable "ec2_public_key" {
    description = "SSH public key"
    default = "assets/finbot_id_rsa.pub"
}

variable "deep_seek_api_key" {
    description = "DeepSeek API Key"
    default     = ""
}

variable "github_pat" {
    description = "GitHub Personal Access Token"
    default     = ""
}
