import json
import boto3  # AWS SDK for Python
import os     # For accessing environment variables
from decimal import Decimal  # Required for DynamoDB number fields
import logging  # For structured logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Retrieve table name from Lambda environment variables
# This allows us to reuse the same code across different environments (dev, staging, prod)
TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# Initialize the DynamoDB resource
# We use resource instead of client for a more Pythonic interface
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Retrieves a product from DynamoDB by its ID.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format from API Gateway:
    Either:
        {
            "queryStringParameters": {
                "ProductID": "123..."  # ProductID as query parameter
            }
        }
    Or:
        {
            "pathParameters": {
                "ProductID": "123..."  # ProductID as path parameter
            }
        }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 404, 400, or 500)
            - body: JSON string containing either:
                - success: Complete product details
                - error: Error message or not found message
    """
    # Log incoming event
    logger.info(f"Incoming event: {json.dumps(event)}")

    try:
        # Check path parameters first (/{ProductID})
        path_parameters = event.get('pathParameters', {})
        if path_parameters and 'ProductID' in path_parameters:
            product_id = path_parameters['ProductID']
            logger.info(f"Found ProductID in path parameters: {product_id}")
        
        # If not in path, check query parameters (?ProductID=123)
        else:
            query_parameters = event.get('queryStringParameters', {})
            if not query_parameters or 'ProductID' not in query_parameters:
                logger.warning("ProductID not found in path or query parameters")
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'message': 'Missing ProductID in request'
                    })
                }
            product_id = query_parameters['ProductID']
            logger.info(f"Found ProductID in query parameters: {product_id}")
        
        # Attempt to retrieve the item from DynamoDB
        # get_item is the most efficient way to retrieve a single item by its primary key
        response = table.get_item(
            Key={
                'ProductID': product_id
            }
        )
        
        # Check if the item was found
        # DynamoDB returns the item in the 'Item' key if found
        if 'Item' in response:
            result = {
                'statusCode': 200,
                'body': json.dumps(response['Item'], default=str)
            }
            logger.info(f"Product found: {product_id}")
            return result
        
        # If we get here, no item was found with the given ProductID
        # Return a 404 Not Found response
        logger.info(f"Product not found: {product_id}")
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': f'Product with ID {product_id} not found'
            })
        }
    
    except Exception as e:
        # Catch all other errors (e.g., DynamoDB errors, permission issues)
        logger.error(f"Error retrieving product: {str(e)}")
        # Return 500 with the error message for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error retrieving product: {str(e)}'
            })
        }