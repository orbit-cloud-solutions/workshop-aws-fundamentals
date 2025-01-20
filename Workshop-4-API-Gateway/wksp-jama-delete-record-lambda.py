import json
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Retrieve table name from Lambda environment variables
TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Deletes a product from DynamoDB by its ID.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format from API Gateway:
    {
        "pathParameters": {
            "ProductID": "123..."  # Required - The unique identifier of the product to delete
        }
    }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 404, 400, or 500)
            - body: JSON string containing either:
                - success: Deletion confirmation message
                - error: Error message
    """
    logger.info(f"Incoming event: {json.dumps(event)}")

    try:
        # Get ProductID from path parameters
        if not event.get('pathParameters') or 'ProductID' not in event['pathParameters']:
            logger.warning("No ProductID found in path parameters")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing ProductID in path'})
            }
        
        product_id = event['pathParameters']['ProductID']
        logger.info(f"Attempting to delete product: {product_id}")

        # Attempt to delete the item
        # Use ReturnValues to get the deleted item's attributes
        response = table.delete_item(
            Key={'ProductID': product_id},
            ReturnValues='ALL_OLD'  # This will return the deleted item's attributes
        )
        
        # Check if item was found and deleted
        if 'Attributes' not in response:
            logger.warning(f"Product {product_id} not found")
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': f'Product with ID {product_id} not found'
                })
            }
        
        logger.info(f"Successfully deleted product: {product_id}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Product deleted successfully',
                'deletedProduct': response['Attributes']
            }, default=str)
        }

    except Exception as e:
        error_msg = f'Error deleting product: {str(e)}'
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': error_msg})
        }