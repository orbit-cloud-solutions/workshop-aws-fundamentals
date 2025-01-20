import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_logs as logs,
    RemovalPolicy,
    Fn,
    CfnOutput
)
from constructs import Construct

class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, name_shortcut: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the DDB name from the DynamoDbStack 
        ddb_table_name = Fn.import_value(f"wksp-{name_shortcut}-ddb-cdk-stack-table-name")
        
        # Lambda function names and associated AWS managed policies
        lambda_policies = {
            'delete': [
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ],
            'get': [
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ],
            'list': [
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ],
            'options': []
            ,
            'update': [
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ]
        }

        for name, policies in lambda_policies.items():
            lambda_function = self.create_lambda(name_shortcut, name, policies, ddb_table_name)
            self.add_lambda_permission(lambda_function, name)

    def create_lambda(self, name_shortcut: str, lambda_name: str, policies: list, ddb_table_name: str):
        function_name = f"wksp-{name_shortcut}-{lambda_name}-lambda-cdk"
        handler_path = os.path.join('lambda_src', lambda_name, 'app.py')

        if not os.path.exists(handler_path):
            raise FileNotFoundError(f"Source code for {lambda_name} not found at {handler_path}")

        # Create CloudWatch Log Group with 1-day retention
        log_group = logs.LogGroup(self, f"{lambda_name}-log-group",
            log_group_name=f"/aws/lambda/{function_name}",
            retention=logs.RetentionDays.ONE_DAY,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create the IAM role for the Lambda function
        lambda_role = iam.Role(self, f"{lambda_name}-execution-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self, lambda_name, "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"),
            ]
        )

        # Add AWS managed policies passed from the lambda_policies dictionary
        for policy in policies:
            lambda_role.add_managed_policy(policy)

        # Create the Lambda function
        lambda_function = _lambda.Function(self, f"{lambda_name}-lambda-function",
            function_name=function_name,
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="app.lambda_handler",  # Assuming the handler is named 'lambda_handler' in each 'app.py'
            code=_lambda.Code.from_asset(os.path.join('lambda_src', lambda_name)),
            log_group=log_group,
            environment={"TABLE_NAME": ddb_table_name},
            role=lambda_role
        )

        # Grant Lambda permissions to write logs to its respective CloudWatch log group
        log_group.grant_write(lambda_role)

        # Create Output
        CfnOutput(self, f"{lambda_name}-lambda-function-arn", value=lambda_function.function_arn, export_name=f"wksp-{name_shortcut}-lambda-cdk-stack-{lambda_name}-function-arn")

        return lambda_function

    def add_lambda_permission(self, lambda_function: _lambda.IFunction, lambda_name: str):
        lambda_function.add_permission(
            f"{lambda_name}-lambda-api-gw-invoke-permissions",
            action="lambda:InvokeFunction",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com")
        )