# Exercise 4 - Passing Environment Variables

## Login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## Download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## Exercise 04
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/04
    * cat Dockerfile # it's Python
    * docker build -t python . # the dot is important
    * docker images # an image is created
    * docker run --rm python
    * docker run --rm -e NAME="Joe" python
    * docker ps # nothing's left
