# AWS Fundamentals Workshop Series

This repository contains materials and exercises for an 8-week AWS fundamentals workshop series, covering core AWS services, serverless architecture, containerization, and Infrastructure as Code.

## Course Structure

#### Workshop 1: Exploring AWS Core Services and Networking Basics
    * VPC setup and configuration
    * IAM roles and policies
    * Security groups
    * S3 bucket creation and management
    * EC2 instance deployment and SSH access

#### Workshop 2: NoSQL Databases, DNS, Monitoring and User Auth
    * Route 53 DNS configuration
    * DynamoDB table setup
    * CloudWatch monitoring and alarms
    * Cognito user authentication

#### Workshop 3: Implementing Serverless CRUD with Lambda
    * Lambda function basics
    * DynamoDB integration
    * CRUD operations implementation
    * Testing and monitoring

#### Workshop 4: Exposing Serverless Functions with API Gateway
    * REST API creation
    * API security implementation
    * Custom domain configuration
    * API testing and monitoring

#### Workshop 5: Developing and Containerizing a Frontend
    * Docker basics
    * Container management
    * Frontend containerization
    * Container networking

#### Workshop 6: Deploying Frontend to AWS ECS with ALB
    * ECR setup
    * ECS deployment
    * ALB configuration
    * Frontend deployment automation

### Workshop 7: Introduction to Infrastructure as Code
    * IaC fundamentals
    * AWS CLI, SDK, and CDK setup
    * Multiple IaC approaches
    * Resource deployment automation

#### Workshop 8: Automating Infrastructure Deployment with CDK
    * Complete architecture deployment
    * Custom CDK constructs
    * CodeBuild integration
    * Deployment automation

## Prerequisites
    * AWS Account
    * Basic understanding of cloud computing
    * Familiarity with Python programming
    * Basic knowledge of Docker and containers
    * Understanding of REST APIs

## Workshop Environment Setup
    * EC2 instance with required permissions
    * Development tools installation
        * AWS CLI
        * Python and pip
        * Node.js and npm
        * AWS CDK
        * Docker

## Target Architecture
    The workshop series builds a complete cloud application with:
    * Frontend hosted on ECS
    * Serverless backend using Lambda and API Gateway
    * DynamoDB for data storage
    * Route 53 for DNS management
    * Cognito for user authentication
    * CloudWatch for monitoring
    * Full IaC deployment capability

## Repository Structure
    Each workshop has its own directory containing:
    * README.md with workshop instructions
    * Exercise files and starter code
    * Solution files
    * Additional resources and documentation

## Additional Resources
### Documentation
    * [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
    * [API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
    * [DynamoDB](https://docs.aws.amazon.com/dynamodb/)
    * [ECS](https://docs.aws.amazon.com/ecs/)
    * [AWS CDK](https://docs.aws.amazon.com/cdk/)

## Notes
    * Workshop materials are designed for hands-on learning
    * Each workshop builds upon previous workshops
    * Focus on practical, real-world scenarios
    * Includes both theoretical concepts and hands-on exercises