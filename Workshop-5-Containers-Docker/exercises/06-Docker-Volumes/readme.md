# Exercise 6 - Docker Volumes

## Login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## Download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## Exercise 06
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/06
    * docker run --name apache --rm -p 80:80 -v $(pwd)/html:/usr/local/apache2/htdocs/ httpd:latest
    * open your public ip address/hostname in web browser
    * notice output from container
    * Ctrl+C will stop and remove the container
    * docker ps -a # it' indeed gone