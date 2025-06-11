# Create IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_ssm_instance_profile" {
  name = "EC2InstanceProfile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_instance" "finbot_ec2" {
  ami                         = "ami-004364947f82c87a0"
  instance_type               = "m5.large"
  key_name                    = aws_key_pair.deployer.key_name
  subnet_id                   = aws_subnet.main_subnet.id
  security_groups             = [aws_security_group.finbot_sg.id]
  associate_public_ip_address = false
  iam_instance_profile        = aws_iam_instance_profile.ec2_ssm_instance_profile.name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install python3-pip -y
              sudo apt install python3-venv -y

              sudo -u ubuntu python3 -m venv /home/ubuntu/finbot
              sudo -u ubuntu /bin/bash -c "
                source /home/ubuntu/finbot/bin/activate && \
                mkdir -p /home/ubuntu/app && \
                cd /home/ubuntu/app && \
                git clone https://Sayan-sam:${var.github_pat}@github.com/finos-labs/dtcc-i-h-2025-ai-sentimental.git . && \
                cd src && \
                pip install -r requirements.txt && \
                nohup streamlit run main.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false > streamlit.log 2>&1 &
              "
              EOF

  tags = {
    Name = "StreamlitApp"
  }
}

resource "aws_eip" "finbot_eip" {
  instance = aws_instance.finbot_ec2.id
  depends_on = [aws_instance.finbot_ec2]
}
