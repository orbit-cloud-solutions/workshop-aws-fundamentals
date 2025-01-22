# Exercise 2 - Create Product Lambda

## Create Lambda function
    * Create new Lambda function:
    * Name: wksp-{NameShortcut}-create-product
    * Runtime: Python 3.13
    * Configure permissions:
        * Add DynamoDB permissions to execution role
    * Paste the code attached
    * Create the environment variable DYNAMODB_TABLE_NAME with the name of your table
    * Test function:
        * Input format: { "ProductName": "Test Product", "Price": 99.99 }
        * Verify ProductID generation
        * Confirm DynamoDB storage