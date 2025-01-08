#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.dynamodb_stack import DynamoDbStack
from stacks.lambda_stack import LambdaStack
from stacks.apigateway_stack import ApiGatewayStack
from stacks.cognito_stack import CognitoStack
from stacks.ecs_alb_stack import EcsAlbStack

# Define parameters directly in app.py as a config
params = {
    "aws_account": "108782094079",
    "aws_region": "eu-central-1",
    "name_shortcut": "fika",
    "table_name": "product",
    "billing_mode": "PAY_PER_REQUEST",
    "table_class": "STANDARD_INFREQUENT_ACCESS",
    "partition_key_name": "ProductID",
    "partition_key_type": "S",
    "api_certificate_arn":"arn:aws:acm:eu-central-1:108782094079:certificate/96afe745-c6cf-484f-8251-85dcf0971ab2",
    "route53_zone_id":"Z08708682948NVKMBZ5GR",
    "route53_zone_name":"workshop.virtualcomputing.cz",
    "container_uri":"108782094079.dkr.ecr.eu-central-1.amazonaws.com/wksp/frontend:latest",
    "app_certificate_arn":"arn:aws:acm:eu-central-1:108782094079:certificate/5dad3efe-c1a2-4676-8cd4-6b9ac9e53ef7",
    "vpc_id":"vpc-00188a5ec2e264a84"
}

# Create an app instance
app = cdk.App()

env = cdk.Environment(account=params["aws_account"], region=params["aws_region"])

ddb_stack_name = f"wksp-{params['name_shortcut']}-ddb-cdk-stack"
lambda_stack_name = f"wksp-{params['name_shortcut']}-lambda-cdk-stack"
apigateway_stack_name = f"wksp-{params['name_shortcut']}-apigateway-cdk-stack"
cognito_stack_name = f"wksp-{params['name_shortcut']}-cognito-cdk-stack"
ecs_alb_stack_name = f"wksp-{params['name_shortcut']}-ecs-alb-cdk-stack"

dynamodbStack = DynamoDbStack(
    app, 
    ddb_stack_name,
    env=env,
    name_shortcut=params["name_shortcut"],
    table_name=params["table_name"],
    billing_mode=params["billing_mode"],
    table_class=params["table_class"],
    partition_key_name=params["partition_key_name"],
    partition_key_type=params["partition_key_type"]
)

lambdaStack = LambdaStack(
    app,
    lambda_stack_name,
    env=env,
    name_shortcut=params["name_shortcut"]
)

apigatewayStack = ApiGatewayStack(
    app,
    apigateway_stack_name,
    env=env,
    name_shortcut=params["name_shortcut"],
    api_certificate_arn=params["api_certificate_arn"],
    route53_zone_id=params["route53_zone_id"],
    route53_zone_name=params["route53_zone_name"]
)

cognitoStack = CognitoStack(
    app,
    cognito_stack_name,
    env=env,
    name_shortcut=params["name_shortcut"],
    route53_zone_name=params["route53_zone_name"]
)

ecsAlbStack = EcsAlbStack(
    app,
    ecs_alb_stack_name,
    env=env,
    name_shortcut=params["name_shortcut"],
    container_uri=params["container_uri"],
    app_certificate_arn=params["app_certificate_arn"],
    vpc_id=params["vpc_id"],
    route53_zone_id=params["route53_zone_id"],
    route53_zone_name=params["route53_zone_name"]
)

# Add dependencies between stacks
lambdaStack.add_dependency(dynamodbStack)  # Lambda depends on DynamoDB
apigatewayStack.add_dependency(lambdaStack)  # API Gateway depends on Lambda
ecsAlbStack.add_dependency(apigatewayStack)  # ECS/ALB depends on API Gateway

# Synthesize the app (prepare for deployment)
app.synth()
