import json
import boto3
import os
from decimal import Decimal
from datetime import datetime
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
    Updates a product in DynamoDB by ProductID.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format from API Gateway:
    {
        "pathParameters": {
            "ProductID": "123..."             # Required - The unique identifier of the product
        },
        "body": {                            # Required - The fields to update
            "ProductName": "Updated Name",    # Optional - New name for the product
            "Price": 199.99                  # Optional - New price for the product
        }
    }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 400, or 500)
            - body: JSON string containing either:
                - success: Updated product attributes
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
        logger.info(f"Updating product: {product_id}")

        # Check for missing or empty body
        if not event.get('body'):
            logger.warning("Request body is missing or empty")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Request body is required'})
            }

        # Parse the body
        try:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON body")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid JSON in request body'})
            }

        # Check if body is empty object
        if not body:
            logger.warning("Request body is empty object")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Request body cannot be empty'})
            }

        logger.info(f"Update payload: {json.dumps(body)}")

        # Initialize update expression
        update_expr = ['SET UpdatedAt = :timestamp']
        expr_values = {':timestamp': datetime.utcnow().isoformat()}
        
        # Add ProductName to update if provided
        if 'ProductName' in body:
            update_expr.append('ProductName = :name')
            expr_values[':name'] = body['ProductName']
            
        # Add Price to update if provided
        if 'Price' in body:
            update_expr.append('Price = :price')
            expr_values[':price'] = Decimal(str(body['Price']))

        # Check if there are any fields to update
        if len(update_expr) == 1:  # Only UpdatedAt is present
            logger.warning("No valid update fields provided")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'No valid fields to update provided'})
            }

        # Perform update
        response = table.update_item(
            Key={'ProductID': product_id},
            UpdateExpression=', '.join(update_expr),
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        
        logger.info(f"Successfully updated product {product_id}")
        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'], default=str)
        }

    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error updating product: {str(e)}'})
        }