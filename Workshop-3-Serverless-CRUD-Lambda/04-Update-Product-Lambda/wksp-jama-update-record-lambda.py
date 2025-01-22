import json
import boto3
import os
from decimal import Decimal
from datetime import datetime

# Retrieve table name from Lambda environment variables
# This allows us to reuse the same code across different environments (dev, staging, prod)
TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# Initialize the DynamoDB resource
# We use resource instead of client for a more Pythonic interface
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Updates a product in DynamoDB by ProductID.
    
    Required environment variables:
    - DYNAMODB_TABLE_NAME: Name of the DynamoDB table
    
    Expected event format:
    {
        "ProductID": "123...",            # Required - The unique identifier of the product
        "ProductName": "Updated Name",    # Optional - New name for the product
        "Price": 199.99                   # Optional - New price for the product
    }
    
    Returns:
        dict: Response object containing:
            - statusCode: HTTP status code (200, 400, or 500)
            - body: JSON string containing either:
                - success: Updated product attributes
                - error: Error message
    """
    try:
        # Extract the ProductID from the event
        # This will raise KeyError if ProductID is missing
        product_id = event['ProductID']
        
        # Initialize the update expression parts
        # UpdateExpression is built dynamically based on what fields are being updated
        # We always update the UpdatedAt timestamp for audit purposes
        update_expr = ['SET UpdatedAt = :timestamp']
        expr_values = {':timestamp': datetime.utcnow().isoformat()}
        
        # If ProductName is provided, add it to the update expression
        # This makes the update operation flexible - you can update just the name
        if 'ProductName' in event:
            update_expr.append('ProductName = :name')
            expr_values[':name'] = event['ProductName']
            
        # If Price is provided, add it to the update expression
        # Convert the price to Decimal as DynamoDB doesn't support float
        if 'Price' in event:
            update_expr.append('Price = :price')
            expr_values[':price'] = Decimal(str(event['Price']))
        
        # Perform the update operation
        # - UpdateExpression: Tells DynamoDB what fields to update
        # - ExpressionAttributeValues: Provides the values for the update
        # - ReturnValues='ALL_NEW': Returns the item's new state after the update
        response = table.update_item(
            Key={'ProductID': product_id},
            UpdateExpression=', '.join(update_expr),  # Combine all updates into single expression
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'  # Returns the item with all its attributes after the update
        )
        
        # Return successful response with updated item
        # default=str handles datetime and Decimal serialization
        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'], default=str)
        }
    
    except KeyError:
        # Return 400 if ProductID is missing from the request
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing ProductID'})
        }
    except Exception as e:
        # Catch all other errors (e.g., DynamoDB errors, permission issues)
        # Return 500 with the error message for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error updating product: {str(e)}'})
        }