import boto3
import logging
import os
from botocore.exceptions import BotoCoreError, ClientError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

ddb_client = boto3.client('dynamodb', 'eu-central-1')

def create_dynamodb_table(full_table_name, billing_mode="PAY_PER_REQUEST", 
                          table_class="STANDARD_INFREQUENT_ACCESS", partition_key_name="ProductID", 
                          partition_key_type="S"):
    """
    Function to create a DynamoDB table using Boto3.

    Parameters:
        full_table_name (str): Full name of the DynamoDB table.
        billing_mode (str): Billing mode for the table (PROVISIONED or PAY_PER_REQUEST).
        table_class (str): Class of the DynamoDB table (STANDARD or STANDARD_INFREQUENT_ACCESS).
        partition_key_name (str): Name of the partition key (primary key).
        partition_key_type (str): Data type of the partition key (S, N, B).

    Returns:
        dict: Response from the `create_table` call.
    """
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

def delete_dynamodb_table(full_table_name):
    """
    Function to delete a DynamoDB table using Boto3.

    Parameters:
        full_table_name (str): Full name of the DynamoDB table.

    Returns:
        dict: Response from the `delete_table` call.
    """
    logger.info(f"Deleting DynamoDB table: {full_table_name}")

    try:
        response = ddb_client.delete_table(
            TableName=full_table_name
        )
        logger.info(f"Successfully initiated deletion of table: {full_table_name}")
        return response
    except (ClientError, BotoCoreError) as e:
        logger.error(f"Failed to delete table: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

def lambda_handler(event, context):
    """
    AWS Lambda handler to create or delete a DynamoDB table.

    Parameters:
        event (dict): Input parameters passed to the Lambda function.
        context (LambdaContext): Lambda runtime information.

    Returns:
        dict: Response from the DynamoDB table operation.

    Event example:
        {
            "Action": "CREATE",  # or "DELETE"
            "NameShortcut": "fika",
            "TableName": "product",
            "BillingMode": "PAY_PER_REQUEST",
            "TableClass": "STANDARD_INFREQUENT_ACCESS",
            "PartitionKeyName": "ProductID",
            "PartitionKeyType": "S"
        }
    """
    logger.info("Lambda function invoked")

    action = event.get("Action", "CREATE").upper()
    name_shortcut = event.get("NameShortcut", "fika")
    table_name = event.get("TableName", "product")
    full_table_name = f"wksp-{name_shortcut}-dynamodb-{table_name}-table-sdk"

    try:
        if action == "CREATE":
            billing_mode = event.get("BillingMode", "PAY_PER_REQUEST")
            table_class = event.get("TableClass", "STANDARD_INFREQUENT_ACCESS")
            partition_key_name = event.get("PartitionKeyName", "ProductID")
            partition_key_type = event.get("PartitionKeyType", "S")

            response = create_dynamodb_table(
                full_table_name=full_table_name,
                billing_mode=billing_mode,
                table_class=table_class,
                partition_key_name=partition_key_name,
                partition_key_type=partition_key_type
            )
            logger.info("Table created successfully in Lambda")
        elif action == "DELETE":
            response = delete_dynamodb_table(
                full_table_name=full_table_name
            )
            logger.info("Table deletion initiated successfully in Lambda")
        else:
            raise ValueError(f"Invalid Action specified: {action}")

        return 'OK'
    except Exception as e:
        logger.error(f"Error in Lambda function: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

if __name__ == "__main__":
    try:
        logger.info("Running locally")
        test_event = {
            "Action": "CREATE",  # Change to "DELETE" for deletion
            "NameShortcut": "fika",
            "TableName": "product",
            "BillingMode": "PAY_PER_REQUEST",
            "TableClass": "STANDARD_INFREQUENT_ACCESS",
            "PartitionKeyName": "ProductID",
            "PartitionKeyType": "S"
        }
        response = lambda_handler(test_event, None)
        logger.info(f"Local execution result: {response}")
    except Exception as e:
        logger.error(f"Error during local execution: {str(e)}")
