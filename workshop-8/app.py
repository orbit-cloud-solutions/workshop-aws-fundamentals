#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.dynamodb_stack import DynamoDbStack
from stacks.lambda_stack import LambdaStack
from stacks.apigateway_stack import ApiGatewayStack


# Define parameters directly in app.py as a config
params = {
    "name_shortcut": "fika",
    "table_name": "product",
    "billing_mode": "PAY_PER_REQUEST",
    "table_class": "STANDARD_INFREQUENT_ACCESS",
    "partition_key_name": "ProductID",
    "partition_key_type": "S",
    "certificate_arn":"arn:aws:acm:eu-central-1:108782094079:certificate/ec7277ab-dc7f-4150-a60f-87483bfdbcc1",
    "route53_zone_id":"Z08708682948NVKMBZ5GR",
    "route53_zone_name":"workshop.virtualcomputing.cz",
}

# Create an app instance
app = cdk.App()

ddb_stack_name = f"wksp-{params['name_shortcut']}-ddb-cdk-stack"
lambda_stack_name = f"wksp-{params['name_shortcut']}-lambda-cdk-stack"
apigateway_stack_name = f"wksp-{params['name_shortcut']}-apigateway-cdk-stack"

# Pass the params directly to the DdbCdkStack
dynamodbStack = DynamoDbStack(
    app, 
    ddb_stack_name,
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
    name_shortcut=params["name_shortcut"]
)

apigatewayStack = ApiGatewayStack(
    app,
    apigateway_stack_name,
    name_shortcut=params["name_shortcut"],
    certificate_arn=params["certificate_arn"],
    route53_zone_id=params["route53_zone_id"],
    route53_zone_name=params["route53_zone_name"]
)

# Synthesize the app (prepare for deployment)
app.synth()
