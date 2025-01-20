from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,  # Import RemovalPolicy
    CfnOutput
)
from constructs import Construct

class DdbCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, 
                 name_shortcut: str, table_name: str, billing_mode: str,
                 table_class: str, partition_key_name: str, partition_key_type: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Convert string values to appropriate CDK types
        billing_mode_enum = dynamodb.BillingMode.PAY_PER_REQUEST if billing_mode == "PAY_PER_REQUEST" else dynamodb.BillingMode.PROVISIONED
        table_class_enum = dynamodb.TableClass.STANDARD_INFREQUENT_ACCESS if table_class == "STANDARD_INFREQUENT_ACCESS" else dynamodb.TableClass.STANDARD
        partition_key_type_enum = dynamodb.AttributeType.STRING if partition_key_type == "S" else dynamodb.AttributeType.NUMBER

        # Define the DynamoDB table
        table = dynamodb.Table(
            self, 
            "DynamoDBTable", 
            table_name=f"wksp-{name_shortcut}-dynamodb-{table_name}-table-cdk",
            partition_key=dynamodb.Attribute(
                name=partition_key_name,
                type=partition_key_type_enum,
            ),
            billing_mode=billing_mode_enum,
            table_class=table_class_enum,
            removal_policy=RemovalPolicy.DESTROY  # Use RemovalPolicy.DESTROY
        )

        # Optionally, add additional configurations or outputs
        CfnOutput(self, "DynamoDBTableName", value=table.table_name)
