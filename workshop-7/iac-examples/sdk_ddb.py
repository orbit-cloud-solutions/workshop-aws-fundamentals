import boto3
import logging
import os
from botocore.exceptions import BotoCoreError, ClientError

# Initialize logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

ddb_client = boto3.client('dynamodb', 'eu-central-1')

def create_dynamodb_table(name_shortcut, table_name, billing_mode="PAY_PER_REQUEST", 
                          table_class="STANDARD_INFREQUENT_ACCESS", partition_key_name="ProductID", 
                          partition_key_type="S"):
    """
    Function to create a DynamoDB table using Boto3.

    Parameters:
        name_shortcut (str): Your name shortcut (e.g., "fika").
        table_name (str): Name of the DynamoDB table.
        billing_mode (str): Billing mode for the table (PROVISIONED or PAY_PER_REQUEST).
        table_class (str): Class of the DynamoDB table (STANDARD or STANDARD_INFREQUENT_ACCESS).
        partition_key_name (str): Name of the partition key (primary key).
        partition_key_type (str): Data type of the partition key (S, N, B).

    Returns:
        dict: Response from the `create_table` call.
    """
    
    full_table_name = f"wksp-{name_shortcut}-dynamodb-{table_name}-table-sdk"
    logger.info(f"Creating DynamoDB table: {full_table_name}")

    try:
        response = ddb_client.create_table(
            TableName=full_table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': partition_key_name,
                    'AttributeType': partition_key_type
                }
            ],
            KeySchema=[
                {
                    'AttributeName': partition_key_name,
                    'KeyType': 'HASH'
                }
            ],
            BillingMode=billing_mode,
            TableClass=table_class
        )
        logger.info(f"Successfully created table: {full_table_name}")
        return response
    except (ClientError, BotoCoreError) as e:
        logger.error(f"Failed to create table: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


def lambda_handler(event, context):
    """
    AWS Lambda handler to create a DynamoDB table.
    
    Parameters:
        event (dict): Input parameters passed to the Lambda function.
        context (LambdaContext): Lambda runtime information.
    
    Returns:
        dict: Response from the DynamoDB table creation process.

    Event example:
        {
            "NameShortcut": "fika",
            "TableName": "product",
            "BillingMode": "PAY_PER_REQUEST",
            "TableClass": "STANDARD_INFREQUENT_ACCESS",
            "PartitionKeyName": "ProductID",
            "PartitionKeyType": "S"
        }
    """
    logger.info("Lambda function invoked")

    name_shortcut = event.get("NameShortcut", "fika")
    table_name = event.get("TableName", "product")
    billing_mode = event.get("BillingMode", "PAY_PER_REQUEST")
    table_class = event.get("TableClass", "STANDARD_INFREQUENT_ACCESS")
    partition_key_name = event.get("PartitionKeyName", "ProductID")
    partition_key_type = event.get("PartitionKeyType", "S")

    try:
        response = create_dynamodb_table(
            name_shortcut=name_shortcut,
            table_name=table_name,
            billing_mode=billing_mode,
            table_class=table_class,
            partition_key_name=partition_key_name,
            partition_key_type=partition_key_type
        )
        logger.info("Table created successfully in Lambda")
        return response
    except Exception as e:
        logger.error(f"Error creating table in Lambda: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


if __name__ == "__main__":
    try:
        logger.info("Running locally")
        response = create_dynamodb_table(
            name_shortcut="fika",
            table_name="product",
            billing_mode="PAY_PER_REQUEST",
            table_class="STANDARD_INFREQUENT_ACCESS",
            partition_key_name="ProductID",
            partition_key_type="S"
        )
        logger.info(f"Local execution result: {response}")
    except Exception as e:
        logger.error(f"Error during local execution: {str(e)}")
