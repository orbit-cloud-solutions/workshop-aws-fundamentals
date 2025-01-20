# Exercise 01 - create Application Load Balancer

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## create target group
    * EC2 > Target Groups > Create target group # not in VPC > Target Groups!
    * Instances
    * Name: wksp-xxxx-tg
    * Protocol: HTTP/80
    * Health checks, HTTP, /
    * Next
    * Register targets - select both wksp-web?-ec2-instances, Include as pending below
    * Create target group, wait...

## create ALB
    * EC2 > Load Balancers > Create Load Balancer
    * Application Load Balancer, Create
    * Name: wksp-xxxx-alb
    * Internet facing
    * IPv4, all 3 Availability Zones
    * Security Group - deselect default, select wksp-alb-sg (allows HTTP and HTTPS)
    * select your target group wksp-xxxx-tg
    * Create load balancer

## test the connection
    * copy DNS name of your ALB
    * go to http://<your_alb_dns_name>/
    * refresh the page - you should see both Instance 1 and 2

## add SSL/TLS listener
    * we already have a certificate
    * EC2 > Load Balancers > select your ALB
    * Add listener
    * HTTPS/443
    * Forward to target groups, select your target group
    * Certificate from ACM, select

## create CNAME
    * go to Route 53 > Hosted Zones
    * select workshop.* zone
    * Create record
    * Record name: xxxx-alb
    * Record type: A
    * Alias
    * Alias to Application and Classic Load Balancer
    * Frankfurt
    * select your ALB
    * Create records

## test the connection
    * go to https://xxxx-alb.workshop.virtualcomputing.cz/
    * refresh the page - you should see both Instance 1 and 2
    
