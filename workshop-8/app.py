#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.dynamodb_stack import DynamoDbStack
from stacks.lambda_stack import LambdaStack

# Define parameters directly in app.py as a config
params = {
    "name_shortcut": "fika",
    "table_name": "product",
    "billing_mode": "PAY_PER_REQUEST",
    "table_class": "STANDARD_INFREQUENT_ACCESS",
    "partition_key_name": "ProductID",
    "partition_key_type": "S"
}

# Create an app instance
app = cdk.App()

ddb_stack_name = f"wksp-{params['name_shortcut']}-ddb-cdk-stack"
lambda_stack_name = f"wksp-{params['name_shortcut']}-lambda-cdk-stack"

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
    name_shortcut=params["name_shortcut"])

# Synthesize the app (prepare for deployment)
app.synth()
