# Exercise 7 - backing up container images and containers

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## exercise 07
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/07
    * docker run --name apache -d -p 80:80 -v $(pwd)/html:/usr/local/apache2/htdocs/ httpd:latest
    * open your public ip address/hostname in web browser
    * docker save httpd:latest | gzip > httpd_latest.tgz # this saves docker image to archive, takes a while
    * ll -h # notice image size
    * docker commit apache apache:saved # creates image from existing container
    * docker images # apache:saved image was created from container
    * you can backup using docker save if you need:
    * docker save httpd:saved | gzip > httpd_saved.tgz # we have container backup now
    * ll -h

## stop
    * docker stop apache

## bonus
    * if you want to restore from backup, you can use:
    * docker load < httpd_saved.tgz # to create docker image from archive
    * docker run... # to run it again
