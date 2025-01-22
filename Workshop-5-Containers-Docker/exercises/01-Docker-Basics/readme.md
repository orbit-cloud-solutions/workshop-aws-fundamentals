# Exercise 1 - Docker Basics

## Create/start EC2 instance
    * upload public key wksp-kavr-ec2-instance-kp
    * wksp-kavr-ec2-instance
    * t3a.micro
    * Amazon Linux 2023
    * subnet A/B/C
    * public IP address
    * IAM role wksp-kavr-ec2-iam-role
        * AmazonEC2ContainerRegistryFullAccess
    * security group wksp-kavr-ec2-instance-sg
        * port 22/tcp from our public IP address
        * port 80/tcp from our public IP address
    * 8GB storage is OK

## Install docker
    * $ sudo su -
    * # yum update && yum install docker
    * # systemctl start docker
    * # systemctl enable docker

## Run your first container
    * docker run hello-world # it automatically does 'docker pull' if needed
    * docker images
