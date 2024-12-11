# Exercise 4 - passing environment variables

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## exercise 04
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/04
    * cat Dockerfile # it's Python
    * docker build -t python . # the dot is important
    * docker images # an image is created
    * docker run --rm python
