import json
import boto3  # AWS SDK for Python
import os     # For accessing environment variables
from decimal import Decimal  # Required for DynamoDB number fields

# Retrieve table name from Lambda environment variables
# This allows us to reuse the same code across different environments (dev, staging, prod)
TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# Initialize the DynamoDB resource
# We use resource instead of client for a more Pythonic interface
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Deletes a product from DynamoDB by its ID.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format:
    {
        "ProductID": "123e4567-e89b-12d3-a456-426614174000"  # Required - Unique identifier of the product to delete
    }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 404, 400, or 500)
            - body: JSON string containing either:
                - success: Deleted product details
                - error: Error message or not found message
    """
    try:
        # Extract the ProductID from the event
        # This will raise KeyError if ProductID is missing
        product_id = event['ProductID']
        
        # Attempt to delete the item from DynamoDB
        # ReturnValues='ALL_OLD' returns the item as it appeared before deletion
        response = table.delete_item(
            Key={
                'ProductID': product_id
            },
            ReturnValues='ALL_OLD'  # This allows us to return the deleted item's details
        )
        
        # Check if an item was actually deleted
        # If 'Attributes' exists in response, it means an item was found and deleted
        if 'Attributes' in response:
            # Return success response with the deleted item's details
            # default=str handles datetime and Decimal serialization
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Product deleted successfully',
                    'deletedProduct': response['Attributes']
                }, default=str)
            }
        
        # If we get here, no item was found with the given ProductID
        # Return a 404 Not Found response
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': f'Product with ID {product_id} not found'
            })
        }
    
    except KeyError:
        # Return 400 if ProductID is missing from the request
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing ProductID in request'
            })
        }
    except Exception as e:
        # Catch all other errors (e.g., DynamoDB errors, permission issues)
        # Return 500 with the error message for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error deleting product: {str(e)}'
            })
        }