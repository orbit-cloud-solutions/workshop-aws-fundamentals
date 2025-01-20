# Exercise 5 - hosting React frontend

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## exercise 05
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/05
    * cat Dockerfile
    * docker build -t frontend . # the dot is important
    * docker images # an image is created
    * docker run -d --name frontend -p 80:80 frontend
    * open your public IP address/hostname in browser

## stoppping the container
    * docker stop frontend
