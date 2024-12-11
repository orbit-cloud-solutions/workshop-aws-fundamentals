# Exercise 3 - interactive Docker, logs

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## exercise 03
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/03
    * cat Dockerfile # it's based on Amazon Linux
    * docker build -t al . # the dot is important
    * docker images # an image is created
    * docker run -itd --name al al
    * # -i means interactive, -t pseudo tty, -d detach
    * docker ps # it is runnning
    * docker exec -it al /bin/bash # runs shell in the container
    * yum install whois # we can modify existing container - install a package interactively
    * # this is normally never done, possibly for troubleshooting
    * Ctrl+D # we disconnected from our docker
    * docker ps # it's still running

## stop docker
    * docker stop al
    * docker ps # no longer running
    * docker ps -a # but we have some stopped containers
    * docker rm al
    
## run docker again
    * docker run -it --rm --name al al # remove docker when we are finished
    * # useful for interactive short tasks
    * Ctrl+D # disconnecting from container will remove it now

## cleanup
    * docker ps -a # amazon linux docker is gone
    * docker images # but its image still exists
    * docker rmi al # we can remove the image
    * docker images # it's gone
