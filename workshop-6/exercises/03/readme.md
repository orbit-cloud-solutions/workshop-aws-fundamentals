# Exercise 03 - hosting React frontend in ECR

## login to EC2
    * login as ec2-user@<ip_address>
    * sudo su -

## download exercises
    * yum install git
    * git clone https://github.com/orbit-cloud-solutions/workshops-aws-fundamentals-code-base.git

## create ECS Task definition
    * AWS > ECS > Task deinitions > Create new task definition
    * Task definition family: wksp-xxxx-ecs-task
    * Launch type: AWS Fargate
    * CPU: .25 vCPU
    * Memory: .5 GB
    * Task execution role: select wksp-ecs-task-er
    * Container 1
        * Name: frontend
        * Image URI: find your image in ECR and copy its URI
        * (108782094079.dkr.ecr.eu-central-1.amazonaws.com/xxx/frontend:latest)
    * Create

## create ECS cluster
    * AWS > ECS > Clusters > Create Cluster
    * Cluster name: wksp-xxxx-ecs-cluster
    * AWS Fargate
    * Create

## create ECS service
    * select your ECS cluster/Services
    * Create
    * Compute options: Launch Type: FARGATE/LATEST
    * Application type: Service
    * Family: wksp-xxxx-ecs-task/LATEST
    * Service name: wksp-xxxx-ecs-service
    * Desired tasks: 1
    * Load balancing:
        * Application Load Balancer
        * Use existing load balancer: wksp-xxxx-alb
        * Use existing listener: 443
        * Create new target group
            * name: wksp-xxxx-ecs-service-tg
            * protocol: HTTP
            * Path pattern: *
            * Evaluation order: 1
    * Create, wait... # you can check progress in CloudFormation

## check the application
    * go to to your ALB https port (https://xxxx-alb.workshop.virtualcomputing.cz/)
    * go to to your ALB http port (http://xxxx-alb.workshop.virtualcomputing.cz/)
    * what happened?
