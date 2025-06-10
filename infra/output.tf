output "streamlit_app_url" {
  value = "http://${aws_eip.finbot_eip.public_ip}:8501"
}

output "ec2_public_ip" {
  value = aws_eip.finbot_eip.public_ip
}
