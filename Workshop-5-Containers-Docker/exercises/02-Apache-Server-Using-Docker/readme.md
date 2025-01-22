# Exercise 2 - Run an Apache Server Using Docker

## Login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## Download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## Build an Apache server
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/02
    * cat Dockerfile
    * docker build -t apache . # the dot is important
    * docker images # an image is created
    * docker run -d --name apache -p 80:80 apache
    * docker ps # docker is running
    * curl http://localhost # the page is returned
    * open public IP address in your browser
    * docker logs apache # displays container log

## Stop Docker
    * docker stop apache
    * docker ps # no longer running
    * docker ps -a # but we have some stopped containers
    * docker rm apache
    * docker ps -a # apache docker is gone
    * docker images # but its image still exists
