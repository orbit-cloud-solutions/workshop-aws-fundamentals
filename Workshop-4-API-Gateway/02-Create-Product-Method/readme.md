# Exercise 2 - Create Product Method

## Create POST method
    * Select /products resource
    * Create POST method:
        * Integration type: Lambda Function
        * Lambda Function: wksp-{NameShortcut}-create-product
        * Use Lambda Proxy integration: Yes
    * Configure method request:
        * API Key Required: true
    * Configure integration request:
        * Verify proxy settings
    * Test method:
        * Use test payload: { "ProductName": "Test Product", "Price": 99.99 }