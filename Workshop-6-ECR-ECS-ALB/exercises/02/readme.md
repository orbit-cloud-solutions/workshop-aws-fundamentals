# Exercise 02 - upload container image to ECR

## login to EC2
    * start your EC2 instance
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## create ECR repository
    * AWS Console > Elastic Container Registry > Create a repository
    * Create private repository
    * Repository name: xxxx/frontend
    * Create

## add permissions to your EC2 instance
    * AWS Console > IAM > Roles > select role of your EC2 instance (wksp-xxxx-ec2-iam-role)
    * attach managed permission AmazonEC2ContainerRegistryFullAccess

## build and upload docker image to repository
    * login to your EC2 as root
    * cd workshops-aws-fundamentals-code-base/workshop-06/exercises/02
    * cat Dockerfile
    * select your ECR repository in AWS Console > View Push commands
    * copy and paste command 1-4 to your EC2 shell
    * Close
    * go to AWS Console > ECR > your repo
    * you should see your image there
