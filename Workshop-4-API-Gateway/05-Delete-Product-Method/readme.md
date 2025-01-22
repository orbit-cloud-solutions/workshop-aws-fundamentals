# Exercise 5 - Delete Product Method

## Configure DELETE method
    * Select /products/{productId} resource
    * Create DELETE method:
        * Integration type: Lambda Function
        * Lambda Function: wksp-{NameShortcut}-delete-product
        * Use Lambda Proxy integration: Yes
    * Configure method request:
        * API Key Required: true
        * URL path parameters: productId
    * Configure integration request:
        * Verify proxy settings
    * Test method:
        * Use path parameter: productId = "123"