import sys
def handler(event, context):
    print("* running lambda handler *")
    return 'Hello from AWS Lambda using Python ' + sys.version + '!'        
