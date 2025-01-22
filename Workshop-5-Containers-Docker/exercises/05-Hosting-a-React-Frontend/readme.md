# Exercise 5 - Hosting a React Frontend

## Login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## Download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## Exercise 05
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/05
    * cat Dockerfile
    * docker build -t frontend . # the dot is important
    * docker images # an image is created
    * docker run -d --name frontend -p 80:80 frontend
    * open your public IP address/hostname in browser

## Stoppping the container
    * docker stop frontend
