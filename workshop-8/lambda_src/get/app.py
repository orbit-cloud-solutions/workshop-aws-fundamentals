import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wksp-kavr-dynamodb-product-table')

def lambda_handler(event, context):
    print(event)
    pathParameters = event['pathParameters']
    product_id = pathParameters.get('ProductID')
    
    if not product_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'ProductID is required'})
        }

    try:
        response = table.get_item(Key={'ProductID': product_id})
        
        if 'Item' in response:
            response['Item']['Price'] = float(response['Item']['Price'])
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item']),
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Product not found'})
            }
    
    except ClientError as e:
        # Pokud nastane chyba při volání DynamoDB
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error fetching product: {str(e)}'})
        }
