import json
import uuid
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    ProductID = body.get('ProductID', None)
    ProductName = body.get('ProductName')
    Price = body.get('Price')
    CreatedAt = body.get('CreatedAt', None)
    UpdatedAt = body.get('UpdatedAt', None)
    print(ProductID)
    
    
    if not ProductID:
        ProductID = str(uuid.uuid4())
    
    if not CreatedAt:
        CreatedAt = datetime.utcnow().isoformat()
    if not UpdatedAt:
        UpdatedAt = datetime.utcnow().isoformat()
    
    item = {
        'ProductID': ProductID,
        'ProductName': ProductName,
        'Price': Price,
        'CreatedAt': CreatedAt,
        'UpdatedAt': UpdatedAt
    }
    
    try:
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Product created successfully',
                'ProductID': ProductID
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                'Access-Control-Allow-Headers': '*'
            }
        }
    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to create product',
                'error': str(e)
            })
        }
