# Exercise 6 - Launch and Connect to EC2

## Launch an EC2 instance
    * Navigate to EC2 service
    * Launch new instance
    * Select Amazon Linux 2 AMI
    * Choose instance type
    * Configure VPC settings:
        * Select custom VPC
        * Choose public subnet
    * Assign IAM role created earlier
    * Select security group created earlier
    * Choose existing key pair
    * Launch instance

## Connect to EC2 instance
    * Click your instance ID
    * Click the "Connect" button
    * Choose "SSH client"
    * Follow the instructions
    * The command to connect will look something like ssh -i "wksp-jama-ec2-instance-kp.pem" ec2-user@ec2-18-184-189-105.eu-central-1.compute.amazonaws.com
