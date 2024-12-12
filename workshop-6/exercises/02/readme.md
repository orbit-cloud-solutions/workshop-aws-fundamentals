# Exercise 02 - upload container image to ECR

## login to EC2
    * start your EC2 instance
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## build docker image
    * cd workshops-aws-fundamentals-code-base/workshop-06/exercises/02
    * cat Dockerfile
    * docker build -t frontend . # the dot is important
    * docker images # frontend image is created

## create ECR repository
    * AWS Console > Elastic Container Registry > Create a repository
    * name: xxxx/frontend
    * Create

## upload docker image to repository
