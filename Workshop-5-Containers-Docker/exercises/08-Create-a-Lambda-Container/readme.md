# Exercise 8 - Create a Lambda Container

## Login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## Download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## Exercise 08
    * cd workshops-aws-fundamentals-code-base/workshop-05/exercises/08
    * docker build -t lambda . # installs python and AWS Runtime Interface Client
    * cat app/index.py # this is Lambda handler
    * docker run -d -p 9000:8080 --name lambda lambda # we run the container
    * curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
    * it should respond

## Cleanup
    * docker stop lambda
    * docker rm lambda
