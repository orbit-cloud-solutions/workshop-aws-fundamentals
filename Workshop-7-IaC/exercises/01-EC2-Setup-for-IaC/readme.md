# Exercise 1 - EC2 Setup for IaC

## Pepare IAM Role
    * Navigate to IAM Console
    * Create role wksp-{NameShortcut}-ec2-iam-role
    * Attach AdministratorAccess policy

## Configure EC2 Instance
    * Increase instance size to t3a.small
    * If using SSM:
        * Switch to /home/ec2-user using sudo
        * Or switch to root using sudo su