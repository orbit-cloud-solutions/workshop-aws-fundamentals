import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wksp-kavr-dynamodb-product-table')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])
        for item in items:
            print(item)
            item['Price'] = float(item['Price'])
        return {
            'statusCode': 200,
            'body': json.dumps(items),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                'Access-Control-Allow-Headers': '*'
            }
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }