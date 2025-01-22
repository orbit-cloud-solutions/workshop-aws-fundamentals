# Exercise 3 - Get Product Method

## Configure GET method
    * Select /products/{productId} resource
    * Create GET method:
        * Integration type: Lambda Function
        * Lambda Function: wksp-{NameShortcut}-get-product
        * Use Lambda Proxy integration: Yes
    * Configure method request:
        * API Key Required: true
        * URL path parameters: productId
    * Configure integration request:
        * Verify proxy settings
    * Test method:
        * Use path parameter: productId = "123"