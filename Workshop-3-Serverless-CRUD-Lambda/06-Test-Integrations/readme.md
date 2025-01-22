# Exercise 5 - Delete Product Lambda

## Create Lambda function
    * Create new Lambda function:
    * Name: wksp-{NameShortcut}-delete-product
    * Runtime: Python 3.13
    * Configure permissions:
        * Add DynamoDB permissions to execution role
    * Paste the code attached
    * Create the environment variable DYNAMODB_TABLE_NAME with the name of your table
    * Test function:
        * Input format: { "ProductID": "123" }
        * Verify item deletion from DynamoDB