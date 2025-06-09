output "streamlit_app_url" {
  value = "http://${aws_instance.finbot_ec2.public_ip}:8501"
}

output "ec2_public_ip" {
  value = aws_instance.finbot_ec2.public_ip
}
