import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wksp-kavr-dynamodb-product-table')

def lambda_handler(event, context):
    ProductID = event['pathParameters']['ProductID']
    
    try:
        response = table.delete_item(
            Key={
                'ProductID': ProductID
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Product with ProductID {ProductID} deleted successfully.'
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
                'message': 'Failed to delete product',
                'error': str(e)
            })
        }
