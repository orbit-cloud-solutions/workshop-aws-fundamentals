import json
import boto3  # AWS SDK for Python
import uuid   # For generating unique identifiers
import os     # For accessing environment variables
from datetime import datetime
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
    Creates a new product in DynamoDB.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format from API Gateway:
    {
        "body": {
            "ProductName": "Test Product",  # Required - Name of the product
            "Price": 99.99                  # Required - Price of the product
        }
    }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 400, or 500)
            - body: JSON string containing either:
                - success: Created product details including generated ID
                - error: Error message
    """
    # Log incoming event
    logger.info(f"Incoming event: {json.dumps(event)}")

    try:
        # Parse the body from API Gateway event
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        logger.info(f"Request body: {json.dumps(body)}")

        # Generate a unique identifier for the product
        # uuid4() creates a random UUID which practically ensures uniqueness
        product_id = str(uuid.uuid4())
        
        # Get current UTC timestamp in ISO format
        # We store both creation and update times for audit purposes
        timestamp = datetime.utcnow().isoformat()
        
        # Prepare the item to be inserted into DynamoDB
        # Note: DynamoDB requires Decimal type for numbers instead of float
        item = {
            'ProductID': product_id,                # Unique identifier
            'ProductName': body['ProductName'],     # Product name from request
            'Price': Decimal(str(body['Price'])),   # Convert price to Decimal
            'CreatedAt': timestamp,                 # Creation timestamp
            'UpdatedAt': timestamp                  # Initial update timestamp
        }
        
        logger.info(f"Attempting to create product with ID: {product_id}")
        
        # Insert the item into DynamoDB
        # put_item will overwrite any existing item with the same key
        table.put_item(Item=item)
        
        # Return successful response with created item details
        # default=str handles datetime and Decimal serialization
        result = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Product created successfully',
                'productId': product_id,
                'product': item
            }, default=str)
        }
        logger.info(f"Product created successfully: {product_id}")
        return result
    
    except KeyError as e:
        # Return 400 if required fields are missing
        # KeyError will include the name of the missing field
        error_msg = f'Missing required field: {str(e)}'
        logger.warning(error_msg)
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': error_msg
            })
        }
    except json.JSONDecodeError as e:
        # Handle invalid JSON in the request body
        error_msg = 'Invalid JSON in request body'
        logger.warning(f"{error_msg}: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': error_msg
            })
        }
    except Exception as e:
        # Catch all other errors (e.g., DynamoDB errors, permission issues)
        # Return 500 with the error message for debugging
        error_msg = f'Error creating product: {str(e)}'
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': error_msg
            })
        }