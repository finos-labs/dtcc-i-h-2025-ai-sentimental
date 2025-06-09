# Create IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_ssm_instance_profile" {
  name = "EC2InstanceProfile"
  role = aws_iam_role.ec2_role.name
}

# Update EC2 Instance to Attach IAM Role
resource "aws_instance" "finbot_ec2" {
  ami                    = "ami-004364947f82c87a0" # Ubuntu 20.04 (update if needed)
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  subnet_id              = aws_subnet.main_subnet.id
  security_groups        = [aws_security_group.finbot_sg.id]
  associate_public_ip_address = true
  iam_instance_profile   = aws_iam_instance_profile.ec2_ssm_instance_profile.name  # Attach IAM role

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install python3-pip -y
              sudo apt install python3-venv -y
              python3 -m venv ~/finbot
              source ~/finbot/bin/activate
              mkdir -p /home/ubuntu/app
              cd /home/ubuntu/app
              git clone https://github.com/Sayan-sam/finbot.git .
              cd src
              pip install -r requirements.txt
              nohup streamlit run main.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false > streamlit.log 2>&1 &
              EOF

  tags = {
    Name = "StreamlitApp"
  }
}
