# Exercise 4 - Update Product Lambda

## Create Lambda function
    * Create new Lambda function:
    * Name: wksp-{NameShortcut}-update-product
    * Runtime: Python 3.13
    * Configure permissions:
        * Add DynamoDB permissions to execution role
    * Paste the code attached
    * Create the environment variable DYNAMODB_TABLE_NAME with the name of your table
    * Test function:
        * Input format: { "ProductID": "123", "ProductName": "Updated Name", "Price": 199.99 }
        * Verify item update in DynamoDB