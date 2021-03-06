#! /bin/sh
yum update -y
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
chkconfig docker on

# make aws cred files
mkdir /home/ec2-user/.aws

# create aws auth folders and files
cat > /home/ec2-user/.aws/credentials << EOF1
[default]
aws_access_key_id=ASI************F4
aws_secret_access_key=u4*******************CA
aws_session_token=Fw**********************************7t
EOF1

cat > /home/ec2-user/.aws/config << EOF2
[default]
region=us-east-1
output=json
EOF2

# launch container from private ECR
# commands are appended to startup script for ec2 instances
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 2********3.dkr.ecr.us-east-1.amazonaws.com >> /home/ec2-user/.bashrc
docker run -d -e PORT=80 -e AWS_ACCESS_KEY_ID='ASI************F4' -e AWS_SECRET_ACCESS_KEY='u4*******************CA' -e AWS_SESSION_TOKEN='Fw**********************************7t' -p 80:80 2*******3.dkr.ecr.us-east-1.amazonaws.com/rpi-aws:0.0.4 >> /home/ec2-user/.bashrc

# just to make sure add startup commands to root user as well (may be redundant)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 2********3.dkr.ecr.us-east-1.amazonaws.com >> /home/ec2-user/.bashrc
docker run -d -e PORT=80 -e AWS_ACCESS_KEY_ID='ASI************F4' -e AWS_SECRET_ACCESS_KEY='u4*******************CA' -e AWS_SESSION_TOKEN='Fw**********************************7t' -p 80:80 2*******3.dkr.ecr.us-east-1.amazonaws.com/rpi-aws:0.0.4 >> /home/ec2-user/.bashrc
