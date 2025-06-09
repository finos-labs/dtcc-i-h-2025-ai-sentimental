resource "aws_ssm_parameter" "deep_seek_api_key" {
  name  = "deep_seek_api_key"
  type  = "SecureString"
  value = var.deep_seek_api_key
}

resource "aws_ssm_parameter" "ec2_host" {
  name      = "ec2_host"
  type      = "String"
  value     = aws_instance.finbot_ec2.public_ip
  depends_on = [aws_instance.finbot_ec2]
}
